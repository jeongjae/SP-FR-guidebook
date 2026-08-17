#!/usr/bin/env python3
"""G2 — `{{fact:}}` 밖의 사실값 하드코딩 검출.

요금(€\\d) · 시각(\\d{1,2}:\\d{2}) · 요일 리터럴을 찾는다.
허용목록(allow_hardcode.txt)에 있는 줄은 건너뛴다.
S0 시점의 검출 수가 baseline 이고, S1 이 필수·우선추천 101곳에서 0 으로 만든다.
"""
import argparse
import json
import re
import sys

from common import (FACT_RE, FACTS, allowed, allowlist, chapter_files,
                    load_json, report)

MONEY = re.compile(r"€\s?\d")
TIME = re.compile(r"\b\d{1,2}:\d{2}\b")
WEEKDAY = re.compile(r"[월화수목금토일]요일\s*(?:휴관|휴무|정기휴일|영업)")

# --scope grade 용: 시설의 '운영정보'를 말하는 줄만 본다.
# 시간표 첫 칸의 방문 시각(| 09:20–10:10 | …)은 일정이지 사실값이 아니다.
OPS_HINT = re.compile(r"휴관|휴무|영업|개관|폐관|운영|요금|입장|성인|통합권|매표|"
                      r"개장|마지막 입장|정기휴")
TIMETABLE_ROW = re.compile(r"^\|\s*\**\d{1,2}[:시]")


def scoped_places(scope):
    """--scope grade → 필수·우선추천 등급 장소의 displayName 집합."""
    doc = load_json(FACTS, {"places": {}})
    return {p["displayName"] for p in doc.get("places", {}).values()
            if len(p["displayName"]) >= 4
            and (scope != "grade" or p.get("grade") in ("essential", "priority"))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=["all", "grade"], default="all",
                    help="grade = 필수·우선추천 장소의 운영정보 줄만 검사")
    args = ap.parse_args()
    names = scoped_places(args.scope) if args.scope == "grade" else None
    allow = allowlist()
    problems = []
    scanned = 0
    universe = 0
    counts = {"money": 0, "time": 0, "weekday": 0}
    for f in chapter_files():
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            s = line.strip()
            if not s:
                continue
            universe += 1
            if allowed(s, allow):
                continue
            if names is not None and s.startswith("|"):
                # 표 행의 주어는 첫 칸이다. 다른 칸에 이름이 스쳤다고 그 장소의
                # 운영정보인 것은 아니다.
                first = s.split("|")[1] if s.count("|") >= 2 else s
                if not any(nm in first for nm in names):
                    continue
            if names is not None:
                # 필수·우선추천 시설을 말하는 줄 전량.
                # 예전에는 여기서 OPS_HINT 로 한 번 더 걸렀고, 그래서 검사 대상이
                # 18줄이었다. 운영정보 서술을 말로 알아내려 한 것이 잘못이다 —
                # 아래 MONEY/TIME/WEEKDAY 가 이미 사실값만 고른다.
                if False:
                    continue
                if not any(nm in s for nm in names):
                    continue
            scanned += 1
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
    label = "fact 토큰 밖 하드코딩" + (" (필수·우선추천 운영정보)" if names is not None else "")
    rc = report("G2", label, problems, scanned=scanned, universe=universe)
    print(f"    baseline: money {counts['money']} · time {counts['time']} · weekday {counts['weekday']}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
