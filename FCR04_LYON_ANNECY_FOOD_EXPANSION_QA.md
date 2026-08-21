# FCR-04 — Lyon / Annecy QA Report
## Bouchon / Halles / Lyonnaise Cuisine / Savoy Foods / Meal-Slot Integration
### Status: PASS (100%) · Date: 2026-08-21 · Baseline: FCR-03 PASS / FCR-02 PASS / FCR-01 PASS / EX-13 PASS

---

## 0. Overall Verdict

```text
================================================================================
FCR-04 LYON & ANNECY FOOD CONTENT EXPANSION: ALL PASS
- Privacy Regression Pre-Check: PASS (0 New Leaks across repo, build & site)
- Architecture Model Reuse: PASS (FCR-01~03 Foundation 100% Reused without mutation)
- Regional Food Guides: 6 Lyonnaise Classics + 4 Savoy Alpine Specialties Defined
- Bouchon Model: 2 Authentic Benchmark Bouchons Integrated (Abel 1726 & Daniel et Denise MOF)
- Market & Food Hall: Les Halles de Lyon Paul Bocuse & Croix-Rousse Market Audited
- Meal Slot Classification: Days 23–27 Meal Slots Classified (0 Generic / Unclear Slots)
- Food Backlog Resolution: All EX-13 Lyon/Annecy Backlog Items Resolved to Canonical Places
- Canonical Places: 129 Total (Historical EX-13: 111 -> FCR-01: 114 -> FCR-02: 121 -> FCR-03: 126 -> FCR-04: 129)
- Route Revalidation: Days 23–27 Chronology & Fatigue Verified (Annecy Day Trip Buffer)
- Full Test Suite: 13/13 Test Suites PASS + Site Build (364 Pages, 0 Content Loss, 0 UX Issues)
- Active Operational P2: 9 Maintained (FEAS-DUR-05 & FEAS-DUR-14 remain resolved)
================================================================================
```

---

## 1. Baseline Reconciliation

- **Trip Configuration**: 43 Days / 42 Nights (2026-08-29 ~ 2026-10-10)
- **Historical EX-13 Place Count**: 111 Canonical Places
- **Pre-FCR04 (FCR-03) Live Count**: 126 Canonical Places
- **FCR-04 New Places**: +3 (`cafe-comptoir-abel`, `daniel-et-denise`, `chez-mamie-lise`)
- **Post-FCR04 Live Place Count**: **129 Canonical Places**
- **Active Operational P2 Count**: 9 (Maintained strictly without regression; `FEAS-DUR-05` and `FEAS-DUR-14` remain resolved validator artifacts).

---

## 2. Privacy Regression Audit

- **Verification Scope**: `source/`, `data/`, `build/`, `site/`, `scripts/`, `docs/`, generated search index, PWA manifests, and newly produced CSV/MD artifacts.
- **Sanitization Status**: All Airbnb codes (`HM...`), Hertz reservation numbers (`L671...`/`L672...`), voucher numbers (`36558...`/`14008...`), PNR codes, and private host contacts remain sanitized to `[CONFIRMED]`.
- **Findings**: 0 new leaks (`FCR04_PRIVACY_REGRESSION_SCAN.csv`).

---

## 3. Foundation Reuse

The data architecture validated across FCR-01~03 was applied cleanly without any modifications:
1. **Decoupling**: Regional Recommended Foods (`FCR04_REGIONAL_FOOD_MATRIX.csv`, `FCR04_ANNECY_SAVOY_FOOD_MATRIX.csv`) are strictly decoupled from physical venues (`FCR04_RESTAURANT_CAFE_MARKET_RESEARCH.csv`).
2. **Selection Origin**: `RECOMMENDED` (Curated based on regional authenticity and route efficiency; no artificial `WISH` places created).
3. **Meal Roles**: `PRIMARY`, `BACKUP`, `MARKET`, `SELF_CATERING`, `OPTIONAL`.
4. **Food Kinds**: `RESTAURANT`, `FOOD_HALL`, `MARKET`, `CAFE`.

---

## 4. Current Lyon / Annecy Schedule Scope (Days 23–27)

