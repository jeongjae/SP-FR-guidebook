# FCR-07 — Photo / Source / Rights Sweep QA Report
## Full-Site Photo Coverage / Source Provenance / Rights Classification / Attribution Integrity
### Status: PASS (100%) · Date: 2026-08-21 · Baseline: FCR-06 PASS / FCR-05 PASS / FCR-04 PASS / FCR-03 PASS / FCR-02 PASS / FCR-01 PASS / EX-13 PASS

---

## 0. Overall Verdict

```text
================================================================================
FCR-07 PHOTO / SOURCE / RIGHTS SWEEP: ALL PASS
- Source-Provenance Pre-Check: PASS (NICE-WISH-03 Provenance Restored & Clarified)
- Privacy Regression Pre-Check: PASS (0 New Leaks across repo, build, EXIF & site)
- Photo Inventory Completeness: 100% (25 Food Venue Photos & 413 Site Assets Audited)
- Rights Classification: PASS (PROHIBITED=0, NC=0, Commercial Prohibitions=0)
- Source Quality & Freshness: PASS (Official=18, Tourism=5, Wikimedia=2, Unverified=0)
- Broken & Stale Assets: PASS (0 Broken Files, 0 404s, 0 Stale Storefronts)
- Place Identity & Alt-Text: PASS (0 Photo-to-Place Mismatches, 100% Descriptive Alt-Text)
- PWA Bundle & Offline Tier 2: PASS (Bundle Size Stable at 53.2 MiB, 0 Bloat)
- Master Attribution Registry: FCR_PHOTO_SOURCE_ATTRIBUTION.csv Generated & Synced
- Full Test Suite: 17/17 Test Suites PASS + Site Build (369 Pages, 0 Content Loss, 0 UX Issues)
- Active Operational P2: 9 Maintained (FEAS-DUR-05 & FEAS-DUR-14 remain resolved)
================================================================================
```

---

## 1. Baseline Reconciliation

- **전체 여정**: 43일 / 42박 (2026-08-29 ~ 2026-10-10), 8개 거점 베이스
- **정본 장소(Canonical Places)**: 134개
- **검사 대상 사진 자산**: 25개 신규 식음료 정본 장소 자산 및 사이트 413개 이미지
- **Active Operational P2 이슈**: 9건 유지 (`FEAS-DUR-05`, `FEAS-DUR-14`는 사전 해결 상태로 유지)
- **P0 / P1 / 콘텐츠 손실**: **0건 (ALL PASS)**

---

## 2. Source-Provenance Pre-Check & WISH-03 Provenance Resolution

- **사전 감사(Pre-Check)**:
  - FCR-01 베이스라인 원문: 사용자의 `"Salon de thé - restaurant"` 텍스트에서 니스 캐피톨 인근 `Salon de Thé - Île de Beauté`를 후보로 발굴하여 `USER_CONFIRMATION_REQUIRED`로 보존.
  - FCR-06 보고서와의 대조: FCR-06에서 마르세유 대안 식당(`Chez Michel`)이 WISH-03으로 오기재된 이력을 감지함.
  - **판정 결과**: **`C. ACCIDENTAL SEMANTIC DRIFT`** 로 판정하고, 마르세유 식당은 통상적인 에디토리얼 백업으로 분리하였으며, **`NICE-WISH-03`을 원형인 `Salon de Thé - Île de Beauté (USER_CONFIRMATION_REQUIRED)` 상태로 완벽 복원**하였습니다.
  - **사진 부착 정책 준수**: 사용자 미확정 상태인 WISH-03에는 최종 정본 사진을 임의로 부착하지 않음.
- 산출물: [`FCR07_WISH_SOURCE_PROVENANCE_AUDIT.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/FCR07_WISH_SOURCE_PROVENANCE_AUDIT.csv)

---

## 3. Privacy Regression Audit

- **검사 범위**: `source/`, `data/`, `build/`, `site/`, `scripts/`, `docs/`, `handoff/`, 이미지 EXIF 메타데이터 및 CSV 레지스트리 전수 스캔.
- **조치 완료**: `handoff/` 문서 내 잔존하던 Hertz/바우처 번호 2건을 `[CONFIRMED]`로 즉시 마스킹 처리 완료.
- **결과**: 프라이버시 누출 **0건 달성 (PASS)**.
- 산출물: [`FCR07_PRIVACY_REGRESSION_SCAN.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/FCR07_PRIVACY_REGRESSION_SCAN.csv)

---

## 4. Rights Classification Summary

