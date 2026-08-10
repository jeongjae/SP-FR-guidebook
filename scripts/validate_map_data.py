#!/usr/bin/env python3
"""Validate the canonical map registry, region groups, and daily routes.

The validator intentionally uses only the Python standard library so it can run
in the static-site build and in GitHub Actions without another dependency.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT / "source" / "ASSETS" / "maps"
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLACE_TYPES = {"accommodation", "attraction", "market", "station", "airport", "parking", "rental"}
MODES = {"walking", "driving", "transit", "bicycling"}
STATUSES = {"confirmed", "planned", "candidate", "alternative"}


def _load(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.name}: 읽을 수 없는 JSON — {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.name}: 최상위 값은 객체여야 함")
        return {}
    if value.get("schemaVersion") != "1.0":
        errors.append(f"{path.name}: schemaVersion은 1.0이어야 함")
    return value


def _valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate(data_dir: Path = DEFAULT_DATA_DIR) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    registry = _load(data_dir / "place-registry.json", errors)
    routes = _load(data_dir / "daily-routes.json", errors)
    groups = _load(data_dir / "region-groups.json", errors)
    if errors:
        return errors, warnings

    places = registry.get("places")
    if not isinstance(places, list) or not places:
        return ["place-registry.json: places는 비어 있지 않은 배열이어야 함"], warnings

    by_id: dict[str, dict] = {}
    required = {
        "id", "name", "city", "type", "lat", "lng", "googlePlaceId",
        "googleMapsUrl", "address", "private", "approximate", "optional", "status",
    }
    for index, place in enumerate(places):
        label = f"place[{index}]"
        if not isinstance(place, dict):
            errors.append(f"{label}: 객체여야 함")
            continue
        missing = required - set(place)
        if missing:
            errors.append(f"{label}: 필수 필드 누락 — {', '.join(sorted(missing))}")
            continue
        pid = place["id"]
        label = f"place {pid!r}"
        if not isinstance(pid, str) or not ID_RE.fullmatch(pid):
            errors.append(f"{label}: 잘못된 ID 형식")
        if pid in by_id:
            errors.append(f"{label}: 중복 ID")
        by_id[pid] = place
        if not isinstance(place["name"], str) or not place["name"].strip():
            errors.append(f"{label}: name이 비어 있음")
        if place["type"] not in PLACE_TYPES:
            errors.append(f"{label}: 알 수 없는 type {place['type']!r}")
        if place["status"] not in STATUSES:
            errors.append(f"{label}: 알 수 없는 status {place['status']!r}")
        for field in ("private", "approximate", "optional"):
            if not isinstance(place[field], bool):
                errors.append(f"{label}: {field}는 boolean이어야 함")
        lat, lng = place["lat"], place["lng"]
        if not isinstance(lat, (int, float)) or isinstance(lat, bool) or not -90 <= lat <= 90:
            errors.append(f"{label}: lat 범위 오류")
        if not isinstance(lng, (int, float)) or isinstance(lng, bool) or not -180 <= lng <= 180:
            errors.append(f"{label}: lng 범위 오류")
        maps_url = place["googleMapsUrl"]
        if maps_url and not _valid_url(maps_url):
            errors.append(f"{label}: googleMapsUrl은 HTTPS URL이어야 함")
        if place.get("sourceUrl") and not _valid_url(place["sourceUrl"]):
            errors.append(f"{label}: sourceUrl은 HTTPS URL이어야 함")
        if place["private"]:
            if not place["approximate"]:
                errors.append(f"{label}: private 지점은 approximate=true여야 함")
            if place["address"] or place["googleMapsUrl"] or place["googlePlaceId"]:
                errors.append(f"{label}: private 지점은 주소·지도 URL·Place ID를 공개할 수 없음")
            if any(len(str(value).partition(".")[2].rstrip("0")) > 3 for value in (lat, lng)):
                errors.append(f"{label}: private 지점 좌표는 소수점 3자리 이하여야 함")
        elif not place["googleMapsUrl"]:
            warnings.append(f"{label}: Google Maps URL 없음")
        if not place["googlePlaceId"] and not place["private"]:
            warnings.append(f"{label}: Google Place ID 미확인")

    regions = groups.get("regions")
    if not isinstance(regions, list) or not regions:
        errors.append("region-groups.json: regions는 비어 있지 않은 배열이어야 함")
    else:
        region_ids: set[str] = set()
        for region in regions:
            if not isinstance(region, dict):
                errors.append("region: 객체여야 함")
                continue
            rid = region.get("id", "")
            if not ID_RE.fullmatch(rid):
                errors.append(f"region {rid!r}: 잘못된 ID 형식")
            if rid in region_ids:
                errors.append(f"region {rid!r}: 중복 ID")
            region_ids.add(rid)
            refs = region.get("placeIds")
            if not isinstance(refs, list) or not refs:
                errors.append(f"region {rid!r}: placeIds가 비어 있음")
                continue
            if len(refs) != len(set(refs)):
                errors.append(f"region {rid!r}: placeIds 중복")
            for ref in refs:
                if ref not in by_id:
                    errors.append(f"region {rid!r}: 없는 placeId {ref!r}")

    days = routes.get("days")
    if not isinstance(days, list) or not days:
        errors.append("daily-routes.json: days는 비어 있지 않은 배열이어야 함")
    else:
        dates: set[str] = set()
        for day in days:
            if not isinstance(day, dict):
                errors.append("day: 객체여야 함")
                continue
            date = day.get("date", "")
            label = f"day {date!r}"
            if date in dates:
                errors.append(f"{label}: 중복 날짜")
            dates.add(date)
            if day.get("defaultMode") not in MODES:
                errors.append(f"{label}: 잘못된 defaultMode")
            stops = day.get("stops")
            if not isinstance(stops, list) or not stops:
                errors.append(f"{label}: stops가 비어 있음")
                continue
            orders = [stop.get("order") for stop in stops if isinstance(stop, dict)]
            if len(orders) != len(set(orders)):
                errors.append(f"{label}: stop order 중복")
            for stop in stops:
                if not isinstance(stop, dict) or stop.get("placeId") not in by_id:
                    errors.append(f"{label}: 없는 stop placeId {getattr(stop, 'get', lambda *_: None)('placeId')!r}")
            for segment in day.get("segments", []):
                if not isinstance(segment, dict):
                    errors.append(f"{label}: segment는 객체여야 함")
                    continue
                for field in ("from", "to"):
                    if segment.get(field) not in by_id:
                        errors.append(f"{label}: segment {field}가 없는 placeId {segment.get(field)!r}")
                if segment.get("mode") not in MODES:
                    errors.append(f"{label}: 잘못된 segment mode {segment.get('mode')!r}")
                target = by_id.get(segment.get("to"))
                if target and target["private"] and not segment.get("manual"):
                    errors.append(f"{label}: private 목적지 segment는 manual=true여야 함")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_dir", nargs="?", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--quiet-warnings", action="store_true")
    args = parser.parse_args(argv)
    errors, warnings = validate(args.data_dir)
    if not args.quiet_warnings:
        for warning in warnings:
            print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"map data validation failed: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(f"map data validation passed ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
