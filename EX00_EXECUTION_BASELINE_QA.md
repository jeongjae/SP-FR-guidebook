# Phase EX-00 QA Report: Program Baseline & Execution Data Model

**작성일**: 2026-08-19  
**프로그램**: SP-FR Guidebook Execution Synchronization Program (EX-00 ~ EX-14)  
**단계**: **EX-00 — Program Baseline & Execution Data Model**  
**상태**: **PASS**  

---

## 1. Overall Verdict

- **전체 판정**: **PASS (Baseline Established & Fully Validated)**
- **요약**: Place Content Enrichment Program(PC-14B)을 통해 완성된 102개 Canonical Place SOT를 기반으로, 43일 전체 여정의 실행 레이어(Itinerary, Daily Cards, Maps, Routes, Bookings, Transport, Accommodation, Meals, Plan B)에 대한 전수 조사를 완료하고 공식 Baseline과 Execution Data Model을 확립하였다.
- **주요 산출물**:
  1. `EX00_EXECUTION_BASELINE_QA.md` (본 종합 감사 보고서)
  2. `EXECUTION_DATA_MODEL.md` (실행 데이터 모델 및 아키텍처 명세서)
  3. `DAY_EXECUTION_INVENTORY.csv` (43일 전체 실행 인벤토리 데이터셋)
  4. `EXECUTION_SYNC_ISSUE_REGISTER.csv` (발견된 78개 이슈 레지스터)

---

## 2. Current Execution Architecture (현재 실행 아키텍처)

실제 저장소의 파일 구조 및 계층 관계를 조사한 결과는 다음과 같다.

```text
[SOT & Source Data]
 ├── source/CURRENT/30_Places/*.md (102개 Canonical Place 장문 정본)
 ├── source/CURRENT/10_Core/itinerary.json (43일 숙박 거점 및 체류 정본)
 ├── source/CURRENT/10_Core/regions.json (8개 권역 메타데이터)
 ├── source/CURRENT/20_Regions/*.md (8개 권역 편집 서술)
 ├── source/ASSETS/91_Place_Registry_v1.0.md (장소 공식 명부 및 등급)
 ├── data/daily-cards/day-NN.json (43일 일자별 실행 정본: stops, legs, times, map)
 ├── data/daily-cards/routes/*.json (11개 운전일 OSRM 사전 계산 경로)
 ├── data/place-facts.json (65개 장소 공식 사실: 운영시간, 요금, 예약)
 └── data/images/image-manifest.json (사진 매니페스트)

[Build & Model Engine]
 ├── build/model.py (Trip, Region, Day, Stop, Leg, Place, Fact 통합 로더)
 ├── build/site.py (정적 사이트 빌더 - 337쪽 생성)
 ├── build/render.py (UI 컴포넌트, Daily Card, MapCard 렌더러)
 ├── build/guards/*.py (Fact 토큰, 충돌, 신선도 가드)
 └── scripts/validate_place_canonical_model.py (Place 정본 보호 가드)
```

---

## 3. SOT Matrix (정본 확정 매트릭스)

| 데이터 도메인 | 단일 정본 (SOT) | 부속/소비 레이어 | 중복/불일치 위험 요소 및 거버넌스 |
|---|---|---|---|
| **장소 심층 해설** | `source/CURRENT/30_Places/<slug>.md` | 8개 지역 챕터, 검색 색인, 장소 HTML | 지역 챕터 내 중복 장문 작성 금지 (PC-14 가드로 보호 중) |
| **일정 순서 (Stop Order)** | `data/daily-cards/day-NN.json` | Daily Card UI, Day Map 핀 순서 | 마크다운 원고와 JSON 간 순서 분기 방지 (Day JSON이 SOT) |
| **방문/이동 시각** | `data/daily-cards/day-NN.json` | Daily Card 타임라인 | 장소 체류시간은 Place 사실, 출발/도착시각은 Day JSON이 SOT |
| **교통편 (Transport/Legs)** | `data/daily-cards/day-NN.json` | Daily Card 이동 배지, 지도 | 장거리 환승/열차편은 `110_Phase8` 잠금 레지스터와 동기화 |
| **고정 예약 (Bookings)** | `110_Phase8_Lock_Register.md` + `place-facts.json` | Day JSON `reservation`, Card 배지 | 고정 예약 시간과 Day stop start 시각 일치 필요 |
| **숙소 (Accommodation)** | `source/CURRENT/10_Core/itinerary.json` | Day JSON `hotel`, 지도 숙소 핀 | `stays` 배열이 거점의 정본, 상세 주소는 `hotel` 객체가 보완 |
| **좌표 (Coordinates)** | `data/daily-cards/day-NN.json` (Stop) / `30_Places` | Day Map, 여정 Map, 길찾기 링크 | WGS84 좌표 기준, 불명 시 `address` 검색 폴백 |
| **경로선 (Daily Route)** | `data/daily-cards/routes/day-NN-*.json` | Day Map OSRM 지오메트리 | 현재 11일(운전일)만 존재, 보행일은 핀만 표시 중 (EX-10 대상) |
| **식사 (Meals)** | `data/daily-cards/day-NN.json` (`food`) | Daily Card 식사 섹션 | 특정 식당 vs 권역 일반식 구분 명시 |
| **Plan B** | `data/daily-cards/day-NN.json` (`backup`) | Daily Card 대안 카드, 20_Regions | 날씨/지연/휴관 대안의 Day별 구체성 강화 필요 |

