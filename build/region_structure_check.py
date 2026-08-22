#!/usr/bin/env python3
"""FCR-02 가드 — 지역 페이지가 개편된 구조를 지키는가.

    python3 build/region_structure_check.py

**계산된 값을 본다.** 마크업 문자열을 고정하지 않는다 — 디자인을 바꿔도
깨지지 않고, 분류가 틀어졌을 때만 멈춘다.

보는 것:
  1 여섯 섹션이 정해진 순서로 있는가
  2 볼거리에 식당·카페가 있는가 / 식당·카페에 관광지가 있는가  (둘 다 0)
  3 없앤 섹션이 되살아났는가 — 일정 · 한눈에 보기 · 역할/리듬 꼬리말
  4 방문일 배지가 실재하는 Day 를 가리키는가
  5 같은 교통 블록이 두 번 나오는가
  6 지역 페이지의 내부 링크가 실제 파일을 가리키는가
  7 식당·카페 카드가 갖춰야 할 것을 갖췄는가 (없는 것은 리포트에 적는다)

7 번은 빌드를 세우지 않는다. 사진이 없다는 것은 구조가 틀렸다는 뜻이
아니라 아직 못 구했다는 뜻이라, 숨기지 않고 세어서 보여 준다.
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = Path(os.environ.get("SPFR_SITE_DIR") or (ROOT / "site"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import model  # noqa: E402
from model import FOOD_ENTITIES  # noqa: E402

SECTION_ORDER = ["overview", "attractions", "food", "stay", "life", "transport"]

# 없앤 섹션. 섹션 제목(sec-head)으로 되살아나면 안 된다. 접이식 요약
# (<summary>)으로 개요 안에 접혀 있는 것은 콘텐츠 보존이라 통과다.
RETIRED_SECTION_TITLES = ["이 지역의 날들", "한눈에 보기", "여행 전체에서의 역할",
                          "추천 체류 리듬"]

SEC_HEAD = re.compile(
    r'<div class="sec-head(?:-rule)?">(?:<span class="label">(.*?)</span>)?'
    r'(?:<h2>(.*?)</h2>)?', re.S)
HREF = re.compile(r'href="([^"#?]+)')
ANCHOR_ID = re.compile(r'id="([a-z]+)"')


def section_slices(page: str) -> dict[str, str]:
    """id="..." 로 잘라낸 여섯 덩어리."""
    marks = [(m.group(1), m.start()) for m in ANCHOR_ID.finditer(page)
             if m.group(1) in SECTION_ORDER]
    out = {}
    for i, (key, pos) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(page)
        out[key] = page[pos:end]
    return out


CARD = re.compile(r'<article class="card[^"]*">.*?</article>', re.S)
CARD_LINK = re.compile(r'<a class="card-link" href="\.\./places/([^"]+)\.html"')


def card_places(chunk: str) -> list[str]:
    """섹션 안의 **카드**가 가리키는 장소.

    본문 목록('이 지역에서 먹는 것')이 문장 안에서 장소를 링크하는 것은
    분류가 아니다 — 'Les Halles 주변 점심' 은 그 시장을 가리키는 문장이지
    식당 카드가 아니다. 카드만 센다.
    """
    return [m.group(1) for card in CARD.findall(chunk)
            for m in CARD_LINK.finditer(card)]


def day_links(chunk: str) -> list[int]:
    return [int(m.group(1))
            for m in re.finditer(r'href="\.\./daily/day-(\d+)\.html"', chunk)]


def check(trip, verbose: bool = True) -> tuple[list[str], dict]:
    problems: list[str] = []
    stats = {"regions": 0, "attraction_cards": 0, "food_cards": 0,
             "food_in_attractions": 0, "attraction_in_food": 0,
             "retired_sections": 0, "bad_day_refs": 0,
             "duplicate_transport_blocks": 0, "broken_internal_links": 0}

    entity = {slug: p.entity_type for slug, p in trip.places.items()}
    day_numbers = {d.n for d in trip.days}

    for r in trip.regions:
        page_path = SITE / "guide" / f"{r.slug}.html"
        if not page_path.exists():
            problems.append(f"{r.slug}: 지역 페이지가 없다")
            continue
        page = page_path.read_text(encoding="utf-8")
        stats["regions"] += 1

        # --- 1) 섹션 여섯 개와 순서 -------------------------------------
        found = [m.group(1) for m in ANCHOR_ID.finditer(page)
                 if m.group(1) in SECTION_ORDER]
        seen, ordered = set(), []
        for key in found:
            if key not in seen:
                seen.add(key)
                ordered.append(key)
        if ordered != SECTION_ORDER:
            problems.append(f"{r.slug}: 섹션 구성·순서가 다르다 — {ordered}")

        chunks = section_slices(page)

        # --- 2) 분류 ----------------------------------------------------
        for slug in card_places(chunks.get("attractions", "")):
            stats["attraction_cards"] += 1
            if entity.get(slug) in FOOD_ENTITIES:
                stats["food_in_attractions"] += 1
                problems.append(
                    f"{r.slug}: 볼거리 섹션에 식당·카페가 있다 — {slug} "
                    f"({entity.get(slug)})")
        for slug in card_places(chunks.get("food", "")):
            stats["food_cards"] += 1
            if entity.get(slug) not in FOOD_ENTITIES:
                stats["attraction_in_food"] += 1
                problems.append(
                    f"{r.slug}: 식당·카페 섹션에 관광지가 있다 — {slug} "
                    f"({entity.get(slug)})")

        # --- 3) 없앤 섹션이 되살아났는가 ---------------------------------
        for m in SEC_HEAD.finditer(page):
            title = html.unescape((m.group(2) or m.group(1) or "").strip())
            for retired in RETIRED_SECTION_TITLES:
                if title.startswith(retired):
                    stats["retired_sections"] += 1
                    problems.append(f"{r.slug}: 없앤 섹션이 다시 있다 — {title}")

        # --- 4) 방문일 배지 ---------------------------------------------
        for n in day_links(page):
            if n not in day_numbers:
                stats["bad_day_refs"] += 1
                problems.append(f"{r.slug}: 없는 Day 를 가리킨다 — Day {n}")
        # 지역 페이지가 가리키는 Day 는 그 지역의 날이거나, 그 지역 장소를
        # 실제로 들르는 날이어야 한다.
        region_days = {d.n for d in r.days}
        place_days = {n for p in r.places for n in p.days}
        for n in set(day_links(page)) - region_days - place_days:
            stats["bad_day_refs"] += 1
            problems.append(f"{r.slug}: 이 지역과 무관한 Day 링크 — Day {n}")

        # --- 5) 교통 블록 중복 ------------------------------------------
        transport = chunks.get("transport", "")
        for label in ("도착과 출발", "도시 교통", "공식 자료와 재확인"):
            n = transport.count(f"<h2>{label}</h2>")
            if n > 1:
                stats["duplicate_transport_blocks"] += n - 1
                problems.append(f"{r.slug}: 교통 블록이 {n}번 나온다 — {label}")

        # --- 6) 내부 링크 ------------------------------------------------
        for href in HREF.findall(page):
            if href.startswith(("http", "mailto:", "tel:", "data:")):
                continue
            target = (page_path.parent / href).resolve()
            if not target.exists():
                stats["broken_internal_links"] += 1
                problems.append(f"{r.slug}: 끊어진 내부 링크 — {href}")

    return problems, stats


def food_report(trip) -> list[dict]:
    """식당·카페 완결성. 없는 것을 숨기지 않는다."""
    images = model.load_images()
    images.pop("__heroes__", None)
    rows = []
    for r in trip.regions:
        for p in r.food_places:
            price = p.fact("price_range") or p.fact("price_adult")
            menus = sorted({s.menu for d in trip.days for s in d.stops
                            if s.place is p and s.menu})
            rows.append({
                "region": r.slug, "slug": p.slug, "name": p.name,
                "entity_type": p.entity_type,
                "photo": bool(images.get(p.slug)),
                "description": bool(p.summary),
                "website": bool(p.fact("booking") or p.practical_md),
                "map": bool(p.map_query or (p.lat and p.lng)),
                "menu": bool(menus),
                "price": bool(price and price.value),
                "price_verified_at": price.verified_at if price else None,
                "visit_day": bool(p.days),
            })
    return rows


def main() -> int:
    trip = model.load_trip()
    problems, stats = check(trip)
    rows = food_report(trip)

    print("FCR-02 지역 구조 검사")
    for key, label in (
            ("regions", "지역"), ("attraction_cards", "볼거리 카드"),
            ("food_cards", "식당·카페 카드"),
            ("food_in_attractions", "볼거리 안의 식당 (목표 0)"),
            ("attraction_in_food", "식당 안의 관광지 (목표 0)"),
            ("retired_sections", "되살아난 옛 섹션 (목표 0)"),
            ("bad_day_refs", "잘못된 Day 참조 (목표 0)"),
            ("duplicate_transport_blocks", "중복 교통 블록 (목표 0)"),
            ("broken_internal_links", "끊어진 내부 링크 (목표 0)")):
        print(f"  {label:32s} {stats[key]}")

    missing = {k: sum(1 for x in rows if not x[k])
               for k in ("photo", "description", "website", "map", "menu",
                         "price", "visit_day")}
    print(f"\n식당·카페 {len(rows)}곳 — 빠진 항목")
    for k, v in missing.items():
        print(f"  {k:16s} {v}")

    out = ROOT / "FCR02_FOOD_COMPLETENESS.json"
    out.write_text(json.dumps({"summary": stats, "missing": missing,
                               "places": rows}, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    print(f"\n리포트 → {out.name}")

    if problems:
        print(f"\n실패 {len(problems)}건:")
        for p in problems[:40]:
            print("  " + p)
        return 1
    print("\n구조 검사 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
