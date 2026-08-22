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
FACT_RE = re.compile(r"\{\{fact:([a-z0-9][a-z0-9-]*)\.([a-z_]+)(?:\|x\d+)?\}\}")
# 원고 절 번호('## 17. Day 1 — …')는 선택이다. 통폐합을 끝낸 챕터는 번호를
# 떼고 '## Day 1 — …' 로만 쓴다 — 번호를 필수로 두면 그 챕터의 Day 섹션이
# 통째로 안 잡혀 요일·달력 대조가 조용히 건너뛴다.
DAY_RE = re.compile(r"^##\s*(?:\d+\.\s*)?Day\s*(\d+)\s*—\s*(\d+)월\s*(\d+)일", re.M)


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
    """허용목록. `re:` 로 시작하는 줄은 정규식이다.

    (문자열, 정규식) 두 벌을 돌려준다. 시간표 행처럼 '모양'으로만 정의되는 것을
    코드 안에 숨기지 않고 목록에 명시하기 위한 것이다 — 숨겨 두면 스코프가 왜
    좁은지 아무도 모른다.
    """
    if not ALLOW.exists():
        return [], []
    plain, regex = [], []
    for l in ALLOW.read_text(encoding="utf-8").splitlines():
        l = l.strip()
        if not l or l.startswith("#"):
            continue
        (regex if l.startswith("re:") else plain).append(l[3:] if l.startswith("re:") else l)
    return plain, [re.compile(r) for r in regex]


def allowed(line, allow):
    plain, regex = allow
    return any(a in line for a in plain) or any(r.search(line) for r in regex)


def report(gid, title, problems, warn=False, scanned=None, universe=None):
    """가드 하나의 결과를 찍고 실패 수를 돌려준다.

    G1d — scanned 를 주면 커버리지를 함께 찍는다. **검사 대상이 0이면
    PASS 가 아니라 WARN 이다.** '대상 0'을 '이상 없음'으로 읽는 것이
    S0 G1 이 아무것도 검사하지 않고 통과한 원인이었다.

    T3-4 — universe 를 주면 같은 원칙을 비율로도 적용한다. 검사 대상이
    전체의 1% 미만이면 PASS 가 아니라 WARN 이다. 이 프로젝트는 같은 실패를
    세 번 했다 — G1 토큰 0 · G2 스코프 18줄 · closed 파서 실효 30건.
    셋 다 '거의 아무것도 안 봤는데 통과'였다.
    """
    zero_target = scanned is not None and scanned == 0
    thin = (scanned is not None and universe and scanned > 0
            and scanned / universe < 0.01)
    tag = "WARN" if (warn or zero_target or thin) else ("PASS" if not problems else "FAIL")
    print(f"[{gid}] {tag} · {title} — {len(problems)}건"
          + (f" · 검사 대상 {scanned}" if scanned is not None else "")
          + (f" / 전체 {universe} ({scanned / universe:.1%})" if universe else ""))
    if zero_target:
        print(f"    ※ 검사 대상 0 — 통과가 아니라 미검사다")
    if thin:
        print(f"    ※ 검사 대상이 전체의 1% 미만 — 통과로 읽으면 안 된다")
    for p in problems[:25]:
        print(f"    · {p}")
    if len(problems) > 25:
        print(f"    … 외 {len(problems) - 25}건")
    return 0 if (warn or not problems) else 1
