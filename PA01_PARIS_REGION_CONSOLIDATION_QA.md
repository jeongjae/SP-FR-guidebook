# PA01 / PA01F — Paris Long Stay Region Editorial Re-Consolidation & Factual Reconciliation QA Report

---

## 1. Overall Status

- **상태**: **PASS (Factual Reconciliation & 8개 지역 회귀 검증 완료)**
- **대상 지역**: `paris` (Paris Long Stay, Chapter 11)
- **적용 스키마**: `rc-region-v1`
- **핵심 성과**:
  - **Musée d'Orsay DEC-A12와 Day 39 SOT 충돌 완전 해소**: Day 32(9/29) 상설 3.5시간 집중 관람과 Day 39(10/6) <Mary Cassatt> 특별전 개막일 2회차 집중 관람을 DEC-A12, Day SOT, Region Schedule, Place Classification 전반에 걸쳐 100% 일치 정합.
  - 마레 지구 연계 일정(Picasso, Carnavalet, 보주 광장)을 Day 39 오후 선택/연계 일정으로 보존하여 임의 삭제 없이 완벽 통합.
  - 15구 생활권(78 Rue de Lourmel) 거점의 일상 루틴 허브화 및 기획 잔재 분리 보존 완료.
  - Paris Transport 섹션(Navigo Weekly 9/28~10/4 1회, 개별권 전략, 요금 수준, Versailles 포함범위, CDG 택시) 100% 현 상태 유지 (Regression = 0).
  - 10개 빌드 및 QA 스위트 전수 PASS (원고 흔적 가드: 전체 8개 지역 원고 흔적 0 달성, pytest 30 passed).

---

## 2. Latest main SHA / Starting Condition

- **Base `origin/main` SHA**: `6e62189e` (`Merge pull request #215 from jeongjae/fix/lyon-region-editorial-consolidation`)
- **작업 브랜치**: `fix/paris-region-editorial-consolidation`

---

## 3. Paris Actual Stay Dates and Nights

- **체류 기간**: 2026-09-24(목) ~ 2026-10-09(금)
- **총 숙박 일수**: **15박 16일**
- **체류 일차**: Day 27 ~ Day 42 (Day 43은 귀국/ICN 도착일로서 `post-Paris return handoff`로 분리)
- **도착**: Day 27 (9/24 목) 15:00 Gare de Lyon 도착 ➔ 15구 숙소 체크인
- **출국**: Day 42 (10/9 금) 11:00 체크아웃 ➔ 14:00 이전 공식 택시로 CDG Terminal 1 이동 ➔ 19:10 OZ502 탑승

---

## 4. Confirmed Lodging Reconciliation

- **확정 숙소**: **78 Rue de Lourmel, 75015 Paris**
- **생활권**: 파리 15구 Convention / Lourmel / Commerce 생활권
- **교통 접근성**: 메트로 8호선(Lourmel, Commerce), 10호선(Avenue Émile Zola), 6호선(La Motte-Picquet - Grenelle)
- **생활 인프라**: Boulangerie Pichard (아티장 빵집), Marché Convention (화·목·일 노천시장)
- **과거 후보 정리**: 5구/7구/13/14구 비교표 및 WeHost 수수료 분석은 아카이브(`11_Paris_Planning_Residue_v1.0.md`)로 분리.

---

## 5. Complete Day-by-Day SOT Reconciliation

