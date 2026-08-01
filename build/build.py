#!/usr/bin/env python3
"""TP Europe Travel Guidebook — 정적 사이트 빌드 스크립트.

source/ 의 리더 에디션 MD, 실행지도 HTML, 마스터 트래커 xlsx를
site/ 아래의 순수 정적 HTML 사이트로 변환한다.

UI/UX 설계: docs/UIUX_Design_v1.0.md
 - 전역: 상단바 + 드로어 메뉴(검색) + 모바일 하단 탭바(홈·일정·오늘·지도·트래커)
 - 챕터: Layer(실행·이해·실용) 점프 + Day 칩 서브내비, 관련 리소스, 이전/다음
 - '오늘' 버튼: 빌드 시 생성한 날짜→Day섹션 매핑(data.js)으로 즉시 이동

사용법:
    python3 build/build.py

필요 패키지: pip install markdown openpyxl
"""

import html
import json
import re
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

try:
    import markdown
    from markdown.extensions.toc import TocExtension, slugify_unicode
except ImportError:
    sys.exit("markdown 패키지가 필요합니다: pip install markdown")

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl 패키지가 필요합니다: pip install openpyxl")

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source"
CHAPTER_DIR = SOURCE / "40_Master_Guidebook"
SITE = ROOT / "site"
ASSETS = ROOT / "build" / "assets"

SITE_TITLE = "Jason과 Julia의 2026 유럽 장기여행 가이드북"
SITE_SHORT = "유럽 43일 가이드북"
TRIP_PERIOD = "2026-08-29 ~ 2026-10-10 · 43일"
TRIP_START = date(2026, 8, 29)
TRIP_END = date(2026, 10, 10)

# 챕터 매니페스트 — kind: intro(안내) / schedule(전체일정) / region(지역 가이드)
CHAPTERS = [
    dict(file="01_How_to_Use_This_Guidebook_Reader_v1.1.md", slug="01",
         kind="intro", title="가이드북 사용법", sub="읽는 법과 기준 문서"),
    dict(file="02_Whole_Trip_Experience_Highlights_Reader_v1.1.md", slug="02",
         kind="intro", title="전체 여행 하이라이트", sub="43일의 경험 설계"),
    dict(file="03_Whole_Trip_Master_Itinerary_Reader_v1.1.md", slug="03",
         kind="schedule", title="43일 Master Itinerary", sub="전체 일정 한눈에"),
    dict(file="04_Barcelona_Sitges_Reader_v1.0.md", slug="04", kind="region",
         title="Barcelona · Sitges", start=date(2026, 8, 29), end=date(2026, 9, 1),
         nights=3),
    dict(file="05_Girona_Collioure_Emporda_Reader_v1.0.md", slug="05", kind="region",
         title="Girona · Collioure · Empordà", start=date(2026, 9, 1), end=date(2026, 9, 4),
         nights=3),
    dict(file="06_Nice_Cote_d_Azur_Reader_v1.1.md", slug="06", kind="region",
         title="Nice · Côte d’Azur", start=date(2026, 9, 4), end=date(2026, 9, 9),
         nights=5, map="nice.html", map_title="Nice 실행지도"),
    dict(file="07_Aix_en_Provence_Reader_v1.1.md", slug="07", kind="region",
         title="Aix-en-Provence", start=date(2026, 9, 9), end=date(2026, 9, 13),
         nights=4),
    dict(file="08_Luberon_Farmhouse_Reader_v1.1.md", slug="08", kind="region",
         title="Luberon Farmhouse", start=date(2026, 9, 13), end=date(2026, 9, 17),
         nights=4),
    dict(file="09_Avignon_Alpilles_Pont_du_Gard_Reader_v1.0.md", slug="09", kind="region",
         title="Avignon · Alpilles · Pont du Gard", start=date(2026, 9, 17), end=date(2026, 9, 21),
         nights=4),
    dict(file="10_Lyon_Annecy_Reader_v1.0.md", slug="10", kind="region",
         title="Lyon · Annecy", start=date(2026, 9, 21), end=date(2026, 9, 25),
         nights=4, map="lyon.html", map_title="Lyon·Annecy 실행지도"),
    dict(file="11_Paris_Long_Stay_Reader_v1.0.md", slug="11", kind="region",
         title="Paris Long Stay", start=date(2026, 9, 25), end=date(2026, 10, 10),
         nights=15),
]

