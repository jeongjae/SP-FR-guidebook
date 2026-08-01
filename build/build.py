#!/usr/bin/env python3
"""TP Europe Travel Guidebook — 정적 사이트 빌드 스크립트.

source/ 의 리더 에디션 MD, 실행지도 HTML, 마스터 트래커 xlsx를
site/ 아래의 순수 정적 HTML 사이트로 변환한다.

사용법:
    python3 build/build.py

필요 패키지: pip install markdown openpyxl
"""

import html
import re
import shutil
import sys
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
TRIP_ROUTE = "Barcelona 3박 → Girona 3박 → Nice 5박 → Aix 4박 → Luberon 4박 → Avignon 4박 → Lyon 4박 → Paris 15박"
TRIP_PERIOD = "2026-08-29 ~ 2026-10-10 · 43일"

# 챕터 매니페스트: (파일명, 슬러그, 카드 제목, 카드 부제)
CHAPTERS = [
    ("01_How_to_Use_This_Guidebook_Reader_v1.1.md", "01",
     "가이드북 사용법", "읽는 법과 기준 문서"),
    ("02_Whole_Trip_Experience_Highlights_Reader_v1.1.md", "02",
     "전체 여행 하이라이트", "43일의 경험 설계"),
    ("03_Whole_Trip_Master_Itinerary_Reader_v1.1.md", "03",
     "43일 Master Itinerary", "전체 일정 한눈에"),
    ("04_Barcelona_Sitges_Reader_v1.0.md", "04",
     "Barcelona · Sitges", "8/29 ~ 9/1 · 3박"),
    ("05_Girona_Collioure_Emporda_Reader_v1.0.md", "05",
     "Girona · Collioure · Empordà", "9/1 ~ 9/4 · 3박"),
    ("06_Nice_Cote_d_Azur_Reader_v1.1.md", "06",
     "Nice · Côte d’Azur", "9/4 ~ 9/9 · 5박"),
    ("07_Aix_en_Provence_Reader_v1.1.md", "07",
     "Aix-en-Provence", "9/9 ~ 9/13 · 4박"),
    ("08_Luberon_Farmhouse_Reader_v1.1.md", "08",
     "Luberon Farmhouse", "9/13 ~ 9/17 · 4박"),
    ("09_Avignon_Alpilles_Pont_du_Gard_Reader_v1.0.md", "09",
     "Avignon · Alpilles · Pont du Gard", "9/17 ~ 9/21 · 4박"),
    ("10_Lyon_Annecy_Reader_v1.0.md", "10",
     "Lyon · Annecy", "9/21 ~ 9/25 · 4박"),
    ("11_Paris_Long_Stay_Reader_v1.0.md", "11",
     "Paris Long Stay", "9/25 ~ 10/10 · 15박"),
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
                    TocExtension(slugify=slugify_unicode, toc_depth="1-2")],
        output_format="html5",
    )
    body = md.convert(text)
    return body, md.toc_tokens


def wrap_tables(body):
    body = body.replace("<table>", '<div class="table-wrap"><table>')
    return body.replace("</table>", "</table></div>")


def rewrite_md_links(body, slug_by_file):
    """챕터 간 .md 링크를 생성된 HTML 경로로 바꾼다."""
    def repl(match):
        target = match.group(1).split("#")[0]
        name = Path(target).name
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
    return (
        '<details class="toc"><summary>이 챕터의 목차</summary><ul>'
        + "".join(items) + "</ul></details>"
    )


def page(title, body, *, rel="..", header_extra="", meta_line=""):
    """공통 페이지 셸."""
    meta_html = f'<p class="meta">{meta_line}</p>' if meta_line else ""
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — {SITE_TITLE}</title>
<link rel="stylesheet" href="{rel}/assets/style.css">
</head>
<body>
<header class="topbar">
  <a class="home" href="{rel}/index.html">🏠 홈</a>
  <span class="site-name">{SITE_TITLE}</span>
  {header_extra}
</header>
<main>
{meta_html}
{body}
</main>
<footer>
  <p>{SITE_TITLE} · {TRIP_PERIOD}</p>
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------- chapters

def build_chapters():
    out_dir = SITE / "chapters"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug_by_file = {fname: slug for fname, slug, _, _ in CHAPTERS}

    for i, (fname, slug, card_title, _) in enumerate(CHAPTERS):
        text = (CHAPTER_DIR / fname).read_text(encoding="utf-8")
        meta, body_md = parse_frontmatter(text)
        body, toc_tokens = md_convert(body_md)
        body = wrap_tables(rewrite_md_links(body, slug_by_file))

        meta_bits = []
        if meta.get("travel_dates"):
            meta_bits.append(meta["travel_dates"])
        if meta.get("version"):
            meta_bits.append(f'v{meta["version"]}')
        meta_line = " · ".join(meta_bits)

        prev_link = next_link = ""
        if i > 0:
            p = CHAPTERS[i - 1]
            prev_link = f'<a href="{p[1]}.html">← {p[2]}</a>'
        if i < len(CHAPTERS) - 1:
            n = CHAPTERS[i + 1]
            next_link = f'<a href="{n[1]}.html">{n[2]} →</a>'
        pager = f'<nav class="pager">{prev_link}<span></span>{next_link}</nav>'

        content = toc_html(toc_tokens) + body + pager
        (out_dir / f"{slug}.html").write_text(
            page(card_title, content, rel="..", meta_line=meta_line),
            encoding="utf-8")
        print(f"  챕터 {slug}: {fname} → chapters/{slug}.html")


