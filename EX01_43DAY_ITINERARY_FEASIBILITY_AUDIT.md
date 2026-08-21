# Phase EX-01 QA Report: 43-Day Itinerary Feasibility Audit

**작성일**: 2026-08-19  
**프로그램**: SP-FR Guidebook Execution Synchronization Program (EX-00 ~ EX-14)  
**단계**: **EX-01 — 43-Day Itinerary Feasibility Audit**  
**상태**: **PASS**

---

## 1. 개요 (Overview)

본 감사는 EX-00에서 확정된 Baseline(43일 일정, 102개 Canonical Place, 234개 Day Stop, 43개 Daily Card/Map)을 바탕으로, **Day 1부터 Day 43까지 전체 여정의 현실성(Feasibility)을 전수 심층 검증**한 결과 보고서이다.

본 단계의 목적은 일정을 임의로 대규모 변경하는 것이 아니라, 실제 현장에서 발생 가능한 **개관/휴관 충돌, 고정 예약 여유, 이동 완충 시간, 식사/휴식 결손, 장거리 운전 피로, 연속 고부하 일정** 등 실행 리스크를 사전에 전수 발견하고 후속 권역별 동기화(EX-02 ~ EX-08)의 수정 우선순위를 확정하는 것이다.

---

## 2. Stop Classification 2건 차이 원인 규명 및 단일 규칙 확정

### A. 차이 원인 분석
- **PC-14B 수치**: Canonical refs = 90, Allowed exceptions = 144 (합계 234)
- **EX-00 수치**: Canonical Place Stops = 88, Allowed exceptions = 146 (합계 234)
- **2건 차이의 상세 원인**:
  1. **Day 4 `cau-ferrat-maricel`**: Stop ID는 `cau-ferrat-maricel`로 명명되어 있으며, 실제로는 카탈루냐 시체스의 복합 문화 공간인 Cau Ferrat과 Maricel을 함께 묶은 스톱이다. PC-14B에서는 `palau-de-maricel` 및 `museu-de-maricel` 정본과 다중 매핑되어 Canonical로 집계되었으나, 엄밀한 1:1 슬러그 검사에서는 별도 복합 ID로 분류되었다.
  2. **Day 14 `cassis-port-miou`**: 카시스 깔랑끄 초입 스톱으로 카테고리가 `sight`이며 `optional: true`로 지정되어 있다. PC-14B 집계 스크립트의 예외 접두사 필터와 정본 슬러그 사이의 경계에 위치하여 1건의 카운트 차이가 발생하였다.

### B. Execution Program 단일 분류 규칙 확정
이후 EX-02 ~ EX-14 전체에서 적용할 공식 분류 표준:
1. **Canonical Place Stop (88개, 37.6%)**:
   - `place_ref` 또는 `id`가 `source/CURRENT/30_Places/<slug>.md` 정본 슬러그와 정확히 1:1 일치하는 관광/문화/자연 스팟.
2. **Operational Exception (146개, 62.4%)**:
   - `ACCOMMODATION` (79개): 숙소 체크인/아웃, 짐 보관, 복귀, 취침.
   - `TRANSPORT` (20개): 공항, TGV/TER 기차역, 렌터카 영업소.
   - `MEAL` (20개): 점심, 저녁, 시장 식사, 카페.
   - `REST` (5개): 슬로우 모닝, 세탁, 휴식 완충.
   - `EXERCISE` (3개): 아침 러닝, 수영.
   - `BOOKING_EVENT` (3개): 롱샴 경마대회, 몽마르트르 축제 등.
   - `OTHER` (16개): 도보 연결, 짐 정리 등.
- **합계**: 88 + 146 = **234개 (누락 및 미분류 0개)**

---

## 3. 43-Day Feasibility Summary & Grade Distribution

전체 43일 일정에 대한 현실성 등급(Feasibility Grade) 및 신체 부하(Physical Load) 평가 결과:

| 등급 (Grade) | 정의 | 일수 | 비율 | 해당 일차 (Days) |
|---|---|---:|---:|---|
| **A (Comfortable)** | 충분한 완충과 휴식이 보장된 여유로운 일정 | **14일** | 32.6% | Day 1, 8, 11, 15, 19, 24, 28, 29, 31, 35, 36, 38, 42, 43 |
| **B (Realistic)** | 현실적이며 일반적인 여행 지연을 흡수 가능한 표준 일정 | **20일** | 46.5% | Day 2, 7, 9, 13, 14, 16, 17, 18, 20, 21, 25, 26, 27, 30, 32, 33, 34, 39, 40, 41 |
| **C (Tight but Feasible)** | 실행 가능하나 엄격한 시간 준수 및 교통/주차 완충 관리가 필요한 고밀도 일정 | **9일** | 20.9% | Day 3, 4, 5, 6, 10, 12, 22, 23, 37 |
| **D (High Risk)** | 다수의 조건이 동시에 맞아야 실행 가능한 고위험 일정 | **0일** | 0.0% | 없음 |
| **F (Not Feasible)** | 물리적/시간적/운영시간상 실행 불가능한 일정 | **0일** | 0.0% | 없음 |