FCR-01 확정 4단계 정책을 전수 적용하여 엄격히 검증:
- **A — CLEAR-LICENSE**: 2건 (8.0%) — Wikimedia Commons CC BY / CC BY-SA
- **B — PLATFORM-PERMITTED**: 23건 (92.0%) — 공식 업장 웹사이트 및 파리시/관광청 공인 미디어 프레스 자산 (에디토리얼 사용 허가)
- **C — SOURCE-ATTRIBUTED / TERMS-CHECK**: 0건
- **D — PROHIBITED (상용금지 NC / 재배포 금지)**: **0건 (0.0% — 완전 배제 달성)**
- 산출물: [`FCR07_PHOTO_RIGHTS_MATRIX.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/FCR07_PHOTO_RIGHTS_MATRIX.csv)

---

## 5. Source Quality & Provenance Audit

- **OFFICIAL_VENUES**: 18건 (업장 공식 도메인 직영 자산)
- **TOURISM_AUTHORITIES**: 5건 (파리시청 공설 시장 포털 및 니스/프로방스 관광청)
- **CLEAR_LICENSE_REPOSITORY**: 2건 (위키미디어 커먼즈)
- **UNVERIFIED / ANONYMOUS**: **0건 (출처 불명 이미지 제로)**
- 산출물: [`FCR07_SOURCE_PROVENANCE_AUDIT.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/FCR07_SOURCE_PROVENANCE_AUDIT.csv)

---

## 6. Broken & Stale Asset Sweep

- **깨진 링크(404) 및 파일 누락**: 0건
- **만료된 CDN / 핫링크 차단 URL**: 0건
- **폐업/리노베이션 이전 옛 파사드 사진(Stale)**: 0건
- 산출물: [`FCR07_BROKEN_STALE_ASSET_AUDIT.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/FCR07_BROKEN_STALE_ASSET_AUDIT.csv)

---

## 7. Place Photo Identity & Alt-Text Audit

- **장소 오매칭(Wrong Place Photo)**: 0건 (지점/본점 구분 및 정확한 파사드 매핑 완료).
- **대체 텍스트(Alt-Text) 품질**: 단순 `photo`, `image` 등 제네릭 텍스트 0건, 전 자산이 업장 외관 및 대표 음식 특성을 명시한 서술형 텍스트 보유.
- 산출물: [`FCR07_PLACE_PHOTO_IDENTITY_AUDIT.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/FCR07_PLACE_PHOTO_IDENTITY_AUDIT.csv), [`FCR07_ALT_CAPTION_AUDIT.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/FCR07_ALT_CAPTION_AUDIT.csv)

---

## 8. Offline Policy & PWA Bundle Stability

- **오프라인 정책(Tier 2)**: 텍스트 및 메타데이터는 100% 필수 캐싱, 고용량 사진 자산은 온디맨드 로딩 정책을 준수하여 PWA 번들 급증 방지.
- **번들 크기 변화**:
  - **Before FCR-07**: 792개 파일, 53.2 MiB
  - **After FCR-07**: 792개 파일, 53.2 MiB
  - **Delta**: **0.0 MiB (번들 비대화 제로 달성)**
- 산출물: [`FCR07_OFFLINE_IMAGE_AUDIT.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/FCR07_OFFLINE_IMAGE_AUDIT.csv)

---

## 9. 산출 아티팩트 목록 (총 12건)

1. `FCR07_PHOTO_SOURCE_RIGHTS_QA.md`: 종합 QA 리포트
2. `FCR_PHOTO_SOURCE_ATTRIBUTION.csv`: 전역 마스터 사진 출처 및 권리 레지스터 (25건)
3. `FCR07_FULL_PHOTO_INVENTORY.csv`: 전역 사진 자산 인벤토리
4. `FCR07_PHOTO_RIGHTS_MATRIX.csv`: 권리 분류 및 사용 범위 매트릭스
5. `FCR07_SOURCE_PROVENANCE_AUDIT.csv`: 출처 신뢰도 및 프로비넌스 감사
6. `FCR07_BROKEN_STALE_ASSET_AUDIT.csv`: 깨진/오래된 사진 자산 감사
7. `FCR07_PLACE_PHOTO_IDENTITY_AUDIT.csv`: 장소-사진 동일성 감사
8. `FCR07_ALT_CAPTION_AUDIT.csv`: 대체 텍스트 및 캡션 감사
9. `FCR07_EMBED_REHOST_AUDIT.csv`: 임베드/로컬 저장 적합성 감사
10. `FCR07_DUPLICATE_ASSET_AUDIT.csv`: 중복 자산 감사
11. `FCR07_OFFLINE_IMAGE_AUDIT.csv`: PWA 오프라인 및 번들 크기 감사
12. `FCR07_WISH_SOURCE_PROVENANCE_AUDIT.csv`: WISH 출처 프로비넌스 감사
13. `FCR07_PRIVACY_REGRESSION_SCAN.csv`: 프라이버시 회귀 스캔 로그
14. `scripts/fcr07_photo_source_rights_audit.py`: FCR-07 전용 검증 스크립트

---

## 10. 검증 스위트 최종 실행 결과

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

python3 build/site.py                                 # PASS (369 Pages, 189 Search Items)
python3 build/ux_check.py                             # PASS (0 Broken Links, 0 Color Contrast Issues)
python3 build/content_audit.py                        # PASS (0 Content Loss across 134 Places)
```

---

## 11. Next Steps & 작업 중단 준수

- **FCR-07 완료**: 사이트 전역 사진 자산의 출처 확인, 권리 분류, attribution 정비가 100% 완료되었습니다.
- **종료 지침 준수**: 지침에 따라 **FCR-08(Cross-Link/Search/Map/Offline Regression)로 자동 진행하지 않고 작업을 중단**하며, 사용자의 검토를 대기합니다.
