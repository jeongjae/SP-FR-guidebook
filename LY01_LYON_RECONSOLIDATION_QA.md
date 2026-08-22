# LY01 — Lyon / Annecy Region Editorial Re-Consolidation QA Report

---

## 1. Executive Summary

- **작업 목적**: Lyon 지역 챕터(`10_Lyon_v2.0.md`) 및 생성 페이지(`source/CURRENT/20_Regions/lyon.md`)를 내부 기획·검토 원고 형태에서 정제된 최종 상용 여행가이드북 IA(`rc-region-v1`)로 재편집·통폐합.
- **작업 브랜치**: `fix/lyon-region-editorial-consolidation`
- **핵심 성과**:
  - **Factual Gate / 렌터카 반납일 인계 정합**: Avignon 렌터카 반납(Day 20 저녁) 이후 무차량 상태에서 Day 23(9/20 일) TGV 이동 ➔ Lyon Part-Dieu 도착(렌터카 절차 없음)으로 SOT 100% 일치.
  - **숙소 상태 정규화**: 확정 숙소(`Lagrange Aparthotel Lyon Lumière`, Monplaisir 생활권)의 메트로 D 접근성 및 장기체류 운영 의미 중심으로 서술. 과거 1순위/1.5순위 권역 비교표, 가중치 채점표는 아카이브로 분리.
  - **Overview 통합**: 내부 평가표(`★★★★★`), `여행의 역할`, `여행자 기준`, `꼭 경험할 세 장면`을 제거하고 `Lyon을 이렇게 본다`로 통합.
  - **Schedule 단일화**: ASCII 다이어그램, 5열 일정표, Day별 식사표를 제거하고 Day SOT 기반의 간결한 2열 일정표 1개로 단일화.
  - **Places 큐레이션 정돈**: 실제 방문 장소(Fourvière, Vieux Lyon, Croix-Rousse, Halles Paul Bocuse, Parc de la Tête d'Or, Annecy, Bellecour) 및 식당(Café Comptoir Abel, Daniel et Denise, Chez Mamie Lise) 총 10개 카드로 정돈.
  - **Transport & Food 압축**: TCL 상세 요금표와 매뉴얼을 분리하고 4개 핵심 소주제(도심은 메트로/도보, Part-Dieu역 이동, Annecy는 TER, Paris 출발)로 압축. 6종 대표 식재료 1문장 축소, 보졸레/론 와인 분리, 시장 2곳 안내.
  - **기획 잔재 아카이브**: `source/ARCHIVE/20_Regional_Chapters/10_Lyon_Planning_Residue_v1.0.md` 생성 및 분리.
  - **자동화 QA**: 30개 단위/통합 테스트 PASS, 원고 흔적 가드 PASS (lyon 흔적 토큰 **0건**).

---

## 2. Factual Gate — Avignon → Lyon 인계 정합

- **대조 결과**:
  - `data/decisions.json` (DEC-A02, DEC-A08): 9/17 저녁 Avignon TGV 렌터카 반납 확정.
  - `data/daily-cards/day-23.json` (9/20 일): TGV INOUI 12176 탑승하여 Lyon Part-Dieu 도착 (렌터카 반납 절차 없음).
  - `data/region-essentials.json`: departureStrategy에 차량 반납 없는 아침 TGV 이동 정합.
- **Region 반영**: Day 23 아침 이동에 차량 반납 절차가 없음을 Region Overview, Schedule, Transport, Stay 전체에 걸쳐 일관되게 서술.

---

## 3. Lodging Status Gate

- **숙소 상태**: `Lagrange Aparthotel Lyon Lumière` (확정 / Monplaisir 3구).
- **Region 처리**:
  - 숙소가 Monplaisir 생활권에 위치하고 메트로 D선(Sans Souci 및 Monplaisir-Lumière 역)을 통해 Bellecour와 Vieux Lyon에 직통 연결됨을 서술.
  - 7개 권역 비교표(Ainay 1순위, Bellecour 1.5순위, Brotteaux 2순위 등)는 `10_Lyon_Planning_Residue_v1.0.md`로 이동.

---

## 4. Canonical / Generated / Render Heading IA Alignment

| 계층 | Region Consolidation Key | 10 Chapter Header | Generated lyon.md | Final Rendered (Web) |
|---|---|---|---|---|
| **Overview** | `verdict` | `## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계` | `## Lyon을 이렇게 본다` | Lyon을 이렇게 본다 |
| **Schedule** | `overview` | `## 한눈에 보기 — 일정` | `## 일정` | 일정 |
| **Stay & Life** | `neighborhoods` | `## 구역별 이해와 숙소 생활권` | `## 숙소와 생활권` | 숙소와 생활권 |
| **Transport** | `transport_deep` | `## 도착·출발·지역 내 교통` | `## Lyon에서 이동하기` | Lyon에서 이동하기 |
| **Food** | `food_culture` | `## 음식·시장·카페·생활체험` | `## 먹고 장보기` | 먹고 장보기 |

---

## 5. Overview Unified Content

```markdown
## Lyon을 이렇게 본다

Lyon에서는 두 강과 두 언덕이 만든 도시 지형을 따라 걷는다. Fourvière에서는 도시 전체를 내려다보고, Vieux Lyon에서는 르네상스 골목과 traboule을 지나며, Croix-Rousse에서는 비단 산업과 생활시장의 흔적을 본다.

도심 일정은 메트로와 도보로 연결하고, Halles de Lyon Paul Bocuse에서는 리옹의 음식문화를 재료와 시장의 관점에서 경험한다. 하루는 Annecy로 이동해 알프스 호수도시의 구시가지와 호숫가를 걷는다.

### 이번 4박의 핵심

- **Fourvière와 Vieux Lyon** — 언덕에서 내려와 구시가지까지 걸으며 도시의 지형을 이해한다.
- **Croix-Rousse와 미식** — 비단 노동자의 동네와 시장, Halles를 한 흐름으로 본다.
- **Annecy** — Lyon과 다른 알프스 호수도시의 풍경과 생활권을 하루 동안 경험한다.

도시 안에서는 관광지를 많이 추가하기보다 서로 다른 동네의 성격을 연결해서 보는 데 시간을 쓴다.
```

---

## 6. Single Schedule Table (Day SOT)

```markdown
## 일정

| 날짜 | 핵심 일정 |
|---|---|
| 9/20 일 | Avignon 체크아웃 · TGV 이동 · Lyon Part-Dieu 도착 · 숙소 체크인 |
| 9/21 월 | Fourvière · Vieux Lyon 트라불 · 손강변 산책 |
| 9/22 화 | Croix-Rousse 시장 & 비단동네 · Halles Paul Bocuse · Parc de la Tête d'Or |
| 9/23 수 | Annecy 당일치기 (TER 이동) · 구시가지 & 안시 호수 |
| 9/24 목 | 숙소 체크아웃 · Part-Dieu역 이동 · Paris행 TGV 탑승 |

상세 시각, 메트로/철도 이동, 식사와 선택 일정은 각 날짜의 Day 페이지에서 확인한다.
```

---

## 7. Places Classification (LY01F 최종 정돈)

| 장소명 | 슬러그 | 등급 | 여행 내 역할 | 최종 Region Card |
|---|---|---|---|:---:|
| **Fourvière** | `fourviere` | 필수 | Day 24 실제 방문지 (기도하는 언덕·바실리카·전망) | **유지** |
| **Vieux Lyon · 트라불** | `vieux-lyon` | 필수 | Day 24 실제 방문지 (르네상스 구시가지·트라불 통로) | **유지** |
| **Croix-Rousse** | `croix-rousse` | 필수 | Day 25 실제 방문지 (일하는 언덕·비단동네·시장) | **유지** |
| **Halles de Lyon Paul Bocuse** | `halles-de-lyon-paul-bocuse` | 필수 | Day 25 실제 방문지 (실내 미식 시장·생마르슬랭) | **유지** |
| **Parc de la Tête d'Or** | `parc-de-la-tete-d-or` | 우선추천 | Day 25 실제 방문지 (도심 생태 공원·온실·장미원) | **유지** |
| **Annecy 구시가지 · 호수** | `annecy` | 필수 | Day 26 실제 방문지 (안시 당일치기·팔레드릴·호수) | **유지** |
| **Bellecour** | `bellecour` | 우선추천 | Day 23 실제 방문지 (붉은 자갈 광장·루이14세기마상) | **유지 (우선추천)** |
| **Café Comptoir Abel** | `cafe-comptoir-abel` | 필수 | Day 23 저녁 식당 (에네 지구 최고 부숑) | **유지 (식당)** |
| **Daniel et Denise** | `daniel-et-denise` | 필수 | Day 24 저녁 식당 (MOF 셰프 정통 부숑) | **유지 (식당)** |
| **Chez Mamie Lise** | `chez-mamie-lise` | 필수 | Day 26 점심 식당 (안시 사부아 전통 산장 식당) | **유지 (식당)** |

---

## 8. Food Cleanup (LY01F 반영)

- **Day 귀속 정합**:
  - `Café Comptoir Abel`: Day 23 (9/20 저녁)
  - `Daniel et Denise`: Day 24 (9/21 저녁)
  - `Halles Paul Bocuse`: Day 25 (9/22 점심 및 시장 체험)
  - `Chez Mamie Lise`: Day 26 (9/23 점심)
- **Lyon과 사부아에서 맛볼 식재료와 전통 요리**: Quenelle de brochet, Saucisson de Lyon, Salade lyonnaise, Cervelle de canut, Gratin dauphinois, Tarte aux pralines 등 6종 1문장 기술.
- **와인**: 보졸레와 론 와인을 독립 문장으로 분리(`리옹은 북쪽의 보졸레(Beaujolais)와 남쪽의 론(Rhône) 와인이 만나는 미식도시다. 저녁 식사나 숙소 휴식 시 로컬 와인을 곁들인다.`).
- **시장 정보**: Halles de Lyon Paul Bocuse 및 Marché de la Croix-Rousse 2곳 링크 수록.
- **방문 업소**: Café Comptoir Abel, Daniel et Denise, Chez Mamie Lise 3곳 및 식사 원칙 문단 수록.

---

## 9. Stay & Local Life Cleanup (LY01F 반영)

- **숙소와 생활권**: 3구 Monplaisir 생활권(Lagrange Aparthotel Lyon Lumière), 메트로 D선 도보 접근성, 간이주방 활용 수칙 서술.
- **아침 운동 현실화**: 장거리 강변/공원 러닝 문구를 축소하고 `아침에는 Monplaisir 숙소 주변에서 가볍게 걷거나 뛰고, 도심 일정이 긴 날에는 별도 운동을 줄인다.`로 생활권 중심 간결화.

---

## 10. Transport Cleanup

- **Lyon에서 이동하기**:
  - `### 도심에서는 메트로와 도보`: 메트로(TCL) 및 F2 푸니쿨라 활용 원칙
  - `### Part-Dieu역과 숙소 이동`: 도착/출발일 큰 짐 택시 이동
  - `### Annecy는 직행 TER`: 차 없이 직행 열차 왕복 및 복귀 시각 관리
  - `### Paris로 출발하는 날`: TGV INOUI 탑승 (Part-Dieu 승차역 확인)

---

## 11. Lodging & Planning Residue Archive

- 모든 숙소 권역 비교표, 과거 후보 분석, 박물관/근교 제외 후보 분석, 문전 이동 실행표 등은 [`source/ARCHIVE/20_Regional_Chapters/10_Lyon_Planning_Residue_v1.0.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/source/ARCHIVE/20_Regional_Chapters/10_Lyon_Planning_Residue_v1.0.md)에 안전하게 분리 보존 완료.

---

## 12. Manuscript Residue Before / After

| 검사 항목 | Before | After | 변화 |
|---|---:|---:|---:|
| `manuscript_residue_check.py` lyon 흔적 토큰 | 28건 | **0건** | -28 (완전 박멸) |
| 원고 번호 및 내부 기획 헤딩 | 12건 | **0건** | -12 |
| 평가 별점 및 점수 표기 | 6건 | **0건** | -6 |

---

## 13. Quantitative Before / After

| 지표 | Before (main) | After (LY01 Consolidation) | 변화 |
|---|---:|---:|---:|
| **원고 줄 수 (Chapter lines)** | 943 | **392** | -551 (-58.4%) |
| **보이는 글자 수 (Visible chars, 공백 포함)** | ~18,500 | **8,505** | -9,995 (-54.0%) |
| **순수 글자 수 (Visible chars, 공백 제외)** | ~14,200 | **6,634** | -7,566 (-53.3%) |
| **표 개수 (Tables)** | 16 | **3** | -13 (-81.3%) |
| **장소 카드 수 (Attraction & Food)** | 10 | **10** | 정합성 유지 |
| **일정 표현 수 (Schedule representations)** | 4 | **1** | -3 (단일 정본) |
| **원고 흔적 토큰 (Residue tokens)** | 28 | **0** | -28 (완전 박멸) |
| **모바일 390px 스크롤 높이 (추정)** | ~50 screens | **~19 screens** | -62% 압축 |

---

## 14. Automated QA Results

| 검사 항목 | 명령어 | 결과 | 비고 |
|---|---|---|---|
| 사이트 전체 빌드 | `python3 build/site.py` | **PASS** | 372쪽 생성, 색인 191건 |
| 단위 및 통합 테스트 | `pytest tests/` | **PASS** | 30 passed |
| 원고 흔적 가드 | `python3 build/manuscript_residue_check.py` | **PASS** | aix 0, avignon 0, barcelona 0, girona 0, luberon 0, lyon 0 |
| 지역 구조 검사 | `python3 build/region_structure_check.py` | **PASS** | 분류·섹션·방문일·링크 0 오류 |
| 사진 연결 검사 | `python3 build/media_lookup_check.py` | **PASS** | 미매핑 0, 누락 0 |
| 표 손실 검사 | `python3 build/table_loss_check.py` | **PASS** | 조용한 열 손실 0 |
| UX & 디자인 토큰 검사 | `python3 build/ux_check.py` | **PASS** | 명암비, 하단탭, URL 0 결함 |
| PWA 오프라인 검사 | `python3 build/pwa_check.py` | **PASS** | 871개 파일 전체 캐시 |
| 다중 뷰포트 검사 | `python3 build/viewport_check.py` | **PASS** | 6개 해상도 가로 오버플로 0 |
| 사실 토큰 가드 | `build/fact_guard.py` (via site.py) | **PASS** | 45개 확정 토큰 생존 확인 |
| 조사 종결 검사 | `python3 build/research_closure_check.py` | **PASS** | 0 unclassified |
