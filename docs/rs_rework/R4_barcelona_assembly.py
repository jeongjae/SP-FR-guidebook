#!/usr/bin/env python3
"""R4-04 — main 04_Barcelona 원문 블록을 이동·재배치해 rs-region-v1 구조로 조립한다."""
import subprocess, pathlib

REPO = pathlib.Path("/mnt/c/Users/NB-24021500/source/worktrees/SP-FR-content-dev")
NAME = "04_Barcelona_Sitges_v2.0.md"
TARGET = REPO / "source/CURRENT/20_Regional_Chapters" / NAME
src = subprocess.run(["git", "show", f"main:source/CURRENT/20_Regional_Chapters/{NAME}"],
                     cwd=REPO, capture_output=True, text=True, check=True).stdout.splitlines()

CONNECTORS = []


def L(a, b=None):
    b = a if b is None else b
    return src[a - 1:b]


def C(text):
    CONNECTORS.append(text)
    return [text, ""]


def H(text):
    return [text, ""]


o = []
o += L(1, 4) + ["content_schema: rs-region-v1"] + L(5, 10) + [""]
o += L(12, 15) + [""]          # 대표사진·크레딧

o += ["# Commercial Guide Module", ""]
o += L(19, 20) + [""]

o += H("## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계")
o += L(24, 30) + [""]
o += L(74, 79) + [""]          # 여행의 역할·여행자 기준

o += H("## 꼭 경험할 세 장면")
o += ["1. **Sagrada Família 내부의 빛** — 외관 조각을 해독하기보다 색유리가 바닥에 만드는 색면을 본다"]
o += ["2. **Sant Pau의 병원 도시** — 모더니즘이 장식이 아니라 도시개혁이었음을 보는 자리"]
o += ["3. **Mercat de la Concepció의 아침** — 관광명소 이전에 생활 인프라인 시장", ""]

o += H("## 생략해도 되는 것")
o += L(575, 581) + [""]

o += H("## 한눈에 보기 — 우선순위·권역·소요시간")
o += L(34, 39) + [""]
o += L(43, 48) + [""]
o += L(783, 794) + [""]        # 미술관·박물관 선택표

o += H("## 지중해 계획도시와 모더니즘, 시장과 책의 도시")
o += L(65, 69) + [""]          # 현장 메모

o += ["# Regional Context & Scheduled Place Dossiers", ""]

o += H("## 여행 전체에서의 역할")
o += L(108, 110) + [""]

o += H("## 추천 체류 리듬")
o += L(361, 372) + [""]
o += L(376, 386) + [""]
o += L(979, 988) + [""]        # 식사 시간대

o += H("## 구역별 이해와 숙소 생활권")
o += L(89, 104) + [""]         # 지역을 이해하는 다섯 개의 층
o += ["### 동네별 성격과 숙소 적합성", ""]
o += L(587, 639) + [""]        # 7.1~7.6
o += ["### 숙소 예산과 확정 숙소", ""]
o += L(849, 874) + [""]        # 11.1 예산 산식 · 11.2 공통 필수 확인
o += L(894, 941) + [""]        # 12.1~12.7 후보와 선택 알고리즘

o += H("## 도착·출발·지역 내 교통")
o += L(1243, 1277) + [""]      # 이 구간의 성격 · 지하철 · Sants · 시체스 · ZBE
o += ["### 공항·시내교통 실용정보", ""]
o += L(1281, 1302) + [""]
o += ["### 렌터카 인수 실행 가이드", ""]
o += L(1306, 1339) + [""]
o += ["### 시체스 주차와 이동", ""]
o += L(1343, 1360) + [""]

o += H("## 핵심 셀프가이드")
o += L(114, 116) + [""]
o += ["---", ""]
o += L(120, 192) + [""]        # Sagrada Família · Sant Pau
o += ["---", ""]
o += L(196, 262) + [""]        # 고딕 지구 · 시장 · 도서관 · MACBA
o += ["---", ""]
o += L(266, 340) + [""]        # 시체스 (Cau Ferrat · Maricel · 해변)
o += ["---", ""]
o += L(806, 841) + [""]        # 시체스 지역 이해와 핵심 동선
o += ["---", ""]
o += L(742, 780) + [""]        # 8.6~8.9 선택 미술관 (Picasso·MNAC·Miró·DHUB)

