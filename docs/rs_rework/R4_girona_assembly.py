#!/usr/bin/env python3
"""R4-05 — main 05_Girona 원문 블록을 이동·재배치해 rs-region-v1 구조로 조립한다.

피로도: Day 2(9/2)=4/5, Day 3(9/3)=3/5 는 사용자 확정값(총괄 지시문 사전확정 2)이며
main 원고에 값이 없던 자리를 채우는 것이다. 창작이 아니라 확정 결정의 기입이다.
"""
import subprocess, pathlib

REPO = pathlib.Path("/mnt/c/Users/NB-24021500/source/worktrees/SP-FR-content-dev")
NAME = "05_Girona_Collioure_Emporda_v2.1.md"
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
# main 05 에는 YAML front matter 가 없다 (60-75행은 평문 메타 리스트).
# 값은 그 리스트에서 그대로 옮기고 형식만 다른 챕터와 맞춘다 — 사실값 창작 아님.
o += ["---",
      'title: "Jason과 Julia의 유럽 장기여행 가이드 — 지로나·콜리우르·엠포르다"',
      "chapter: 05",
      'version: "2.1"',
      "content_schema: rs-region-v1",
      'status: "일정 확정·숙소 예약 반영·1차 공식자료 검증 완료"',
      'travel_dates: "2026-09-01 – 2026-09-04"',
      'travelers: "Jason · Julia"',
      'last_web_verification: "2026-07-30"',
      'source_priority: "공식기관·시설·사업자 → 공식 관광기구 → 숙박업체 공식 사이트"',
      "---", ""]
o += L(1, 3) + [""]

o += ["# Commercial Guide Module", ""]
o += L(8, 9) + [""]

o += H("## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계")
o += L(13, 19) + [""]
o += L(576, 584) + [""]        # 이 일정이 Jason·Julia에게 맞는 이유

o += H("## 꼭 경험할 세 장면")
o += ["1. **Onyar 강변의 저녁** — 색색의 강변 파사드와 중세도시가 겹치는 대표경관"]
o += ["2. **Chemin du Fauvisme** — 야수파가 색을 찾아온 자리에서 원화와 실경을 겹쳐 본다"]
o += ["3. **Peratallada의 점심** — 석조마을의 생활감을 자리에 앉아 겪는 시간", ""]

o += H("## 생략해도 되는 것")
o += ["| 장소·경험 | 판단 | 이유 |", "|---|---|---|"]
o += L(1091, 1093) + [""]

o += H("## 한눈에 보기 — 우선순위·권역·소요시간")
o += L(1079, 1090) + [""]
o += L(23, 29) + [""]
o += L(33, 38) + [""]

o += H("## 중세도시의 저녁, 프랑스 카탈루냐 해안마을, 석조마을과 코스타브라바")
o += L(55, 58) + [""]

o += ["# Regional Context & Scheduled Place Dossiers", ""]

o += H("## 여행 전체에서의 역할")
o += L(88, 92) + [""]

o += H("## 추천 체류 리듬")
o += L(515, 528) + [""]        # Quick Reference
o += L(532, 537) + [""]        # 전체 일정표
o += L(541, 572) + [""]        # 동선 도식

o += H("## 구역별 이해와 숙소 생활권")
o += L(96, 126) + [""]         # 지역을 이해하는 다섯 개의 층
o += ["### 확정 숙소와 거점 운영", ""]
o += L(65, 73) + [""]
o += L(590, 623) + [""]        # 5.1~5.3

o += H("## 도착·출발·지역 내 교통")
o += L(1267, 1357) + [""]      # 15. 주차·운전·안전 전체

o += H("## 핵심 셀프가이드")
o += L(130, 132) + [""]
o += ["---", ""]
o += L(136, 266) + [""]        # Day 1 지로나 dossier 묶음
o += ["---", ""]
o += L(270, 364) + [""]        # 콜리우르·페랄라다
o += ["---", ""]
o += L(368, 488) + [""]        # 엠포르다·코스타브라바
o += ["---", ""]
o += L(490, 499) + [""]        # 유대사 박물관

o += H("## 음식·시장·카페·생활체험")
o += L(1141, 1232) + [""]      # 13. 음식·시장·카페
o += ["### 운동과 휴식", ""]
o += L(1100, 1137) + [""]

o += H("## 당일치기·우천·피로 대안")
o += L(1473, 1508) + [""]      # 16. 우천·교통지연 대체안
o += ["### 배제한 대안 루트", ""]
o += L(1405, 1469) + [""]

o += H("## 예약·비용·안전·주차·귀가")
o += ["### 경비 구조", ""]
o += L(1361, 1401) + [""]
o += ["### 예약 카드", ""]
o += L(1512, 1557) + [""]

o += H("## 공식 확인 정보와 재확인 대상")
o += ["### 2026년 체류기간 이벤트", ""]
o += L(1236, 1263) + [""]
o += ["### 출발 전 최종 확인", ""]
o += L(1561, 1577) + [""]
o += ["### 확정사항과 남은 미결정", ""]
o += L(1865, 1882) + [""]
o += ["### 공식·주요 참고자료", ""]
o += L(1811, 1861) + [""]

o += H("## 검증 상태 — 보강본 근거")
o += L(1886, 1903) + [""]

o += H("## 실행지도 · 현장 사용")
o += L(503, 509) + [""]

# ── Day 섹션 ────────────────────────────────────────────────────────────
DAYS = [
    dict(no=17, n=1, date="9월 1일 화요일", sub=626, fat="4/5",
         verdict="체크인 시각에 따라 지로나 구시가지를 넣을지 결정하는 날이다.",
         blocks=[(630, 640), (644, 698)]),
    dict(no=18, n=2, date="9월 2일 수요일", sub=701, fat="4/5",
         verdict="국경을 넘는 해안 당일치기이고 운전과 주차가 이 날의 변수다.",
         blocks=[(705, 719), (723, 847)]),
    dict(no=19, n=3, date="9월 3일 목요일", sub=850, fat="3/5",
         verdict="석조마을과 어촌을 잇되 한 곳씩만 깊게 보고 Bàscara로 돌아온다.",
         blocks=[(854, 870), (874, 1025)]),
    dict(no=20, n=4, date="9월 4일 금요일", sub=1028, fat="4–5/5",
         verdict="렌터카 반납과 국제선 환승이 겹치는 이동일이다.",
         blocks=[(1030, 1073)]),
]

for d in DAYS:
    o += [f"## {d['no']}. Day {d['n']} — {d['date']}"]
    o += L(d["sub"])
    o += [""]
    o += [f"*   **오늘의 결론**: {d['verdict']}", ""]
    o += [f"**오늘의 피로도: {d['fat']}.**", ""]
    for a, b in d["blocks"]:
        o += L(a, b) + [""]
    o += ["---", ""]

while o and o[-1] in ("", "---"):
    o.pop()
o += [""]

TARGET.write_text("\n".join(o) + "\n", encoding="utf-8")
print(f"행 {len(o)} · 글자 {len('\n'.join(o))} / 원문 {len(src)}행 {len('\n'.join(src))}자")
print(f"연결문 {len(CONNECTORS)}건")
for c in CONNECTORS:
    print("  -", c)