| Date | Day | Morning Routine | Afternoon Anchor | Evening | Actual / Optional | Reservation | Event / Theme |
|---|---:|---|---|---|---|---|---|
| **9/24 목** | 27 | Lyon 체크아웃 & TGV 이동 | Paris 15구 숙소 체크인 (15박 정착) | 15구 첫 장보기 & 숙소식 | Actual | TGV INOUI 6618 / 숙소 | 파리 입성 및 정착 |
| **9/25 금** | 28 | 숙소 아침 & 아침 운동 | Tootbus 시티투어 풀 루프 & Grand Palais 세잔전 | Café du Commerce 브라세리 저녁 | Actual | Grand Palais 세잔전 | 가을 특별전 개막 |
| **9/26 토** | 29 | 15구 토요 장보기 & 루틴 | Musée du Luxembourg 워홀전 & 뤽상부르 & 생제르맹 | 15구 숙소 귀환 & 저녁 | Actual | Luxembourg 워홀전 | 좌안 지성 산책 & 노트르담 외관 |
| **9/27 일** | 30 | Marché Convention 일요 장보기 | Musée de l'Orangerie (수련) & 튀일르리 & 팔레 루아얄 | Bouillon Chartier Montparnasse 저녁 | Actual | Orangerie 수련 | 고전 파리 & 오페라 외관 |
| **9/28 월** | 31 | 숙소 아침 & 출발 준비 | Musée Gustave Moreau & 9구 누벨 아테네 & 마레 지구 | 15구 숙소 귀환 & 저녁 | Actual | Moreau 상설 | Paris Fashion Week 개막 분위기 |
| **9/29 화** | 32 | Art-Heavy 빠른 아침 | Musée d'Orsay 3.5시간 집중 관람 & Musée Rodin | Café du Commerce 저녁 | Actual | Orsay 09:30 슬롯 | 인상주의 1회차 & 앵발리드 외관 |
| **9/30 수** | 33 | 단축 아침 & 출발 준비 | Petit Palais & 몽테뉴 거리 & Palais de Tokyo | 15구 숙소 귀환 & 저녁 | Actual | Petit Palais 무료 | Fashion Week 서부 축 |
| **10/1 목** | 34 | 숙소 출발 ➔ RER C 이동 | Château de Versailles (본관 10:00) & 대정원 & 트리아농 | Le Grand Pan 비스트로 저녁 | Actual | Versailles 10:00 여권권 | 베르사유 전일 투어 |
| **10/2 금** | 35 | 숙소 아침 & 점심 준비 | Musée du Louvre 마스터피스 4시간 집중 관람 | 센 강변 일몰 산책 & 숙소식 | Actual | Louvre 사전지정 | 루브르 명작 관람 |
| **10/3 토** | 36 | 15구 토요 장보기 & 루틴 | Musée Marmottan Monet (<인상, 해돋이>) & 파시 산책 | 15구 조기 귀환 & 휴식 | Actual | Marmottan 상설 | 모네 명작 & 경마 전야 휴식 |
| **10/4 일** | 37 | 숙소 출발 ➔ 롱샹 셔틀 | Qatar Prix de l'Arc de Triomphe (개선문상 본선) | 15구 숙소 귀환 & 저녁 | Actual | Arc 본선 티켓 | 세계 최고 권위 잔디 경마 축제 |
| **10/5 월** | 38 | 경마 후 늦은 기상 & 세탁 | Musée Jacquemart-André & 몽소 공원 산책 | 15구 숙소 귀환 & 저녁 | Actual | Jacquemart 상설 | 경마 후 회복 & 저택 박물관 |
| **10/6 화** | 39 | Marché Convention 화요 장보기 | Musée d'Orsay <Mary Cassatt> 특별전 개막 & 마레 지구 | 15구 숙소 귀환 & 저녁 | Actual | Orsay Cassatt 14:00 | 카사트 회고전 2회차 & 마레 연계 |
| **10/7 수** | 40 | 단축 아침 & 출발 준비 | Bourse de Commerce (피노 컬렉션) & 몽마르트르 포도축제 | 15구 숙소 귀환 & 저녁 | Actual | Bourse 11:00 슬롯 | 피노 컬렉션 개막 & 포도축제 |
| **10/8 목** | 41 | Art-Heavy 빠른 아침 | Musée Guimet & Musée d'Art Moderne (MAM) | 트로카데로 일몰 & Le Grand Pan | Actual | Guimet 상설 | 아시아/현대미술 & 고별 만찬 |
| **10/9 금** | 42 | 최종 짐 정리 & 체크아웃 | Café du Commerce 점심 & 공식 택시 CDG 이동 | OZ502 탑승 (19:10 발) | Actual | OZ502 항공권 | 파리 15박 완료 및 출국 |
| *(10/10 토)* | *43* | *기내 수면 & 시차 적응* | *14:10 인천공항(ICN) 제1터미널 도착 (Post-Paris Handoff)* | *자택 귀환* | *Actual* | *ICN 도착* | *43일 대여정 공식 완결* |