o += H("## 음식·시장·카페·생활체험")
o += L(947, 977) + [""]        # 카탈루냐 요리의 문법 · xató · 식사 전략
o += ["### 레스토랑·카페", ""]
o += L(994, 1098) + [""]       # 13.1~13.6 · 14 카페
o += ["### 시장·슈퍼·제철", ""]
o += L(1102, 1152) + [""]
o += ["### 운동·수영", ""]
o += L(1158, 1218) + [""]

o += H("## 당일치기·우천·피로 대안")
o += L(1364, 1405) + [""]      # 22.1~22.6

o += H("## 예약·비용·안전·주차·귀가")
o += ["### 피로도와 하루 활동량", ""]
o += L(517, 526) + [""]
o += ["### 예약 우선순위 실행표", ""]
o += L(530, 541) + [""]
o += ["### 예약카드", ""]
o += L(1409, 1470) + [""]      # A~E
o += ["### 경비 구조", ""]
o += L(1532, 1601) + [""]
o += ["### 현지 안전", ""]
o += L(1520, 1528) + [""]

o += H("## 공식 확인 정보와 재확인 대상")
o += ["### 2026 행사·특별전", ""]
o += L(1222, 1239) + [""]
o += ["### 8월 31일 중요 정정", ""]
o += L(344, 345) + [""]
o += ["### 출발 전 확인목록", ""]
o += L(1474, 1516) + [""]

o += H("## 검증 상태 — 보강본 근거")
o += L(1900, 1912) + [""]

o += H("## 실행지도 · 현장 사용")
o += L(349, 355) + [""]

DAYS = [
    dict(no=17, n=1, date="8월 29일 토요일", sub=391, fat="3/5",
         verdict="야간 도착일이다. 장보기·생활권 파악은 Day 2 아침으로 넘긴다. 항공이 지연되어도 체크인 창(00:00) 안이면 문제없다.",
         lead=(393, 393), tt=(395, 401), extra=None),
    dict(no=18, n=2, date="8월 30일 일요일", sub=408, fat="3/5",
         verdict="유료 핵심 관광지는 2곳뿐이지만 사그라다의 밀도와 더위 때문에 오후 휴식이 필요하다.",
         lead=None, tt=(410, 420), extra=None),
    dict(no=19, n=3, date="8월 31일 월요일", sub=429, fat="3/5",
         verdict="이동은 많아 보이지만 각 구간이 짧다. MACBA에서 2시간을 넘기지 않고, 책방 뒤에는 반드시 숙소로 돌아온다.",
         lead=None, tt=(431, 445), extra=None),
    dict(no=20, n=4, date="9월 1일 화요일", sub=452, fat="4/5",
         verdict="운전 3시간 안팎과 체크인 2회가 겹친다. 시체스에서 활동을 추가하지 않는다.",
         lead=None, tt=(454, 471), extra=(475, 513)),
]

for d in DAYS:
    o += [f"## {d['no']}. Day {d['n']} — {d['date']}"]
    o += L(d["sub"])
    o += [""]
    o += [f"*   **오늘의 결론**: {d['verdict']}", ""]
    o += [f"**오늘의 피로도: {d['fat']}.**", ""]
    if d["lead"]:
        o += L(*d["lead"]) + [""]
    o += ["#### 실행 시간표", ""]
    o += L(*d["tt"]) + [""]
    if d["extra"]:
        o += L(*d["extra"]) + [""]
    o += ["---", ""]

while o and o[-1] in ("", "---"):
    o.pop()
o += [""]

TARGET.write_text("\n".join(o) + "\n", encoding="utf-8")
print(f"행 {len(o)} · 글자 {len('\n'.join(o))} / 원문 {len(src)}행 {len('\n'.join(src))}자")
print(f"연결문 {len(CONNECTORS)}건")
for c in CONNECTORS:
    print("  -", c)
