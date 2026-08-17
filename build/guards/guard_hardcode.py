#!/usr/bin/env python3
"""G2 — `{{fact:}}` 밖의 사실값 하드코딩 검출.

요금(€\\d) · 시각(\\d{1,2}:\\d{2}) · 요일 리터럴을 찾는다.
허용목록(allow_hardcode.txt)에 있는 줄은 건너뛴다.
S0 시점의 검출 수가 baseline 이고, S1 이 필수·우선추천 101곳에서 0 으로 만든다.
"""
import re
import sys

from common import FACT_RE, allowlist, chapter_files, report

MONEY = re.compile(r"€\s?\d")
TIME = re.compile(r"\b\d{1,2}:\d{2}\b")
WEEKDAY = re.compile(r"[월화수목금토일]요일\s*(?:휴관|휴무|정기휴일|영업)")
SKIP_LINE = re.compile(r"^\s*(?:>?\s*\||```|!\[|\[.*\]\(http)")


def main():
    allow = allowlist()
    problems = []
    counts = {"money": 0, "time": 0, "weekday": 0}
    for f in chapter_files():
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            s = line.strip()
            if not s or s.startswith("#") or SKIP_LINE.match(s):
                pass
            if any(a in s for a in allow):
                continue
            bare = FACT_RE.sub("", s)          # 토큰이 낸 값은 하드코딩이 아니다
            hits = []
            if MONEY.search(bare):
                hits.append("money"); counts["money"] += 1
            if TIME.search(bare):
                hits.append("time"); counts["time"] += 1
            if WEEKDAY.search(bare):
                hits.append("weekday"); counts["weekday"] += 1
            if hits:
                problems.append(f"{f.name}:{i} [{'/'.join(hits)}] {s[:70]}")
    rc = report("G2", "fact 토큰 밖 하드코딩", problems)
    print(f"    baseline: money {counts['money']} · time {counts['time']} · weekday {counts['weekday']}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
