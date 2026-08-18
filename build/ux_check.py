#!/usr/bin/env python3
"""UX 검사 — 명암비 · 내비 구성 · 데일리 전수.

2026-08-18 에 마크업을 문자열로 고정하던 HIG 검사를 걷어냈다. 이 파일은 그
대체다. 마크업 모양이 아니라 **계산된 값**을 본다 — 그래서 디자인을 바꿔도
깨지지 않고, 야외에서 못 읽는 화면만 잡는다.

기준은 Apple HIG 최소치가 아니라 이 프로젝트 기준이다.
본문 7:1 · 보조 4.5:1 — 주광 아래에서 읽는 도구이기 때문이다.

    python3 build/ux_check.py            # 전체
    python3 build/ux_check.py --contrast # 명암비만 (site/ 없이도 돈다)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "build" / "assets" / "style.css"
SITE = ROOT / "site"

BODY_MIN = 7.0
SECONDARY_MIN = 4.5


# ---------------------------------------------------------------- 색 계산

def _srgb(channel: float) -> float:
    """sRGB 채널 하나를 선형광량으로. WCAG 2.x 정의 그대로."""
    c = channel / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _srgb(r) + 0.7152 * _srgb(g) + 0.0722 * _srgb(b)


def contrast(fg: str, bg: str) -> float:
    a, b = luminance(fg), luminance(bg)
    lo, hi = min(a, b), max(a, b)
    return (hi + 0.05) / (lo + 0.05)


# ---------------------------------------------------------------- 토큰 읽기

TOKEN_RE = re.compile(r"^\s*(--[a-z0-9-]+):\s*(#[0-9A-Fa-f]{3,8})\s*;", re.M)


def read_tokens(text: str) -> dict[str, str]:
    """:root 블록의 hex 토큰만. rgba()·blur() 같은 건 명암비 대상이 아니다."""
    return {m.group(1): m.group(2) for m in TOKEN_RE.finditer(text)}


# 검사할 조합 — (전경토큰, 배경토큰, 최소비, 설명)
# 여기 없는 토큰은 '면'에만 쓰는 색이다 (국기 원색·틴트 등).
PAIRS = [
    ("--text",    "--canvas",  BODY_MIN,      "본문 / 바탕"),
    ("--text",    "--surface", BODY_MIN,      "본문 / 카드"),
    ("--text-2",  "--canvas",  BODY_MIN,      "보조 본문 / 바탕"),
    ("--text-2",  "--surface", BODY_MIN,      "보조 본문 / 카드"),
    ("--muted",   "--canvas",  SECONDARY_MIN, "캡션·메타 / 바탕"),
    ("--muted",   "--surface", SECONDARY_MIN, "캡션·메타 / 카드"),
    ("--primary", "--canvas",  SECONDARY_MIN, "링크·강조 / 바탕"),
    ("--primary", "--surface", SECONDARY_MIN, "링크·강조 / 카드"),
    ("--on-primary", "--primary", SECONDARY_MIN, "버튼 글자 / 버튼 면"),
    ("--sig-alert-ink",   "--canvas",  BODY_MIN, "경고 글자 / 바탕"),
    ("--sig-alert-ink",   "--surface", BODY_MIN, "경고 글자 / 카드"),
    ("--sig-caution-ink", "--canvas",  BODY_MIN, "미확정 글자 / 바탕"),
    ("--sig-caution-ink", "--surface", BODY_MIN, "미확정 글자 / 카드"),
    ("--sig-ok-ink",      "--canvas",  BODY_MIN, "확정 글자 / 바탕"),
    ("--sig-ok-ink",      "--surface", BODY_MIN, "확정 글자 / 카드"),
    # 상단바는 앱 아이콘 색이다. 여기 글자가 안 읽히면 위치를 잃는다.
    ("--on-brand",    "--brand", BODY_MIN,      "상단바 글자 / 브랜드 면"),
    ("--brand-accent", "--brand", SECONDARY_MIN, "브랜드 강조 / 브랜드 면"),
]


def check_contrast() -> list[str]:
    text = CSS.read_text(encoding="utf-8")
    tokens = read_tokens(text)
    problems, rows = [], []
    for fg, bg, floor, label in PAIRS:
        if fg not in tokens or bg not in tokens:
            problems.append(f"토큰 없음: {fg} 또는 {bg} ({label})")
            continue
        ratio = contrast(tokens[fg], tokens[bg])
        ok = ratio >= floor
        rows.append(f"  {'OK ' if ok else 'FAIL'} {ratio:5.2f}:1  (≥{floor})  {label}"
                    f"  {tokens[fg]} on {tokens[bg]}")
        if not ok:
            problems.append(
                f"명암비 미달 {ratio:.2f}:1 < {floor}:1 — {label} "
                f"({fg}={tokens[fg]} on {bg}={tokens[bg]})")
    print("명암비:")
    print("\n".join(rows))

    # 지역 액센트 8종은 '면' 이자 글자다. 흰 글자를 얹으므로 흰색 대비를 본다.
    accents = {k: v for k, v in tokens.items() if k.startswith("--region-")}
    if accents:
        print("지역 액센트 (흰 글자 기준):")
        for name, value in sorted(accents.items()):
            ratio = contrast("#FFFFFF", value)
            ok = ratio >= SECONDARY_MIN
            print(f"  {'OK ' if ok else 'FAIL'} {ratio:5.2f}:1  {name} {value}")
            if not ok:
                problems.append(
                    f"지역 액센트 흰 글자 미달 {ratio:.2f}:1 — {name}={value}")
    return problems


# ---------------------------------------------------------------- 사이트 검사

TAB_RE = re.compile(r'<a[^>]*data-tab="([a-z]+)"')
EXPECTED_TABS = ["today", "schedule", "guide", "map", "prepare"]


def check_site() -> list[str]:
    problems = []
    if not SITE.exists():
        return ["site/ 가 없다 — 먼저 python3 build/build.py 를 돌린다."]

    pages = sorted(SITE.rglob("*.html"))

    # 1) 하단탭은 모든 페이지에서 정확히 5개, 같은 순서다.
    bad_tabs = []
    for path in pages:
        body = path.read_text(encoding="utf-8", errors="replace")
        if 'class="bottomnav"' not in body and "bottomnav" not in body:
            continue  # 리다이렉트 페이지엔 탭이 없다
        tabs = TAB_RE.findall(body)
        if tabs != EXPECTED_TABS:
            bad_tabs.append(f"{path.relative_to(SITE)}: {tabs}")
    if bad_tabs:
        problems.append(
            f"하단탭 구성이 어긋난 페이지 {len(bad_tabs)}건 "
            f"(기대: {EXPECTED_TABS}) — 예: {bad_tabs[0]}")
    else:
        print(f"하단탭: {len(pages)}쪽 전수 {EXPECTED_TABS}")

    # 2) 데일리 카드 43일 전수. 하나라도 비면 현장에서 그날이 없는 것이다.
    missing = [n for n in range(1, 44)
               if not (SITE / "daily" / f"day-{n:02d}.html").exists()]
    if missing:
        problems.append(f"데일리 카드 누락: {missing}")
    else:
        print("데일리 카드: 43일 전수 존재")

    # 3) 글자로만 있는 URL. 누를 수 없는 주소는 현장에서 손으로 옮겨 적어야
    #    한다는 뜻이고, 그러느니 없는 편이 낫다. 확인할 수 없는 근거는
    #    근거가 아니다. (사실 출처 286건이 실제로 그런 상태였다.)
    anchor = re.compile(r"<a\b[^>]*>.*?</a>", re.S | re.I)
    scripts = re.compile(r"<script.*?</script>|<style.*?</style>", re.S | re.I)
    bare_url = re.compile(r'(?:https?://|www\.)[^\s<>"\')\]]+')
    naked = {}
    for path in pages:
        body = scripts.sub(" ", path.read_text(encoding="utf-8", errors="replace"))
        text = re.sub(r"<[^>]+>", " ", anchor.sub(" ", body))
        for url in bare_url.findall(text):
            naked.setdefault(url, str(path.relative_to(SITE)))
    if naked:
        first = list(naked.items())[:3]
        problems.append(
            f"링크가 걸리지 않은 URL {len(naked)}종 — "
            + " · ".join(f"{u[:48]} ({p})" for u, p in first))
    else:
        print("링크: 글자로만 있는 URL 0건")

    # 4) 빈 href — 눌러도 제자리다
    for path in pages:
        if 'href=""' in path.read_text(encoding="utf-8", errors="replace"):
            problems.append(f"빈 href: {path.relative_to(SITE)}")
            break

    # 5) 뷰포트 설정 — 확대를 막으면 저시력 사용자가 못 쓴다.
    for path in pages:
        body = path.read_text(encoding="utf-8", errors="replace")
        if "user-scalable=no" in body or "maximum-scale=1" in body:
            problems.append(f"확대 차단 뷰포트: {path.relative_to(SITE)}")
            break

    return problems


def main() -> int:
    only_contrast = "--contrast" in sys.argv
    problems = check_contrast()
    if not only_contrast:
        problems += check_site()

    print()
    if problems:
        print(f"UX 검사 실패 — {len(problems)}건")
        for p in problems:
            print("  " + p)
        return 1
    print("UX 검사 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
