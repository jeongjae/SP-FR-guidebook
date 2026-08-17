#!/usr/bin/env python3
"""G6 — verified_at + ttl_days 초과 사실 목록 (경고).

--trip-start 를 주면 그 날짜 기준으로 판정한다 (D-2 게이트용).
"""
import argparse
import sys
from datetime import date, datetime

from common import facts, report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trip-start")
    a = ap.parse_args()
    today = datetime.strptime(a.trip_start, "%Y-%m-%d").date() if a.trip_start else date.today()

    doc = facts()
    ttl_def = doc.get("ttl_defaults", {})
    stale, unreachable = [], []
    for pid, p in doc.get("places", {}).items():
        for k, fct in p.get("facts", {}).items():
            if fct.get("confidence") == "unreachable":
                unreachable.append(f"{p['displayName']}.{k} — {fct.get('blocked_reason','')[:50]}")
                continue
            va = fct.get("verified_at")
            if not va:
                continue
            ttl = fct.get("ttl_days") or ttl_def.get(k, 90)
            d = datetime.strptime(va, "%Y-%m-%d").date()
            over = (today - d).days - ttl
            if over > 0:
                stale.append(f"{p['displayName']}.{k} — {va} +{ttl}일, {over}일 초과")
    rc = report("G6", f"신선도 (기준 {today})", stale, warn=True)
    print(f"    unreachable {len(unreachable)}건 — 전화 문의 대상")
    return rc


if __name__ == "__main__":
    sys.exit(main())
