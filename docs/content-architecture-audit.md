# 콘텐츠 아키텍처 감사 v1.0

**기준일** 2026-08-03 · **대상** 저장소 전체 (site/ 산출물 제외한 원천 기준)
**목적** 중복 통합·콘텐츠 정리 작업의 사실 기반. 이 문서의 모든 수치는
`build/audit_content.py` 산출물(`data/*.csv`)과 코드 직접 확인으로 검증했다.

## 1. 시스템 개요

| 항목 | 값 |
|---|---|
| 프레임워크 | 자체 정적 생성기 `build/build.py` (4,521줄, 런타임 의존성 0) |
| 원고 | `source/` 마크다운 56개 · 5,548섹션 · 약 225,000단어(48,600줄) |
| 산출물 | `site/` HTML 313개 = 실페이지 252 + 리다이렉트 스텁 61 |
| 배포 | GitHub Actions → gh-pages (`main` 푸시 = 즉시 배포) |
| 검사 | 빌드 내 가드 15종 + `hig_check.py` (Playwright) |

## 2. 빌드가 실제로 읽는 원천 (Source of Truth 실측)

`build.py`는 디렉터리를 훑지 않고 **명시 경로만** 읽는다. 따라서 아래 목록이
사이트의 전체 원천이다.

### 2.1 본문 (CHAPTERS, build.py:66-97)

- `CURRENT/10_Core/01_How_to_Use_This_Guidebook_v1.0.md`
- `CURRENT/10_Core/02_Whole_Trip_Experience_Highlights_v1.0.md`
- `CURRENT/10_Core/03_Whole_Trip_Master_Itinerary_v1.2.md`
- `CURRENT/20_Regional_Chapters/` — **v2.0/v2.1 8개만.** v1.x는 어떤 코드도 열지 않는다.

### 2.2 데이터·에셋

| 파일 | 용도 |
|---|---|
| `ASSETS/91_Place_Registry_v1.0.md` | 장소 그래프 정본 (82 spot + 3 node → places/ 82페이지) |
| `ASSETS/75_Execution_Maps/*` | 실행지도 8종 + GeoJSON/KML |
| `ASSETS/80_Daily_Mobile_Guide_Images/*` | 데일리 카드 43장 (+Phase4 13장) |
| `ASSETS/88_Representative_Public_Photos/*` + 크레딧 MD | 히어로 사진 8장 (크레딧 가드) |
| `ASSETS/85_Editorial_Visuals/*` | 편집 다이어그램 6종 |
| `OPERATIONS/TP_Europe_Travel_Master_Tracker_v1.2.xlsx` | 트래커 6페이지 + content-model |
| `OPERATIONS/100/116/41/117` | 실행감사표·검증 3등록부 |
| `ASSETS/89·90`, `Governance/89·90`, `OPERATIONS/118` | **가드 전용** (구조 검사만, 렌더 안 함) |

### 2.3 빌드가 전혀 읽지 않는 파일 (전량 감사 확인)

- **지역 챕터 구버전 8개** `20_Regional_Chapters/*_v1.*.md`
- **Reader Edition 전체 9개** `30_Reader_Edition/`
- **`10_Core/42_TP_Europe_Travel_Guidebook_Master_v1.4.md`** (8,888줄 — 저장소의 18%)
- 거버넌스 색인 2종 (`00_Current_Source_of_Truth_Index_v1.9`, `37_Supersession_Matrix_v1.1`) · `88_Editorial_Style_Guide`
- OPERATIONS: `103`(라우팅표 — 코드 `MAP_DAY_SPANS`로 재구현됨) · `110` · `119` · `90_Scorecard` · `Decision_Register_v0.4`
- ASSETS 색인류: `70·71·75_Index·80_Index·85_Index·85_Visual_Asset_Register·86·87`
- `handoff/` 47개 (2026-08-01 인계 번들 — Girona v2.1 구사본 포함)

