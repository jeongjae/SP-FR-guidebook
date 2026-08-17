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
# 2인 합계·범위·예산은 1인 요금과 다른 축이다 — 충돌이 아니다.
PER_TWO = re.compile(r"/\s*2\s*인|2인\s*€|€[\d.,]+\s*[–\-~]\s*[\d.,]+|예산|예상")


def money_norm(s):
    """€36.00 과 €36 을 같은 값으로 본다."""
    v = s.replace("€", "").replace(" ", "").rstrip(".,")
    try:
        return f"{float(v):.2f}"
    except ValueError:
        return v


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
            known = {money_norm(x) for x in MONEY.findall(pa)}
            if not known:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                if name not in line:
                    continue
                # 시설명이 다른 고유명사의 일부인 경우 (La Paradeta Sagrada Família)
                pos = line.find(name)
                if pos > 0 and line[pos - 1] not in " |*·(>":
                    continue
                if PER_TWO.search(line):
                    continue
                bare = FACT_RE.sub("", line)
                found = {money_norm(x) for x in MONEY.findall(bare)}
                odd = found - known
                if odd:
                    problems.append(
                        f"{f.name}:{i} {name} — 원고 {sorted(odd)} vs facts {sorted(known)}")

    # (b) '시각 흩어짐' 규칙은 제거했다 — 시간표에는 원래 여러 시각이 있어
    #     오탐만 냈다. 시각 충돌은 G1(요일)·G1c(날짜)가 다른 축으로 잡는다.

    scanned = sum(1 for pid, p in places.items()
                  if p.get("facts", {}).get("price_adult", {}).get("value"))
    return report("G4", "같은 사실 다중 하드코딩 충돌", problems, scanned=scanned)


if __name__ == "__main__":
    sys.exit(main())