---

## 6. “오전 생활 / 오후 외출” Coverage

- **생활 루틴 구현**: Paris 체류 전반에 걸쳐 숙소 아침, 인근 빵집(Boulangerie Pichard 등), 장보기(Marché Convention 등), 운동·산책과 housekeeping을 반복하는 생활 루틴을 안정적으로 유지합니다.
- **오후 외출 커버리지**: 15박 전체 중 단 하루의 공백 없이 매일 명확한 핵심 문화/도시 앵커가 배치됨 (누락 = 0).

---

## 7. Dates with Legitimate Exceptions

- **Day 27 (9/24 목)**: Lyon→Paris 이동 및 15박 숙소 체크인·정착일 (오후: 생활권 첫 장보기 & 동네 파악).
- **Day 34 (10/1 목)**: Château de Versailles 전일 근교 투어 (RER C선 왕복, 09:30~17:00).
- **Day 37 (10/4 일)**: Qatar Prix de l'Arc de Triomphe 파리롱샹 전일 스포츠 축제.
- **Day 42 (10/9 금)**: 15구 체크아웃, 마지막 점심 및 CDG 공항 출국일 (오후: 14:00 이전 공항 이동).

---

## 8. Overview Before / After

- **Before**: 4개의 분산된 철학 블록(`이 체류의 역할`, `Jason·Julia 맞춤 원칙`, `15개 미술관과 도시의 유기적 결합`, `세 개의 파리`, `왜 이 설계가 옳은가`, `디자인 메모` 등 총 120여 줄의 기획 문장).
- **After**: `Paris에서 15박을 이렇게 보낸다` 단일 H2 아래 15박의 핵심 3대 가치(생활하는 Paris, 오후의 문화 일정, 특별한 날)를 2-3개 단락으로 압축.

---

## 9. Schedule Before / After

- **Before**: 장소별 Day 표, 5열 일정 배분표, 오페라 패키지 표, 주간 리듬 표 등 4개의 중복된 일정표 혼재.
- **After**: 9/24 도착일부터 10/9 출국일까지 15박 핵심 일정을 담은 **단일 2열 일정표 1개**로 정규화 (Day 43은 귀국 handoff로 분리).

---

## 10. Museum Actual / Optional / Archive Classification

- **Actual Cards**: Grand Palais, Musée du Luxembourg, Musée de l'Orangerie, Musée Gustave Moreau, Musée d'Orsay, Musée Rodin, Petit Palais, Château de Versailles, Musée du Louvre, Musée Marmottan Monet, Musée Jacquemart-André, Musée Picasso Paris, Musée Carnavalet, Bourse de Commerce, Musée Guimet, Musée d'Art Moderne de Paris (MAM).
- **Optional / Reference**: BnF Richelieu (우선추천), Giverny (우선추천/근교선택).
- **Archive / Notice**: Centre Pompidou (2025~2030 전면 개보수 폐관 안내), Jenny Holzer (10/20 개막으로 체류 후 제외), Fondation Louis Vuitton (10/9 개막으로 제외).

---

## 11. Musée d'Orsay DEC-A12 / Day 39 Factual Reconciliation

