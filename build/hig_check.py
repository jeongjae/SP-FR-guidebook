#!/usr/bin/env python3
"""Apple HIG 적합성 검사 — 기계로 확인 가능한 부분만.

명료함·경의·깊이 같은 원칙은 여기서 확인되지 않는다. 이 검사가 통과했다고
HIG 를 만족한다고 말하면 안 된다. 아래 목록만 봤다고 말해야 한다.

  1. 터치 타깃      컨트롤은 44×44pt 이상 (HIG Layout)
  2. 글자 크기      렌더된 텍스트 11pt 이상 (HIG Typography 최소)
  3. 명암비         본문 7:1 · 보조 4.5:1 이상
                    HIG 최소치가 아니라 이 프로젝트 기준이다. 야외 주광에서
                    읽는 도구라 Apple 의 secondaryLabel 계열로는 모자란다.
  4. 안전영역       하단 고정 바가 env(safe-area-inset-bottom) 을 반영
  5. 리플로         320px 에서 가로 스크롤 0
  6. 뷰포트         viewport-fit=cover

사용: python3 build/hig_check.py [--all]
      기본은 페이지 유형별 표본. --all 은 전체 페이지.
"""
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

SITE = Path(__file__).resolve().parent.parent / "site"
CHROME = "/opt/pw-browsers/chromium"

# 유형별 표본 — 셸·본문·표·카드·지도가 모두 들어가게 고른다
SAMPLE = [
    "index.html", "regions.html", "credits.html",
    "chapters/paris/index.html", "chapters/paris/food.html",
    "chapters/paris/day-37.html", "chapters/girona/places.html",
    "chapters/itinerary.html",
    "daily/index.html", "daily/day-21.html", "daily/day-01.html",
    "topics/index.html", "topics/food.html", "topics/reverify.html",
    "places/index.html", "places/palais-des-papes.html",
    "maps/index.html", "maps/offline.html",
    "tracker/index.html", "tracker/dashboard.html",
]

# 본문 안의 문장 링크는 컨트롤이 아니다. 크롬·카드·칩만 44pt 를 요구한다.
CONTROL_SEL = (
    ".topbar a, .topbar button, .bottomnav a, .subnav a, .coords a, "
    ".card, .rg-card .card-title, .tp-item, .pl-day, .day-jump a, "
    ".daily-item, .related a, .pager a, #back-top, #sheet-close"
)

JS = r"""
(sel) => {
  const out = {targets: [], small: [], contrast: [], scroll: 0};
  const vw = document.documentElement.clientWidth;
  out.scroll = document.documentElement.scrollWidth - vw;

  const vis = el => {
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    return s.display !== 'none' && s.visibility !== 'hidden' &&
           s.opacity !== '0' && r.width > 0 && r.height > 0;
  };
  const label = el => (el.textContent || el.getAttribute('aria-label') || el.id ||
                       el.className || el.tagName).toString().trim().slice(0, 40);

  /* 1. 터치 타깃 */
  for (const el of document.querySelectorAll(sel)) {
    if (!vis(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 43.5 || r.height < 43.5)
      out.targets.push({t: label(el), w: Math.round(r.width), h: Math.round(r.height),
                        c: el.className.toString().slice(0, 30)});
  }

  /* 색 파싱 · 상대휘도 · 명암비 */
  /* Chromium 은 color-mix 를 color(srgb 0..1 / a) 로 돌려준다.
     0..255 로 읽으면 명암비가 통째로 틀린다. 접두어를 보고 환산한다. */
  const rgb = s => {
    const v = (s.match(/[\d.]+/g) || []).map(Number);
    if (!v.length) return v;
    if (/^color\(/.test(s)) {
      const a = v.length > 3 ? v[3] : 1;
      return [v[0] * 255, v[1] * 255, v[2] * 255, a];
    }
    return v;
  };
  const lin = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
  const lum = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
  const over = (fg, bg) => {                       /* 알파 합성 */
    const a = fg.length > 3 ? fg[3] : 1;
    return [0, 1, 2].map(i => fg[i] * a + bg[i] * (1 - a));
  };
  const bgOf = el => {
    let cur = el, acc = null;
    while (cur && cur !== document.documentElement) {
      const c = rgb(getComputedStyle(cur).backgroundColor);
      if (c.length && (c.length < 4 || c[3] > 0)) {
        acc = acc === null ? c : over(acc, c);
        if (c.length < 4 || c[3] === 1) return acc.slice(0, 3);
      }
      cur = cur.parentElement;
    }
    return acc ? acc.slice(0, 3) : [255, 255, 255];
  };
  const ratio = (a, b) => {
    const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p);
    return (x + 0.05) / (y + 0.05);
  };

  /* 2·3. 글자 크기 · 명암비 — 텍스트를 직접 가진 요소만 */
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  let n;
  while ((n = walker.nextNode())) {
    const txt = n.textContent.trim();
    if (!txt) continue;
    const el = n.parentElement;
    if (!el || seen.has(el) || !vis(el)) continue;
    if (el.closest('script, style, noscript')) continue;
    seen.add(el);
    const s = getComputedStyle(el);
    const size = parseFloat(s.fontSize);
    if (size < 11) out.small.push({t: txt.slice(0, 30), px: size, c: el.className.toString().slice(0, 30)});
    const fg = over(rgb(s.color), bgOf(el));
    const r = ratio(fg, bgOf(el));
    /* 하한을 두 가지로 나눈다.
       본문(main 안의 읽는 글) 7:1  — 야외 주광에서 읽는 도구다. 이 프로젝트 기준.
       크롬(내비·탭·칩)     4.5:1 — WCAG AA. 짧고 위치로도 식별된다. */
    const inMain = !!el.closest('main');
    const need = inMain ? 7.0 : 4.5;
    if (r < need)
      out.contrast.push({t: txt.slice(0, 30), r: Math.round(r * 100) / 100,
                         need, px: size, c: el.className.toString().slice(0, 30)});
  }
  return out;
}
"""

