# 상용 가이드북 개편 — 베이스라인 v1.0

> **추기 v1.0.1 (2026-08-06, 기준 커밋 `c274d42`):** 작성 다음 날 PR #51~#62 가
> 머지되어 아래 수치가 이동했다. 변한 것: ① 지역 실행지도 8/8 이 **Google Maps 로
> 전환** (Leaflet 지역지도 시대 종료, 지도 정본은 `source/ASSETS/maps/*.json` 72곳,
> §5·§9 의 "3계보" 진단은 Google Maps 계보로 수렴 중) ② 사진 Girona·Nice 27장
> 추가(총 40장, 3/8지역) ③ 액션맵 카드 Day 1~15 완료 ④ Barcelona 숙소 확정
> (Occidental Barcelona 1929) ⑤ 사이트 328페이지. 재검증 완료: 빌드·HIG·PWA 모두
> 통과 (2026-08-06). 나머지 절(§2 여정, §6 예약, §7 정합성 결함, §8 처분표)은 유효.

- **기준 커밋:** `7d6838f` (origin/main = PR #50 머지 시점, 2026-08-05)
- **작성일:** 2026-08-05
- **작성 방법:** 저장소 전면 재감사(빌드 시스템 · 원고 · 생성 사이트 · 문서 최신성) + 빌드/HIG/PWA 실검증.
  기존 Phase 0~10 보고서는 **이 문서의 근거로 쓰지 않았다** — 전부 코드·데이터에서 다시 확인했다.
- **이 문서가 대체하는 것:** `docs/PHASE0_BASELINE_REPORT_v1.0.md` 및 Phase 1~10 보고서의 "현황" 서술.
  각 Phase 보고서는 작업 이력 기록으로만 남는다(§8 처분표 참조).

---

## 1. 검증 결과 (2026-08-05 실행)

| 검사 | 결과 |
|---|---|
| `python3 build/build.py` | **통과** — 327개 HTML 생성, 전 가드 이상 없음 |
| `python3 build/hig_check.py` | **통과** — 19쪽 표본 × 320/390px × 라이트/다크, 6항목(터치타깃·글자크기·명암비 7:1/4.5:1·안전영역·리플로·뷰포트) |
| `python3 build/pwa_check.py` | **통과** — 457파일 14.3 MiB 전체 저장 · 오프라인 심층 탐색 |
| CI (`.github/workflows/pages.yml`) | main 푸시 시 attribution 검사 → 빌드 → itinerary/media 검증 → PWA → HIG → gh-pages 배포 |

빌드 가드 실측: **상위 게이트 17종 + 생성 중 인라인 가드 약 12종** (build.py `main()` 4977~4996행 기준).
CLAUDE.md의 "빌드 가드 7종" 서술은 구판이다.

---

## 2. 여정 정본 (source/CURRENT/10_Core/itinerary.json)

2026-08-29 ~ 2026-10-10 · 43일 42박 · 거점 8곳. 검증: itinerary.json = 트래커 Accommodation 시트 = 마스터 일정표 v1.2 모두 일치.

| 거점 | 체크인 | 체크아웃 | 박 |
|---|---|---|---:|
| Barcelona | 08-29 | 09-01 | 3 |
| Bàscara (키: girona) | 09-01 | 09-04 | 3 |
| Nice | 09-04 | 09-09 | 5 |
| Aix-en-Provence | 09-09 | 09-13 | 4 |
| Luberon | 09-13 | 09-16 | 3 |
| Avignon | 09-16 | 09-20 | 4 |
| Lyon | 09-20 | 09-24 | 4 |
| Paris | 09-24 | 10-10 | **16** |

- 마르세유(Day 14, Aix발) · 아를(Day 22, Avignon발)은 **당일치기**다. 거점은 8곳 그대로.
- 파리는 **16박**이다. "15박"은 변경해야 할 기존 예약을 가리키는 값(트래커 R008)일 뿐이다.
  커밋 메시지 `b4fdf65`("15-night")와 일부 구판 문서에 15박 표기가 남아 있다.
- 파리 고정 P0 3건: Day 34 (10/1) Il Barbiere di Siviglia 19:30 · Day 37 (10/4) Prix de l'Arc de Triomphe · Day 42 (10/9) Hamlet 19:30.

---

## 3. 생성 사이트 구조 (data/site-page-inventory.csv + build.py)

327개 HTML = 실페이지 약 264 + 리다이렉트 62 (+오프라인 폴백).

| 축 | 페이지 | 비고 |
|---|---|---|
| 홈 | 1 | 5개 주행동 + 보조 6행 |
| 데일리 | 43 + 인덱스 | 유일 정본. 챕터 쪽 day-NN 50건은 전부 리다이렉트(가드 강제) |
| 지역 챕터 | 허브 8 + 주제 페이지 각 7~9 | 슬러그: barcelona·girona·nice·aix·luberon·avignon·lyon·paris |
| 장소 | 94 spot + 인덱스 + 리다이렉트 1 | 정본: `source/ASSETS/91_Place_Registry_v1.0.md` (97행: spot 94 · node 3) |
| 주제 | 14 (허브+분류 10+상태 3) | |
| 지도 | 8 지역 실행지도 + 인덱스 + offline | Leaflet 로컬 번들, KML 81 기준점 |
| 트래커 | 인덱스 + 6시트 | `TP_Europe_Travel_Master_Tracker_v1.2.xlsx` 미러(읽기 전용) |

**내비게이션(코드 실측, CLAUDE.md L0/L1/L2 모델과 일치):**
- L0 하단탭 5개 고정: 오늘·일정·지역·준비·검색 (가드가 정확한 튜플을 강제)
- 상단바 = 위치 경로 + 검색 버튼(시트). 햄버거 없음.
- L1 좌표 바: 홈 + 세 축 뿌리 + 데일리 43쪽. 챕터·장소 페이지엔 없음(L2 서브내비가 대체 — 의도된 설계, navigation-consolidation-plan.md §4).
- 탭 정의가 build.py·nav.js·가드 **3곳에 중복** — 구조 부채.

**검색:** `data.js` 인덱스 1,880항목. 클라이언트는 제목+분류 부분일치만(본문 미포함, 형태소 없음, 30건 캡).

**PWA:** 코어 20경로 프리캐시 + 전체 저장(457파일) + 런타임 캐시 3단. 네트워크 우선 3초 타임아웃. 실기기(iPhone) 검증은 `docs/iphone-local-pwa-implementation-plan.md`에 2026-08-05 배포 검증 통과로 기록.

**이미지:** 사진은 전부 로컬 라이선스 파일이다. CLAUDE.md의 "위키백과에서 온라인일 때만 사진을 불러온다"는 서술은 **현재 코드와 다르다** — 위키백과는 참고 링크로만 쓰인다(레지스트리 `위키` 열 97행 중 87 채움).

---

## 4. 완료·보존 자산 (개편에서 건드리지 않는다)

1. 빌드 파이프라인 + 가드 17종 + CI 배포 (전부 통과 상태)
2. 여정 정본 3종 일치 상태 (itinerary.json · 마스터 일정표 · 트래커)
3. 데일리 43쪽 단일 정본 구조 + 리다이렉트 62건
4. 장소 레지스트리 97행 · 장소 dossier 51건 (`source/ASSETS/90_…Compendium_v1.0.md`)
5. 지역 실행지도 8종 (GeoJSON·KML 81 기준점, 2026-08-05 일정 반영 재생성됨)
6. PWA 오프라인 전체 저장 (검사 자동화 포함)
7. 공식정보 검증 레지스터 F001~F023 (`source/OPERATIONS/116`)
8. 라이선스 이미지 파이프라인 (media-catalog + 검증 + attribution 자동 생성)
9. 개인숙소 보호 (private→approximate+GoogleMaps URL 공란, 빌드 강제)
10. 명명규칙 "번호가 아니라 지명" (`handoff/01_plan/10_명명규칙_v1.0.md` — 계속 유효)
11. **벤치마킹 보고서** `handoff/05_evidence/06_벤치마킹_보고서_v1.0.md` — **원문 그대로 보존.**
    미채택 핵심 제안(등급 언어에 '우회 비용' 인코딩 — Michelin 방식)은 개편 검토 대상으로 살아 있다.

---

## 5. 미완 작업 (부분개선 진행 중 — 개편 착수 전 범위 확정 필요)

| 항목 | 현재 | 목표 대비 |
|---|---|---|
| 날짜별 인터랙티브 지도 (Leaflet) | **5 / 43일** (Day 1·2·3·5·6, daily-maps.json) | 가드는 3일만 강제 |
| v2 액션맵 (PR #50, 좌표 기반 정적 카드) | **3 / 43일** 렌더 완료 (Day 2·4·5) · 43일 JSON 스캐폴드는 전부 존재 (`data/daily-cards/`) | 구판 카드와 병행 중 |
| 데일리 카드 이미지 | 43장 중 **23장 구판이라 숨김 처리** (`SUPERSEDED_DAILY_CARDS`: 4·5·6·14·19~28) | 파일명이 Day 19부터 하루 밀림 |
| 라이선스 이미지 | **3 / 8지역** (barcelona·girona·nice 24장). 나머지 5지역은 구 HERO_PHOTOS 경로와 이원화 | image-requirements 125행 중 101 미선정(P0 72) |
| content_model.json | 생성·검증만 됨. **아직 정본 아님**(자체 주석: 마이그레이션 중) | |
| 검색 | 제목·분류만. 작업지시서의 자연어 키워드(우천·요일 등) 미지원 | |

## 6. 예약·운영 실상 (여행 87일 전 시점)

- **실예약 잠금률 0%** (`source/OPERATIONS/90_…Scorecard`: 원고 완성도 99.7% vs 잠금 0%).
- 예약 28건 중 **예약완료 1건**(R002 Bàscara 숙소)뿐. 예약대기 4(파리 P0 공연·경마) · 재확인 ~10 · 나머지 미조사. 항공 2건 포함 교통 대부분 미조사, T003 Bàscara→Nice는 수단 자체가 미정.
- 숙소: 확정 1 / "기존 예약 변경 필요" 4 (Luberon·Avignon·Lyon·Paris) / 미조사 3 (Barcelona·Nice·Aix).
- 재검증 대기 `badge:pending` 토큰 273건. 파리 챕터 상당 부분이 "숙소 확정 후" 게이트에 걸려 있음.
- Organic Maps KML 임포트는 **실기기 미검증** (maps/offline.html에 명시).

## 7. 정합성 결함 (구판 일정 잔재 — 개편 전 정리 대상)

2026-08-04~05의 여정 재편(마르세유·아를 추가, Luberon 4→3박, 파리 재편 Day 27~43)이 반영되지 않은 파일들:

| 파일 | 문제 |
|---|---|
| `source/OPERATIONS/100_…Execution_Audit_v1.0.md` | Day 29~43이 폐기된 루브르 중심 파리 일정 |
| `source/OPERATIONS/117_…Reverification_Calendar_v1.0.md` | 게이트 날짜 다수가 하루 어긋남 + 구일정 게이트(베르사유·지베르니 등) + 제외된 Peralada 포함 |
| `source/OPERATIONS/41_…Register_v1.0.md` | P0 티켓이 구판(루브르·오르세·그랑팔레) |
| `source/OPERATIONS/90_…Scorecard_v1.9.md` | 공식검증 "18건"(실제 23건) |
| `source/OPERATIONS/119_…SHA256.txt` | 157개 중 26개가 존재하지 않는 경로 — 무결성 매니페스트 기능 상실 |
| `source/ASSETS/75_Execution_Map_Index_v1.1.md` | 전환일·Day 범위가 구 번호 체계 |
| `source/ASSETS/80_…Image_Index_v1.1.md` + PNG 파일명 | Day 19부터 하루 밀림 |
| `source/ASSETS/85_Editorial_Visuals_Index_v1.0.md` | "Paris 15박" 표기 |
| `source/ASSETS/89_Commercial_City_Experience_Cards_v1.0.md` | Girona 거점 표기·Peralada·Luberon 4박·아를 부재 |
| `README.md` (저장소 루트) | 존재하지 않는 경로·트래커 v1.1 기술 |
| `CLAUDE.md` | 가드 "7종"(실제 17+12) · "위키백과 사진 점진적 향상"(현재 로컬 라이선스 이미지) |
| `03_Whole_Trip_Master_Itinerary_v1.2.md` | 파일명 v1.2 vs 프런트매터 version 1.3 |

원고 내 잔존 중복(content-duplicate-matrix.csv, 8그룹 40행 — recommendedAction 전부 공란): Phase 10 원칙문·실행지도 안내문·현장 메모·Editor's Verdict가 8개 챕터에 동일 반복, Bàscara 숙소 블록 3중 중복, 루브르 본문이 dossier와 파리 챕터에 공존.

## 8. 문서 처분표

**보존 (그대로):** `handoff/05_evidence/06_벤치마킹_보고서_v1.0.md` · `handoff/01_plan/10_명명규칙_v1.0.md` · `docs/image-policy.md` · `docs/image-sourcing-guide.md` · `docs/image-attributions.md`(자동생성) · `docs/content-refactor-changelog.md` · `docs/iphone-local-pwa-implementation-plan.md`

**사실만 승계 후 이력화:** PHASE0(회귀 불변조건) · PHASE2(ID 체계) · PHASE3(5탭 확정) · PHASE8(예약 미입력 원칙 + R024→R028 정정) · navigation-consolidation-plan.md §4 관찰 · content-architecture-audit.md의 "빌드는 명시 경로만 읽는다" 원칙

**구판 (여행 판단에 사용 금지):** PHASE1·4·5·6·7·9·10 보고서 · PHASE0_URL_REDIRECT_MAP_v0.1.csv(미구현 설계안, 현 빌드와 모순) · content-deduplication-audit.md · UIUX_Design_v1.0.md(햄버거 시대) · handoff/ 전체(보존 2건 제외)

## 9. 구조 부채 (개편 설계 시 다뤄야 할 것)

1. **Phase 가드의 리터럴 잠금** — dossier 51 · 예약 28 · 기준점 81 · 검증 23 등 완료 수치가 build.py 상수로 고정. 콘텐츠가 늘 때마다 코드 수정 필요. 회귀 방지 목적은 유지하되 수치를 데이터에서 유도하는 방식 검토.
2. **build.py 단일 파일 5,000행** — 템플릿·가드·데이터 로딩이 한 파일.
3. **탭 정의 3중화** (build.py · nav.js · 가드).
4. **이미지 시스템 이원화** (media-catalog 3지역 vs HERO_PHOTOS 5지역).
5. **데일리 지도 3계보 병존** — 구판 PNG 카드 · Leaflet 인터랙티브(5일) · v2 액션맵(3일).
6. **hig_check 안전영역 검사가 소스 CSS를 읽음**(빌드 산출물 아님) + 사어 코드 `SAFE_AREA_JS`.
7. **content_model.json 이중 정본 위험** — 마이그레이션 완료 전까지 레거시가 정본임을 유지.
