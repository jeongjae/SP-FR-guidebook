---
title: "RS01 Phase 0 — 영향 범위 전수 조사 보고"
version: "1.0"
created: "2026-08-28"
scope: "Day 12–22 (2026-09-09 ~ 2026-09-19) Verdon 1박 삽입"
status: "Phase 1 착수 승인 대기"
artifacts: ["RS01_IMPACT_INVENTORY.csv", "RS01_PRE_CHANGE_SNAPSHOT.md"]
---

# Phase 0 보고 — 영향 범위 전수 조사

**파일은 한 줄도 수정하지 않았다.** 조사 산출물 3개만 새로 만들었다.

## 1. 조사 결과 요약

검색 패턴: `2026-09-(09~19)` · `9/(9~19)` · `Day (12~22)`
제외: `site/`(빌드 산출물), `.git/`, `_maps_download/`

| 지표 | 값 |
|---|---:|
| 참조가 있는 파일 | **195개** |
| 총 참조 라인 | **1,550개** |
| 영향받는 장소 | **43개** / 전체 117개 |

### 처리 구분별

| 처리 | 파일 수 | 의미 |
|---|---:|---|
| `rewrite` | 8 | Day SOT 전면 재작성 (day-12~19) |
| `edit` | 44 | 손으로 내용 수정 |
| `regenerate` | 44 | 빌드·스크립트로 재생성 |
| `review` | 51 | 생성 스크립트 — 갱신 여부 개별 판단 |
| `verify` | 12 | 확인만, 수정 없을 가능성 높음 |
| `archive` | **36** | **수정 금지** — 시점 감사 기록 |

전체 목록은 `RS01_IMPACT_INVENTORY.csv` (phase·매치수 순 정렬).

## 2. 계획을 바꾸는 발견 4가지

### 2.1 [해소] 챕터 파일 리네임이 필요 없다

지시서 2.3에서 미결로 남긴 문제다. 빌드는 파일명 순서에 의존하지 않는다 —
`build/promote_regions.py:29`와 `build/content_guard.py:33`의 `CHAPTER_FILES`
딕셔너리가 slug→파일명을 **명시적으로** 매핑한다.

```
CHAPTER_FILES = { "barcelona": "04_...", "girona": "05_...", "nice": "06_...", ... }
```

→ `"verdon": "06B_Verdon_Moustiers_v1.0.md"` 한 줄을 두 곳에 추가하면 끝이다.
**07~11 챕터 4개 리네임과 그에 딸린 경로 참조 붕괴가 사라졌다.** 작업량이
눈에 띄게 줄었다.

### 2.2 [유리] Day→지역 매핑은 자동 유도된다

`build/model.py:639 load_days()`가 각 Day의 지역을 `itinerary.json`의 `stays`
날짜 범위에서 계산한다. daily-card에는 지역 필드가 없다.

```python
sleeping = [s for s in stays if checkin <= d < checkout]
primary  = (sleeping or here)[-1]["key"]
```

→ itinerary.json만 정확하면 **Day 12는 자동으로 verdon에 붙는다.**
단 `primary`가 리스트의 **마지막** 원소를 쓰므로, `stays` 배열에서
**verdon은 반드시 nice 다음**에 와야 한다. (9/9은 nice 체크아웃일이자
verdon 체크인일이라 둘 다 `here`에 들어온다.)

### 2.3 [주의] 빌드에 재확인 기한 게이트가 있다

`model.py:758-782`가 `transit-facts.json`·`transit-resources.json`의
`recheckBy`를 **해당 지역 체크인 이전**으로 강제하고, 위반 시 빌드를 중단한다.

이번 변경은 aix·luberon·avignon 체크인을 모두 **하루 뒤로** 미루므로 기존
항목은 전부 유효하다. 문제는 신규 verdon이다 — 등록하려면 `verifiedAt` ≤ 오늘,
`recheckBy` < 2026-09-09를 만족하는 **실제 검증 이력**이 있어야 한다.
조사 없이 값을 지어내면 이 게이트의 존재 이유가 사라진다.

### 2.4 [추가 발견] 지시서에 없던 동기화 대상 2개

grep으로 잡히지 않은 것들이다.

| 파일 | 성격 |
|---|---|
| `source/OPERATIONS/TP_Europe_Travel_Master_Tracker_v1.2.xlsx` | **바이너리 마스터 트래커.** `scripts/sync_provence_itinerary_sot.py`가 하드코딩된 날짜표로 갱신한다 |
| `source/ASSETS/maps/daily-routes.json` | 일자별 경로 정본. 같은 스크립트가 함께 쓴다 |

