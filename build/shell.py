#!/usr/bin/env python3
"""페이지 셸과 공통 컴포넌트.

내비게이션은 레벨마다 정확히 하나만 맡는다. 스트립이 서로의 일을 하면
현장에서 어느 쪽을 눌러야 하는지 판단해야 하고, 그 판단은 비용이다.

    L0 전역   하단탭    오늘 · 전체 일정 · 가이드 · 지도 · 준비
    L1 위치   상단바    위치 경로(빵부스러기) + 검색
    L2 형제   탭 스트립 지금 묶음 안에서 옆으로

전체 메뉴(햄버거)는 두지 않는다. 홈이 여정을, 하단탭이 축을 맡는다.
같은 목록을 네 번째로 늘어놓으면 메뉴가 사이트의 사본이 되고 어느 쪽이
최신인지 알 수 없게 된다.
"""
from __future__ import annotations

import html
import json

SITE_TITLE = "유럽 43일 가이드북"
TRIP_PERIOD = "2026-08-29 — 2026-10-10"

# 하단탭 — 정확히 5개. 여행 중의 행동으로 나눈다.
TABS = [
    ("today",    "오늘",      "today",  "index.html"),
    ("schedule", "전체 일정",  "list",   "schedule.html"),
    ("guide",    "가이드",    "region", "guide/index.html"),
    ("map",      "지도",      "map",    "map/index.html"),
    ("prepare",  "준비",      "check",  "prepare/index.html"),
]


def esc(s) -> str:
    return html.escape(str(s if s is not None else ""))


def ic(name: str, cls: str = "") -> str:
    """아이콘. CSS 마스크라 페이지 무게가 0 이고 색은 currentColor 를 받는다."""
    extra = f" {cls}" if cls else ""
    return f'<b class="ic ic-only ic-{name}{extra}" aria-hidden="true"></b>'


def bottomnav(rel: str, active: str) -> str:
    items = []
    for key, label, icon, url in TABS:
        cur = ' aria-current="page"' if key == active else ""
        items.append(
            f'<a href="{rel}/{url}" data-tab="{key}"{cur}>{ic(icon)}'
            f'<span>{label}</span></a>')
    return ('<nav class="bottomnav" aria-label="주요 메뉴">\n  '
            + "\n  ".join(items) + "\n</nav>")


def crumbs(rel: str, trail: list[tuple[str, str | None]]) -> str:
    """위치 경로. 마지막 조각은 링크가 아니라 현재 위치다."""
    parts = []
    for i, (label, url) in enumerate(trail):
        sep = '<span class="sep" aria-hidden="true">›</span>' if i else ""
        if url:
            parts.append(f'{sep}<a href="{rel}/{url}">{esc(label)}</a>')
        else:
            parts.append(f"{sep}<b>{esc(label)}</b>")
    return f'<nav class="crumbs" aria-label="위치">{"".join(parts)}</nav>'


def tabs_strip(items: list[tuple[str, str, bool]]) -> str:
    """L2 형제 이동. (라벨, URL, 현재인가)"""
    if not items:
        return ""
    out = []
    for label, url, current in items:
        cur = ' aria-current="page"' if current else ""
        out.append(f'<a href="{url}"{cur}>{esc(label)}</a>')
    return f'<nav class="tabs" aria-label="하위 메뉴">{"".join(out)}</nav>'


def sec_head(label: str, title: str = "", more: tuple[str, str] | None = None,
             rule: bool = False) -> str:
    """SectionHeader. rule=True 는 editorial 변형 — 액센트 규칙으로 연다."""
    if rule:
        h = f"<h2>{esc(title)}</h2>" if title else ""
        return (f'<div class="sec-head-rule"><span class="label">{esc(label)}</span>'
                f"{h}</div>")
    left = f'<span class="label">{esc(label)}</span>'
    if title:
        left = f"<h2>{esc(title)}</h2>"
    right = f'<a href="{more[1]}">{esc(more[0])}</a>' if more else ""
    return f'<div class="sec-head">{left}{right}</div>'


