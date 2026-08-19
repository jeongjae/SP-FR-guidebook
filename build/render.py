#!/usr/bin/env python3
"""페이지 렌더러 — 콘텐츠 모델에서 사이트를 만든다.

여기 있는 함수는 model.py 의 엔티티만 읽는다. 마크다운을 정규식으로 긁지
않고, 빌드 산출물을 다시 파싱하지도 않는다. 그 두 가지가 이전 파이프라인이
"문서를 웹으로 변환한 것"처럼 보였던 이유였다.

축은 목록을 맡고 본문을 갖지 않는다.

    Day    = 실행의 정본. 시간표·이동·예약·Plan B 가 여기에만 있다.
    Region = 탐색과 이해. Day 시간표를 복제하지 않는다.
    Place  = 장문의 정본. Region 과 Day 는 참조만 한다.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
from urllib.parse import quote
from datetime import date
from pathlib import Path

import markdown as md_lib

import md_tidy

import icons
import model
from model import Day, Place, Region, Trip
from shell import (GRADE_BADGE, SITE_TITLE, alert, badge, esc, ic, page,
                   redirect, sec_head, tabs_strip)

ROOT = Path(__file__).resolve().parent.parent
# 출력 경로. SPFR_SITE_DIR 로 바꿀 수 있다 — 같은 워크트리에서 다른 빌드가
# 동시에 돌 때 서로의 산출물을 지우지 않게 하기 위한 것이다.
SITE = Path(os.environ.get("SPFR_SITE_DIR") or (ROOT / "site"))
ASSETS = ROOT / "build" / "assets"
IMAGE_MANIFEST = ROOT / "data" / "images" / "image-manifest.json"
TRACKER_XLSX = ROOT / "source" / "OPERATIONS" / "TP_Europe_Travel_Master_Tracker_v1.2.xlsx"

SEARCH_INDEX: list[dict] = []

# 지도 키는 환경에서 온다 (CI 시크릿). 없으면 지도 없이 목록만 남는다 —
# 로컬 빌드가 키 때문에 막히지 않게 한다.
MAPS_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "").strip()
MAPS_ID = os.environ.get("GOOGLE_MAPS_MAP_ID", "").strip()
IMAGES: dict = {}

# 어휘표. daily-cards 가 쓰는 값을 화면 말로 옮긴다.
#
# 여기 없는 값이 들어오면 빌드를 세운다 (check_vocabulary). 조용히 넘기면
# 한국어 화면에 영어 코드가 그대로 새고, 더 나쁘게는 'unconfirmed' 같은
# 미확정 표시가 확정처럼 보인다.
CAT_ICON = {
    "culture": "book", "sight": "pin", "food": "food", "cafe": "food",
    "hotel": "stay", "transport": "train", "activity": "gauge",
    "shopping": "pin",
}
MODE_ICON = {
    "walk": "pin", "metro": "train", "tram": "train", "bus": "train",
    "train": "train", "drive": "car", "car": "car", "flight": "plane",
    "taxi": "car", "unconfirmed": "alert",
}
MODE_LABEL = {
    "walk": "도보", "metro": "지하철", "tram": "트램", "bus": "버스",
    "train": "기차", "drive": "운전", "car": "운전", "flight": "비행",
    "taxi": "택시",
    # 이동수단이 아직 안 정해진 구간. 확정처럼 보이면 안 된다.
    "unconfirmed": "이동수단 미정",
}
FACT_LABEL = {
    "hours": "운영시간", "closed": "휴무", "price_adult": "요금",
    "price_range": "가격대", "booking": "예약", "getting_there": "가는 법",
    "duration": "소요시간", "note": "메모",
}


SEP_ROW = re.compile(r"^\s*\|?[\s:|-]*-{2,}[\s:|-]*\|?\s*$")


def _cells(line: str) -> list[str]:
    row = line.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [c.strip() for c in row.split("|")]


def _inline(text: str) -> str:
    """셀 안의 굵게·링크만 변환한다. 문단 태그는 벗긴다."""
    out = md_lib.markdown(text, extensions=["attr_list"]).strip()
    if out.startswith("<p>") and out.endswith("</p>"):
        out = out[3:-4]
    return out


def headerless_tables(text: str) -> tuple[str, dict[str, str]]:
    """헤더 없는 파이프 표를 직접 HTML 로 만든다.

    마크다운 표는 헤더 행과 구분선이 있어야 표로 읽힌다. 원고에는 둘 없이
    데이터 행만 있는 표가 있고(Barcelona·Paris), Aix 는 구분선만 있고 헤더가
    없다. 그대로 두면 파이프가 글자로 나와 화면이 깨진다.

    첫 행을 헤더로 승격시키지 않는다 — 'Essential' 은 열 이름이 아니라 값이다.
    없는 열 이름을 지어내느니 헤더 없는 표로 둔다.
    """
    lines = text.splitlines()
    parts, holes, i, n = [], {}, 0, 0
    while i < len(lines):
        if not lines[i].lstrip().startswith("|"):
            parts.append(lines[i])
            i += 1
            continue
        j = i
        while j < len(lines) and lines[j].lstrip().startswith("|"):
            j += 1
        block = lines[i:j]
        # 제대로 된 표(2행이 구분선)는 마크다운에게 맡긴다
        if len(block) >= 2 and SEP_ROW.match(block[1]):
            parts.extend(block)
            i = j
            continue
        rows = [b for b in block if not SEP_ROW.match(b)]
        if len(rows) < 2:
            parts.extend(block)
            i = j
            continue
        body = "".join(
            "<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in _cells(r)) + "</tr>"
            for r in rows)
        key = f"@@TABLE{n}@@"
        holes[key] = f'<div class="table-wrap"><table><tbody>{body}</tbody></table></div>'
        # 빈 줄로 감싼다. 표 뒤에 --- 가 오는 원고가 있는데, 그러면 마크다운이
        # 바로 앞 줄(자리표시자)을 제목으로 읽어 표가 <h2> 안에 들어간다.
        parts += ["", key, ""]
        n += 1
        i = j
    return "\n".join(parts), holes


def md(text: str) -> str:
    if not text.strip():
        return ""
    # 표 앞뒤를 빈 줄로 가른다. 원고는 사람이 쓴 것이라 표 바로 뒤에 문장이
    # 붙어 있는 곳이 많고, 그러면 그 문장이 표의 한 행으로 빨려 들어가
    # 열 너비가 문장 길이만큼 늘어난다.
    #
    # 승격 단계가 아니라 여기서 한다. 장소 장문(30_Places)은 이제 손으로
    # 관리하는 정본이라 빌드가 고쳐 쓰지 않는다 — 원고는 쓴 대로 두고
    # 렌더가 방어한다.
    text = md_tidy.tidy(text)
    text, holes = headerless_tables(text)
    html_out = md_lib.markdown(
        text, extensions=["tables", "fenced_code", "sane_lists", "attr_list"])
    # 표는 감싸서 그 안에서만 가로 스크롤시킨다 — 본문이 가로로 흐르면 안 된다
    html_out = re.sub(r"<table>", '<div class="table-wrap"><table>',
                      html_out).replace("</table>", "</table></div>")
    for key, block in holes.items():
        html_out = html_out.replace(f"<p>{key}</p>", block).replace(key, block)
    return html_out


LAYER_LABEL = {"role": "여행 전체에서의 역할", "rhythm": "추천 체류 리듬"}

FACTS: dict = {}   # slug → {key: Fact}. load_facts() 가 채운다.

FACT_TOKEN = re.compile(r"\{\{fact:([a-z0-9-]+)\.([a-z_]+)\}\}")


def resolve_fact(match: "re.Match") -> str:
    """{{fact:<장소>.<항목>}} 을 실제 값으로 바꾼다.

    값을 감추지 않는다. 확인된 값 76곳을 전부 '확인 필요' 로 덮고 있었는데,
    그건 규칙 3 을 반대 방향으로 어긴 것이다 — 아는 것을 모른다고 쓰면
    현장에서 쓸 수 있는 정보를 버린다.

    다만 확정되지 않은 값에는 반드시 표시를 붙인다. 요금·운영시간을
    확정으로 믿고 움직이는 것이 이 프로젝트 최악의 사고다.
    """
    slug, key = match.group(1), match.group(2)
    fact = (FACTS.get(slug) or {}).get(key)
    if fact is None or not fact.value:
        reason = fact.blocked_reason if fact and fact.blocked_reason else "확인 필요"
        return f"({esc(reason)})"
    if fact.is_confirmed:
        return esc(fact.value)
    return f"{esc(fact.value)} (재확인)"


# 원고에 남아 있는 옛 주소. 승격된 본문이 그대로 들고 오면 링크가 깨진다.
LEGACY_LINK = re.compile(
    r"\((?:\.\./)*(chapters/([a-z]+)/[a-z-]+\.html|topics/[a-z-]+\.html"
    r"|tracker/[a-z-]+\.html|regions\.html|daily/index\.html)([^)]*)\)")


def _relink(m: "re.Match") -> str:
    """옛 주소를 새 IA 로 옮긴다. 리다이렉트가 있긴 하지만 본문 링크가
    한 번 더 튕기게 두지 않는다 — 오프라인에서는 그 왕복이 실패한다."""
    target, region = m.group(1), m.group(2)
    if target.startswith("chapters/") and region:
        return f"(../guide/{region}.html{m.group(3)})"
    if target.startswith("tracker/"):
        return f"(../prepare/index.html{m.group(3)})"
    return f"(../guide/index.html{m.group(3)})"


def strip_tokens(text: str) -> str:
    """원고의 토큰을 사람이 읽는 형태로 바꾼다."""
    text = LEGACY_LINK.sub(_relink, text)
    text = re.sub(r"\{\{grade:[^}]*\}\}", "", text)
    text = re.sub(r"\{\{badge:[^|}]*\|([^}]*)\}\}", r"(\1)", text)
    text = re.sub(r"\{\{badge:([^}]*)\}\}", r"(\1)", text)
    text = FACT_TOKEN.sub(resolve_fact, text)
    return re.sub(r"\{\{[^}]*\}\}", "", text)


# 글자로만 있는 URL 을 누를 수 있게 만든다.
#
# 사실 출처(place-facts 의 source) 286건이 전부 맨 URL 이라 화면에 글자로만
# 나왔다. 현장에서 "운영시간이 맞나" 를 확인하려면 그 주소를 손으로 옮겨
# 적어야 했다는 뜻이다. 확인할 수 없는 근거는 근거가 아니다.
URL_IN_TEXT = re.compile(r'https?://[^\s<>"\')\]]+')


def domain_of(url: str) -> str:
    """보여줄 이름. 전체 주소는 390px 에서 서너 줄을 먹고 읽히지도 않는다."""
    host = url.split("//", 1)[-1].split("/", 1)[0]
    return host[4:] if host.startswith("www.") else host


def linkify(text: str, *, show: str = "domain") -> str:
    """**이스케이프된** 문자열 안의 맨 URL 을 <a> 로 바꾼다.

    이스케이프를 먼저 하고 여기 넣어야 한다. 순서를 뒤집으면 우리가 만든
    태그가 다시 이스케이프돼 글자로 나온다.
    """
    def repl(m):
        raw = m.group(0)
        url = raw.rstrip(".,·;")
        tail = raw[len(url):]
        shown = domain_of(url) if show == "domain" else url
        return (f'<a href="{url}" rel="nofollow noopener">{shown}</a>{tail}')
    return URL_IN_TEXT.sub(repl, text)


def first_source_url(place) -> str:
    """이 장소의 근거 URL 하나. 공식 페이지인 경우가 대부분이라 상단
    행동줄에 '공식 정보' 로 내보낸다 — 현장에서 눌러 지금 값을 확인한다."""
    for key in ("booking", "hours", "price_adult", "closed", "getting_there"):
        f = place.facts.get(key)
        if f and f.source:
            m = URL_IN_TEXT.search(f.source)
            if m:
                return m.group(0).rstrip(".,·;")
    return ""


# ---------------------------------------------------------------- 이미지

def load_image_index() -> dict:
    if not IMAGE_MANIFEST.exists():
        return {"by_place": {}, "heroes": {}}
    raw = json.loads(IMAGE_MANIFEST.read_text(encoding="utf-8"))
    by_place, heroes = {}, {}
    for img in raw.get("images", []):
        pid = img.get("placeId")
        if pid and pid not in by_place:
            by_place[pid] = img
        if img.get("regionHero") and img.get("region"):
            heroes.setdefault(img["region"], img)
    return {"by_place": by_place, "heroes": heroes}


def img_src(img: dict, role: str, rel: str) -> tuple[str, str]:
    """(src, srcset). 카탈로그에 없는 이미지는 애초에 여기 오지 않는다."""
    variants = (img.get("variants") or {}).get(role) or []
    if not variants:
        for other in ("content", "hero", "thumbnail"):
            variants = (img.get("variants") or {}).get(other) or []
            if variants:
                break
    if not variants:
        return "", ""
    ordered = sorted(variants, key=lambda v: v.get("width", 0))
    src = f"{rel}/{ordered[-1]['sitePath']}"
    srcset = ", ".join(f"{rel}/{v['sitePath']} {v['width']}w" for v in ordered)
    return src, srcset


def figure(img: dict | None, rel: str, role: str = "content",
           cls: str = "", sizes: str = "100vw") -> str:
    """사진. 카탈로그에 항목이 없으면 자리를 아예 만들지 않는다.

    저작자 표시가 필요한 라이선스는 화면에 표시한다 — 이 사이트는 공개
    배포되므로 표시 의무가 실제로 발생한다.
    """
    if not img:
        return ""
    src, srcset = img_src(img, role, rel)
    if not src:
        return ""
    alt = esc(img.get("altKo") or img.get("titleKo") or "")
    ss = f' srcset="{srcset}" sizes="{sizes}"' if srcset else ""
    return (f'<img class="{cls}" src="{src}"{ss} alt="{alt}" '
            f'loading="lazy" decoding="async">')


def credit_line(img: dict | None) -> str:
    if not img:
        return ""
    who = esc(img.get("creator") or "")
    lic = esc(img.get("license") or "")
    src = img.get("sourcePage") or ""
    if not (who or lic):
        return ""
    link = f'<a href="{esc(src)}" rel="nofollow noopener">{who}</a>' if src else who
    return f'<p class="meta">사진 {link} · {lic}</p>'


# ---------------------------------------------------------------- 컴포넌트

def place_card(p: Place, rel: str, large: bool = False) -> str:
    """PlaceCard. 목록에서는 이 형태 하나만 쓴다 — 페이지마다 카드를 새로
    만들면 사이트가 조각난다."""
    img = IMAGES["by_place"].get(p.slug)
    grade = GRADE_BADGE.get(p.grade or "")
    grade_html = badge(*grade) if grade else ""
    url = f"{rel}/places/{p.slug}.html"

    if large:
        thumb = figure(img, rel, "content", "thumb", "(min-width:600px) 50vw, 100vw")
        return f"""<article class="card place-card-lg">
  {thumb}
  <div class="card-body">
    <div class="metarow">{grade_html}</div>
    <h3 class="card-title"><a class="card-link" href="{url}">{esc(p.name)}</a></h3>
    <p class="card-dek">{esc(p.summary)}</p>
  </div>
