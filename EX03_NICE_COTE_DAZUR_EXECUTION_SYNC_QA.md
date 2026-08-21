# Phase EX-03 QA Report: Nice & Côte d'Azur Execution Synchronization (Days 8–11) [Revision]

**작성일**: 2026-08-20  
**프로그램**: SP-FR Guidebook Execution Synchronization Program (EX-00 ~ EX-14)  
**단계**: **EX-03 — Nice & Côte d'Azur Execution Synchronization (Days 8–11) [Mandatory Stop Expansion]**  
**상태**: **PASS**

---

## 1. Overall Verdict: **PASS (Days 8–11 Revised & Fully Synchronized)**

- **적용 범위**: Day 8 ~ Day 11 (Nice 시내, Antibes + Cannes, Villefranche-sur-Mer + Èze Village + Monaco + Menton, Nice 생활/회복 및 렌터카 준비)
- **핵심 개정 사항**:
  1. **Day 9 개정**: `Nice ➔ Cannes ➔ Nice` 단독 일정에서 **`Nice ➔ Antibes ➔ Cannes ➔ Nice`**로 개편하여 **Antibes를 필수 방문지(Mandatory Stop)**로 완전 편입.
  2. **Day 10 개정**: `Nice ➔ Monaco ➔ Menton ➔ Nice` 일정에서 **`Nice ➔ Villefranche-sur-Mer ➔ Èze Village ➔ Monaco ➔ Menton ➔ Nice`**로 전면 재설계하여 **4개 도시 모두 필수 방문지(Mandatory Stop)**로 완전 편입.
  3. **교통 모드 정밀 분리**: TER 철도 구간, Zou! / Lignes d'Azur 버스 구간(Bus 602/82/83), 도보 및 공공 수직 엘리베이터(Ascenseurs publics) 구간을 명확히 분리하여 렌더링 및 실행 정합성 확보.
- **검증 게이트**: 4대 표준 검증 스크립트 전원 **100% PASS** (Content Loss = 0)

---

## 2. Scope & Baseline

- **대상 일차**: Days 8–11 (4개 일차, 니스 거점 5박 중 4일)
- **숙소 앵커**: `Nice Palais ALZIRA, 12 Rue Verdi (확정 Airbnb [CONFIRMED], 9/4 18:00 체크인 ~ 9/9 11:00 체크아웃)`
- **교통망 앵커**:
  - SNCF TER 철도망: Nice-Ville ↔ Antibes (18분), Antibes ↔ Cannes (12분), Nice-Ville ↔ Villefranche (7분), Monaco ↔ Menton (11분), Menton ↔ Nice-Ville (35분)
  - Zou! 버스 602번 / Lignes d'Azur 버스 82·83번: Villefranche ➔ Èze Village (20분), Èze Village ➔ Monaco Place d'Armes (20분)

---

## 3. Day 9 Sync — Antibes Mandatory Inclusion & Cannes 재구성

```text
[Day 9 Execution Chain]
Nice 숙소(12 Rue Verdi) 출발 (08:00)
 ➔ Nice-Ville역 (08:15) ➔ [TER 18분] ➔ Gare d'Antibes (08:42)
 ➔ Vieil Antibes & Marché Provençal (08:45~11:15, 2.5시간 compact visit)
 ➔ Gare d'Antibes (11:20) ➔ [TER 12분] ➔ Gare de Cannes (11:42)
 ➔ Marché Forville & Vieux-Port 해산물 점심 (11:55~14:00)
 ➔ Le Suquet 구시가지 언덕 전망대 (14:00~15:15)
 ➔ Boulevard de la Croisette & 팔레 데 페스티발 (15:30~16:45)
 ➔ Gare de Cannes (16:45) ➔ [TER 30분] ➔ Nice-Ville (17:30) ➔ 숙소 귀환 (18:00)
```

### A. Antibes Integration & TER Feasibility
- **체류 목표**: 08:45~11:15 (2시간 30분 compact visit).
- **동선**: 앙티브역 ➔ Avenue Robert Soleau ➔ 구시가지 중심(Rue de la République) ➔ **Marché Provençal (Cours Masséna, 06:00~13:00 운영, 09:00~10:30 활성화 시간대 적기 방문)** ➔ 성벽길(Promenade Amiral de Grasse) ➔ 피카소 미술관(Château Grimaldi) 외관 ➔ 포르 보방(Port Vauban) 조망 ➔ 역 복귀.
- **시장 비교**: 앙티브의 프로방스 시장(Marché Provençal)은 아침 활성화 시간대에 방문하고, 칸 포르빌 시장(Marché Forville)은 12시 전후 점심 연계로 자연스럽게 관찰하도록 동선을 분리하여 두 시장의 충돌을 방지함.

---

## 4. Day 10 Sync — Villefranche + Èze + Monaco + Menton 4개 도시 연계 재설계

