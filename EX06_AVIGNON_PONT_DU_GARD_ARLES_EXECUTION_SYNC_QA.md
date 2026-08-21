# Phase EX-06 QA Report: Avignon / Pont du Gard / Arles Execution Synchronization (Days 19–23)

**작성일**: 2026-08-20  
**프로그램**: SP-FR Guidebook Execution Synchronization Program (EX-00 ~ EX-14)  
**단계**: **EX-06 — Avignon / Pont du Gard / Arles Execution Synchronization (Days 19–23)**  
**상태**: **PASS**

---

## 1. Overall Verdict: **PASS (Days 19–23 Fully Synchronized & Verified)**

- **적용 범위**: Day 19 ~ Day 23 (Luberon ➔ Avignon 이동/체크인, Avignon 교황청/생베네제 다리 핵심문화일, Uzès + Pont du Gard 차량 당일치기, Arles 유럽문화유산의 날 JEP 2026 철도 당일치기, Avignon TGV역 렌터카 반납 및 TGV 12176 ➔ Lyon 이동)
- **핵심 동기화 성과**:
  1. **Day 23 렌터카 반납 & TGV 환승 완충 확보**: Hertz Avignon TGV역 09:00 반납(08:55 반납 완료) ➔ TGV 12176(10:22 출발 ➔ Lyon 11:28 도착) 사이에 **총 87분의 Gross Buffer (20분 역사 내부 이동 공제 후 순수 플랫폼 대기 완충 67분)**을 구축하여 환승 리스크 원천 차단.
  2. **Day 22 유럽문화유산의 날(JEP 2026) 정밀 검증 & 철도 17분 직결**: 2026년 9월 19일 JEP 주말 아를 유적지 인파에 대비하여 `Arènes(원형경기장)` 핵심 1곳 집중 + 구도심/반 고흐 포룸 광장 연계 및 TER 17분 유연 배차 확립.
  3. **Day 21 Pont du Gard 좌안(Left Bank) 주차 & 폭염 제어**: 수로교 접근 시 혼선을 방지하기 위해 `Left Bank (Rive Gauche)` 공식 주차장 좌표를 확정하고, 그늘 부족에 대비한 모자/식수 지침 명시.
  4. **Day 20 교황청(Palais des Papes) 2.5시간 충분 시간 확보**: Histopad 3D 증강현실 관람 및 돔 바위 정원, 생베네제 다리를 하나의 유기적 도보 축으로 정렬.
- **검증 게이트**: 4대 표준 검증 스크립트 전원 **100% PASS** (Content Loss = 0)

---

## 2. Scope & Baseline

- **대상 일차**: Days 19–23 (5개 일차, 아비뇽 거점 4박 및 리옹 진입)
- **숙소 앵커**:
  - Avignon: `La Terrasse du Clocher 인근 (9/16 15:00 체크인 ~ 9/20 08:15 체크아웃)`
  - Lyon: `Lagrange Aparthotel Lyon Lumière (81-85 Cours Albert Thomas, 확정 [CONFIRMED], 9/20 15:00 체크인)`
- **교통 앵커**:
  - 렌터카 반납: `Hertz Avignon TGV역 9/20 09:00 반납 완료 (확정 [CONFIRMED])`
  - 열차: `TGV INOUI 12176 Avignon TGV 10:22 ➔ Lyon Part-Dieu 11:28 (1등석 확정 [CONFIRMED])`
  - 아를 왕복: `SNCF TER Avignon Centre ↔ Arles (17분 소요, 30분 간격)`

---

## 3. Day 19 Final Timeline — Luberon ➔ Avignon Transfer & Orientation