# ---------------------------------------------------------------- home

def build_home():
    cards = []
    for fname, slug, title, sub in CHAPTERS:
        cards.append(f"""<a class="card" href="chapters/{slug}.html">
  <span class="card-num">{slug}</span>
  <span class="card-title">{title}</span>
  <span class="card-sub">{sub}</span>
</a>""")

    map_cards = []
    for _, out_name, title, sub in MAPS:
        map_cards.append(f"""<a class="card card-alt" href="maps/{out_name}">
  <span class="card-num">🗺</span>
  <span class="card-title">{title}</span>
  <span class="card-sub">{sub}</span>
</a>""")

    tracker_cards = [f"""<a class="card card-alt" href="tracker/index.html">
  <span class="card-num">📋</span>
  <span class="card-title">마스터 트래커</span>
  <span class="card-sub">일정 · 예약 · 이동 · 숙소 · 대시보드</span>
</a>"""]

    body = f"""<section class="hero">
  <h1>{SITE_TITLE}</h1>
  <p class="period">{TRIP_PERIOD}</p>
  <p class="route">{TRIP_ROUTE}</p>
</section>
<h2>가이드북 챕터</h2>
<div class="grid">{''.join(cards)}</div>
<h2>실행지도 · 트래커</h2>
<div class="grid">{''.join(map_cards + tracker_cards)}</div>
<p class="note">지도 배경 타일은 인터넷 연결 시 표시됩니다. 오프라인에서도 마커·경로 목록과 본문은 모두 열람할 수 있습니다.</p>
"""
    html_text = page("홈", body, rel=".")
    # 홈은 사이트 이름이 hero에 있으므로 상단바 사이트명 중복 제거
    html_text = html_text.replace(f'<span class="site-name">{SITE_TITLE}</span>', "")
    (SITE / "index.html").write_text(html_text, encoding="utf-8")
    print("  홈 → index.html")


# ---------------------------------------------------------------- maps

def build_maps():
    out_dir = SITE / "maps"
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ASSETS / "vendor" / "leaflet", out_dir / "vendor" / "leaflet",
                    dirs_exist_ok=True)
    for src_name, out_name, title, _ in MAPS:
        text = (SOURCE / "maps" / src_name).read_text(encoding="utf-8")
        text = text.replace(
            "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css", "vendor/leaflet/leaflet.css")
        text = text.replace(
            "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js", "vendor/leaflet/leaflet.js")
        # 지도에서 사이트로 돌아가는 홈 버튼 삽입
        back = ('<a href="../index.html" style="position:absolute;z-index:1100;right:12px;top:12px;'
                'background:#1f4e78;color:#fff;padding:7px 12px;border-radius:8px;'
                'font-size:13px;text-decoration:none;box-shadow:0 1px 6px rgba(0,0,0,.3)">🏠 홈</a>')
        text = text.replace('<div id="map"></div>', f'<div id="map"></div>{back}', 1)
        (out_dir / out_name).write_text(text, encoding="utf-8")
        print(f"  지도: {src_name} → maps/{out_name} ({title})")


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
    # 전부 빈 열 제거
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
            page(label, body, rel="..",
                 meta_line="TP_Europe_Travel_Master_Tracker_v1.1.xlsx 기준"),
            encoding="utf-8")
        cards.append(f'<a class="card card-alt" href="{slug}.html">'
                     f'<span class="card-title">{label}</span>'
                     f'<span class="card-sub">{sheet_name}</span></a>')
        print(f"  트래커: {sheet_name} → tracker/{slug}.html")

    body = ('<h1>마스터 트래커</h1>'
            '<p class="meta">TP_Europe_Travel_Master_Tracker_v1.1.xlsx에서 변환</p>'
            f'<div class="grid">{"".join(cards)}</div>')
    (out_dir / "index.html").write_text(page("마스터 트래커", body, rel=".."),
                                        encoding="utf-8")


# ---------------------------------------------------------------- checks

def check_links():
    """생성된 HTML의 로컬 링크 대상이 존재하는지 검사한다."""
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


# ---------------------------------------------------------------- main

def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    (SITE / "assets").mkdir()
    shutil.copy(ASSETS / "style.css", SITE / "assets" / "style.css")

    print("챕터 빌드:")
    build_chapters()
    build_home()
    print("지도 빌드:")
    build_maps()
    print("트래커 빌드:")
    build_tracker()
    check_links()
    print(f"\n완료: {SITE} ({sum(1 for _ in SITE.rglob('*.html'))}개 HTML 페이지)")


if __name__ == "__main__":
    main()
