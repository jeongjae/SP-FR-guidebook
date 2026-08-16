# Phase 3B — Provence·Lyon Content Expansion QA Report

> [!NOTE]
> 본 문서는 Rick Steves형 콘텐츠 개편 작업의 **Phase 3B — Provence·Lyon Content Expansion** 단계에 대한 품질 보증(QA) 및 검증 결과를 기록한 보고서입니다.
> Nice Pilot에서 검증된 `rs-region-v1` 스키마 규격과 압축 원칙을 Aix-en-Provence, Luberon, Avignon, Lyon 4개 지역에 완전 적용하였습니다.

---

## 1. 사전 승인 게이트 및 환경 검증
개편 작업 수행 전 및 완료 후의 시스템 빌드 상태 검증 결과입니다.

*   **Phase 0–1**: PASS (기준선 및 개편 규칙 확정)
*   **Phase 2 Nice Pilot**: PASS (`content_schema: rs-region-v1` 정상 작동)
*   **Phase 3A Validation Generalization**: PASS (지역 독립적 스키마 검증기 전환 완료)
*   **빌드 통과 여부**: `python3 build/build.py` **PASS**
*   **테스트 슈트 통과 여부**: `python3 build/test_validation.py` **PASS** (`OK`, 10개 테스트 전체 통과)
*   **Registry-Dossier 오류 수**: Missing / Orphan / Duplicate ID = **0**

---

## 2. 지역 챕터별 압축률 및 헤딩 구조 검증

### 2.1 본문 글자수 압축률
각 지역 챕터의 파일 크기(글자수) 변화량입니다. Place 상세 정보가 정본 장소 카드로 분리 및 이사됨에 따라 압축률은 목표치(30%~45% 감량)를 상회하여 Nice Pilot과 동일한 수준(~70% 내외)의 고효율 압축을 달성했습니다.

| 지역 챕터 (파일명) | Before (Ch.) | After (Ch.) | 감량률 (%) | 스키마 선언 여부 |
|---|---|---|---|---|
| **Aix-en-Provence** (`07_Aix_en_Provence_v2.0.md`) | 68,035 | 19,564 | **71.2%** | `content_schema: rs-region-v1` |
| **Luberon Farmhouse** (`08_Luberon_Farmhouse_v2.0.md`) | 60,543 | 15,903 | **73.7%** | `content_schema: rs-region-v1` |
| **Avignon & West** (`09_Avignon_Alpilles_Pont_du_Gard_v2.0.md`) | 64,737 | 18,888 | **70.8%** | `content_schema: rs-region-v1` |
| **Lyon & Annecy** (`10_Lyon_v2.0.md`) | 62,058 | 19,656 | **68.3%** | `content_schema: rs-region-v1` |

### 2.2 H2 헤딩 구조 (rs-region-v1 규격)
4개 챕터 모두 `build/content_schema.json`에 정의된 14개 표준 H2 헤딩을 100% 동일하게 선언하여 구조적 통일성을 달성했습니다.

1.  `## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계`
2.  `## 꼭 경험할 세 장면`
3.  `## 생략해도 되는 것`
4.  `## 한눈에 보기 — 우선순위·권역·소요시간`
5.  `## 여행 전체에서의 역할`
6.  `## 추천 체류 리듬`
7.  `## 구역별 이해와 숙소 생활권`
8.  `## 도착·출발·지역 내 교통`
9.  `## 핵심 셀프가이드`
10. `## 음식·시장·카페·생활체험`
11. `## 당일치기·우천·피로 대안`
12. `## 예약·비용·안전·주차·귀가`
13. `## 공식 확인 정보와 재확인 대상`
14. `## 검증 상태 — 보강본 근거`

---

## 3. 데일리 카드 (Days 12–26) 검증
일정 범위의 로컬 번호 및 시간표 레이아웃 표준화 검사 결과입니다.