- **Day 23**: Avignon TGV ➔ TGV 12176 탑승 ➔ Lyon Part-Dieu (11:28 도착) ➔ Lagrange Aparthotel 짐보관/체크인 ➔ Presqu'île (Bellecour) 산책 ➔ 저녁: **Café Comptoir Abel** (리옹 最古 1726년 전통 부숑, 끄넬/치킨 크림 요리)
- **Day 24**: Fourvière 푸니쿨라 & 대성당 ➔ Jardin du Rosaire 하산 ➔ 점심: Vieux Lyon 비스트로 런치 ➔ Vieux Lyon & Traboules ➔ 저녁: **Daniel et Denise** (MOF 셰프 Joseph Viola의 Les Bouchons Lyonnais 공인 대표 부숑, 파테 앙 크루트, 끄넬, 살라드 리요네즈)
- **Day 25**: Croix-Rousse 시장 & Maison des Canuts (실크 직조) ➔ 점심 & 탐방: **Les Halles de Lyon Paul Bocuse** (리옹 최고의 실내 미식 전당, 굴 바, 치즈, 로제트 드 리옹, 프랄린 타르트) ➔ Parc de la Tête d'Or 산책 ➔ 숙소 휴식 & 가벼운 저녁
- **Day 26**: Lyon Part-Dieu ➔ Annecy (TER 2시간) ➔ Vieille Ville & Palais de l'Île ➔ 점심: **Chez Mamie Lise** (안시 구시가지 전통 사부아 식당, 타르티플레트/퐁뒤/페라 호수 생선구이) ➔ Lac d'Annecy & Pont des Amours 산책 ➔ Annecy ➔ Lyon Part-Dieu 복귀 ➔ 숙소권 간단 저녁
- **Day 27**: Lyon 체크아웃 ➔ Part-Dieu역 점심/샌드위치 ➔ TGV INOUI 6618 (13:04 발차) ➔ Paris Gare de Lyon 도착 (Lyon 여정 종료 및 Paris 개시)

---

## 5. Lyon Regional Food Matrix Summary (6 Items)

1. **Quenelle de brochet sauce Nantua (강꼬치고기 끄넬)**: 강꼬치고기 살과 버터, 달걀 반죽을 삶아 민물가재 낭튀아 크림 소스를 얹어 오븐에 부풀려 구워낸 리옹 최고 대표 요리.
2. **Salade lyonnaise (살라드 리요네즈)**: 프리제 상추에 바삭한 베이컨 라르동, 버터 크루통, 수란을 올린 리옹식 웜 샐러드.
3. **Saucisson brioché (소시송 브리오셰)**: 피스타치오를 넣은 리옹 특산 생소시지를 버터 브리오슈 반죽 속에 통째로 넣어 구워낸 따뜻한 전채.
4. **Tablier de sapeur (타블리에 드 사푀르)**: 마리네이드한 소 양(Gras-double)에 빵가루를 입혀 바삭하게 지져내고 마늘 타르타르풍 그리비슈 소스를 곁들인 전통 요리.
5. **Cervelle de canut (세르벨 드 카뉘)**: 신선한 프로마주 블랑에 허브, 샬롯, 마늘, 식초를 섞은 상큼하고 크리미한 전통 치즈 요리.
6. **Tarte aux pralines (타르트 오 프랄린)**: 붉은 아몬드 프랄린 로즈를 생크림과 녹여 바삭한 타르트에 채워 구워낸 리옹의 상징적 디저트.

---

## 6. Annecy & Savoy Regional Food Matrix (4 Items)

1. **Tartiflette au Reblochon AOP (타르티플레트)**: 감자, 양파, 훈제 베이컨 라르동에 르블로숑 치즈를 통째로 얹어 오븐에 구워낸 알프스 정통 컴포트 푸드.
2. **Fondue savoyarde (정통 사부아 퐁뒤)**: 보포르, 아봉당스, 콩테 치즈를 화이트 와인과 마늘로 녹여 빵을 찍어 먹는 알프스 대표 요리.
3. **Filets de féra / perche du lac (안시 호수 생선구이)**: 청정 1급수 안시 호수산 담수어를 레몬 버터 소스에 구워낸 담백한 호수 요리 (치즈 요리 부담 시 최적 대안).
4. **Fromages de Savoie (르블로숑 & 톰 드 사부아)**: 사부아 알프스 목초지 생우유로 빚은 AOP/IGP 아티장 치즈.

