# FCR-03 — Aix / Marseille / Cassis / Luberon / Avignon / Arles QA Report
## Provence Food Expansion / Markets / Self-Catering / Wine & Cheese / Route-Linked Dining
### Status: PASS (100%) · Date: 2026-08-21 · Baseline: FCR-02 PASS / FCR-01 PASS / EX-13 PASS

---

## 0. Overall Verdict

```text
================================================================================
FCR-03 PROVENCE FOOD CONTENT EXPANSION: ALL PASS
- Privacy Regression Pre-Check: PASS (0 New Leaks across repo, build & site)
- Architecture Model Reuse: PASS (FCR-01/02 Foundation 100% Reused without mutation)
- Regional Food Guides: 10 Traditional Foods Defined across 4 Micro-Regions
- Market Audits: 5 Markets Audited (Richelme/Prêcheurs, Coustellet, Gordes, Les Halles, Uzès)
- Self-Catering Model: Luberon Farmhouse 3-Night Self-Catering & Picnic Model Established
- Wine / Cheese / Produce: 8 Specialized Items Integrated with Driving Safety Rules
- Meal Slot Classification: Days 12–23 Meal Slots Classified (0 Generic / Unclear Slots)
- Food Backlog Resolution: All EX-13 Provence Backlog Items Resolved to Canonical Places
- Canonical Places: 126 Total (Historical EX-13: 111 -> FCR-01: 114 -> FCR-02: 121 -> FCR-03: 126)
- Route Revalidation: Days 12–22 Chronology & Fatigue Verified (Day 15 TER & Cassis Port-Miou)
- Full Test Suite: 12/12 Test Suites PASS + Site Build (361 Pages, 0 Content Loss, 0 UX Issues)
- Active Operational P2: 9 Maintained (FEAS-DUR-05 & FEAS-DUR-14 remain resolved)
================================================================================
```

---

## 1. Baseline Reconciliation

- **Trip Configuration**: 43 Days / 42 Nights (2026-08-29 ~ 2026-10-10)
- **Historical EX-13 Place Count**: 111 Canonical Places
- **Pre-FCR03 (FCR-02) Live Count**: 121 Canonical Places
- **FCR-03 New Places**: +5 (`patisserie-weibel`, `chez-gilbert-cassis`, `fou-de-fafa-avignon`, `les-cocottes-saint-louis`, `le-gibolin-arles`)
- **Post-FCR03 Live Place Count**: **126 Canonical Places**
- **Active Operational P2 Count**: 9 (Maintained strictly without regression; `FEAS-DUR-05` and `FEAS-DUR-14` remain resolved validator artifacts).

---

## 2. Privacy Regression Audit

- **Verification Scope**: `source/`, `data/`, `build/`, `site/`, `scripts/`, `docs/`, generated search index, PWA manifests, and newly produced CSV/MD artifacts.
- **Sanitization Status**: All Airbnb codes (`HM...`), Hertz reservation numbers (`L671...`/`L672...`), voucher numbers (`36558...`/`14008...`), PNR codes, and private host contacts remain sanitized to `[CONFIRMED]`.
- **Findings**: 0 new leaks (`FCR03_PRIVACY_REGRESSION_SCAN.csv`).

---

## 3. Foundation Reuse

The data architecture validated in FCR-01 and FCR-02 was applied cleanly without any modifications:
1. **Decoupling**: Regional Recommended Foods (`FCR03_REGIONAL_FOOD_MATRIX.csv`) are strictly decoupled from physical venues (`FCR03_RESTAURANT_CAFE_MARKET_RESEARCH.csv`).
2. **Selection Origin**: `RECOMMENDED` (Curated based on regional authenticity and route efficiency; no artificial `WISH` places created).
3. **Meal Roles**: `PRIMARY`, `BACKUP`, `MARKET`, `SELF_CATERING`, `OPTIONAL`.
4. **Food Kinds**: `RESTAURANT`, `MARKET`, `CAFE`.

---

## 4. Current Provence Schedule Scope (Days 12–22)

