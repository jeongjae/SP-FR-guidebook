# AV01 — Avignon / Pont du Gard / Arles Region Editorial Re-Consolidation QA Report

---

## 1. Executive Summary

- **작업 목적**: Avignon 지역 챕터(`09_Avignon_Alpilles_Pont_du_Gard_v2.0.md`) 및 생성 페이지(`source/CURRENT/20_Regions/avignon.md`)를 내부 기획·검토 원고 형태에서 정제된 최종 상용 여행가이드북 IA(`rc-region-v1`)로 재편집·통폐합.
- **작업 브랜치**: `fix/avignon-region-editorial-consolidation`
- **핵심 성과**:
  - **Factual Gate / 렌터카 반납일 정규화**: Day 20(9/17 목) 저녁 Avignon TGV역 Hertz 렌터카 최종 반납, Day 21(금) Arles TER 당일치기, Day 22(토) 시내 도보, Day 23(일) TGV 이동(차량 절차 없음)으로 SOT 100% 정합 완료.
  - **숙소 상태 정규화**: 성벽 안(intra-muros) 도보 생활권 거점 수칙 및 `candidate` 상태 일관 유지. 숙소 권역 비교표, 가중치 채점표, 과거 예산안을 아카이브로 분리.
  - **Overview 통합**: 내부 평가표(`★★★★★`), `여행의 역할`, `여행자 기준`, `꼭 경험할 세 장면`을 제거하고 `Avignon과 서부 Provence를 이렇게 본다`로 통합.
  - **Schedule 단일화**: ASCII 다이어그램, 5열 일정표, Day별 식사표를 제거하고 Day SOT 기반의 간결한 2열 일정표 1개로 단일화.
  - **Places 큐레이션 정돈**: 실제 방문 장소(Avignon 시내, Uzès, Pont du Gard, Nîmes, Arles) 및 선택/대체 옵션(Alpilles 등) 정규화.
  - **Transport & Food 압축**: ZOU!/일반 도로 매뉴얼 분리, 4개 핵심 소주제(시내는 도보, Uzès/Pont은 렌터카, Arles는 TER, Lyon 이동)로 압축. 6종 대표 식재료 1문장 축소, 론 남부 와인 분리, 시장 2곳 안내.
  - **기획 잔재 아카이브**: `source/ARCHIVE/20_Regional_Chapters/09_Avignon_Planning_Residue_v1.0.md` 생성 및 분리.
  - **자동화 QA**: 30개 단위/통합 테스트 PASS, 원고 흔적 가드 PASS (avignon 흔적 토큰 **0건**).

---

## 2. Factual Gate — 렌터카 반납일 및 이동 정합

- **대조 결과**:
  - `data/decisions.json` (DEC-A02): 일요일(9/20) 09:00 반납 금지 결정 반영 상태.
  - `data/daily-cards/day-20.json` (9/17 목): Uzès · Pont du Gard · Nîmes 후 16:30~18:30 Avignon TGV Hertz 반납.
  - `data/daily-cards/day-21.json` (9/18 금): Arles TER 철도 당일치기 (차량 반납 완료 상태).
  - `data/daily-cards/day-22.json` (9/19 토): Avignon 시내 도보일.
  - `data/daily-cards/day-23.json` (9/20 일): TGV INOUI 12176 탑승하여 Lyon 이동 (렌터카 절차 없음).
  - `data/region-essentials.json`: departureStrategy에 차량 반납 없는 아침 TGV 이동 정합.
- **Region 반영**: Day 20 저녁 Hertz Avignon TGV 반납 완료 및 Day 23 아침 차량 절차 없음을 Region Overview, Schedule, Transport, Stay 전체에 걸쳐 일관되게 서술.

---

## 3. Lodging Status Gate