</article>"""

    thumb = figure(img, rel, "thumbnail", "thumb", "84px")
    return f"""<article class="card place-card">
  {thumb}
  <div class="card-body" style="padding:0">
    <h3 class="card-title"><a class="card-link" href="{url}">{esc(p.name)}</a></h3>
    <p class="card-dek">{esc(p.summary)}</p>
    <div class="metarow">{grade_html}</div>
  </div>
</article>"""


def day_card(d: Day, rel: str, region: Region | None = None) -> str:
    transfer = badge("caution", "거점 이동") if d.is_transfer else ""
    fatigue = f'<span>{ic("gauge")}피로 {esc(d.fatigue)}</span>' if d.fatigue else ""
    return f"""<article class="card day-card">
  <div class="card-body">
    <div class="day-card-head">
      <span class="day-num">DAY {d.n}</span>
      <span class="day-date">{esc(d.date_label)}</span>
    </div>
    <div class="day-route"><a class="card-link" href="{rel}/{d.url}">{esc(d.city)}</a></div>
    <p class="card-dek">{esc(d.title)}</p>
    <div class="metarow">{transfer}{fatigue}</div>
  </div>
</article>"""


def timeline(d: Day, rel: str) -> str:
    """하루의 뼈대. stop 과 leg 를 순서대로 엮는다."""
    legs = {(l.frm, l.to): l for l in d.legs}
    rows, stops = [], d.stops
    for i, s in enumerate(stops):
        icon = CAT_ICON.get(s.category, "pin")
        name = esc(s.name)
        if s.place is not None:
            name = f'<a href="{rel}/places/{s.place.slug}.html">{name}</a>'
        marks = []
        if s.optional:
            marks.append(badge("neutral", "선택"))
        if s.reservation:
            marks.append(badge("caution", "예약"))
        note = f'<p class="tl-note">{esc(s.summary)}</p>' if s.summary else ""
        res = (f'<p class="tl-note">{ic("ticket")}{esc(s.reservation)}</p>'
               if s.reservation else "")
        rows.append(f"""<li class="tl-item" data-start="{esc(s.start or '')}" data-end="{esc(s.end or '')}">
  <div class="tl-time">{esc(s.start or '')}</div>
  <div class="tl-body">
    <div class="tl-name">{ic(icon)} {name} {''.join(marks)}</div>
    {note}{res}
  </div>
</li>""")
        nxt = stops[i + 1] if i + 1 < len(stops) else None
        leg = legs.get((s.id, nxt.id)) if nxt else None
        if leg:
            bits = [MODE_LABEL.get(leg.mode, leg.mode)]
            unconfirmed = leg.mode == "unconfirmed"
            if leg.duration:
                bits.append(leg.duration)
            if leg.distance:
                bits.append(leg.distance)
            if leg.line:
                bits.append(leg.line)
            cls = "tl-leg tl-leg-open" if unconfirmed else "tl-leg"
            rows.append(f"""<li class="{cls}">
  <div></div>
  <div class="tl-body"><span class="tl-leg-line">{ic(MODE_ICON.get(leg.mode, 'pin'))}
    {esc(' · '.join(bits))}</span></div>
