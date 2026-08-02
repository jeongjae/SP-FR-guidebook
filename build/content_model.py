"""Normalized content graph for the TP guidebook build.

The legacy sources remain authoritative during the migration, but every consumer
can now address records through stable IDs instead of matching display strings.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
import json
import re
import unicodedata

import openpyxl


SCHEMA_VERSION = "1.0"


def _value(value):
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return value


def _rows(path: Path, sheet: str):
    wb = openpyxl.load_workbook(path, data_only=True, read_only=False)
    ws = wb[sheet]
    values = list(ws.iter_rows(values_only=True))
    header_at = next(i for i, row in enumerate(values) if row and row[0] is not None and i >= 2)
    headers = [str(v).strip() if v is not None else "" for v in values[header_at]]
    result = []
    for row in values[header_at + 1:]:
        if not row or row[0] is None:
            continue
        result.append({headers[i]: _value(v) for i, v in enumerate(row) if i < len(headers) and headers[i]})
    return result


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _name_key(value: str) -> str:
    value = "".join(c for c in unicodedata.normalize("NFKD", value.lower())
                    if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9가-힣]", "", value)


def _day_id(value, trip_start, trip_end):
    if not value:
        return None
    d = date.fromisoformat(value)
    if not trip_start <= d <= trip_end:
        return None
    return f"day:{(d - trip_start).days + 1:03d}"


def build_graph(*, chapters, trip_start, trip_end, places, place_days,
                tracker_path: Path):
    regions = []
    region_by_name = {}
    for c in chapters:
        if c["kind"] != "region":
            continue
        rid = f'region:{c["name"]}'
        record = {
            "id": rid, "slug": c["name"], "name": c["region"],
            "title": c["title"], "start": c["start"].isoformat(),
            "end": c["end"].isoformat(), "nights": c["nights"],
            "chapterId": f'chapter:{c["slug"]}', "mapId": f'map:{c["name"]}',
        }
        regions.append(record)
        region_by_name[c["region"].lower()] = rid
        region_by_name[c["name"].lower()] = rid

    itinerary = _rows(tracker_path, "Master Itinerary")
    itinerary_by_date = {r["날짜"]: r for r in itinerary}
    days = []
    d = trip_start
    while d <= trip_end:
        n = (d - trip_start).days + 1
        row = itinerary_by_date.get(d.isoformat(), {})
        region_id = region_by_name.get(str(row.get("거점", "")).lower())
        if not region_id:
            containing = [r for r in regions if r["start"] <= d.isoformat() < r["end"]]
            region_id = containing[0]["id"] if containing else regions[-1]["id"]
        days.append({
            "id": f"day:{n:03d}", "number": n, "date": d.isoformat(),
            "regionId": region_id, "theme": row.get("테마/핵심일정"),
            "dayType": row.get("일정유형"), "fatigue": row.get("피로도(1~5)"),
            "status": row.get("계획상태"), "url": f"daily/day-{n:02d}.html",
        })
        d += timedelta(days=1)

    place_records = []
    places_by_name = {}
    chapter_region = {c["slug"]: f'region:{c["name"]}' for c in chapters if c["kind"] == "region"}
    for p in places:
        day_nums, evidence = place_days.get(p["slug"], ([], None))
        record = {
            "id": f'place:{p["slug"]}', "slug": p["slug"], "name": p["name"],
            "regionIds": [chapter_region[p["chapter"]]], "type": p["type"],
            "grade": p["grade"], "aliases": [x for x in (p.get("pin"), p.get("head")) if x],
            "legacySlugs": [],
            "dayIds": [f"day:{n:03d}" for n in day_nums], "dayEvidence": evidence,
            "url": f'places/{p["slug"]}.html',
        }
        key = (_name_key(p["name"]), p["type"])
        existing = places_by_name.get(key)
        if existing:
            existing["regionIds"] = sorted(set(existing["regionIds"] + record["regionIds"]))
            existing["dayIds"] = sorted(set(existing["dayIds"] + record["dayIds"]))
            existing["aliases"] = sorted(set(existing["aliases"] + record["aliases"]))
            existing["legacySlugs"].append(record["slug"])
        else:
            places_by_name[key] = record
            place_records.append(record)

    stays = []
    for row in _rows(tracker_path, "Accommodation"):
        rid = region_by_name.get(str(row["거점"]).lower())
        stays.append({
            "id": f'stay:{_slug(str(row["거점"]))}', "regionId": rid,
            "checkIn": row.get("체크인"), "checkOut": row.get("체크아웃"),
            "nights": row.get("박수"), "status": row.get("상태"),
            "area": row.get("생활권/후보"), "address": row.get("주소"),
            "bookingNumber": row.get("예약번호"), "sourceUrl": row.get("소스 URL"),
        })

    reservations = []
    for row in _rows(tracker_path, "Reservations"):
        reservations.append({
            "id": f'reservation:{str(row["ID"]).lower()}', "regionId": region_by_name.get(str(row.get("지역", "")).lower()),
            "scheduledDate": row.get("날짜"),
            "dayId": _day_id(row.get("날짜"), trip_start, trip_end),
            "category": row.get("카테고리"), "name": row.get("예약항목"),
            "status": row.get("상태"), "priority": row.get("우선순위"),
            "targetDate": row.get("예약목표일"), "sourceUrl": row.get("소스 URL"),
        })

    transports = []
    for row in _rows(tracker_path, "Transport"):
        transports.append({
            "id": f'transport:{str(row["구간ID"]).lower()}',
            "dayId": _day_id(row.get("날짜"), trip_start, trip_end),
            "from": row.get("출발지"), "to": row.get("도착지"), "mode": row.get("수단"),
            "status": row.get("예약상태"), "operator": row.get("사업자/편명"),
            "risk": row.get("핵심 리스크"), "fallback": row.get("대체안"),
        })

    return {"schemaVersion": SCHEMA_VERSION, "trip": {"start": trip_start.isoformat(), "end": trip_end.isoformat()},
            "regions": regions, "days": days, "places": place_records, "stays": stays,
            "reservations": reservations, "transports": transports}


def validate_graph(graph):
    errors = []
    collections = ("regions", "days", "places", "stays", "reservations", "transports")
    ids = []
    for name in collections:
        ids.extend(r["id"] for r in graph[name])
    if len(ids) != len(set(ids)):
        errors.append("record ID duplicate")
    known = set(ids)
    for name in collections:
        for row in graph[name]:
            for key, value in row.items():
                refs = value if key.endswith("Ids") and isinstance(value, list) else [value]
                if (key.endswith("Id") or key.endswith("Ids")):
                    for ref in refs:
                        if ref and ref not in known and not str(ref).startswith(("chapter:", "map:")):
                            errors.append(f'{row["id"]}.{key} -> {ref}')
    if len(graph["days"]) != 43:
        errors.append(f'days must be 43, got {len(graph["days"])}')
    return errors


def write_graph(graph, path: Path):
    path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
