# Provence 실제 일정 반영 (9/10–9/16) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 9/10~9/16 Aix→Luberon→Avignon 구간을 실제 확정 일정(Aix 4박 · Gordes 1박 · Avignon 5박)에 맞게 정본·파생 데이터 전체에서 정정한다.

**Architecture:** 정본 우선순위대로 고친다 — decisions.json → itinerary.json + 트래커 xlsx → daily-cards → 마스터 일정 MD(+파생 itinerary-places 재생성) → 챕터 07/08/09 → region-essentials·map-queries·maps assets → 검증 스크립트 기대값. 검증은 이 저장소의 가드 스위트가 테스트다.

**Tech Stack:** Python(빌드·가드), openpyxl(트래커), JSON/MD 수기 편집.

**Spec:** 사용자 지시문 (2026-09-16 대화). §16 중단조건은 사용자 지시로 무시 — 충돌은 보고만.

## Global Constraints

- 날짜·Day 매핑: 8/29=Day 1 고정 → 9/10=D13 … 9/16=D19. Day 번호 재부여 없음.
- 숙박: Aix 9/10~9/14 4박(불변) · Gordes 9/14~9/15 1박 · Avignon 9/15~9/20 5박.
- 주소 정본 형식: "104 Rte des Moines, 84220 Gordes, France" · "10 Rue d'Annanelle, 84000 Avignon, France".
- 숙소 이름(모든 day 카드에서 완전 동일해야 함 — model.validate 숙소 일관성 가드):
  - "Gordes 숙소 — Rte des Moines" (status confirmed, lat 43.9099822, lng 5.1972296 ← Nominatim 도로 수준)
  - "Avignon 숙소 — Rue d'Annanelle" (status confirmed, lat 43.9472485, lng 4.8021506 ← Nominatim 번지 수준)
- 확정 식사: 9/14 저녁 La Trinquette(55 Rue des Tracapelles, Gordes · 화요 휴무 → 월요일 영업 확인됨 · 04 90 72 11 62) = 결혼기념일. 9/15 저녁 = 장보기 후 숙소 식사.
- 신규 방문지: Château La Coste — Tadao Ando Art Centre (2750 Route de la Cride, 13610 Le Puy-Sainte-Réparade · 연중무휴 10:00–19:00 · +33 4 42 61 89 98) → 9/12 오후. 기존 `lacoste`(사드 성)와 별개 — 혼동 금지. 신규 canonical place 는 만들지 않고 place_ref 없는 stop 으로 넣는다 (La Récréation 전례).
- 시장 검증 완료: 9/12(토) Aix 대형시장 ✓ · 9/15(화) Gordes 시장 ✓ · 9/16(수) Saint-Rémy 시장 ✓.
- 렌터카: 9/9 인수 ~ 9/17 18:30 Avignon TGV 반납 — 변경 없음. 9/16 Alpilles 는 반납 전 ✓.
- 9/17~9/20 (D20~23)은 숙소 객체 교체 + stale 문구만 수정.
- site/ · 20_Regions 직접 편집 금지. 75_Execution_Maps·80_* v0.x 레거시 자산은 빌드 미참조라 보존.

## 최종 일정 (Source of Truth)

| Day | 날짜 | 요일 | 내용 | 숙박 |
|---|---|---|---|---|
| 13 | 9/10 | 목 | Moustiers→(Crêtes·Galetas 유지)→Valensole→Aix 체크인·시내 파악 | Aix |
| 14 | 9/11 | 금 | Marseille 당일치기 (TER, 기존 유지) | Aix |
| 15 | 9/12 | 토 | Aix 토요시장 · Vieil Aix · Atelier de Cézanne · Château La Coste(Tadao Ando) | Aix |
| 16 | 9/13 | 일 | 오전 Aix 운동(Rotonde–Mirabeau–Parc Jourdan 기존 안) · 오후 Lourmarin(마을·샤토·수채화 90분) | Aix |
| 17 | 9/14 | 월 | Aix 체크아웃 → Roussillon → Gordes 16:00 체크인 → La Trinquette 결혼기념일 저녁 | Gordes |
| 18 | 9/15 | 화 | Gordes 시장 → 체크아웃 → Sénanque → L'Isle-sur-la-Sorgue → Avignon 체크인·장보기·숙소 저녁 | Avignon |
| 19 | 9/16 | 수 | Avignon → Saint-Rémy(수요시장, 오전) → Les Baux(오후) → Avignon 복귀 | Avignon |

### Task 1: 결정 레지스터 (data/decisions.json)
- [ ] DEC-A07 → 9/15–9/20. DEC-A10 → Gordes 1박 확정으로 개정. DEC-RS01-A/B/C 본문·금지패턴 개정('Avignon 5박' 금지 해제, 'Gordes 2박'·'Avignon 4박' 금지 추가). 신규 DEC-EX16(실제 일정 반영, also_check_daily_cards).