- **충돌 원인 분석**: DEC-A12(8/17)는 Orsay 2회 방문(9/29 상설 3.5시간 집중, 10/6 Mary Cassatt 특별전 개막 14:00 슬롯)을 확정하였으나, Day 39 데일리 카드와 리전 초안에 마레 지구 박물관(Picasso, Carnavalet)만 표기되어 불일치가 발생했음.
- **최종 해결 조치**:
  1. **DEC-A12**: 9/29(화) 1회차 상설 집중 관람 + 10/6(화) 2회차 <Mary Cassatt> 대형 회고전 개막 집중 관람으로 확정.
  2. **Day 32 (9/29 화)**: Musée d'Orsay 상설 컬렉션 3.5시간 집중 관람 + Musée Rodin 조각 정원.
  3. **Day 39 (10/6 화)**: Marché Convention 장보기 ➔ Musée d'Orsay <Mary Cassatt> 특별전 개막(14:00 슬롯, 90–120분) ➔ 마레 지구 연계(Musée Picasso Paris / Musée Carnavalet / 보주 광장 선택) ➔ 15구 귀환.
  4. **Day 39 데일리 카드 (`day-39.json`)**: 오르세 카사트 특별전 개막 슬롯을 메인 오후 앵커(order 2)로 추가하고, 피카소와 카르나발레를 마레 지구 연계 선택 일정(order 3, 4)으로 편성.
  5. **Region Schedule & Chapter**: 오르세 2회 방문 및 Day 39 카사트전 개막 ➔ 마레 지구 연계로 통일.
  6. **Place Classification**: `musee-d-orsay` dossier에 Day 32 및 Day 39 2회 방문 반영, `musee-picasso-paris` 및 `musee-carnavalet` Day 39 마레 연계 유지.
- **결과**: **DEC-A12, Day SOT, Region Schedule, Place Classification 전수 일치 (Contradiction = 0)**.

---

## 12. Bourse de Commerce Reconciliation (DEC-A05)

- **방문일**: **Day 40 (2026-10-07 수)**
- **정합성**: 8/26~10/5 전시 준비기간 및 10/6(화) 정기 휴관을 완벽히 피해, 10/7 신규 기획전(<Remember Me>) 개막 당일 슬롯으로 정확히 배치됨.

---

## 13. Temporary Exhibitions Reconciliation

- Grand Palais: <Cézanne et nous> (9/23~2027/1/17) ➔ Day 28 (9/25) 방문
- Musée du Luxembourg: <Andy Warhol> (9/16~2027/1/17) ➔ Day 29 (9/26) 방문
- Musée d'Orsay: <Mary Cassatt. L'indépendante> (10/6~2027/1/31) ➔ Day 39 (10/6) 개막 당일 방문
- Bourse de Commerce: <Remember Me> (10/7 개막) ➔ Day 40 (10/7) 방문
- Orangerie: <Monet, peindre le temps> ➔ Day 30 (9/27) 방문

---

## 14. Fashion Week Status

- **9/28 (Day 31)**: Paris Fashion Week 개막 분위기 & 마레 지구 스트리트 무드 관찰.
- **9/30 (Day 33)**: 몽테뉴 거리 & 팔레 드 도쿄 서부 패션위크 축 도시 관찰.
- 내부 셀럽 추정/쇼장 추측 문구를 제거하고 도시 라이프 관찰로 정돈.

---

## 15. Qatar Prix de l'Arc de Triomphe Status

- **일정**: **Day 37 (2026-10-04 일)**
- **역할**: 이번 파리 체류의 단일 최고 스포츠 앵커.
- **이동**: 메트로 10호선 Porte d'Auteuil ➔ 무료 셔틀 ➔ ParisLongchamp 경마장.
- **대형 미술관 중복 배제**: 경마일 당일 및 익일 오전 회복 보호.

---

## 16. Fête des Vendanges de Montmartre Status

- **일정**: **Day 40 (2026-10-07 수 오후~저녁)**
- **역할**: 몽마르트르 포도밭 축제 및 사크레쾨르 언덕 조망.

---

## 17. Performance / Opera Status

