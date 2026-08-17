#!/usr/bin/env python3
"""T2-1 — data/verify-queue.csv 생성.

**FRESH 와 BLOCKED 는 조사 대상에서 자동 제외한다.** 이것이 중복 조사를 막는 지점이다.

priority
  P0  closed 전부 (G1 커버리지가 곧 closed 보유 수다 — 이번 세션 최우선)
      + 확정 등급(essential·priority)의 hours · booking
      + 일정에 고정된 식당·시장의 영업일
  P1  확정 등급의 price_adult · getting_there
  P2  그 외
"""
import csv
import json
import pathlib
from datetime import date, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
FACTS = ROOT / "data/place-facts.json"
PLACE_DAYS = ROOT / "data/place-days.json"
OUT = ROOT / "data/verify-queue.csv"

KEYS = ["closed", "hours", "booking", "price_adult", "getting_there", "duration"]
CONFIRMED = ("essential", "priority")
# 영업일이 일정에 직접 걸리는 유형 — 이름으로 판별한다
EATERY_HINT = ("marche", "marché", "mercat", "market", "시장", "restaurant", "bistrot",
               "café", "cafe", "bar-", "halles", "bouillon", "chez-", "la-", "le-")


def load(p, d):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else d


def is_eatery(pid, place):
    n = (pid + " " + place["displayName"]).lower()
    return any(h in n for h in EATERY_HINT)


def status_of(fact, key, ttl_defaults, today):
    if fact is None:
        return "MISSING"
    conf = fact.get("confidence", "unverified")
    if conf == "unreachable":
        return "BLOCKED"
    if not (fact.get("value") or "").strip():
        return "MISSING"
    if conf in ("unverified",):
        return "MISSING"
    va = fact.get("verified_at")
    if not va:
        return "STALE"
    ttl = fact.get("ttl_days") or ttl_defaults.get(key, 90)
    d = datetime.strptime(va, "%Y-%m-%d").date()
    return "STALE" if (today - d).days > ttl else "FRESH"


def priority_of(pid, place, key, scheduled):
    grade = place.get("grade", "none")
    if key == "closed":
        return "P0"
    if grade in CONFIRMED and key in ("hours", "booking"):
        return "P0"
    if key == "hours" and pid in scheduled and is_eatery(pid, place):
        return "P0"
    if grade in CONFIRMED and key in ("price_adult", "getting_there"):
        return "P1"
    return "P2"


def main():
    doc = load(FACTS, {"places": {}})
    places = doc.get("places", {})
    ttl_defaults = doc.get("ttl_defaults", {})
    pdays = load(PLACE_DAYS, {"places": {}}).get("places", {})
    scheduled = set(pdays)
    today = date.today()

    rows = []
    for pid, place in sorted(places.items()):
        facts = place.get("facts", {})
        for key in KEYS:
            f = facts.get(key)
            st = status_of(f, key, ttl_defaults, today)
            if st == "MISSING" and key in ("duration", "getting_there") \
               and place.get("grade") not in CONFIRMED:
                continue                      # 확정 등급 아닌 곳의 부가 키는 큐에 넣지 않는다
            rows.append({
                "placeId": pid,
                "fact_key": key,
                "status": st,
                "priority": priority_of(pid, place, key, scheduled),
                "last_attempt": (f or {}).get("verified_at", ""),
                "blocked_reason": (f or {}).get("blocked_reason", ""),
                "phone": place.get("phone", ""),
                "source_hint": (f or {}).get("source", ""),
                "region": place.get("region", ""),
                "grade": place.get("grade", "none"),
                "displayName": place["displayName"],
                "days": ";".join(str(d) for d in pdays.get(pid, {}).get("days", [])),
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    import collections
    st = collections.Counter(r["status"] for r in rows)
    pr = collections.Counter(r["priority"] for r in rows)
    todo = [r for r in rows if r["status"] not in ("FRESH", "BLOCKED")]
    todo_p0 = [r for r in todo if r["priority"] == "P0"]
    print(f"큐 {len(rows)}행 → {OUT.relative_to(ROOT)}")
    print(f"status: {dict(st)}")
    print(f"priority: {dict(pr)}")
    print(f"조사 대상(FRESH·BLOCKED 제외): {len(todo)} · 그중 P0 {len(todo_p0)}")
    print(f"  P0 중 closed: {sum(1 for r in todo_p0 if r['fact_key'] == 'closed')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