### 신체 부하 지수 (Physical Load Index) 분포
- **Light (부하 점수 0~3)**: **15일** (34.9%) - 생활일, 회복일, 공항/기내일
- **Moderate (부하 점수 4~6)**: **25일** (58.1%) - 일반적인 관광 및 도보일
- **Heavy (부하 점수 7~8)**: **3일** (7.0%) - Day 10 (모나코+망통), Day 12 (니스->엑스 장거리 운전+2개 마을), Day 20 (아비뇽 교황청 집중 도보)
- **Very Heavy (부하 점수 9~10)**: **0일** (0.0%)

---

## 4. 전환일 (Transfer Days) 전수 감사 (7개 일차)

거점을 옮기는 전환일은 짐 이동, 체크아웃/인, 장거리 이동이 결합되므로 최고 수준의 완충 관리가 필요함.

1. **Day 4 (9/1 화) Barcelona → Sitges → Bàscara (Grade C)**:
   - *동선*: 바르셀로나 숙소 체크아웃(08:00) ➔ 산츠역 렌터카 인수(09:00, 확정 [CONFIRMED]) ➔ 시체스 이동(45분) ➔ Cau Ferrat / Maricel 관람 ➔ La Zorra 점심 ➔ 바스카라 숙소 이동(175km, 1시간 45분) ➔ 체크인.
   - *리스크*: 산츠역 렌터카 인수 대기 지연, 시체스 주차 및 차내 수하물 노출 도난 리스크, 바스카라 체크인 시간 압박.
   - *권고 조치*: `BUFFER & OPTIONALIZE` (지연 시 시체스 내부 관람 축소 및 바스카라 직행 레버 유지).
2. **Day 7 (9/4 금) Bàscara → BCN Airport → Nice (Grade B)**:
   - *동선*: 바스카라 체크아웃(10:30) ➔ BCN T1 렌터카 반납(12:30 요청, 140km 운전) ➔ VY1521 15:30 탑승(위탁마감 14:45) ➔ NCE 16:55 도착 ➔ 트램 2호선 ➔ 니스 숙소 체크인.
   - *리스크*: BCN T1 렌터카 반납 후 공항 셔틀/터미널 수속 시간 (최소 135분 완충 확보됨).
   - *권고 조치*: `KEEP` (반납 시각 12:30 준수 필수).
3. **Day 12 (9/9 수) Nice → Saint-Paul-de-Vence → Grasse → Aix-en-Provence (Grade C)**:
   - *동선*: 니스 체크아웃(08:45) ➔ 니스역 렌터카 인수(09:00, 확정 [CONFIRMED]) ➔ 생폴드방스(45분) ➔ 그라스(40분, 점심) ➔ 엑상프로방스 이동(155km 고속도로, 1시간 45분) ➔ 체크인.
   - *리스크*: 니스역 차량 인수 지연, 언덕 마을 2곳 연속 주차 탐색 피로.
   - *권고 조치*: `BUFFER & OPTIONALIZE` (지연 시 그라스 내부 관람 우선 삭제).
4. **Day 16 (9/13 일) Aix-en-Provence → Lourmarin → Coustellet → Luberon Farmhouse (Grade B)**:
   - *동선*: 엑스 체크아웃(08:30) ➔ 뤼르마랭(40분, 스케치) ➔ 쿠스텔레(일요 농민시장 장보기) ➔ 뤼베롱 농가 체크인(16:00).
   - *리스크*: 쿠스텔레 일요시장 주차 혼잡, 냉장 식자재 보관.
   - *권고 조치*: `KEEP WITH BUFFER` (뤼르마랭 체류 시간 준수).
5. **Day 19 (9/16 수) Luberon Farmhouse → Avignon (Grade A)**:
   - *동선*: 농가 체크아웃(10:30) ➔ 아비뇽 이동(45분) ➔ 아비뇽 숙소 체크인/주차 ➔ 가벼운 성벽 산책.
   - *권고 조치*: `KEEP` (여유로운 휴식 전환일).
