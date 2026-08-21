# Phase EX-05 QA Report: Luberon Driving Execution Synchronization (Days 16–18)

**작성일**: 2026-08-20  
**프로그램**: SP-FR Guidebook Execution Synchronization Program (EX-00 ~ EX-14)  
**단계**: **EX-05 — Luberon Driving Execution Synchronization (Days 16–18)**  
**상태**: **PASS**

---

## 1. Overall Verdict: **PASS (Days 16–18 Fully Synchronized)**

- **적용 범위**: Day 16 ~ Day 18 (Aix ➔ Luberon 이동일, Roussillon/Sentier des Ocres, Gordes 화요시장 & Bories/Sénanque/Ménerbes, 농가 숙소 체류 및 아비뇽 이동 준비)
- **핵심 동기화 성과**:
  1. **숙소 기준선 완전 확립**: 뤼베롱 농가 숙소(`Domaine des Peyre`, 43.87088, 5.12202)를 매일의 출발/귀환 앵커로 전면 배치하고 실측 이동시간 및 진입 농로(Chemin des Peyres) 특성 반영.
  2. **시장 및 식재료 확보 체계화**: Day 16 Coustellet 일요 파머스 마켓(13:00 마감 전 신선 식재료 구매) 및 Day 18 Gordes 화요 대형 시장(08:15 조기 출발로 외곽 주차장 선점) 완벽 설계.
  3. **지형/환경 리스크 제어**: 오커 트레일 붉은 먼지 주의(어두운색 의류/신발), 한낮 13:30~15:30 폭염 회피를 위한 농가 휴식(Siesta), D177 일방통행 협곡 도로 서행 수칙 명시.
  4. **과다 이동(Village-Hopping) 방지**: 하루 2~3개 핵심 스톱으로 제한하고 Goult/Bonnieux/Ménerbes 선택 규칙 명시.
- **검증 게이트**: 4대 표준 검증 스크립트 전원 **100% PASS** (Content Loss = 0)

---

## 2. Scope & Baseline

- **대상 일차**: Days 16–18 (3개 일차, 뤼베롱 거점 3박)
- **숙소 앵커**: `Domaine des Peyre (Robion/Coustellet 인근 농가 숙소, 9/13 15:30 체크인 ~ 9/16 10:30 체크아웃)`
- **교통망**: 렌터카 (Hertz Nice역 인수 차량 [CONFIRMED] 보유 상태 운행)

---

## 3. Day 16 Final Timeline — Aix ➔ Luberon Transfer & Coustellet Market

```text
[Day 16 Execution Chain]
08:00~08:45 Aix 숙소 체크아웃 & 수하물 완전 은폐 적재 (가림막 장착)
 ➔ [D543/D943 40분, 36.8km] ➔ Parking du Rayol 주차
 ➔ [Stop 1] Lourmarin 마을 & 르네상스 샤토 외관 (09:30~11:30, 2시간)
 ➔ [D943/D900 30분, 28.0km] ➔ Parking de la Gare 주차
 ➔ [Stop 2] Marché Paysan de Coustellet & 3박 식재료 구매 (12:00~13:30, 90분)
 ➔ [D900 12분, 8.5km] ➔ [Stop 3 (선택)] Goult 완충 & Café de la Poste (13:45~15:00, 75분)
 ➔ [D900/농로 13분, 11.0km] ➔ [Stop 4] Domaine des Peyre 농가 체크인 (15:30~20:30)
 ➔ 수영장/테라스 휴식 및 쿠스텔레 시장 식재료로 테라스 첫 저녁 식사
```

### A. 차량 짐 은폐 및 루르마랭 안전 수칙
- 엑스 체크아웃 후 이동일이므로 트렁크에 모든 짐이 실려 있음.
- **수칙**: 루르마랭 외곽 공식 주차장(`Parking du Rayol` / `Parking du Château`) 이용, 트렁크 짐 노출 금지(가림막 필수), 귀중품 휴대.

### B. Coustellet 일요 파머스 마켓 식재료 미션
- **운영시간**: 매주 일요일 08:00~13:00 운영. 12:00 도착으로 폐장 전 신선 치즈, 프로방스 멜론, 무화과, 바게트, 샤퀴테리, 와인 및 생수 3박 분량 확보.

---

## 4. Day 17 Final Timeline — Roussillon / Sentier des Ocres & Goult

