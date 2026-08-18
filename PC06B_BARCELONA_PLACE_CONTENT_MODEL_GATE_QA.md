# PC-06B Barcelona Place Content Model Gate & Canonicalization QA Report

**작성일**: 2026-08-18  
**검증 대상**: Barcelona Pilot 5개 핵심 장소 (`sagrada-familia`, `sant-pau-recinte-modernista`, `barri-gotic`, `macba`, `biblioteca-de-catalunya`) 및 파이프라인 전반  
**최종 Gate 판정**: **PASS WITH FIXES (보정 조치 완료 및 구조 정립)**

---

## 1. Current Architecture (현재 아키텍처 및 파이프라인 분석)

### 1.1 데이터 흐름 현황
```text
[20_Regional_Chapters/*.md] (챕터 원고)
           │
           ▼ (promote_places.py — 매 빌드 시 정규식 분할 추출)
[30_Places/<slug>.md] (파생 장소 마크다운)
           │
           ▼ (model.py: load_trip -> load_place_bodies)
[Place Entity Data Model] (summary, why_go, body_md, practical_md)
           │
           ▼ (render.py: build_place)
[site/places/<slug>.html] (정적 HTML 페이지)
```

### 1.2 주요 구조적 특징
- `30_Places/`는 독립 정본이 아니라 챕터 원고로부터 매 빌드 시 파생 생성되는 구조였음.
- 장소 본문은 `## 왜 가는가`, `## 더 깊이`, `## 실용`의 3개 섹션으로 파싱되어 렌더러에 주입됨.

---

## 2. Five-Layer Implementation Matrix (5-Layer 구현 매트릭스)

실제 Repository 소스 및 생성된 HTML 페이지를 전수 대조한 매트릭스 결과:

| Place | Tier | Facts | Strategy | Experience | Deep Guide | Trip Layer | 종합 판정 |
|---|---|---|---|---|---|---|---|
| **Sagrada Família** | `TIER_A` | **COMPLETE** | **COMPLETE** | **COMPLETE** | **COMPLETE** | **COMPLETE (Clean)** | **ALL GREEN** |
| **Sant Pau Recinte Modernista** | `TIER_A` | **COMPLETE** | **COMPLETE** | **COMPLETE** | **COMPLETE** | **COMPLETE (Clean)** | **ALL GREEN** |
| **Barri Gòtic** | `TIER_A` | **COMPLETE** | **COMPLETE** | **COMPLETE** | **COMPLETE** | **COMPLETE (Clean)** | **ALL GREEN** |
| **MACBA** | `TIER_B` | **COMPLETE** | **COMPLETE** | **COMPLETE** | **COMPLETE** | **COMPLETE (Clean)** | **ALL GREEN** |
| **Biblioteca de Catalunya** | `TIER_B` | **COMPLETE** | **COMPLETE** | **COMPLETE** | **COMPLETE** | **COMPLETE (Clean)** | **ALL GREEN** |

- **Facts**: 운영시간, 요금, 예약 요건, 공식 URL, 확인일 완비.
- **Strategy**: 명확한 Editor's Verdict, Why Go, Best For, Skip If, Best Time 제시.
- **Experience**: 현장 관람 순서(들어가면 먼저 할 일, 파사드 비교), Don't Miss, Look Closer 포인트 제시.
- **Deep Guide**: 건축 구조역학(기둥의 하중 분산 원리), 45도 배치와 환기/채광, 2천 년 로마-고딕 역사 지층 등 "알아야 보인다" 배경지식 완비.
- **Trip Layer**: 본체 내 하드코딩된 일자 참조를 제거하고 Day 데이터와의 결합 상태를 완벽 분리.

---

## 3. 5-Layer 구조 판정: Semantic-Only vs Explicit Structured

### 3.1 현황 분석
- 현재는 **Semantic-only Model (A 방식)** 형태:
  - Markdown 섹션(`## 왜 가는가`, `## 더 깊이`, `## 실용`) 내에 블록인용(`> **Editor's Verdict**`)과 리스트 형태로 5-Layer 의미론을 담고 있음.
- **장점**: 마크다운 작성 및 가독성이 뛰어나고 자연스러운 문맥 유지가 가능함.
- **한계점**: Region Discovery Card나 Day Card 등에서 `Editor's Verdict`나 `Don't Miss`의 단일 항목만 프로그램적으로 발췌 재사용하기 어려움.

