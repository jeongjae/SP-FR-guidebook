#!/usr/bin/env python3
"""조사 CSV 의 가격대를 place-facts 의 사실 레코드로 옮긴다.

    python3 scripts/migrate_price_range.py girona nice aix
    python3 scripts/migrate_price_range.py --all --dry-run

FCR 조사 라운드가 지역마다 `price_range`·`source_url`·`verified_at` 을 이미
기록해 두었다. 그런데 사이트가 읽는 정본은 `data/place-facts.json` 이라,
CSV 에만 있는 값은 화면에 '미확인' 으로 나온다. 이 스크립트가 그 간극을
옮긴다 — **값을 만들지 않는다.** CSV 에 없으면 넘어간다.

규칙 셋.
  · 이미 place-facts 에 `price_range` 가 있으면 건드리지 않는다 (손편집 보존)
  · 출처 URL 과 확인일이 없는 행은 옮기지 않는다 — 근거 없는 값은 사실이 아니다
  · 신뢰도는 형제 사실(hours·booking)과 같게 둔다. 같은 조사·같은 출처·같은
    날짜에서 나온 값이라 한 항목만 다른 등급을 주면 화면이 거짓말을 한다
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

import model  # noqa: E402

FACTS = ROOT / "data" / "place-facts.json"
RESEARCH_GLOBS = ("FCR0*RESTAURANT*.csv", "FCR0*RESEARCH.csv")
TTL_DAYS = 180


def research_rows() -> dict[str, dict]:
    rows: dict[str, dict] = {}
    seen_files = set()
    for pattern in RESEARCH_GLOBS:
        for path in sorted(glob.glob(str(ROOT / pattern))):
            if path in seen_files:
                continue
            seen_files.add(path)
            for row in csv.DictReader(open(path, encoding="utf-8")):
                slug = (row.get("place_slug") or "").strip()
                if slug and slug not in rows:
                    rows[slug] = {**row, "_file": Path(path).name}
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("regions", nargs="*")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    trip = model.load_trip()
    wanted = set(args.regions) or ({r.slug for r in trip.regions} if args.all else set())
    if not wanted:
        parser.error("지역을 적거나 --all 을 준다")

    rows = research_rows()
    payload = json.loads(FACTS.read_text(encoding="utf-8"))
    places = payload["places"]

    moved, skipped = [], []
    for slug, place in sorted(trip.places.items()):
        if place.region not in wanted:
            continue
        row = rows.get(slug)
        if not row or not row.get("price_range"):
            continue
        if slug not in places:
            skipped.append((slug, "place-facts 에 항목이 없다"))
            continue
        facts = places[slug].setdefault("facts", {})
        if "price_range" in facts:
            skipped.append((slug, "이미 있다 — 손대지 않는다"))
            continue
        source = (row.get("source_url") or "").strip()
        verified = (row.get("verified_at") or "").strip()
        if not source.startswith("http") or not verified:
            skipped.append((slug, "출처 URL·확인일이 없다"))
            continue
        sibling = facts.get("hours") or facts.get("booking") or {}
        facts["price_range"] = {
            "value": row["price_range"].strip(),
            "confidence": sibling.get("confidence", "secondary"),
            "source": source,
            "verified_at": verified,
            "ttl_days": TTL_DAYS,
        }
        moved.append((place.region, slug, row["price_range"].strip(), verified,
                      row["_file"]))

    for region, slug, value, verified, src in moved:
        print(f"  + {region:10s} {slug:34s} {value:16s} {verified}  ({src})")
    for slug, why in skipped:
        print(f"  · {slug:34s} 건너뜀 — {why}")

    if moved and not args.dry_run:
        FACTS.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
    print(f"\n이관 {len(moved)}건 · 건너뜀 {len(skipped)}건"
          + (" (dry-run)" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