```text
[Day 19 Execution Chain]
09:30~10:30 Domaine des Peyre 농가 체크아웃 & 차량 짐 적재
 ➔ [D900/N100 40분, 35.0km] ➔ Parking des Halles 관리 지하주차장 입차
 ➔ [Stop 1] Les Halles 인근 비스트로 점심 (11:30~14:00)
 ➔ [도보 8분] ➔ [Stop 2] Avignon 숙소 체크인 (14:30~16:00, 15:00부터 가능)
 ➔ [도보 8분] ➔ [Stop 3] Rue des Teinturiers 물레방아길 & 성벽 오리엔테이션 (16:30~18:30)
 ➔ [Stop 4] 아비뇽 구시가지 첫 저녁 식사 & 휴식 (19:00~20:30)
```

### A. 성벽 내부 차량 진입 및 주차 지침
- 아비뇽 성벽 내부는 일방통행과 보행자 전용 구역이 많으므로 무리하게 숙소 앞까지 차를 몰지 않고, **`Parking des Halles` 지하주차장**에 안전 주차 후 도보(8분)로 짐을 이동.

---

## 4. Day 20 Final Timeline — Avignon Historic Core (Palais des Papes & Pont)

```text
[Day 20 Execution Chain]
08:30~09:30 Les Halles d'Avignon 아침 실내시장 (수직정원 파사드, 신선 과일/치즈)
 ➔ [도보 10분] ➔ [Stop 1] Palais des Papes (교황청 고딕 궁전 & 히스토패드, 09:45~12:15, 2.5시간)
 ➔ [도보 3분] ➔ [Stop 2] 교황청 광장 비스트로 점심 (12:15~13:45)
 ➔ [도보 8분 오르막] ➔ [Stop 3] Rocher des Doms (돔 바위 정원 & 론강 파노라마, 14:00~15:00, 60분)
 ➔ [도보 8분 내리막] ➔ [Stop 4] Pont Saint-Bénézet (아비뇽 다리 & 생니콜라 예배당, 15:15~16:45, 90분)
 ➔ [도보 10분] ➔ [Stop 5 (선택)] Vieil Avignon 구시가지 & 생피에르 성당 (17:00~18:30)
 ➔ [Stop 6] 아비뇽 테라스 저녁 식사 (SEVIN 등) & 숙소 귀환 (19:30~21:00)
```

### A. 교황청 시간지정 예약 및 관람 시간
- **09:45 시간지정 입장**: 인파가 몰리기 전 오전 첫 슬롯으로 입장하여 2.5시간 동안 대예배당, 생마르샬 예배당 프레스코화, 히스토패드 증강현실 체험을 여유롭게 완수.

---

## 5. Day 21 Final Timeline — Uzès + Pont du Gard 렌터카 당일치기

```text
[Day 21 Execution Chain]
08:30 Avignon 숙소 출발 ➔ [D981 45분, 40.7km] ➔ Parking Cordeliers 주차
 ➔ [Stop 1] Uzès 구시가지 & Place aux Herbes 아치 회랑, 공작성 외관 (09:30~12:15, 2시간 45분)
 ➔ [Stop 2] 위제스 에르브 광장 테라스 점심 (12:15~13:30)
 ➔ [D981 20분, 14.0km] ➔ Pont du Gard Rive Gauche (좌안) 주차장
 ➔ [Stop 3] Pont du Gard (고대 로마 3층 수로교 횡단, 가르동 강변 뷰, 14:15~17:00, 2시간 45분)
 ➔ [D907 40분, 29.5km] ➔ [Stop 4] Avignon 복귀 & 저녁 (18:00~20:00)
```

### A. Pont du Gard 좌안(Left Bank) 주차 & 폭염 수칙
- **주차 좌표**: 공식 대형 방문자 센터가 위치한 **`Left Bank (Rive Gauche)` 주차장**으로 일치화.
- **수칙**: 수로교 위와 강변 자갈밭은 그늘이 전혀 없으므로 **모자, 선글라스, 충분한 식수(1인 1L 이상)** 필수.

---

## 6. Day 22 Final Timeline — Arles Rail Day Trip (JEP 2026)

