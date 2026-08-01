#!/usr/bin/env python3
"""
가이드북 페이지 빌더 — 챕터 05 프로토타입

설계 의도
  기존: 큰 마크다운 1개 → HTML 1장 + 앵커
  변경: 마크다운 소스 몇 개 → HTML 여러 장

  authoring 파일 수 ≠ output 페이지 수.
  places.md 하나를 편집하면 방문지 페이지 11장이 나온다.
  각 페이지가 독립 URL을 가지므로 사진·링크·지도를 자유롭게 붙일 수 있다.

의존성 없음. python3 build.py 로 실행.
"""

import json, os, re, shutil, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content", "girona")
DIST = os.path.join(ROOT, "dist")
OUT = os.path.join(DIST, "chapters", "girona")


# ────────────────────────────────────────────────────────────
# 1. 최소 마크다운 변환기 (의존성 0)
# ────────────────────────────────────────────────────────────

def inline(t):
    t = t.replace(PIPE, "|")
    t = H.escape(t, quote=False)
    t = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)',
               lambda m: f'<figure class="fig"><img src="{m.group(2)}" alt="{m.group(1)}" loading="lazy">'
                         + (f'<figcaption>{m.group(3)}</figcaption>' if m.group(3) else '')
                         + '</figure>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    # 배지 문법:  {{badge:pending|미확정}}  {{badge:p0|P0 연결}}
    t = re.sub(r'\{\{badge:([a-z0-9]+)\|([^}]+)\}\}',
               r'<span class="badge badge-\1">\2</span>', t)
    # 등급 문법:  {{grade:essential|필수}}
    t = re.sub(r'\{\{grade:([a-z]+)\|([^}]+)\}\}',
               r'<span class="grade grade-\1">\2</span>', t)
    # 안전장치 — 남은 VISUAL 토큰 제거
    t = re.sub(r'\{\{VISUAL:[^}]*\}\}\s*', '', t)
    return t


PIPE = "\x00PIPE\x00"


def protect(t):
    """{{...}} 토큰 안의 | 를 표 구분자로 오인하지 않도록 보호."""
    return re.sub(r'\{\{[^}]*\}\}', lambda m: m.group(0).replace("|", PIPE), t)


def md(src):
    src = protect(src)
    out, lines, i = [], src.split("\n"), 0
    while i < len(lines):
        ln = lines[i]

        if not ln.strip():
            i += 1; continue

        # 표
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r'^\s*\|[\s:\-|]+\|\s*$', lines[i+1]):
            head = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append('<div class="table-wrap"><table><thead><tr>'
                       + "".join(f"<th>{inline(c)}</th>" for c in head)
                       + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows)
                       + "</tbody></table></div>")
            continue

        # 인용 (관람 요령 블록)
        if ln.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].strip()); i += 1
            out.append('<blockquote class="tip">' + md("\n".join(buf)) + "</blockquote>")
            continue

        # 헤딩
        m = re.match(r'^(#{1,4})\s+(.*)$', ln)
        if m:
            lv = len(m.group(1))
            txt = m.group(2).strip()
            slug = re.sub(r'[^\w가-힣]+', '-', txt).strip('-').lower()
            out.append(f'<h{lv} id="{slug}">{inline(txt)}</h{lv}>')
            i += 1; continue

        # 구분선
        if re.match(r'^-{3,}$', ln.strip()):
            out.append("<hr>"); i += 1; continue

        # 목록
        if re.match(r'^\s*[-*]\s+', ln):
            items = []
            while i < len(lines) and re.match(r'^\s*[-*]\s+', lines[i]):
                items.append(inline(re.sub(r'^\s*[-*]\s+', '', lines[i]))); i += 1
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>")
            continue
        if re.match(r'^\s*\d+\.\s+', ln):
            items = []
            while i < len(lines) and re.match(r'^\s*\d+\.\s+', lines[i]):
                items.append(inline(re.sub(r'^\s*\d+\.\s+', '', lines[i]))); i += 1
            out.append("<ol>" + "".join(f"<li>{x}</li>" for x in items) + "</ol>")
            continue

        # 문단
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,4}\s|>|\||\s*[-*]\s|\s*\d+\.\s|-{3,}$)', lines[i]):
            buf.append(lines[i]); i += 1
        if buf:
            out.append("<p>" + inline(" ".join(buf)) + "</p>")
    return "\n".join(out)