MAPS = [
    ("68_Nice_Cote_d_Azur_Execution_Map_v0.2.html", "nice.html",
     "Nice · Côte d’Azur 실행지도", "9/4~9/9 동선 · Cannes · Monaco · 9/9 이동축"),
    ("69_Lyon_Annecy_Execution_Map_v0.1.html", "lyon.html",
     "Lyon · Annecy 실행지도", "9/21~9/25 동선 · Annecy 당일치기"),
]

TRACKER_XLSX = SOURCE / "TP_Europe_Travel_Master_Tracker_v1.1.xlsx"
TRACKER_SHEETS = [
    ("Master Itinerary", "itinerary", "43일 전체 일정표"),
    ("Reservations", "reservations", "예약 현황"),
    ("Transport", "transport", "이동·교통"),
    ("Accommodation", "accommodation", "숙소 후보·확정"),
    ("Dashboard", "dashboard", "진행 대시보드"),
]

LAYER_LABELS = {"1": "일정", "2": "여행정보", "3": "실용정보"}
DAY_RE = re.compile(r"Day\s*(\d+)\s*[—\-–]\s*(\d+)월\s*(\d+)일")

# 빌드 중 수집되는 전역 데이터
TODAY_MAP = {}      # 'YYYY-MM-DD' -> 사이트 루트 기준 상대 URL (지역 범위 기반)
DAY_OVERRIDES = {}  # 'YYYY-MM-DD' -> Day 섹션 앵커 URL (범위 매핑보다 우선)
SEARCH_INDEX = []   # {t: 제목, c: 위치, u: URL}


# ---------------------------------------------------------------- utilities

def parse_frontmatter(text):
    """단순 YAML frontmatter를 dict로 파싱하고 본문을 돌려준다."""
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].strip().splitlines():
                if ":" in line:
                    key, _, value = line.partition(":")
                    meta[key.strip()] = value.strip().strip('"')
            text = text[end + 4:]
    return meta, text.lstrip("\n")


def md_convert(text):
    md = markdown.Markdown(
        extensions=["tables", "fenced_code",
                    TocExtension(slugify=slugify_unicode, toc_depth="1-3")],
        output_format="html5",
    )
    body = md.convert(text)
    return body, md.toc_tokens


def flatten_tokens(tokens):
    flat = []
    for tok in tokens:
        flat.append(tok)
        flat.extend(flatten_tokens(tok.get("children", [])))
    return flat


def wrap_tables(body):
    body = body.replace("<table>", '<div class="table-wrap"><table>')
    return body.replace("</table>", "</table></div>")


def mark_layer_headings(body):
    """Layer 경계 h1에 시각 구분용 클래스를 부여한다."""
    return re.sub(r'<h1 id="([^"]*)">(Layer\s*\d[^<]*)</h1>',
                  r'<h1 id="\1" class="layer-h">\2</h1>', body)


def rewrite_md_links(body, slug_by_file):
    def repl(match):
        name = Path(match.group(1).split("#")[0]).name
        if name in slug_by_file:
            return f'href="{slug_by_file[name]}.html"'
        return match.group(0)
    return re.sub(r'href="([^"]+\.md)"', repl, body)


def toc_html(tokens):
    items = []
    for tok in tokens:
        items.append(f'<li><a href="#{tok["id"]}">{html.escape(tok["name"])}</a></li>')
        for child in tok.get("children", []):
            items.append(
                f'<li class="toc-sub"><a href="#{child["id"]}">{html.escape(child["name"])}</a></li>')
    if not items:
        return ""
    return ('<details class="toc"><summary>전체 목차</summary><ul>'
            + "".join(items) + "</ul></details>")


def date_label(d):
    return f"{d.month}/{d.day}"


# ---------------------------------------------------------------- page shell

