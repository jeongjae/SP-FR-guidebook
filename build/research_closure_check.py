#!/usr/bin/env python3
"""FCR-03 가드 — 조사 결과가 닫혀 있는가.

    python3 build/research_closure_check.py

세 가지를 본다.

  1 **잘못된 업소 사진**  식당·카페의 사진은 그 업소의 것이라는 근거를
    데이터로 들고 있어야 한다. Google Maps 사진이면 상호·주소·placeKey 를,
    그 밖이면 출처 페이지를 갖는다. 근거 없는 사진은 붙이지 않는다.

  2 **중복 canonical**  같은 실체가 place-facts 에 두 번 있으면 운영시간이
    갈린다. 실제로 `les-halles-d-avignon` ↔ `les-halles` 가 그랬고, 화면은
    그중 하나만 읽었다. 명부에 없는 슬러그는 전부 판정이 있어야 한다.

  3 **미분류 판정**  사진·슬러그·승격 후보 중 상태가 비어 있는 것이 없어야
    한다. '아직 안 봤다' 와 '보고 나서 안 쓰기로 했다' 는 다른 상태다.

`NO_IMAGE` · `KEEP_RESEARCH_ONLY` 는 실패가 아니다. 근거가 적혀 있으면
정상 종료다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import model  # noqa: E402

PHOTO_STATUS = ROOT / "data" / "images" / "food-photo-status.json"
DISPOSITION = ROOT / "data" / "place-facts-disposition.json"

PHOTO_OK = {"VALID_GOOGLE_MAPS", "VALID_EXISTING", "NO_IMAGE"}
PHOTO_BAD = {"WRONG_BUSINESS", "GENERIC_IMAGE", "UNKNOWN_SOURCE"}
SLUG_OK = {"VALID_PLACE_NEEDS_FACTS", "ALIAS_OF_EXISTING_PLACE",
           "ROUTE_OR_UTILITY_NOT_PLACE", "RESTAURANT_OR_CAFE",
           "REGION_OR_NEIGHBORHOOD", "DAY_ONLY_REFERENCE", "OBSOLETE",
           "UNKNOWN_NEEDS_RESEARCH"}


def check(trip) -> tuple[list[str], dict]:
    problems: list[str] = []
    stats = {"food_entities": 0, "photo_with_identity": 0, "photo_no_image": 0,
             "wrong_business": 0, "unclassified_photo": 0,
             "orphan_fact_slugs": 0, "unclassified_slugs": 0,
             "duplicate_canonical": 0}

    known = set(trip.places) | {r.slug for r in trip.regions}
    images = model.load_images(known)["by_place"]
    status = json.loads(PHOTO_STATUS.read_text(encoding="utf-8"))["places"] \
        if PHOTO_STATUS.exists() else {}

    # --- 1) 사진 근거 --------------------------------------------------
    for region in trip.regions:
        for place in region.food_places:
            stats["food_entities"] += 1
            row = status.get(place.slug)
            img = images.get(place.slug)
            if row is None:
                stats["unclassified_photo"] += 1
                problems.append(f"사진 상태가 없다 — {place.slug}")
                continue
            if row["status"] in PHOTO_BAD:
                stats["wrong_business"] += 1
                problems.append(
                    f"쓰면 안 되는 사진이 상태에 남아 있다 — {place.slug} "
                    f"({row['status']})")
            if row["status"] not in PHOTO_OK | PHOTO_BAD:
                stats["unclassified_photo"] += 1
                problems.append(f"모르는 사진 상태 — {place.slug} ({row['status']})")
            if img is None:
                if row["status"] != "NO_IMAGE":
                    problems.append(
                        f"사진이 없는데 상태는 {row['status']} 다 — {place.slug}")
                else:
                    stats["photo_no_image"] += 1
                continue
            # 사진이 있으면 그 업소의 것이라는 근거를 갖고 있어야 한다
            identity = img.get("businessIdentity")
            if img.get("licenseCode") == "google-maps-ugc":
                need = ("name", "address", "mapsUrl")
                if not identity or any(not identity.get(k) for k in need):
                    problems.append(
                        f"Maps 사진인데 업소 신원이 비어 있다 — {place.slug}")
                    continue
            elif not img.get("sourcePage"):
                problems.append(f"사진에 출처 페이지가 없다 — {place.slug}")
                continue
            stats["photo_with_identity"] += 1

    # --- 2·3) 명부에 없는 fact 슬러그의 판정 ------------------------------
    facts = json.loads((ROOT / "data" / "place-facts.json")
                       .read_text(encoding="utf-8"))["places"]
    rules = json.loads(DISPOSITION.read_text(encoding="utf-8"))["slugs"] \
        if DISPOSITION.exists() else {}
    for slug in sorted(facts):
        if slug in trip.places:
            continue
        stats["orphan_fact_slugs"] += 1
        rule = rules.get(slug)
        if rule is None:
            stats["unclassified_slugs"] += 1
            problems.append(
                f"명부에 없는 fact 슬러그인데 판정이 없다 — {slug}. "
                f"data/place-facts-disposition.json 에 적는다")
            continue
        if rule["disposition"] not in SLUG_OK:
            problems.append(f"모르는 판정 — {slug} ({rule['disposition']})")
        if rule["disposition"] == "ALIAS_OF_EXISTING_PLACE":
            stats["duplicate_canonical"] += 1
            problems.append(
                f"별칭인데 아직 병합되지 않았다 — {slug} → {rule.get('canonical')}. "
                f"scripts/merge_fact_aliases.py 를 돌린다")
    return problems, stats


def main() -> int:
    trip = model.load_trip()
    problems, stats = check(trip)
    print("FCR-03 조사 종결 검사")
    for key, label in (
            ("food_entities", "식당·카페 엔티티"),
            ("photo_with_identity", "  업소 신원이 붙은 사진"),
            ("photo_no_image", "  근거를 남기고 비운 것"),
            ("wrong_business", "잘못된 업소 사진 (목표 0)"),
            ("unclassified_photo", "미분류 사진 상태 (목표 0)"),
            ("orphan_fact_slugs", "명부에 없는 fact 슬러그"),
            ("unclassified_slugs", "  판정 없는 것 (목표 0)"),
            ("duplicate_canonical", "  병합 안 된 별칭 (목표 0)")):
        print(f"  {label:32s} {stats[key]}")
    if problems:
        print(f"\n실패 {len(problems)}건:")
        for p in problems[:30]:
            print("  " + p)
        return 1
    print("\n조사 종결 검사 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