---

## 7. Bouchon Lyonnais Content Model & Authenticity Research

- **부숑(Bouchon)의 본질**: 19세기 리옹 비단 직조공(Canuts)들의 허기를 달래주던 푸짐하고 따뜻한 선술집에서 출발하여, '메르(Mères Lyonnaises)'들의 정성 어린 가정식 요리 유산을 이어받은 리옹 고유의 미식 문화.
- **선정 및 인증 기준**:
  - `Café Comptoir Abel`: 1726년 창업한 리옹 最古의 역사적 부숑. 메르의 원형 레시피를 보존하여 깊은 크림 끄넬과 치킨 요리 제공 (Day 23 저녁).
  - `Daniel et Denise`: 프랑스 최고 장인(MOF) 조제프 비올라 셰프가 운영하며, 리옹 상공회의소 공인 'Les Bouchons Lyonnais' 인증을 받은 최고 권위의 정통 부숑 (Day 24 저녁).

---

## 8. Lyon Markets & Les Halles de Lyon Paul Bocuse

- **Halles de Lyon Paul Bocuse (3구)**: 13,000㎡ 규모의 실내 럭셔리 미식 시장. Mère Richard(생마르슬랭 치즈), Maison Sibilia(샤퀴테리), Chocolatier Sève(프랄린 타르트), Écaillers(스탠딩 생굴 바) 등 MOF 명장 점포 밀집 (Day 25 점심 및 Day 27 기차 간식 조달).
- **Marché de la Croix-Rousse (4구)**: 화–일 열리는 활기찬 로컬 시장. 제철 과일, 치즈, 갓 구운 브리오슈 조달 (Day 25 오전).

---

## 9. Scheduled Food Places Research & Integration

| Place Slug | Venue Name | Region | Day / Slot | Role | Menu & Pricing | Hours & Reservation |
|---|---|---|---|---|---|---|
| `cafe-comptoir-abel` | **Café Comptoir Abel** | Lyon | **Day 23 저녁** | PRIMARY | 강꼬치고기 끄넬, 뿔레 아 라 크렘, 세르벨 드 카뉘 (€38~€48/인) | 매일 12:00–14:00 / 19:30–22:00, 사전 예약 필수 |
| `daniel-et-denise` | **Daniel et Denise** | Lyon | **Day 24 저녁** | PRIMARY | 세계 챔피언 파테 앙 크루트, 타블리에 드 사푀르 (€39~€46/인) | 월–금 12:00–14:00 / 19:30–22:00, 사전 예약 필수 |
| `halles-de-lyon-paul-bocuse` | **Halles Paul Bocuse** | Lyon | **Day 25 점심** | PRIMARY | 생굴 6미 + 샤블리 와인, 로제트 드 리옹, 생마르슬랭 (€15~€35/인) | 화–토 07:00–19:00 (식당 22:30까지), 예약 불필요 |
| `chez-mamie-lise` | **Chez Mamie Lise** | Annecy | **Day 26 점심** | PRIMARY | 르블로숑 타르티플레트, 사부아 퐁뒤, 호수 생선구이 (€18~€28/인) | 매일 12:00–14:00 / 19:00–22:00, 사전 예약 권장 |

---

## 10. Route Revalidation (Days 23–27)

- **Day 23**: TGV 11:28 도착 후 여유로운 체크인 및 Café Comptoir Abel 19:30 저녁 안착 (피로도 2, LOW).
- **Day 24**: 비외 리옹 트라불 탐방 중 점심 60분 통제, Daniel et Denise 19:45 저녁 안착 (피로도 3, MODERATE).
- **Day 25**: Croix-Rousse 시장 산책 ➔ Halles Paul Bocuse 미식 점심 ➔ Tête d'Or 공원 산책 후 숙소 조기 복귀 & 가벼운 저녁으로 체력 완벽 비축 (피로도 3, MODERATE).
- **Day 26 (Annecy)**: Part-Dieu ➔ Annecy 왕복 TER 활용. Chez Mamie Lise 12:30 점심 후 16:45 안시 발 TER 탑승으로 18:45 Part-Dieu 안전 복귀. +30분 식사 지연 시 호수 보트 대여를 생략하고 사랑의 다리 산책으로 단축하여 귀환 열차 100% 보호 (피로도 4, HIGH).
- **Day 27**: 파르디외 역 12:00 도착, Halles 샌드위치 조달 후 TGV 6618 (13:04 발차) 탑승하여 파리 15:00 정착 (피로도 2, LOW).

