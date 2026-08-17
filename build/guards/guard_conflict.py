#!/usr/bin/env python3
"""G4 — 같은 사실의 다중 하드코딩 충돌.

두 가지를 본다.
 (a) place-facts 의 한 값이 원고에도 다른 값으로 하드코딩돼 있는가
 (b) 같은 시설명 옆에 서로 다른 요금·시각이 여러 번 나오는가

진단 §5-2 ①(사실값의 단일 소스 없음)이 만든 결함 유형이다.
"""
import re
import sys
from collections import defaultdict

from common import FACT_RE, chapter_files, facts, report

MONEY = re.compile(r"€\s?\d[\d.,]*")
TIME = re.compile(r"\b\d{1,2}:\d{2}\b")


def main():
    doc = facts()
    places = doc.get("places", {})
    problems = []

    # (a) displayName 이 있는 줄에서 place-facts 값과 다른 요금이 나오는가
    for f in chapter_files():
        text = f.read_text(encoding="utf-8")
        for pid, p in places.items():
            name = p["displayName"]
            if len(name) < 4 or name not in text:
                continue
            pa = p.get("facts", {}).get("price_adult", {}).get("value", "")
            if not pa:
                continue
            known = set(MONEY.findall(pa))
            if not known:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                if name not in line:
                    continue
                bare = FACT_RE.sub("", line)
                found = set(MONEY.findall(bare))
                odd = {x for x in found if x.replace(" ", "") not in
                       {k.replace(" ", "") for k in known}}
                if odd:
                    problems.append(
                        f"{f.name}:{i} {name} — 원고 {sorted(odd)} vs facts {sorted(known)}")

    # (b) 같은 (파일, 시설명) 에서 서로 다른 시각 집합이 3회 이상 흩어져 있는가
    for f in chapter_files():
        text = f.read_text(encoding="utf-8")
        per = defaultdict(set)
        for line in text.splitlines():
            for pid, p in places.items():
                name = p["displayName"]
                if len(name) >= 4 and name in line:
                    for t in TIME.findall(FACT_RE.sub("", line)):
                        per[(f.name, name)].add(t)
        for (fn, name), times in per.items():
            if len(times) >= 6:
                problems.append(f"{fn} {name} — 시각 {len(times)}종 흩어짐: {sorted(times)[:6]}…")

    return report("G4", "같은 사실 다중 하드코딩 충돌", problems)


if __name__ == "__main__":
    sys.exit(main())