```text
[Day 17 Execution Chain]
08:30 농가 숙소 출발 ➔ [D900/D104 20분, 16.7km] ➔ Parking Saint-Michel 주차
 ➔ [Stop 1] Sentier des Ocres (오커 트레일 붉은 절벽길, 09:00~10:30, 90분)
 ➔ [Stop 2] Roussillon 구시가지 & 비스트로 점심 (10:30~13:15, 165분)
 ➔ [D227/D900 20분, 17.2km] ➔ [Stop 3] 농가 숙소 복귀 & 한낮 휴식 (Siesta, 13:45~15:45, 2시간)
 ➔ [D900/D218 13분, 10.8km] ➔ [Stop 4] Goult 생활마을 & 예루살렘 풍차 언덕 (16:00~18:00, 2시간)
 ➔ [D218/D900 13분, 10.9km] ➔ [Stop 5] 농가 복귀 & 테라스 저녁 (18:30~20:30)
```

### A. 오커 트레일 실전 주의사항 (Ochre Dust Caution)
- **오전 방문**: 09:00~10:30 햇살이 붉은 황토벽을 가장 선명하게 비추는 시간대 방문.
- **의류/신발 주의**: 붉은 오커 흙먼지가 섬유에 영구 착색될 수 있으므로 **밝은색 옷/흰 운동화 착용 절대 금지**, 어두운색 편한 신발과 모자, 생수 필수.

### B. 한낮 폭염 회피 (Siesta) & Goult 2차 마을 선택
- 13:30~15:30 한낮 폭염 시간대에는 농가 숙소로 복귀하여 수영장/에어컨 휴식.
- 16:00 이후 선선해진 시간에 관광객이 적고 한적한 돌담길 생활마을인 **Goult(구트)**를 집중 산책(풍차 언덕 뷰).

---

## 5. Day 18 Final Timeline — Gordes Tuesday Market & Stone Culture

```text
[Day 18 Execution Chain]
08:15 농가 숙소 조기 출발 ➔ [D15 15분, 9.8km] ➔ Parking Bel-Air (외곽 주차장 선점)
 ➔ [Stop 1] Gordes 화요 대형 시장 & 벨베데레 전경 (08:45~11:30, 2시간 45분)
 ➔ [D15 8분, 4.4km] ➔ [Stop 2] Village des Bories (건식 석조 가옥 마을, 11:45~12:45, 60분)
 ➔ [Stop 3] 고르드 시장 식재료 피크닉 점심 (12:45~13:45, 60분)
 ➔ [D177 12분, 7.5km] ➔ [Stop 4 (선택)] Abbaye de Sénanque 외관 (14:00~15:15, 75분)
 ➔ [D177/D3 20분, 15.0km] ➔ [Stop 5 (선택)] Ménerbes 언덕마을 산책 (15:45~17:00, 75분)
 ➔ [D3/D900 12분, 10.2km] ➔ [Stop 6] 농가 복귀 & 익일 Avignon 이동 준비 (17:30~19:30)
```

### A. Gordes 화요 시장 교통/주차 전략
- 뤼베롱 최대 혼잡일이므로 **08:15 조기 출발하여 08:45 이전 외곽 `Parking Bel-Air` 선점** (셔틀 또는 도보 8분 마을 진입).
- Google Maps 단순 ETA(12분) 대신 진입로 병목 및 주차 대기 완충(+15분) 배정.

### B. Sénanque 수도원 9월 현실성 및 도로 주의
- 9월 중순은 라벤더 수확이 끝난 시기이므로 라벤더 기대 대신 **12세기 시토회 수도원의 순수한 석조 건축미** 감상에 집중.
- 진입로 **D177 지방도는 좁은 협곡 일방통행 구간**이 포함되어 있으므로 서행 필수.

### C. Day 19 Avignon 이동 보호
- 17:30 농가 조기 복귀하여 주유, 짐 정리, 체크아웃 준비 완료.

---

## 6. 주차장 체계 (Primary / Backup Parking Layer)

| 마을 | Primary Parking | Backup Parking | 비고 |
|---|---|---|---|
| **Lourmarin** | `Parking du Rayol` (무료/외곽) | `Parking du Château` (유료/고성앞) | 진입 평이, 도보 5분 |
| **Coustellet** | `Parking de la Gare` (시장 광장) | `Super U 주차장` | 장보기 연계 편리 |
| **Roussillon** | `Parking Saint-Michel` (오커길 입구) | `Parking des Sablières` (외곽) | 09:00 이전 선점 권장 |
| **Goult** | `Place de la Libération` (마을 입구) | `Rue de la République 노상` | 주차 여유로움 |
| **Gordes** | `Parking Bel-Air` (외곽, 셔틀/도보) | `Parking Charles de Gaulle` (유료) | 화요시장 08:45 전 진입 필수 |
| **Village des Bories**| `Bories 전용 주차장` (현장) | — | 진입로 협소(교행 주의) |
| **Abbaye de Sénanque**| `수도원 전용 주차장` (P1/P2) | — | D177 일방통행 주의 |
| **Ménerbes** | `Parking de la Mairie` (마을 중심) | `Parking du Lavoir` (하단) | 언덕길 도보 5분 |

