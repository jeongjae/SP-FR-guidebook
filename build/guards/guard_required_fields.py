#!/usr/bin/env python3
"""G3 — 필수·우선추천 등급인데 hours/closed/price_adult/booking 미참조.

S0·S1 에서는 경고(exit 0), 2026-08-22 부터 실패로 승격한다 (지시서 T0-4).
"""
import sys
from datetime import date

from common import FACT_RE, chapter_files, facts, report

REQUIRED = ("hours", "closed", "price_adult", "booking")
STRICT_FROM = date(2026, 8, 22)


def main():
    doc = facts()
    places = doc.get("places", {})
    referenced = {}
    for f in chapter_files():
        for m in FACT_RE.finditer(f.read_text(encoding="utf-8")):
            referenced.setdefault(m.group(1), set()).add(m.group(2))

    problems = []
    for pid, p in places.items():
        if p.get("grade") not in ("essential", "priority"):
            continue
        have = referenced.get(pid, set())
        missing = [k for k in REQUIRED if k not in have]
        if missing:
            problems.append(f"{p['displayName']} ({pid}) 미참조: {', '.join(missing)}")
    warn = date.today() < STRICT_FROM
    scanned = sum(1 for p in places.values() if p.get("grade") in ("essential", "priority"))
    rc = report("G3", "필수·우선추천 필수항목 참조", problems, warn=warn, scanned=scanned)
    if warn:
        print(f"    ※ {STRICT_FROM} 부터 실패로 승격")
    return rc


if __name__ == "__main__":
    sys.exit(main())