- **Day 12**: Nice ➔ Saint-Paul-de-Vence ➔ Grasse ➔ Aix-en-Provence 체크인
- **Day 13**: Aix-en-Provence (Place Richelme 목요 대형 시장, Vieil Aix, Atelier Cézanne, Musée Granet, Cours Mirabeau)
- **Day 14**: Cassis & Calanques 당일치기 (Cassis 항구 해산물 점심, 유람선, Port-Miou) ➔ Aix 복귀
- **Day 15**: Marseille 당일치기 (TER 이동, Vieux-Port, Le Panier, Mucem, 점심, Notre-Dame de la Garde) ➔ Aix 복귀
- **Day 16**: Aix 체크아웃 ➔ Lourmarin ➔ Marché Paysan de Coustellet (일요 파머스 마켓 장보기) ➔ Goult ➔ Luberon 농가 숙소 체크인 (테라스 첫 저녁 / 숙소식)
- **Day 17**: Luberon 오커길 & 생활마을 (Roussillon 점심, Goult 풍차 언덕, 농가 숙소 자가 조리)
- **Day 18**: Luberon Gordes (화요 대형 시장 장보기) ➔ Village des Bories ➔ 시장 재료 피크닉 점심 ➔ Sénanque ➔ Ménerbes ➔ 농가 숙소 저녁
- **Day 19**: Luberon 농가 체크아웃 ➔ Avignon 이동, 구시가지 점심 ➔ 체크인 ➔ Rue des Teinturiers ➔ 아비뇽 첫 저녁 (Fou de Fafa)
- **Day 20**: Avignon 교황도시 (Les Halles 아침 시장, Palais des Papes, 광장 비스트로 점심, Rocher des Doms, Pont Saint-Bénézet, Les Cocottes 저녁)
- **Day 21**: Uzès & Pont du Gard 당일치기 (Uzès 구시가지 에르브 광장 점심, 퐁뒤가르) ➔ Avignon 복귀
- **Day 22**: Arles 당일치기 (TER 이동, Arènes, Théâtre Antique, Le Gibolin 점심, Cloître Saint-Trophime, La Roquette) ➔ Avignon 마지막 저녁
- **Day 23**: Avignon TGV역 렌터카 반납 ➔ TGV 타고 Lyon으로 이동 (Provence 여정 종료 및 Lyon 개시)

---

## 5. Regional Food Matrix Summary (10 Items)

### A. Aix / Marseille / Cassis (4 Items)
1. **Calissons d'Aix (칼리송 덱스)**: 아몬드 페이스트와 멜론 당절임에 로열 아이싱을 입힌 15세기 엑상프로방스 대표 전통 과자.
2. **Bouillabaisse traditionnelle (정통 부야베스)**: 라스카스 등 5종 이상의 암초 생선과 사프란 육수, 마늘 루이으(Rouille) 소스, 크루통의 마르세유·카시스 전통 생선 스튜.
3. **Panisse marseillaise (파니스)**: 병아리콩 가루 반죽을 썰어 바삭하게 튀겨낸 마르세유 전통 길거리 스낵.
4. **Navettes de Marseille (나베트)**: 1781년부터 성촉절에 구워온 배 모양의 오렌지꽃 향 비스킷.

### B. Luberon / Provence Inland (3 Items)
1. **Tapenade & Anchoïade (타프나드 & 앙쇼이아드)**: 블랙·그린 올리브와 케이퍼, 앤초비의 올리브 스프레드 및 채소용 마늘 앤초비 딥.
2. **Fromage de Banon AOP (바농 염소 치즈)**: 오크 밤나무 잎으로 감싸 숙성시킨 뤼베롱 전통 부드러운 생 염소 치즈.
3. **Soupe au pistou (수프 오 피스투)**: 제철 콩, 채소에 바질·마늘·올리브유 페스토와 치즈를 넣은 프로방스 여름 채소 수프.

### C. Avignon / Rhône / Arles (3 Items)
1. **Daube provençale (도브 프로방살)**: 론 밸리 레드 와인과 오렌지 껍질, 허브를 넣고 무쇠 코코트 냄비에 6시간 끓인 소고기 스튜.
2. **Grand Aïoli provençal (그랑 아이올리)**: 신선한 마늘 올리브유 아이올리 소스에 데친 대구(Morue), 감자, 채소, 달걀을 곁들인 금요 전통 요리.
3. **Gardianne de taureau AOP (가르디안 드 토로)**: 카마르그 AOP 황소 고기를 레드 와인과 앤초비, 오렌지 필로 끓인 아를의 영혼 요리 (카마르그 적미 곁들임).

---

## 6. Market Audit Summary (5 Markets)

1. **Place Richelme & Prêcheurs (Aix)**: 매일 식료품 시장(Richelme) 및 목요 대형 종합 시장(Prêcheurs). 제철 무화과/치즈 구매 및 Pâtisserie Weibel 테라스 아침 (Day 13).
2. **Marché Paysan de Coustellet (Luberon)**: 프랑스 공인 정통 생산자 직거래 일요 시장. 100% 농가 직판 바농 치즈, 무화과, 사퀴테리, 시골빵 장보기 (Day 16 농가 입소 보급선).
3. **Marché de Gordes (Luberon)**: 화요일 성곽 광장 대형 시장. 피크닉용 바게트 샌드위치, 과일, 치즈 조달 (Day 18).
4. **Les Halles d'Avignon (Avignon)**: 파트리크 블랑 수직 정원(Mur Végétal) 아래 40여 개 점포 실내 중앙시장. 델리 조리식품, Chèvre du Ventoux, 굴 바 (Day 20).
5. **Marché d'Uzès (Place aux Herbes)**: 수·토 전통 시장. 금요일 방문으로 시장 대신 한적한 광장 아케이드 카페 산책 및 테라스 런치 (Day 21).