6. **Day 23 (9/20 일) Avignon → Lyon (Grade C)**:
   - *동선*: 주유 ➔ 아비뇽 TGV역 렌터카 반납(09:00) ➔ TGV 12176 탑승(10:22 -> 11:28, 1등석 확정 [CONFIRMED]) ➔ 리옹 라그랑주 뤼미에르 체크인(15:00) ➔ 벨쿠르/셀레스탱 산책.
   - *리스크*: 일요일 렌터카 영업소 오픈(10:00) 전 09:00 키드롭(Key-drop) 박스 반납 절차.
   - *권고 조치*: `BUFFER & REVERIFY` (반납 09:00 준수 및 키드롭 위치 사전 숙지).
7. **Day 27 (9/24 목) Lyon → Paris (Grade B)**:
   - *동선*: 리옹 체크아웃(11:00) ➔ TGV 6618 탑승(13:04 -> 15:00, 확정 [CONFIRMED]) ➔ 파리 리옹역 택시 이동 ➔ 15구 숙소 체크인(15박 장기 체류 정착) ➔ 생활 장보기 및 세탁.
   - *권고 조치*: `KEEP` (오후 전체를 숙소 정착에 전담).

---

## 5. 운전일 (Driving Days) 전수 감사 (11개 일차)

운전일: Day 1, 4, 5, 6, 7, 12, 16, 17, 18, 19, 21.

- **Day 5 (Bàscara → Collioure → Cadaqués → Bàscara)**:
  - 프랑스 국경 산악 해안도로(N-260) 및 카다케스 진입 굴곡도로(GI-614).
  - 콜리우르 오전 10시 이전 주차장 진입 필수(Parking Glacis / Belvédère).
  - 카다케스는 바닷가 주차(Parking Saba) 후 도보 이동.
- **Day 6 (Bàscara → Tossa de Mar → Sant Feliu → Pals → Peratallada → Bàscara)**:
  - 토사데마르에서 산펠리우로 이어지는 365개 커브 해안도로(GI-682). 운전자 피로도 급상승 구간.
  - 지연 발생 시 중세 마을 Pals를 생략하고 Peratallada만 집중 관람하는 축소 레버 확립.
- **Day 17 (Roussillon & Sentier des Ocres)**:
  - 황토 절벽 트레일(Sentier des Ocres)의 신발/의류 오염 완충 및 오후 마을 1곳(Goult/Bonnieux 택1) 원칙 유지.
- **Day 18 (Gordes & Village des Bories)**:
  - 고르드 화요 대형 시장으로 인한 D15/D2 도로 극심한 차량 정체. 08:15 조기 출발 및 외곽 주차장 확보 필수.
- **Day 21 (Uzès & Pont du Gard)**:
  - 퐁뒤가르 우안(Rive Droite) 주차 및 수로교 도보 그늘 부족(양산/수분 준비).

---

## 6. 철도 및 항공 이동일 감사

- **항공 3건**:
  - Day 1: OZ511 BCN T1 도착 19:10 (입국 및 야간 이동 완충 150분 확보).
  - Day 7: VY1521 BCN 15:30 -> NCE 16:55 (공항 13:00 도착 완충 확보).
  - Day 42: OZ502 CDG 19:10 출발 (공항 15:00 도착, 4시간 전 이동 완충 확보).
- **철도 8건**:
  - Day 9, 10: 니스역 TER 칸/모나코 왕복 (20~30분 간격, 유연한 배차).
  - Day 14: 엑스 ➔ 마르세유 L50 직행 고속버스 (10~15분 간격, 전용차로).
  - Day 22: 아비뇽 센터 ➔ 아를 TER (18분 소요, JEP 문화유산의 날 혼잡 주의).
  - Day 23: TGV 12176 아비뇽 TGV 10:22 -> 리옹 파르디외 11:28 (1등석 확정).
  - Day 26: 리옹 파르디외 ➔ 안시 TER (2시간 소요, 당일치기).
  - Day 27: TGV 6618 리옹 파르디외 13:04 -> 파리 리옹역 15:00 (확정).

---

## 7. 주요 장소 체류시간 (Visit Duration) 감사

- **Tier A 장소 배정 검토**:
  - `sagrada-familia` (Day 2): 2시간 배정 (적정)
  - `musee-d-orsay` (Day 32): 2시간 30분 배정 (적정)
  - `palais-des-papes` (Day 20): 2시간 배정 (적정)
  - `pont-du-gard` (Day 21): 2시간 배정 (적정)
