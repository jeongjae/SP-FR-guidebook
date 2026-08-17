#!/usr/bin/env python3
"""Stage C — 전 챕터의 {{badge:pending}} 을 단일 REVERIFY 레지스터로 수집하고
실행성 기계 감사를 수행한다.

산출:
  docs/RS_RESTRUCTURE_REVERIFY_REGISTER_v1.0.md
  docs/RS_RESTRUCTURE_DEPARTURE_RECHECK_CALENDAR_v1.0.md

기계 감사:
  A 방문 요일 vs 휴관일 충돌
  B 43일 날짜·요일·거점 diff
  C 하루 핵심 행동/방문지 상한
  D Day 별 실행 가능성 PASS/CONDITIONAL/FAIL
"""
import json
import pathlib
import re
from datetime import date, timedelta

ROOT = pathlib.Path(__file__).resolve().parent.parent
CH = ROOT / "source/CURRENT/20_Regional_Chapters"
CARDS = ROOT / "data/daily-cards"
DOCS = ROOT / "docs"

TRIP_START = date(2026, 8, 29)
# 캘린더 경과 표시 기준일. 재생성 시 이 값을 그날로 갱신한다.
TODAY = "2026-08-17"
WD = "월화수목금토일"

PENDING_RE = re.compile(r"\{\{badge:pending\|([^}]*)\}\}")
DAY_RE = re.compile(r"^##\s*\d+\.\s*Day\s*(\d+)\s*—\s*(\d+)월\s*(\d+)일\s*(\S+)", re.M)
# 챕터마다 '오늘의 피로도: 4/5' · '피로도 3/5' 두 표기가 섞여 있다.
FATIGUE_RE = re.compile(r"(?:오늘의\s*)?피로도[:*\s]*([1-5](?:[–\-~][1-5])?)\s*/\s*5")

# 휴관 서술에서 요일을 뽑는다 — "화요일 휴관", "월요일 휴무"
CLOSED_RE = re.compile(r"([월화수목금토일])요일\s*(?:휴관|휴무|정기휴일)")


def chapters():
    return sorted(CH.glob("*.md"))


def collect_pending():
    rows = []
    for f in chapters():
        text = f.read_text(encoding="utf-8")
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            for note in PENDING_RE.findall(line):
                # 항목명: 표 행이면 첫 셀, 아니면 앞 40자
                if line.strip().startswith("|"):
                    cells = [c.strip() for c in line.strip().strip("|").split("|")]
                    item = re.sub(r"\*+", "", cells[0])[:60] if cells else ""
                else:
                    item = re.sub(r"[#>*\-]", "", line).strip()[:60]
                src_m = re.search(r"출처[:\s]*([^\s|]+\.[a-z]{2,})", line)
                date_m = re.search(r"(20\d\d-\d\d(?:-\d\d)?)", line)
                rows.append(dict(chapter=f.name, line=i, item=item or "(본문)",
                                 note=note.strip(),
                                 source=src_m.group(1) if src_m else "",
                                 verified=date_m.group(1) if date_m else ""))
    return rows


def audit_days():
    """43일 날짜·요일 정합 + 챕터 Day 섹션과 daily-card 대조."""
    problems, days = [], {}
    for f in chapters():
        text = f.read_text(encoding="utf-8")
        for m in DAY_RE.finditer(text):
            local, mon, dd, wd = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
            d = date(2026, mon, dd)
            expect_wd = WD[d.weekday()] + "요일"
            if wd != expect_wd:
                problems.append(f"{f.name} Day {local}: 요일 표기 '{wd}' (실제 {expect_wd})")
            gday = (d - TRIP_START).days + 1
            # 다음 Day 헤딩까지가 그 날의 본문이다.
            # 부제가 H2 인 챕터가 있어 단순히 다음 '## ' 로 자르면 본문이 사라진다.
            seg = text[m.end():]
            nxt = DAY_RE.search(seg)
            body = seg[:nxt.start()] if nxt else seg
            fm = FATIGUE_RE.search(body)
            prev = days.get(gday)
            if prev:
                # 전환일 — 떠나는 챕터와 도착 챕터 양쪽에 Day 섹션이 있다.
                prev.setdefault("also", []).append(
                    dict(chapter=f.name, fatigue=fm.group(1) if fm else None))
                continue
            days[gday] = dict(chapter=f.name, local=local, date=d.isoformat(),
                              fatigue=fm.group(1) if fm else None, body=body)
    missing = [n for n in range(1, 44) if n not in days]
    if missing:
        problems.append(f"챕터 Day 섹션이 없는 글로벌 Day: {missing}")
    notes = []
    for n, info in sorted(days.items()):
        card = CARDS / f"day-{n:02d}.json"
        cf = ""
        if card.exists():
            j = json.loads(card.read_text(encoding="utf-8"))
            if j.get("date") != info["date"]:
                problems.append(f"Day {n}: 날짜 불일치 챕터 {info['date']} vs 카드 {j.get('date')}")
            cf = str(j.get("fatigue", "")).strip()
        if not info["fatigue"]:
            # 챕터 Day 섹션에 인라인 표기가 없는 날 — 빌드는 챕터의 피로도 표에서 공급한다.
            notes.append(f"Day {n}: Day 섹션 인라인 피로도 없음 (표/카드에서 공급: {cf or '—'})")
            info["fatigue"] = cf or None
        elif cf and cf != info["fatigue"]:
            alt = [a["fatigue"] for a in info.get("also", [])]
            if cf in alt:
                notes.append(f"Day {n}: 전환일 — 떠나는 챕터 {info['fatigue']} / "
                             f"도착 챕터 {cf} (카드는 이동 기준값을 쓴다)")
            else:
                problems.append(f"Day {n}: 피로도 불일치 챕터 {info['fatigue']} vs 카드 {cf}")
    return problems, days, notes