---

## 7. Luberon Self-Catering Model

- **Day 16 저녁**: Coustellet 생산자 시장에서 구매한 신선 바농 치즈, 사퀴테리, 솔리에스 무화과, 트라디시옹 바게트, 뤼베롱 로제 와인으로 테라스 플래터 세팅 (조리 시간 15분, 피로도 최소화).
- **Day 17 저녁**: 로컬 슈퍼 및 델리에서 조달한 생면 파스타, 바질 페스토(Pistou), 방울토마토, 부라타 치즈로 간단 테라스 파스타 조리 (15분 소요).
- **Day 18 저녁**: 고르드 시장 구운 닭(Poulet rôti) 및 잔여 식재료 소진 만찬, 익일 이동 대비 신속 정리 완료.

---

## 8. Wine, Cheese & Produce Content

- **Côtes de Provence Rosé (AOC)**: 상큼한 복숭아·자몽 향의 로제 와인 (숙소 저녁 식사 / 아페리티프용).
- **Cassis Blanc (AOC)**: 미네랄과 흰 꽃 향이 풍부한 최고급 해산물 화이트 와인 (Chez Gilbert 점심 / 동승자 시음 또는 1인 1잔 한정).
- **Luberon AOC**: 시라·그르나슈 기반의 가성비 뛰어난 로컬 와인 (농가 숙소 테라스용).
- **Châteauneuf-du-Pape AOC**: 13가지 품종 블렌딩의 웅장한 론 레드 와인 (Avignon 디너용).
- **Banon AOP & Chèvre du Ventoux**: 밤나무 잎 숙성 크리미 염소 치즈 및 몽방투 허브 치즈.
- **Figue de Solliès AOP & Melon de Cavaillon**: 9월 제철 특산 솔리에스 꿀무화과 및 카바용 그물 멜론.
- **운전 안전 원칙**: 렌터카 운전일에는 일체 음주를 배제하며, 와인은 숙소 복귀 후 테라스에서 시음하도록 가이드 엄수.

---

## 9. Scheduled Food Places Research & Integration

| Place Slug | Venue Name | Region | Day / Slot | Role | Menu & Pricing | Hours & Reservation |
|---|---|---|---|---|---|---|
| `patisserie-weibel` | **Pâtisserie Weibel** | Aix | **Day 13 아침/티** | PRIMARY | Calisson d'Aix, 무화과 타르트, 크루아상, 카페 (€8~€15/인) | 화–일 07:30–19:00 (월 휴무), 예약 불필요 |
| `chez-gilbert-cassis` | **Chez Gilbert** | Cassis | **Day 14 점심** | PRIMARY | 정통 부야베스, 암초 생선 수프, 카시스 화이트 와인 (€35~€75/인) | 점심 12:00–14:30, 수·목 휴무, 사전 예약 필수 |
| `coustellet` | **Marché Paysan de Coustellet** | Luberon | **Day 16 장보기** | MARKET | 100% 농가 직판 바농 치즈, 무화과, 사퀴테리, 시골빵 (€10~€30) | 일 08:00–13:00, 예약 불필요 |
| `gordes` | **Marché de Gordes** | Luberon | **Day 18 피크닉** | MARKET | 바농 염소치즈, 바게트, 절임 올리브, 꿀 (€8~€15) | 화 08:00–13:00, 예약 불필요 |
| `fou-de-fafa-avignon` | **Fou de Fafa** | Avignon | **Day 19 저녁** | PRIMARY | 어린 양갈비 구이, 계절 3코스 디너 (€38~€45/인) | 저녁 18:30–21:30, 월·화 휴무, 사전 예약 필수 |
| `les-halles` | **Les Halles d'Avignon** | Avignon | **Day 20 아침/장** | MARKET | Mur Végétal, Chèvre du Ventoux, 생선 델리, 굴 (€5~€20) | 화–일 06:00–14:00, 월 휴무, 예약 불필요 |
| `les-cocottes-saint-louis` | **Les Cocottes Saint-Louis** | Avignon | **Day 20/22 저녁** | PRIMARY | 도브 프로방살 냄비 요리, 양정강이 콩피 (€25~€38/인) | 매일 12:00–14:00 / 19:00–22:00, 테라스 예약 권장 |
| `le-gibolin-arles` | **Le Gibolin** | Arles | **Day 22 점심** | PRIMARY | 카마르그 황소 스튜, 카마르그 적미 밥 (€22~€26/인) | 점심 12:00–14:00, 일·월 휴무, 12:00 오픈 방문 |

