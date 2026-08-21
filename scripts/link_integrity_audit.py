#!/usr/bin/env python3
"""링크 무결성 전수감사 — 내부·외부 참조와 링크 가시성.

빌드 산출물과 원본 데이터를 대조해 다음을 전수 검사한다.

  A. 고아 콘텐츠   장소 페이지가 있는데 본문 어디에서도 링크되지 않는 것
  B. 미실현 참조   daily-card 의 place_ref 가 링크로 렌더되지 않는 것
  C. 링크 가시성   밑줄·색이 없어 클릭 가능함을 알 수 없는 링크
  D. 가이드 누락   지역 페이지가 표시 상한 때문에 빠뜨린 필수 장소
  E. 외부 링크     끊긴 링크·rel=noopener 누락

내비게이션(상단바·하단탭·꼬리말·탭 스트립)은 모든 페이지에 있으므로
'본문 링크' 집계에서 제외한다. 축은 목록을 맡고 본문을 갖지 않는다는
정보구조 원칙에 따라, 축에서만 닿는 것은 연결로 치지 않는다.

사용:
    SPFR_SITE_DIR=<빌드경로> python3 scripts/link_integrity_audit.py [--out DIR]
    (--out 없으면 저장소 루트에 LINK_AUDIT_*.csv 를 쓴다)
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = re.compile(r"<(nav|footer|header)\b.*?</\1>", re.S)
TABS = re.compile(r'<div class="tabs".*?</div>', re.S)
ANCHOR = re.compile(r'<a\b([^>]*)href="([^"]+)"([^>]*)>')
REFRESH = 'http-equiv="refresh"'


def load_pages(site: Path) -> tuple[dict[str, str], dict[str, str]]:
    pages, redirects = {}, {}
    for path in site.rglob("*.html"):
        rel = path.relative_to(site).as_posix()
        html = path.read_text(encoding="utf-8", errors="replace")
        if REFRESH in html:
            m = re.search(r"url=([^\"']+)", html)
            redirects[rel] = m.group(1) if m else ""
        else:
            pages[rel] = html
    return pages, redirects


def resolve(rel: str, href: str) -> str | None:
    if href.startswith(("http://", "https://", "#", "mailto:", "tel:", "javascript:")):
        return None
    base = os.path.dirname(rel)
    target = os.path.normpath(os.path.join(base, href.split("#")[0]))
    return target.replace("\\", "/")


def body_html(html: str) -> str:
    """내비게이션을 걷어낸 본문. 축(chrome)에서만 닿는 링크는 연결이 아니다."""
    return TABS.sub(" ", CHROME.sub(" ", html))


def build_graph(pages, redirects):
    body_in = defaultdict(set)
    edges = []
    external = defaultdict(set)
    broken = []
    for rel, html in pages.items():
        for scope, source in (("body", body_html(html)), ("all", html)):
            for m in ANCHOR.finditer(source):
                href = m.group(2)
                if href.startswith(("http://", "https://")):
                    if scope == "body":
                        external[href].add(rel)
                    continue
                target = resolve(rel, href)
                if not target or target in (".", ""):
                    continue
                if scope == "body":
                    body_in[target].add(rel)
                    edges.append((rel, target, href))
                    if target not in pages and target not in redirects:
                        broken.append((rel, href, target))
    # 리다이렉트를 최종 목적지로 접는다
    def final(target: str) -> str:
        seen: set[str] = set()
        while target in redirects and target not in seen:
            seen.add(target)
            nxt = redirects[target]
            if not nxt:
                break
            target = os.path.normpath(
                os.path.join(os.path.dirname(target), nxt.split("#")[0])
            ).replace("\\", "/")
        return target

    folded = defaultdict(set)
    for target, srcs in body_in.items():
        folded[final(target)] |= srcs
    return folded, edges, external, broken


def place_refs():
    """daily-card 의 place_ref 전수. 빌드는 stop.id 만 보고 이 필드를 읽지 않는다."""
    slugs = {p.stem for p in (ROOT / "source/CURRENT/30_Places").glob("*.md")}
    rows = []
    for path in sorted((ROOT / "data/daily-cards").glob("day-*.json")):
        card = json.loads(path.read_text(encoding="utf-8"))
        for stop in card.get("stops", []):
            ref = stop.get("place_ref")
            if not ref:
                continue
            rows.append({
                "day": card["day"],
                "stop_id": stop.get("id", ""),
                "place_ref": ref,
                "stop_name": stop.get("name", ""),
                "ref_exists": ref in slugs,
                "linked_by_build": ref == stop.get("id"),
            })
    return rows


def measure_visibility(site: Path):
    """실제 렌더에서 링크의 밑줄·색을 잰다. 클릭 가능함이 보이는가."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  (playwright 없음 — 가시성 측정을 건너뛴다)", file=sys.stderr)
        return []
    targets = sorted(
        p.relative_to(site).as_posix()
        for pat in ("daily/*.html", "guide/*.html", "places/*.html",
                    "map/*.html", "index.html", "schedule.html",
                    "prepare/*.html", "about/*.html")
        for p in site.glob(pat)
    )
    rows = []
    script = """() => {
      const out = [];
      for (const a of document.querySelectorAll('a')) {
        if (a.closest('nav,footer,header')) continue;
        const r = a.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) continue;
        const cs = getComputedStyle(a);
        const parent = a.parentElement ? getComputedStyle(a.parentElement) : null;
        out.push({
          text: (a.textContent || '').trim().slice(0, 60),
          cls: a.className || '',
          href: a.getAttribute('href') || '',
          decoration: cs.textDecorationLine,
          color: cs.color,
          parent_color: parent ? parent.color : '',
          in_card: !!a.closest('article,.card'),
        });
      }
      return out;
    }"""
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 390, "height": 900})
        for rel in targets:
            page.goto((site / rel).as_uri())
            page.wait_for_timeout(100)
            for item in page.evaluate(script):
                item["page"] = rel
                rows.append(item)
        browser.close()
    return rows


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})
    print(f"  {path.name}  {len(rows)}행")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT))
    args = ap.parse_args()
    site = Path(os.environ.get("SPFR_SITE_DIR") or (ROOT / "site")).resolve()
    if not site.exists():
        print(f"빌드 산출물이 없다: {site}\n먼저 python3 build/site.py 를 돌린다.")
        return 1
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    pages, redirects = load_pages(site)
    inbound, edges, external, broken = build_graph(pages, redirects)
    print(f"실페이지 {len(pages)} · 리다이렉트 {len(redirects)} · 본문 링크 {len(edges)}")

    sys.path.insert(0, str(ROOT / "build"))
    import model  # noqa: E402
    trip = model.load_trip()

    # A. 고아 장소
    place_pages = [p for p in pages if p.startswith("places/")]
    orphans = []
    for rel in sorted(place_pages):
        if inbound.get(rel):
            continue
        slug = rel.split("/")[1][:-5]
        place = trip.places.get(slug)
        orphans.append({
            "page": rel, "slug": slug,
            "region": getattr(place, "region", ""),
            "grade": str(getattr(place, "grade", "")),
            "kind": getattr(place, "kind", ""),
            "linked_days": ";".join(map(str, getattr(place, "days", []) or [])),
            "has_summary": bool(getattr(place, "summary", "")),
        })

    # B. 미실현 place_ref
    refs = place_refs()
    unrealized = [r for r in refs if not r["linked_by_build"]]

    # C. 링크 가시성
    vis = measure_visibility(site)
    invisible = [
        r for r in vis
        if r["decoration"] == "none" and r["color"] == r["parent_color"]
    ]

    # D. 가이드가 상한 때문에 빠뜨린 필수 장소
    dropped = []
    for region in trip.regions:
        essential = [p for p in region.essential_places if p.summary]
        for place in essential[6:]:
            dropped.append({
                "region": region.slug, "slug": place.slug, "name": place.name,
                "grade": str(place.grade),
                "reason": "guide 'Don't Miss' 상한 6개 초과 · grade=essential 이라 '그 밖의 장소'에서도 제외",
            })

    # E. 외부 링크
    ext_rows = []
    for rel, html in pages.items():
        for m in ANCHOR.finditer(body_html(html)):
            attrs = m.group(1) + m.group(3)
            href = m.group(2)
            if not href.startswith(("http://", "https://")):
                continue
            ext_rows.append({
                "page": rel, "url": href,
                "host": re.sub(r"^https?://([^/]+).*", r"\1", href),
                "has_noopener": "noopener" in attrs,
            })

    print("\n산출물:")
    write_csv(out / "LINK_AUDIT_ORPHAN_PLACES.csv",
              ["page", "slug", "region", "grade", "kind", "linked_days", "has_summary"], orphans)
    write_csv(out / "LINK_AUDIT_UNREALIZED_PLACEREF.csv",
              ["day", "stop_id", "place_ref", "stop_name", "ref_exists", "linked_by_build"], unrealized)
    write_csv(out / "LINK_AUDIT_INVISIBLE_LINKS.csv",
              ["page", "text", "cls", "href", "decoration", "color", "parent_color", "in_card"], invisible)
    write_csv(out / "LINK_AUDIT_GUIDE_DROPPED_ESSENTIAL.csv",
              ["region", "slug", "name", "grade", "reason"], dropped)
    write_csv(out / "LINK_AUDIT_EXTERNAL_LINKS.csv",
              ["page", "url", "host", "has_noopener"], ext_rows)
    write_csv(out / "LINK_AUDIT_BROKEN_LINKS.csv",
              ["page", "href", "resolved"],
              [{"page": a, "href": b, "resolved": c} for a, b, c in broken])
    write_csv(out / "LINK_AUDIT_LINK_GRAPH.csv",
              ["source", "target", "href"],
              [{"source": a, "target": b, "href": c} for a, b, c in edges])

    print("\n요약")
    print(f"  A 고아 장소            {len(orphans):4} / 장소 {len(place_pages)}")
    print(f"  B 미실현 place_ref     {len(unrealized):4} / place_ref 총 {len(refs)}")
    print(f"  C 보이지 않는 링크     {len(invisible):4} / 측정 {len(vis)}"
          f" (본문 인라인 {sum(1 for r in invisible if not r['cls'])})")
    print(f"  D 가이드 누락 필수     {len(dropped):4}")
    print(f"  E 끊긴 내부 링크       {len(broken):4} · noopener 누락 "
          f"{sum(1 for r in ext_rows if not r['has_noopener'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