def drawer_html(rel):
    intro = "".join(
        f'<a href="{rel}/chapters/{c["slug"]}.html">{c["slug"]} {c["title"]}</a>'
        for c in CHAPTERS if c["kind"] != "region")
    regions = "".join(
        f'<a href="{rel}/chapters/{c["slug"]}.html">{c["slug"]} {c["title"]}'
        f'<span>{date_label(c["start"])}–{date_label(c["end"])} · {c["nights"]}박</span></a>'
        for c in CHAPTERS if c["kind"] == "region")
    maps = "".join(
        f'<a href="{rel}/maps/{out}">{title}</a>' for _, out, title, _ in MAPS)
    tracker = "".join(
        f'<a href="{rel}/tracker/{slug}.html">{label}</a>'
        for _, slug, label in TRACKER_SHEETS)
    return f"""<div id="overlay"></div>
<aside id="drawer" aria-label="전체 메뉴">
  <div class="dw-head">
    <span>{SITE_SHORT}</span>
    <button id="drawer-close" aria-label="닫기">✕</button>
  </div>
  <input id="search-input" type="search" placeholder="장소·섹션 검색" autocomplete="off">
  <div id="search-results"></div>
  <nav class="dw-nav">
    <a href="{rel}/index.html" class="dw-home">🏠 홈 — 여정 타임라인</a>
    <h3>시작하기</h3>{intro}
    <h3>지역 가이드</h3>{regions}
    <h3>실행지도</h3>{maps}
    <h3>트래커</h3>{tracker}
  </nav>
</aside>"""


def page(title, body, *, rel="..", topbar_title=None, meta_line="", subnav=""):
    meta_html = f'<p class="meta">{meta_line}</p>' if meta_line else ""
    tb_title = html.escape(topbar_title or title)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — {SITE_TITLE}</title>
<link rel="stylesheet" href="{rel}/assets/style.css">
</head>
<body data-rel="{rel}">
<header class="topbar">
  <button id="menu-btn" aria-label="메뉴 열기">☰</button>
  <a class="tb-title" href="{rel}/index.html">{tb_title}</a>
  <nav class="tb-links">
    <a href="{rel}/chapters/03.html">일정</a>
    <a href="{rel}/maps/index.html">지도</a>
    <a href="{rel}/tracker/index.html">트래커</a>
  </nav>
</header>
{subnav}
{drawer_html(rel)}
<main>
{meta_html}
{body}
</main>
<footer>
  <p>{SITE_TITLE} · {TRIP_PERIOD}</p>
</footer>
<nav class="bottomnav" aria-label="주요 메뉴">
  <a href="{rel}/index.html"><b>🏠</b><span>홈</span></a>
  <a href="{rel}/chapters/03.html"><b>📅</b><span>일정</span></a>
  <a href="#" class="nav-today"><b>📍</b><span>오늘</span></a>
  <a href="{rel}/maps/index.html"><b>🗺️</b><span>지도</span></a>
  <a href="{rel}/tracker/index.html"><b>📋</b><span>트래커</span></a>
</nav>
<button id="back-top" aria-label="맨 위로">↑</button>
<script src="{rel}/assets/data.js" defer></script>
<script src="{rel}/assets/nav.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- chapters

def chapter_subnav(chapter, flat_tokens):
    """Layer 점프 + Day 칩 서브내비 (지역 챕터 전용)."""
    layers, days = [], []
    for tok in flat_tokens:
        m = re.match(r"Layer\s*(\d)", tok["name"])
        if m and tok["level"] == 1 and m.group(1) in LAYER_LABELS:
            layers.append(f'<a href="#{tok["id"]}">{LAYER_LABELS[m.group(1)]}</a>')
        dm = DAY_RE.search(tok["name"])
        if dm:
            days.append(f'<a href="#{tok["id"]}" title="{html.escape(tok["name"])}">'
                        f'{int(dm.group(2))}/{int(dm.group(3))}</a>')
    if not layers and not days:
        return ""
    layer_html = f'<div class="sn-layers">{"".join(layers)}</div>' if layers else ""
    days_html = f'<div class="sn-days">{"".join(days)}</div>' if days else ""
    return f'<nav class="subnav">{layer_html}{days_html}</nav>'


def related_box(chapter, rel="ration"):
    """지역 챕터 상단의 관련 리소스 링크."""
    if chapter["kind"] != "region":
        return ""
    links = []
    if chapter.get("map"):
        links.append(f'<a href="../maps/{chapter["map"]}">🗺️ {chapter["map_title"]}</a>')
    links.append('<a href="../tracker/reservations.html">📋 예약 현황</a>')
    links.append('<a href="../chapters/03.html">📅 43일 일정표</a>')
    return f'<div class="related">{"".join(links)}</div>'


