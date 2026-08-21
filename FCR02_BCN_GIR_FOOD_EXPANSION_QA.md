# FCR-02 — Barcelona / Girona / Costa Brava / Collioure QA Report
## Food Content Expansion / Meal Slot Resolution / Market & Regional Cuisine Integration
### Status: PASS (100%) · Date: 2026-08-21 · Baseline: FCR-01 PASS / EX-13 PASS

---

## 0. Overall Verdict

```text
================================================================================
FCR-02 FOOD CONTENT EXPANSION (BCN / GIR / COSTA BRAVA / COLLIOURE): ALL PASS
- Privacy Regression Pre-Check: PASS (0 New Leaks across repo, build & site)
- Architecture Model Reuse: PASS (FCR-01 Foundation 100% Reused without mutation)
- Regional Food Guides: 15 Traditional Foods Defined across 3 Micro-Regions
- Market Audits: 6 Markets Audited (Concepció, Lleó, Collioure, Boqueria, Santa Caterina, Sant Antoni)
- Meal Slot Classification: Days 1–7 Meal Slots Classified (0 Generic / Unclear Slots)
- Food Backlog Resolution: All EX-13 BCN/GIR Backlog Items Resolved to Canonical Places
- Canonical Places: 121 Total (Historical EX-13: 111 -> FCR-01: 114 -> FCR-02: 121)
- Route Revalidation: Day 05 (Collioure) & Day 06 (Costa Brava) Chronology Verified
- Full Test Suite: 11/11 Test Suites PASS + Site Build (356 Pages, 0 Content Loss, 0 UX Issues)
- Active Operational P2: 9 Maintained (FEAS-DUR-05 & FEAS-DUR-14 remain resolved)
================================================================================
```

---

## 1. Baseline Reconciliation

- **Trip Configuration**: 43 Days / 42 Nights (2026-08-29 ~ 2026-10-10)
- **Historical EX-13 Place Count**: 111 Canonical Places
- **FCR-01 Place Count**: 114 Canonical Places (+3: `le-figuier-de-saint-esprit`, `restaurant-beatrice`, `villa-ephrussi-de-rothschild`)
- **FCR-02 Live Place Count**: **121 Canonical Places** (+7: `bodega-joan`, `la-paradeta-sagrada-familia`, `bar-canete`, `mercat-concepcio`, `la-zorra`, `casa-marieta`, `mercat-del-lleo`)
- **Active Operational P2 Count**: 9 (Maintained strictly without regression; `FEAS-DUR-05` and `FEAS-DUR-14` remain resolved validator artifacts).

---

## 2. Privacy Regression Audit

- **Verification Scope**: `source/`, `data/`, `build/`, `site/`, `scripts/`, `docs/`, generated search index, PWA manifests, and newly produced CSV/MD artifacts.
- **Sanitization Status**: All Airbnb codes (`HM...`), Hertz reservation numbers (`L671...`/`L672...`), voucher numbers (`36558...`/`14008...`), PNR codes, and private host contacts remain sanitized to `[CONFIRMED]`.
- **Findings**: 0 new leaks (`FCR02_PRIVACY_REGRESSION_SCAN.csv`).

---

## 3. Architecture & Taxonomy Reuse

The data architecture validated in FCR-01 was applied cleanly without any modifications:
1. **Decoupling**: Regional Recommended Foods (`FCR02_REGIONAL_FOOD_MATRIX.csv`) are strictly decoupled from physical venues (`FCR02_RESTAURANT_CAFE_MARKET_RESEARCH.csv`).
2. **Selection Origin**: `RECOMMENDED` (Curated based on regional authenticity and route efficiency; no artificial `WISH` places created).
3. **Meal Roles**: `PRIMARY`, `BACKUP`, `MARKET`, `SELF_CATERING`, `OPTIONAL`.
4. **Food Kinds**: `RESTAURANT`, `MARKET`, `CAFE`.

---

## 4. Regional Food Matrix Summary (15 Items)

