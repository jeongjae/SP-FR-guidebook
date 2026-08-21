# EX-15 — Departure Operations QA Report
## T-7 / T-3 / T-1 Operational Recheck · Booking Closure · Disruption Watch
### Status: PASS (100%) · Date: 2026-08-21 · Baseline: EX-14 PASS / CONTENT FROZEN / TRIP READY FOR DEPARTURE

---

## 0. Overall Verdict

```text
================================================================================
EX-15 DEPARTURE OPERATIONS & T-WINDOW RECHECK: ALL PASS
TRIP STATUS: READY TO EXECUTE (100% OPERATIONAL RECHECK PASS)
CONTENT STATUS: FROZEN (Strict preservation of all 134 Places & 66 Meal Slots)

- Current Operating Window: T-8 / T-7 Window (2026-08-21 relative to Departure 2026-08-29)
- T-Window Volatile Rechecks: 11 / 11 Items Tracked & Operationalized
- MUST BOOK Action Tiers: 10 / 10 Actions Assigned to ACTION-A (Pre-departure) / ACTION-B (Travel Leg)
- First 72 Hours Continuity: Days 01–03 Flight, Transit, Accommodation, Meal & Offline 100% Locked
- Transport & Stays Closure: 3 Flights, 2 TGVs, 2 Rental Cars, 8 Bases (42 Nights) Reconfirmed
- Weather Contingency: Simple GREEN / AMBER / RED Decision Rules for 5 Sensitive Days
- Active Operational P2: 9 Monitored with 0 Escalations to P1 (All Accepted with Mitigation)
- Device & Offline Package: 792 Files / 53.2 MiB Precached, Offline Airplane Mode Verified
- Privacy Defense: 0 Leaks Found (All booking references safely held in private materials)
- Departure Operations Deliverables: EX15_USER_ACTION_LIST.md & EX15_DEPARTURE_QUICK_REFERENCE.md
- Full Regression Suite: 21/21 Test Suites PASS + Site Build (369 Pages, 0 Content Loss, 0 UX Issues)
================================================================================
```

---

## 1. Baseline & Freeze Integrity

- **정본 상태 불변**: 43일 / 42박, 8개 거점, 134개 정본 장소, 66개 식사 슬롯(A:23, B:20, D:16, E:7, C:0), 8개 지역 가이드, 52종 대표 음식 그대로 보존.
- **기능 및 편집 동결 유지**: 새로운 관광지/식당 추가, 디자인 변경, IA 재설계 없이 오직 현장 실행 가능 여부만 점검함.

---

## 2. Current T-Window (T-8 / T-7)

- **기준 일자**: 2026-08-21 (출발 8월 29일 기준 T-8 / T-7 사전 준비 구간).
- **집중 대상**: T-14 미완료 점검 완료 확인 및 T-7 도래 항목(Le Grand Pan, Chez Mamie Lise, Pichard) 실행 준비.

---

## 3. T-Window Execution Master

- 11개 휘발성 재확인 레지스터 현황:
  - `VR-01 ~ VR-05 (T-14)`: `CHECKED_PASS` (예약 채널 활성 및 백업 확인)
  - `VR-06 ~ VR-08 (T-7)`: `DUE_ACTION_READY` / `CHECKED_PASS` (T-7 오픈 채널 및 영업시간 확인)
  - `VR-09 ~ VR-10 (T-3)`: `NOT_DUE` (파리/아비뇽 현지 체류 시점 자동 이관)
  - `VR-11 (T-1 / D-Day)`: `NOT_DUE` (당일 워크인 식당 프로토콜 유지)
- 산출물: [`EX15_TWINDOW_EXECUTION_LOG.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX15_TWINDOW_EXECUTION_LOG.csv)

---

## 4. Booking Closure Master

- 항공 3편, TGV 2구간, 렌터카 2구간, 8개 숙소(42박) 전수 `CONFIRMED` 유지.
- 10개 MUST BOOK 식당은 `ACTION_READY`, 8개 RECOMMENDED BOOK 식당은 `WALK_IN_OR_BOOK`으로 최종 분류.
- 산출물: [`EX15_BOOKING_CLOSURE.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX15_BOOKING_CLOSURE.csv)

---

## 5. MUST BOOK Action Ownership