def collect_search(chapter, flat_tokens):
    label = f'{chapter["slug"]} {chapter["title"]}'
    SEARCH_INDEX.append({"t": chapter["title"], "c": f'챕터 {chapter["slug"]}',
                         "u": f'chapters/{chapter["slug"]}.html'})
    for tok in flat_tokens:
        name = tok["name"].strip()
        if not name or name.startswith("Layer"):
            continue
        SEARCH_INDEX.append({"t": name, "c": label,
                             "u": f'chapters/{chapter["slug"]}.html#{tok["id"]}'})


def collect_today(chapter, flat_tokens):
    """날짜 → URL 매핑. 지역 범위로 채우고 Day 섹션이 있으면 앵커로 덮어쓴다."""
    if chapter["kind"] != "region":
        return
    url = f'chapters/{chapter["slug"]}.html'
    d = chapter["start"]
    last = chapter["end"] if chapter["slug"] == "11" else chapter["end"] - timedelta(days=1)
    while d <= last:
        TODAY_MAP[d.isoformat()] = url
        d += timedelta(days=1)
    # Day 섹션 앵커는 별도로 모아 전체 범위 매핑이 끝난 뒤 덮어쓴다.
    # (뒤 챕터의 범위 채우기가 앞 챕터의 이동일 Day 앵커를 지우지 않도록)
    for tok in flat_tokens:
        dm = DAY_RE.search(tok["name"])
        if dm:
            day_date = date(2026, int(dm.group(2)), int(dm.group(3)))
            DAY_OVERRIDES[day_date.isoformat()] = f'{url}#{tok["id"]}'


def build_chapters():
    out_dir = SITE / "chapters"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug_by_file = {c["file"]: c["slug"] for c in CHAPTERS}

    for i, c in enumerate(CHAPTERS):
        text = (CHAPTER_DIR / c["file"]).read_text(encoding="utf-8")
        meta, body_md = parse_frontmatter(text)
        body, toc_tokens = md_convert(body_md)
        flat = flatten_tokens(toc_tokens)
        body = mark_layer_headings(wrap_tables(rewrite_md_links(body, slug_by_file)))

        collect_search(c, flat)
        collect_today(c, flat)

        meta_bits = []
        if c["kind"] == "region":
            meta_bits.append(f'{date_label(c["start"])} ~ {date_label(c["end"])} · {c["nights"]}박')
        if meta.get("version"):
            meta_bits.append(f'v{meta["version"]}')

        prev_link = next_link = ""
        if i > 0:
            p = CHAPTERS[i - 1]
            prev_link = f'<a href="{p["slug"]}.html">← {p["title"]}</a>'
        if i < len(CHAPTERS) - 1:
            n = CHAPTERS[i + 1]
            next_link = f'<a href="{n["slug"]}.html">{n["title"]} →</a>'
        pager = f'<nav class="pager">{prev_link}<span></span>{next_link}</nav>'

        content = related_box(c) + toc_html(toc_tokens) + body + pager
        (out_dir / f'{c["slug"]}.html').write_text(
            page(c["title"], content, rel="..",
                 topbar_title=f'{c["slug"]} · {c["title"]}',
                 meta_line=" · ".join(meta_bits),
                 subnav=chapter_subnav(c, flat)),
            encoding="utf-8")
        print(f'  챕터 {c["slug"]}: {c["file"]} → chapters/{c["slug"]}.html')


# ---------------------------------------------------------------- home

