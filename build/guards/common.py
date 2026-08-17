#!/usr/bin/env python3
"""가드 공통 — 경로·로딩·Day↔날짜 표·출력 형식."""
import json
import pathlib
import re
from datetime import date, datetime, timedelta

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
CHAPTERS = ROOT / "source/CURRENT/20_Regional_Chapters"
FACTS = ROOT / "data/place-facts.json"
DECISIONS = ROOT / "data/decisions.json"
ITINERARY = ROOT / "source/CURRENT/10_Core/itinerary.json"
ALLOW = pathlib.Path(__file__).resolve().parent / "allow_hardcode.txt"

WD = "월화수목금토일"
FACT_RE = re.compile(r"\{\{fact:([a-z0-9][a-z0-9-]*)\.([a-z_]+)\}\}")
DAY_RE = re.compile(r"^##\s*\d+\.\s*Day\s*(\d+)\s*—\s*(\d+)월\s*(\d+)일", re.M)


def load_json(p, default=None):
    if not p.exists():
        return default if default is not None else {}
    return json.loads(p.read_text(encoding="utf-8"))


def facts():
    return load_json(FACTS, {"places": {}})


def decisions():
    d = load_json(DECISIONS, {"decisions": []})
    return d.get("decisions", d if isinstance(d, list) else [])


def trip_start():
    it = load_json(ITINERARY, {})
    s = (it.get("trip") or {}).get("start")
    return datetime.strptime(s, "%Y-%m-%d").date() if s else date(2026, 8, 29)


def day_calendar():
    """글로벌 Day 번호 → date. itinerary.json 의 trip.start 가 단일 진실이다."""
    start = trip_start()
    it = load_json(ITINERARY, {})
    n = (it.get("trip") or {}).get("days", 43)
    return {i: start + timedelta(days=i - 1) for i in range(1, n + 1)}


def chapter_files():
    return sorted(CHAPTERS.glob("*.md"))


def day_sections(text):
    """(글로벌 Day 없이) 챕터 안 Day 섹션: [(로컬번호, date, 본문)]"""
    out = []
    ms = list(DAY_RE.finditer(text))
    for i, m in enumerate(ms):
        d = date(trip_start().year, int(m.group(2)), int(m.group(3)))
        body = text[m.end(): ms[i + 1].start() if i + 1 < len(ms) else len(text)]
        out.append((int(m.group(1)), d, body))
    return out


def allowlist():
    if not ALLOW.exists():
        return []
    return [l.strip() for l in ALLOW.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")]


def report(gid, title, problems, warn=False, scanned=None):
    """가드 하나의 결과를 찍고 실패 수를 돌려준다.

    G1d — scanned 를 주면 커버리지를 함께 찍는다. **검사 대상이 0이면
    PASS 가 아니라 WARN 이다.** '대상 0'을 '이상 없음'으로 읽는 것이
    S0 G1 이 아무것도 검사하지 않고 통과한 원인이었다.
    """
    zero_target = scanned is not None and scanned == 0
    tag = "WARN" if (warn or zero_target) else ("PASS" if not problems else "FAIL")
    print(f"[{gid}] {tag} · {title} — {len(problems)}건"
          + (f" · 검사 대상 {scanned}" if scanned is not None else ""))
    if zero_target:
        print(f"    ※ 검사 대상 0 — 통과가 아니라 미검사다")
    for p in problems[:25]:
        print(f"    · {p}")
    if len(problems) > 25:
        print(f"    … 외 {len(problems) - 25}건")
    return 0 if (warn or not problems) else 1
