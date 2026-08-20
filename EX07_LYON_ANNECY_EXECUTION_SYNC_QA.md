# Phase EX-07 QA Report: Lyon & Annecy Execution Synchronization (Days 24–27)

**작성일**: 2026-08-20  
**프로그램**: SP-FR Guidebook Execution Synchronization Program (EX-00 ~ EX-14)  
**단계**: **EX-07 — Lyon & Annecy Execution Synchronization (Days 24–27)**  
**상태**: **PASS**

---

## 1. Overall Verdict: **PASS (Days 24–27 Fully Synchronized & Verified)**

- **적용 범위**: Day 24 ~ Day 27 (Lyon Fourvière/Vieux Lyon/부숑, Croix-Rousse 실크언덕/폴보퀴즈시장/테트도르공원, Annecy 알프스 호수 철도 당일치기, Lyon ➔ Paris TGV 6618 이동 및 15구 15박 정착)
- **핵심 동기화 성과**:
  1. **언덕 수직 이동 부하 완벽 제어**: Fourvière(Day 24)와 Croix-Rousse(Day 25)를 분리하고, **푸니쿨라 F2 및 메트로 C선을 통해 언덕 정상으로 상행 후 완만한 정원/트라불 하산 동선**을 채택하여 무릎/체력 부하 최소화.
  2. **Day 26 Annecy 알프스 호수 철도 당일치기 정밀화**: Part-Dieu역 직통 TER(08:08 ➔ 10:06 / 귀환 17:53 ➔ 19:52)을 축으로 튜 운하, 팔레 드 릴, 사랑의 다리, 유럽 정원 및 사부아 점심을 완벽 연결.
  3. **Day 27 Lyon ➔ Paris TGV 6618 확정 앵커 정렬**: **`TGV 6618 (13:04 Lyon Part-Dieu ➔ 15:00 Paris Gare de Lyon 확정 X6CVW5, 1등석)`** 탑승 후 파리 15구(78 Rue de Lourmel) 체크인 및 15박 생활권 장보기 완충 수립.
  4. **EX-06 Day 23 환승 완충 수식 보정 완료**: 08:55 반납 ➔ 10:22 탑승 간 총 87분의 Gross Buffer (20분 역내 이동 공제 시 67분 Net 플랫폼 대기 완충)로 일치화.
- **검증 게이트**: 4대 표준 검증 스크립트 전원 **100% PASS** (Content Loss = 0)

---

## 2. Scope & Baseline

- **대상 일차**: Days 24–27 (4개 일차, 리옹 거점 4박 중 후반 3일 및 파리 진입일)
- **숙소 앵커**:
  - Lyon: `Lagrange Aparthotel Lyon Lumière (81-85 Cours Albert Thomas, 확정 5882.730.884, 9/24 11:00 체크아웃)`
  - Paris: `78 Rue de Lourmel, 75015 Paris (확정, 9/24 15:00 체크인 ~ 10/9 11:00 체크아웃, 15박 거주)`
- **교통 앵커**:
  - Lyon TCL: Metro D선 (Monplaisir ↔ Vieux Lyon), Funicular F2 (Vieux Lyon ↔ Fourvière), Metro C선 (Hôtel de Ville ↔ Croix-Rousse)
  - Annecy TER: `SNCF TER Lyon Part-Dieu ↔ Annecy (1시간 58분 소요)`
  - Paris TGV: `TGV INOUI 6618 Part-Dieu 13:04 ➔ Paris Gare de Lyon 15:00 (1등석 확정 X6CVW5)`

---

## 3. EX-06 Buffer Minor Correction (선행 보정 완료)

- **Day 23 반납 ➔ 열차 완충 명확화**:
  ```text
  08:55 Hertz 렌터카 반납 완료 ➔ 10:22 TGV INOUI 12176 출발
  총 소요 시간 간격: 87분 (Gross Buffer)
  역사 진입 및 플랫폼 접근 여유: -20분
  순수 플랫폼 대기 안전 완충: 67분 (Net Safety Buffer)
  ```
- `EX06_AVIGNON_PONT_DU_GARD_ARLES_EXECUTION_SYNC_QA.md` 및 `day-23.json`에 동일하게 정정 반영 완료.

---

## 4. Day 24 Final Timeline — Fourvière & Vieux Lyon & 정통 부숑