SAFE_AREA_JS = r"""
() => {
  const nav = document.querySelector('.bottomnav');
  if (!nav) return {ok: true, why: 'bottomnav 없음'};
  const pb = getComputedStyle(nav).paddingBottom;
  return {ok: true, pb};
}
"""


def check_page(pg, rel, width, problems):
    pg.goto("file://" + str((SITE / rel).resolve()))
    pg.wait_for_timeout(180)
    r = pg.evaluate(JS, CONTROL_SEL)
    tag = f"{rel} @{width}"
    if r["scroll"] > 0:
        problems.append(f"[리플로] {tag}: 가로 스크롤 +{r['scroll']}px")
    for t in r["targets"][:6]:
        problems.append(f"[터치타깃] {tag}: {t['w']}×{t['h']}px  \"{t['t']}\" .{t['c']}")
    for s in r["small"][:6]:
        problems.append(f"[글자크기] {tag}: {s['px']}px  \"{s['t']}\" .{s['c']}")
    for c in r["contrast"][:6]:
        problems.append(f"[명암비] {tag}: {c['r']}:1 (필요 {c['need']}) "
                        f"{c['px']}px  \"{c['t']}\" .{c['c']}")


def main():
    pages = SAMPLE
    if "--all" in sys.argv:
        pages = sorted(str(p.relative_to(SITE)) for p in SITE.rglob("*.html"))
    pages = [p for p in pages if (SITE / p).exists()]
    # 리다이렉트 스텁은 열자마자 meta refresh 로 넘어간다. 평가 도중 이동하면
    # "Execution context was destroyed" 로 검사기가 죽는다 — 사이트 문제가
    # 아니라 검사기 문제다. 검사할 화면도 없으니 목록에서 뺀다.
    stubs = [p for p in pages
             if 'http-equiv="refresh"' in (SITE / p).read_text(encoding="utf-8")[:800]]
    pages = [p for p in pages if p not in set(stubs)]
    if not pages:
        print("검사할 페이지가 없다. 먼저 build.py 를 돌려라.")
        return 1

    problems = []

    # 6. 뷰포트 — 안전영역을 쓰려면 viewport-fit=cover 가 있어야 한다
    for p in pages:
        head = (SITE / p).read_text(encoding="utf-8")[:1200]
        m = re.search(r'<meta name="viewport" content="([^"]+)"', head)
        if not m:
            problems.append(f"[뷰포트] {p}: viewport 메타 없음")
        elif "viewport-fit=cover" not in m.group(1):
            problems.append(f"[뷰포트] {p}: viewport-fit=cover 없음")

    # 4. 안전영역 — 하단 고정 바가 inset 을 반영하는지 CSS 원본으로 본다
    css = (Path(__file__).resolve().parent / "assets" / "style.css").read_text(encoding="utf-8")
    if "safe-area-inset-bottom" not in css:
        problems.append("[안전영역] .bottomnav 가 env(safe-area-inset-bottom) 을 쓰지 않는다")

    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        # 라이트·다크 양쪽을 본다. 다크에서 신호색이 밝아지면 그 위 글자가 뒤집혀야 한다.
        for scheme in ("light", "dark"):
            for w, h in ((320, 568), (390, 844)):
                pg = b.new_page(viewport={"width": w, "height": h},
                                color_scheme=scheme)
                for rel in pages:
                    check_page(pg, rel, f"{w}·{scheme}", problems)
                pg.close()
        b.close()

    if problems:
        print(f"HIG 검사 실패 — {len(problems)}건")
        for p in problems[:40]:
            print("  " + p)
        if len(problems) > 40:
            print(f"  … 외 {len(problems) - 40}건")
        return 1
    print(f"HIG 검사: {len(pages)}쪽 × 2폭 × 라이트/다크 — 터치타깃 · 글자크기 · 명암비 · "
          f"안전영역 · 리플로 · 뷰포트 이상 없음")
    if stubs:
        print(f"  (리다이렉트 스텁 {len(stubs)}쪽은 검사하지 않았다)")
    print("  (명료함·경의·깊이 같은 원칙은 이 검사로 확인되지 않는다)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
