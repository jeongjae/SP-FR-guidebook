#!/usr/bin/env python3
"""웹앱 데이터 스냅샷 — site/app/data/ 로 정본을 JSON 으로 내보낸다.

앱(site/app/)은 이 스냅샷을 IndexedDB 에 담아 오프라인에서 읽고, 편집은
이벤트 저널로 쌓아 GitHub 로 되보낸다. 여기서 내보내는 형태가 곧
클라이언트·서버(적용 스크립트)가 공유하는 스키마다.

원칙:
  - 일일카드는 원형 그대로 내보낸다 — data/daily-cards/schema.json 하나를
    양쪽이 공유해야 적용 스크립트가 같은 모양을 되쓴다.
  - 장소 장문은 markdown 원문을 유지한다 — HTML 로 바꾸면 되돌릴 수 없다.
  - 결정적 출력이다. 시각·난수를 넣지 않는다 — 내용이 같으면 버전도 같아
    기기가 헛되이 다시 받지 않는다 (write_pwa 와 같은 이유).
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content_model
import model
from render import SITE

ROOT = Path(__file__).resolve().parent.parent
APP_DATA = SITE / "app" / "data"
SCHEMA_VERSION = "1.0"


def _json_default(value):
    # 트래커 xlsx 의 datetime 셀. 날짜만 의미가 있다.
    if hasattr(value, "isoformat"):
        return value.isoformat()
    raise TypeError(f"직렬화 불가: {type(value)!r}")


def _write(rel: str, payload) -> dict:
    path = APP_DATA / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"),
                     default=_json_default) + "\n"
    data = raw.encode("utf-8")
    path.write_bytes(data)
    return {"path": rel, "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def _trip_payload(trip: model.Trip) -> dict:
    itinerary = json.loads(
        (ROOT / "source/CURRENT/10_Core/itinerary.json").read_text(encoding="utf-8"))
    regions_raw = json.loads(
        (ROOT / "source/CURRENT/10_Core/regions.json").read_text(encoding="utf-8"))
    return {
        "schemaVersion": SCHEMA_VERSION,
        "trip": itinerary["trip"],
        "stays": itinerary["stays"],
        "regions": [
            {"slug": r["slug"], "name": r["name"], "nameKo": r.get("nameKo"),
             "country": r.get("country"), "tagline": r.get("tagline")}
            for r in regions_raw["regions"]
        ],
        "days": [
            {"n": d.n, "date": d.date.isoformat(), "dateLabel": d.date_label,
             "city": d.city, "title": d.title, "dayType": d.day_type,
             "fatigue": d.fatigue, "region": d.region,
             "hotel": {"name": d.hotel.get("name"),
                       "status": d.hotel.get("status")}}
            for d in trip.days
        ],
    }


def _places_payloads(trip: model.Trip) -> tuple[dict, dict[str, dict]]:
    bodies = model.load_place_bodies()
    index = {"schemaVersion": SCHEMA_VERSION, "places": []}
    by_region: dict[str, dict] = {}
    for p in sorted(trip.places.values(), key=lambda x: x.slug):
        index["places"].append({
            "slug": p.slug, "name": p.name, "region": p.region,
            "kind": p.kind, "grade": p.grade, "gradeLabel": p.grade_label,
            "foodKind": p.food_kind, "mealRole": p.meal_role,
            "pin": p.pin, "wiki": p.wiki, "mapQuery": p.map_query,
            "summary": p.summary, "days": sorted(p.days),
        })
        body = bodies.get(p.slug)
        if body is None:
            continue
        region_doc = by_region.setdefault(
            p.region, {"schemaVersion": SCHEMA_VERSION, "region": p.region,
                       "places": {}})
        region_doc["places"][p.slug] = {
            "summary": body.get("summary", ""),
            "whyGoMd": body.get("why_go", ""),
            "bodyMd": body.get("body", ""),
            "practicalMd": body.get("practical_md", ""),
            "dontMiss": body.get("dont_miss", []) or [],
            "foodKind": body.get("food_kind"),
            "mealRole": body.get("meal_role"),
        }
    return index, by_region


def _bookings_payload() -> dict:
    tracker = ROOT / "source/OPERATIONS/TP_Europe_Travel_Master_Tracker_v1.2.xlsx"
    accommodations, reservations = [], []
    for row in content_model._rows(tracker, "Accommodation"):
        base = str(row.get("거점") or "")
        private_stay = base.lower() == "bàscara"  # content_model 과 같은 규칙
        accommodations.append({
            "base": base, "checkIn": row.get("체크인"),
            "checkOut": row.get("체크아웃"), "nights": row.get("박수"),
            "status": row.get("상태"), "area": row.get("생활권/후보"),
            "address": None if private_stay else row.get("주소"),
            "checkInOut": row.get("체크인/아웃"),
            "note": None if private_stay else row.get("비고"),
        })
    for row in content_model._rows(tracker, "Reservations"):
        reservations.append({
            "id": str(row.get("ID")), "category": row.get("카테고리"),
            "name": row.get("예약항목"), "date": row.get("날짜"),
            "time": row.get("시간"), "status": row.get("상태"),
            "targetDate": row.get("예약목표일"),
            "address": row.get("주소/역"), "note": row.get("비고"),
        })
    overrides_path = ROOT / "data" / "booking-overrides.json"
    overrides = (json.loads(overrides_path.read_text(encoding="utf-8"))
                 if overrides_path.exists() else {"overrides": {}})
    return {"schemaVersion": SCHEMA_VERSION,
            "accommodations": accommodations,
            "reservations": reservations,
            "overrides": overrides.get("overrides", {})}


def export(trip: model.Trip) -> None:
    APP_DATA.mkdir(parents=True, exist_ok=True)
    files: list[dict] = []

    files.append(_write("trip.json", _trip_payload(trip)))

    for card in sorted((ROOT / "data" / "daily-cards").glob("day-*.json")):
        payload = json.loads(card.read_text(encoding="utf-8"))
        files.append(_write(f"days/{card.name}", payload))

    index, by_region = _places_payloads(trip)
    files.append(_write("places-index.json", index))
    for region, doc in sorted(by_region.items()):
        files.append(_write(f"places/{region}.json", doc))

    files.append(_write("bookings.json", _bookings_payload()))

    version = hashlib.sha256()
    for f in sorted(files, key=lambda x: x["path"]):
        version.update(f["path"].encode("utf-8") + b"\0")
        version.update(f["sha256"].encode("ascii") + b"\n")
    manifest = {
        "schemaVersion": SCHEMA_VERSION,
        "version": version.hexdigest(),
        "baseCommit": os.environ.get("GITHUB_SHA", "local"),
        "files": sorted(files, key=lambda x: x["path"]),
    }
    (APP_DATA / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8")
    total = sum(f["bytes"] for f in files)
    print(f"  앱 스냅샷: {len(files)}개 파일 · {total/1024:.0f} KiB · "
          f"버전 {manifest['version'][:12]}")


if __name__ == "__main__":
    export(model.load_trip())