def build_home():
    stops = []
    for c in CHAPTERS:
        if c["kind"] != "region":
            continue
        map_link = (f' <a class="tl-map" href="maps/{c["map"]}">지도</a>'
                    if c.get("map") else "")
        stops.append(f"""<li>
  <div class="tl-dates">{date_label(c["start"])} – {date_label(c["end"])}<b>{c["nights"]}박</b></div>
  <div class="tl-body">
    <a class="tl-title" href="chapters/{c["slug"]}.html">{c["title"]}</a>{map_link}
  </div>
</li>""")

    intro_cards = "".join(
        f'<a class="card" href="chapters/{c["slug"]}.html">'
        f'<span class="card-num">{c["slug"]}</span>'
        f'<span class="card-title">{c["title"]}</span>'
        f'<span class="card-sub">{c["sub"]}</span></a>'
        for c in CHAPTERS if c["kind"] != "region")

    tool_cards = "".join(
        f'<a class="card card-alt" href="maps/{out}">'
        f'<span class="card-num">🗺️</span><span class="card-title">{title}</span>'
        f'<span class="card-sub">{sub}</span></a>'
        for _, out, title, sub in MAPS) + (
        '<a class="card card-alt" href="tracker/index.html">'
        '<span class="card-num">📋</span><span class="card-title">마스터 트래커</span>'
        '<span class="card-sub">일정 · 예약 · 이동 · 숙소 · 대시보드</span></a>')

    body = f"""<section class="hero">
  <h1>{SITE_TITLE}</h1>
  <p class="period">{TRIP_PERIOD}</p>
  <a href="#" class="nav-today btn-today">📍 오늘 일정 열기</a>
</section>
<h2>여정</h2>
<ol class="timeline">{''.join(stops)}</ol>
<h2>시작하기</h2>
<div class="grid">{intro_cards}</div>
<h2>도구</h2>
<div class="grid">{tool_cards}</div>
<p class="note">지도 배경 타일은 인터넷 연결 시 표시됩니다. 본문·마커·경로 목록은 오프라인에서도 열람됩니다.</p>
"""
    (SITE / "index.html").write_text(
        page("홈", body, rel=".", topbar_title=SITE_SHORT), encoding="utf-8")
    print("  홈 → index.html")


# ---------------------------------------------------------------- maps

def build_maps():
    out_dir = SITE / "maps"
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ASSETS / "vendor" / "leaflet", out_dir / "vendor" / "leaflet",
                    dirs_exist_ok=True)
    cards = []
    for src_name, out_name, title, sub in MAPS:
        text = (SOURCE / "maps" / src_name).read_text(encoding="utf-8")
        text = text.replace(
            "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css", "vendor/leaflet/leaflet.css")
        text = text.replace(
            "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js", "vendor/leaflet/leaflet.js")
        back = ('<a href="../maps/index.html" style="position:absolute;z-index:1100;right:12px;top:12px;'
                'background:#1f4e78;color:#fff;padding:7px 12px;border-radius:8px;'
                'font-size:13px;text-decoration:none;box-shadow:0 1px 6px rgba(0,0,0,.3)">← 지도 목록</a>')
        text = text.replace('<div id="map"></div>', f'<div id="map"></div>{back}', 1)
        (out_dir / out_name).write_text(text, encoding="utf-8")
        cards.append(f'<a class="card card-alt" href="{out_name}">'
                     f'<span class="card-num">🗺️</span><span class="card-title">{title}</span>'
                     f'<span class="card-sub">{sub}</span></a>')
        SEARCH_INDEX.append({"t": title, "c": "실행지도", "u": f"maps/{out_name}"})
        print(f"  지도: {src_name} → maps/{out_name}")

    body = ('<h1>실행지도</h1>'
            '<p class="meta">지역 동선·마커·경유지를 담은 인터랙티브 지도. '
            '배경 타일은 인터넷 연결 시 표시된다.</p>'
            f'<div class="grid">{"".join(cards)}</div>')
    (out_dir / "index.html").write_text(
        page("실행지도", body, rel=".."), encoding="utf-8")
    print("  지도 목록 → maps/index.html")


# ---------------------------------------------------------------- tracker

def format_cell(v):
    if v is None:
        return ""
    if hasattr(v, "hour"):  # datetime — 시각이 00:00이면 날짜만
        if (v.hour, v.minute, v.second) == (0, 0, 0):
            return v.strftime("%Y-%m-%d")
        return v.strftime("%Y-%m-%d %H:%M")
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def sheet_to_table(ws):
    rows = []
    for row in ws.iter_rows(values_only=True):
        cells = [format_cell(v) for v in row]
        if any(c.strip() for c in cells):
            rows.append(cells)
    if not rows:
        return ""
    # 선두의 제목 행(비어 있지 않은 셀이 1개뿐)은 캡션으로 분리
    captions = []
    while rows and sum(1 for c in rows[0] if c.strip()) == 1:
        captions.append(next(c for c in rows[0] if c.strip()))
        rows.pop(0)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    keep = [i for i in range(width) if any(r[i].strip() for r in rows)]
    rows = [[r[i] for i in keep] for r in rows]

    head = "".join(f"<th>{html.escape(c)}</th>" for c in rows[0])
    body_rows = []
    for r in rows[1:]:
        body_rows.append("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>")
    caption_html = "".join(f'<p class="meta">{html.escape(c)}</p>' for c in captions)
    return (f'{caption_html}<div class="table-wrap"><table><thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(body_rows)}</tbody></table></div>')