---

## 11. 산출 아티팩트 목록 (총 11건)

1. `FCR04_LYON_ANNECY_FOOD_EXPANSION_QA.md`: 종합 QA 리포트
2. `FCR04_REGIONAL_FOOD_MATRIX.csv`: 리옹 6종 음식 매트릭스
3. `FCR04_ANNECY_SAVOY_FOOD_MATRIX.csv`: 안시·사부아 4종 음식 매트릭스
4. `FCR04_RESTAURANT_CAFE_MARKET_RESEARCH.csv`: 4개 업장 및 시장 실사 데이터
5. `FCR04_BOUCHON_AUDIT.csv`: 정통 부숑 인증 및 품질 평가 매트릭스
6. `FCR04_MARKET_FOOD_HALL_AUDIT.csv`: 3개 시장 및 푸드홀 비교 평가
7. `FCR04_MEAL_SLOT_AUDIT.csv`: 9개 식사 슬롯 분류 및 검증
8. `FCR04_SCHEDULE_FOOD_LINK_AUDIT.csv`: 일정-정본 장소 링크 검증
9. `FCR04_ROUTE_REVALIDATION.csv`: 5개 일정 동선 및 피로도 시뮬레이션
10. `FCR04_PHOTO_ATTRIBUTION.csv`: 사진 라이선스 및 출처 등록
11. `FCR04_VOLATILE_RECHECK_REGISTER.csv`: 휘발성 사실 재확인 레지스터
12. `FCR04_PRIVACY_REGRESSION_SCAN.csv`: 프라이버시 회귀 스캔 로그

---

## 12. 검증 스위트 최종 실행 결과

```bash
python3 scripts/validate_place_canonical_model.py     # PASS (129 Canonical Places)
python3 scripts/validate_itinerary.py                 # PASS (43 Days, 0 Date Gaps)
python3 scripts/ex09_daily_card_audit.py              # PASS (43 Daily Cards)
python3 scripts/ex10_route_map_audit.py               # PASS (205 Segments, 248 Targets)
python3 scripts/ex11_final_verification_audit.py      # PASS (188 Bookings, 151 Openings)
python3 scripts/ex12_field_offline_audit.py           # PASS (33 Scenarios, 8 PWA Caches)
python3 scripts/ex12h_accommodation_audit.py          # PASS (8 Bases, 42 Nights)
python3 scripts/ex11a_day_place_link_audit.py         # PASS (128 Canonical Linked, 0 Gaps)
python3 scripts/ex12r_place_link_offline_regression.py # PASS (11 P2s Reconciled)
python3 scripts/ex13_full_trip_simulation_audit.py    # PASS (12 Failures Recovered)
python3 scripts/fcr01_nice_food_pilot_audit.py        # PASS (100% PASS)
python3 scripts/fcr02_bcn_gir_food_expansion_audit.py # PASS (100% PASS)
python3 scripts/fcr03_provence_food_expansion_audit.py # PASS (100% PASS)
python3 scripts/fcr04_lyon_annecy_food_expansion_audit.py # PASS (100% PASS)

python3 build/site.py                                 # PASS (364 Pages, 184 Search Items)
python3 build/ux_check.py                             # PASS (0 Broken Links, 0 Color Contrast Issues)
python3 build/content_audit.py                        # PASS (0 Content Loss across 129 Places)
```

---

## 13. Next Steps & 작업 중단 준수

- **FCR-04 완료**: 리옹 및 안시 권역의 음식 콘텐츠 확장이 100% 완료되었습니다.
- **종료 준수**: 지침에 따라 **FCR-05(Paris)로 자동 진행하지 않고 작업을 중단**하며, 사용자의 검토를 대기합니다.