---

## 7. 정본 참조(Canonical Place Ref) 무결성

- `lourmarin` ➔ `lourmarin` (1:1 바인딩)
- `coustellet` ➔ `coustellet` (1:1 바인딩)
- `goult` ➔ `goult` (1:1 바인딩)
- `sentier-ocres` ➔ `roussillon-sentier-des-ocres` (1:1 바인딩)
- `roussillon` ➔ `roussillon-sentier-des-ocres` (1:1 바인딩)
- `gordes` ➔ `gordes` (1:1 바인딩)
- `village-des-bories` ➔ `village-des-bories` (1:1 바인딩)
- `senanque` ➔ `abbaye-de-senanque` (1:1 바인딩)
- `menerbes` ➔ `menerbes` (1:1 바인딩)
- *숙소/식사(`aix-checkout`, `farm-checkin`, `farm-depart`, `farm-rest`, `farm-return`, `picnic`)는 `place_ref: null`로 표준화.*

---

## 8. Feasibility Metrics 및 신체 부하

```text
============================================================
           EX-05 POST-SYNC FEASIBILITY METRICS
============================================================
Synchronized Scope                  : Days 16–18 (Luberon Driving)
Total Days Audited                  : 43
Grade Distribution:
  - Grade A (Comfortable)           : 14 (32.6%)
  - Grade B (Realistic)             : 21 (48.8%) [Days 16, 17, 18 모두 Grade B 유지]
  - Grade C (Tight but Feasible)    : 8  (18.6%)
  - Grade D / F                     : 0  (0.0%)

Physical Load:
  - Day 16: Moderate (5) - 이동 및 장보기, 농가 조기 정착
  - Day 17: Moderate (5) - 오커 트레일 도보 + 한낮 Siesta 휴식으로 완화
  - Day 18: Moderate (6) - 화요시장 보행 + Bories 관람 + 17:30 조기 복귀
============================================================
```

---

## 9. 검증 게이트 (Validation Results)

1. `validate_place_canonical_model.py`: **ALL GATES PASSED** (102 Canonical Places 100% 무결성)
2. `build/site.py`: **PASS** (337쪽 정상 빌드 완료)
3. `build/ux_check.py`: **PASS** (UX 표준 100% 통과)
4. `build/content_audit.py`: **PASS** (Content Loss = 0)

---

## 10. 생성 및 수정된 파일

- [data/daily-cards/day-16.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/data/daily-cards/day-16.json) (Aix 체크아웃, 루르마랭 짐 은폐, 쿠스텔레 장보기, 농가 체크인 완비)
- [data/daily-cards/day-17.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/data/daily-cards/day-17.json) (오커 트레일 복장 주의, 한낮 Siesta, Goult 2차 마을 완비)
- [data/daily-cards/day-18.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/data/daily-cards/day-18.json) (08:15 조기출발, 고르드 시장 주차, Bories/세낭크/메네르브 및 아비뇽 준비 완비)
- [scripts/sync_days_16_18.py](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/scripts/sync_days_16_18.py) (신규 생성)
- [EX05_LUBERON_DRIVING_EXECUTION_SYNC_QA.md](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX05_LUBERON_DRIVING_EXECUTION_SYNC_QA.md) (신규 생성)

---

## 11. 차기 단계 권고사항 (Recommendation for EX-06)

- **EX-05 판정**: **완전 통과 (COMPLETE)**
- **차기 단계 권고**: 다음 권역인 **`EX-06 — Avignon / Pont du Gard / Arles Execution Sync (Days 19–23)`** (Luberon ➔ Avignon 체크인, 교황청/성벽, Uzès & Pont du Gard 차량 이동, Arles 유럽문화유산의 날(JEP) 철도 당일치기, Avignon TGV역 렌터카 반납 및 TGV 12176 탑승) 착수를 권고합니다.
- 지침에 따라 자동으로 진행하지 않고 대기합니다.