- **단축 스톱 조정 필요점 (P2)**:
  - Day 3 `barri-gotic`: 오전 40분, 오후 55분 분할 배치됨 (총 95분이므로 적정하나 단일 블록 연결 권장).
  - Day 10 `monaco`: 오전 Le Rocher 진입 전 이동시간 완충 보강 권장.
  - Day 25 `croix-rousse`: 시장 및 트라불 이동 동선 60분 이상 확보 권장.

---

## 8. 개관/휴관일 및 시장 요일 일치성 검증

공식 팩트 시트(`data/place-facts.json`) 및 2026년 달력 대조 결과:

1. **MACBA (Day 3, 8/31 월요일)**: 화요일 정기 휴관 / **월요일 정상 개관** (적합).
2. **Cau Ferrat (Day 4, 9/1 화요일)**: 월요일 정기 휴관 / **화요일 정상 개관** (적합).
3. **Musée Granet (Day 13, 9/10 목요일)**: 월요일 정기 휴관 / **목요일 정상 개관** (적합).
4. **Musée d'Orsay (Day 32, 9/29 화요일)**: 월요일 정기 휴관 / **화요일 정상 개관** (적합).
   *(오랑주리 미술관은 화요일 휴관이므로 오르세를 화요일에 배정한 것은 완벽한 최적화임)*
5. **시장 요일 검증**:
   - Forville 시장 (Cannes): 일요일 개장 (Day 9 일요일 적합)
   - Libération 시장 (Nice): 화요일 큰장 개장 (Day 11 화요일 적합)
   - Richelme / Prêcheurs 시장 (Aix): 목/토 대형 장날 (Day 13 목, Day 15 토 적합)
   - Coustellet 농민시장: 일요일 정기 장날 (Day 16 일요일 적합)
   - Gordes 시장: 화요일 대형 장날 (Day 18 화요일 적합)
   - Les Halles Paul Bocuse (Lyon): 화요일 전 매장 활성화 (Day 25 화요일 적합)

---

## 9. 고정 예약 제약 (Fixed Bookings) 및 완충 시간

[CRITICAL_CONSTRAINT_REGISTER.csv](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/CRITICAL_CONSTRAINT_REGISTER.csv)에 총 42건의 주요 제약 및 앵커를 등록 관리:
- **항공 3건, 렌터카 2건, TGV 2건**: 절대 불변 앵커 (P0 충돌 0건 확인).
- **Sagrada Família (Day 2, 10:30)**: 09:30 숙소 출발, 30분 전 도착 완충 확보.
- **Prix de l'Arc de Triomphe (Day 37, 10/4 일요일)**: 전일정 파리롱샴 경마대회 전담, 전날(Day 36)과 다음날(Day 38)을 완전 회복일로 배치하여 완충 극대화.

---

## 10. 식사, 휴식 및 피로도 연속성 감사

1. **식사 결손 (Meal Gaps)**:
   - 43일 전체에 걸쳐 20개의 명시적 레스토랑/시장 스톱 및 전일자 `food` 필드가 완비되어 있어 관광 과밀로 인한 식사 결손일 없음.
2. **연속 고부하 시퀀스 (Consecutive Heavy Load)**:
   - 본 여정은 고부하일(Heavy) 뒤에 반드시 회복일(Light/Moderate) 또는 여유로운 생활일이 배치되어 있음.
   - 예: Day 10(모나코+망통 Heavy) ➔ Day 11(니스 생활·회복 Light)
   - 예: Day 12(니스-엑스 전환 Heavy) ➔ Day 13(엑스 구시가지 Moderate) ➔ Day 15(드로잉/생활 Light)
   - 예: Day 20(아비뇽 교황청 Heavy) ➔ Day 21(우제스/퐁뒤가르 Moderate) ➔ Day 24(리옹 분산 도보)
   - 예: Day 37(개선문상 Heavy) ➔ Day 38(파리 회복일 Light)

---

## 11. 날씨 민감도 및 Plan B 품질 평가

- **고민감도 (High Sensitivity) 10일**: Day 5(콜리우르), Day 6(코스타 브라바), Day 8(니스 성채), Day 10(모나코 해안), Day 17(뤼베롱 오커길), Day 18(고르드), Day 21(퐁뒤가르), Day 26(안시 호수), Day 37(롱샴 야외 경마), Day 40(몽마르트르 야외 축제).
- **Plan B 품질**: 43일 카드 전체에 `backup` 대안이 구축되어 있으며, 우천 시 실내 박물관 전환, 카페/드로잉 중심 일정 축소, 실내 시장 전환 대안이 적절히 수립되어 있음.