## 3. 라우트 구조 (313 URL)

```
/                       홈 (여정)
/regions.html           지역 축 뿌리
/credits.html
/chapters/{how-to-use|highlights|itinerary}.html      코어 3
/chapters/<region>/     허브 + schedule + 주제 9종 (8지역 × 11 = 88)
/chapters/<region>/day-NN.html                        리다이렉트 50 (→ daily)
/chapters/NN.html                                     리다이렉트 11 (구 번호 주소)
/daily/day-NN.html      일자 정본 43 + index
/places/<slug>.html     장소 정본 82 + index
/topics/<slug>.html     주제 축 13 + index
/maps/                  지역 지도 8 + index + offline
/tracker/               트래커 6 + index
```

**정본 위치는 이미 축별로 유일하다**: 하루=`daily/`, 장소=`places/`,
지역 서사=`chapters/<region>/`. 챕터의 day 페이지는 전부 리다이렉트임을
가드가 강제한다(사본 재발 방지).

## 4. 내비게이션 (실측)

| 레벨 | 구현 | 정의 위치 |
|---|---|---|
| L0 하단탭 5개 | 오늘·일정·지역·준비·검색 | build.py:1755 하드코딩 (nav.js:188, 가드 :3960과 3중 동기 필요) |
| L1 좌표 바 | 일자·지역·주제 | 홈·축 뿌리·데일리 47페이지에만 렌더 |
| L2 서브내비 | 형제 이동 | `siblings_nav()` 공용 1개, 228페이지 |
| 상단바 | 경로 + 검색 | 햄버거 없음 (설계 원칙) |
| 꼬리말 | credits · offline 2링크 | 하드코딩 |

검색 인덱스 1,899건은 `data.js`로 일원 생성. **메뉴 사본 문제는 이전
리팩터에서 이미 해소된 상태**다. 상세는 `navigation-consolidation-plan.md`.

## 5. 유지보수 위험요소

1. **헤딩 문자열이 5곳에서 로드베어링**: `CAT_OVERRIDES`(~180쌍) ·
   phase9/10 가드의 리터럴 헤딩 · 레지스트리 `헤딩` 칸 · TOC 앵커 ·
   장소 본문 추출. **v2 챕터의 헤딩을 고치는 편집은 이 5곳과 함께 움직여야 한다.**
2. 매직 넘버 가드: Day 섹션 50 · 43일 · 지도 기준점 65 · 도시어 51 ·
   검증 F001-18 등 — 콘텐츠 증감 시 가드 갱신 필수.
3. `PLACES`(build.py:772)와 레지스트리의 장소 목록 이중화 — 가드가 한
   방향(레지스트리→PLACES)만 검사, 위키 제목은 양쪽에 따로 존재.
4. `gen_place_registry.py` 재실행 시 손편집(위키 열 포함) 소실 — CLAUDE.md 경고 유지.
5. 하단탭·홈 액션 문자열이 코드-가드-nav.js 3중 하드코딩.
6. 죽은 코드: `strip_title_number`(미호출) · `chapter_subnav`/`chapter_coords`
   (전 지역 분할 이후 도달 불가) · `build_chapters`의 비분할 렌더 경로
   (지역 8개 전부 분할이라 결과 폐기됨).
7. 레지스트리 꼬리말 집계 `spot 83`은 실제 82와 불일치 (손편집 드리프트).
8. `hig_check.py` 표본에 리다이렉트 스텁(`chapters/paris/day-37.html`)이
   들어 있어 표본 1칸이 낭비된다.

## 6. 파일 목록·수치

전체 파일 단위 인벤토리는 `data/content-inventory.csv`(섹션 5,548행) ·
`data/site-page-inventory.csv`(313행), 중복은 `data/content-duplicate-matrix.csv`
(712그룹), 반복 문구는 `data/content-boilerplate.csv` 참조.
