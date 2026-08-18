# Place Canonicalization & SOT Architecture Design

**상태**: **IMPLEMENTED (Phase PC-06C Cutover 완료)**  
**작성일**: 2026-08-18  

---

## 1. 아키텍처 개요 (Cutover 완료 상태)

```text
[source/CURRENT/30_Places/<slug>.md]  (★ 유일한 장소 장문 정본 Canonical SOT)
                  │
        ┌─────────┴───────────────────────┐
        ▼                                 ▼
[build/model.py: load_place_bodies]  [Region / Day / Search / Map]
        │                                 │
        ▼                                 ▼
[site/places/<slug>.html]            [site/guide/*.html, daily/*.html]
(Full 5-Layer Guide)                 (Compact Cards & Direct Links)
```

---

## 2. 핵심 원칙 및 구현 상태

### 2.1 1 Place = 1 Canonical Long-Form File
- `source/CURRENT/30_Places/<slug>.md`가 장소 장문의 유일한 정본(Single Source of Truth)으로 승격되었습니다.
- `build/site.py` 실행 시 더 이상 `promote_places.py`를 자동 호출하여 `30_Places`를 덮어쓰지 않으며, `30_Places`의 파일들을 직접 읽어 모델에 로드합니다.

### 2.2 promote_places.py의 최종 상태
- **상태**: **LEGACY / ONE-TIME MIGRATION TOOL ONLY**
- 빌드 파이프라인의 자동 의존성에서 완전히 격하 및 제외되었습니다.
- 일반적인 `python3 build/site.py` 실행 시 장소 파일을 덮어쓰지 않으므로 `30_Places/<slug>.md`를 수동 편집하더라도 온전히 보존됩니다.

### 2.3 Region & Day는 Reference Consumer
- **Region 챕터 원고 (`20_Regional_Chapters/*.md`)**:
  - 장소의 장문을 중복 유지하지 않고, Name, Priority, Compact Summary/Verdict, 체류시간, `[상세 가이드 보기](../places/<slug>.html)` 명시적 참조만 유지합니다.
- **Day 일정 (`data/daily-cards/*.json`)**:
  - Stops 시각, 이동 Leg, 예약 상태, 당일 핵심 하이라이트만 보유하며, `place_ref` 링크를 통해 전체 장소 페이지로 연결합니다.

### 2.4 Trip Layer의 완전한 격리 (Decoupling)
- 장소 본문에는 특정 여행 일자(`8월 30일`, `Day 2` 등)를 기재하지 않고 일반적인 방문 조건 및 시간대 전략만 기술하여, 일정 변경 시에도 장소 정본 수정이 필요 없습니다.

---

## 3. 후속 권역 Rollout 가이드라인

1. **대상 권역 순서**:
   - `Girona & Costa Brava` → `Nice & Côte d'Azur` → `Aix-en-Provence` → `Luberon` → `Avignon` → `Lyon` → `Paris`
2. **권역별 전환 절차**:
   - 1) `30_Places/<slug>.md`를 5-Layer 표준(Facts, Strategy, Experience, Deep Guide, Practical)으로 고도화
   - 2) 해당 Region 챕터 원고의 장소 장문을 Compact Reference로 축약하여 중복 제거
   - 3) `scripts/validate_place_canonical_model.py` 및 `build/content_audit.py` 검증 수행