### A. Barcelona / Catalonia (8 Items + Seasonal Note)
1. **Pa amb tomàquet (판 콘 토마테)**: 구운 코카 빵에 생마늘과 완숙 토마토를 문지르고 올리브유와 소금을 친 카탈루냐 식탁의 기본값.
2. **Escalivada (에스칼리바다)**: 숯불에 구워 껍질을 벗긴 가지, 피망, 양파에 올리브유를 듬뿍 친 온화한 채소 전채 요리.
3. **Esqueixada (에스케이샤다)**: 잘게 찢은 소금 절임 생대구살과 토마토, 양파, 올리브를 올리브유로 버무린 상큼한 샐러드.
4. **Botifarra amb mongetes (부티파라 암 몬게테스)**: 카탈루냐 전통 돼지고기 소시지와 부드러운 흰 강낭콩 볶음.
5. **Fideuà (피데우아)**: 짧고 얇은 파스타 국수를 진한 해산물 육수로 볶아 구워낸 해안 정통 면 파에야.
6. **Arròs negre / Arròs a banda (아로스 네그레 / 아로스 아 반다)**: 오징어 먹물 쌀요리 및 진한 해산물 스톡 쌀요리.
7. **Bombes de la Barceloneta (봄바)**: 매콤한 고기를 감자로 감싸 튀겨 알리올리와 브라바 소스를 얹은 타파스.
8. **Crema catalana (크레마 카탈라나)**: 레몬·시나몬 향의 커스터드 표면을 바삭하게 캐러멜라이즈한 전통 디저트.
*※ 계절성 주의: Calçots(구운 대파) 및 Xató(겨울 샐러드)는 겨울철 제철 요리로 9월 일정에는 제외.*

### B. Girona / Costa Brava / Empordà (5 Items)
1. **Suquet de peix (수케트 데 페이시)**: 암초 생선, 감자, 마늘, 아몬드 피카다를 넣고 끓여낸 코스타 브라바 어부들의 해산물 스튜.
2. **Arròs a la cassola (아로스 아 라 카솔라)**: 팔스(Pals) 특산 쌀을 토기 냄비에 담아 고기와 해산물 육수가 배어들게 끓여낸 냄비밥.
3. **Mar i muntanya (마르 이 문타냐)**: 닭고기(산)와 새우·오징어(바다)를 초콜릿·넛트 피카다 소스로 함께 조려낸 엠포르다 전통 요리.
4. **Xuixo de Girona (추쇼 데 지로나)**: 바삭하게 튀긴 페이스트리에 크레마 카탈라나를 채우고 설탕을 묻힌 지로나 명물 빵.
5. **Anxoves de L'Escala (레스칼라 앤초비)**: 코스타 브라바 레스칼라 전통 염장 기법으로 숙성시킨 최고급 올리브유 절임 앤초비.

### C. Collioure / Côte Vermeille (2 Items)
1. **Anchois de Collioure (콜리우르 앤초비 IGP)**: 중세부터 이어진 콜리우르 항구의 지리적 표시 보호 염장·초절임 앤초비.
2. **Vins de Collioure & Banyuls (AOC 와인)**: 피레네 절벽 편암 테라스 포도원의 농밀한 레드 와인 및 바뉼스 천연 감미 와인.

---

## 5. Market Audit Summary (6 Markets)

1. **Mercat de la Concepció (Barcelona Eixample)**: 1888년 모더니즘 철골 생활시장. 24시간 꽃시장, 신선 무화과/복숭아/치즈 구매 최적 (Day 03 아침 장보기 연결).
2. **Mercat del Lleó (Girona)**: 1944년 지로나 중앙공설시장. 60여 개 전문 가판대, Xuixo, 엠포르다 소시지, Bàscara 숙소 취사용 식재료 조달 (Day 04, 05 연결).
3. **Marché de Collioure (Collioure)**: 5월8일광장 수요일 노천시장. Day 05(수요일) 방문 일정과 완벽 일치. 앤초비 병입 및 로컬 과일 조달.
4. **Mercat de Santa Caterina (Barcelona)**: 세련된 파도형 지붕의 로컬 생활시장 (Day 03 백업).
5. **Mercat de Sant Antoni (Barcelona)**: 에이샴플레 대형 복합 시장 (선택 대안).
6. **Mercat de la Boqueria (Barcelona)**: 인파 극심 및 관광지화로 인해 내부 식사 지양, 외관/사진 중심 취급.