```text
[Day 10 Execution Chain]
Nice 숙소 출발 (08:00) ➔ Nice-Ville역 ➔ [TER 7분] ➔ Gare de Villefranche-sur-Mer (08:32)
 ➔ [Stop 1] Villefranche-sur-Mer 구시가지 & 콰이 쿠르베 (08:40~10:00, 75분)
 ➔ [Bus 20분] ➔ [Stop 2] Èze Village 중세 절벽마을 & 이국적 정원 (10:30~12:15, 105분)
 ➔ [Zou! Bus 602 20분] ➔ [Stop 3] Monaco Port Hercule & 라 콘다민 시장 점심 (12:45~13:45)
 ➔ [공공 엘리베이터 상행] ➔ [Stop 4] Le Rocher / 대공궁 광장·대성당 (14:00~15:30, 90분)
 ➔ Monaco역 (15:40) ➔ [TER 11분] ➔ Gare de Menton (15:56)
 ➔ [Stop 5] Menton 구시가지·바질리크 생미셸·사블레트 해변 황금빛 전경 (16:00~18:30)
 ➔ [Stop 6] Menton 구항구 저녁 식사 — Le Petit Port (18:30~20:00)
 ➔ Gare de Menton (20:15) ➔ [TER 35분] ➔ Nice-Ville (20:55) ➔ 숙소 귀환 (21:00)
```

### A. Villefranche-sur-Mer Integration (Stop 1)
- **교통**: Nice-Ville역에서 TER로 단 1정거장, 7분 소요. 기차역이 해변(Plage des Marinières) 바로 앞에 위치하여 즉시 보행 진입 가능.
- **동선 (75분)**: 콰이 쿠르베(Quai Courbet) 해안로 ➔ 13세기 지하 아치 골목인 **Rue Obscure** ➔ 생피에르礼배당(장 콕토 벽화) 외관 ➔ 16세기 생텔름 성채(Citadelle Saint-Elme) 조망.

### B. Èze Village 접근 및 고도차 극복 (Stop 2)
- **교통 검증**: 해안가 Èze-sur-Mer역에서 절벽 마을(Èze Village, 해발 429m)로 올라가는 니체 트레일(Sentier Nietzsche)은 급경사로 60분 이상 소요되어 4개 도시 일정에서 체력 소모가 극심함.
- **공식 대중교통 채택**: Villefranche / Beaulieu에서 버스 82번/83번을 탑승하여 **Èze Village 입구 버스 정류장(Place du 8 Mai 1945)**으로 직접 이동(20분 소요).
- **체류 (105분)**: 중세 돌골목 ➔ **Jardin Exotique (이국적 정원)** 정상에서 생장캅페라 반도와 지중해 360도 절벽 파노라마 조망.

### C. Èze ➔ Monaco 직결 연결 (Stop 3 & 4)
- **교통 검증**: Èze Village 버스 정류장에서 Zou! **Bus 602번**을 탑승하면 해안으로 내려갈 필요 없이 모옌 코르니슈를 따라 **Monaco Place d'Armes(르 로셰 진입로)**까지 직통 20분 만에 도착.
- **Monaco 압축**: 몽테카를로 카지노 외곽 지역을 생략하고, 라 콘다민 시장/포르 에르퀼 점심 ➔ 공공 엘리베이터 상행 ➔ **Le Rocher (Monaco-Ville, 대공궁 광장·대성당·클리프 전망대)**에 90분 집중.

### D. Monaco ➔ Menton & Sunset Dinner (Stop 5 & 6)
- **교통**: 모나코역에서 TER 열차로 11분 만에 Gare de Menton 도착.
- **동선**: 멘통역 ➔ 오귀스트 카르펜티에 거리 ➔ **Basilique Saint-Michel (생 미셸 대성당 & 자갈 모자이크 광장)** ➔ **Les Rampes Saint-Michel (지그재그 바로크 계단)** ➔ **Plage des Sablettes (17:00~18:30 황금빛 일몰 시간대 파스텔 구시가지 전경)**.
- **저녁 식사**: 구항구의 테라스 레스토랑(Le Petit Port)에서 18:30~20:00 지중해 해산물 저녁 식사 후 20:15 TER로 니스 귀환.

---

## 5. Drop Levers (지연 시 단계별 결정 규칙)

4개 도시를 모두 방문하는 기본 일정을 보호하기 위해, 지연 발생 시 도시를 삭제하는 대신 **도시 내부의 부속 활동을 순차 압축**하는 3단계 레버 확립:

```text
[NORMAL PLAN]
- Villefranche(75분) + Èze(105분) + Monaco(90분) + Menton(150분 + 저녁 식사) = 4개 도시 완벽 완주

[DELAY COMPRESSION (30분 이상 지연 시)]
- Option 1: Èze Village에서 이국적 정원 내부 입장을 생략하고 마을 골목 전망대만 관람 (-30분).
- Option 2: Monaco에서 몽테카를로 완전 제외, Le Rocher 단일 집중 (-30분).
- Option 3: Menton 저녁 식사를 생략하고 사블레트 해변 산책 후 18:30 TER로 니스 조기 귀환 (-90분).

[EMERGENCY FALLBACK (철도 파행 / 극심한 악천후)]
- Èze 및 Menton을 생략하고 Monaco 해양박물관 중심 실내 전환 후 15:00 니스 복귀.
```

