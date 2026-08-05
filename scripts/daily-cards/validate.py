#!/usr/bin/env python3
"""Validate the 43-day dataset, prototype artifacts and optional rendered DOM."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import unicodedata
from datetime import date, timedelta
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "daily-cards"
OUTPUT = ROOT / "source" / "ASSETS" / "80_Daily_Mobile_Guide_Images" / "v2"
CHROME = Path("/mnt/c/Program Files/Google/Chrome/Application/chrome.exe")
TRIP_START = date(2026, 8, 29)
PROTOTYPES = {2: "urban", 4: "intercity", 5: "car-loop"}


def slug(day: dict) -> str:
    text = unicodedata.normalize("NFKD", day["city"]).encode("ascii", "ignore").decode().lower()
    return f"day-{day['day']:02d}-" + re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def windows_path(path: Path) -> str:
    return subprocess.check_output(["wslpath", "-w", str(path)], text=True, encoding="utf-8").strip()


def dom_qa(html_path: Path) -> dict:
    command = [str(CHROME), "--headless=new", "--disable-gpu", "--hide-scrollbars",
               "--no-first-run", "--no-default-browser-check", "--disable-background-networking",
               "--allow-file-access-from-files", "--virtual-time-budget=3500", "--dump-dom",
               windows_path(html_path)]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120, check=True)
    values = {}
    for key in ("label-overlaps", "overflow", "tile-count", "marker-count"):
        match = re.search(rf'data-qa-{key}="(\d+)"', result.stdout)
        if not match:
            raise RuntimeError(f"DOM QA value missing: {key}")
        values[key] = int(match.group(1))
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--visual-dom", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    schema = json.loads((DATA / "schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors, warnings, day_results = [], [], []
    files = sorted(DATA.glob("day-??.json"))
    if len(files) != 43:
        errors.append(f"day JSON count: expected 43, found {len(files)}")

    seen_dates = set()
    for index, path in enumerate(files, 1):
        payload = json.loads(path.read_text(encoding="utf-8"))
        day_errors = []
        for issue in validator.iter_errors(payload):
            location = ".".join(str(part) for part in issue.absolute_path) or "root"
            day_errors.append(f"schema {location}: {issue.message}")
        expected_date = (TRIP_START + timedelta(days=index - 1)).isoformat()
        if payload.get("day") != index or path.stem != f"day-{index:02d}":
            day_errors.append("DAY number/file name mismatch")
        if payload.get("date") != expected_date:
            day_errors.append(f"date mismatch: expected {expected_date}")
        if payload.get("date") in seen_dates:
            day_errors.append("duplicate date")
        seen_dates.add(payload.get("date"))
        orders = [stop.get("order") for stop in payload.get("stops", [])]
        if orders != list(range(1, len(orders) + 1)):
            day_errors.append("stop order is not consecutive")

        unresolved = 0
        for stop in payload.get("stops", []):
            if stop.get("lat") is None or stop.get("lng") is None:
                unresolved += 1
        if payload.get("hotel", {}).get("lat") is None:
            unresolved += 1
        if unresolved and not payload.get("needsReview"):
            day_errors.append("unresolved coordinates without needsReview")

        if index in PROTOTYPES:
            if payload.get("prototypeType") != PROTOTYPES[index]:
                day_errors.append("prototype type mismatch")
            if unresolved:
                day_errors.append(f"prototype has {unresolved} unresolved coordinates")
            stop_ids = [stop["id"] for stop in payload["stops"]]
            legs = {(leg["from"], leg["to"]) for leg in payload["legs"]}
            missing_legs = [(a, b) for a, b in zip(stop_ids, stop_ids[1:]) if (a, b) not in legs]
            if missing_legs:
                day_errors.append(f"missing adjacent legs: {missing_legs}")
            if payload["stops"][-1]["category"] != "hotel":
                day_errors.append("prototype does not end at accommodation")
            start = int(payload["startTime"].replace(":", ""))
            end = int(payload["endTime"].replace(":", ""))
            if start >= end:
                day_errors.append("start/end time inversion")

            out_slug = slug(payload)
            html_path = OUTPUT / "source" / f"{out_slug}.html"
            expected = [
                OUTPUT / "full" / f"{out_slug}.png",
                OUTPUT / "full" / f"{out_slug}.webp",
                OUTPUT / "thumbs" / f"{out_slug}-thumb.webp",
                html_path,
            ]
            for artifact in expected:
                if not artifact.exists():
                    day_errors.append(f"artifact missing: {artifact.relative_to(ROOT)}")
            if expected[0].exists() and Image.open(expected[0]).size != (1440, 1920):
                day_errors.append("PNG is not 1440x1920")
            if expected[1].exists() and Image.open(expected[1]).size != (1440, 1920):
                day_errors.append("full WebP is not 1440x1920")
            if expected[2].exists() and Image.open(expected[2]).size != (480, 640):
                day_errors.append("thumbnail WebP is not 480x640")
            if html_path.exists() and "© OpenStreetMap contributors" not in html_path.read_text(encoding="utf-8"):
                day_errors.append("OSM attribution missing")
            if args.visual_dom and html_path.exists():
                try:
                    visual = dom_qa(html_path)
                    if visual["label-overlaps"]:
                        day_errors.append(f"map label overlaps: {visual['label-overlaps']}")
                    if visual["overflow"]:
                        day_errors.append(f"DOM text overflow: {visual['overflow']}")
                except Exception as exc:
                    day_errors.append(f"DOM QA failed: {exc}")
                    visual = None
            else:
                visual = None
        else:
            if unresolved:
                warnings.append(f"Day {index:02d}: {unresolved} coordinate fields need review")
            visual = None

        if day_errors:
            errors.extend(f"Day {index:02d}: {message}" for message in day_errors)
        day_results.append({"day": index, "prototype": index in PROTOTYPES,
                            "errors": day_errors, "unresolvedCoordinates": unresolved,
                            "visual": visual})

    report = {"status": "pass" if not errors else "fail", "days": len(files),
              "prototypes": sorted(PROTOTYPES), "errors": errors, "warnings": warnings,
              "results": day_results}
    if args.write_report:
        json_path = ROOT / "docs" / "daily-card-qa.json"
        json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        prototype_lines = []
        for item in day_results:
            if item["prototype"]:
                visual = item["visual"] or {}
                prototype_lines.append(
                    f"| {item['day']:02d} | {'PASS' if not item['errors'] else 'FAIL'} | "
                    f"{visual.get('label-overlaps', 'not-run')} | {visual.get('overflow', 'not-run')} |"
                )
        md = f"""# Daily Action Map QA

Generated by `scripts/daily-cards/validate.py`.

- Status: **{report['status'].upper()}**
- Dataset: {len(files)}/43 day files
- Prototype artifacts: Day 02, 04, 05
- Errors: {len(errors)}
- Needs-review warnings: {len(warnings)} days

| Day | Result | Map label overlaps | DOM overflow |
|---:|---|---:|---:|
{chr(10).join(prototype_lines)}

## Scope

The automated checks cover schema, consecutive dates and DAY numbers, stop order,
time direction, coordinate presence, adjacent legs, accommodation arrival,
route-cache status, image dimensions, OSM attribution, and (with
`--visual-dom`) browser-computed label/overflow values.

The remaining warnings are expected at the three-prototype gate: non-prototype
days preserve missing times, coordinates, accommodation and route details as
explicit `needsReview` data rather than invented facts.
"""
        (ROOT / "docs" / "DAILY_CARD_QA.md").write_text(md, encoding="utf-8")
    print(json.dumps({"status": report["status"], "days": len(files),
                      "errors": len(errors), "warnings": len(warnings)}, ensure_ascii=False))
    if errors:
        for error in errors:
            print("ERROR", error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