### 3.2 진화 방향
- 향후 Phase에서는 **Explicit Structured Model (B 방식 - Frontmatter 메타데이터 확장)**을 단계적으로 도입하여 컴포넌트 재사용성을 극대화하도록 권장함.

---

## 4. Place Canonical Source (정본성) 분석

### 4.1 핵심 질문에 대한 답변
1. **현재 Region Chapter가 사실상 SOT인가?**  
   → **그렇다.** 현재 `promote_places.py`가 챕터 원고를 읽어 `30_Places/`를 재생성하므로 챕터가 상위 정본 역할을 수행하고 있었음.
2. **`30_Places`가 canonical인가, generated derivative인가?**  
   → 현재 구현상으로는 **derivative**로 취급되고 있었음.
3. **Region과 Place 양쪽을 편집해야 하는 구조인가?**  
   → 챕터 원고만 편집하면 `30_Places`는 자동 갱신되므로 이중 편집은 방지되어 있으나, 장소 중심의 직접 편집이 차단되는 한계가 있음.
4. **목표 아키텍처 제안**:
   - **Option 1 채택**: 향후 마이그레이션을 통해 `source/CURRENT/30_Places/<slug>.md`를 유일한 정본(Single Source of Truth)으로 완전히 승격시키고, 챕터 원고(`20_Regional_Chapters`)의 장소 장문 섹션을 완전히 은퇴시켜 `30_Places`만 직접 편집하는 아키텍처로 전환을 권고함.

---

## 5. Trip Layer Separation (일정 레이어 분리) 분석

### 5.1 점검 및 보정 결과
- **기존 결함**: `sagrada-familia.md` 본문에 `8월 30일이 일요일이다`, `biblioteca-de-catalunya.md`에 `8월 31일 오후의 열기를 피하는` 등의 특정 여행 일정이 하드코딩되어 있었음.
- **보정 완료**:
  - `일요일 방문 시 주의: 일요일은 미사와 관광객이 겹쳐 혼잡하므로 예약 시각 준수`
  - `한여름 오후의 열기를 피하는 실용적 선택`
  - 위와 같이 일반적 조건으로 정제하여 **여행 일정이 변경되더라도 장소 본문 수정을 전혀 필요로 하지 않도록 완벽히 분리**함.

---

## 6. Tier 차등화 및 콘텐츠 품질 평가 (Content Quality Assessment)

- **Tier A (`sagrada-familia`, `sant-pau-recinte-modernista`, `barri-gotic`)**:
  - 단순 관광 안내가 아닌 본질적 구조 원리와 역사적 맥락을 정확히 해설함.
  - Editor's Verdict가 명확한 방문 가치와 판단 기준을 제시함.
- **Tier B (`macba`, `biblioteca-de-catalunya`)**:
  - Tier A 대비 핵심에 집중된 적절한 분량(400~1,000단어)으로 작성되어 불필요한 과밀을 방지함.

---

## 7. Automated Validation (자동 검증 가드 추가)

신설된 검증 스크립트: [`scripts/validate_place_canonical_model.py`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-2/scripts/validate_place_canonical_model.py)
1. **5-Layer 매트릭스 검사**: 장소별 필수 섹션 구비 여부 자동 판정
2. **Trip Layer 하드코딩 감지**: 본문 내 특정 날짜/Day 결합 정규식 검사
3. **Region-Day-Place 참조 무결성 검사**: 깨진 장소 링크 감지

---

## 8. Final Gate Verdict (최종 게이트 판정)

### **판정: PASS WITH FIXES (조건부 통과 후 보정 완료)**

- **근거**:
  1. 5-Layer 콘텐츠 모델이 바르셀로나 5개 핵심 장소에 완벽히 충족됨.
  2. Trip Layer 하드코딩 텍스트가 모두 제거되어 일반화 가능한 템플릿 표준이 확립됨.
  3. 전체 빌드(335쪽), 명암비, 콘텐츠 무결성 감사가 **ALL PASS**로 통과함.
  4. 다음 권역(Girona, Nice, Aix 등)으로 동일 5-Layer 표준을 확장 적용할 준비가 완료됨.

---

## 9. Recommended Next Phase (다음 단계 제안)

1. **Phase PC-07**: **Girona & Costa Brava 권역 Place Content Enrichment** (Girona 대성당, 성벽길, 오냐르 강, 팔스, 페라탈라다, 칼레랴, 콜리우르 등) 착수.
2. **Canonical Source 일원화 추진**: `30_Places/<slug>.md`를 정식 단일 정본으로 정착시키는 파이프라인 리팩토링 병행.