- 과거 기획되었던 오페라 3건(Il Barbiere 10/1, Este Mundo 10/8, Hamlet 10/9)은 2026-08-10 비용 및 일정 부담 사유로 전량 취소되었으며, 현재 Day SOT 기준 고정 티켓 공연은 0건입니다.
- 취소 이력 및 구버전 비교표는 `11_Paris_Planning_Residue_v1.0.md`로 분리 보존 완료.

---

## 18. Versailles / Suburban-Trip Status

- **Versailles**: **Day 34 (2026-10-01 목)** 전일 투어 확정 (10:00 본관 예약, 대정원, 트리아농).
- **Giverny / Chartres / 기타 근교**: 장기체류 생활 리듬 보호를 위해 기본안에서 제외하고 선택 대안 및 아카이브로 분리.

---

## 19. Restaurant / Cafe Classification

| 식음 장소 | 슬러그 | 분류 | 역할 |
|---|---|---|---|
| **Boulangerie Pichard** | `boulangerie-pichard` | 필수 (베이커리) | 15구 생활 거점 아침 바게트·크루아상 조달 (월·화 휴무) |
| **Marché Convention** | `marche-convention` | 필수 (시장) | 15구 노천시장 (화·목·일) 식재료 및 로티세리 치킨 조달 |
| **Café du Commerce** | `cafe-du-commerce` | 필수 (브라세리) | 15구 아르데코 3층 브라세리 (Day 28, Day 32, Day 42 점심) |
| **Le Grand Pan** | `le-grand-pan` | 필수 (비스트로) | 15구 숯불 스테이크 비스트로노미 (Day 34, Day 41 고별만찬) |
| **Bouillon Chartier Montparnasse** | `bouillon-chartier-montparnasse` | 필수 (부이용) | 6구 역사기념물 가성비 부이용 (Day 30 저녁) |

---

## 20. Food Cleanup

- **먹고 장보기**: 15구에서 반복 이용하기, 시장과 장보기, Paris 대표 식재료 7종 1문장 서술, 방문 업소 3곳 및 식사 원칙으로 간결화.
- 10여 개가 넘던 과거 후보 식당 목록은 아카이브 및 Place 소관으로 정리.

---

## 21. Stay & Local Life Cleanup

- **숙소와 15구 생활권**: 15구 확정 숙소(78 Rue de Lourmel) 거점의 일상 루틴과 생활 인프라 기술.
- **아침 운동**: `아침에는 15구 숙소 주변(센 강변, 샹드마르스, 시뉴 섬 방향)에서 가볍게 걷거나 뛰고, 근교일이나 대형 미술관 일정이 있는 날에는 별도 운동을 줄인다.`로 정돈.

---

## 22. Transport Preservation (현 상태 100% 유지)

- **Paris에서 이동하기**:
  - `### 평소에는 Metro와 도보`: 메트로 8·10·6호선 중심 이동 원칙
  - `### 오후 일정은 생활권에서 한 번에 이동`: 생활권과 목적지 간 직통/1회 환승
  - `### 대중교통 이용권 전략`:
    - 9/28–10/4 Weekly 한 번만 활용 (€32.40 / 13회 손익분기)
    - 도착/출국 주간 개별권 이용 (€2.55 단일권 / €2.05 10회 충전)
    - Navigo Weekly는 실물 카드/스마트폰 충전 (Navigo Easy에 넣지 않음)
    - 일드프랑스 1–5존 커버 (베르사유 RER C, 롱샹 셔틀 포함, 공항역 진출입만 제외)
    - 1개월 정기권(Monthly €90.80) 비효율로 미사용
  - `### 근교일은 철도`: 베르사유 RER C선 Javel역 직통
  - `### 출국일은 CDG 이동`: 14:00 이전 공식 택시 정액제 이동 (CDG Terminal 1)
- **Regression 여부**: **0건 (Transport 내용 완벽 보존)**

---

## 23. Lyon → Paris Handoff

- Day 27 (9/24 목): Lyon Part-Dieu역 13:04 발차 TGV INOUI 6618 탑승 ➔ 15:00 Paris Gare de Lyon 도착 ➔ 택시로 15구 숙소 이동 및 체크인. Contradiction = 0.