</li>""")
    return f'<ol class="timeline">{"".join(rows)}</ol>'


def map_card(stops, rel: str, center=None, zoom: int = 14,
             label: str = "지도") -> str:
    """MapCard. 핀은 Place DB 에서만 온다 — HTML 에 좌표를 따로 박지 않는다.

    지도는 눌렀을 때만 불러온다. 43일 내내 열리는 화면마다 지도 SDK 를
    받으면 데이터가 약한 곳에서 첫 화면이 늦는다.

    JS 나 네트워크가 없어도 목록과 Google Maps 링크는 남는다. 현장에서
    스크립트가 안 뜨는 상황이 실제로 있고, 그때 좌표 링크만이라도 손에
    있어야 한다.
    """
    pins = [{"id": s.id, "name": s.name, "lat": s.lat, "lng": s.lng,
             "cat": s.category, "time": s.start,
             "address": s.address,
             "place": s.place.slug if s.place else None}
            for s in stops if (s.lat and s.lng) or s.address]
    if not pins:
        return ""
    located = [p for p in pins if p["lat"] and p["lng"]]
    if center is None:
        if not located:
            return ""
        center = [sum(p["lat"] for p in located) / len(located),
                  sum(p["lng"] for p in located) / len(located)]
    payload = json.dumps({"center": center, "zoom": zoom, "pins": located},
                         ensure_ascii=False, separators=(",", ":")) \
        .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")

    items = []
    for i, p in enumerate(pins, 1):
        name = esc(p["name"])
        if p["place"]:
            name = f'<a href="{rel}/places/{p["place"]}.html">{name}</a>'
        when = f'<span class="meta">{esc(p["time"])}</span>' if p["time"] else ""
        href = maps_url(p["lat"], p["lng"], p.get("address") or "")
        items.append(
            f'<li data-pin="{esc(p["id"])}">{when}'
            f'<span class="map-name">{name}</span>'
            f'<a class="map-open" rel="nofollow noopener" href="{esc(href)}">'
            f'{ic("map")}'
            f'<span class="visually-hidden">{esc(p["name"])} </span>열기</a></li>')

    return f"""<div class="map-card">
  <div class="map-canvas" id="map-canvas" hidden></div>
  <p class="map-status meta" id="map-status" role="status" aria-live="polite"></p>
  <script type="application/json" id="map-data">{payload}</script>
  <div class="map-card-foot">
    <span class="label">{esc(label)} · {len(pins)}곳</span>
    <div class="map-toggle" role="group" aria-label="지도와 목록 전환">
      <button type="button" data-view="map" aria-pressed="false">지도</button>
      <button type="button" data-view="list" aria-pressed="true">목록</button>
    </div>
  </div>
  <ol class="map-list" id="map-list">{"".join(items)}</ol>
</div>"""


def maps_url(lat=None, lng=None, address: str = "") -> str:
    """지도 링크. 좌표가 있으면 좌표로, 없으면 주소로 연다.

    확정 숙소인데 검증된 좌표가 없는 경우가 있다. 틀린 좌표를 남기면
    현장에서 엉뚱한 곳으로 간다 — 그게 이 프로젝트 최악의 사고다.
    주소는 확정이므로 Google 지도가 정확히 찾는다.
    """
    if lat and lng:
        return f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
    if address:
        return ("https://www.google.com/maps/search/?api=1&query="
                + quote(address))
    return ""


def index_search(title: str, url: str, kind: str, extra: str = "") -> None:
    SEARCH_INDEX.append({"t": title, "u": url, "k": kind, "x": extra})


# ================================================================ 페이지

def build_place(p: Place, trip: Trip) -> str:
    """Place — Action → Experience → Practical → Deep Guide.

    길 찾는 손이 먼저 닿아야 하는 것은 서술이 아니라 지도와 시각이다.
    긴 역사·건축 서술은 지우지 않고 아래로 내린다.
    """
    rel = ".."
    region = trip.region(p.region)
    img = IMAGES["by_place"].get(p.slug)
    grade = GRADE_BADGE.get(p.grade or "")

    # --- Action -----------------------------------------------------------
    meta = []
    if grade:
        meta.append(badge(*grade))
    dur = p.fact("duration")
    if dur and dur.is_confirmed:
        meta.append(f'<span>{ic("clock")}{esc(dur.value)}</span>')
    for n in sorted(p.days):
        d = trip.day(n)
        if d:
            meta.append(f'<a href="{rel}/{d.url}">Day {n} · {esc(d.date_label)}</a>')

    actions = []
    if p.lat and p.lng:
        actions.append(
            f'<a class="btn btn-primary" rel="nofollow noopener" '
            f'href="https://www.google.com/maps/dir/?api=1&destination={p.lat},{p.lng}">'
            f'{ic("map")}길찾기</a>')
    url_fact = p.fact("url")
    official = (url_fact.value if url_fact and url_fact.value.startswith("http")
                else first_source_url(p))
    if official:
        actions.append(f'<a class="btn btn-secondary" href="{esc(official)}" '
                       f'rel="nofollow noopener">{ic("link")}공식 정보</a>')
    if p.wiki:
        wiki_url = (f"https://{p.wiki_lang}.wikipedia.org/wiki/"
                    f"{p.wiki.replace(' ', '_')}")
        actions.append(f'<a class="btn btn-secondary" href="{esc(wiki_url)}" '
                       f'rel="nofollow noopener">{ic("book")}위키백과</a>')

    hero = ""
    if img:
        src, srcset = img_src(img, "hero", rel)
        if src:
            hero = (f'<img class="hero-img" src="{src}" srcset="{srcset}" '
                    f'sizes="100vw" alt="{esc(img.get("altKo") or p.name)}" '
                    f'fetchpriority="high" decoding="async">')

    parts = [f"""<div class="hero">
  {hero}
  <div class="hero-body"><div class="hero-card">
    <div class="hero-eyebrow"><span class="label">{esc(region.name if region else '')}</span></div>
    <h1>{esc(p.name)}</h1>
    <div class="metarow">{''.join(meta)}</div>
    {f'<p class="hero-dek">{esc(p.summary)}</p>' if p.summary else ''}
    {f'<div class="btn-row" style="margin-top:1rem">{"".join(actions)}</div>' if actions else ''}
  </div></div>
</div>
<div class="wrap-read">
{credit_line(img)}"""]

    # --- Experience -------------------------------------------------------
    if p.why_go:
        parts.append(sec_head("WHY GO", "왜 가는가", rule=True))
        parts.append(f'<div class="prose">{md(strip_tokens(p.why_go))}</div>')
    if p.dont_miss:
        parts.append(sec_head("DON'T MISS", "놓치지 말 것", rule=True))
        items = "".join(f"<li>{esc(x)}</li>" for x in p.dont_miss)
        parts.append(f'<div class="prose"><ol>{items}</ol></div>')

    # --- Practical --------------------------------------------------------
    facts = [(k, f) for k, f in p.facts.items() if f.value or f.blocked_reason]
    if facts:
        parts.append(sec_head("PRACTICAL", "실용", rule=True))
        rows = []
        for key, f in sorted(facts, key=lambda kv: list(FACT_LABEL).index(kv[0])
                             if kv[0] in FACT_LABEL else 99):
            label = FACT_LABEL.get(key, key)
            if f.is_confirmed:
                mark = ""
                value = esc(f.value)
            else:
                # 확정처럼 보이면 안 된다. 이걸 믿고 움직이는 것이 최악의 사고다.
                mark = badge("caution", "재확인")
                value = esc(f.value) if f.value else \
                    f'<span class="meta">{esc(f.blocked_reason or "미확인")}</span>'
            src = (f'<br><span class="meta">출처 {linkify(esc(f.source))}</span>'
                   if f.source else "")
            rows.append(f"<tr><th scope=\"row\">{esc(label)}</th>"
                        f"<td>{value} {mark}{src}</td></tr>")
        parts.append(f'<div class="table-wrap"><table><tbody>{"".join(rows)}'
                     f"</tbody></table></div>")
    if p.practical_md.strip():
        if not facts:
            parts.append(sec_head("PRACTICAL", "실용", rule=True))
        parts.append(f'<div class="prose">{md(strip_tokens(p.practical_md))}</div>')

    # --- Deep Guide -------------------------------------------------------
    body = strip_tokens(p.body_md)
    if body.strip():
        parts.append(sec_head("DEEP GUIDE", "더 깊이", rule=True))
        parts.append(f'<div class="prose">{md(body)}</div>')

    # 같은 지역의 다른 장소 — 길이 끊기지 않게 옆으로 나가는 문을 둔다
    if region:
        sibs = [x for x in region.places if x.slug != p.slug and x.summary][:6]
        if sibs:
            parts.append(sec_head("", f"{region.name} 의 다른 장소",
                                   more=("전체", f"{rel}/guide/{region.slug}.html")))
            parts.append('<div class="scroll-x place-siblings">'
                         + "".join(place_card(x, rel) for x in sibs) + "</div>")

    parts.append("</div>")

    index_search(p.name, f"places/{p.slug}.html", "place",
                 region.name if region else "")

    return page(
        title=p.name, body="\n".join(parts), rel=rel, tab="guide",
        region=p.region, country=region.country if region else "",
        description=p.summary,
        trail=[("홈", "index.html"), ("가이드", "guide/index.html"),
               (region.name if region else "", f"guide/{p.region}.html"),
               (p.name, None)],
    )


def build_day(d: Day, trip: Trip) -> str:
    """Day — 실행 화면. 첫 1~2 스크린에서 다음이 보여야 한다.
    지금 어디로 · 다음 일정 · 예약 · 주의 · 지도."""
    rel = ".."
    region = trip.region(d.region)
    prev_d, next_d = trip.day(d.n - 1), trip.day(d.n + 1)

    head_marks = []
    if d.is_transfer:
        head_marks.append(badge("caution", "거점 이동"))
    if not d.is_authoritative:
        head_marks.append(badge("neutral", "검토 중"))
    if d.fatigue:
        head_marks.append(f'<span>{ic("gauge")}피로도 {esc(d.fatigue)}</span>')
    if d.total_distance:
        head_marks.append(f'<span>{esc(d.total_distance)}</span>')

    parts = [f"""<div class="wrap">