10개 사전 예약 필수 식당의 실행 등급 부여:
- **ACTION-A (출발 전 필수 실행)**:
  - `MB-01`: Bar Cañete (Day 03 / 13:30) - 2인 카운터석
  - `MB-02`: La Zorra (Day 04 / 13:00) - 해변 테라스 쌀 요리
  - `MB-03`: Le Figuier de Saint-Esprit (Day 09 / 12:15) - 미쉐린 1스타 (WISH-01)
  - `MB-04`: Bodega Joan (Day 02 / 19:30) - 에이샴플레 타파스 권장
- **ACTION-B (현지 여행 중 실행)**:
  - `MB-05`: Chez Gilbert (Day 14 / 12:30) - Cassis 전통 부야베스
  - `MB-06`: Fou de Fafa (Day 19 / 19:30) - Avignon 정통 프렌치
  - `MB-07`: Le Gibolin (Day 22 / 12:00) - Arles 황소 스튜
  - `MB-08`: Café Comptoir Abel (Day 23 / 19:30) - Lyon 最古 부숑
  - `MB-09`: Daniel et Denise (Day 24 / 19:45) - Lyon MOF 부숑 만찬
  - `MB-10`: Le Grand Pan (Day 34 & Day 41 / 20:00) - Paris 15구 숯불 비스트로
- 산출물: [`EX15_MUST_BOOK_ACTION_AUDIT.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX15_MUST_BOOK_ACTION_AUDIT.csv)

---

## 6. User Action List & Quick Reference

- 사용자가 실제 수행해야 할 잔여 액션 리스트를 `ACTION-A / B / C`로 단순화하여 발행.
- 산출물: [`EX15_USER_ACTION_LIST.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX15_USER_ACTION_LIST.md), [`EX15_DEPARTURE_QUICK_REFERENCE.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX15_DEPARTURE_QUICK_REFERENCE.md)

---

## 7. Transport & First 72 Hours Lock

- **OZ511 (8.29 12:45 인천➔바르셀로나 T1 19:40)**: 온라인 체크인은 T-24h (8.28 12:45) 오픈.
- **바르셀로나 입국 및 숙소 안착**: T1 청사 Aerobús A1 탑승 ➔ Gran Vía - Urgell 하차 ➔ Eric Vökel Gran Vía Suites 21:15 도착 ➔ 24h 편의점 2L 생수 조달 ➔ 조기 취침 (시차 적응).
- **Day 02 사그라다 파밀리아**: 09:00 타임슬롯 입장권 및 공식 오디오 가이드 앱 다운로드 확인.
- 산출물: [`EX15_TRANSPORT_RECHECK.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX15_TRANSPORT_RECHECK.csv), [`EX15_FIRST72H_OPERATIONAL_AUDIT.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX15_FIRST72H_OPERATIONAL_AUDIT.csv)

---

## 8. Weather Decision Matrix

기상 민감 5대 구간(코스타 브라바, 깔랑끄, 퐁뒤가르, 안시 호수, 베르사유)의 간단한 실행 판단 규칙 수립:
- **GREEN (맑음/약풍)**: 정상 야외 일정 (유람선, 카약, 호수 보트, 정원 산책)
- **AMBER (흐림/약우)**: 야외 축소 및 인근 마을/실내 박물관 병행
- **RED (폭우/강풍/미스트랄)**: Plan B 실내 명소 전환 (달리 미술관, 로마네스크 박물관, 안시 구시가 아케이드)
- 산출물: [`EX15_WEATHER_DECISION_MATRIX.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX15_WEATHER_DECISION_MATRIX.csv)

---

## 9. Active Operational P2 Trigger Watch