def build_tracker():
    out_dir = SITE / "tracker"
    out_dir.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.load_workbook(TRACKER_XLSX, data_only=True)

    def tabs_of(active):
        links = []
        for _, s, label in TRACKER_SHEETS:
            cls = ' class="active"' if s == active else ""
            links.append(f'<a href="{s}.html"{cls}>{label}</a>')
        return '<nav class="tabs">' + "".join(links) + "</nav>"

    cards = []
    for sheet_name, slug, label in TRACKER_SHEETS:
        if sheet_name not in wb.sheetnames:
            print(f"  경고: 시트 없음 — {sheet_name}")
            continue
        table = sheet_to_table(wb[sheet_name])
        body = f"<h1>{label}</h1>{tabs_of(slug)}{table}"
        (out_dir / f"{slug}.html").write_text(
            page(label, body, rel="..", topbar_title=f"트래커 · {label}",
                 meta_line="TP_Europe_Travel_Master_Tracker_v1.1.xlsx 기준"),
            encoding="utf-8")
        cards.append(f'<a class="card card-alt" href="{slug}.html">'
                     f'<span class="card-title">{label}</span>'
                     f'<span class="card-sub">{sheet_name}</span></a>')
        SEARCH_INDEX.append({"t": label, "c": "트래커", "u": f"tracker/{slug}.html"})
        print(f"  트래커: {sheet_name} → tracker/{slug}.html")

    body = ('<h1>마스터 트래커</h1>'
            '<p class="meta">TP_Europe_Travel_Master_Tracker_v1.1.xlsx에서 변환</p>'
            f'<div class="grid">{"".join(cards)}</div>')
    (out_dir / "index.html").write_text(
        page("마스터 트래커", body, rel="..", topbar_title="마스터 트래커"),
        encoding="utf-8")


# ---------------------------------------------------------------- data.js

def build_data_js():
    TODAY_MAP.update(DAY_OVERRIDES)
    data = {
        "tripStart": TRIP_START.isoformat(),
        "tripEnd": TRIP_END.isoformat(),
        "today": TODAY_MAP,
        "search": SEARCH_INDEX,
    }
    js = "window.GUIDE = " + json.dumps(data, ensure_ascii=False) + ";\n"
    (SITE / "assets" / "data.js").write_text(js, encoding="utf-8")
    print(f"  data.js: 날짜 매핑 {len(TODAY_MAP)}일 · 검색 인덱스 {len(SEARCH_INDEX)}항목")


# ---------------------------------------------------------------- checks

def check_links():
    broken = []
    for f in SITE.rglob("*.html"):
        for href in re.findall(r'href="([^"]+)"', f.read_text(encoding="utf-8")):
            if href.startswith(("http", "#", "mailto:")) or "${" in href:
                continue
            target = (f.parent / href.split("#")[0]).resolve()
            if not target.exists():
                broken.append(f"{f.relative_to(SITE)} → {href}")
    if broken:
        print("깨진 링크:")
        for b in broken:
            print("  " + b)
        sys.exit(1)
    print("링크 검사: 이상 없음")


def check_today_map():
    d = TRIP_START
    missing = []
    while d <= TRIP_END:
        if d.isoformat() not in TODAY_MAP:
            missing.append(d.isoformat())
        d += timedelta(days=1)
    if missing:
        print("날짜 매핑 누락:", ", ".join(missing))
        sys.exit(1)
    print(f"날짜 매핑 검사: {TRIP_START} ~ {TRIP_END} 전체 {len(TODAY_MAP)}일 이상 없음")


# ---------------------------------------------------------------- main

def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    (SITE / "assets").mkdir()
    shutil.copy(ASSETS / "style.css", SITE / "assets" / "style.css")
    shutil.copy(ASSETS / "nav.js", SITE / "assets" / "nav.js")

    print("챕터 빌드:")
    build_chapters()
    build_home()
    print("지도 빌드:")
    build_maps()
    print("트래커 빌드:")
    build_tracker()
    build_data_js()
    check_links()
    check_today_map()
    print(f"\n완료: {SITE} ({sum(1 for _ in SITE.rglob('*.html'))}개 HTML 페이지)")


if __name__ == "__main__":
    main()
