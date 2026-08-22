#!/usr/bin/env python3
"""사이트 빌드.

    python3 build/site.py

모델 → 페이지. 이 파일은 순서만 정하고, 내용은 render.py 가, 정본은
model.py 가 맡는다.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_guard
import fact_guard
import model
import promote_places
import promote_regions
import render
from render import SITE


def clean_site() -> None:
    """site/ 를 비운다.

    /mnt/c (WSL 의 Windows 파일시스템) 에서는 방금 지운 디렉터리가 아직
    비어 있지 않다고 보고되는 일이 있다 — 윈도우 쪽 인덱서·바이러스검사가
    핸들을 잠깐 붙잡는다. 몇 번 다시 시도하면 풀린다.
    """
    import time
    for attempt in range(6):
        if not SITE.exists():
            break
        try:
            shutil.rmtree(SITE)
            break
        except OSError as e:
            if attempt == 5:
                raise
            time.sleep(0.4 * (attempt + 1))
    SITE.mkdir(parents=True, exist_ok=True)


def main() -> int:
    # 30_Places/<slug>.md 가 장소 장문의 유일한 정본(Canonical SOT)이다.
    # 매 빌드마다 챕터 원고에서 덮어쓰지 않고 30_Places 를 직접 사용한다.
    place_bodies = model.load_place_bodies()
    promoted = set(place_bodies.keys())
    regions_promoted = promote_regions.regenerate()
    print(f"정본 장소: {len(promoted)}개 · 지역 편집 승격: {len(regions_promoted)}개")

    trip = model.load_trip()
    problems = model.validate(trip)
    if problems:
        print("콘텐츠 모델 검증 실패:")
        for p in problems:
            print("  " + p)
        return 1
    guard = render.check_vocabulary(trip) + render.check_place_prose(trip, promoted)
    if guard:
        print("가드 실패:")
        for g in guard:
            print("  " + g)
        return 1

    print(f"모델: {trip.total_days}일 · 지역 {len(trip.regions)} · "
          f"장소 {len(trip.places)} (장문 "
          f"{sum(1 for p in trip.places.values() if p.has_deep_guide)})")

    clean_site()

    import shell
    metas = []
    if render.MAPS_KEY:
        metas.append(f'<meta name="google-maps-api-key" content="{render.MAPS_KEY}">')
    if render.MAPS_ID:
        metas.append(f'<meta name="google-maps-map-id" content="{render.MAPS_ID}">')
    shell.MAPS_META = ("\n".join(metas) + "\n") if metas else ""
    print(f"지도 키: {'있음' if render.MAPS_KEY else '없음 — 목록으로 연다'}")

    render.IMAGES = render.load_image_index()
    render.FACTS = model.load_facts()
    render.HOTEL_QUERIES = {
        k: v["query"] for k, v in
        json.loads((ROOT / "data" / "map-queries.json").read_text(encoding="utf-8"))
        .get("hotels", {}).items()}
    shell.MASK = render.mask_booking_codes
    res = render.load_reservations()
    print(f"예약: 유효 {res['active']}건 · 미확정 {res['undone']}건")

    def write(path: str, html: str) -> None:
        p = SITE / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(html, encoding="utf-8")

    # 장소가 먼저다 — 검색 색인과 Day↔Place 링크를 채운다
    for p in trip.places.values():
        write(f"places/{p.slug}.html", render.build_place(p, trip))
    print(f"장소 {len(trip.places)}쪽")

    for d in trip.days:
        write(d.url, render.build_day(d, trip))
    print(f"데일리 {len(trip.days)}쪽")

    for r in trip.regions:
        write(f"guide/{r.slug}.html", render.build_region(r, trip))
    write("guide/index.html", render.build_guide_index(trip))
    print(f"지역 {len(trip.regions)}쪽")

    write("schedule.html", render.build_schedule(trip))
    write("index.html", render.build_home(trip, res))

    for name, html in render.build_map_pages(trip).items():
        write(f"map/{name}", html)
    for name, html in render.build_prepare(trip, res).items():
        write(f"prepare/{name}", html)

    write("about/credits.html", render.build_credits(trip))
    write("about/sources.html", render.build_sources(trip))

    # 원고 쪽 가드. 배포 산출물을 보는 것이 있어 페이지를 다 쓴 뒤 돈다.
    fact_guard.check_confirmed_fact_token_guards()
    content_guard.check_phase9_commercial_depth_guards()


    n_red = render.write_redirects(trip)
    print(f"리다이렉트 {n_red}쪽 — 옛 주소를 살려 둔다")

    write("offline.html", render.build_offline_page())
    write("offline-fallback.html", render.build_offline_fallback())
    render.write_assets(trip)
    render.write_pwa()

    # FCR-02 — 지역 페이지의 분류와 구조. 링크까지 보므로 자산을 다 쓴 뒤 돈다.
    import region_structure_check
    structure_problems, _ = region_structure_check.check(trip)
    if structure_problems:
        print("지역 구조 가드 실패:")
        for problem in structure_problems[:20]:
            print("  " + problem)
        return 1
    print("지역 구조 가드: 분류·섹션·방문일·링크 이상 없음")

    total = sum(1 for _ in SITE.rglob("*.html"))
    print(f"\n완료: {SITE} ({total}쪽 · 검색 색인 {len(render.SEARCH_INDEX)}건)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