<div class="stack-lg" style="padding-top:1.5rem">
<header>
  <div class="metarow"><span class="day-num">DAY {d.n}</span>
    <span class="day-date">{esc(d.date_label)}</span></div>
  <h1>{esc(d.city)}</h1>
  <p class="day-summary">{esc(d.title)}</p>
  <div class="metarow">{''.join(head_marks)}</div>
</header>"""]

    # --- NEXT — 지금 시각 기준. 오늘이 아니면 첫 일정을 보여준다 ------------
    real = [s for s in d.stops if s.category != "hotel" and s.start]
    if real:
        first = real[0]
        name = esc(first.name)
        if first.place:
            name = f'<a href="{rel}/places/{first.place.slug}.html">{name}</a>'
        parts.append(f"""<section class="action-card" id="next-action"
    data-day="{d.date.isoformat()}">
  <span class="label">NEXT</span>
  <div class="action-when">{esc(first.start)}</div>
  <div class="action-what">{name}</div>
  {f'<p class="card-dek">{esc(first.summary)}</p>' if first.summary else ''}
</section>""")

    # --- 예약 — 당일에 잠긴 것 -------------------------------------------
    reserved = d.reserved_stops
    if reserved:
        rows = "".join(
            f'<li><strong>{esc(s.start or "")} {esc(s.name)}</strong> — '
            f"{esc(s.reservation)}</li>" for s in reserved)
        parts.append(sec_head("BOOKING", "오늘 예약"))
        parts.append(f'<div class="prose"><ul>{rows}</ul></div>')

    # --- 시간표 -----------------------------------------------------------
    parts.append(sec_head("TODAY", "오늘 일정"))
    parts.append(timeline(d, rel))

    # --- 주의 ------------------------------------------------------------
    checks = []
    if d.backup:
        checks.append(f"<strong>Plan B</strong> — {esc(d.backup)}")
    for x in d.needs_review:
        checks.append(esc(x))
    if checks:
        parts.append(sec_head("CHECK", "확인할 것"))
        parts.append("".join(
            alert("caution", c) for c in checks))

    # --- 지도 ------------------------------------------------------------
    m = d.map or {}
    mc = map_card(d.stops, rel, center=m.get("center"), zoom=m.get("zoom", 14),
                  label=f"Day {d.n} 동선")
    if mc:
        parts.append(sec_head("MAP", "오늘 지도"))
        parts.append(mc)

    # --- 보조 정보 --------------------------------------------------------
    aside = []
    if d.transport:
        aside.append(("이동", d.transport))
    if d.food:
        aside.append(("식사", d.food))
    if d.highlights:
        aside.append(("오늘의 핵심", d.highlights))
    if aside:
        blocks = "".join(
            f'<details class="acc"><summary>{esc(name)}</summary>'
            f'<div class="acc-body"><ul>'
            + "".join(f"<li>{esc(x)}</li>" for x in items)
            + "</ul></div></details>" for name, items in aside)
        parts.append(f'<div class="stack">{blocks}</div>')

    # --- 이전/다음 --------------------------------------------------------
    nav = []
    if prev_d:
        nav.append(f'<a class="btn btn-secondary" href="{rel}/{prev_d.url}">'
                   f"← Day {prev_d.n}</a>")
    if next_d:
        nav.append(f'<a class="btn btn-secondary" href="{rel}/{next_d.url}">'
                   f"Day {next_d.n} →</a>")
    parts.append(f'<div class="btn-row" style="justify-content:space-between">'
                 f'{"".join(nav)}</div>')
    parts.append("</div></div>")

    # 형제 이동 — 그 지역의 날들
    sib = tabs_strip([
        (f"Day {x.n}", f"{rel}/{x.url}", x.n == d.n)
        for x in (region.days if region else [])])

    index_search(f"Day {d.n} · {d.date_label} {d.city}", d.url, "day", d.title)

    return page(
        title=f"Day {d.n} · {d.city}", body="\n".join(parts), rel=rel,
        tab="today", region=d.region, country=d.country, subnav=sib,
        description=d.title,
        trail=[("홈", "index.html"), ("전체 일정", "schedule.html"),
               (f"Day {d.n}", None)],
    )


def build_region(r: Region, trip: Trip) -> str:
    """Region — editorial destination landing. 상위 섹션 6개.

    Overview · Places · Schedule · Food · Stay & Local Life · Transport
    Day 의 상세 시간표를 여기에 복제하지 않는다.
    """
    rel = ".."
    hero_img = IMAGES["heroes"].get(r.slug) or IMAGES["by_place"].get(r.slug)
    hero = ""
    if hero_img:
        src, srcset = img_src(hero_img, "hero", rel)
        if src:
            hero = (f'<img class="hero-img" src="{src}" srcset="{srcset}" '
                    f'sizes="100vw" alt="{esc(hero_img.get("altKo") or r.name)}" '
                    f'fetchpriority="high" decoding="async">')

    sections = [("overview", "개요"), ("places", "장소"), ("days", "일정"),
                ("food", "먹거리"), ("stay", "숙박·생활"), ("transport", "교통")]
    subnav = tabs_strip([(label, f"#{key}", False) for key, label in sections])

    parts = [f"""<div class="hero">
  {hero}
  <div class="hero-body"><div class="hero-card">
    <div class="hero-eyebrow"><span class="label">{esc(r.tagline)}</span></div>
    <h1>{esc(r.name)}</h1>
    <p class="hero-sub">{esc(r.date_range)} · {r.nights}박 · {esc(r.day_range)}
      · 거점 {esc(r.base)}</p>
    <p class="hero-dek">{esc(r.dek)}</p>
    <div class="btn-row" style="margin-top:1rem">
      <a class="btn btn-primary" href="{rel}/map/{r.slug}.html">{ic("map")}지역 지도</a>
      <a class="btn btn-secondary" href="{rel}/{r.days[0].url}">{ic("today")}첫날 열기</a>
    </div>
  </div></div>
</div>
<div class="wrap">
{credit_line(hero_img)}
<div class="stack-lg" id="overview">"""]

    ed = r.editorial

    # --- Editor's Verdict — 이 지역에 시간을 쓸 가치와 한계 -----------------
    # 목록보다 먼저 온다. "여기서 무엇을 볼 가치가 있는가" 가 Region 의
    # 질문이고, 그 답이 판단이지 목록이 아니다.
    if ed.get("verdict"):
        # 레이블을 원고 표기 그대로 쓴다. 콘텐츠 스키마가 이 말을 배포
        # 산출물에서 찾는다 — 편집 표준의 이름이기도 하다.
        # 표기는 원고 그대로 둔다. 대문자는 CSS 가 입힌다 — 콘텐츠 스키마가
        # 배포 산출물에서 이 말을 찾으므로 글자를 바꾸면 안 된다.
        parts.append(sec_head("Editor’s Verdict", "시간을 쓸 가치와 한계",
                              rule=True))
        parts.append(f'<div class="prose">{md(strip_tokens(ed["verdict"]))}</div>')

    # --- 꼭 경험할 세 장면 · 생략해도 되는 것 ------------------------------
    if ed.get("scenes"):
        parts.append(sec_head("EXPERIENCE", "꼭 경험할 세 장면", rule=True))
        parts.append(f'<div class="prose">{md(strip_tokens(ed["scenes"]))}</div>')
    if ed.get("skip"):
        parts.append('<details class="acc"><summary>생략해도 되는 것</summary>'
                     f'<div class="acc-body prose">{md(strip_tokens(ed["skip"]))}'
                     "</div></details>")

    # --- Don't Miss -------------------------------------------------------
    must = [p for p in r.essential_places if p.summary][:6]
    if must:
        parts.append(f'<div id="places">{sec_head("DON\'T MISS", "놓치지 말 것", rule=True)}</div>')
        parts.append('<div class="grid grid-2">'
                     + "".join(place_card(p, rel, large=True) for p in must)
                     + "</div>")

    others = [p for p in r.places
              if p.grade != "essential" and p.summary and p.kind == "spot"]
    if others:
        parts.append(sec_head("", "그 밖의 장소"))
        parts.append('<div class="grid grid-2">'
                     + "".join(place_card(p, rel) for p in others) + "</div>")

    # --- Your days — 목록만. 시간표는 Day 가 갖는다 -----------------------
    if ed.get("overview"):
        parts.append(sec_head("AT A GLANCE", "한눈에 보기", rule=True))
        parts.append(f'<div class="prose">{md(strip_tokens(ed["overview"]))}</div>')

    parts.append(f'<div id="days">{sec_head("YOUR DAYS", "이 지역의 날들", rule=True)}</div>')
    parts.append('<div class="grid grid-2">'
                 + "".join(day_card(d, rel, r) for d in r.days) + "</div>")

    # --- Food -------------------------------------------------------------
    dishes, spots = [], []
    for d in r.days:
        for item in d.food:
            if item not in dishes:
                dishes.append(item)
        for s in d.stops:
            if s.category == "food" and s.name not in [x.name for x in spots]:
                spots.append(s)
    if dishes or spots:
        parts.append(f'<div id="food">{sec_head("EAT", "먹거리", rule=True)}</div>')
        if spots:
            cards = "".join(f"""<article class="card food-card">
  <div class="food-dish">{esc(s.name)}</div>
  <p class="food-why">{esc(s.summary)}</p>
  {f'<div class="metarow">{ic("ticket")}{esc(s.reservation)}</div>' if s.reservation else ''}