- **숙소 상태**: `La Terrasse du Clocher (후보)` / `candidate` 상태.
- **Region 처리**:
  - 특정 숙소를 고정 확정으로 기술하지 않고, "성벽 안(intra-muros) 도보 생활권" 원칙으로 서술.
  - 6개 권역 비교표, 7개 후보 채점표, 10개 평가 기준 가중치표 등은 `09_Avignon_Planning_Residue_v1.0.md`로 이동.

---

## 4. Canonical / Generated / Render Heading IA Alignment

| 계층 | Region Consolidation Key | 09 Chapter Header | Generated avignon.md | Final Rendered (Web) |
|---|---|---|---|---|
| **Overview** | `verdict` | `## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계` | `## Avignon과 서부 Provence를 이렇게 본다` | Avignon과 서부 Provence를 이렇게 본다 |
| **Schedule** | `overview` | `## 한눈에 보기 — 일정` | `## 일정` | 일정 |
| **Stay & Life** | `neighborhoods` | `## 구역별 이해와 숙소 생활권` | `## 숙소와 생활권` | 숙소와 생활권 |
| **Transport** | `transport_deep` | `## 도착·출발·지역 내 교통` | `## Avignon에서 이동하기` | Avignon에서 이동하기 |
| **Food** | `food_culture` | `## 음식·시장·카페·생활체험` | `## 먹고 장보기` | 먹고 장보기 |

---

## 5. Overview Unified Content

```markdown
## Avignon과 서부 Provence를 이렇게 본다

Avignon에서는 교황청이 남긴 중세 도시 구조를 보고, 근교에서는 로마 수로와 도시 유산, Arles에서는 로마와 중세의 흔적이 지금의 생활도시 안에 어떻게 남아 있는지 연결해서 본다.

시내에서는 차 없이 성벽 안을 걷고, 하루는 Uzès와 Pont du Gard를 중심으로 근교를 이동하며, 하루는 TER로 Arles를 다녀온다. Avignon 자체는 Les Halles, Palais des Papes, Rocher des Doms와 Pont Saint-Bénézet를 한날에 연결한다.

### 이번 체류의 핵심

- **교황도시 Avignon** — 성벽과 교황궁을 통해 중세 교황권이 만든 도시의 규모를 본다.
- **Uzès와 Pont du Gard** — 작은 지역도시와 로마 수도교를 한 흐름으로 연결한다.
- **Arles** — 로마유적, 생트로핌과 구시가지가 현재 생활도시 안에 함께 남아 있는 모습을 걷는다.

근교일은 이동 자체가 길기 때문에 방문지를 추가하기보다 각 날의 핵심 동선을 유지한다.
```

---

## 6. Single Schedule Table (Day SOT)

```markdown
## 일정

| 날짜 | 핵심 일정 |
|---|---|
| 9/16 수 | Luberon 체크아웃 · Avignon 체크인 · 성벽 안 가벼운 산책 |
| 9/17 목 | Uzès · Pont du Gard · Nîmes · 렌터카 반납 |
| 9/18 금 | Arles 당일치기 (TER 이동) |
| 9/19 토 | Les Halles · Palais des Papes · Rocher des Doms · Pont Saint-Bénézet |
| 9/20 일 | Avignon 체크아웃 · TGV 이동 · Lyon 정착 |

상세 시각, 이동, 식사와 선택 일정은 각 날짜의 Day 페이지에서 확인한다.
```

---

## 7. Places Classification