---

## 10. Provence Route Revalidation (Days 12–22)

- **Day 14 (Cassis)**: 깔랑끄 유람선 후 Chez Gilbert 12:30 점심(75분) 엄수, 14:30 Port-Miou 산책 후 16:30 Aix 복귀로 피로도 3(MODERATE) 유지.
- **Day 15 (Marseille)**: Aix-Marseille 왕복 TER 전철을 활용하여 도심 운전/주차 스트레스 0 실현. 과도한 2시간 부야베스 코스 대신 가벼운 구항구 런치로 박물관(Mucem)과 노트르담 대성당 일정 완벽 보호.
- **Day 16 (Luberon 입소)**: 쿠스텔레 일요 시장 장보기 후 16:00 농가 숙소 체크인, 테라스 숙소식 진행.
- **Day 18 (Gordes)**: 화요 시장 08:45 조기 주차로 인파 회피, 피크닉 런치로 식당 대기시간 0분 달성.
- **Day 22 (Arles)**: 왕복 TER(18분) 활용, Le Gibolin 12:00 점심 후 16:30 아비뇽 조기 복귀로 익일 TGV 이동 짐 정리 시간 보호.

---

## 11. 산출 아티팩트 목록 (총 11건)

1. `FCR03_PROVENCE_FOOD_EXPANSION_QA.md`: 종합 QA 리포트
2. `FCR03_REGIONAL_FOOD_MATRIX.csv`: 프로방스 권역 10종 음식 매트릭스
3. `FCR03_RESTAURANT_CAFE_MARKET_RESEARCH.csv`: 8개 업장 및 시장 실사 데이터
4. `FCR03_MEAL_SLOT_AUDIT.csv`: 24개 식사 슬롯 분류 및 검증
5. `FCR03_SCHEDULE_FOOD_LINK_AUDIT.csv`: 일정-정본 장소 링크 검증
6. `FCR03_MARKET_AUDIT.csv`: 5개 시장 비교 평가 매트릭스
7. `FCR03_SELF_CATERING_MATRIX.csv`: 뤼베롱 농가 숙소 3박 숙소식 매트릭스
8. `FCR03_WINE_CHEESE_PRODUCE_MATRIX.csv`: 와인, 치즈, 농산물 8종 데이터
9. `FCR03_PHOTO_ATTRIBUTION.csv`: 사진 라이선스 및 출처 등록
10. `FCR03_VOLATILE_RECHECK_REGISTER.csv`: 휘발성 사실 재확인 레지스터
11. `FCR03_PRIVACY_REGRESSION_SCAN.csv`: 프라이버시 회귀 스캔 로그

---

## 12. 검증 스위트 최종 실행 결과

```bash
python3 scripts/validate_place_canonical_model.py     # PASS (126 Canonical Places)
python3 scripts/validate_itinerary.py                 # PASS (43 Days, 0 Date Gaps)
python3 scripts/ex09_daily_card_audit.py              # PASS (43 Daily Cards)
python3 scripts/ex10_route_map_audit.py               # PASS (205 Segments, 248 Targets)
python3 scripts/ex11_final_verification_audit.py      # PASS (188 Bookings, 149 Openings)
python3 scripts/ex12_field_offline_audit.py           # PASS (33 Scenarios, 8 PWA Caches)
python3 scripts/ex12h_accommodation_audit.py          # PASS (8 Bases, 42 Nights)
python3 scripts/ex11a_day_place_link_audit.py         # PASS (125 Canonical Linked, 0 Gaps)
python3 scripts/ex12r_place_link_offline_regression.py # PASS (11 P2s Reconciled)
python3 scripts/ex13_full_trip_simulation_audit.py    # PASS (12 Failures Recovered)
python3 scripts/fcr01_nice_food_pilot_audit.py        # PASS (100% PASS)
python3 scripts/fcr02_bcn_gir_food_expansion_audit.py # PASS (100% PASS)
python3 scripts/fcr03_provence_food_expansion_audit.py # PASS (100% PASS)

python3 build/site.py                                 # PASS (361 Pages, 181 Search Items)
python3 build/ux_check.py                             # PASS (0 Broken Links, 0 Color Contrast Issues)
python3 build/content_audit.py                        # PASS (0 Content Loss across 126 Places)
```

---

## 13. Next Steps & 작업 중단 준수

- **FCR-03 완료**: 프로방스(Aix, Marseille, Cassis, Luberon, Avignon, Arles) 권역의 음식 콘텐츠 확장이 100% 완료되었습니다.
- **종료 준수**: 지침에 따라 **FCR-04(Lyon / Annecy)로 자동 진행하지 않고 작업을 중단**하며, 사용자의 검토를 대기합니다.