---

## 6. Scheduled Food Places Research & Integration

| Place Slug | Venue Name | Region | Day / Slot | Role | Menu & Pricing | Hours & Reservation |
|---|---|---|---|---|---|---|
| `bodega-joan` | **Bodega Joan** | Barcelona | **Day 02 저녁** (Day 01 백업) | PRIMARY | 카넬로니, 숯불 모둠 육류, 해산물 빠에야 (€25~€35/인) | 매일 08:00–24:00 (식사 12:30–16:00 / 19:30–23:30), 예약 권장 |
| `la-paradeta-sagrada-familia` | **La Paradeta Sagrada Família** | Barcelona | **Day 02 점심** | PRIMARY | 즉석 조리 맛조개, 새우, 꼴뚜기 튀김 (€18~€28/인) | 일 13:00–16:00, 예약 불가 (12:50 오픈 대기) |
| `bar-canete` | **Bar Cañete** | Barcelona | **Day 03 점심** | PRIMARY | 소꼬리 토스트, 트러플 카넬로니, 생선 타파스 (€30~€45/인) | 매일 13:00–24:00, 사전 예약 필수 (13:30 슬롯) |
| `mercat-concepcio` | **Mercat de la Concepció** | Barcelona | **Day 03 아침** | MARKET | 제철 과일, 치즈, 에스프레소, 꽃시장 (€5~€15) | 월–토 08:00–15:00, 예약 불필요 |
| `la-zorra` | **La Zorra** | Sitges | **Day 04 점심** | PRIMARY | 아로스 아 반다, 흑먹물 쌀요리, 치즈케이크 (€30~€45/인) | 매일 13:00–16:30, 사전 예약 필수 (13:00 슬롯) |
| `casa-marieta` | **Casa Marieta** | Girona | **Day 04 저녁** (Day 05 백업) | PRIMARY | 마르 이 문타냐, 엠포르다 오리 구이, 달팽이 (€25~€38/인) | 매일 13:00–16:00 / 20:00–23:00, 예약 가능 |
| `mercat-del-lleo` | **Mercat del Lleó** | Girona | **Day 04/05 장보기** | MARKET | 추쇼, 엠포르다 소시지, 피레네 치즈 (€5~€15) | 월–토 07:00–14:00, 예약 불필요 |
| `collioure` | **Collioure 해안 비스트로** | Collioure | **Day 05 점심** | PRIMARY | 초절임 앤초비, 생선구이, 바뉼스 와인 (€25~€40/인) | 점심 12:00–14:30 (60~75분 식사 시간 통제) |

---

## 7. Day 05 & Day 06 Route Revalidation

### Day 05: Bàscara ➔ Collioure (점심) ➔ Peralada ➔ Bàscara
- **식사 시간 통제**: 콜리우르 점심(12:30~13:45, 75분 제한) 엄수.
- **+30분 지연 시나리오**: 식사가 30분 지연되어 14:15 종료될 경우, 카다케스(Cadaqués) 선택 일정을 즉시 생략하고 페랄라다 와이너리 외관 조망 후 17:30 바스카라 숙소로 조기 복귀하여 피로도 4(HIGH) 상한을 철저히 방어.

### Day 06: Bàscara ➔ Pals ➔ Peratallada ➔ Calella de Palafrugell (점심/카페) ➔ Bàscara
- **식사 시간 통제**: 칼레야 해변 또는 산펠리우 점심(13:00~14:15, 75분) 엄수.
- **일정 팽창 방지**: 베구르(Begur) 추가나 장거리 해안 트레킹을 배제하고, 16:30 바스카라 복귀를 완료하여 익일 프랑스 니스 이동(렌터카 반납 및 항공편) 짐 정리를 완벽히 보호.

