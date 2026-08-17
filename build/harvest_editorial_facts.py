#!/usr/bin/env python3
"""T4-0 — 빈 토큰을 **웹 조사가 아니라 원고에서 수확한다.**

`duration` 은 애초에 시설이 공표하는 값이 아니다. 체류 시간은 이 가이드북의 **편집
판단**이고 이미 원고에 있다 — "최적 방문: 체류 30–60분", Walk 의 "소요 시간",
실행 시간표의 블록 길이. `price_range` 도 "예산 €15–30/인" 으로 이미 적혀 있다.

값이 두 곳(블록 토큰 · 산문)에 있으면 독자는 "미확인"과 "30–60분"을 나란히 본다 —
이 인프라가 막으려던 바로 그 상태다. 그래서 **수확한 뒤 산문 쪽을 지운다.**
블록이 정본이 되고 산문은 해석·맥락만 남긴다.

confidence 는 `editorial` — 공식 소스가 아니라 우리 편집 판단이라는 뜻이고,
source 에 원고 줄 번호를 남긴다. 조사 큐는 이것을 채워야 할 항목으로 세지 않는다.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FACTS = ROOT / "data/place-facts.json"
CH = ROOT / "source/CURRENT/20_Regional_Chapters"

# S3 이 헤딩 바로 아래 넣은 **블록인용**. 이것만 "이 섹션은 이 장소다" 의 표지다.
# 표 안에도 같은 토큰이 있으므로 `>` 로 시작하는 줄로 한정해야 한다 —
# 안 그러면 검증표 한 줄이 세 장소의 섹션 시작으로 잡힌다.
ANCHOR = re.compile(r"^>\s*(?:\*\*요금\*\*|📍)\s*\{\{fact:([a-z0-9][a-z0-9-]*)\.")
HEADING = re.compile(r"^#{2,4}\s")

# ── 산문에서 값을 뽑는 패턴. 우선순위 순서대로 시도한다. ──────────────────────
DURATION = [
    re.compile(r"체류\s*(약\s*)?(\d+\s*[–~-]\s*\d+\s*분|\d+\s*분|\d+\s*시간(?:\s*\d+분)?)"),
    re.compile(r"소요\s*시간\s*[:：]\s*(?:약\s*)?(\d+\s*시간(?:\s*\d+\s*분)?|\d+\s*[–~-]\s*\d+\s*분|\d+\s*분)"),
    re.compile(r"(?:^|\s)(\d+\s*[–~-]\s*\d+\s*분)만?\s*(?:고르|본다|걷|머무)"),
]
PRICE_RANGE = [
    re.compile(r"예산\s*(€\s?\d[\d.,]*\s*[–~-]\s*\d[\d.,]*\s*/\s*인)"),
    re.compile(r"예산\s*(€\s?\d[\d.,]*\s*[–~-]\s*\d[\d.,]*)"),
]
# 가는 법 — 수단 + 시간이 함께 있는 서술만 받는다. "근처다" 같은 말은 값이 아니다.
GETTING = re.compile(
    r"((?:숙소|역|정류장|중심가|구시가지|[A-ZÀ-Ü][\w'’\-]+)\S*\s*(?:에서|부터)?\s*"
    r"[^.\n|]{0,40}?(?:도보|트램|버스|메트로|지하철|푸니쿨라|택시|TER|기차)"
    r"[^.\n|]{0,30}?\d+\s*(?:분|km))")

# 3순위 — 실행 시간표 행의 시간 블록 길이. "| 09:30–10:20 | **Marché Forville** | …"
TIMETABLE = re.compile(r"^\|\s*\**\s*(\d{1,2}):(\d{2})\s*[–~-]\s*(\d{1,2}):(\d{2})\s*\**\s*\|([^|]*)\|")

# 이동·수속 행은 체류가 아니다. "| 16:10–16:25 | Peratallada 이동 |" 의 15분은
# 그 마을에 머무는 시간이 아니라 운전 시간이다.
TRANSIT = re.compile(r"이동|출발|도착|귀환|귀가|체크인|체크아웃|반납|인수|환승|이동중|"
                     r"→|이송|픽업|정리|휴식|샤워|취침|기상")

CLEAN = re.compile(r"\s+")


def timetable_durations(lines, names):
    """장소 이름이 2번째 칸에 있는 시간표 행에서 체류 길이를 뽑는다."""
    out = {}
    for i, l in enumerate(lines):
        m = TIMETABLE.match(l.strip())
        if not m:
            continue
        a = int(m.group(1)) * 60 + int(m.group(2))
        b = int(m.group(3)) * 60 + int(m.group(4))
        mins = b - a
        if not (15 <= mins <= 240):
            continue
        cell = m.group(5)
        if TRANSIT.search(cell):
            continue
        for pid, nm in names:
            if nm in cell and pid not in out:
                out[pid] = (f"{mins}분", i + 1)
    return out


def norm(s):
    return CLEAN.sub(" ", s).strip(" ·|-—")


def sections(text):
    """(placeId, 시작줄, 끝줄) — 블록 토큰이 가리키는 섹션 범위."""
    lines = text.splitlines()
    anchors = []
    for i, l in enumerate(lines):
        m = ANCHOR.search(l)
        if m:
            anchors.append((m.group(1), i))
    out = []
    for k, (pid, i) in enumerate(anchors):
        end = len(lines)
        for j in range(i + 1, len(lines)):
            if HEADING.match(lines[j]):
                end = j
                break
        out.append((pid, i, end))
    return out, lines


def first_match(pats, lines, lo, hi):
    for pat in pats:
        for j in range(lo, hi):
            m = pat.search(lines[j])
            if m:
                return norm(m.group(m.lastindex or 0)), j + 1
    return None, None


def main():
    apply = "--apply" in sys.argv
    doc = json.loads(FACTS.read_text(encoding="utf-8"))
    places = doc["places"]
    got = {"duration": 0, "price_range": 0, "getting_there": 0}
    dropped = []
    detail = []

    for f in sorted(CH.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        secs, lines = sections(text)
        names = [(pid, places[pid]["displayName"]) for pid, _, _ in secs
                 if pid in places and len(places[pid]["displayName"]) >= 4]
        tt = timetable_durations(lines, names)
        for pid, lo, hi in secs:
            p = places.get(pid)
            if not p:
                continue
            fx = p.setdefault("facts", {})
            for key, pats in (("duration", DURATION), ("price_range", PRICE_RANGE)):
                if (fx.get(key, {}).get("value") or "").strip():
                    continue
                val, ln = first_match(pats, lines, lo, hi)
                if not val and key == "duration" and pid in tt:
                    val, ln = tt[pid]          # 3순위 — 실행 시간표 블록 길이
                if not val:
                    continue
                fx[key] = {"value": val, "confidence": "editorial",
                           "source": f"원고 {f.name} L{ln}", "ttl_days": 3650,
                           "note": "시설이 공표하는 값이 아니라 이 가이드북의 편집 판단"}
                got[key] += 1
                detail.append((pid, key, val, f"{f.name}:{ln}"))

    if apply:
        doc["places"] = places
        FACTS.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"수확 — duration {got['duration']} · price_range {got['price_range']}"
          f" · getting_there {got['getting_there']}")
    print("--apply 없이 미리보기" if not apply else "적용 완료")
    for pid, key, val, where in detail[:60]:
        print(f"    {pid:34s} {key:14s} {val[:44]:46s} ← {where}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