```text
[Day 24 Execution Chain]
08:30 숙소(Lagrange Lumière) 출발 ➔ 메트로 D선 (Monplaisir ➔ Vieux Lyon)
 ➔ [Stop 1] Funicular F2 푸니쿨라 상행 (08:45~09:00, 수직고도 120m 5분 극복)
 ➔ [Stop 2] Basilique Notre-Dame de Fourvière & 로마극장 (09:00~11:00, 2시간)
    * 대성당 내부 모자이크, 파노라마 전망대(리옹 도심·벨쿠르·몽블랑 뷰), 기원전 15년 로마 대극장
 ➔ [도보 하산] ➔ [Stop 3] Jardin du Rosaire 완만한 정원길 하산 (11:00~11:45, 무릎 부하 최소화)
 ➔ [Stop 4] Vieux Lyon 르네상스 비스트로 점심 (12:00~13:30)
 ➔ [Stop 5] Vieux Lyon & Traboules (13:30~15:30, 2시간)
    * 생장 대성당, Passage de la Tour Rose, 54 Rue Saint-Jean 등 공공 개방 트라불 도보
 ➔ [Stop 6 (선택)] Saône 강변 & Passerelle Saint-Georges 인도교 산책 (15:45~17:15)
 ➔ [메트로 D선] ➔ [Stop 7] 정통 부숑 만찬 (Daniel & Denise) & 숙소 귀환 (19:00~21:30)
```

### A. 미식 부숑(Bouchon) 경험
- 리옹의 전통 어머니 요리사(Mères Lyonnaises) 전통을 잇는 공인 부숑 `Daniel & Denise`에서 파테 앙 크루트, 퀘넬 드 브로셰, 타블리에 드 사푀르 만찬.

---

## 5. Day 25 Final Timeline — Croix-Rousse 실크 언덕 & 폴 보퀴즈 시장 & 테트도르 공원

```text
[Day 25 Execution Chain]
08:30 숙소 출발 ➔ 메트로 D선 + 메트로 C선 (Hôtel de Ville ➔ Croix-Rousse 플라토 정상 상행)
 ➔ [Stop 1] Marché de la Croix-Rousse 화요 로컬 시장 탐방 (08:30~10:00)
 ➔ [Stop 2] Le Mur des Canuts (유럽 최대 트롱프뢰유 벽화) & 실크 직공 트라불 (10:00~12:00, 2시간)
    * 카뉘(Canuts) 작업실 거리 ➔ Cour des Voraces 6층 석조 계단 트라불을 통해 완만하게 하산
 ➔ [메트로 C+B선 20분] ➔ [Stop 3] Les Halles de Lyon Paul Bocuse & 미식 점심 (12:30~14:30)
    * Mère Richard 생 마르슬랭 치즈, Sibilia 샤퀴테리 탐방 & 시장 내 굴/해산물 점심
 ➔ [도보 18분] ➔ [Stop 4] Parc de la Tête d'Or (황금머리 공원 호수·장미원 산책, 15:00~17:30)
 ➔ [메트로 B+D선 20분] ➔ [Stop 5] 숙소 복귀 & 익일 Annecy 당일치기 준비 (18:00~20:00)
```

### A. Croix-Rousse 언덕 부하 제어
- 가파른 경사를 걸어 올라가지 않고 **메트로 C선을 타고 플라토 정상(Croix-Rousse역)으로 먼저 상행**한 후, 벽화와 Cour des Voraces 트라불을 거쳐 **내리막으로 하산**하는 스마트 동선 수립.

---

## 6. Day 26 Final Timeline — Annecy Rail Day Trip

```text
[Day 26 Execution Chain]
07:30 숙소 출발 ➔ 메트로 D+B선 Part-Dieu역 이동
 ➔ 08:08~10:06 [TER 직통 1시간 58분] ➔ Annecy역 도착 [Backup: 09:08]
 ➔ [도보 5분] ➔ [Stop 1] Annecy Vieille Ville & Palais de l'Île (10:15~12:30, 2시간 15분)
    * 튜(Thiou) 운하, 12세기 수상 감옥 요새, Rue Sainte-Claire 아케이드 파스텔 골목
 ➔ [Stop 2] 사부아(Savoy) 로컬 점심 (타르티플레트/호수 생선, 12:30~14:00)
 ➔ [Stop 3] Lac d'Annecy & Pont des Amours & Jardins de l'Europe (14:15~16:45, 2시간 30분)
    * 알프스 설산 호숫가, 사랑의 다리, 유럽 정원 거목 산책로 (선택: 1시간 호수 크루즈)
 ➔ 17:53~19:52 [TER 직통 1시간 58분] ➔ Lyon Part-Dieu역 복귀 [Backup: 18:53]
 ➔ [Stop 4] 숙소 복귀 & 익일 Day 27 Paris 이동 짐 정리 (20:15~21:30)
```