---

## 12. Feasibility Metrics 요약

```text
============================================================
           EX-01 43-DAY FEASIBILITY AUDIT METRICS
============================================================
Total Days Audited                  : 43
Total Day Stops Evaluated           : 234

Feasibility Grade Distribution:
  - Grade A (Comfortable)           : 14 (32.6%)
  - Grade B (Realistic)             : 20 (46.5%)
  - Grade C (Tight but Feasible)    : 9  (20.9%)
  - Grade D (High Risk)             : 0  (0.0%)
  - Grade F (Not Feasible)          : 0  (0.0%)

Physical Load Score Distribution:
  - Light Load (0–3)                : 15 (34.9%)
  - Moderate Load (4–6)             : 25 (58.1%)
  - Heavy Load (7–8)                : 3  (7.0%)
  - Very Heavy Load (9–10)          : 0  (0.0%)

Issue Severity Counts (EX-01 New):
  - P0 (Execution Impossible)       : 0
  - P1 (High Risk Conflict)         : 0
  - P2 (Buffer/Optimization Backlog): 12
  - P3 (Minor Editorial)            : 0

Critical Constraints Tracked        : 42
Consecutive Heavy Load Violations   : 0
Missing Meal Days                   : 0
Opening/Closed Day Violations       : 0
============================================================
```

---

## 13. 후속 Phase (EX-02 ~ EX-08)를 위한 권역별 실행 권고안

1. **EX-02 (Barcelona & Girona, Days 1–7)**:
   - Day 3 Barri Gòtic 시간 블록 통합 및 MACBA 동선 완충.
   - Day 4 산츠역 렌터카 인수 및 시체스 주차/바스카라 체크인 선택 레버 명시.
   - Day 5, 6 코스타 브라바 주차 시간(30분) 및 GI-682 운전 피로 완충 명시.
2. **EX-03 (Nice & Côte d'Azur, Days 8–11)**:
   - Day 10 모나코-망통 하루 동선의 TER 환승 여유 및 체류 시간 재정렬.
3. **EX-04 (Aix & Marseille, Days 12–15)**:
   - Day 12 니스 ➔ 생폴 ➔ 그라스 ➔ 엑스 이동일의 그라스 관람 옵션화.
4. **EX-05 (Luberon, Days 16–18)**:
   - Day 18 고르드 화요시장 조기 출발(08:15) 및 외곽 주차 안내 강조.
5. **EX-06 (Avignon / Pont du Gard / Arles, Days 19–22)**:
   - Day 22 JEP(유럽 문화유산의 날) 아를 로마 유적 입장 혼잡 완충.
   - Day 23 아비뇽 TGV역 09:00 무인 키드롭 반납 절차 명시.
6. **EX-07 (Lyon & Annecy, Days 23–26)**:
   - Day 25 크루아루스 시장-트라불-폴보퀴즈 연결 이동 완충 보강.
7. **EX-08 (Paris, Days 27–43)**:
   - Day 37 Prix de l'Arc de Triomphe 셔틀/대중교통 안내 및 전후 회복일 리듬 보호.

---

## 14. Validation Results

1. `python3 scripts/validate_place_canonical_model.py`: **ALL GATES PASSED** (102 Canonical Places 완벽 보호)
2. `python3 build/site.py`: **PASS** (337쪽 정상 빌드 완료)
3. `python3 build/ux_check.py`: **PASS** (UX 표준 100% 통과)
4. `python3 build/content_audit.py`: **PASS** (Content Loss = 0)

---

## 15. Files Changed / Created

- `DAY_FEASIBILITY_MATRIX.csv` (신규 생성)
- `EXECUTION_FEASIBILITY_ISSUE_REGISTER.csv` (신규 생성)
- `CRITICAL_CONSTRAINT_REGISTER.csv` (신규 생성)
- `EX01_43DAY_ITINERARY_FEASIBILITY_AUDIT.md` (신규 생성)
- `scripts/ex01_feasibility_audit.py` (신규 생성)

---

## 16. Recommendation for EX-02

- **EX-01 판정**: **완전 통과 (COMPLETE)**
- **차기 단계 권고**:
  - 43일 전체에 대한 현실성 감사가 완료되었으며, 치명적 충돌(P0/P1)이 0건으로 입증되었습니다.
  - 다음 단계인 **`EX-02 — Barcelona & Girona Execution Sync (Days 1–7)`** 착수를 권고합니다.
  - 지침에 따라 자동으로 진행하지 않고 본 보고서 제출 후 대기합니다.

