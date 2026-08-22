#!/usr/bin/env python3
"""G5 — Jason 확정 결정의 forbidden_patterns 잔존 검출.

decisions.json 이 정본이다. 결정이 뒤집히면 원고가 아니라 그 파일을 먼저 고친다.

**챕터 산문만 본다 — Day SOT(data/daily-cards/*.json)는 기본적으로 안 본다.**
DEC-A03(Saint-Paul-de-Vence 날짜)이 실제로 새고 있던 곳은 정확히 여기였다.
결정 레지스터는 9/8 을 금지했는데 실제 충돌은 day-12.json 이 9/9 에 Saint-Paul
을 두면서 생겼다 — 리터럴 문자열이 챕터에는 없고 JSON 에만 있어 G5 가 통과했다.

그렇다고 모든 결정이 매번 daily-cards 전체를 스캔하게 넓히지 않는다. 결정이
`"also_check_daily_cards": true` 를 명시할 때만 그 결정의 forbidden_patterns 를
day-*.json 원문에도 대조한다 — opt-in 이라 다른 12건의 동작은 그대로다.
"""
import fnmatch
import sys
from pathlib import Path

from common import ROOT, chapter_files, decisions, report

DAILY_CARDS = ROOT / "data" / "daily-cards"


def daily_card_files():
    return sorted(DAILY_CARDS.glob("day-*.json")) if DAILY_CARDS.exists() else []


def main():
    problems = []
    scanned = 0
    for d in decisions():
        pats = d.get("forbidden_patterns") or []
        scopes = d.get("scope") or ["*"]
        if not pats:
            continue
        for f in chapter_files():
            if not any(fnmatch.fnmatch(f.name, s) for s in scopes):
                continue
            scanned += 1
            for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                for pat in pats:
                    if pat in line:
                        problems.append(
                            f"{d['id']} {f.name}:{i} '{pat}' — {d['decision'][:34]}")
        if not d.get("also_check_daily_cards"):
            continue
        for f in daily_card_files():
            scanned += 1
            for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                for pat in pats:
                    if pat in line:
                        problems.append(
                            f"{d['id']} {f.name}:{i} '{pat}' — {d['decision'][:34]}")
    return report("G5", "확정 결정 잔재", problems, scanned=scanned)


if __name__ == "__main__":
    sys.exit(main())
