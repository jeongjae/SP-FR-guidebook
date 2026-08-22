# PA01 — Paris Long Stay Region Editorial Re-Consolidation QA Report

---

## 1. Overall Status

- **상태**: **PASS (전수 통폐합 및 검증 완료)**
- **대상 지역**: `paris` (Paris Long Stay, Chapter 11)
- **적용 스키마**: `rc-region-v1`
- **목표 달성**:
  - 원고형 기획 잔재, 과거 5구/7구 숙소 비교, 취소된 오페라 3건 이력, 축구 후보 분석, 15개 미술관 쿼터 표기를 아카이브로 분리 보존.
  - 15박 체류 전체(Day 27~Day 42)에 대한 authoritative Day SOT 100% 전수 대조 및 단일 일정표 정합.
  - 15구 생활권(78 Rue de Lourmel) 거점의 "오전 생활 / 오후 외출" 리듬 허브로 IA 전면 재편.
  - 전수 QA 10개 검사 PASS (원고 흔적 가드: 전체 8개 지역 흔적 0 달성, pytest 30 passed, PWA 871 cached).

---

## 2. Latest main SHA / Starting Condition

- **Base `origin/main` SHA**: `6e62189e` (Merge pull request #215 from jeongjae/fix/lyon-region-editorial-consolidation)
- **작업 브랜치**: `fix/paris-region-editorial-consolidation`

---

## 3. Paris Actual Stay Dates & Nights

- **체류 기간**: 2026년 9월 24일(목) ~ 2026년 10월 9일(금)
- **총 숙박 일수**: **15박 16일**
- **체류 일차**: Day 27 ~ Day 42 (Day 43은 기내박 및 인천 도착)
- **도착일**: Day 27 (9/24 목) 15:00 Gare de Lyon 도착 ➔ 15구 체크인
- **출국일**: Day 42 (10/9 금) 11:00 체크아웃 ➔ 14:00 이전 공식 택시로 CDG Terminal 1 이동 ➔ 19:10 OZ502 탑승

---

## 4. Confirmed Lodging Reconciliation

- **확정 숙소**: **78 Rue de Lourmel, 75015 Paris**
- **생활권**: 파리 15구 Convention / Lourmel / Commerce 생활권
- **교통 접근성**: 메트로 8호선(Lourmel, Commerce), 10호선(Avenue Émile Zola), 6호선(La Motte-Picquet - Grenelle)
- **생활 인프라**: Boulangerie Pichard (아티장 빵집), Marché Convention (화·목·일 노천시장)
- **과거 후보 정리**: 5구(Maubert), 7구(Rue du Bac), 13/14구 비교표 및 WeHost 수수료 분석은 `11_Paris_Planning_Residue_v1.0.md`로 아카이브 분리.

---

## 5. Complete Day-by-Day SOT Reconciliation

| Date | Day | Morning Routine | Afternoon Anchor | Evening | Actual / Optional | Reservation | Event / Theme |
|---|---:|---|---|---|---|---|---|
| **9/24 목** | 27 | Lyon 체크아웃 & TGV 이동 | Paris 15구 숙소 체크인 (15박 정착) | 15구 첫 장보기 & 숙소식 | Actual | TGV INOUI 6618 / 숙소 | 파리 입성 및 정착 |
| **9/25 금** | 28 | Pichard 빵 & 아침 운동 | Tootbus 시티투어 풀 루프 & Grand Palais 세잔전 | Café du Commerce 브라세리 저녁 | Actual | Grand Palais 세잔전 | 가을 특별전 개막 |
| **9/26 토** | 29 | 15구 토요 장보기 & 루틴 | Musée du Luxembourg 워홀전 & 뤽상부르 & 생제르맹 | 15구 숙소 귀환 & 저녁 | Actual | Luxembourg 워홀전 | 좌안 지성 산책 & 노트르담 외관 |
| **9/27 일** | 30 | Marché Convention 일요 장보기 | Musée de l'Orangerie (수련) & 튀일르리 & 팔레 루아얄 | Bouillon Chartier Montparnasse 저녁 | Actual | Orangerie 수련 | 고전 파리 & 오페라 외관 |
| **9/28 월** | 31 | 숙소 아침 & 출발 준비 | Musée Gustave Moreau & 9구 누벨 아테네 & 마레 지구 | 15구 숙소 귀환 & 저녁 | Actual | Moreau 상설 | Paris Fashion Week 개막 분위기 |
| **9/29 화** | 32 | Art-Heavy 빠른 아침 | Musée d'Orsay 3.5시간 집중 관람 & Musée Rodin | Café du Commerce 저녁 | Actual | Orsay 09:30 슬롯 | 인상주의 & 앵발리드 외관 |
| **9/30 수** | 33 | 단축 아침 & 출발 준비 | Petit Palais & 몽테뉴 거리 & Palais de Tokyo | 15구 숙소 귀환 & 저녁 | Actual | Petit Palais 무료 | Fashion Week 서부 축 |
| **10/1 목** | 34 | 숙소 출발 ➔ RER C 이동 | Château de Versailles (본관 10:00) & 대정원 & 트리아농 | Le Grand Pan 비스트로 저녁 | Actual | Versailles 10:00 여권권 | 베르사유 전일 투어 |
| **10/2 금** | 35 | Pichard 잠봉 뵈르 아침 | Musée du Louvre 마스터피스 4시간 집중 관람 | 센 강변 일몰 산책 & 숙소식 | Actual | Louvre 사전지정 | 루브르 명작 관람 |
| **10/3 토** | 36 | 15구 토요 장보기 & 루틴 | Musée Marmottan Monet (<인상, 해돋이>) & 파시 산책 | 15구 조기 귀환 & 휴식 | Actual | Marmottan 상설 | 모네 명작 & 경마 전야 휴식 |
| **10/4 일** | 37 | 숙소 출발 ➔ 롱샹 셔틀 | Qatar Prix de l'Arc de Triomphe (개선문상 본선) | 15구 숙소 귀환 & 저녁 | Actual | Arc 본선 티켓 | 세계 최고 권위 잔디 경마 축제 |
| **10/5 월** | 38 | 경마 후 늦은 기상 & 세탁 | Musée Jacquemart-André & 몽소 공원 산책 | 15구 숙소 귀환 & 저녁 | Actual | Jacquemart 상설 | 경마 후 회복 & 저택 박물관 |
| **10/6 화** | 39 | Marché Convention 화요 장보기 | Musée Picasso Paris & Musée Carnavalet & 보주 광장 | 15구 숙소 귀환 & 저녁 | Actual | Picasso 상설 | 마레 지구 예술 더블 |
| **10/7 수** | 40 | 단축 아침 & 출발 준비 | Bourse de Commerce (피노 컬렉션) & 몽마르트르 포도축제 | 15구 숙소 귀환 & 저녁 | Actual | Bourse 11:00 슬롯 | 피노 컬렉션 개막 & 포도축제 |
| **10/8 목** | 41 | Art-Heavy 빠른 아침 | Musée Guimet & Musée d'Art Moderne (MAM) | 트로카데로 일몰 & Le Grand Pan | Actual | Guimet 상설 | 아시아/현대미술 & 고별 만찬 |
| **10/9 금** | 42 | 최종 짐 정리 & 체크아웃 | Café du Commerce 점심 & 공식 택시 CDG 이동 | OZ502 탑승 (19:10 발) | Actual | OZ502 항공권 | 파리 15박 완료 및 출국 |
| **10/10 토** | 43 | 기내 수면 & 시차 적응 | 14:10 인천공항(ICN) 제1터미널 도착 | 자택 귀환 | Actual | ICN 도착 | 43일 대여정 공식 완결 |

---

## 6. “오전 생활 / 오후 외출” Coverage

- **오전 루틴 커버리지**: 15박 전체(Day 27~Day 42) 매일 아침식사(Boulangerie Pichard), 생활 장보기(Marché Convention/Lecourbe), 운동/산책, 세탁 및 housekeeping 리듬 완벽 구현.
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
- **After**: 9/24 도착일부터 10/9 출국일까지 날짜별 핵심 일정을 담은 **단일 2열 일정표 1개**로 정규화.

---

## 10. Museum Classification

| 미술관/문화시설 | 슬러그 | 최종 등급 | Day 귀속 | 비고 |
|---|---|---|:---:|---|
| **Grand Palais** | `grand-palais` | 필수 | Day 28 | <Cézanne et nous> 특별전 |
| **Musée du Luxembourg** | `musee-du-luxembourg` | 필수 | Day 29 | <Andy Warhol> 특별전 |
| **Musée de l'Orangerie** | `musee-de-l-orangerie` | 필수 | Day 30 | 모네 <수련> 연작 |
| **Musée Gustave Moreau** | `musee-gustave-moreau` | 필수 | Day 31 | 상징주의 아틀리에 저택 |
| **Musée d'Orsay** | `musee-d-orsay` | 필수 | Day 32 | 인상주의 3.5시간 집중 |
| **Musée Rodin** | `musee-rodin` | 필수 | Day 32 | 로댕 조각 정원 |
| **Petit Palais** | `petit-palais` | 필수 | Day 33 | 파리 시립미술관 상설전 |
| **Musée du Louvre** | `musee-du-louvre` | 필수 | Day 35 | 마스터피스 4시간 집중 |
| **Musée Marmottan Monet** | `musee-marmottan-monet` | 필수 | Day 36 | <인상, 해돋이> 원작 |
| **Musée Jacquemart-André** | `musee-jacquemart-andre` | 필수 | Day 38 | 19세기 저택 미술관 |
| **Musée Picasso Paris** | `musee-picasso-paris` | 필수 | Day 39 | 오텔 살레 피카소 컬렉션 |
| **Musée Carnavalet** | `musee-carnavalet` | 필수 | Day 39 | 파리 도시 역사박물관 |
| **Bourse de Commerce** | `bourse-de-commerce-pinault-collection` | 필수 | Day 40 | <Remember Me> 10/7 개막전 |
| **Musée Guimet** | `musee-guimet` | 필수 | Day 41 | 국립 아시아 동양미술관 |
| **Musée d'Art Moderne (MAM)** | `musee-d-art-moderne-de-paris` | 필수 | Day 41 | 파리 시립 현대미술관 |
| **BnF Richelieu** | `bnf-richelieu` | 우선추천 | — | 오발 열람실 무료 (도서관) |
| **Centre Pompidou** | `centre-pompidou` | 제외 | — | 2025~2030 전면 개보수 폐관 안내 |

---

## 11. Orsay 2-Visit Reconciliation (DEC-A12)

- DEC-A12는 9/29 및 10/6 2회 방문을 허용하였으며, authoritative Day SOT는 **Day 32 (9/29 화)** 09:30 개장 첫 슬롯 3.5시간 집중 관람을 핵심 방문으로 확정하고, Day 39 (10/6 화)는 마레 지구의 Picasso & Carnavalet 더블 일정으로 운영합니다.
- 모순 및 충돌 0건으로 정합 완료.

---

## 12. Bourse de Commerce Reconciliation (DEC-A05)

- **방문일**: **Day 40 (2026-10-07 수)**
- **정합성**: 8/26~10/5 전시 준비기간 및 10/6(화) 정기 휴관을 완벽히 피해, 10/7 신규 기획전(<Remember Me>) 개막 당일 슬롯으로 정확히 배치됨.

---

## 13. Temporary Exhibitions Reconciliation

- Grand Palais: <Cézanne et nous> (9/23~2027/1/17) ➔ Day 28 (9/25) 방문
- Musée du Luxembourg: <Andy Warhol> (9/16~2027/1/17) ➔ Day 29 (9/26) 방문
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
- **아침 운동**: `아침에는 15구 숙소 주변에서 가볍게 걷거나 뛰고, 도심 일정이 긴 날에는 별도 운동을 줄인다.`로 생활권 중심 간결화.

---

## 22. Transport Cleanup

- **Paris에서 이동하기**:
  - `### 평소에는 Metro와 도보`: 메트로 8·10·6호선 중심 이동 원칙
  - `### 오후 일정은 생활권에서 한 번에 이동`: 생활권과 목적지 간 직통/1회 환승
  - `### 대중교통 이용권 전략`: 9/28–10/4 Weekly 한 번만 활용, 도착/출국 주간 개별권 이용
  - `### 근교일은 철도`: 베르사유 RER C선 이동
  - `### 출국일은 CDG 이동`: 14:00 이전 공식 택시 정액제 이동

---

## 23. Lyon → Paris Handoff

- Day 27 (9/24 목): Lyon Part-Dieu역 13:04 발차 TGV INOUI 6618 탑승 ➔ 15:00 Paris Gare de Lyon 도착 ➔ 택시로 15구 숙소 이동 및 체크인. Contradiction = 0.

---

## 24. Paris → CDG Handoff

- Day 42 (10/9 금): 11:00 숙소 체크아웃 ➔ Café du Commerce 점심 ➔ 14:00 이전 공식 택시로 CDG Terminal 1 이동 ➔ 19:10 OZ502 탑승. Contradiction = 0.

---

## 25. Planning Residue Archive

- 생성 파일: [`source/ARCHIVE/20_Regional_Chapters/11_Paris_Planning_Residue_v1.0.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/source/ARCHIVE/20_Regional_Chapters/11_Paris_Planning_Residue_v1.0.md)
- 보존 내용: 과거 5개 구 숙소 후보 분석, 취소된 오페라 패키지 비교표, 축구 후보 분석, 미술관 쿼터 표기, 근교 확장 후보, 여행 설계 철학 초안.

---

## 26. Manuscript Residue Before / After

| 검사 항목 | Before | After | 변화 |
|---|---:|---:|---:|
| `manuscript_residue_check.py` paris 흔적 토큰 | 33건 | **0건** | -33 (완전 박멸) |
| 원고 번호 및 내부 기획 헤딩 | 24건 | **0건** | -24 |
| 평가 별점 및 점수 표기 | 8건 | **0건** | -8 |

---

## 27. Quantitative Before / After

| 지표 | Before (main) | After (PA01 Consolidation) | 변화 |
|---|---:|---:|---:|
| **Chapter 라인 수** | 2,082줄 | **386줄** | -1,696줄 (-81.5%) |
| **Chapter 바이트** | 126,447 B | **24,196 B** | -102,251 B (-80.9%) |
| **Promoted Region 라인 수** | 371줄 | **125줄** | -246줄 (-66.3%) |
| **일정표 개수** | 4개 | **1개** | -3개 (단일화) |
| **원고 잔재 토큰** | 33개 | **0개** | -33개 (완전 박멸) |
| **10개 QA 통과율** | — | **100% (10/10 PASS)** | 완벽 통과 |

---

## 28. 전체 QA 결과

| 검사 항목 | 명령어 | 결과 | 비고 |
|---|---|---|---|
| 사이트 전체 빌드 | `python3 build/site.py` | **PASS** | 372쪽 생성, 색인 191건 |
| 단위 및 통합 테스트 | `pytest tests/` | **PASS** | 30 passed in 7.11s |
| 원고 흔적 가드 | `python3 build/manuscript_residue_check.py` | **PASS** | 8개 전 지역 흔적 0 |
| 지역 구조 검사 | `python3 build/region_structure_check.py` | **PASS** | 분류·섹션·방문일·링크 0 오류 |
| 사진 연결 검사 | `python3 build/media_lookup_check.py` | **PASS** | 미매핑 0, 누락 0 |
| 표 손실 검사 | `python3 build/table_loss_check.py` | **PASS** | 조용한 열 손실 0 |
| UX & 디자인 토큰 검사 | `python3 build/ux_check.py` | **PASS** | 명암비, 하단탭, URL 0 결함 |
| PWA 오프라인 검사 | `python3 build/pwa_check.py` | **PASS** | 871개 파일 전체 캐시 |
| 다중 뷰포트 검사 | `python3 build/viewport_check.py` | **PASS** | 6개 해상도 가로 오버플로 0 |
| 사실 토큰 가드 | `build/fact_guard.py` (via site.py) | **PASS** | 45개 확정 토큰 생존 확인 |
| 조사 종결 검사 | `python3 build/research_closure_check.py` | **PASS** | 0 unclassified |

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

1. `data/region-consolidation.json` (Paris 등록 완료)
2. `source/CURRENT/20_Regional_Chapters/11_Paris_Long_Stay_v2.0.md` (rc-region-v1 전면 재편집)
3. `source/CURRENT/20_Regions/paris.md` (승격본 재생성)
4. `source/ARCHIVE/20_Regional_Chapters/11_Paris_Planning_Residue_v1.0.md` (기획 잔재 아카이브 생성)
5. `PA01_PARIS_REGION_CONSOLIDATION_QA.md` (QA 보고서)