| 장소명 | 슬러그 | 등급 | 여행 내 역할 |
|---|---|---|---|
| **Les Halles d'Avignon** | `les-halles` | 필수 | Day 22 실제 장보기 및 식재료 기준점 |
| **Palais des Papes** | `palais-des-papes` | 필수 | Day 22 실제 방문지 (히스토패드 증강현실) |
| **Pont Saint-Bénézet** | `pont-saint-benezet` | 필수 | Day 22 실제 방문지 (아비뇽 다리 교각) |
| **Rocher des Doms** | `rocher-des-doms` | 필수 | Day 22 실제 방문지 (바위산 파노라마 전망대) |
| **Uzès Place aux Herbes** | `uzes` | 필수 | Day 20 실제 방문지 (공작성 및 에르브 광장) |
| **Pont du Gard** | `pont-du-gard` | 필수 | Day 20 실제 방문지 (3층 로마 수도교) |
| **Arènes de Nîmes** | `arenes-de-nimes` | 필수 | Day 20 실제 방문지 (로마 원형경기장) |
| **Maison Carrée** | `maison-carree` | 필수 | Day 20 실제 방문지 (고대 로마 신전) |
| **Arles** | `arles` | 필수 | Day 21 실제 방문지 (아를 시티 워크) |
| **Arènes d’Arles** | `arenes-d-arles` | 필수 | Day 21 실제 방문지 (아를 원형경기장) |
| **Théâtre Antique d'Arles** | `theatre-antique-arles` | 필수 | Day 21 실제 방문지 (고대 극장) |
| **Place du Forum** | `place-du-forum-arles` | 우선추천 | Day 21 실제 방문지 (반 고흐 카페 광장) |
| **Cloître Saint-Trophime** | `cloitre-saint-trophime` | 우선추천 | Day 21 실제 방문지 (로마네스크 수도원 회랑) |
| **Fondation Vincent van Gogh Arles** | `fondation-vincent-van-gogh-arles` | 선택 | Day 21 선택 옵션 (현대미술 재단) |
| **La Roquette** | `la-roquette` | 우선추천 | Day 21 실제 방문지 (옛 어부 지구 골목) |
| **Fou de Fafa** | `fou-de-fafa-avignon` | 필수 | Day 22 저녁 식당 (탕튀리에 골목 비스트로) |
| **Les Cocottes Saint-Louis** | `les-cocottes-saint-louis` | 필수 | Day 22 저녁 식당 (수도원 안뜰 비스트로) |
| **Le Gibolin** | `le-gibolin-arles` | 필수 | Day 21 점심 식당 (아를 황소 스튜 비스트로) |
| **Les Baux-de-Provence** | `les-baux-de-provence` | 대체 | Alpilles 대체 옵션 |
| **Carrières des Lumières** | `carrieres-des-lumieres` | 우선추천 | Alpilles 대체 옵션 |
| **Saint-Rémy-de-Provence** | `saint-remy-de-provence` | 대체 | Alpilles 대체 옵션 |
| **Saint-Paul-de-Mausole** | `saint-paul-de-mausole` | 필수 | Alpilles 대체 옵션 |
| **Glanum** | `glanum` | 대체 | Alpilles 대체 옵션 |

---

## 8. Food Cleanup

- **아비뇽과 서부 프로방스에서 맛볼 식재료**: Papeton d'Aubergine, Daube avignonnaise, Brandade de Nîmes, Gardianne de taureau, Fougasse, Tapenade & Anchoïade 등 6종 1문장 기술.
- **와인**: 론 남부 와인을 독립 문장으로 분리(`아비뇽과 서부 프로방스는 론(Rhône) 남부 와인의 중심지다. 운전하는 날에는 마시지 않고 저녁 식사 때 선택한다.`).
- **시장 정보**: Les Halles d'Avignon 및 Place aux Herbes 2곳 링크 수록.
- **방문 업소**: Fou de Fafa, Les Cocottes Saint-Louis, Le Gibolin 3곳 및 식사 원칙 문단 수록.

---

## 9. Stay & Local Life Cleanup

- **숙소와 생활권**: 성벽 안(intra-muros) 도보 생활권 거점, Les Halles 시장 활용, 주방/세탁 구비 숙소 기준, 성벽 남쪽/론강/바르틀라스 섬 아침 러닝 코스로 3개 문단 압축.

---

## 10. Transport Cleanup