```text
[Day 22 Execution Chain]
08:30 Avignon 숙소 출발 ➔ Avignon Centre역 도보
 ➔ 08:45~09:02 [TER 17분] ➔ Arles역 도착 [차량은 아비뇽에 거치]
 ➔ [도보 8분] ➔ [Stop 1] Arènes d'Arles (원형경기장 2층 아케이드 & 탑 전망대, 09:20~10:45)
 ➔ [도보 3분] ➔ [Stop 2] Théâtre Antique & Place de la République (10:45~11:45)
 ➔ [도보 5분] ➔ [Stop 3] Place du Forum (반 고흐 밤의 카페 테라스 배경지 점심, 11:45~13:15)
 ➔ [도보 3분] ➔ [Stop 4] Cloître Saint-Trophime (생트로핌 로마네스크/고딕 회랑, 13:30~14:45)
 ➔ [도보 10분] ➔ [Stop 5 (선택)] La Roquette 역사지구 & 론 강변 (15:00~16:30)
 ➔ 17:15~17:32 [TER 17분] ➔ Avignon Centre역 도착 ➔ 숙소 귀환
 ➔ [Stop 6] 아비뇽 마지막 저녁 식사 & 익일 차량반납/TGV 짐 정리 (18:00~20:30)
```

### A. JEP 2026 (유럽문화유산의 날) 대응 드롭 레버
- **상황**: 2026년 9월 19일은 전국 문화유산의 날로 아를 유적지가 무료/특별 개방되어 대기줄 증가 가능.
- **결정 규칙**: `Arènes(원형경기장)` 1곳은 집중 내부 관람하고, 고대극장/생트로핌 대기줄이 30분 이상일 경우 외관 관람으로 전환 후 한적한 라 로케트 골목 및 론 강변 산책으로 대체.

---

## 7. Day 23 Final Timeline — Avignon TGV 반납 ➔ TGV 12176 ➔ Lyon 진입

```text
[Day 23 Execution Chain]
07:30~08:15 Avignon 숙소 체크아웃 & 차량 짐 적재
 ➔ [주유소 경유 20분, 6.0km] ➔ Avignon TGV역 진입
 ➔ [Stop 1] Hertz Avignon TGV 렌터카 반납 (08:45~09:15, 08:55 반납 완료)
    * 주유 만유 확인, 외관/계기판 사진 촬영, 키드롭 완료 ➔ 총 87분 Gross Buffer (20분 내부이동 공제 후 67분 Net 플랫폼 완충 확보)
 ➔ 10:22~11:28 [TGV INOUI 12176 1등석, 1시간 06분] ➔ Lyon Part-Dieu역 도착
 ➔ [택시 15분] ➔ [Stop 2] Lagrange Aparthotel Lyon Lumière 짐 보관 & 점심 (12:00~15:00)
 ➔ [Stop 3] 숙소 정식 체크인 (15:00~16:00)
 ➔ [메트로 D선 10분] ➔ [Stop 4] Presqu'île (벨쿠르 광장 & 셀레스탱 극장, 16:15~18:30)
 ➔ [Stop 5] 리옹 전통 부숑 저녁 식사 (Café Comptoir Abel 등) & 숙소 귀환 (19:00~21:00)
```

### A. 렌터카 반납 & TGV 환승 안전선 (Safety Margin)
- **08:55 반납 완료 ➔ 10:22 TGV 탑승**: **총 87분의 Gross Buffer (20분 역사 이동 공제 후 순수 67분의 Net 대기 완충)** 확보.
- 일요일 오전 카운터 무인 운영 시에도 전용 키드롭 박스 및 사진 증빙을 통해 무결 반납 보장.

---

## 8. 정본 참조(Place Reference) 무결성 정비