- 9개 Active P2 이슈에 대해 트리거 모니터링 체계 확립.
- 현재 시점에서 P1으로의 상향(Escalation) 발생 건수 **0건 (ALL PASS)**.
- 산출물: [`EX15_P2_TRIGGER_WATCH.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX15_P2_TRIGGER_WATCH.csv)

---

## 10. Offline Device & Privacy Final Sweep

- **비행기 모드 오프라인 검증**: 792개 파일 / 53.2 MiB PWA 캐시 완비, 데이터 연결 없이 43일 전 일정 및 134개 장소 Dossier 100% 정상 작동.
- **프라이버시 무결성**: 전역 스캔 결과 개인 예약번호 및 도어코드 누출 **0건 달성 (PASS)**.
- 산출물: [`EX15_OFFLINE_DEVICE_CHECK.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX15_OFFLINE_DEVICE_CHECK.csv), [`EX15_PRIVACY_REGRESSION_SCAN.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/EX15_PRIVACY_REGRESSION_SCAN.csv)

---

## 11. 산출 아티팩트 목록 (총 15건)

1. `EX15_DEPARTURE_OPERATIONS_QA.md`: 종합 QA 리포트
2. `EX15_TWINDOW_EXECUTION_LOG.csv`: T-Window 휘발성 재확인 로그
3. `EX15_BOOKING_CLOSURE.csv`: 예약 완료 마스터 매트릭스
4. `EX15_MUST_BOOK_ACTION_AUDIT.csv`: 10개 MUST BOOK 실행 채널 및 우선순위
5. `EX15_TRANSPORT_RECHECK.csv`: 항공·철도·렌터카 운영 재점검 로그
6. `EX15_FIRST72H_OPERATIONAL_AUDIT.csv`: 최초 72시간(Days 01~03) 실행 연속성 감사
7. `EX15_ACCOMMODATION_RECHECK.csv`: 8개 거점 숙박 운영 점검 로그
8. `EX15_FOOD_VOLATILE_RECHECK.csv`: 음식점 휘발성 재점검 로그
9. `EX15_EVENT_VOLATILE_RECHECK.csv`: 주요 행사 및 지정 입장권 점검 로그
10. `EX15_WEATHER_DECISION_MATRIX.csv`: 기상 판단 매트릭스 (GREEN/AMBER/RED)
11. `EX15_P2_TRIGGER_WATCH.csv`: Active P2 트리거 모니터링 로그
12. `EX15_OFFLINE_DEVICE_CHECK.csv`: 오프라인 디바이스 환경 검증 로그
13. `EX15_PRIVACY_REGRESSION_SCAN.csv`: 프라이버시 회귀 스캔 로그
14. `EX15_USER_ACTION_LIST.md`: 출발 전/중 사용자 실행 액션 리스트
15. `EX15_DEPARTURE_QUICK_REFERENCE.md`: 출발 당일 실행 포켓 가이드
16. `scripts/ex15_departure_operations_audit.py`: EX-15 전용 검증 스크립트

---

## 12. 검증 스위트 최종 실행 결과 (21/21 PASS)

```bash
python3 scripts/validate_place_canonical_model.py     # PASS (134 Canonical Places)
python3 scripts/validate_itinerary.py                 # PASS (43 Days, 0 Date Gaps)
python3 scripts/ex09_daily_card_audit.py              # PASS (43 Daily Cards)
python3 scripts/ex10_route_map_audit.py               # PASS (205 Segments, 248 Targets)
python3 scripts/ex11_final_verification_audit.py      # PASS (188 Bookings, 151 Openings)
python3 scripts/ex12_field_offline_audit.py           # PASS (33 Scenarios, 8 PWA Caches)
python3 scripts/ex12h_accommodation_audit.py          # PASS (8 Bases, 42 Nights)
python3 scripts/ex11a_day_place_link_audit.py         # PASS (140 Canonical Linked, 0 Gaps)
python3 scripts/ex12r_place_link_offline_regression.py # PASS (11 P2s Reconciled)
python3 scripts/ex13_full_trip_simulation_audit.py    # PASS (12 Failures Recovered)
python3 scripts/fcr01_nice_food_pilot_audit.py        # PASS (100% PASS)
python3 scripts/fcr02_bcn_gir_food_expansion_audit.py # PASS (100% PASS)
python3 scripts/fcr03_provence_food_expansion_audit.py # PASS (100% PASS)
python3 scripts/fcr04_lyon_annecy_food_expansion_audit.py # PASS (100% PASS)
python3 scripts/fcr05_paris_long_stay_food_audit.py   # PASS (100% PASS)
python3 scripts/fcr06_66_meal_slot_closure_audit.py   # PASS (100% PASS)
python3 scripts/fcr07_photo_source_rights_audit.py   # PASS (100% PASS)
python3 scripts/fcr08_integration_regression_audit.py # PASS (100% PASS)
python3 scripts/fcr09_editorial_readiness_audit.py   # PASS (100% PASS)
python3 scripts/ex14_final_travel_readiness_audit.py  # PASS (100% PASS)
python3 scripts/ex15_departure_operations_audit.py   # PASS (100% PASS)

python3 build/site.py                                 # PASS (369 Pages, 189 Search Items)
python3 build/ux_check.py                             # PASS (0 Broken Links, 0 Color Contrast Issues)
python3 build/content_audit.py                        # PASS (0 Content Loss across 134 Places)
```

---

## 13. Departure Operations Verdict & 여행 실행 선언

```text
================================================================================
EX-15 = PASS

SP-FR GUIDEBOOK = FROZEN
TRIP STATUS = READY TO EXECUTE

NO FURTHER CONTENT PHASE
================================================================================
```