---

## 24. Paris → CDG Handoff

- Day 42 (10/9 금): 11:00 숙소 체크아웃 ➔ Café du Commerce 점심 ➔ 14:00 이전 공식 택시로 CDG Terminal 1 이동 ➔ 19:10 OZ502 탑승. Contradiction = 0.

---

## 25. Day 43 Scope

- Paris 숙박은 Day 27~Day 42 (15박)입니다.
- Paris Region의 15박 Schedule에는 9/24~10/9까지만 표기합니다.
- Day 43 (10/10 토)은 `post-Paris return handoff` (기내 수면 및 14:10 ICN 도착)로 전 여정 감사 및 실행표에만 명시합니다.

---

## 26. Planning Residue Archive

- 생성 파일: [`source/ARCHIVE/20_Regional_Chapters/11_Paris_Planning_Residue_v1.0.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/source/ARCHIVE/20_Regional_Chapters/11_Paris_Planning_Residue_v1.0.md)
- 보존 내용: 과거 5개 구 숙소 후보 분석, 취소된 오페라 패키지 비교표, 축구 후보 분석, 미술관 쿼터 표기, 근교 확장 후보, 여행 설계 철학 초안.

---

## 27. Manuscript Residue Before / After

| 검사 항목 | Before | After | 변화 |
|---|---:|---:|---:|
| `manuscript_residue_check.py` paris 흔적 토큰 | 33건 | **0건** | -33 (완전 박멸) |
| 원고 번호 및 내부 기획 헤딩 | 24건 | **0건** | -24 |
| 평가 별점 및 점수 표기 | 8건 | **0건** | -8 |

---

## 28. Quantitative Before / After

| 지표 | Before (main) | After (PA01F Final) | 변화 |
|---|---:|---:|---:|
| **Chapter 라인 수** | 2,082줄 | **386줄** | -1,696줄 (-81.5%) |
| **Chapter 바이트** | 126,447 B | **24,265 B** | -102,182 B (-80.8%) |
| **Promoted Region 라인 수** | 371줄 | **125줄** | -246줄 (-66.3%) |
| **일정표 개수** | 4개 | **1개** | -3개 (단일화) |
| **원고 잔재 토큰** | 33개 | **0개** | -33개 (완전 박멸) |
| **10개 QA 통과율** | — | **100% (10/10 PASS)** | 완벽 통과 |

---

## 29. Full-Region Regression QA (8개 지역 전수)

| Region | Consolidation Entry | Residue Count | Schema | Card/Heading Regression |
|---|:---:|:---:|:---:|:---:|
| **Barcelona** | O | 0 | `rc-region-v1` | 0 |
| **Girona** | O | 0 | `rc-region-v1` | 0 |
| **Nice** | O | 0 | `rc-region-v1` | 0 |
| **Aix** | O | 0 | `rc-region-v1` | 0 |
| **Luberon** | O | 0 | `rc-region-v1` | 0 |
| **Avignon** | O | 0 | `rc-region-v1` | 0 |
| **Lyon** | O | 0 | `rc-region-v1` | 0 |
| **Paris** | O | 0 | `rc-region-v1` | 0 |

---

## 30. Changed Files

1. `data/daily-cards/day-39.json` (Day 39 SOT에 Orsay Mary Cassatt 특별전 개막 슬롯 추가 및 마레 연계 정합)
2. `data/region-consolidation.json` (Paris 등록)
3. `source/CURRENT/20_Regional_Chapters/11_Paris_Long_Stay_v2.0.md` (rc-region-v1 정본 재편집 및 Day 39 카사트전 반영)
4. `source/CURRENT/20_Regions/paris.md` (승격본 재생성)
5. `source/ARCHIVE/20_Regional_Chapters/11_Paris_Planning_Residue_v1.0.md` (기획 잔재 아카이브)
6. `PA01_PARIS_REGION_CONSOLIDATION_QA.md` (QA 보고서)