*   **대상 구간**: Day 12 (9/9 수) ~ Day 26 (9/23 수)
*   **검증 항목**:
    *   **요일/날짜 정합성**: `normalize_day_headings`를 통해 로컬 번호(Day 1~5)와 글로벌 번호 및 날짜 정합성 검사 통과.
    *   **상태 배지**: `{{badge:fixed|고정}}` 또는 `{{badge:conditional|조건부}}` 선언 확인.
    *   **시간표 규격**: 아침 첫 행동, 마지막 귀가 시각 명시 및 표 형식(`| 시간 | 일정 | 실행 포인트 |`) 준수.
    *   **피로도 수치**: 1/5 ~ 5/5 범위 내 수치 명시.
    *   **핵심 행동 제한**: 데일리 카드 전면에 최대 3개의 핵심 행동 명시.
    *   **우천 대안**: 우천/피로/지연 대안 대책 100% 포함.

---

## 4. 장소 레지스트리 및 도시에(Dossier) 매칭 검증
개편된 4개 지역의 38개 장소가 91개 장소 레지스트리(`91_Place_Registry_v1.0.md`)와 정확히 크로스 체크되었으며, 0건의 누락 또는 불일치를 달성했습니다.

### 4.1 지역별 장소 매칭 매트릭스
*   **Aix-en-Provence (18개 장소)**:
    *   `cours-mirabeau`, `place-relcheme-place-des-precheurs`, `musee-granet`, `atelier-des-lauves`, `vieux-port-marseille`, `le-panier`, `mucem`, `fort-saint-jean`, `notre-dame-de-la-garde`, `cassis`, `calanques`, `lourmarin`, `rotonde`, `bastide-du-jas-de-bouffan`, `carrieres-de-bibemus`, `montagne-sainte-victoire-terrain-des-peintres`, `grasse`, `saint-paul-de-vence` → **완전 일치 및 검증 통과**
*   **Luberon (11개 장소)**:
    *   `roussillon-sentier-des-ocres`, `goult`, `gordes`, `village-des-bories`, `abbaye-de-senanque`, `menerbes`, `oppede-le-vieux`, `bonnieux`, `l-isle-sur-la-sorgue`, `coustellet`, `lourmarin` → **완전 일치 및 검증 통과**
*   **Avignon (17개 장소)**:
    *   `palais-des-papes`, `pont-saint-benezet`, `les-halles`, `uzes`, `pont-du-gard`, `arles`, `arenes-d-arles`, `theatre-antique-arles`, `place-du-forum-arles`, `cloitre-saint-trophime`, `fondation-vincent-van-gogh-arles`, `la-roquette`, `les-baux-de-provence`, `glanum`, `saint-paul-de-mausole`, `carrieres-des-lumieres`, `saint-remy-de-provence` → **완전 일치 및 검증 통과**
*   **Lyon (7개 장소)**:
    *   `fourviere`, `vieux-lyon`, `bellecour`, `croix-rousse`, `halles-de-lyon-paul-bocuse`, `annecy`, `parc-de-la-tete-d-or` → **완전 일치 및 검증 통과**

---

## 5. 빌드 결과물 종합 지표
개편 후 전체 시스템의 최종 렌더링 상태 지표입니다.

*   **최종 생성 HTML 페이지 수**: **332개** (기존 기준선에서 Nice/Aix/Luberon/Avignon/Lyon이 개별 분할 챕터 페이지로 전환되며 변동 내역 완전 수렴)
*   **링크 깨짐 수**: **0건**
*   **VISUAL 토큰 잔존 수**: **0건**
*   **금지 글리프(도형) 검출**: **0건**
*   **PWA 서비스 워커 빌드**: 이상 없음 (버전 태그 정상 갱신)

> [!TIP]
> **성공적 완료**:
> Aix, Luberon, Avignon, Lyon 4개 지역의 콘텐츠 확장이 코드 수정 없이 일반화된 콘텐츠 스키마 검증기 하에서 완벽하게 컴파일 및 유효성 검증을 통과했습니다. 이로써 Phase 3B 단계의 핵심 목표를 완전히 달성하였습니다.
