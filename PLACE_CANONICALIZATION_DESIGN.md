# Place Canonicalization & SOT Architecture Design

## 1. 배경 및 문제 정의

현재 SP-FR-guidebook의 장소 콘텐츠는 다음 구조로 동작하고 있습니다:
- `source/CURRENT/20_Regional_Chapters/*.md` 챕터 원고에서 `promote_places.py`가 정규식으로 장소 섹션을 잘라내어 `source/CURRENT/30_Places/<slug>.md`를 매 빌드마다 덮어쓰고 있습니다.
- 이로 인해 `30_Places/`는 사실상 '파생물'로 취급되어 장소 중심의 독립적인 편집과 고도화가 제약받는 구조적 한계가 존재합니다.

---

## 2. 목표 아키텍처 (Option 1: Place Markdown as Canonical SOT)

```text
[source/CURRENT/30_Places/<slug>.md]  (★ 유일한 장소 장문 정본)
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
[build/model.py]     [Region / Day / Search / Map]
        │                   │
        ▼                   ▼
[site/places/*.html]  [site/guide/*.html, daily/*.html]
```

### 핵심 원칙
1. **1 Place = 1 Canonical File**:
   - 모든 장소의 전체 장문, Facts, Strategy, Experience, Deep Guide는 `source/CURRENT/30_Places/<slug>.md`에만 존재합니다.
2. **Region & Day는 참조(Reference)만 보유**:
   - 지역 페이지는 요약 카드(Discovery Card)와 링크만 표시하며, 중복 장문을 포함하지 않습니다.
   - Day 페이지는 일정표(Stop, Leg, 시간, 예약)와 핵심 Don't Miss 포인트만 담고 장소 페이지로 연결합니다.
3. **Trip Layer의 완전한 격리**:
   - 장소 본문에는 특정 여행 일자(예: 8월 30일)나 Day 번호를 기재하지 않고, 일반적인 방문 가이드와 시간대 전략만 기술합니다.

---

## 3. 단계별 마이그레이션 로드맵

1. **Phase 1 (완료)**: 바르셀로나 5개 장소 5-Layer 표준화 및 Trip Layer 하드코딩 분리.
2. **Phase 2 (차기 권역 확장)**: Girona, Nice, Aix, Luberon, Avignon, Lyon, Paris 권역의 장소들을 5-Layer 표준으로 점진 승격.
3. **Phase 3 (SOT 전환)**: `promote_places.py`를 일회성 도구로 종료하고 `build/site.py`가 `30_Places/*.md`를 직접 상위 정본으로 읽도록 파이프라인 단일화.