### Task 2: itinerary.json + 트래커 xlsx
- [ ] stays: luberon checkout 2026-09-15/nights 1 · avignon checkin 2026-09-15/nights 5.
- [ ] xlsx Accommodation: Gordes(9/14~15·1박·예약완료·주소·비고), Avignon(9/15~20·5박·예약완료·주소·비고).
- [ ] xlsx Reservations: R005 "Gordes 숙소 1박 — Rte des Moines" 9/14 확정 · R006 "Avignon 숙소 5박 — Rue d'Annanelle" 9/15 확정.

### Task 3: daily-cards D13~D23
- [ ] D13: stop 문구에 시내·시장 위치 파악 반영(소폭). D14: "익일 Luberon 이동 준비" → 익일 Aix 시장일로 정정.
- [ ] D15: Granet → Château La Coste 오후 블록(차량)으로 교체, Granet 은 우천 대안으로. dayType 재검토(city→driving 요소), routeCache null.
- [ ] D16: Cassis 전체 삭제 → 오전 운동 + 오후 Lourmarin(마을·Château·수채화 스케치 90분) + Aix 복귀. routeCache null.
- [ ] D17: Lourmarin/Lacoste/Bonnieux 제거 → Roussillon(Sentier des Ocres) → Gordes 16:00 체크인 → 마을 산책 → La Trinquette 저녁(결혼기념일 MUST). 숙소 객체 확정.
- [ ] D18: Gordes 시장(장날 ✓)→체크아웃→Sénanque(9/15 회차 기존 확인 유지)→L'Isle(필수 경유로 승격)→Avignon 체크인→장보기·숙소 저녁. Roussillon 제거.
- [ ] D19: 출발·복귀를 Avignon 으로, Gordes 체크아웃 제거, 숙소 객체 Avignon 확정.
- [ ] D19~D22 hotel 객체 "Avignon 숙소 — Rue d'Annanelle"/confirmed/주소/좌표, D17 "Gordes 숙소 — Rte des Moines". D20~22 stale 문구 정리.

### Task 4: 마스터 일정 MD + itinerary-places 재생성
- [ ] 03_Whole_Trip D15~D19 행·장거리 이동일 표·잠금 열 갱신 → `python3 scripts/extract_itinerary_places.py`.

### Task 5: 챕터 07/08/09
- [ ] 07 Aix: 한눈에 보기·Cassis 절→La Coste/Lourmarin 반일, Day 15/16/17 절 재작성, 우천 대안·예약 절 갱신.
- [ ] 08 Luberon: 2박→1박 전면(개요·숙소·식사 배치·Day 17/18/19 절·최종 확인 체크리스트), La Trinquette 확정 저녁 기재.
- [ ] 09 Avignon: 5박·9/15 체크인·숙소 확정 주소, Day 19 절을 Avignon 기점 당일기로 재작성, 도착일=Day 18 로 수정.

### Task 6: 파생·지도 데이터
- [ ] data/region-essentials.json aix/luberon/avignon 재작성(스테일 일자 포함 전면 정정).
- [ ] data/map-queries.json hotels: 신규 두 숙소(FOUND·주소 쿼리) 추가, 옛 후보 키 정리; La Coste·La Trinquette stop 쿼리 추가(day-15:…, day-17:…).
- [ ] source/ASSETS/maps: place-registry(두 숙소 confirmed 로 교체, chateau-la-coste attraction 추가) · daily-routes idx14~18 재작성.
- [ ] data/place-facts.json: Sénanque 9/14 표기→9/15, fou-de-fafa "9/16 첫 저녁" note 정정.
- [ ] 30_Places dossier stale Day/일자 참조 grep 후 최소 수정 (cassis 계열은 '일정 외 대안'으로 표기).

### Task 7: 검증 스크립트 기대값
- [ ] scripts/validate_itinerary.py: R005/R006 기대값, day-16 필수 용어(Lourmarin·수채화 등), day-15 (La Coste), 홈 stale/필수 문자열 교체.

### Task 8: 빌드·가드·감사
- [ ] `python3 build/site.py` → `python3 build/ux_check.py` → `python3 build/content_audit.py` → `python3 build/guards/run_all.py` → `python3 scripts/validate_itinerary.py` → `python3 scripts/validate_media.py` → `python3 scripts/validate_map_data.py --quiet-warnings` → `python3 build/test_validation.py` → `python3 build/pwa_check.py`.
- [ ] 링크·중복 감사: schedule/guide/daily 페이지에서 옛 패턴 잔존 grep (site/ 기준, §12 목록).

### Task 9: 커밋·PR·배포
- [ ] 논리 단위 커밋 → PR → CI PASS → merge → 배포 watch → main sync (standing instruction).