---

## 4. 43-Day Inventory Summary

`DAY_EXECUTION_INVENTORY.csv` 생성 완료 (43행 전수 조사):

- **총 일수**: 43일 (2026-08-29 ~ 2026-10-10)
- **총 권역**: 8개 거점 (Barcelona, Girona/Bàscara, Nice, Aix-en-Provence, Luberon, Avignon, Lyon, Paris)
- **전환일 (Transfer Days)**: 7일 (Day 4, 7, 12, 16, 19, 23, 27)
- **렌터카 이용일**: 11일 (스페인 4일: Day 4~7, 프랑스 남부 8일: Day 12~19, 21, 23 반납)
- **철도(TGV/TER) 이용일**: 8일 (Day 9, 10, 14, 22, 23, 26, 27)
- **비행기 이동일**: 3일 (Day 1 입국, Day 7 BCN->NCE, Day 42~43 귀국)

---

## 5. Stop Classification (234개 전체 Stop 분류)

전체 234개 Day Stop에 대한 분류 결과:

| 분류 (Taxonomy) | 개수 | 비율 | 주요 예시 |
|---|---:|---:|---|
| **PLACE** (정본 장소) | **88** | 37.6% | Sagrada Família, Musée d'Orsay, Pont du Gard, Palais des Papes 등 |
| **ACCOMMODATION** (숙소) | **79** | 33.8% | 체크인, 체크아웃, 샤워, 짐 보관, 복귀, 취침 |
| **TRANSPORT** (교통 허브) | **20** | 8.5% | BCN 공항, NCE 공항, Sants역, Avignon TGV역, Part-Dieu역, CDG 공항 |
| **MEAL** (식사/카페) | **20** | 8.5% | 점심/저녁 식사, Bar Cañete, La Zorra, Forville 시장 점심 등 |
| **REST** (휴식/생활) | **5** | 2.1% | 슬로우 모닝, 세탁/정리, 완충 시간 |
| **EXERCISE** (운동) | **3** | 1.3% | 아침 조깅, 야외 수영 |
| **BOOKING_EVENT** (행사) | **3** | 1.3% | Prix de l'Arc de Triomphe, 몽마르트르 축제 등 |
| **OTHER** (기타 연결) | **16** | 6.8% | 동네 적응 산책, 귀로 이동, 짐 정리 |
| **합계** | **234** | **100.0%** | **미분류 갭: 0개** |

---

## 6. Daily Card Architecture 감사

- **보유 현황**: 43개 파일 전수 존재 (`data/daily-cards/day-01.json` ~ `day-43.json`).
- **스키마 준수율**: 100% (모든 파일이 `schemaVersion`, `day`, `date`, `city`, `title`, `stops`, `legs`, `transport`, `food`, `highlights`, `backup`, `map` 포함).
- **일치성 검토**:
  - Stop 방문 순서가 마스터 일정표 및 지역 챕터의 권장 동선과 기본 일치함.
  - 53개 Stop에 `place_ref`가 명시되어 있으며, 35개는 `id` 자체가 Canonical Slug와 일치하여 총 88개 Stop이 Canonical Place로 직접 바인딩됨.
  - 나머지 146개 Stop은 숙소/교통/식사/휴식 등 허용된 실행 예외 Stop임.

