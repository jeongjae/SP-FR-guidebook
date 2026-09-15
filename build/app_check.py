#!/usr/bin/env python3
"""웹앱 스냅샷 검사 — site/app/data/ 가 앱이 믿을 수 있는 상태인가.

빌드가 내보낸 스냅샷을 앱 입장에서 다시 읽는다:
  1. manifest 의 파일 목록·해시·크기가 실제 파일과 일치하는가
  2. 일일카드 43개가 전부 있고 정본 스키마(data/daily-cards/schema.json)를
     통과하는가 — 클라이언트·적용 스크립트가 같은 모양을 쓰는 전제다
  3. trip.json 의 날짜·거점이 스냅샷 일일카드와 어긋나지 않는가
  4. places-index 슬러그 유일성과 지역 파일 존재
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
APP_DATA = ROOT / "site" / "app" / "data"
CARD_SCHEMA = ROOT / "data" / "daily-cards" / "schema.json"


def main() -> int:
    problems: list[str] = []
    manifest_path = APP_DATA / "manifest.json"
    if not manifest_path.exists():
        print("앱 스냅샷 없음: site/app/data/manifest.json — build/site.py 를 먼저 돌린다")
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    listed = {f["path"]: f for f in manifest.get("files", [])}
    actual = {p.relative_to(APP_DATA).as_posix()
              for p in APP_DATA.rglob("*") if p.is_file()} - {"manifest.json"}
    if set(listed) != actual:
        problems.append(f"manifest 목록 불일치: 누락 {sorted(actual - set(listed))[:5]} "
                        f"· 없는 파일 {sorted(set(listed) - actual)[:5]}")
    for rel, item in listed.items():
        path = APP_DATA / rel
        if not path.exists():
            continue
        data = path.read_bytes()
        if len(data) != item["bytes"]:
            problems.append(f"크기 불일치: {rel}")
        if hashlib.sha256(data).hexdigest() != item["sha256"]:
            problems.append(f"SHA-256 불일치: {rel}")

    schema = json.loads(CARD_SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    days = sorted((APP_DATA / "days").glob("day-*.json"))
    if len(days) != 43:
        problems.append(f"일일카드 {len(days)}개 (기대 43)")
    dates = {}
    for card_path in days:
        card = json.loads(card_path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(card), key=lambda e: e.json_path)
        for e in errors[:2]:
            problems.append(f"{card_path.name}: 스키마 위반 — {e.json_path}: {e.message[:80]}")
        dates[card.get("day")] = card.get("date")

    trip = json.loads((APP_DATA / "trip.json").read_text(encoding="utf-8"))
    for entry in trip.get("days", []):
        if dates.get(entry["n"]) != entry["date"]:
            problems.append(f"trip.json Day {entry['n']} 날짜 불일치: "
                            f"{entry['date']} != {dates.get(entry['n'])}")
    nights = sum(s["nights"] for s in trip.get("stays", []))
    expected = trip["trip"]["nights"] - trip["trip"].get("inflightNights", 0)
    if nights != expected:
        problems.append(f"stays 박수 합계 {nights} != {expected}")

    index = json.loads((APP_DATA / "places-index.json").read_text(encoding="utf-8"))
    slugs = [p["slug"] for p in index.get("places", [])]
    if len(slugs) != len(set(slugs)):
        problems.append("places-index 슬러그 중복")
    for region in {p["region"] for p in index.get("places", [])}:
        if not (APP_DATA / "places" / f"{region}.json").exists():
            problems.append(f"지역 장문 파일 누락: places/{region}.json")

    if problems:
        print("앱 스냅샷 검사 실패:")
        for problem in problems[:20]:
            print("  " + problem)
        return 1
    total = sum(f["bytes"] for f in listed.values())
    print(f"앱 스냅샷 검사 통과: {len(listed)}개 파일 · {total/1024:.0f} KiB · "
          f"일일카드 43 · 장소 {len(slugs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