def audit_weekday_closures(days):
    """방문 요일 vs 휴관 요일 충돌 — 같은 Day 본문 안에서 검사."""
    conflicts = []
    for n, info in sorted(days.items()):
        d = date.fromisoformat(info["date"])
        wd = WD[d.weekday()]
        for m in CLOSED_RE.finditer(info["body"]):
            if m.group(1) == wd:
                ctx = info["body"][max(0, m.start() - 90):m.end() + 40].replace("\n", " ")
                # '피한다·아니다·없다·금지' 같은 회피 서술이면 충돌이 아니다
                if re.search(r"피한|아니|없다|금지|말라|말 것|주의|재확인|대신", ctx):
                    continue
                conflicts.append(f"Day {n}({info['date']} {wd}): {ctx.strip()[:150]}")
    return conflicts


def audit_density(days):
    """하루 방문지 상한 — 등급 헤딩·굵은 장소 표기 수를 센다."""
    over = []
    for n, info in sorted(days.items()):
        rows = [l for l in info["body"].splitlines()
                if l.strip().startswith("|") and re.match(r"\|\s*\**\d{1,2}[:시]", l.strip())]
        bolds = set(re.findall(r"\*\*([^*]{2,40})\*\*", info["body"]))
        if len(rows) > 16:
            over.append(f"Day {n}: 시간표 행 {len(rows)}건 (16 초과)")
        if len(bolds) > 22:
            over.append(f"Day {n}: 강조 항목 {len(bolds)}개 (22 초과)")
    return over


def feasibility(days, conflicts, density):
    """Day 별 실행 가능성 판정."""
    bad_days = set()
    for line in conflicts:
        m = re.match(r"Day (\d+)", line)
        if m:
            bad_days.add(int(m.group(1)))
    cond_days = set()
    for line in density:
        m = re.match(r"Day (\d+)", line)
        if m:
            cond_days.add(int(m.group(1)))
    out = {}
    for n, info in sorted(days.items()):
        if n in bad_days:
            out[n] = ("FAIL", "방문 요일과 휴관일 충돌")
        elif n in cond_days:
            out[n] = ("CONDITIONAL", "하루 밀도 상한 초과 — 삭제 순서 적용 필요")
        elif info["fatigue"] and info["fatigue"][0] in "45":
            out[n] = ("CONDITIONAL", f"피로도 {info['fatigue']} — 삭제 순서·대안 확인")
        else:
            out[n] = ("PASS", "")
    return out