### A. 알프스 호수 & 날씨 Plan B
- **정상 운영**: 호숫가 잔디밭(Le Pâquier) 및 사랑의 다리 산책 + 호수 유람선.
- **우천 Plan B**: 호수 크루즈를 생략하고 샤토 디아느시(Château d'Annecy) 성채 박물관 관람 및 구시가지 아케이드 카페 휴식으로 전환.

---

## 7. Day 27 Final Timeline — Lyon ➔ Paris TGV 6618 & 15박 정착

```text
[Day 27 Execution Chain]
09:30~11:15 Lagrange Aparthotel Lyon Lumière 체크아웃 & Part-Dieu역 이동 (택시 15분)
 ➔ [Stop 1] Part-Dieu역 카페 점심 & TGV 플랫폼 대기 (11:30~12:45)
 ➔ 13:04~15:00 [TGV INOUI 6618 1등석, 1시간 56분] ➔ Paris Gare de Lyon 도착 (확정 X6CVW5)
 ➔ [택시 35분, 7.5km] ➔ [Stop 2] Paris 15구 숙소 체크인 (78 Rue de Lourmel, 15:30~17:30)
    * 15박 장기 체류 짐 풀기, 세탁기/주방/Wi-Fi 시설 점검
 ➔ [도보 5분] ➔ [Stop 3] 15구 생활권 첫 장보기 & 에펠탑 방향 산책 (17:45~19:30)
    * Monoprix Lourmel 식재료 구매 및 Rue du Commerce / Champ de Mars 800m 산책
 ➔ [Stop 4] 동네 비스트로 저녁 또는 숙소 첫 식사 & 15박 거주 시작 (19:45~21:30)
```

---

## 8. 정본 참조(Place Reference) 무결성 정비

- `fourviere` ➔ `fourviere` (1:1 바인딩)
- `vieux-lyon` ➔ `vieux-lyon` (1:1 바인딩)
- `croix-rousse-market` ➔ `croix-rousse` (1:1 바인딩)
- `croix-rousse-slopes` ➔ `croix-rousse` (1:1 바인딩)
- `halles` ➔ `halles-de-lyon-paul-bocuse` (1:1 바인딩)
- `tete-dor` ➔ `parc-de-la-tete-d-or` (1:1 바인딩)
- `vieille-ville` ➔ `annecy` (1:1 바인딩)
- `lakefront` ➔ `annecy` (1:1 바인딩)

---

## 9. Feasibility Metrics 결과

```text
============================================================
           EX-07 POST-SYNC FEASIBILITY METRICS
============================================================
Synchronized Scope                  : Days 24–27 (Lyon, Annecy, Paris Transfer)
Total Days Audited                  : 43
Grade Distribution:
  - Grade A (Comfortable)           : 14 (32.6%)
  - Grade B (Realistic)             : 21 (48.8%) [Days 24, 25, 26, 27 모두 Grade B 달성]
  - Grade C (Tight but Feasible)    : 8  (18.6%)
  - Grade D / F                     : 0  (0.0%)

Feasibility Issue Register:
  - P0 (Critical Conflict)          : 0
  - P1 (High Risk Conflict)         : 0
  - P2 (Optimization Backlog)       : 8 (Day 25 Croix-Rousse duration underallocation 해결 완료)
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

- [data/daily-cards/day-24.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/data/daily-cards/day-24.json) (푸니쿨라 F2, 로제르 정원 하산, 트라불, Daniel et Denise 부숑)
- [data/daily-cards/day-25.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/data/daily-cards/day-25.json) (메트로 C선 상행, Canuts 벽화, 폴 보퀴즈 시장 점심, 테트도르 공원)
- [data/daily-cards/day-26.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/data/daily-cards/day-26.json) (안시 TER 08:08/17:53 직통, 튜 운하, 알프스 호수, 사부아 점심)
- [data/daily-cards/day-27.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/data/daily-cards/day-27.json) (TGV 6618 13:04 확정, 파리 15구 78 Rue de Lourmel 15박 체크인)
- [EX06_AVIGNON_PONT_DU_GARD_ARLES_EXECUTION_SYNC_QA.md](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX06_AVIGNON_PONT_DU_GARD_ARLES_EXECUTION_SYNC_QA.md) (Day 23 87분 Gross/67분 Net 완충 보정)
- [scripts/sync_days_24_27.py](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/scripts/sync_days_24_27.py) (신규 생성)
- [EX07_LYON_ANNECY_EXECUTION_SYNC_QA.md](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX07_LYON_ANNECY_EXECUTION_SYNC_QA.md) (신규 생성)

---

## 12. 차기 단계 권고사항 (Recommendation for EX-08)

- **EX-07 판정**: **완전 통과 (COMPLETE)**
- **차기 단계 권고**: 다음 권역인 **`EX-08 — Paris 15-Day Long-Stay Execution Synchronization (Days 28–42)`** (파리 15구 생활권 적응, 박물관 시간지정 예약 잠금, 파리 패션위크 공개동선, 센강/좌안/우안 도보 축, 오르세/퐁피두/루브르/피카소 미술관 정밀 동기화) 착수를 권고합니다.
- 지침에 따라 자동으로 진행하지 않고 대기합니다.

