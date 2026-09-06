#!/usr/bin/env python3
"""Synchronize the 2026-09-29 / 2026-10-01 Paris day swap.

The script fails closed unless the two source cards still contain the expected
pre-swap stop sets.  It updates the Day source of truth and both map datasets;
the remaining generated indexes are rebuilt by the normal build commands.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "data" / "daily-cards"
MAP_QUERIES = ROOT / "data" / "map-queries.json"
MAP_ASSETS = ROOT / "source" / "ASSETS" / "maps"
VERIFIED_AT = "2026-09-06"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def by_id(day: dict, stop_id: str) -> dict:
    return next(stop for stop in day["stops"] if stop["id"] == stop_id)


def assert_source(day32: dict, day34: dict) -> None:
    if day32.get("date") != "2026-09-29" or day34.get("date") != "2026-10-01":
        raise RuntimeError("Day/date precondition failed")
    ids32 = {stop["id"] for stop in day32["stops"]}
    ids34 = {stop["id"] for stop in day34["stops"]}
    if not {"musee-d-orsay", "musee-rodin", "invalides-exterior"} <= ids32:
        raise RuntimeError("Day 32 is no longer the expected Orsay/Rodin source")
    if not {"versailles-palace", "versailles-gardens", "trianon-hamlet"} <= ids34:
        raise RuntimeError("Day 34 is no longer the expected Versailles source")


def build_day32(source: dict) -> dict:
    day = copy.deepcopy(source)
    day.update({
        "day": 32,
        "date": "2026-09-29",
        "title": "베르사유 궁전 & 대정원 & 트리아농 전일 투어",
        "startTime": "08:30",
        "endTime": "21:30",
        "totalDuration": "13시간",
    })
    palace = by_id(day, "versailles-palace")
    palace["start"], palace["end"] = "09:45", "12:30"
    palace["summary"] = palace["summary"].replace("10:00 시간지정 입장", "10:00 전후 시간지정 입장")
    lunch = by_id(day, "versailles-lunch")
    lunch["start"], lunch["end"] = "12:45", "13:30"
    lunch["summary"] = lunch["summary"].replace("90분 슬롯이지만 실질 착석은 65분", "45분 슬롯이므로")
    for status in lunch.get("executionStatuses", []):
        status["detail"] = status["detail"].replace("12:45~13:00", "12:45")
        status["detail"] = status["detail"].replace("10/1은", "9/29(화)는")
    gardens = by_id(day, "versailles-gardens")
    gardens["start"], gardens["end"] = "13:30", "15:00"
    for status in gardens.get("executionStatuses", []):
        if status["type"] == "check":
            status["detail"] = "9/29(화)는 Jardins Musicaux 운영일. Passport 티켓으로 정원 구역 입장."
    trianon = by_id(day, "trianon-hamlet")
    trianon["start"], trianon["end"] = "15:00", "16:30"
    dinner = by_id(day, "paris-return")
    dinner["start"], dinner["end"] = "20:00", "21:30"
    dinner["summary"] = "17:00 전후 베르사유 출발, RER C로 18:00~18:30 파리 귀환 후 15구 Le Grand Pan 저녁"
    for status in dinner.get("executionStatuses", []):
        status["detail"] = status["detail"].replace("목요일", "화요일")
    day["food"] = ["La Flottille 점심 (12:45)", "Le Grand Pan 저녁 (20:00)"]
    day["highlights"] = [
        "10:00 전후 본관 시간지정 입장",
        "9/29 화요일 Jardins Musicaux",
        "피로 시 트리아농·왕비의 촌락 선택 축소",
    ]
    day["needsReview"] = [
        "베르사유 Passport 티켓 9/29 10:00 전후 궁전 슬롯 예매",
        "9/29 RER C 운행·공사 여부 출발 전 재확인",
    ]
    day["sourceRefs"] = [
        "source/CURRENT/20_Regional_Chapters/11_Paris_Long_Stay_v2.0.md#Day-6-9월29일",
        "source/CURRENT/30_Places/versailles.md",
    ]
    day["map"] = {"zoom": 12, "center": [48.825, 2.205], "routeCache": None}
    return day


def build_day34(source: dict) -> dict:
    day = copy.deepcopy(source)
    day.update({
        "day": 34,
        "date": "2026-10-01",
        "title": "인상주의 & 조각 — 오르세 상설·로댕",
        "startTime": "09:30",
        "endTime": "20:00",
        "totalDuration": "10시간 30분",
        "totalDistance": "메트로 + 파리 좌안 예술도보 약 5.0km",
    })
    morning = by_id(day, "morning-routine")
    morning["start"], morning["end"] = "09:30", "10:15"
    morning["name"] = "Left Bank Art Morning (오르세 출발)"
    morning["summary"] = "09:30 숙소 출발, 10:15 오르세 Entrée 1 - Quai 도착 후 10:30 예약 입장 준비"
    morning["executionStatuses"] = [{
        "type": "check", "label": "ON TIME",
        "detail": "09:30 숙소 출발 ➔ 메트로 8·12호선 ➔ 10:15 Entrée 1 - Quai 도착.",
    }]
    morning["executionNote"] = "예약 시각 15분 전 도착. 10:30 입장권 QR을 오프라인 저장."

    orsay = by_id(day, "musee-d-orsay")
    orsay["start"], orsay["end"] = "10:30", "13:00"
    orsay["name"] = "Musée d'Orsay (상설 컬렉션 중심)"
    orsay["summary"] = "인상주의·후기인상주의 상설 컬렉션 중심: Monet, Renoir, Degas, Cézanne, Van Gogh, Gauguin 주요작을 2시간 30분에 집중 관람"
    orsay["executionStatuses"] = [{
        "type": "confirmed", "label": "BOOKED 10:30",
        "detail": "Musée d'Orsay 10/1(목) 10:30 시간지정 예약 확정 · 10:15까지 Entrée 1 - Quai 도착.",
    }]
    orsay["executionNote"] = "1 Rue de la Légion d'Honneur. Entrée 1 - Quai 이용, 예약 QR 오프라인 저장. 10/6 Mary Cassatt 특별전과 분리된 상설 컬렉션 방문."

    lunch = by_id(day, "rue-du-bac-lunch")
    lunch["start"], lunch["end"] = "13:00", "14:00"
    for status in lunch.get("executionStatuses", []):
        status["detail"] = status["detail"].replace("화요일", "목요일").replace("13:00–14:15", "13:00–14:00")

    rodin = by_id(day, "musee-rodin")
    rodin["start"], rodin["end"] = "14:15", "16:00"
    rodin["summary"] = rodin["summary"].replace("(2시간)", "(1시간 45분)")
    for status in rodin.get("executionStatuses", []):
        status["detail"] = status["detail"].replace("14:30", "14:15").replace("화요일", "목요일")
    rodin["executionNote"] = rodin["executionNote"].replace("화요일", "목요일")

    invalides = by_id(day, "invalides-exterior")
    invalides["start"], invalides["end"] = "16:00", "17:00"
    for status in invalides.get("executionStatuses", []):
        status["detail"] = status["detail"].replace("오르세 3.5시간", "오르세·로댕")

    dinner = by_id(day, "paris-return")
    dinner["start"], dinner["end"] = "18:30", "20:00"
    day["food"] = ["Café Varenne 점심 (13:00)", "Café du Commerce 저녁 (18:30)"]
    day["highlights"] = [
        "10/1 10:30 오르세 예약 확정",
        "상설 컬렉션 중심 2시간 30분",
        "10/6 Mary Cassatt 특별전 재방문과 역할 분리",
    ]
    day["backup"] = day["backup"].replace("오르세 관람 후", "오르세·로댕 관람 중")
    day["needsReview"] = ["Musée Rodin 10/1 14:15 입장권은 예약 권장(미확정)"]
    day["sourceRefs"] = [
        "source/CURRENT/20_Regional_Chapters/11_Paris_Long_Stay_v2.0.md#Day-8-10월1일",
        "사용자 확인: Musée d'Orsay 2026-10-01 10:30 예약 완료",
    ]
    return day


def swap_map_queries() -> None:
    data = load(MAP_QUERIES)
    routes = data["routes"]
    old32 = {key: value for key, value in routes.items() if key.startswith("day-32:")}
    old34 = {key: value for key, value in routes.items() if key.startswith("day-34:")}
    if "day-32:musee-d-orsay" not in old32 or "day-34:versailles-palace" not in old34:
        raise RuntimeError("map-queries swap precondition failed")
    for key in [*old32, *old34]:
        del routes[key]
    routes.update({key.replace("day-32:", "day-34:"): value for key, value in old32.items()})
    routes.update({key.replace("day-34:", "day-32:"): value for key, value in old34.items()})
    for key, value in routes.items():
        if key.startswith(("day-32:", "day-34:")):
            value["verifiedAt"] = VERIFIED_AT
    data["verifiedAt"] = VERIFIED_AT
    save(MAP_QUERIES, data)


def add_map_place(registry: dict, entry: dict) -> None:
    ids = {place["id"] for place in registry["places"]}
    if entry["id"] not in ids:
        registry["places"].append(entry)


def map_place(pid: str, name: str, lat: float, lng: float, query: str, *, optional=False) -> dict:
    return {
        "id": pid, "name": name, "city": "Paris", "type": "attraction",
        "lat": lat, "lng": lng, "googlePlaceId": "",
        "googleMapsUrl": f"https://www.google.com/maps/search/?api=1&query={query}",
        "address": "", "private": False, "approximate": False,
        "optional": optional, "status": "planned", "coordinatesVerified": VERIFIED_AT,
    }


def update_daily_routes() -> None:
    registry_path = MAP_ASSETS / "place-registry.json"
    registry = load(registry_path)
    additions = [
        map_place("versailles-gardens", "Gardens of Versailles", 48.8060, 2.1150, "Gardens+of+Versailles"),
        map_place("grand-trianon", "Grand Trianon", 48.8150, 2.1050, "Grand+Trianon", optional=True),
        map_place("musee-rodin", "Musée Rodin", 48.8553, 2.3158, "Mus%C3%A9e+Rodin+Paris"),
        map_place("hotel-des-invalides", "Hôtel des Invalides", 48.8566, 2.3125, "H%C3%B4tel+des+Invalides", optional=True),
    ]
    for entry in additions:
        add_map_place(registry, entry)
    save(registry_path, registry)

    groups_path = MAP_ASSETS / "region-groups.json"
    groups = load(groups_path)
    paris = next(group for group in groups["regions"] if group["id"] == "paris")
    for entry in additions:
        if entry["id"] not in paris["placeIds"]:
            paris["placeIds"].append(entry["id"])
    save(groups_path, groups)

    routes_path = MAP_ASSETS / "daily-routes.json"
    routes = load(routes_path)
    by_date = {day["date"]: day for day in routes["days"]}
    by_date["2026-09-29"].update({
        "title": "Versailles Palace & Gardens",
        "center": [48.805, 2.115], "zoom": 14, "defaultMode": "transit",
        "stops": [
            {"placeId": "paris-stay-candidate", "order": 0, "plannedTime": "08:30", "note": "Javel역에서 RER C 이용."},
            {"placeId": "versailles", "order": 1, "plannedTime": "10:00–12:30", "note": "Passport 시간지정 본관 입장."},
            {"placeId": "versailles-gardens", "order": 2, "plannedTime": "13:30–15:00", "note": "Jardins Musicaux 운영일."},
            {"placeId": "grand-trianon", "order": 3, "plannedTime": "15:00–16:30", "note": "피로 시 생략 또는 미니트레인."},
        ],
        "segments": [
            {"from": "paris-stay-candidate", "to": "versailles", "mode": "transit"},
            {"from": "versailles", "to": "versailles-gardens", "mode": "walking"},
            {"from": "versailles-gardens", "to": "grand-trianon", "mode": "walking"},
        ],
    })
    by_date["2026-10-01"].update({
        "title": "Musée d'Orsay & Musée Rodin",
        "center": [48.857, 2.320], "zoom": 15, "defaultMode": "transit",
        "stops": [
            {"placeId": "paris-stay-candidate", "order": 0, "plannedTime": "09:30", "note": "10:15 오르세 도착 목표."},
            {"placeId": "musee-d-orsay", "order": 1, "plannedTime": "10:30–13:00", "note": "예약 확정 · 상설 컬렉션 중심."},
            {"placeId": "musee-rodin", "order": 2, "plannedTime": "14:15–16:00", "note": "시간지정 예매 권장."},
            {"placeId": "hotel-des-invalides", "order": 3, "plannedTime": "16:00 이후", "note": "선택 외관 산책."},
        ],
        "segments": [
            {"from": "paris-stay-candidate", "to": "musee-d-orsay", "mode": "transit"},
            {"from": "musee-d-orsay", "to": "musee-rodin", "mode": "walking"},
            {"from": "musee-rodin", "to": "hotel-des-invalides", "mode": "walking"},
        ],
    })
    save(routes_path, routes)


def main() -> None:
    path32 = CARDS / "day-32.json"
    path34 = CARDS / "day-34.json"
    day32, day34 = load(path32), load(path34)
    assert_source(day32, day34)
    save(path32, build_day32(day34))
    save(path34, build_day34(day32))
    swap_map_queries()
    update_daily_routes()
    print("synchronized: 9/29 Versailles · 10/1 Orsay 10:30 + Rodin + Invalides")


if __name__ == "__main__":
    main()