`sync_provence_itinerary_sot.py`의 `MASTER` 딕셔너리에 구 일정(9/13 Gordes
체크인, "Avignon 5박" 등)이 **문자열로 박혀 있다.** 이 스크립트를 고치지 않고
다시 돌리면 구 일정이 되살아난다.

## 3. verdon 지역 신설에 필요한 등록 슬롯 — 7곳

현재 8개 지역이 아래 7개 파일에 **각각** 등록돼 있다. verdon은 7곳 전부에
들어가야 하고, 하나라도 빠지면 빌드나 렌더가 어긋난다.

| # | 파일 | 현재 키 |
|---:|---|---|
| 1 | `source/CURRENT/10_Core/itinerary.json` (stays) | 8 |
| 2 | `source/CURRENT/10_Core/regions.json` | 8 |
| 3 | `data/region-essentials.json` | 8 |
| 4 | `data/transit-facts.json` | 8 — **2.3 게이트 적용** |
| 5 | `data/transit-resources.json` | 8 — **2.3 게이트 적용** |
| 6 | `data/region-consolidation.json` (consolidated + layerTitles) | 8 |
| 7 | `build/promote_regions.py` · `build/content_guard.py` (CHAPTER_FILES ×2) | 8 |

## 4. 영향받는 장소 43개

| 지역 | 장소 수 |
|---|---:|
| avignon | 17 |
| aix | 14 |
| luberon | 11 |
| nice | 1 |

`data/place-days.json`의 `days` 배열이 전부 재계산 대상이다. 신규 Verdon 장소
5개(Moustiers·협곡·Route des Crêtes·Sainte-Croix 호수·Valensole)가 추가되면
48개가 된다.

## 5. 손대지 않을 것 — 과거 감사 기록 36개

`AV01_`·`AX01_`·`EX01_`·`FCR03_`·`NC01F_`·`MP01_` 계열 QA·감사 리포트는
**그 시점에 무엇을 검증했는지의 기록**이다. 지금 일정에 맞춰 고쳐 쓰면 감사
이력이 위조된다.

→ 수정하지 않고 `data/superseded.json`에 "RS01로 대체됨"을 등재한다.
`handoff/`·`docs/` 하위도 같다.

반대로 `EX14_`·`EX15_`·`DAY_`·`CRITICAL_`·`PLACE_MASTER_` 계열은 **현재
상태를 나타내는 살아있는 대장**이므로 갱신 대상이다. 이 구분이
`RS01_IMPACT_INVENTORY.csv`의 `처리` 열에 들어 있다.

## 6. 작업 환경 리스크

`git` 명령이 이 마운트 경유로는 **45초 타임아웃 안에 끝나지 않는다.**
브랜치 생성·커밋·PR은 사용자 로컬 터미널에서 직접 실행하는 편이 안전하다.
파일 수정 자체는 정상 속도다.

## 7. 다음 단계 — Phase 1 착수 제안

| 순서 | 작업 | 게이트 |
|---:|---|---|
| 1 | `feat/verdon-reschedule` 브랜치 생성 (**사용자 로컬 실행**) | — |
| 2 | 빌드 기준선 확보 — 변경 전 빌드가 통과하는지 확인 | 통과해야 진행 |
| 3 | `itinerary.json` stays 수정 (verdon 삽입, 3개 지역 날짜 이동) | 총 42박·43일 |
| 4 | `regions.json`·`region-consolidation.json`·`CHAPTER_FILES` ×2에 verdon 등록 | — |
| 5 | 빌드 재실행 — 실패 지점으로 남은 필수 슬롯을 역으로 확인 | — |

**3~5는 verdon 챕터 원고와 transit 데이터가 없으면 빌드가 깨진다.**
그래서 Phase 1을 "골격만 넣고 빌드를 일부러 깨뜨려 필수 슬롯을 드러내는"
단계로 쓰고, Phase 2(조사·콘텐츠 작성)에서 채워 복구하는 순서를 제안한다.
이 방법이 누락 슬롯을 추측 대신 빌드 오류로 확인시켜 준다.

## 8. 승인이 필요한 결정 2가지

1. **Verdon 챕터 파일명** — `06B_Verdon_Moustiers_v1.0.md`로 삽입 (리네임 없음).
   기존 번호 체계에 `06B`가 끼는 것을 허용하는지.
2. **git 작업 주체** — 브랜치·커밋을 사용자가 로컬에서 직접 실행할지,
   느리더라도 세션에서 시도할지.