---

## 6. Stop Classification 정비 (Non-canonical Visit Stop 도입)

실제 필수 관광지인 `antibes-old-town`, `villefranche-sur-mer`, `eze-village`를 단순 호텔/환승과 같은 Operational Exception으로 취급하지 않고, **`NON_CANONICAL_VISIT_STOP`**으로 명확히 분류하여 데이터 모델의 투명성 확보.

```text
- CANONICAL_VISIT_STOP    : 77개 (cours-saleya, vieux-nice, colline-du-chateau, marche-forville, le-suquet, le-rocher, menton, marche-de-la-liberation, promenade-des-anglais 등)
- NON_CANONICAL_VISIT_STOP: 27개 (antibes-old-town, villefranche-sur-mer, eze-village, cadaques, tossa, croisette, port-lympia, port-hercule, charles-negre 등)
- OPERATIONAL EXCEPTIONS  : ACCOMMODATION (79), MEAL (24), TRANSPORT (20), REST (4), EXERCISE (3), BOOKING_EVENT (2), OTHER (4)
- TOTAL STOPS             : 240개 (결손 0개)
```

---

## 7. Day 8~11 현실성 등급 및 신체 부하 전후 비교

| Day | 일자 | 테마 | 변경 전 등급 | 변경 후 등급 | 신체 부하 | 평가 코멘트 |
|---|---|---|:---:|:---:|:---:|---|
| **8** | 9/5 토 | Nice 시장·구시가지·성채 언덕 | A | **A** | Moderate (5) | 엘리베이터 상행 명시로 피로 최소화, 여유로운 니스 적응일 |
| **9** | 9/6 일 | 앙티브 요새마을 + 칸 당일치기 | B | **B** | Moderate (6) | 앙티브 2.5시간 + 칸 4시간의 균형 잡힌 TER 일정 |
| **10** | 9/7 월 | 빌프랑슈·에즈·모나코·망통 4개 도시 | C | **C** | Heavy (7) | 4개 도시 연계로 밀도는 높으나 버스 602 직결 및 완충 수립으로 현실성 확보 |
| **11** | 9/8 화 | Nice 회복·렌터카 준비 | A | **A** | Light (3) | 리베라시옹 시장 및 세탁·해변 휴식, 익일 렌터카 준비 완충 완벽 보호 |

---

## 8. 검증 게이트 (Validation Results)

1. `validate_place_canonical_model.py`: **ALL GATES PASSED** (102 Canonical Places 완벽 보호)
2. `build/site.py`: **PASS** (337쪽 정상 빌드 완료)
3. `build/ux_check.py`: **PASS** (UX 표준 100% 통과)
4. `build/content_audit.py`: **PASS** (Content Loss = 0)

---

## 9. 생성 및 수정된 파일

- [data/daily-cards/day-09.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/data/daily-cards/day-09.json) (Antibes mandatory stop 반영 및 타임라인 완비)
- [data/daily-cards/day-10.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/data/daily-cards/day-10.json) (Villefranche, Eze Village, Monaco, Menton 4개 도시 연계 및 버스 602 동선 완비)
- [source/CURRENT/10_Core/03_Whole_Trip_Master_Itinerary_v1.2.md](file:///mnt/c/Users/NB-24021500/source/CURRENT/10_Core/03_Whole_Trip_Master_Itinerary_v1.2.md) (Day 9, Day 10 마스터 일정표 동기화)
- [source/OPERATIONS/100_Whole_Trip_43_Day_Execution_Audit_v1.0.md](file:///mnt/c/Users/NB-24021500/source/OPERATIONS/100_Whole_Trip_43_Day_Execution_Audit_v1.0.md) (Day 9, Day 10 실행 감사표 동기화)
- [scripts/ex00_baseline_audit.py](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/scripts/ex00_baseline_audit.py) (NON_CANONICAL_VISIT_STOP 분류 체계 반영)
- [scripts/apply_ex03_revision.py](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/scripts/apply_ex03_revision.py) (신규 생성)
- [EX03_NICE_COTE_DAZUR_EXECUTION_SYNC_QA.md](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX03_NICE_COTE_DAZUR_EXECUTION_SYNC_QA.md) (전면 갱신)

---

## 10. 차기 단계 권고사항 (Recommendation for EX-04)

- **EX-03 Revision 판정**: **완전 통과 (COMPLETE)**
- **차기 단계 권고**: 다음 권역인 **`EX-04 — Aix & Marseille Execution Sync (Days 12–15)`** (Nice ➔ Saint-Paul ➔ Grasse ➔ Aix 렌터카 이동일 최적화, 엑스 도보, 마르세유 대중교통 L50 당일치기) 착수를 권고합니다.
- 지침에 따라 자동으로 진행하지 않고 대기합니다.