def main():
    rows = collect_pending()
    problems, days, notes = audit_days()
    conflicts = audit_weekday_closures(days)
    density = audit_density(days)
    verdicts = feasibility(days, conflicts, density)

    # ── REVERIFY 레지스터 ────────────────────────────────────────────
    by_ch = {}
    for r in rows:
        by_ch.setdefault(r["chapter"], []).append(r)
    out = ["# REVERIFY 단일 레지스터", "",
           "**생성:** `build/reverify_register.py` (자동 수집 — 손으로 고치지 말 것)",
           f"**수집 대상:** 8개 지역 챕터의 `{{{{badge:pending}}}}` 전량 · **{len(rows)}건**", "",
           "출처·최종확인일 열은 같은 행에 표기된 것만 추출한다. 비어 있으면 아직 공식 출처가 붙지 않은 항목이다.",
           ""]
    for ch in sorted(by_ch):
        out += [f"## {ch} — {len(by_ch[ch])}건", "",
                "| 행 | 항목 | 재확인 내용 | 출처 | 최종확인 | 담당 Phase |",
                "|---:|---|---|---|---|---|"]
        for r in by_ch[ch]:
            out.append(f"| {r['line']} | {r['item']} | {r['note']} | {r['source'] or '—'} | "
                       f"{r['verified'] or '—'} | Phase 6 |")
        out.append("")
    (DOCS / "RS_RESTRUCTURE_REVERIFY_REGISTER_v1.0.md").write_text("\n".join(out) + "\n",
                                                                   encoding="utf-8")

    # ── 출발 전 재검증 캘린더 ────────────────────────────────────────
    cal = ["# 출발 전 재검증 캘린더", "",
           "**생성:** `build/reverify_register.py`",
           "**기준:** 여행 시작 2026-08-29. 날짜가 걸린 pending 을 방문일 역산으로 배치한다.", ""]
    today = date.fromisoformat(TODAY)
    def mark(day_iso):
        d = date.fromisoformat(day_iso)
        if d < today:
            return f"**경과 ({day_iso}) — 즉시 착수**"
        return f"D-{(TRIP_START - d).days} ({day_iso})"
    cal += [f"> **오늘 {TODAY} 기준.** 지난 시점은 '경과'로 표시한다 — "
            "지난 날짜를 미래처럼 두면 현장에서 건너뛴다.", ""]
    cal += ["| 시점 | 할 일 | 근거 |", "|---|---|---|"]
    cal += [f"| {mark('2026-08-15')} | 숙소·렌터카 확정 예약 재확인, 미확정 숙소(Aix·Luberon) 현지 결정 자료 갱신 | 재작업 QA |",
            f"| {mark('2026-08-22')} | 미술관·전시 예약창 확인 (세잔 사이트·Granet·Mucem·Orsay·Grand Palais) | REVERIFY 레지스터 |",
            f"| {mark('2026-08-26')} | 시장 요일·휴관일 최종 확인, 파업·공사 공지 확인 | 요일 충돌 감사 |",
            f"| {mark('2026-08-28')} | 첫 3일(항공·숙소·사그라다) 최종 확인 | CF001·CF002 |",
            "| 각 지역 도착 전날 | 해당 지역 pending 항목 일괄 확인 (아래 지역별 건수) | 레지스터 |"]
    cal.append("")
    cal += ["| 지역 | 도착일 | pending 건수 |", "|---|---|---:|"]
    arrive = {"04_Barcelona_Sitges_v2.0.md": "2026-08-29",
              "05_Girona_Collioure_Emporda_v2.1.md": "2026-09-01",
              "06_Nice_Cote_d_Azur_v2.0.md": "2026-09-04",
              "07_Aix_en_Provence_v2.0.md": "2026-09-09",
              "08_Luberon_Farmhouse_v2.0.md": "2026-09-13",
              "09_Avignon_Alpilles_Pont_du_Gard_v2.0.md": "2026-09-16",
              "10_Lyon_v2.0.md": "2026-09-20",
              "11_Paris_Long_Stay_v2.0.md": "2026-09-24"}
    for ch in sorted(by_ch):
        cal.append(f"| {ch} | {arrive.get(ch, '—')} | {len(by_ch[ch])} |")
    cal.append("")
    (DOCS / "RS_RESTRUCTURE_DEPARTURE_RECHECK_CALENDAR_v1.0.md").write_text("\n".join(cal) + "\n",
                                                                            encoding="utf-8")

    # ── 콘솔 보고 ───────────────────────────────────────────────────
    print(f"REVERIFY 수집: {len(rows)}건 → docs/RS_RESTRUCTURE_REVERIFY_REGISTER_v1.0.md")
    print(f"43일 정합 감사: 문제 {len(problems)}건")
    for p in problems[:20]:
        print("  ·", p)
    print(f"  (참고) Day 섹션 인라인 피로도 없는 날 {len(notes)}건 — 챕터 표/카드에서 공급")
    print(f"요일 vs 휴관 충돌: {len(conflicts)}건")
    for c in conflicts[:20]:
        print("  ·", c)
    print(f"하루 밀도 상한 초과: {len(density)}건")
    for d in density[:20]:
        print("  ·", d)
    n_fail = sum(1 for v, _ in verdicts.values() if v == "FAIL")
    n_cond = sum(1 for v, _ in verdicts.values() if v == "CONDITIONAL")
    print(f"실행 가능성: PASS {len(verdicts) - n_fail - n_cond} · CONDITIONAL {n_cond} · FAIL {n_fail}")
    for n, (v, why) in sorted(verdicts.items()):
        if v != "PASS":
            print(f"  Day {n}: {v} — {why}")
    return 1 if (problems or n_fail) else 0


if __name__ == "__main__":
    raise SystemExit(main())