</article>""" for s in spots[:8])
            parts.append(f'<div class="grid grid-2">{cards}</div>')
        if dishes:
            parts.append('<div class="prose"><ul>'
                         + "".join(f"<li>{esc(x)}</li>" for x in dishes[:12])
                         + "</ul></div>")

    # --- Stay & Local Life ------------------------------------------------
    # 그 지역에서 **자는** 날의 숙소만 싣는다. 이동일은 두 지역에 걸쳐 있어
    # 그냥 모으면 다음 거점의 숙소가 이 지역 날짜를 달고 나타난다.
    hotels = {d.hotel.get("name"): d.hotel for d in r.days
              if d.region == r.slug and d.hotel.get("name")}
    parts.append(f'<div id="stay">{sec_head("STAY", "숙박 · 생활", rule=True)}</div>')
    if hotels:
        cards = []
        for name, h in hotels.items():
            confirmed = h.get("status") == "confirmed"
            mark = badge("ok", "확정") if confirmed else badge("caution", "미확정")
            href = maps_url(h.get("lat"), h.get("lng"), h.get("address") or "")
            link = (f'<a class="btn btn-secondary" rel="nofollow noopener" '
                    f'href="{esc(href)}">{ic("map")}지도</a>') if href else ""
            addr = (f'<dt>주소</dt><dd>{esc(h["address"])}</dd>'
                    if h.get("address") else "")
            cards.append(f"""<article class="card booking-card">
  <div class="booking-head"><span class="booking-name">{esc(name)}</span>{mark}</div>
  <dl><dt>체크인</dt><dd>{esc(r.checkin.isoformat())}</dd>
      <dt>체크아웃</dt><dd>{esc(r.checkout.isoformat())}</dd>
      <dt>박수</dt><dd>{r.nights}박</dd>{addr}</dl>
  <div class="btn-row">{link}</div>
</article>""")
        parts.append(f'<div class="grid grid-2">{"".join(cards)}</div>')
    else:
        parts.append(alert("caution",
                           "<strong>숙소 미확정</strong> — 확정되면 여기에 표시된다. "
                           "확정 전 주소를 믿고 이동하지 않는다.", "stay"))

    # --- Transport --------------------------------------------------------
    modes = []
    for d in r.days:
        for t in d.transport:
            if t not in modes:
                modes.append(t)
    parts.append(f'<div id="transport">{sec_head("TRANSPORT", "교통", rule=True)}</div>')
    arrive, leave = r.days[0], r.days[-1]
    parts.append(f"""<div class="prose">
<ul>
  <li><strong>도착</strong> — Day {arrive.n} · {esc(arrive.date_label)} · {esc(arrive.city)}</li>
  <li><strong>출발</strong> — Day {leave.n} · {esc(leave.date_label)} · {esc(leave.city)}</li>
</ul>
{'<ul>' + ''.join(f'<li>{esc(m)}</li>' for m in modes[:10]) + '</ul>' if modes else ''}
</div>""")

    extra = [(k, LAYER_LABEL[k]) for k in ("role", "rhythm") if ed.get(k)]
    if extra:
        parts.append("".join(
            f'<details class="acc"><summary>{esc(label)}</summary>'
            f'<div class="acc-body prose">{md(strip_tokens(ed[key]))}</div></details>'
            for key, label in extra))

    if r.rain_plan:
        parts.append(alert("caution",
                           f"<strong>우천 전환</strong> — {esc(r.rain_plan)}"))

    parts.append("</div></div>")

    index_search(r.name, f"guide/{r.slug}.html", "region", r.tagline)

    return page(
        title=r.name, body="\n".join(parts), rel=rel, tab="guide",
        region=r.slug, country=r.country, subnav=subnav, description=r.dek,
        trail=[("홈", "index.html"), ("가이드", "guide/index.html"),
               (r.name, None)],
    )


def build_guide_index(trip: Trip) -> str:
    """가이드 — 8개 지역을 이동 순서대로. 축은 목록을 맡고 본문을 갖지 않는다."""
    rel = ".."   # guide/index.html 은 하위 디렉터리에 있다
    cards = []
    for r in trip.regions:
        img = IMAGES["heroes"].get(r.slug)
        thumb = figure(img, rel, "content", "thumb",
                       "(min-width:600px) 50vw, 100vw")
        cards.append(f"""<article class="card place-card-lg" data-region="{r.slug}">
  {thumb}
  <div class="card-body">
    <div class="metarow"><span class="label" style="color:var(--accent)">
      {esc(r.tagline)}</span></div>
    <h3 class="card-title"><a class="card-link" href="{r.slug}.html">
      {esc(r.name)}</a></h3>
    <p class="card-dek">{esc(r.dek)}</p>
    <div class="metarow"><span>{esc(r.date_range)}</span><span class="sep">·</span>
      <span>{r.nights}박</span><span class="sep">·</span>
      <span>{esc(r.day_range)}</span></div>
  </div>
</article>""")
    body = f"""<div class="wrap"><div class="stack-lg" style="padding-top:1.5rem">
<header>
  <h1>가이드</h1>
  <p class="hero-dek">8개 거점을 이동 순서대로 놓았다. 각 지역에서 무엇을 보고
    먹고 경험할지는 지역 페이지가 맡는다.</p>
</header>
<div class="grid grid-2">{''.join(cards)}</div>
</div></div>"""
    return page(title="가이드", body=body, rel=rel, tab="guide",
                description="8개 지역 가이드",
                trail=[("홈", "index.html"), ("가이드", None)])


def build_schedule(trip: Trip) -> str:
    """전체 일정 — 43일. 하루의 본문은 Day 가 갖는다, 여기는 목록이다."""
    rel = "."
    blocks = []
    for r in trip.regions:
        own = [d for d in r.days if d.region == r.slug]
        if not own:
            continue
        blocks.append(f'<div id="{r.slug}" data-region="{r.slug}">'
                      + sec_head(r.tagline, r.name,
                                 more=("지역 가이드", f"guide/{r.slug}.html"),
                                 rule=False) + "</div>")
        blocks.append('<div class="grid grid-2">'
                      + "".join(day_card(d, rel, r) for d in own) + "</div>")
    last = trip.day(43)
    if last and last.region == "return":
        blocks.append(sec_head("", "귀국"))
        blocks.append(f'<div class="grid grid-2">{day_card(last, rel)}</div>')

    jump = tabs_strip([(r.name, f"#{r.slug}", False) for r in trip.regions])
    body = f"""<div class="wrap"><div class="stack-lg" style="padding-top:1.5rem">
<header>
  <h1>전체 일정</h1>
  <p class="hero-dek">{trip.start.isoformat()} — {trip.end.isoformat()} ·
    43일 42박 · 8개 거점</p>
