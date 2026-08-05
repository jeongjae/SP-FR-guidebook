#!/usr/bin/env python3
"""Bootstrap 43 editable day JSON files from a named itinerary source ref.

This script is intentionally separate from normal rendering. Re-running it
overwrites day JSON files, so it requires --force and should only be used when
the schedule source itself changes.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "daily-cards"
DEFAULT_REF = "feat/itinerary-marseille-arles"
MASTER = "source/CURRENT/10_Core/03_Whole_Trip_Master_Itinerary_v1.2.md"
AUDIT = "source/OPERATIONS/100_Whole_Trip_43_Day_Execution_Audit_v1.0.md"
TRIP_START = date(2026, 8, 29)


def git_text(ref: str, path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{ref}:{path}"], cwd=ROOT, text=True, encoding="utf-8"
    )


def table_rows(text: str, expected: int) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if not re.match(r"^\|\s*\d+\s*\|", line):
            continue
        cells = [cell.strip().replace("**", "") for cell in line.strip("|").split("|")]
        if len(cells) == expected:
            rows.append(cells)
    if len(rows) != 43:
        raise SystemExit(f"expected 43 rows, found {len(rows)}")
    return rows


def slug(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value or "stop"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-ref", default=DEFAULT_REF)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    existing = sorted(OUT.glob("day-??.json"))
    if existing and not args.force:
        raise SystemExit("day JSON already exists; pass --force to replace it")

    master_rows = table_rows(git_text(args.source_ref, MASTER), 8)
    audit_rows = table_rows(git_text(args.source_ref, AUDIT), 11)
    audit_by_day = {int(row[0]): row for row in audit_rows}
    source_commit = subprocess.check_output(
        ["git", "rev-parse", args.source_ref], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()

    OUT.mkdir(parents=True, exist_ok=True)
    for cells in master_rows:
        day = int(cells[0])
        _, _date_label, city, title, core, optional, fatigue, lock = cells
        audit = audit_by_day[day]
        actual_date = TRIP_START + timedelta(days=day - 1)
        raw_stops = [part.strip() for part in re.split(r",\s*", core) if part.strip()]
        stops = []
        used = set()
        for order, name in enumerate(raw_stops[:6], 1):
            stop_id = slug(name)
            if stop_id in used:
                stop_id = f"{stop_id}-{order}"
            used.add(stop_id)
            stops.append({
                "id": stop_id,
                "order": order,
                "start": None,
                "end": None,
                "name": name,
                "category": "sight",
                "lat": None,
                "lng": None,
                "summary": name,
                "menu": None,
                "reservation": lock if lock != "없음" else None,
                "optional": False,
            })

        payload = {
            "schemaVersion": "1.0",
            "day": day,
            "date": actual_date.isoformat(),
            "city": city,
            "title": title,
            "sourceStatus": "candidate-latest-needs-review",
            "prototypeType": None,
            "startTime": None,
            "endTime": None,
            "totalDuration": None,
            "totalDistance": None,
            "fatigue": fatigue,
            "hotel": {"name": None, "lat": None, "lng": None, "status": "needs-review"},
            "stops": stops,
            "legs": [],
            "transport": [lock] if lock != "없음" else [],
            "food": [audit[6]],
            "highlights": [core, f"선택·축소: {optional}"],
            "backup": audit[9],
            "map": None,
            "needsReview": [
                "숙소명과 좌표 확정",
                "각 일정의 시작·종료 시각 확정",
                "방문지 좌표 검증",
                "모든 이동구간의 교통수단·거리·시간·경로 확정",
                f"최신 후보 일정 브랜치 승인: {source_commit[:12]}",
            ],
            "sourceRefs": [
                f"{source_commit}:{MASTER}",
                f"{source_commit}:{AUDIT}",
            ],
        }
        (OUT / f"day-{day:02d}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(f"wrote 43 day files from {args.source_ref} ({source_commit[:12]})")


if __name__ == "__main__":
    main()
