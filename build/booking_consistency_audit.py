"""Validate that Prepare and Paris Museum render one Booking SOT."""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
sys.path.insert(0, str(ROOT / "build"))
import render  # noqa: E402


def main() -> int:
    records = render.paris_booking_records()
    errors: list[str] = []
    ids = [r["id"] for r in records]
    if len(ids) != len(set(ids)):
        errors.append("duplicate booking id")
    if len(records) != 19:
        errors.append(f"Paris SOT record count {len(records)} != 19")
    expected = {
        "grand-palais|2026-09-25|special",
        "paris-museum-pass|2026-09-26|144h",
        "versailles|2026-09-29|10:00",
        "musee-de-l-orangerie|2026-09-30|permanent",
        "musee-d-orsay|2026-10-01|10:30",
        "qatar-prix-de-l-arc|2026-10-04|general-entry",
    }
    if set(ids) & expected != expected:
        errors.append("representative Paris booking missing")
    statuses = Counter(r["canonical_status"] for r in records)
    if statuses != Counter({"booked": 6, "book-later": 8, "book-now": 3,
                            "check-sale": 1, "no-reservation": 1}):
        errors.append(f"unexpected Paris status counts: {dict(statuses)}")
    res = render.load_reservations()
    all_prepare = res["confirmed"] + res["todo"] + res.get("not_required", [])
    if any(r.get("예약항목") in render.PARIS_BOOKING_DUPLICATE_TITLES
           for r in all_prepare if not r.get("_canonical_paris")):
        errors.append("tracker duplicate/aggregate Paris booking leaked into Prepare")
    if Counter(r.get("_booking_id") for r in all_prepare if r.get("_canonical_paris")) != Counter(ids):
        errors.append("Prepare canonical Paris subset differs from SOT")
    prepare = (SITE / "prepare" / "index.html").read_text(encoding="utf-8")
    museum = (SITE / "prepare" / "paris-museums.html").read_text(encoding="utf-8")
    if "입장권 Paris 주요 미술관 시간지정권" in prepare or "입장권 Paris 주요 미술관 시간지정권" in museum:
        errors.append("aggregate Paris booking row rendered")
    cards = re.findall(r'class="paris-museum-card" data-museum-id="([^"]+)"[^>]*data-canonical-status="([^"]+)"', museum)
    if len(cards) != len(records) or Counter(i for i, _ in cards) != Counter(ids):
        errors.append("Paris Museum rendered cards differ from SOT")
    if Counter(s for _, s in cards) != statuses:
        errors.append("Paris Museum rendered status counts differ from SOT")
    if not re.search(r"전체 \(19\)", museum) or not re.search(r"예약 항목 — 19건", museum):
        errors.append("Paris Museum total is not data-derived")
    if not re.search(r"Booking SOT 기준 · 예약완료 6 · 예약필요 12 · 예약불필요 1", prepare):
        errors.append("Prepare Paris summary counts differ from SOT")
    print("Booking consistency audit")
    print(f"  SOT records: {len(records)}")
    print(f"  Paris Museum cards: {len(cards)}")
    print(f"  Prepare canonical Paris records: {sum(1 for r in all_prepare if r.get('_canonical_paris'))}")
    print("  duplicate booking id: 0" if len(ids) == len(set(ids)) else "  duplicate booking id: FAIL")
    print(f"  aggregate row rendered: {'yes' if 'aggregate Paris booking row rendered' in errors else 'no'}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: Prepare summary and Paris Museum detail share one Booking SOT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