# ────────────────────────────────────────────────────────────
# 2. 소스 분할 — 파일 1개 → 페이지 N개
# ────────────────────────────────────────────────────────────

def split_pages(path):
    """`=== slug | 제목 | 부제` 마커로 페이지를 나눈다."""
    if not os.path.exists(path):
        return []
    raw = open(path, encoding="utf-8").read()
    parts = re.split(r'^===\s*(.+?)\s*$', raw, flags=re.M)
    pages = []
    for j in range(1, len(parts), 2):
        head = [x.strip() for x in parts[j].split("|")]
        slug = head[0]
        title = head[1] if len(head) > 1 else slug
        sub = head[2] if len(head) > 2 else ""
        pages.append({"slug": slug, "title": title, "sub": sub, "body": parts[j + 1].strip()})
    return pages


# ────────────────────────────────────────────────────────────
# 3. 템플릿
# ────────────────────────────────────────────────────────────

def shell(meta, title, sub, body, crumbs, prev=None, nxt=None, rel="../.."):
    nav = "".join(
        f'<a href="{c["href"]}">{H.escape(c["label"])}</a>' if c.get("href")
        else f'<span>{H.escape(c["label"])}</span>'
        for c in crumbs)
    pager = ""
    if prev or nxt:
        pager = '<nav class="pager">' \
            + (f'<a href="{prev["href"]}">◂ {H.escape(prev["label"])}</a>' if prev else "<span></span>") \
            + (f'<a href="{nxt["href"]}">{H.escape(nxt["label"])} ▸</a>' if nxt else "<span></span>") \
            + "</nav>"
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{H.escape(title)} — {H.escape(meta['chapterTitle'])}</title>
<link rel="stylesheet" href="{rel}/assets/style.css">
</head>
<body data-rel="{rel}">
<header class="topbar">
  <button id="menu-btn" aria-label="메뉴 열기">☰</button>
  <a class="tb-title" href="{rel}/index.html">유럽 43일 가이드북</a>
  <nav class="tb-links">
    <a href="{rel}/chapters/03.html">일정</a>
    <a href="{rel}/maps/index.html">지도</a>
    <a href="{rel}/tracker/index.html">트래커</a>
  </nav>
</header>

<nav class="crumbs" aria-label="현재 위치">{nav}</nav>

<main>
<header class="pagehead">
  <p class="eyebrow">{H.escape(meta['eyebrow'])}</p>
  <h1>{H.escape(title)}</h1>
  {f'<p class="sub">{H.escape(sub)}</p>' if sub else ''}
</header>

{body}

{pager}
</main>

<footer>
  <p>{H.escape(meta['chapterTitle'])} · {H.escape(meta['dates'])}</p>
</footer>

<nav class="bottomnav" aria-label="주요 메뉴">
  <a href="{rel}/index.html"><b>◉</b><span>오늘</span></a>
  <a href="{rel}/chapters/03.html"><b>▤</b><span>일정</span></a>
  <a href="{rel}/chapters/girona/index.html"><b>◇</b><span>지역</span></a>
  <a href="{rel}/maps/girona.html"><b>⌖</b><span>지도</span></a>
  <a href="{rel}/tracker/index.html"><b>▦</b><span>트래커</span></a>