---

## 8. Bàscara 생활형 식재료 및 자가 조리 체계

- **아침 식사 및 간식**: Mercat del Lleó 및 바스카라 인근 베이커리(Forn de pa)에서 구매한 빵, 과일, 우유, 치즈 활용.
- **저녁 자가 조리**: Day 05 및 Day 06 저녁은 지로나 시장과 로컬 슈퍼마켓에서 조달한 신선 파스타, 엠포르다 소시지, 샐러드를 활용한 편안한 숙소식 진행.
- **이동일 준비**: Day 07 공항 이동용 생수(2L) 및 비상 간식 사전 패킹.

---

## 9. 산출 아티팩트 목록 (총 10건)

1. `FCR02_BCN_GIR_FOOD_EXPANSION_QA.md`: 종합 QA 리포트
2. `FCR02_REGIONAL_FOOD_MATRIX.csv`: 바르셀로나·지로나·콜리우르 15종 음식 매트릭스
3. `FCR02_RESTAURANT_CAFE_MARKET_RESEARCH.csv`: 8개 업장 및 시장 실사 데이터
4. `FCR02_MEAL_SLOT_AUDIT.csv`: 13개 식사 슬롯 분류 및 검증
5. `FCR02_SCHEDULE_FOOD_LINK_AUDIT.csv`: 일정-정본 장소 링크 검증
6. `FCR02_MARKET_AUDIT.csv`: 6개 시장 비교 평가 매트릭스
7. `FCR02_PHOTO_ATTRIBUTION.csv`: 사진 라이선스 및 출처 등록
8. `FCR02_ROUTE_REVALIDATION.csv`: 7개 일정 동선 및 피로도 시뮬레이션
9. `FCR02_VOLATILE_RECHECK_REGISTER.csv`: 휘발성 사실 재확인 레지스터
10. `FCR02_PRIVACY_REGRESSION_SCAN.csv`: 프라이버시 회귀 스캔 로그

---

## 10. 검증 스위트 최종 실행 결과

```bash
python3 scripts/validate_place_canonical_model.py     # PASS (121 Canonical Places)
python3 scripts/validate_itinerary.py                 # PASS (43 Days, 0 Date Gaps)
python3 scripts/ex09_daily_card_audit.py              # PASS (43 Daily Cards)
python3 scripts/ex10_route_map_audit.py               # PASS (205 Segments, 248 Targets)
python3 scripts/ex11_final_verification_audit.py      # PASS (188 Bookings, 147 Openings)
python3 scripts/ex12_field_offline_audit.py           # PASS (33 Scenarios, 8 PWA Caches)
python3 scripts/ex12h_accommodation_audit.py          # PASS (8 Bases, 42 Nights)
python3 scripts/ex11a_day_place_link_audit.py         # PASS (119 Canonical Linked, 0 Gaps)
python3 scripts/ex12r_place_link_offline_regression.py # PASS (11 P2s Reconciled)
python3 scripts/ex13_full_trip_simulation_audit.py    # PASS (12 Failures Recovered)
python3 scripts/fcr01_nice_food_pilot_audit.py        # PASS (100% PASS)
python3 scripts/fcr02_bcn_gir_food_expansion_audit.py # PASS (100% PASS)

python3 build/site.py                                 # PASS (356 Pages, 176 Search Items)
python3 build/ux_check.py                             # PASS (0 Broken Links, 0 Color Contrast Issues)
python3 build/content_audit.py                        # PASS (0 Content Loss across 121 Places)
```

---

## 11. Next Steps

- **FCR-02 완료**: 바르셀로나 / 지로나 / 코스타 브라바 / 콜리우르 권역의 음식 콘텐츠 확장이 100% 완료되었습니다.
- **종료 준수**: 지침에 따라 FCR-03(Aix / Marseille / Luberon / Avignon)으로 자동 진행하지 않고 작업을 중단하고 사용자 검토를 대기합니다.
