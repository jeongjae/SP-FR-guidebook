#!/usr/bin/env python3
"""FCR-02 Phase A — 지역 가이드 콘텐츠 인벤토리와 재분류 맵.

**개편 전 렌더 규칙**으로 지역 페이지에 나오던 것을 하나씩 세고, 각각이
어느 섹션으로 가야 하는지 판정한다. 이 파일은 이관의 기준선이라 개편 뒤에
다시 돌려도 같은 값을 낸다 — 옛 규칙을 코드로 들고 있기 때문이다.
개편 뒤의 상태를 보는 것은 `build/region_structure_check.py` 다. 판정 기준은 **제목이 아니라 엔티티**다 —
'…점심' 이라는 제목만 보고 식당으로 분류하지 않는다. 30_Places 정본의
`food_kind`·`meal_role` 이 있어야 식당·카페·시장이다.

    python3 build/region_audit.py

산출물 (저장소 루트):
    REGION_CONTENT_AUDIT.json
    REGION_CONTENT_AUDIT.md
    REGION_RECLASSIFICATION_MAP.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import model  # noqa: E402
from model import Place, Region, Trip  # noqa: E402

# 지금 렌더러가 '먹거리' 목록에서 걸러내는 실행 메모. 이 목록은
# render.build_region 의 것과 같아야 한다 — 감사에서 세는 것과 화면에
# 나오는 것이 달라지면 감사가 거짓말을 한다.
GENERIC_FOOD_NOTES = [
    "기내", "편의점", "물만", "이동용 물", "출발 시각", "숙소 간단식", "숙소 저녁",
    "숙소식", "숙소 점심", "숙소권 간단", "숙소권 저녁 또는 숙소식", "숙소식 또는 동네",
    "이동 중 간단식", "숙소 주변 가벼운 저녁", "가벼운 저녁", "가벼운 점심",
    "이른 저녁", "저녁 무예약", "동네 저녁 (무예약)", "가까운 저녁",
    "첫 장보기", "필수품만", "점심·휴식", "브런치·숙소", "숙소권 가벼운 점심",
]

FOOD_KIND_ENTITY = {
    "RESTAURANT": "restaurant",
    "CAFE": "cafe",
    "BAKERY": "bakery",
    "MARKET": "market",
    "FOOD_HALL": "food-hall",
    "WINE_BAR": "wine-bar",
}

# 목적지 섹션 (개편 후 6개 상위 섹션의 하위 키)
S_ATTR_MUST = "attractions.mustVisit"
S_ATTR_REC = "attractions.recommended"
S_FOOD = "restaurantsCafes"
S_FOOD_DISH = "restaurantsCafes.regionalDishes"
S_STAY = "accommodation"
S_LIFE = "localLife"
S_TR_ARR = "transport.arrival"
S_TR_DEP = "transport.departure"
S_TR_PUB = "transport.publicTransport"
S_TR_REF = "transport.references"
S_OVERVIEW = "overview"
S_DAY = "(day page — 지역 페이지에 두지 않는다)"
S_NONE = "(렌더하지 않는다)"

LAYER_TITLE = {
    "verdict": "이 지역에 시간을 쓸 가치와 한계",
    "scenes": "꼭 경험할 세 장면",
    "skip": "생략해도 되는 것",
    "overview": "한눈에 보기",
    "role": "여행 전체에서의 역할",
    "rhythm": "추천 체류 리듬",
}


def entity_type(p: Place) -> str:
    """장소 하나의 엔티티 종류. 정본 필드만 읽는다."""
    if p.kind == "node":
        return "transport-node"
    if p.food_kind:
        return FOOD_KIND_ENTITY.get(str(p.food_kind).upper(), "restaurant")
    if p.meal_role in ("PRIMARY", "BACKUP"):
        return "restaurant"
    if p.meal_role == "MARKET":
        return "market"
    if p.meal_role == "SELF_CATERING":
        return "market"
    if p.kind == "walk":
        return "walk"
    return "attraction"


def is_food_entity(kind: str) -> bool:
    return kind in ("restaurant", "cafe", "bakery", "market", "food-hall", "wine-bar")


def current_places_sections(r: Region) -> dict[str, str]:
    """지금 렌더러가 장소를 어느 블록에 넣는가. build_region 과 같은 규칙."""
    out: dict[str, str] = {}
    essential = [p for p in r.essential_places if p.summary]
    must, rest_essential = essential[:6], essential[6:]
    for p in must:
        out[p.slug] = "장소 — 놓치지 말 것"
    seen = {p.slug for p in must}
    others = list(rest_essential) + [
        p for p in r.places
        if p.grade != "essential" and p.summary and p.kind == "spot"]
    for p in others:
        if p.slug in seen:
            continue
        seen.add(p.slug)
        out[p.slug] = "장소 — 그 밖의 장소"
    return out


def current_food_stops(r: Region) -> list:
    """지금 '먹거리' 섹션이 카드로 만드는 stop (앞의 8개만 화면에 나온다)."""
    spots = []
    for d in r.days:
        for s in d.stops:
            if s.category == "food" and s.name not in [x.name for x in spots]:
                spots.append(s)
    return spots


def current_dishes(r: Region) -> list[str]:
    dishes = []
    for d in r.days:
        for item in d.food:
            item = item.strip()
            if any(g in item for g in GENERIC_FOOD_NOTES):
                continue
            if item not in dishes:
                dishes.append(item)
    return dishes


def audit_region(r: Region, trip: Trip) -> list[dict]:
    rows: list[dict] = []
    cur = current_places_sections(r)

    # --- 1) 장소 명부의 모든 장소 --------------------------------------
    for p in sorted(r.places, key=lambda x: x.slug):
        kind = entity_type(p)
        cur_sec = cur.get(p.slug, S_NONE)
        if kind == "transport-node":
            target, action = S_NONE, "KEEP"
            note = "이동 기준점 — 장소 페이지도 카드도 만들지 않는다"
        elif is_food_entity(kind):
            target = S_FOOD
            action = "MOVE" if cur_sec.startswith("장소") else "KEEP"
            note = "정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다"
        else:
            target = S_ATTR_MUST if p.grade == "essential" else S_ATTR_REC
            action = "KEEP"
            note = ""
            if cur_sec == S_NONE and p.summary:
                action, note = "MOVE", "요약이 있는데 어느 블록에도 안 나온다"
            elif cur_sec == S_NONE:
                action, note = "KEEP", "요약이 없어 카드를 만들지 않는다"
        rows.append({
            "region": r.slug,
            "item_id": p.slug,
            "title": p.name,
            "current_section": cur_sec,
            "entity_type": kind,
            "target_section": target,
            "duplicate": False,
            "day_refs": sorted(p.days),
            "source": f"source/CURRENT/30_Places/{p.slug}.md"
            if p.has_deep_guide or p.summary else "source/ASSETS/91_Place_Registry_v1.0.md",
            "action": action,
            "note": note,
        })

    # --- 2) '먹거리' 카드이 실제로 무엇을 가리키는가 ---------------------
    for s in current_food_stops(r):
        p = s.place
        if p is None:
            kind, target, action = "meal-slot", S_DAY, "DELETE"
            note = "상호·메뉴가 있는 실제 업소가 아니다 — 하루의 식사 슬롯이다"
            item_id = f"stop:{s.id}"
        else:
            kind = entity_type(p)
            item_id = p.slug
            if is_food_entity(kind):
                target = S_FOOD
                action = "MERGE"
                note = "장소 카드와 같은 대상 — 식당 카드 하나로 합친다"
            else:
                target = S_DAY
                action = "DELETE"
                note = (f"'{p.name}' 은 관광지다. 이 카드는 그 장소에서 먹는다는 "
                        f"하루의 식사 슬롯이지 식당이 아니다")
        rows.append({
            "region": r.slug,
            "item_id": item_id,
            "title": s.name,
            "current_section": "먹거리 — 카드",
            "entity_type": kind,
            "target_section": target,
            "duplicate": p is not None and p.region != r.slug,
            "day_refs": sorted({d.n for d in r.days for x in d.stops if x.id == s.id}),
            "source": "data/daily-cards/day-*.json (stops[])",
            "action": action,
            "note": note,
        })

    # --- 3) 지역 음식 목록 (문자열) --------------------------------------
    for item in current_dishes(r):
        rows.append({
            "region": r.slug, "item_id": f"dish:{item[:40]}", "title": item,
            "current_section": "먹거리 — 목록",
            "entity_type": "regional-dish",
            "target_section": S_FOOD_DISH,
            "duplicate": False, "day_refs": [],
            "source": "data/daily-cards/day-*.json (food[])",
            "action": "KEEP",
            "note": "업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다",
        })

    # --- 4) 편집 층 -------------------------------------------------------
    ed_target = {
        "verdict": (S_OVERVIEW, "KEEP", "Overview 의 첫 블록"),
        "scenes": (S_OVERVIEW, "KEEP", "Overview 안"),
        "skip": (S_OVERVIEW, "KEEP", "Overview 안 접이식"),
        "overview": (S_OVERVIEW, "MOVE",
                     "'한눈에 보기' 섹션을 없애고 Overview 안 접이식으로 흡수한다 — "
                     "예상 체류·확정 일정·추천 이유는 다른 곳에 없다"),
        "role": (S_OVERVIEW, "MOVE", "페이지 하단 꼬리말에서 Overview 로 올린다"),
        "rhythm": (S_OVERVIEW, "MOVE", "페이지 하단 꼬리말에서 Overview 로 올린다"),
    }
    for key, (target, action, note) in ed_target.items():
        if not r.editorial.get(key):
            continue
        rows.append({
            "region": r.slug, "item_id": f"editorial:{key}",
            "title": LAYER_TITLE[key],
            "current_section": {
                "verdict": "개요", "scenes": "개요", "skip": "개요",
                "overview": "한눈에 보기", "role": "꼬리말", "rhythm": "꼬리말",
            }[key],
            "entity_type": "editorial",
            "target_section": target, "duplicate": False, "day_refs": [],
            "source": f"source/CURRENT/20_Regions/{r.slug}.md",
            "action": action, "note": note,
        })

    # --- 5) 일정 섹션 -----------------------------------------------------
    rows.append({
        "region": r.slug, "item_id": "section:days",
        "title": f"이 지역의 날들 — Day 카드 {len(r.days)}장",
        "current_section": "일정",
        "entity_type": "schedule-index",
        "target_section": S_OVERVIEW,
        "duplicate": True,
        "day_refs": [d.n for d in r.days],
        "source": "data/daily-cards/day-*.json",
        "action": "MOVE",
        "note": ("일정 섹션을 없앤다. Day 로 가는 길은 끊지 않는다 — Overview 의 "
                 "날짜 칩과 카드의 방문일 배지가 같은 Day 를 가리킨다"),
    })

    # --- 6) 숙박 ----------------------------------------------------------
    hotels = {d.hotel.get("name"): d.hotel for d in r.days
              if d.region == r.slug and d.hotel.get("name")}
    for name, h in hotels.items():
        confirmed = h.get("status") == "confirmed"
        rows.append({
            "region": r.slug, "item_id": f"hotel:{name}", "title": name,
            "current_section": "숙박·생활",
            "entity_type": "stay",
            "target_section": S_STAY, "duplicate": False,
            "day_refs": [d.n for d in r.days if d.hotel.get("name") == name],
            "source": "data/daily-cards/day-*.json (hotel)",
            "action": "KEEP",
            "note": "확정" if confirmed else "미확정 — 확정처럼 보이면 안 된다",
        })
    if r.essentials:
        rows.append({
            "region": r.slug, "item_id": "essentials:staySummary",
            "title": r.essentials["staySummary"][:60],
            "current_section": "숙박·생활", "entity_type": "stay-note",
            "target_section": S_STAY, "duplicate": False, "day_refs": [],
            "source": "data/region-essentials.json", "action": "KEEP", "note": "",
        })
        for i, item in enumerate(r.essentials.get("lifeEssentials") or []):
            rows.append({
                "region": r.slug, "item_id": f"essentials:life[{i}]",
                "title": item[:60],
                "current_section": "숙박·생활", "entity_type": "local-life",
                "target_section": S_LIFE, "duplicate": False, "day_refs": [],
                "source": "data/region-essentials.json", "action": "MOVE",
                "note": "숙박과 생활을 두 섹션으로 가른다",
            })
        if r.essentials.get("lateReturnRule"):
            rows.append({
                "region": r.slug, "item_id": "essentials:lateReturnRule",
                "title": r.essentials["lateReturnRule"][:60],
                "current_section": "숙박·생활", "entity_type": "local-life",
                "target_section": S_LIFE, "duplicate": False, "day_refs": [],
                "source": "data/region-essentials.json", "action": "MOVE", "note": "",
            })
        for key, target in (("arrivalStrategy", S_TR_ARR),
                            ("departureStrategy", S_TR_DEP)):
            rows.append({
                "region": r.slug, "item_id": f"essentials:{key}",
                "title": r.essentials[key][:60],
                "current_section": "교통", "entity_type": "transport",
                "target_section": target, "duplicate": False, "day_refs": [],
                "source": "data/region-essentials.json", "action": "KEEP", "note": "",
            })

    # --- 7) 교통 ----------------------------------------------------------
    modes = []
    for d in r.days:
        if d.region != r.slug:
            continue
        for t in d.transport:
            if t not in modes:
                modes.append(t)
    for m in modes:
        rows.append({
            "region": r.slug, "item_id": f"mode:{m[:40]}", "title": m,
            "current_section": "교통 — 자유문자열 목록",
            "entity_type": "transport",
            "target_section": S_TR_PUB, "duplicate": True,
            "day_refs": [d.n for d in r.days
                         if d.region == r.slug and m in d.transport],
            "source": "data/daily-cards/day-*.json (transport[])",
            "action": "DELETE",
            "note": ("Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 "
                     "이미 있고 지역 페이지가 그것을 복사해 왔다"),
        })
    if r.transit:
        rows.append({
            "region": r.slug, "item_id": "transit:recommendation",
            "title": r.transit["recommendation"]["title"],
            "current_section": "교통 — 도시 공공교통",
            "entity_type": "transport",
            "target_section": S_TR_PUB, "duplicate": False, "day_refs": [],
            "source": "data/transit-facts.json", "action": "KEEP", "note": "",
        })
        for src in r.transit.get("sources") or []:
            rows.append({
                "region": r.slug, "item_id": f"transit-source:{src['label'][:36]}",
                "title": src["label"],
                "current_section": "교통 — 공식 출처 접이식",
                "entity_type": "transport-reference",
                "target_section": S_TR_REF, "duplicate": False, "day_refs": [],
                "source": "data/transit-facts.json", "action": "MOVE",
                "note": "참고 링크는 Transport 맨 아래 References 로 모은다",
            })
    for res in r.transport_resources:
        rows.append({
            "region": r.slug, "item_id": f"transport-resource:{res['title'][:36]}",
            "title": res["title"],
            "current_section": "교통 — 교통 지도·공식 자료",
            "entity_type": "transport-reference",
            "target_section": S_TR_REF, "duplicate": False, "day_refs": [],
            "source": "data/transit-resources.json", "action": "MOVE", "note": "",
        })
    return rows


def food_completeness(trip: Trip) -> list[dict]:
    """식당·카페 카드가 갖춰야 할 것이 실제로 있는가. 없는 것은 숨기지 않는다."""
    import re
    out = []
    images = model.load_images()
    images.pop("__heroes__", None)
    for p in trip.places.values():
        if not is_food_entity(entity_type(p)):
            continue
        body = p.body_md + "\n" + p.practical_md
        website = bool(re.search(r"https?://", p.practical_md)) or bool(
            p.facts.get("booking") and "http" in (p.facts["booking"].source or ""))
        menu = bool(re.search(r"대표 메뉴|추천 메뉴|메뉴", body)) or bool(p.dont_miss)
        price = bool(re.search(r"€\s?\d|가격대", body)) or bool(
            p.facts.get("price_range") or p.facts.get("price_adult"))
        price_fact = p.facts.get("price_range") or p.facts.get("price_adult")
        out.append({
            "slug": p.slug, "name": p.name, "region": p.region,
            "entity_type": entity_type(p),
            "photo": bool(images.get(p.slug)),
            "description": bool(p.summary),
            "deep_guide": p.has_deep_guide,
            "website": website,
            "map": bool(p.map_query or (p.lat and p.lng)),
            "menu": menu,
            "price": price,
            "price_verified_at": (price_fact.verified_at if price_fact else None),
            "hours": bool(p.facts.get("hours")),
            "booking": bool(p.facts.get("booking")),
            "visit_days": sorted(p.days),
        })
    return sorted(out, key=lambda x: (x["region"], x["slug"]))


def main() -> int:
    trip = model.load_trip()
    rows: list[dict] = []
    for r in trip.regions:
        rows += audit_region(r, trip)

    completeness = food_completeness(trip)

    # 카탈로그에는 있는데 어느 장소도 가리키지 않는 사진. 슬러그가 어긋나면
    # 사진이 저장소에 있으면서 화면에는 영영 안 나온다 — 실제로
    # mercat-de-la-concepcio 가 그랬다.
    images = model.load_images()
    images.pop("__heroes__", None)
    known = set(trip.places) | {r.slug for r in trip.regions}
    photo_orphans = sorted(
        ({"placeId": pid, "imageId": img.get("imageId")}
         for pid, img in images.items() if pid not in known),
        key=lambda x: x["placeId"])

    # --- 요약 ------------------------------------------------------------
    def n(pred):
        return sum(1 for x in rows if pred(x))

    summary = {
        "regions": len(trip.regions),
        "inventory_rows": len(rows),
        "food_in_attractions": n(lambda x: x["current_section"].startswith("장소")
                                 and is_food_entity(x["entity_type"])),
        "attraction_in_food": n(lambda x: x["current_section"] == "먹거리 — 카드"
                                and x["entity_type"] == "attraction"),
        "mealslot_in_food": n(lambda x: x["current_section"] == "먹거리 — 카드"
                              and x["entity_type"] == "meal-slot"),
        "schedule_sections": n(lambda x: x["entity_type"] == "schedule-index"),
        "at_a_glance_sections": n(lambda x: x["item_id"] == "editorial:overview"),
        "footer_role_rhythm": n(lambda x: x["item_id"] in
                                ("editorial:role", "editorial:rhythm")),
        "transport_strings_copied_from_days": n(
            lambda x: x["current_section"] == "교통 — 자유문자열 목록"),
        "transport_blocks_after_merge": n(
            lambda x: x["entity_type"] in ("transport", "transport-reference")
            and x["action"] != "DELETE"),
        "cross_region_food_duplicates": n(lambda x: x["duplicate"]
                                          and x["current_section"] == "먹거리 — 카드"),
        "food_places": len(completeness),
        "food_places_without_photo": sum(1 for x in completeness if not x["photo"]),
        "food_places_without_price": sum(1 for x in completeness if not x["price"]),
        "photo_orphans": len(photo_orphans),
    }

    (ROOT / "REGION_CONTENT_AUDIT.json").write_text(json.dumps(
        {"summary": summary, "inventory": rows,
         "foodCompleteness": completeness, "photoOrphans": photo_orphans},
        ensure_ascii=False, indent=1),
        encoding="utf-8")

    # --- 재분류 맵 --------------------------------------------------------
    moves = {}
    for r in trip.regions:
        rr = [x for x in rows if x["region"] == r.slug]
        moves[r.slug] = {
            "targetStructure": [
                "overview", "attractions.mustVisit", "attractions.recommended",
                "restaurantsCafes", "accommodation", "localLife",
                "transport.arrival", "transport.departure",
                "transport.publicTransport", "transport.references"],
            "attractionToFood": [
                {"id": x["item_id"], "title": x["title"],
                 "from": x["current_section"], "to": x["target_section"],
                 "entity_type": x["entity_type"]}
                for x in rr if x["action"] == "MOVE"
                and is_food_entity(x["entity_type"])
                and x["current_section"].startswith("장소")],
            "foodToDayOrAttraction": [
                {"id": x["item_id"], "title": x["title"],
                 "from": x["current_section"], "to": x["target_section"],
                 "entity_type": x["entity_type"], "reason": x["note"]}
                for x in rr if x["current_section"] == "먹거리 — 카드"
                and x["action"] == "DELETE"],
            "mergedIntoPlaceCard": [
                {"id": x["item_id"], "title": x["title"]}
                for x in rr if x["action"] == "MERGE"
                and x["current_section"] == "먹거리 — 카드"],
            "removedSections": [
                {"id": x["item_id"], "title": x["title"],
                 "to": x["target_section"], "reason": x["note"]}
                for x in rr if x["item_id"] in
                ("section:days", "editorial:overview", "editorial:role",
                 "editorial:rhythm")],
            "transportMerges": [
                {"id": x["item_id"], "title": x["title"], "to": x["target_section"]}
                for x in rr if x["entity_type"] in
                ("transport", "transport-reference")
                and x["action"] in ("MERGE", "MOVE")],
        }
    (ROOT / "REGION_RECLASSIFICATION_MAP.json").write_text(
        json.dumps({"generatedBy": "build/region_audit.py", "regions": moves},
                   ensure_ascii=False, indent=1), encoding="utf-8")

    # --- 사람이 읽는 표 ---------------------------------------------------
    md = ["# REGION_CONTENT_AUDIT — 지역 가이드 콘텐츠 인벤토리",
          "",
          "`python3 build/region_audit.py` 가 만든다. 손으로 고치지 않는다.",
          "",
          "판정은 제목이 아니라 엔티티로 한다. `점심`·`저녁`·`Lunch`·`Dinner` 가",
          "제목에 있다는 이유로 식당으로 분류하지 않는다 — 30_Places 정본에",
          "`food_kind`·`meal_role` 이 있어야 식당·카페·시장이다.",
          "", "## 요약", "", "| 항목 | 값 |", "|---|---:|"]
    label = {
        "regions": "지역 수", "inventory_rows": "인벤토리 항목",
        "food_in_attractions": "**장소 섹션에 있던 식당·카페·시장**",
        "attraction_in_food": "**먹거리 섹션에 있던 관광지**",
        "mealslot_in_food": "먹거리 섹션의 업소 아닌 식사 슬롯",
        "schedule_sections": "제거 대상 일정 섹션",
        "at_a_glance_sections": "제거 대상 한눈에 보기 섹션",
        "footer_role_rhythm": "제거 대상 꼬리말 블록",
        "transport_strings_copied_from_days": "Day 에서 복사해 오던 교통 문자열",
        "transport_blocks_after_merge": "통합 후 남는 교통 블록",
        "cross_region_food_duplicates": "지역을 넘나든 식당 카드",
        "food_places": "식당·카페·시장 장소",
        "food_places_without_photo": "사진 없는 식당·카페",
        "food_places_without_price": "가격 근거 없는 식당·카페",
        "photo_orphans": "어느 장소도 가리키지 않는 사진",
    }
    for k, v in summary.items():
        md.append(f"| {label.get(k, k)} | {v} |")

    for r in trip.regions:
        rr = [x for x in rows if x["region"] == r.slug]
        md += ["", f"## {r.name} (`{r.slug}`)", "",
               "| 항목 | 현재 위치 | 엔티티 | 이동할 위치 | 방문일 | 조치 | 메모 |",
               "|---|---|---|---|---|---|---|"]
        for x in rr:
            days = ",".join(f"D{d}" for d in x["day_refs"][:6]) or "—"
            md.append(f"| {x['title']} | {x['current_section']} | {x['entity_type']} "
                      f"| {x['target_section']} | {days} | **{x['action']}** "
                      f"| {x['note']} |")

    md += ["", "## 식당·카페 카드 완결성", "",
           "| 지역 | 장소 | 종류 | 사진 | 소개 | 장문 | 공홈 | 지도 | 메뉴 | 가격 | 가격확인일 | 운영시간 | 예약 | 방문일 |",
           "|---|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|:-:|:-:|---|"]
    for c in completeness:
        def m(b):
            return "O" if b else "**X**"
        md.append(f"| {c['region']} | {c['name']} | {c['entity_type']} | {m(c['photo'])} "
                  f"| {m(c['description'])} | {m(c['deep_guide'])} | {m(c['website'])} "
                  f"| {m(c['map'])} | {m(c['menu'])} | {m(c['price'])} "
                  f"| {c['price_verified_at'] or '—'} | {m(c['hours'])} | {m(c['booking'])} "
                  f"| {','.join('D%d' % d for d in c['visit_days']) or '**없음**'} |")
    md += ["", "## 어느 장소도 가리키지 않는 사진", "",
           "카탈로그에는 있는데 명부의 슬러그와 맞지 않아 화면에 영영 안 나오는",
           "사진이다. 요리 사진(socca·xuixo 등)은 장소가 아니라 정상이고,",
           "나머지는 슬러그 오타이거나 승격되지 않은 장소다.", "",
           "| placeId | imageId |", "|---|---|"]
    for o in photo_orphans:
        md.append(f"| `{o['placeId']}` | {o['imageId']} |")

    (ROOT / "REGION_CONTENT_AUDIT.md").write_text("\n".join(md) + "\n",
                                                  encoding="utf-8")

    for k, v in summary.items():
        print(f"  {label.get(k, k):32s} {v}")
    print("\nREGION_CONTENT_AUDIT.json · .md · REGION_RECLASSIFICATION_MAP.json 갱신")
    return 0


if __name__ == "__main__":
    sys.exit(main())
