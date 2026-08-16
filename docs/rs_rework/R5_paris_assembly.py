#!/usr/bin/env python3
"""Stage B — main 11_Paris 원문 블록을 이동·재배치해 rs-region-v1 구조로 조립한다.

취소 공연·폐기 패키지·이전 후보 기록은 DROPPED 에 전량 기록하고 제거한다.
VISUAL 사진 에셋 브리프(### {{VISUAL:...}} + 다음 '- 설명:' 줄)도 제거한다.
"""
import re
import subprocess, pathlib

REPO = pathlib.Path("/mnt/c/Users/NB-24021500/source/worktrees/SP-FR-content-dev")
NAME = "11_Paris_Long_Stay_v2.0.md"
TARGET = REPO / "source/CURRENT/20_Regional_Chapters" / NAME
src = subprocess.run(["git", "show", f"main:source/CURRENT/20_Regional_Chapters/{NAME}"],
                     cwd=REPO, capture_output=True, text=True, check=True).stdout.splitlines()

CONNECTORS = []
DROPPED = []          # 제거한 취소·폐기 기록 (보고서에 전량 싣는다)

CANCEL_RE = re.compile(r"취소 \(2026-08-10|~~|전 회차 취소")


def L(a, b=None, drop_cancelled=False, drop_visual=True):
    b = a if b is None else b
    out = []
    lines = src[a - 1:b]
    i = 0
    while i < len(lines):
        line = lines[i]
        if drop_visual and line.startswith("### {{VISUAL:"):
            i += 1
            while i < len(lines) and (lines[i].startswith("- 설명:") or not lines[i].strip()):
                i += 1
            continue
        if drop_cancelled and CANCEL_RE.search(line):
            DROPPED.append(f"main L{a + i}: {line.strip()[:150]}")
            i += 1
            continue
        out.append(line)
        i += 1
    return out


def C(text):
    CONNECTORS.append(text)
    return [text, ""]


def H(text):
    return [text, ""]


o = []
o += L(65, 68) + ["content_schema: rs-region-v1"] + L(69, 74) + [""]
o += L(1, 3) + [""]
o += L(63) + [""]          # 3개 사이클 편집도식

o += ["# Commercial Guide Module", ""]
o += L(8, 9) + [""]

o += H("## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계")
o += L(13, 19) + [""]
o += L(79, 88) + [""]

o += H("## 꼭 경험할 세 장면")
o += ["1. **Fête des Vendanges de Montmartre** — 파리가 자기 동네를 축하하는 주말"]
o += ["2. **Arc de Triomphe 경마** — 큰 이벤트 하나를 제대로 겪고 다음 날을 회복일로 둔다"]
o += ["3. **매일 가는 빵집과 시장** — 관광이 아니라 15박 거주자의 리듬", ""]

o += H("## 생략해도 되는 것")
o += L(1170, 1176) + [""]

o += H("## 한눈에 보기 — 우선순위·권역·소요시간")
o += L(1156, 1169) + [""]
o += L(34, 39) + [""]

o += H("## ‘한 달 살기’의 축소판 — 운동하는 아침, 문화가 있는 오후, 공연과 동네 저녁")
o += L(56, 59) + [""]

o += ["# Regional Context & Scheduled Place Dossiers", ""]

o += H("## 여행 전체에서의 역할")
o += L(117, 141) + [""]

o += H("## 추천 체류 리듬")
o += L(589, 624, drop_cancelled=True) + [""]
o += L(628, 644) + [""]
o += L(670, 691) + [""]
o += L(695, 715) + [""]

o += H("## 구역별 이해와 숙소 생활권")
o += L(100, 113) + [""]
o += ["### 파리를 생활도시로 읽는 법", ""]
o += L(1110, 1132) + [""]
o += ["### 숙소 생활권 비교", ""]
o += L(1136, 1152) + [""]
o += ["### 숙소 선정 전략", ""]
o += L(1721, 1769) + [""]

o += H("## 도착·출발·지역 내 교통")
o += L(1951, 2035) + [""]
o += ["### 귀국일 — 출국", ""]
o += L(242, 261) + [""]

o += H("## 핵심 셀프가이드")
o += L(265, 573) + [""]          # 장소별 상세 가이드
o += ["---", ""]
o += L(1180, 1451) + [""]        # 전시·미술관 2026 가을
o += ["---", ""]
o += L(1455, 1519) + [""]        # 미술관 실용 · 도서관·서점
o += ["---", ""]
o += L(1523, 1613, drop_cancelled=True) + [""]   # 공연과 스포츠
o += ["---", ""]
o += L(1617, 1715) + [""]        # 근교

o += H("## 음식·시장·카페·생활체험")
o += L(1811, 1899) + [""]
o += ["### 시장과 장보기", ""]
o += L(1773, 1807) + [""]
o += ["### 운동·러닝·수영", ""]
o += L(1903, 1947) + [""]

o += H("## 당일치기·우천·피로 대안")
o += L(2078, 2103) + [""]
o += ["### 대안 루트 — 계획이 깨졌을 때", ""]
o += L(2368, 2527, drop_cancelled=True) + [""]

o += H("## 예약·비용·안전·주차·귀가")
o += ["### 추천 고정 이벤트", ""]
o += L(167, 191, drop_cancelled=True) + [""]
o += ["### 예약 게이트", ""]
o += L(227, 238, drop_cancelled=True) + [""]
o += L(1094, 1104) + [""]
o += ["### 예약카드", ""]
o += L(2107, 2120) + [""]
o += ["### 치안과 일상 안전", ""]
o += L(2039, 2054) + [""]
o += ["### 경비", ""]
o += L(2124, 2196) + [""]

o += H("## 공식 확인 정보와 재확인 대상")
o += ["### 2026년 특별 이벤트와 변동요인", ""]
o += L(2058, 2074) + [""]
o += ["### 출발 전 확인목록", ""]
o += L(2200, 2236) + [""]
o += ["### 공식자료", ""]
o += L(2531, 2567) + [""]

o += H("## 검증 상태 — 보강본 근거")
o += L(2571, 2626) + [""]

o += H("## 실행지도 · 현장 사용")
o += L(577, 583) + [""]

# ── Day 섹션 17개 (main 717–1047) ───────────────────────────────────────
day_start = 717
day_end = 1047
block = L(day_start, day_end, drop_cancelled=True)
# 원문 '## N. Day n — 월 일 요일' 헤딩을 그대로 유지한다 (로컬 Day 표기 컨벤션 준수)
o += block
o += [""]

# 일정 교체 매트릭스·실행성 감사는 Day 뒤에 둔다
o += ["## 일정 교체 매트릭스", ""]
o += L(1051, 1059) + [""]
o += ["## 실행성 감사 — 15박 운영판", ""]
o += L(1063, 1090) + [""]

while o and o[-1] in ("", "---"):
    o.pop()
o += [""]

TARGET.write_text("\n".join(o) + "\n", encoding="utf-8")
print(f"행 {len(o)} · 글자 {len('\n'.join(o))} / 원문 {len(src)}행 {len('\n'.join(src))}자")
print(f"연결문 {len(CONNECTORS)}건")
for c in CONNECTORS:
    print("  -", c)
print(f"제거한 취소·폐기 기록 {len(DROPPED)}건")
for d in DROPPED:
    print("  ×", d)