</header>
{''.join(blocks)}
</div></div>"""
    return page(title="전체 일정", body=body, rel=rel, tab="schedule",
                subnav=jump, description="43일 전체 일정",
                trail=[("홈", "index.html"), ("전체 일정", None)])


def build_home(trip: Trip, res: dict) -> str:
    """홈 — 중심은 Today.

    여행 전에는 준비, 여행 중에는 오늘이 첫 화면이다. 정적 사이트라
    빌드 시각에 모드를 굳히지 않고 브라우저가 오늘 날짜로 고른다 —
    출발 전에 빌드한 페이지가 여행 중에도 맞아야 한다.
    """
    rel = "."
    days_payload = [{
        "n": d.n, "date": d.date.isoformat(), "city": d.city, "title": d.title,
        "url": d.url, "region": d.region,
        "next": [{"t": s.start, "n": s.name,
                  "u": f"places/{s.place.slug}.html" if s.place else None}
                 for s in d.stops if s.start and s.category != "hotel"][:4],
    } for d in trip.days]

    # 여행 전 화면 — 아직 잠기지 않은 것부터 보여준다
    undone = res.get("undone", 0)
    active = res.get("active", 0)
    pre_items = "".join(
        f"<li>{esc(name)} {badge('caution', esc(status))}</li>"
        for _id, name, status in res.get("items", [])
        if status not in ("예약완료", "확정", "취소"))[:0] or "".join(
        f"<li>{esc(name)} {badge('caution', esc(status))}</li>"
        for _id, name, status in res.get("items", [])
        if status not in ("예약완료", "확정", "취소"))

    region_cards = "".join(f"""<article class="card" data-region="{r.slug}"
    style="min-width:0">
  <div class="card-body">
    <span class="label" style="color:var(--accent)">{esc(r.day_range)}</span>
    <h3 class="card-title"><a class="card-link" href="guide/{r.slug}.html">
      {esc(r.name)}</a></h3>
    <p class="card-dek">{esc(r.tagline)}</p>
    <div class="metarow"><span>{esc(r.date_range)}</span><span class="sep">·</span>
      <span>{r.nights}박</span></div>
  </div>
</article>""" for r in trip.regions)

    body = f"""<div class="wrap"><div class="stack-lg" style="padding-top:1.5rem">

<section id="today-panel" class="stack" aria-live="polite">
  <noscript><p class="meta">오늘 화면은 기기의 날짜로 고릅니다.
    <a href="schedule.html">전체 일정</a>을 여세요.</p></noscript>
</section>

<section>
  {sec_head("JOURNEY", "여정", more=("전체 일정", "schedule.html"), rule=True)}
  <div class="scroll-x journey-grid">{region_cards}</div>
</section>

<section>
  {sec_head("PREPARE", "준비", more=("준비 화면", "prepare/index.html"), rule=True)}
  <div class="card"><div class="card-body">
    <div class="metarow">
      <span>{ic("check")}예약 {active}건</span>
      <span class="sep">·</span>
      <span>{badge('caution', f'미확정 {undone}건')}</span>
    </div>
    {f'<div class="prose"><ul>{pre_items}</ul></div>' if pre_items else ''}
  </div></div>
</section>

<section>
  {sec_head("TOOLS", "빠른 도구", rule=True)}
  <nav class="quick" aria-label="빠른 도구">
    <a href="#" id="quick-search">{ic("search")}<span>검색</span></a>
    <a href="map/index.html">{ic("map")}<span>지도</span></a>
    <a href="schedule.html">{ic("list")}<span>전체 일정</span></a>
    <a href="prepare/emergency.html">{ic("alert")}<span>긴급</span></a>
  </nav>
</section>

</div></div>
<script type="application/json" id="trip-data">{json.dumps(
    {"start": trip.start.isoformat(), "end": trip.end.isoformat(),
     "days": days_payload}, ensure_ascii=False)}</script>"""

    return page(title="오늘", body=body, rel=rel, tab="today",
                bar_title="2026년 유럽여행 가이드",
                description=f"{SITE_TITLE} — 43일 여행 가이드")


def build_map_pages(trip: Trip) -> dict[str, str]:
    """지도 — Trip · Region · Day 세 수준. 핀은 Place DB 에서만 온다."""
    out = {}
    rel = ".."
    all_stops = []
    seen = set()
    for d in trip.days:
        for s in d.stops:
            if s.lat and s.id not in seen and s.category != "hotel":
                seen.add(s.id)
                all_stops.append(s)

    links = "".join(
        f'<li><a href="{r.slug}.html">{esc(r.name)}</a> — {esc(r.day_range)}</li>'
        for r in trip.regions)
    out["index.html"] = page(
        title="지도", rel=rel, tab="map",
        trail=[("홈", "index.html"), ("지도", None)],
        body=f"""<div class="wrap"><div class="stack-lg" style="padding-top:1.5rem">
<header><h1>지도</h1>
<p class="hero-dek">전체 여정의 장소 {len(all_stops)}곳. 지역별 지도와 날짜별
동선은 각각 지역 페이지와 Day 페이지에 있다.</p></header>
{map_card(all_stops, rel, zoom=5, label="전체 여정")}
{sec_head("", "지역별 지도")}
<div class="prose"><ul>{links}</ul></div>
</div></div>""")

    for r in trip.regions:
        stops, s_seen = [], set()
        for d in r.days:
            for s in d.stops:
                if s.lat and s.id not in s_seen:
                    s_seen.add(s.id)
                    stops.append(s)
        day_links = "".join(
            f'<li><a href="../{d.url}">Day {d.n} · {esc(d.date_label)}</a> — '
            f"{esc(d.title)}</li>" for d in r.days)
        out[f"{r.slug}.html"] = page(
            title=f"{r.name} 지도", rel=rel, tab="map", region=r.slug,
            country=r.country,
            trail=[("홈", "index.html"), ("지도", "map/index.html"),
                   (r.name, None)],
            body=f"""<div class="wrap"><div class="stack-lg" style="padding-top:1.5rem">
<header><h1>{esc(r.name)} 지도</h1>
<p class="hero-dek">{esc(r.date_range)} · 장소 {len(stops)}곳</p></header>
{map_card(stops, r_rel := rel, zoom=12, label=f"{r.name} 지도")}
{sec_head("", "날짜별 동선")}
<div class="prose"><ul>{day_links}</ul></div>
<div class="btn-row"><a class="btn btn-secondary" href="../guide/{r.slug}.html">
  {ic("region")}{esc(r.name)} 가이드</a></div>
</div></div>""")
    return out


def build_prepare(trip: Trip, res: dict) -> dict[str, str]:
    """준비 — 무엇을 예약·확인해야 하는가.

    개인정보는 나가지 않는다. 예약번호·주소·금액은 렌더하지 않고 상태와
    건수만 보여준다.
    """
    rel = ".."
    out = {}
    items = res.get("items", [])
    done = [i for i in items if i[2] in ("예약완료", "확정")]
    open_ = [i for i in items if i[2] not in ("예약완료", "확정", "취소")]

    def rows(group):
        return "".join(
            f"""<article class="card booking-card">
  <div class="booking-head"><span class="booking-name">{esc(name)}</span>
    {badge('ok', '확정') if status in ('예약완료', '확정') else badge('caution', esc(status))}</div>
</article>""" for _id, name, status in group)

    out["index.html"] = page(
        title="준비", rel=rel, tab="prepare",
        description="여행 준비 상태를 점검한다",
        trail=[("홈", "index.html"), ("준비", None)],
        body=f"""<div class="wrap"><div class="stack-lg" style="padding-top:1.5rem">
<header><h1>준비</h1>
<p class="hero-dek">여행 준비 상태를 점검한다. 예약 {res.get('active', 0)}건 중
  미확정 {res.get('undone', 0)}건.</p></header>

{alert('caution', '<strong>확정되지 않은 예약이 있다.</strong> 확정 전 주소·시각을 '
       '믿고 이동하지 않는다. 확정된 것만 화면에 확정으로 표시된다.')
 if open_ else ''}

{sec_head('TO LOCK', f'미확정 {len(open_)}건', rule=True) if open_ else ''}
<div class="grid grid-2">{rows(open_)}</div>

{sec_head('LOCKED', f'확정 {len(done)}건', rule=True) if done else ''}
<div class="grid grid-2">{rows(done)}</div>

<div class="btn-row"><a class="btn btn-secondary" href="emergency.html">
  {ic('alert')}긴급 연락처</a></div>
</div></div>""")

    out["emergency.html"] = page(
        title="긴급", rel=rel, tab="prepare",
        trail=[("홈", "index.html"), ("준비", "prepare/index.html"),
               ("긴급", None)],
        body=f"""<div class="wrap-read"><div class="stack-lg" style="padding-top:1.5rem">
<header><h1>긴급 연락처</h1>
<p class="hero-dek">국경을 넘으면 번호가 바뀐다. Day 7 에 스페인에서
  프랑스로 넘어간다.</p></header>
<div class="table-wrap"><table>
<thead><tr><th>국가</th><th>번호</th><th>용도</th></tr></thead>
<tbody>
<tr><td>공통 (EU)</td><td><strong>112</strong></td><td>모든 긴급 — 경찰·소방·구급</td></tr>
<tr><td>스페인</td><td>091 / 061</td><td>경찰 / 구급</td></tr>
<tr><td>프랑스</td><td>17 / 15</td><td>경찰 / 구급 (SAMU)</td></tr>
</tbody></table></div>
{alert('ok', '<strong>112 는 EU 전역에서 통한다.</strong> 어느 나라인지 '
       '헷갈리면 112 를 누른다. 휴대폰 잠금 상태에서도 걸린다.', 'check')}
