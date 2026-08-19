#!/usr/bin/env python3
"""뷰포트 검사 — 가로 오버플로 · 터치 타깃 · 겹침.

야외에서 한 손으로 쓰는 도구다. 가로로 흐르는 화면은 현장에서 못 쓴다.
마크업을 문자열로 고정하지 않고 **실제로 렌더해서 측정한다** — 그래서
디자인을 바꿔도 이 검사는 살아 있다.

    python3 build/viewport_check.py [site_dir]
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent

# 390 이 여행 중 핵심 뷰포트다. 360 은 하한, 위로 태블릿·데스크톱.
VIEWPORTS = [360, 390, 430, 768, 1024, 1440]
TAP_MIN = 44          # HIG 최소 터치 타깃
FONT_MIN = 11         # 이보다 작은 글자는 주광에서 못 읽는다

MEASURE = """() => {
  const de = document.documentElement;
  const overflow = de.scrollWidth - de.clientWidth;
  const wide = [];
  if (overflow > 1) {
    document.querySelectorAll('body *').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.right > de.clientWidth + 1) {
        const cs = getComputedStyle(el);
        if (cs.position === 'fixed') return;
        // 스스로 가로 스크롤을 처리하는 상자는 정상이다
        let p = el.parentElement, contained = false;
        while (p && p !== document.body) {
          const pcs = getComputedStyle(p);
          if (pcs.overflowX === 'auto' || pcs.overflowX === 'scroll') { contained = true; break; }
          p = p.parentElement;
        }
        if (!contained) wide.push(el.tagName.toLowerCase()
          + (el.className && typeof el.className === 'string'
             ? '.' + el.className.trim().split(/\\s+/).slice(0,2).join('.') : '')
          + ' →' + Math.round(r.right));
      }
    });
  }
  const small = [];
  document.querySelectorAll('a, button, summary, input').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    if (getComputedStyle(el).visibility === 'hidden') return;
    // 건너뛰기 링크는 포커스 전까지 1x1 이다 — 표준 기법이라 대상이 아니다
    if (el.classList.contains('visually-hidden')) return;
    // 카드 링크는 ::after 가 카드 전체를 덮는다 — 실제 타깃은 카드다
    if (el.classList.contains('card-link')) {
      const card = el.closest('.card');
      if (card && card.getBoundingClientRect().height >= 44) return;
    }
    if (r.height < 44 - 0.5 || r.width < 20) {
      // 본문 안 인라인 링크는 문장의 일부라 44 를 요구하지 않는다
      const inProse = el.closest('.prose, .crumbs, .metarow, footer, .tl-note, table, .meta');
      if (!inProse) small.push(el.tagName.toLowerCase()
        + (el.className && typeof el.className === 'string'
           ? '.' + el.className.trim().split(/\\s+/)[0] : '')
        + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
    }
  });
  const tiny = [];
  document.querySelectorAll('body *').forEach(el => {
    if (!el.childNodes.length) return;
    const hasText = Array.from(el.childNodes)
      .some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
    if (!hasText) return;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs < 11) tiny.push(el.tagName.toLowerCase() + ' ' + fs + 'px');
  });
  return { overflow, wide: [...new Set(wide)].slice(0, 6),
           small: [...new Set(small)].slice(0, 6),
           tiny: [...new Set(tiny)].slice(0, 4) };
}"""


def main() -> int:
    # 상대경로면 as_uri() 가 깨진다 — CI 는 인자 없이 부른다.
    site = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else \
        Path(os.environ.get("SPFR_SITE_DIR") or (ROOT / "site")).resolve()
    pages = ["index.html", "schedule.html", "guide/index.html",
             "guide/barcelona.html", "daily/day-02.html", "daily/day-12.html",
             "places/sagrada-familia.html", "places/sant-pau-recinte-modernista.html",
             "map/index.html", "map/barcelona.html", "prepare/index.html"]
    problems = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for width in VIEWPORTS:
            page = browser.new_page(viewport={"width": width, "height": 844},
                                    device_scale_factor=2)
            for rel in pages:
                f = site / rel
                if not f.exists():
                    problems.append(f"{rel}: 파일 없음")
                    continue
                page.goto(f.as_uri(), wait_until="load")

                # 스타일이 붙었는지 먼저 본다. CSS 가 아직 안 쓰인 상태에서
                # 재면 모든 요소가 기본 크기라 가짜 실패가 쏟아지고, 그 소음이
                # 진짜 문제를 덮는다. (빌드와 검사가 겹치면 실제로 그랬다.)
                styled = page.evaluate(
                    "() => getComputedStyle(document.body).backgroundColor")
                if styled in ("rgba(0, 0, 0, 0)", "rgb(255, 255, 255)"):
                    problems.append(
                        f"{rel}: CSS 가 적용되지 않은 채 렌더됐다 — "
                        f"빌드가 끝난 뒤 다시 돌려라")
                    continue

                r = page.evaluate(MEASURE)
                if r["overflow"] > 1:
                    problems.append(
                        f"{width}px {rel}: 가로 오버플로 {r['overflow']}px "
                        f"— {', '.join(r['wide']) or '원인 미상'}")
                if r["small"]:
                    problems.append(
                        f"{width}px {rel}: 터치 타깃 44pt 미만 — "
                        f"{', '.join(r['small'])}")
                if r["tiny"]:
                    problems.append(
                        f"{width}px {rel}: 글자 11px 미만 — {', '.join(r['tiny'])}")
            page.close()
        browser.close()

    print(f"뷰포트 {VIEWPORTS} × 페이지 {len(pages)}개")
    if problems:
        print(f"\n문제 {len(problems)}건:")
        for p in problems[:30]:
            print("  " + p)
        return 1
    print("가로 오버플로 0 · 터치 타깃 44pt 이상 · 글자 11px 이상 — 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
