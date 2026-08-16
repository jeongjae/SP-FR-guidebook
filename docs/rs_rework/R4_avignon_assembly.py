#!/usr/bin/env python3
"""R4-09 — main 09_Avignon 원문 블록을 이동·재배치해 rs-region-v1 구조로 조립한다."""
import subprocess, pathlib

REPO = pathlib.Path("/mnt/c/Users/NB-24021500/source/worktrees/SP-FR-content-dev")
NAME = "09_Avignon_Alpilles_Pont_du_Gard_v2.0.md"
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
o += L(64, 67) + ["content_schema: rs-region-v1"] + L(68, 73) + [""]
o += L(1, 3) + [""]

o += ["# Commercial Guide Module", ""]
o += L(8, 9) + [""]

o += H("## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계")
o += L(13, 19) + [""]
o += L(78) + [""]
o += L(80) + [""]

o += H("## 꼭 경험할 세 장면")
o += ["1. **Palais des Papes** — 전시물이 아니라 크기와 동선을 보는 권력건축"]
o += ["2. **Pont du Gard** — 숫자보다 비례를 보는 로마 수로"]
o += ["3. **Arles** — 로마유적·중세회랑·반 고흐의 기억이 한 동선에 겹치는 하루", ""]

o += H("## 생략해도 되는 것")
o += ["| 장소·경험 | 판단 | 이유 |", "|---|---|---|"]
o += L(958, 960) + [""]

o += H("## 한눈에 보기 — 우선순위·권역·소요시간")
o += L(944, 957) + [""]
o += L(31, 38) + [""]

o += H("## 교황도시, 로마 수도교와 아를의 실제 도시생활")
o += L(53, 58) + [""]

o += ["# Regional Context & Scheduled Place Dossiers", ""]

o += H("## 여행 전체에서의 역할")
o += L(97, 103) + [""]

o += H("## 추천 체류 리듬")
o += L(615, 630) + [""]
o += L(633, 645) + [""]
o += L(671, 679) + [""]
o += L(1197, 1207) + [""]

o += H("## 구역별 이해와 숙소 생활권")
o += L(107, 135) + [""]
o += ["### 유럽 문화유산의 날 — 9월 19–20일", ""]
o += L(139, 162) + [""]
o += ["### 동네·숙소 생활권 비교", ""]
o += L(925, 940) + [""]
o += ["### 숙소 평가 기준과 후보", ""]
o += L(1086, 1148) + [""]

o += H("## 도착·출발·지역 내 교통")
o += L(1368, 1435) + [""]
o += ["### 주차·차량안전 실무", ""]
o += L(1439, 1465) + [""]

o += H("## 핵심 셀프가이드")
o += L(166, 168) + [""]
o += ["---", ""]
o += L(172, 191) + [""]        # Les Halles
o += ["---", ""]
o += L(193, 234) + [""]        # Palais des Papes
o += ["---", ""]
o += L(236, 274) + [""]        # Rocher des Doms · Pont Saint-Bénézet
o += ["---", ""]
o += L(280, 311) + [""]        # Uzès
o += ["---", ""]
o += L(313, 364) + [""]        # Pont du Gard
o += ["---", ""]
o += L(368, 467) + [""]        # Arles 일괄 (Arènes·Théâtre·Forum·Cloître·Fondation·Roquette)
o += ["---", ""]
o += L(471, 581) + [""]        # 선택 대안 — Alpilles (Les Baux·Carrières·Saint-Rémy·Mausole·Glanum)
o += ["---", ""]
o += L(585, 599) + [""]        # Avignon TGV 렌터카 반납

o += H("## 음식·시장·카페·생활체험")
o += L(1152, 1195) + [""]
o += ["### 레스토랑·카페", ""]
o += L(1214, 1247) + [""]
o += L(1250, 1273) + [""]
o += ["### 시장·슈퍼·제철", ""]
o += L(1277, 1303) + [""]
o += ["### 운동·수영", ""]
o += L(1307, 1333) + [""]

o += H("## 당일치기·우천·피로 대안")
o += L(1469, 1497) + [""]
o += ["### 배제한 대안 루트", ""]
o += L(1662, 1673) + [""]
o += L(1682, 1736) + [""]

o += H("## 예약·비용·안전·주차·귀가")
o += ["### 피로도·삭제 우선순위", ""]
o += L(887, 895) + [""]
o += ["### 경비 구조", ""]
o += L(1501, 1548) + [""]
o += ["### 예약카드", ""]
o += L(1554, 1565) + [""]

o += H("## 공식 확인 정보와 재확인 대상")
o += ["### 2026 행사·특별운영", ""]
o += L(1337, 1362) + [""]
o += ["### 출발 전 확인목록", ""]
o += L(1569, 1658) + [""]
o += ["### 공식자료", ""]
o += L(1740, 1777) + [""]

o += H("## 검증 상태 — 보강본 근거")
o += L(1805, 1834) + [""]

o += H("## 실행지도 · 현장 사용")
o += L(603, 609) + [""]

DAYS = [
    dict(no=17, n=1, date="9월 16일 수요일", sub=682, fat="3/5",
         verdict="이동일이므로 체크인과 Avignon 첫 산책이면 충분하다.",
         tt=(689, 702), acts=(708, 710), cut=(714, 716), alt=None),
    dict(no=18, n=2, date="9월 17일 목요일", sub=721, fat="3/5",
         verdict="예상 보행 7–9km, 실내 관람 2시간.",
         tt=(731, 744), acts=(765, 770), cut=None, alt=(750, 761)),
    dict(no=19, n=3, date="9월 18일 금요일", sub=773, fat="4/5",
         verdict="시장 혼잡+운전+노출된 유적지 보행이 겹친다.",
         tt=(783, 797), acts=(807, 810), cut=None, alt=(814, 827)),
    dict(no=20, n=4, date="9월 19일 토요일", sub=830, fat="4/5",
         verdict="문화유산의 날 혼잡과 고대유적 계단이 변수다.",
         tt=(836, 848), acts=None, cut=None, alt=(854, 856)),
    dict(no=21, n=5, date="9월 20일 일요일", sub=859, fat="4/5",
         verdict="차량반납과 대형짐 이동이 핵심 변수다.",
         tt=(864, 872), acts=None, cut=None, alt=(878, 883)),
]

for d in DAYS:
    o += [f"## {d['no']}. Day {d['n']} — {d['date']}"]
    o += L(d["sub"])
    o += [""]
    o += [f"*   **오늘의 결론**: {d['verdict']}", ""]
    o += [f"**오늘의 피로도: {d['fat']}.**", ""]
    o += ["#### 실행 시간표", ""]
    o += L(*d["tt"]) + [""]
    if d["acts"]:
        o += ["#### 오늘 꼭 해볼 것", ""]
        o += L(*d["acts"]) + [""]
    if d["cut"]:
        o += ["#### 삭제 및 단축 순서 (늦었거나 피곤할 때)", ""]
        o += L(*d["cut"]) + [""]
    if d["alt"]:
        o += ["#### 대안·실용 메모", ""]
        o += L(*d["alt"]) + [""]
    o += ["---", ""]

while o and o[-1] in ("", "---"):
    o.pop()
o += [""]

TARGET.write_text("\n".join(o) + "\n", encoding="utf-8")
print(f"행 {len(o)} · 글자 {len('\n'.join(o))} / 원문 {len(src)}행 {len('\n'.join(src))}자")
print(f"연결문 {len(CONNECTORS)}건")
for c in CONNECTORS:
    print("  -", c)