</div></div>""")
    return out


# ================================================================ 자산·색인

def load_reservations() -> dict:
    """예약 상태. 개인정보는 나오지 않는다 — 상태와 건수만 밖으로 나간다.

    주소·예약번호·금액은 렌더하지 않는다. 공개 배포되는 사이트다.
    """
    try:
        from openpyxl import load_workbook
    except ImportError:
        return {"active": 0, "undone": 0, "items": [], "by_date": {}}
    if not TRACKER_XLSX.exists():
        return {"active": 0, "undone": 0, "items": [], "by_date": {}}
    wb = load_workbook(TRACKER_XLSX, data_only=True)
    if "Reservations" not in wb.sheetnames:
        return {"active": 0, "undone": 0, "items": [], "by_date": {}}
    rows = list(wb["Reservations"].iter_rows(values_only=True))
    hdr_i = next((i for i, r in enumerate(rows) if r and r[0] == "ID"), None)
    if hdr_i is None:
        return {"active": 0, "undone": 0, "items": [], "by_date": {}}
    hdr = list(rows[hdr_i])
    ix = {n: hdr.index(n) for n in ("ID", "날짜", "상태", "예약항목")}
    by_date, items, cancelled = {}, [], 0
    for r in rows[hdr_i + 1:]:
        if not r or not r[ix["ID"]]:
            continue
        status = str(r[ix["상태"]] or "").strip()
        if status == "취소":
            cancelled += 1
            continue
        d = r[ix["날짜"]]
        if hasattr(d, "date"):
            by_date.setdefault(d.date().isoformat(), []).append(status)
        items.append((str(r[ix["ID"]] or "").strip(),
                      str(r[ix["예약항목"]] or "").strip(), status))
    undone = sum(1 for _i, _n, s in items if s not in ("예약완료", "확정"))
    return {"active": len(items), "undone": undone, "items": items,
            "by_date": by_date}


def write_assets(trip: Trip) -> None:
    out = SITE / "assets"
    out.mkdir(parents=True, exist_ok=True)
    # 아이콘은 CSS 마스크로 붙인다 — 페이지마다 스프라이트를 인라인하면
    # 페이지 수만큼 무게가 붙는다. 마스크는 CSS 한 번이고 페이지 무게는 0 이다.
    (out / "style.css").write_text(
        (ASSETS / "style.css").read_text(encoding="utf-8") + "\n" + icons.css(),
        encoding="utf-8")
    for name in ("app.js", "pwa.js"):
        shutil.copy(ASSETS / name, out / name)
    # 글꼴은 번들하지 않는다. 기기의 기본 한글 글꼴을 쓰므로 내려받을 것이
    # 없고, 그만큼 오프라인 패키지가 가벼워진다.
    pwa = ROOT / "source" / "ASSETS" / "pwa"
    if pwa.exists():
        shutil.copytree(pwa, out / "pwa", dirs_exist_ok=True)

    # 사진 — 매니페스트에 있는 것만 옮긴다. 카탈로그에 없으면 자리도 없다.
    raw = json.loads(IMAGE_MANIFEST.read_text(encoding="utf-8"))
    copied = 0
    for img in raw.get("images", []):
        for variants in (img.get("variants") or {}).values():
            for v in variants:
                src = ROOT / v["path"]
                dst = SITE / v["sitePath"]
                if src.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    if not dst.exists():
                        shutil.copy(src, dst)
                        copied += 1
    print(f"  사진 {copied}개 복사")

    (out / "search-index.js").write_text(
        "window.SEARCH_INDEX=" + json.dumps(SEARCH_INDEX, ensure_ascii=False)
        + ";", encoding="utf-8")


PWA_ICON_SPECS = (
    ("apple-touch-icon.png", "180x180", "any"),
    ("icon-192.png", "192x192", "any"),
    ("icon-512.png", "512x512", "any"),
    ("icon-maskable-512.png", "512x512", "maskable"),
)

# 연결이 끊겨도 반드시 열려야 하는 것들. 없으면 빌드를 세운다.
PWA_CORE_PATHS = (
    "index.html",
    "offline.html",
    "offline-fallback.html",
    "schedule.html",
    "guide/index.html",
    "map/index.html",
    "prepare/index.html",
    "prepare/emergency.html",
    "assets/style.css",
    "assets/app.js",
    "assets/search-index.js",
)


def build_offline_page() -> str:
    """오프라인 준비 화면. 여행 전에 전체를 기기에 저장시킨다.

    43일 중 상당 구간이 데이터가 약하거나 로밍이 비싸다. 현장에서 페이지가
    안 열리는 것이 이 도구의 실패다.

    DOM 은 build/assets/pwa.js 의 계약이다 — id 를 바꾸면 저장 기능이
    조용히 죽는다. 스크립트가 없으면 안내 문구만 남는다.
    """
    return page(
        title="오프라인 준비", rel=".", tab="prepare",
        description="가이드북 전체를 기기에 저장한다",
        trail=[("홈", "index.html"), ("오프라인 준비", None)],
        body=f"""<div class="wrap-read"><div class="stack-lg" style="padding-top:1.5rem">
<header><h1>오프라인 준비</h1>
<p class="hero-dek">가이드북 전체를 기기에 저장한다. 연결이 없어도 일정 ·
장소 · 지도 목록이 열린다.</p></header>

<div class="card" id="pwa-panel"><div class="card-body stack">
  <dl class="pwa-facts">
    <dt>저장 상태</dt><dd id="pwa-status">확인 중</dd>
    <dt>설치 형태</dt><dd id="pwa-install-mode">확인 중</dd>
    <dt>저장 용량</dt><dd id="pwa-storage">—</dd>
    <dt>버전</dt><dd id="pwa-version">—</dd>
  </dl>
  <p class="meta" id="pwa-detail"></p>
  <div class="btn-row">
    <button class="btn btn-primary" id="pwa-save" type="button">
      {ic("download")}전체 저장</button>
    <button class="btn btn-secondary" id="pwa-clear" type="button">
      {ic("close")}저장 비우기</button>
  </div>
  <progress class="pwa-progress" id="pwa-progress" value="0" max="1"
    aria-label="저장 진행률"></progress>
  <div id="pwa-update-box" hidden>
    {alert("caution", '새 버전이 있다. <button class="btn btn-quiet" '
           'id="pwa-activate-update" type="button">지금 적용</button>')}
  </div>
</div></div>

<noscript><p class="meta">저장 기능은 자바스크립트가 필요하다.
연결이 되는 곳에서 이 화면을 다시 열어라.</p></noscript>

{alert("caution", "<strong>출발 전과 장거리 이동 전에 다시 확인한다.</strong> "
       "iOS 는 저장 공간이 부족하거나 앱을 오래 쓰지 않으면 웹 데이터를 "
       "정리할 수 있다.")}

<div class="prose">
<h2>담기는 것</h2>
<ul>
  <li>43일 일정과 하루별 시간표 · 이동 · 예약</li>
  <li>장소 페이지 전체와 사진</li>
  <li>지역 가이드 · 지도 목록과 좌표 링크</li>
  <li>준비 화면과 긴급 연락처</li>
</ul>
<p>지도 타일은 담기지 않는다. 좌표와 Google Maps 링크는 저장되므로
연결이 되는 곳에서 열 수 있다.</p>
</div>
</div></div>""")


def build_offline_fallback() -> str:
    """저장되지 않은 페이지를 오프라인에서 열었을 때. 막다른 화면을 만들지 않는다."""
    return page(
        title="저장되지 않은 페이지", rel=".", tab="today",
        trail=[("홈", "index.html"), ("오프라인", None)],
        body=f"""<div class="wrap-read"><div class="stack-lg" style="padding-top:1.5rem">
<header><h1>이 페이지는 아직 저장되지 않았다</h1>
<p class="hero-dek">연결이 없고, 요청한 페이지가 기기에 없다.</p></header>
{alert("caution", "연결이 되는 곳에서 <strong>오프라인 준비</strong> 화면을 열어 "
       "전체 저장을 마치면 이런 일이 생기지 않는다.")}
<div class="btn-row">
  <a class="btn btn-primary" href="index.html">{ic("today")}저장된 홈 열기</a>
  <a class="btn btn-secondary" href="offline.html">{ic("download")}오프라인 준비</a>
