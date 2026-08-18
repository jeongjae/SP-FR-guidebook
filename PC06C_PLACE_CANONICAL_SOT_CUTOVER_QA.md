# PC-06C Place Canonical SOT Pipeline Cutover QA Report

**작성일**: 2026-08-18  
**상태**: **ALL PASS (Pipeline Cutover & Validation Complete)**  
**브랜치**: `feat/pc-06c-canonical-cutover`  

---

## 1. Previous Pipeline vs New Canonical Pipeline

### 1.1 이전 파이프라인 (Previous Pipeline)
```text
[20_Regional_Chapters/*.md] (Region Chapter)
             │
             ▼ (매 빌드 시 promote_places.py 자동 실행 — 덮어쓰기 발생)
[30_Places/*.md] (파생물 Derivative)
             │
             ▼ (model.py / render.py)
[site/places/*.html]
```
- **문제점**: `30_Places`를 직접 수정해도 다음 빌드 시 챕터 원고에 의해 덮어써짐.

### 1.2 신규 정본 파이프라인 (New Canonical Pipeline — IMPLEMENTED)
```text
[source/CURRENT/30_Places/<slug>.md] (★ Canonical Place SOT)
             │
   ┌─────────┴───────────────────────┐
   ▼                                 ▼
[build/model.py: load_place_bodies]  [Region / Day / Search / Map]
   │                                 │
   ▼                                 ▼
[site/places/<slug>.html]            [site/guide/*.html, daily/*.html]
(Full 5-Layer Guide)                 (Compact Cards & Direct Links)
```
- **개선점**: `30_Places/<slug>.md`가 유일한 정본이 되며, 빌드 시 절대 덮어쓰지 않고 직접 소비됨.

---

## 2. promote_places.py의 최종 상태 (Final Role)

- **역할**: **LEGACY / ONE-TIME MIGRATION TOOL ONLY**
- **조치**: `build/site.py`의 `main()`에서 자동 호출 제거.
- **보장**: `30_Places/<slug>.md`를 수동 편집하거나 고도화한 후 `python3 build/site.py`를 실행해도 내용이 100% 보존됨 (Overwrite Protection PASS).

---

## 3. Barcelona 5개 파일럿 장소 마이그레이션 및 중복 제거 (Dedup Result)

- **대상 장소**: `sagrada-familia`, `sant-pau-recinte-modernista`, `barri-gotic`, `macba`, `biblioteca-de-catalunya`
- **Region 원고 (`04_Barcelona_Sitges_v2.0.md`)**:
  - 장문 텍스트(역사, 건축, Deep Guide, 상세 실용)를 제거하고 **Compact Summary / Why Go 요약 / Editor's Verdict / 체류시간 / [상세 가이드 보기] 링크**로 전환.
- **정본 장소 파일 (`30_Places/<slug>.md`)**:
  - 5-Layer 표준(Facts, Strategy, Experience, Deep Guide, Practical)의 완벽한 정본 원고로 보존.
- **콘텐츠 손실**: **0건 (Content Loss = 0)** — 상세 맵핑은 [`PLACE_DEDUP_MIGRATION_MAP_BARCELONA.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-2/PLACE_DEDUP_MIGRATION_MAP_BARCELONA.md)에 기록.

---

## 4. Trip Layer Separation Result (일정 레이어 격리)

- Barcelona 5개 장소 본체에서 특정 여행 일자(`8월 30일`, `8월 31일`, `Day 2` 등)를 완전히 제거하고 일반적인 시간대/방문 조건으로 정제.
- 장소 본문이 여행 일정 변경으로부터 완전히 독립됨.

---

## 5. 검증 결과 요약 (Validation Suite ALL PASS)

| 검증 항목 | 대상 도구 | 결과 | 세부 내용 |
|---|---|---|---|
| **Place Overwrite Protection** | `validate_place_canonical_model.py` | **PASS** | 빌드 전후 94개 Place 파일 SHA-256 해시 100% 일치 |
| **Duplicate Long-Form Detection** | `validate_place_canonical_model.py` | **PASS** | Barcelona 5개 장소의 Region 원고 내 중복 장문 0건 |
| **Trip Layer Separation** | `validate_place_canonical_model.py` | **PASS** | Barcelona 5개 장소 본체 내 일자 하드코딩 0건 |
| **Reference Integrity** | `validate_place_canonical_model.py` | **PASS** | Region ↔ Place ↔ Day Stop 참조 무결성 100% |
| **Content Audit Guard** | `build/content_audit.py` | **PASS** | 94개 장소 485개 문단 검사, 콘텐츠 손실 0건 |
| **UX & Outdoor Contrast** | `build/ux_check.py` | **PASS** | 335개 페이지 전수 명암비 및 하단탭/카드 통과 |
| **Static Site Build** | `build/site.py` | **PASS** | 335개 정적 페이지 정상 빌드 |

---

## 6. 최종 판정 및 다음 권역 추천

- **최종 판정**: **PASS (Pipeline Cutover 완료)**
- **후속 단계 (Next Region Rollout)**:
  - Barcelona에서 확정된 SOT 파이프라인 구조를 바탕으로 **Girona & Costa Brava 권역 Place Content Enrichment (Phase PC-07)**로 안전하게 확장이 가능합니다.