---

## 7. Map & Route Architecture 감사

### 지도 유형 현황
1. **Day Map (일자별 지도)**: 43개 전수 존재 (Leaflet/HTML 기반 렌더링).
2. **Region Map (권역 지도)**: 8개 권역 전수 존재 (`map/<region>.html`).
3. **Trip Map (전체 여정 지도)**: 1개 전수 존재 (`map/index.html`).
4. **Google Maps 외부 딥링크**: 모든 Stop마다 실시간 길찾기/검색 URL 자동 생성 연동 (`https://www.google.com/maps/search/?api=1&query=lat,lng`).

### Route Status Classification (43일 전체 경로 현황)

- **상태 D (사전 계산된 운전 지오메트리 보유)**: **11일** (Day 1, 4, 5, 6, 7, 12, 16, 17, 18, 19, 21)
- **상태 A (순서화된 장소 핀만 표시)**: **32일** (대다수 도보일 및 파리 장기 체류일)
- **상태 G (지도 없음)**: **0일**

> **주요 발견점**: 현재 렌터카 이동일에 대해서만 OSRM GeoJSON 캐시가 생성되어 있으며, 대도시 도보일(Barcelona, Nice, Aix, Lyon, Paris)은 핀만 표시되고 실제 도보 연결선이 없음. 이는 **Phase EX-10 (Daily Route Map Full Rebuild)**에서 전수 생성/보완 예정.

---

## 8. Place ↔ Day Coverage 감사

- **총 Canonical Place**: 102개
- **Daily Card 스톱에 직접 배치된 장소**: 63개 (88개 Stop references)
- **Daily Card 스톱 미배치 장소**: 39개
  - *원인 분석*: 미배치된 39개 장소는 Regional Chapter에 수록된 선택 관광지(`optional`), 테마별 도보 코스(`walk`), 인근 추천 마을, 대체 목적지(`alternative`)로 구성되어 있음. (예: `abbaye-de-senanque`, `bonnieux`, `cannes-walk`, `carrieres-de-bibemus` 등).
  - *조치 계획*: Regional Sync Phase(EX-02 ~ EX-08)에서 해당 선택지들을 Daily Card의 Plan B 또는 선택 스톱으로 적절히 노출하도록 정비.

---

## 9. Day ↔ Card ↔ Map Consistency

- **Day ↔ Card 순서 일치율**: **100% (43/43 Days MATCH)**
- **Day ↔ Map 핀 순서 일치율**: **100% (43/43 Days MATCH)**
  - MapCard는 Day JSON의 `stops` 배열을 그대로 순회하여 핀을 생성하므로 Stop Order와 Map Pin Order의 구조적 불일치가 원천 방지되어 있음.

---

## 10. Time, Transport & Booking Architecture

1. **시간 데이터 구조**:
   - `Day`: 당일 전체 시작/종료 시각 (`startTime`, `endTime`), 총 소요시간 (`totalDuration`).
   - `Stop`: 개별 스톱 도착/출발 시각 (`start`, `end`).
   - `Leg`: 구간별 이동 소요시간 (`duration`).
2. **교통 데이터 구조**:
   - `legs` 배열을 통해 각 구간의 이동 수단(`mode`: walk, metro, train, drive, flight), 노선 번호(`line`), 거리(`distance`)를 표현.
3. **예약 데이터 구조**:
   - 항공편 3건 (OZ511, VY1521, OZ502 확정 PNR 수록)
   - 렌터카 2건 (Hertz 스페인 [CONFIRMED], 프랑스 [CONFIRMED])
   - 열차편 2건 (TGV 12176, TGV 6618 1등석 확정 PNR 수록)
   - 미술관/유적 19건 (Sagrada Família, Sant Pau, Granet, Pont du Gard, Orsay 등 예약 상태 관리)

---

## 11. Accommodation, Meal & Plan B Architecture

1. **숙소 (Accommodation)**:
   - 8개 거점 숙소(호텔, 에어비앤비, 농가)의 체크인/아웃 시각과 숙소 복귀 동선이 Day 1~43 전체에 79개 스톱으로 촘촘히 통합됨.
2. **식사 (Meal)**:
   - 20개의 핵심 식사/시장 스톱이 타임라인에 명시되어 있으며, 43개 Card 전체에 `food` 추천 리스트가 구성됨.
