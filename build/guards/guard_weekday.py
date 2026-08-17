#!/usr/bin/env python3
"""G1 — 방문 요일 vs 휴관 요일 충돌 (T1-0b 보강판).

**보강 이유**: 이전 G1 은 Day 섹션 안의 `{{fact:}}` 참조만 봤다. 원고에 아직
토큰이 없었으므로 검사 대상이 0이었고, 그 상태로 "PASS 0건"을 냈다.
대상 0은 통과가 아니다 — 아래 G1d 가 이 상태를 WARN 으로 잡는다.

  G1a 스캔 범위를 챕터 전문으로. 방문일 판정은 세 단계다.
      ① 같은 줄·직전 줄의 날짜 리터럴 (9/22 · 9월 22일)
      ② 그 위치를 감싸는 Day 헤딩
      ③ place-days.json (엔트리매트릭스 days 열)
  G1b 날짜 리터럴 스캐너 — 우천 대안표·예약카드처럼 Day 섹션 밖에 있는 배치를 잡는다.
  G1c 챕터 Day 헤딩 날짜 ↔ itinerary day_calendar() 3자 대조.
  G1d 커버리지 보고 — 검사 대상 0이면 PASS 가 아니라 WARN.
"""
import json
import re
import sys

from common import (DAY_RE, FACT_RE, ITINERARY, ROOT, WD, chapter_files,
                    day_calendar, facts, load_json, report, trip_start)

PLACE_DAYS = ROOT / "data/place-days.json"

WD_ORDER = "월화수목금토일"
# 앞 글자가 한글이면 '공휴일'·'평일', 숫자면 '12월'·'25일' 의 끝글자를 요일로 오독한 것이다.
_WD = r"(?<![가-힣0-9])[월화수목금토일](?:요일)?"
# 요일(들) 바로 뒤에 휴관 표현이 붙은 것만 휴관 요일로 본다.
# "화요일 휴관" · "일요일·월요일 휴관" · "월–금 휴무" · "9/1~6/30 월요일 휴장"
CLOSED_WD = re.compile(
    rf"((?:{_WD})(?:\s*[·,및]\s*(?:{_WD}))*(?:\s*[~\-–]\s*(?:{_WD}))?)"
    r"\s*(?:은|는|만|에|엔|과|와)?\s*"
    r"(?:정기\s*)?(?:휴관|휴무|휴장|휴점|폐관|폐장|closed)")
WD_TOKEN = re.compile(_WD)
# "그 날은 닫혀서 못 간다"고 이미 쓴 줄은 충돌이 아니라 회피 서술이다.
AVOID = re.compile(r"불가|휴관|휴무|제외|대신|아니다|않는다|금지|피한|못\s|없다|"
                   r"decision-pending|대안|대체")
# 9/22 · 9월 22일 · 09/22
DATE_LIT = re.compile(r"(?<!\d)(\d{1,2})\s*[/월]\s*(\d{1,2})\s*일?(?!\d)")


def closed_weekdays(value):
    """휴관 요일만 뽑는다. 영업시간 나열('월–금 09:00')을 휴관으로 읽으면 안 된다."""
    if not value:
        return set()
    out = set()
    for m in CLOSED_WD.finditer(value):
        span = m.group(1)
        wds = [t[0] for t in WD_TOKEN.findall(span)]
        if len(wds) == 2 and re.search(r"[~\-–]", span):     # "월–금" 은 범위다
            a, b = (WD_ORDER.index(w) for w in wds)
            out |= {WD_ORDER[i] for i in range(a, b + 1)} if a <= b else {wds[0], wds[1]}
        else:
            out |= set(wds)
    return out


def line_date(line, year):
    """줄에서 날짜 리터럴을 뽑는다. 여행 기간(8/29–10/10) 안의 것만."""
    from datetime import date as _d
    out = []
    for m in DATE_LIT.finditer(line):
        mo, dd = int(m.group(1)), int(m.group(2))
        if not (1 <= mo <= 12 and 1 <= dd <= 31):
            continue
        try:
            d = _d(year, mo, dd)
        except ValueError:
            continue
        if _d(year, 8, 29) <= d <= _d(year, 10, 10):
            out.append(d)
    return out