- **Avignon에서 이동하기**:
  - `### 시내에서는 걷기`: 성벽 안 100% 도보 원칙
  - `### Uzès와 Pont du Gard는 렌터카`: 근교 이동 후 저녁 TGV역 최종 반납
  - `### Arles는 TER`: 17분 직통 기차 이동 및 도보 원칙
  - `### Lyon으로 출발하는 날`: TGV INOUI 탑승 (렌터카 절차 없음)

---

## 11. Lodging & Planning Residue Archive

- 모든 숙소 권역 비교표, 숙소 채점표, 평가 가중치표, 과거 예산안, Alpilles 대안 분석, 프랑스 일반 도로 매뉴얼 등은 [`source/ARCHIVE/20_Regional_Chapters/09_Avignon_Planning_Residue_v1.0.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/source/ARCHIVE/20_Regional_Chapters/09_Avignon_Planning_Residue_v1.0.md)에 안전하게 분리 보존 완료.

---

## 12. Manuscript Residue Before / After

| 검사 항목 | Before | After | 변화 |
|---|---:|---:|---:|
| `manuscript_residue_check.py` avignon 흔적 토큰 | 32건 | **0건** | -32 (완전 박멸) |
| 원고 번호 및 내부 기획 헤딩 | 14건 | **0건** | -14 |
| 평가 별점 및 점수 표기 | 9건 | **0건** | -9 |

---

## 13. Quantitative Before / After

| 지표 | Before (main) | After (AV01 Consolidation) | 변화 |
|---|---:|---:|---:|
| **원고 줄 수 (Chapter lines)** | 1,307 | **536** | -771 (-59.0%) |
| **보이는 글자 수 (Visible chars, 공백 포함)** | ~21,000 | **10,147** | -10,853 (-51.7%) |
| **순수 글자 수 (Visible chars, 공백 제외)** | ~16,200 | **7,858** | -8,342 (-51.5%) |
| **표 개수 (Tables)** | 19 | **3** | -16 (-84.2%) |
| **장소 카드 수** | 23 | **23** | 정합성 유지 |
| **일정 표현 수 (Schedule representations)** | 4 | **1** | -3 (단일 정본) |
| **원고 흔적 토큰 (Residue tokens)** | 32 | **0** | -32 (완전 박멸) |
| **모바일 390px 스크롤 높이 (추정)** | ~65 screens | **~24 screens** | -63% 압축 |

---

## 14. Automated QA Results

| 검사 항목 | 명령어 | 결과 | 비고 |
|---|---|---|---|
| 사이트 전체 빌드 | `python3 build/site.py` | **PASS** | 372쪽 생성, 색인 191건 |
| 단위 및 통합 테스트 | `pytest tests/` | **PASS** | 30 passed |
| 원고 흔적 가드 | `python3 build/manuscript_residue_check.py` | **PASS** | aix 0, avignon 0, barcelona 0, girona 0, luberon 0 |
| 지역 구조 검사 | `python3 build/region_structure_check.py` | **PASS** | 분류·섹션·방문일·링크 0 오류 |
| 사진 연결 검사 | `python3 build/media_lookup_check.py` | **PASS** | 미매핑 0, 누락 0 |
| 표 손실 검사 | `python3 build/table_loss_check.py` | **PASS** | 조용한 열 손실 0 |
| UX & 디자인 토큰 검사 | `python3 build/ux_check.py` | **PASS** | 명암비, 하단탭, URL 0 결함 |
| PWA 오프라인 검사 | `python3 build/pwa_check.py` | **PASS** | 871개 파일 전체 캐시 |
| 다중 뷰포트 검사 | `python3 build/viewport_check.py` | **PASS** | 6개 해상도 가로 오버플로 0 |
| 사실 토큰 가드 | `build/fact_guard.py` (via site.py) | **PASS** | 45개 확정 토큰 생존 확인 |
| 조사 종결 검사 | `python3 build/research_closure_check.py` | **PASS** | 0 unclassified |