3. **Plan B**:
   - 43개 Card 전체에 `backup` 필드가 존재하여 우천/휴관/피로 시 대안 경로가 정의됨.

---

## 12. Baseline Metrics 종합

```text
============================================================
           SP-FR EXECUTION PROGRAM BASELINE METRICS
============================================================
Total Trip Days                     : 43
Total Trip Regions                  : 8
Total Canonical Places              : 102
Total Day Stops                     : 234

Stop Breakdown:
  - Canonical Place Stops           : 88 (37.6%)
  - Accommodation Stops             : 79 (33.8%)
  - Transport Hub Stops             : 20 (8.5%)
  - Meal & Dining Stops             : 20 (8.5%)
  - Rest & Recovery Stops           : 5  (2.1%)
  - Exercise & Wellness Stops       : 3  (1.3%)
  - Booking & Event Stops           : 3  (1.3%)
  - Other Operational Stops         : 16 (6.8%)

Daily Cards Status:
  - Cards Present                   : 43 / 43 (100%)
  - Cards Missing                   : 0

Map & Routing Status:
  - Day Maps Present                : 43 / 43 (100%)
  - Precomputed OSRM Driving Routes : 11 (Days 1, 4-7, 12, 16-19, 21)
  - Pin-only Maps (Walking/Transit) : 32
  - Missing Maps                    : 0

Consistency & Integrity:
  - Day Stop vs Card Order Match    : 43 / 43 (100%)
  - Day Stop vs Map Pin Order Match : 43 / 43 (100%)
  - Broken Place References         : 0
  - Content Loss                    : 0
============================================================
```

---

## 13. P0/P1/P2/P3 Issue Register Summary

`EXECUTION_SYNC_ISSUE_REGISTER.csv`에 등록된 78개 이슈 현황:

- **P0 (치명적 일정/예약 충돌)**: **0건**
- **P1 (일정·지도·카드 간 순서 불일치)**: **0건**
- **P2 (개선/보완 필요 사항)**: **78건**
  - `MAP_ROUTE` (32건): 도보/대중교통일의 사전 계산 경로 지오메트리 부재 (EX-10에서 생성 예정).
  - `ORPHAN_CANONICAL_PLACE` (39건): Daily Card 기본 스톱에 미포함된 선택/대체 관광지 (EX-02~EX-08에서 카드 Plan B 및 선택 스톱으로 노출 보완 예정).
  - `CANONICAL_REF` (7건): 장거리 이동일 등 정본 장소 방문이 없는 날의 스톱 참조 정비 (EX-02~EX-08 대상).
- **P3 (UX/스타일 미세 조정)**: **0건**

---

## 14. Validation Results

모든 표준 게이트 검증 스크립트 실행 결과:

1. `python3 scripts/validate_place_canonical_model.py`: **ALL GATES PASSED** (102 Canonical Places 100% 무결성 보존)
2. `python3 build/site.py`: **PASS** (337쪽 정상 빌드 완료)
3. `python3 build/ux_check.py`: **PASS** (대비율, 하단탭, 데일리 카드 100% 정상)
4. `python3 build/content_audit.py`: **PASS** (Content Loss = 0)

---

## 15. Files Changed / Created

- `DAY_EXECUTION_INVENTORY.csv` (신규 생성)
- `EXECUTION_SYNC_ISSUE_REGISTER.csv` (신규 생성)
- `EXECUTION_DATA_MODEL.md` (신규 생성)
- `EX00_EXECUTION_BASELINE_QA.md` (신규 생성)
- `scripts/ex00_baseline_audit.py` (신규 생성)

---

## 16. Recommendation for EX-01

- **EX-00 판정**: **완전 통과 (COMPLETE)**
- **차기 단계 권고사항**:
  - `EX-01 — 43-Day Itinerary Feasibility Audit`로 진입할 준비가 완벽히 갖추어짐.
  - EX-01에서는 43일 전체 일정에 대해 각 날짜별 체류시간, 이동시간 완충, 식사/휴식 시간 확보, 개관/운영시간 제약, 누적 피로도를 전수 검토하여 `DAY_FEASIBILITY_MATRIX.csv` 및 `EX01_43DAY_ITINERARY_FEASIBILITY_AUDIT.md`를 산출할 것을 권고함.
  - 지침에 따라 EX-01로 자동 진행하지 않고 보고 후 대기함.