</div>
</div></div>""")


def write_pwa() -> None:
    """manifest · 오프라인 목록 · 서비스워커.

    버전은 파일 내용 해시다. 내용이 안 바뀌면 버전도 안 바뀌고, 그래서
    기기가 헛되이 다시 받지 않는다.
    """
    (SITE / "manifest.webmanifest").write_text(json.dumps({
        "id": "./",
        "name": SITE_TITLE,
        "short_name": "유럽 가이드북",
        "description": "Barcelona 에서 Paris 까지 43일 여행 현장 가이드북",
        "lang": "ko",
        "start_url": "./index.html",
        "scope": "./",
        "display": "standalone",
        "background_color": "#FAF6EF",
        "theme_color": "#FAF6EF",
        "icons": [
            {"src": f"./assets/pwa/{name}", "sizes": sizes,
             "type": "image/png", "purpose": purpose}
            for name, sizes, purpose in PWA_ICON_SPECS
        ],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    excluded = {"sw.js", "offline-files.json", ".nojekyll"}
    records, version_hash = [], hashlib.sha256()
    for path in sorted(p for p in SITE.rglob("*") if p.is_file()):
        rel = path.relative_to(SITE).as_posix()
        if rel in excluded:
            continue
        content = path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        records.append({"path": rel, "size": len(content), "sha256": digest})
        version_hash.update(rel.encode("utf-8") + b"\0")
        version_hash.update(digest.encode("ascii") + b"\n")
    version = version_hash.hexdigest()

    (SITE / "offline-files.json").write_text(json.dumps({
        "version": version,
        "totalFiles": len(records),
        "totalBytes": sum(r["size"] for r in records),
        "files": records,
    }, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

    missing = [p for p in PWA_CORE_PATHS if not (SITE / p).is_file()]
    if missing:
        sys.exit("PWA 핵심 파일 누락: " + ", ".join(missing))

    template = (ASSETS / "service-worker.js").read_text(encoding="utf-8")
    sw = template.replace("__PWA_VERSION__", version).replace(
        "__PWA_CORE_PATHS__", json.dumps(list(PWA_CORE_PATHS), ensure_ascii=False))
    if "__PWA_" in sw:
        sys.exit("Service Worker 템플릿 토큰이 남아 있다")
    (SITE / "sw.js").write_text(sw, encoding="utf-8")
    mib = sum(r["size"] for r in records) / 1048576
    print(f"  PWA: {len(records)}개 파일 · {mib:.1f} MiB · 버전 {version[:12]}")


# 옛 주소 → 새 주소. 404 를 늘리지 않는다.
def write_redirects(trip: Trip) -> int:
    n = 0
    def put(path: str, target: str, label: str):
        nonlocal n
        p = SITE / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(redirect(target, label), encoding="utf-8")
        n += 1

    put("regions.html", "guide/index.html", "가이드")
    put("daily/index.html", "../schedule.html", "전체 일정")
    put("maps/index.html", "../map/index.html", "지도")
    put("tracker/index.html", "../prepare/index.html", "준비")
    put("places/index.html", "../guide/index.html", "가이드")

    # 챕터 10개 카테고리 → 새 지역 페이지의 해당 섹션
    section = {
        "index": "", "about": "#overview", "schedule": "#days",
        "places": "#places", "food": "#food", "stay": "#stay",
        "transport": "#transport", "tips": "#overview",
        "booking": "", "cost": "", "sources": "",
    }
    for r in trip.regions:
        for name, anchor in section.items():
            target = (f"../../prepare/index.html"
                      if name in ("booking", "cost")
                      else f"../../about/sources.html" if name == "sources"
                      else f"../../guide/{r.slug}.html{anchor}")
            put(f"chapters/{r.slug}/{name}.html", target, r.name)
        for d in r.days:
            put(f"chapters/{r.slug}/day-{d.n:02d}.html",
                f"../../{d.url}", f"Day {d.n}")
    for name in ("index", "days", "places", "food", "stay", "transport",
                 "tips", "booking", "cost", "essential", "p0", "about",
                 "sources", "reverify"):
        put(f"topics/{name}.html", "../guide/index.html", "가이드")
    for name in ("dashboard", "itinerary", "reservations", "accommodation",
                 "transport", "locks"):
        put(f"tracker/{name}.html", "../prepare/index.html", "준비")
    return n


def build_credits(trip: Trip) -> str:
    """사진 저작자 표시. 표시가 필요한 라이선스는 화면에 남긴다."""
    raw = json.loads(IMAGE_MANIFEST.read_text(encoding="utf-8"))
    def cell_link(url: str, label: str) -> str:
        """주소가 없으면 링크를 만들지 않는다. 빈 href 는 눌러도 제자리다."""
        if not url:
            return esc(label) if label else "—"
        return (f'<a href="{esc(url)}" rel="nofollow noopener">'
                f'{esc(label) if label else domain_of(url)}</a>')

    rows = "".join(f"""<tr><td>{esc(i.get('titleKo') or i.get('title'))}</td>
<td>{linkify(esc(i.get('creator') or '—'))}</td>
<td>{cell_link(i.get('licenseUrl') or '', i.get('license') or '')}</td>
<td>{cell_link(i.get('sourcePage') or '', '출처')}</td></tr>"""
        for i in raw.get("images", []))
    return page(
        title="사진 저작자 표시", rel="..", tab="guide",
        trail=[("홈", "index.html"), ("사진 저작자 표시", None)],
        body=f"""<div class="wrap"><div class="stack-lg" style="padding-top:1.5rem">
<header><h1>사진 저작자 표시 · 라이선스</h1>
<p class="hero-dek">이 사이트는 공개 배포되므로 재배포가 허용된 이미지만
쓴다. 저작자 표시가 필요한 라이선스는 여기에 표시한다.</p></header>
<div class="table-wrap"><table>
<thead><tr><th>사진</th><th>저작자</th><th>라이선스</th><th>출처</th></tr></thead>
<tbody>{rows}</tbody></table></div>
</div></div>""")


def build_sources(trip: Trip) -> str:
    return page(
        title="출처와 검증", rel="..", tab="guide",
        trail=[("홈", "index.html"), ("출처와 검증", None)],
        body=f"""<div class="wrap-read"><div class="stack-lg" style="padding-top:1.5rem">
<header><h1>출처와 검증</h1></header>
<div class="prose">
<p>이 가이드북은 확인한 것만 싣는다. 확인하지 못한 운영시간·요금은
기술하지 않거나 <strong>재확인</strong> 표시를 단다. 추측으로 채우지 않는다.</p>
<ul>
  <li>역사·건축·인물 — 복수 출처를 확인한 뒤 기술한다.</li>
  <li>운영시간·요금 — 근거와 확인 날짜를 함께 들고 다닌다.
    장소 페이지의 <strong>실용</strong> 표에서 볼 수 있다.</li>
  <li>개인 해석 — 주어를 밝힌다.</li>
  <li>미확인 — 기술하지 않는다.</li>
</ul>
<p>예약은 아직 전부 잠기지 않았다. <strong>확정 전 주소를 확정으로 믿고
이동하지 않는다.</strong> 확정된 것만 화면에 확정으로 표시된다.</p>
</div></div></div>""")


# ================================================================ 가드

def check_vocabulary(trip: Trip) -> list[str]:
    """데이터가 쓰는 값을 렌더러가 전부 아는가.

    콘텐츠 편집은 이 개편과 나란히 계속된다. 편집자가 새 이동수단이나
    새 카테고리를 쓰면 렌더러는 그 값을 모른 채 **영어 코드를 그대로**
    화면에 흘린다. 실제로 그런 일이 있었다 — Nice 일정이 갱신되면서
    'tram' 과 'unconfirmed' 가 들어왔고, 특히 'unconfirmed' 는 아직
    이동수단이 안 정해졌다는 뜻인데 확정된 구간과 똑같이 보였다.

    그래서 빌드를 세운다. 현장에서 읽는 화면이 조용히 틀리는 것보다
    빌드가 시끄럽게 멈추는 편이 낫다.
    """
    problems = []
    bad_modes, bad_cats, bad_status = {}, {}, {}
    for d in trip.days:
        for leg in d.legs:
            if leg.mode not in MODE_LABEL:
                bad_modes.setdefault(leg.mode, []).append(d.n)
        for s in d.stops:
            if s.category not in CAT_ICON:
                bad_cats.setdefault(s.category, []).append(d.n)
        if d.source_status not in ("authoritative", "candidate-latest-needs-review",
                                   "prototype-reviewed"):
            bad_status.setdefault(d.source_status, []).append(d.n)

    for mode, days in bad_modes.items():
        problems.append(
            f"모르는 이동수단 '{mode}' — Day {sorted(set(days))[:6]}. "
            f"render.py 의 MODE_LABEL·MODE_ICON 에 한국어 표기를 더한다.")
    for cat, days in bad_cats.items():
        problems.append(
            f"모르는 장소 분류 '{cat}' — Day {sorted(set(days))[:6]}. "
            f"render.py 의 CAT_ICON 에 아이콘을 지정한다.")
    for st, days in bad_status.items():
        problems.append(f"모르는 sourceStatus '{st}' — Day {sorted(set(days))[:6]}")

    # 등급도 마찬가지다. 배지가 안 붙으면 '필수' 가 그냥 사라진다.
    for pl in trip.places.values():
        if pl.grade_label and pl.grade is None:
            problems.append(
                f"모르는 등급 '{pl.grade_label}' — {pl.slug}. "
                f"model.py 의 grade_map 에 더한다.")
    return problems


def check_place_prose(trip: Trip, promoted: set[str]) -> list[str]:
    """장문을 갖고 있던 장소가 장문을 잃지 않았는가.

    챕터 원고에서 절 제목이 바뀌면 대조에 실패해 장소 페이지가 조용히
    빈 껍데기가 된다. 그게 이 파이프라인에서 가장 잘 일어나는 사고다.
    """
    problems = []
    for slug in sorted(promoted):
        pl = trip.places.get(slug)
        if pl is None:
            problems.append(f"승격된 장문의 주인이 명부에 없다: {slug}")
        elif not pl.has_deep_guide and not pl.why_go:
            problems.append(f"장문이 사라졌다: {slug} — 챕터 원고의 절 제목이 "
                            f"바뀌었을 수 있다")
    return problems
