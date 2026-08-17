#!/usr/bin/env python3
"""G1 — 방문 요일 vs 휴관 요일 충돌.

itinerary.json 으로 Day↔날짜↔요일 표를 만들고, 각 Day 섹션에서 참조된
place-facts 의 `closed` 값과 그 날 요일을 대조한다. 원고의 요일 리터럴이 아니라
**데이터의 closed 값**을 본다 — 원고가 틀렸어도 잡힌다.
"""
import re
import sys

from common import (FACT_RE, WD, chapter_files, day_sections, facts, report)

CLOSED_WD = re.compile(r"([월화수목금토일])(?:요일)?")


def closed_weekdays(value):
    """closed 값에서 요일 집합을 뽑는다. '월요일 다수 점포 휴무' → {월}"""
    if not value:
        return set()
    head = value.split("(")[0]
    return {m.group(1) for m in CLOSED_WD.finditer(head)}


def main():
    doc = facts()
    places = doc.get("places", {})
    problems = []
    for f in chapter_files():
        text = f.read_text(encoding="utf-8")
        for local, d, body in day_sections(text):
            wd = WD[d.weekday()]
            for pid, key in {(m.group(1), m.group(2)) for m in FACT_RE.finditer(body)}:
                p = places.get(pid)
                if not p:
                    continue
                cl = p.get("facts", {}).get("closed")
                if not cl:
                    continue
                if wd in closed_weekdays(cl.get("value", "")):
                    problems.append(
                        f"{f.name} Day {local} ({d.isoformat()} {wd}) — "
                        f"{p['displayName']} 휴관: {cl['value'][:50]}")
    return report("G1", "방문 요일 vs 휴관일", problems)


if __name__ == "__main__":
    sys.exit(main())
