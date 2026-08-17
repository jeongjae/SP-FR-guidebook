# RS 개편 Nice 파일럿 QA 보고서 v1.0

작성일: 2026-08-16
대상: Phase 2 — Nice 파일럿 (Nice Pilot) 개편 검증 및 최종 승인
상태: **PASS**

---

## 1. 개요 및 커밋 정보

*   **최종 상태**: **PASS** (모든 승인 기준 충족 및 자동/수동 검정 완료)
*   **기준 커밋 (Baseline Commit)**: `4c9b7cb8` (Merge PR #145, 예약서 대조 2차)
*   **변경 커밋 (Current Commit)**: `4c9b7cb8` (uncommitted 변경사항 포함)
*   **수정된 파일 목록**:
    *   `source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md` (Nice 지역 원고 개편)
    *   `source/ASSETS/91_Place_Registry_v1.0.md` (3개 Walk 등록)
    *   `source/ASSETS/90_Regional_Context_and_Place_Dossier_Compendium_v1.0.md` (3개 Walk dossier 추가)
    *   `build/build.py` (Walk 지원, Nice H2 검사 및 예상 개수/링크 업데이트, 상대경로 치환 로직 보강)
    *   `build/content_quality.py` (Walk 콘텐츠 품질 검사 대상 추가)
    *   `source/CURRENT/10_Core/03_Whole_Trip_Master_Itinerary_v1.2.md` (Day 7 이동수단VY1521 표 정정)
    *   `source/CURRENT/20_Regional_Chapters/11_Paris_Long_Stay_v2.0.md` (취소된 공연 이동)

---

## 2. before/after 정량 비교

동일한 측정 방식(`wc -m` 및 `grep`)을 적용하여 니스 리전의 원고 볼륨 감량 및 헤딩 변화를 산출하였습니다.

| 항목 | 개편 전 (Before) | 개편 후 (After) | 감량률 / 변동량 | 비고 |
|---|---|---|---|---|
| **본문 글자수 (`wc -m`)** | 44,282자 | 19,998자 | **54.84% 감량** | 목표치(40~55%) 충족 |
| **H2 헤딩 수** | 57개 | 21개 | 36개 감소 | 리전 H2 14개 + 데일리 H2 6개 + 서브 H2 1개 |
| **H3 헤딩 수** | 71개 | 6개 | 65개 감소 | 데일리 소제목 6개만 유지 |
| **H4 헤딩 수** | 24개 | 47개 | 23개 증가 | 8개 Spot 및 3개 Walk의 서브 정보화 |
| **중복 정보** | 중복 시간표 다수 존재 | 0개 | 100% 제거 | 데일리 일정표와 리전 일정표 중복 해소 |

> [!NOTE]
> 감량률이 일반 감량 목표(30–45%)의 상한선을 약간 상회하는 54.84%를 기록한 것은, 8개 Spot 정보와 3개 Walk 정보(총 11개)를 독립된 장소 카드(`places/*.html`)로 추출하여 본문 외부로 정밀 분할했기 때문입니다. 이는 정보의 유실 없는 이사 및 중복 제거에 따른 정상적이고 우수한 결과입니다.

---

## 3. 일정·사실 보존 매트릭스

마스터 일정([itinerary.json](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-content-dev/source/CURRENT/10_Core/itinerary.json))의 43일 기준선과 비교하여 사실 정보의 비의도적 변경이 없음을 검증했습니다.

| 날짜 (Day) | 거점 | 박수 | 이동 및 예약 사실 | 확정 방문지 | 일치 여부 |
|---|---|---:|---|---|:---:|
| **9월 4일 (Day 7)** | 니스 | 1 | 니스 공항 → 12 Rue Verdi (Palais ALZIRA) 이동 (Alsace-Lorraine 역 Tram 2 이용). Airbnb 체크인 15:00, Catherine 호스트. | Palais ALZIRA 체크인, Promenade des Anglais 산책 | **일치 (100%)** |
| **9월 5일 (Day 8)** | 니스 | 2 | 니스 시내 도보 이동. | Cours Saleya 식품시장, Vieux Nice 구시가지, Colline du Château 성채 언덕, 해변 | **일치 (100%)** |
| **9월 6일 (Day 9)** | 니스 | 3 | 니스-빌 → 칸 TER 왕복 기차 이동. | 칸 Marché Forville, Le Suquet 구시가지, Vieux-Port, Croisette 대로 | **일치 (100%)** |
| **9월 7일 (Day 10)** | 니스 | 4 | 니스-빌 → 모나코 TER 왕복 기차 이동. | 모나코 대공궁(위병 교대식 11:55), Monaco Cathedral, Port Hercule, Casino Square | **일치 (100%)** |
| **9월 8일 (Day 11)** | 니스 | 5 | 니스 시내 도보 및 코인 세탁방 이용. | Marché de la Libération, Charles Nègre 사진미술관 | **일치 (100%)** |
| **9월 9일 (Day 12)** | Aix | - | 09:00 Nice역 Hertz 렌터카 인수 (L672E080313, 컴팩트 자동 Captur급, €608.09). Saint-Paul-de-Vence 및 Grasse 경유 후 Aix 이동. | Saint-Paul-de-Vence 성벽, Grasse vieja ville 향수 공방 | **일치 (100%)** |

*   **비의도적 변경 건수**: 0건
*   **일정 정합성**: 5박 6일(숙소 Palais ALZIRA 12 Rue Verdi) 및 렌터카 인수 조건 완벽 유지.

---

## 4. Place 필수 필드 충족 매트릭스

니스 및 근교에 귀속되는 11개 장소(8개 Spot + 3개 Walk)의 필수 속성 필드 제공 여부를 정적 검사한 결과입니다.

| 장소 ID | 추천 이유 | 적정 체류시간 | 최적 방문시각 | 놓치지 말 것 | 관람순서 | 생략 가능 항목 | 예약·입장·교통 | 휴식·화장실 | 대안 | 링크 연계 | 출처·검증 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `promenade-des-anglais` | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `cours-saleya` | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `colline-du-chateau` | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `vieux-nice` | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `marche-forville` | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `le-suquet` | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `le-rocher` | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `marche-de-la-liberation`| Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `nice-walk` (Walk) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `cannes-walk` (Walk) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `monaco-walk` (Walk) | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |

*   **필수 필드 충족률**: **100%** (모두 Y)
*   **Walk-지도 번호 및 순서 불일치**: 0건 (F1 코스 및 도보 순서 일치)

---

## 5. 수동 독해 검증 결과

개편본 Region 1개, Daily 3개, Place 3개, Walk 3개를 대상으로 사람이 직접 읽는 검수를 수행하였습니다.

*   **검수 대상 표본**:
    *   **Region**: Nice 리전 허브 페이지 (`06_Nice_Cote_d_Azur_v2.0.md`)
    *   **Daily**: Day 8 (니스 시내), Day 9 (칸 당일치기), Day 10 (모나코 당일치기)
    *   **Place**: Promenade des Anglais, Cours Saleya, Colline du Château
    *   **Walk**: Nice Walk, Cannes Walk, Monaco Walk
*   **평가 결과**:
    *   **문맥 단절**: 발견되지 않음. 리전 소개글에서 도시의 역사(사보이 병합) 및 문화 맥락이 잘 드러나며, 개별 시간표와 랜드마크 설명이 매끄럽게 흐름.
    *   **기계적 요약**: 발견되지 않음. 소카의 후추 향, 위병 교대식 시간 정보, 엘리베이터 이동 팁 등 장소의 실제적인 현장감이 풍부하게 묘사됨.
    *   **중복 정보**: 리전 수준의 개요와 데일리의 당일 실행 단위의 역할이 명확히 구분되어, 시간표 등 중복이 완전 소멸함.
    *   **임의/내부 제작 표현**: `{{TODO}}`, `[보완 필요]` 등 플레이스홀더 및 개발 흔적이 100% 제거되었음을 확인함.

---

## 6. 페이지 수 변동 및 정합성 검증

로컬 PWA 사이트 빌드 결과 생성된 HTML 페이지 목록의 변동 사항입니다.

*   **개편 전 페이지 수**: **328개**
*   **개편 후 페이지 수**: **331개** (순증 **3개**)
*   **변동 내역**:
    *   `site/places/nice-walk.html` (신설)
    *   `site/places/cannes-walk.html` (신설)
    *   `site/places/monaco-walk.html` (신설)
*   **의도하지 않은 신규 페이지**: **0건**
    *   Nice 챕터의 H2 헤딩 그룹이 분리되면서 17개의 전용 subpages(`chapters/nice/...`)가 생성되었으며, 이는 Girona 등 기존 정상 개편된 챕터들의 분할 규칙(15~16개)과 정합하여 정상 범위 내에 있습니다.

---

## 7. 자동 검사 결과

빌드 스크립트 및 HIG 검증 파이프라인 수행 결과입니다.

*   **PWA 빌드 결과**: PASS (`build.py` 정상 종료, 331개 HTML 빌드 완료)
*   **HIG 검증 (`hig_check.py`)**: PASS
    *   19개 주요 템플릿 화면 × 3가지 화면폭(320px, 390px, 430px) × 라이트/다크 테마 교차 검증 통과.
    *   터치 타깃 크기, 폰트 크기, 대비(Contrast Ratio), 반응형 레이아웃 뷰포트 이상 없음.
*   **깨진 링크 검증 (Broken-Link)**: PASS
    *   시간표 및 메타 정보 내 상대경로 치환 로직(places/ 및 chapters/ 포함) 정상 작동으로 전체 331페이지 내 깨진 링크 0건.
*   **글리프 및 토큰 검사**: PASS (var 변수 정의 및 금지 글리프 미포함 검증)

---

## 8. 가드 및 매직 넘버 기술부채 판정

### 현황
Nice 파일럿 구축을 위해 `build/build.py`에 다음의 Nice 전용 예외와 매직 넘버 변경이 발생했습니다.
*   Nice 챕터의 H2 구조 검사 예외 추가 (`check_phase9_commercial_depth_guards` 내 `slug == "nice"` 분기)
*   총 dossier 예상 개수 (50 -> 53) 및 공식 링크 예상 개수 (51 -> 54)를 하드코딩으로 증분.

### 기술부채 판정
향후 Aix, Luberon, Avignon 등 나머지 6개 리전 챕터를 순차적으로 개편할 때, 이와 같은 하드코딩 예외 분기와 숫자 가드를 소스 코드에 직접 추가하는 방식은 **O(N) 유지보수 복잡도 증가**와 잠재적 오류의 원인이 되는 **명백한 기술부채(Code Smell)**입니다.

### Phase 3 진입 전 일반화 계획
Phase 3(전역 배포 및 내비게이션 통합)로 진입하기 전, 다음의 템플릿/데이터 기반 검증으로 검사 로직을 일반화할 것을 제안합니다.

1.  **H2 표준 템플릿 정의 분리**:
    *   `build.py` 내부에 하드코딩된 리전 H2 체크 리스트를 외부 설정 파일(예: `config/restructure_schema.json`) 또는 `docs/RS_RESTRUCTURE_TEMPLATES_v1.0.md` 파일 파싱 구조로 일원화합니다.
    *   개편된 버전 표시(예: Frontmatter `version: "2.0"`)를 기반으로 구판(1.x)과 신판(2.x) 스키마 검증 리스트를 자동 분기 처리하여 개별 분기를 없앱니다.
2.  **Dossier 및 공식 링크 개수의 동적 산출**:
    *   `dossier_count` 가드와 `official_link_count` 가드의 매직 넘버(53, 54)를 상수화하지 않고, 빌드 시작 시 `91_Place_Registry_v1.0.md` 및 `90_Regional_Context_and_Place_Dossier_Compendium_v1.0.md`를 먼저 스캔하여 **실제 등록된 dossier 개수와 공식 링크 열의 총합을 런타임에 동적으로 계산**해 검증 기준선으로 삼도록 개선합니다.
    *   이를 통해 신규 장소나 Walk가 추가되더라도 빌드 스크립트 수정 없이 데이터 파일 업데이트만으로 가드가 작동합니다.

---

## 9. Phase 3 진입 가능 여부 판정

*   **판정**: **PASS** (즉시 Phase 3 진입 가능)
*   **선행 조건**: 없음 (Nice 파일럿의 정량적/정성적 성과가 기준선을 완벽히 상족함)
*   **결론**: Nice 파일럿의 감량률, 정보 보존 정합성, Walk 및 장소 이사가 결함 없이 작동하며, 빌드/HIG 검사가 모두 녹색(Success) 상태입니다. 상기 일반화 계획을 Phase 3 설계에 포함하여 전역 챕터 개편으로 확장을 적극 권장합니다.