def day_of_line(lines, idx, day_spans, year):
    """줄 idx 의 방문일 판정 — ① 리터럴 ② 감싸는 Day 헤딩."""
    for probe in (idx, idx - 1, idx - 2):
        if 0 <= probe < len(lines):
            ds = line_date(lines[probe], year)
            if ds:
                return ds[0], "literal"
    for start, end, d in day_spans:
        if start <= idx < end:
            return d, "day-heading"
    return None, None


def main():
    doc = facts()
    places = doc.get("places", {})
    pdays = load_json(PLACE_DAYS, {"places": {}}).get("places", {})
    cal = day_calendar()
    year = trip_start().year

    problems, g1c = [], []
    checked = skipped_no_closed = skipped_no_day = avoided = 0
    by_source = {"literal": 0, "day-heading": 0, "place-days": 0}

    # 이름 → placeId (본문에 토큰이 없어도 시설명으로 잡는다)
    name_to_pid = {}
    for pid, p in places.items():
        nm = p["displayName"]
        if len(nm) >= 4:
            name_to_pid.setdefault(nm, pid)

    for f in chapter_files():
        text = f.read_text(encoding="utf-8")
        lines = text.splitlines()

        # G1c — Day 헤딩 날짜가 itinerary 달력과 맞는가
        spans = []
        ms = list(DAY_RE.finditer(text))
        for i, m in enumerate(ms):
            from datetime import date as _d
            d = _d(year, int(m.group(2)), int(m.group(3)))
            s_line = text[:m.start()].count("\n")
            e_line = (text[:ms[i + 1].start()].count("\n") if i + 1 < len(ms) else len(lines))
            spans.append((s_line, e_line, d))
            if d not in cal.values():
                g1c.append(f"{f.name} Day 헤딩 {d.isoformat()} — itinerary 달력 밖")

        # G1a/G1b — 전문 스캔
        for idx, line in enumerate(lines):
            hits = {(m.group(1), m.group(2)) for m in FACT_RE.finditer(line)}
            pids = {pid for pid, _ in hits}
            for nm, pid in name_to_pid.items():
                if nm in line:
                    pids.add(pid)
            if not pids:
                continue
            for pid in pids:
                p = places.get(pid)
                if not p:
                    continue
                cl = p.get("facts", {}).get("closed")
                if not cl or not cl.get("value"):
                    skipped_no_closed += 1
                    continue
                d, src = day_of_line(lines, idx, spans, year)
                if d is None:
                    days = pdays.get(pid, {}).get("days") or []
                    if days:
                        d, src = cal.get(days[0]), "place-days"
                if d is None:
                    skipped_no_day += 1
                    continue
                checked += 1
                by_source[src] = by_source.get(src, 0) + 1
                wd = WD[d.weekday()]
                if AVOID.search(line):
                    avoided += 1
                    continue
                if wd in closed_weekdays(cl["value"]):
                    problems.append(
                        f"{f.name}:{idx+1} [{src}] {d.isoformat()}({wd}) "
                        f"{p['displayName']} 휴관: {cl['value'][:40]}")

    rc = report("G1", "방문 요일 vs 휴관일", problems)
    rc_c = report("G1c", "Day 헤딩 ↔ itinerary 3자 대조", g1c)

    total = checked + skipped_no_closed + skipped_no_day + avoided
    print(f"    커버리지: 검사 {checked} / 후보 {total} · "
          f"건너뜀 {skipped_no_closed}(closed 없음) + {skipped_no_day}(방문일 판정 실패) "
          f"+ {avoided}(회피 서술)")
    print(f"    판정 출처: " + " · ".join(f"{k} {v}" for k, v in by_source.items() if v))
    if checked == 0:
        print("[G1d] WARN · 검사 대상 0 — 통과가 아니라 미검사다")
        return 1
    return rc or rc_c


if __name__ == "__main__":
    sys.exit(main())