def badge(kind: str, text: str) -> str:
    return f'<span class="badge badge-{kind}">{esc(text)}</span>'


GRADE_BADGE = {
    "essential": ("must", "필수"),
    "priority": ("neutral", "우선 추천"),
    "optional": ("neutral", "선택"),
    # 대체안은 기본 일정이 아니다 — 우천·피로 때 바꿔 넣는 자리다.
    "alternative": ("neutral", "대체"),
    "discouraged": ("neutral", "비추천"),
}


def alert(kind: str, body: str, icon: str = "alert") -> str:
    """AlertCard. 색만으로 뜻을 전하지 않는다 — 아이콘과 글자가 함께 간다."""
    return (f'<div class="alert-card alert-{kind}">{ic(icon)}'
            f"<div>{body}</div></div>")


def page(*, title: str, body: str, rel: str, tab: str,
         trail: list[tuple[str, str | None]] | None = None,
         region: str = "", country: str = "", subnav: str = "",
         description: str = "", extra_head: str = "",
         extra_scripts: str = "") -> str:
    """페이지 하나. 셸은 여기 한 곳에서만 만든다."""
    region_attr = f' data-region="{region}"' if region else ""
    band = (f'<div class="country-band" data-country="{country}" '
            f'role="presentation"></div>') if country and country != "none" else ""
    desc = (f'<meta name="description" content="{esc(description)}">\n'
            if description else "")
    trail_html = crumbs(rel, trail) if trail else '<span class="crumbs"></span>'

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#FAF6EF">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="유럽 가이드북">
<title>{esc(title)} — {SITE_TITLE}</title>
{desc}<link rel="manifest" href="{rel}/manifest.webmanifest">
<link rel="apple-touch-icon" href="{rel}/assets/pwa/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="{rel}/assets/pwa/icon-192.png">
{extra_head}<link rel="stylesheet" href="{rel}/assets/style.css">
</head>
<body{region_attr}>
<a href="#main" class="visually-hidden">본문으로 건너뛰기</a>
<header class="topbar">
  <button class="tb-back" type="button" aria-label="이전 페이지로" hidden>{ic("back")}</button>
  {trail_html}
  <button id="search-btn" type="button" aria-label="검색 열기" aria-expanded="false">{ic("search")}</button>
</header>
{band}
{subnav}
<div class="search-sheet" id="search-sheet" hidden role="dialog" aria-modal="true" aria-label="검색">
  <div class="search-bar">
    <input type="search" id="search-input" placeholder="장소 · 날짜 · 지역" autocomplete="off">
    <button type="button" id="search-close" aria-label="검색 닫기">{ic("close")}</button>
  </div>
  <div id="search-results" aria-live="polite"></div>
</div>
<main id="main">
{body}
</main>
<footer>
  <p>{SITE_TITLE} · {TRIP_PERIOD}</p>
  <p><a href="{rel}/about/credits.html">사진 저작자 표시 · 라이선스</a></p>
</footer>
{bottomnav(rel, tab)}
<script src="{rel}/assets/search-index.js" defer></script>
<script src="{rel}/assets/app.js" defer></script>
<script src="{rel}/assets/pwa.js" defer></script>{extra_scripts}
</body>
</html>
"""


def redirect(target: str, label: str) -> str:
    """옛 주소는 리다이렉트만 남는다. 404 를 늘리지 않는다.

    자바스크립트가 꺼져 있어도 meta refresh 로 넘어가고, 그것도 실패하면
    링크가 보인다 — 현장에서 막다른 화면을 만들지 않는다.
    """
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url={target}">
<link rel="canonical" href="{target}">
<title>{esc(label)}로 이동</title>
</head>
<body>
<p><a href="{target}">{esc(label)}로 이동합니다</a></p>
<script>location.replace({json.dumps(target)});</script>
</body>
</html>
"""