</nav>
<button id="back-top" aria-label="맨 위로">↑</button>
</body>
</html>
"""


def card(href, num, title, sub, cls=""):
    eyebrow = f'<span class="card-num">{H.escape(num)}</span>' if num else ""
    return (f'<a class="card {cls}" href="{href}">{eyebrow}'
            f'<span class="card-title">{H.escape(title)}</span>'
            f'<span class="card-sub">{H.escape(sub)}</span></a>')


# ────────────────────────────────────────────────────────────
# 4. 빌드
# ────────────────────────────────────────────────────────────

def build():
    meta = json.load(open(os.path.join(CONTENT, "meta.json"), encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)

    places = split_pages(os.path.join(CONTENT, "places.md"))
    days = split_pages(os.path.join(CONTENT, "days.md"))
    topics = split_pages(os.path.join(CONTENT, "topics.md"))

    base = [{"label": "홈", "href": "../../index.html"},
            {"label": meta["short"], "href": "index.html"}]

    # ── 방문지 페이지 ──
    for k, p in enumerate(places):
        crumbs = base + [{"label": "방문지", "href": "index.html#places"}, {"label": p["title"]}]
        prev = {"href": f'place-{places[k-1]["slug"]}.html', "label": places[k-1]["title"]} if k else None
        nxt = {"href": f'place-{places[k+1]["slug"]}.html', "label": places[k+1]["title"]} if k + 1 < len(places) else None
        open(os.path.join(OUT, f'place-{p["slug"]}.html'), "w", encoding="utf-8").write(
            shell(meta, p["title"], p["sub"], md(p["body"]), crumbs, prev, nxt))

    # ── 일자 페이지 ──
    for k, d in enumerate(days):
        crumbs = base + [{"label": "일정", "href": "index.html#days"}, {"label": d["title"]}]
        prev = {"href": f'{days[k-1]["slug"]}.html', "label": days[k-1]["title"]} if k else None
        nxt = {"href": f'{days[k+1]["slug"]}.html', "label": days[k+1]["title"]} if k + 1 < len(days) else None
        open(os.path.join(OUT, f'{d["slug"]}.html'), "w", encoding="utf-8").write(
            shell(meta, d["title"], d["sub"], md(d["body"]), crumbs, prev, nxt))

    # ── 주제 페이지 ──
    for t in topics:
        crumbs = base + [{"label": t["title"]}]
        open(os.path.join(OUT, f'{t["slug"]}.html'), "w", encoding="utf-8").write(
            shell(meta, t["title"], t["sub"], md(t["body"]), crumbs))

    # ── 챕터 허브 ──
    intro = open(os.path.join(CONTENT, "intro.md"), encoding="utf-8").read()
    body = [md(intro)]

    body.append('<h2 id="days">일정</h2><div class="grid">')
    for d in days:
        body.append(card(f'{d["slug"]}.html', d["title"].split("·")[1].strip() if "·" in d["title"] else "",
                         d["title"], d["sub"]))
    body.append("</div>")

    body.append('<h2 id="places">방문지</h2>'
                '<p class="note">일정에 포함된 곳. 각 페이지에 관람 요령과 실용 정보가 있다.</p>'
                '<div class="grid">')
    for p in places:
        body.append(card(f'place-{p["slug"]}.html', "", p["title"], p["sub"]))
    body.append("</div>")

    body.append('<h2 id="topics">주제별</h2><div class="grid">')
    for t in topics:
        body.append(card(f'{t["slug"]}.html', "", t["title"], t["sub"], "card-alt"))
    body.append("</div>")

    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
        shell(meta, meta["chapterTitle"], meta["dates"], "\n".join(body),
              [{"label": "홈", "href": "../../index.html"}, {"label": meta["short"]}]))

    n = len(places) + len(days) + len(topics) + 1
    print(f"완료: {n}개 페이지 → {OUT}")
    print(f"  방문지 {len(places)} · 일자 {len(days)} · 주제 {len(topics)} · 허브 1")


if __name__ == "__main__":
    build()