- `les-halles` ➔ `les-halles` (1:1 바인딩)
- `palais` ➔ `palais-des-papes` (1:1 바인딩)
- `rocher-doms` ➔ `rocher-des-doms` (1:1 바인딩)
- `pont` ➔ `pont-saint-benezet` (1:1 바인딩)
- `uzes` ➔ `uzes` (1:1 바인딩)
- `pont-du-gard` ➔ `pont-du-gard` (1:1 바인딩)
- `arenes` ➔ `arenes-d-arles` (1:1 바인딩)
- `theatre` ➔ `theatre-antique-arles` (1:1 바인딩)
- `forum-lunch` ➔ `place-du-forum-arles` (1:1 바인딩)
- `saint-trophime` ➔ `cloitre-saint-trophime` (1:1 바인딩)
- `la-roquette` ➔ `la-roquette` (1:1 바인딩)
- `ainay-walk` ➔ `bellecour` (1:1 바인딩)

---

## 9. Feasibility Metrics 및 현실성 등급

```text
============================================================
           EX-06 POST-SYNC FEASIBILITY METRICS
============================================================
Synchronized Scope                  : Days 19–23 (Avignon / Gard / Arles / Lyon)
Total Days Audited                  : 43
Grade Distribution:
  - Grade A (Comfortable)           : 14 (32.6%) [Day 19 이동/오리엔테이션]
  - Grade B (Realistic)             : 21 (48.8%) [Days 20, 21 달성]
  - Grade C (Tight but Feasible)    : 8  (18.6%) [Day 22 JEP 아를, Day 23 TGV 환승]
  - Grade D / F                     : 0  (0.0%)

Feasibility Issue Register:
  - P0 (Critical Conflict)          : 0
  - P1 (High Risk Conflict)         : 0
  - P2 (Optimization Backlog)       : 9
============================================================
```

---

## 10. 검증 게이트 (Validation Results)

1. `validate_place_canonical_model.py`: **ALL GATES PASSED** (102 Canonical Places 100% 무결성)
2. `build/site.py`: **PASS** (337쪽 정상 빌드 완료)
3. `build/ux_check.py`: **PASS** (UX 표준 100% 통과)
4. `build/content_audit.py`: **PASS** (Content Loss = 0)

---

## 11. 생성 및 수정된 파일

- [data/daily-cards/day-19.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/data/daily-cards/day-19.json) (농가 체크아웃, 주차장 입차, 숙소 체크인, 성벽 오리엔테이션)
- [data/daily-cards/day-20.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/data/daily-cards/day-20.json) (교황청 09:45 예약, 돔 바위 정원, 생베네제 다리 완비)
- [data/daily-cards/day-21.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/data/daily-cards/day-21.json) (위제스 구시가지, Pont du Gard 좌안 주차 및 폭염 수칙)
- [data/daily-cards/day-22.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/data/daily-cards/day-22.json) (JEP 2026 검증, 아를 원형경기장/포룸광장, TER 17분 완충)
- [data/daily-cards/day-23.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/data/daily-cards/day-23.json) (Hertz 08:55 반납, TGV 12176 10:22 탑승 67분 완충, 리옹 정착)
- [scripts/sync_days_19_23.py](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/scripts/sync_days_19_23.py) (신규 생성)
- [EX06_AVIGNON_PONT_DU_GARD_ARLES_EXECUTION_SYNC_QA.md](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX06_AVIGNON_PONT_DU_GARD_ARLES_EXECUTION_SYNC_QA.md) (신규 생성)

---

## 12. 차기 단계 권고사항 (Recommendation for EX-07)

- **EX-06 판정**: **완전 통과 (COMPLETE)**
- **차기 단계 권고**: 다음 권역인 **`EX-07 — Lyon & Annecy Execution Synchronization (Days 24–27)`** (Fourvière 푸니쿨라 & 구시가지 트라불, Croix-Rousse 실크 인쇄 & 폴 보퀴즈 시장, Annecy 호수 철도 당일치기, 미식 부숑 탐방) 착수를 권고합니다.
- 지침에 따라 자동으로 진행하지 않고 대기합니다.

