# RS 개편 기준선 v1.0

작성일 2026-08-16 · Rick Steves형 콘텐츠 구조 개편 Phase 0 산출물.
이 문서는 개편 착수 시점의 상태 스냅숏이다. 개편 중 판단이 갈리면 이 문서가 아니라
**현행 정본 파일**(아래 §2)이 우선한다.

## 1. 저장소 상태 (2026-08-16 기준)

| 항목 | 값 |
|---|---|
| 작업 워크트리 | `/mnt/c/Users/NB-24021500/source/worktrees/SP-FR-content-dev` |
| 브랜치 | `jeongjae/content-improvement` |
| HEAD | `4c9b7cb8` (Merge PR #145, 예약서 대조 2차) |
| 작업트리 | **클린** — 미커밋 변경 0건 |
| main | `4c9b7cb8` (동일 커밋 — 분기 없음) |

다른 워크트리 (이번 작업과의 충돌 여부):

| 워크트리 | 브랜치 | HEAD | 충돌 판정 |
|---|---|---|---|
| `~/.openclaw-spfr-team/phase17/tasks/*` 3개 | `spfr-task/chore-diagnostics-data`, `spfr-task/fix-schedule-single-source(-r2)` | `e1a1115f` (구 커밋) | **주의** — "schedule single source" 작업이 일정 정본을 만질 수 있음. 니스 파일럿 착수 전 머지 여부 확인 필요 |
| `orca/.../update-plan` | `jeongjae/r5b-essential-photos` | `2aef4587` | 무관 (이미 머지된 사진 작업) |
| `SP-FR-kimi-claw-pilot` | `jeongjae/kimi-claw-pilot` | `e1a1115f` | 무관 (게이트웨이 파일럿) |

Phase 0–1 산출물은 `docs/RS_RESTRUCTURE_*` 신규 파일뿐이며 위 어느 브랜치와도 파일이 겹치지 않는다.

## 2. 정본·비정본 경계

원칙(00_Current_Source_of_Truth_Index_v2.0.md): 정보 유형마다 정본은 한 파일, 사본은 `source/ARCHIVE/` 에만.

| 구분 | 경로 | 개편에서의 취급 |
|---|---|---|
| 구조화 정본 | `source/CURRENT/10_Core/itinerary.json` | 날짜·거점·박수의 기계 정본. **변경 금지** |
| 코어 원고 | `source/CURRENT/10_Core/01·02·03` | 03 마스터일정 표 앞 3열(Day·날짜·거점)은 빌드가 파싱하는 사실상 스키마 |
| 지역 챕터 정본 | `source/CURRENT/20_Regional_Chapters/04~11` (8개, v2.x만) | **개편의 주 대상.** 새 버전 파일 금지, 제자리 수정 |
| 편집 표준 | `00_Governance/88·89·90` | 개편과 겹침·충돌 있음 (SCOPE 문서 §3) |
| 장소 정본 | `source/ASSETS/91_Place_Registry_v1.0.md` | 등급 헤딩 개명 시 동반 갱신 |
| 지도 정본 | `source/ASSETS/maps/*.json` (D-07) | 변경 금지 (스트림 ③ 산출물) |
| 데일리 카드 | `data/daily-cards/day-NN.json` | 변경 금지 (스트림 ① 산출물) |
| 운영 정본 | `source/OPERATIONS/` 7건 (트래커 xlsx·100·41·116·117·118·90) | 원고 아님. 편집 흔적 이동의 수용처 후보 |
| URL 정본 | `docs/COMMERCIAL_REDESIGN_URL_MAP_v1.0.csv` (keep 266 · redirect 62, D-08) | URL 변경 시 redirect 행 추가만, 삭제 금지 |
| 아카이브 | `source/ARCHIVE/` | 여행 판단에 쓰지 않음. 개편에서 손대지 않음 |
| 산출물 | `site/` (gitignore) | 직접 편집 금지 |

**Daily 43일의 정본 위치**: 별도 파일이 아니라 **지역 챕터 원고 안의 Day 절**이다.
빌드가 `schedule` 카테고리에서 Day 절을 떼어 `daily/day-NN.html` 로 보내고, 실행 요약
3필드는 `OPERATIONS/100_..._Execution_Audit` 표에서 온다. 챕터 쪽 `day-*.html` 61개는
전부 리다이렉트이며 가드가 사본 부활을 차단한다. → **Region 감량에서 Day 절을 지우면
Daily 페이지가 사라진다. Day 절은 감량 대상이 아니라 이동·유지 대상이다.**

## 3. 현행 사이트맵 (2026-08-16 로컬 빌드 실측)

`python3 build/build.py` 전 가드 통과, **328 HTML** (리다이렉트 스텁 63 포함).

| 유형 | HTML 수 | 비고 |
|---|---:|---|
| chapters | 152 | 실페이지 91 + 리다이렉트 61 (day-NN 스텁 등) |
| places | 96 | 장소 95 + 리다이렉트 1 (lourmarin-2) |
| daily | 44 | 43일 + index |
| topics | 14 | 주제 축 |
| maps | 10 | 8지역 + index + offline |
| tracker | 7 | |
| root | 4 | index·regions·credits 등 |
| about | 1 | |

레지스트리: spot 94 · node 3 · 등급 미정 0. 지도 기준점 113. 예약 레코드 R001–R030 (P0 15).
공식검증 F001–F042. 검색 인덱스 약 1,899건.

챕터 원고 규모 (개편 감량률의 기준선):

| 챕터 | 글자수(wc -m) | h2 | h3 | h4 |
|---|---:|---:|---:|---:|
| 04 Barcelona·Sitges | 70,385 | 60 | 111 | 27 |
| 05 Girona·Collioure·Empordà | 50,416 | 93 | 68 | 15 |
| 06 Nice·Côte d'Azur | 44,282 | 57 | 71 | 24 |
| 07 Aix-en-Provence | 68,035 | 62 | 116 | 45 |
| 08 Luberon | 60,543 | 69 | 139 | 28 |
| 09 Avignon·Alpilles·Pont du Gard | 64,737 | 61 | 120 | 36 |
| 10 Lyon | 62,058 | 68 | 104 | 33 |
| 11 Paris | 86,285 | 80 | 157 | 36 |
| **계** | **506,741** | 550 | 886 | 244 |

(참고: CONTENT_QUALITY_PLAN §1.1 의 자수 합계 약 465,166자는 다른 측정 방식 —
감량률 보고 시 어느 기준을 쓰는지 명시할 것.)

## 4. 43일 일정 기준선

itinerary.json (schemaVersion 1.0): 2026-08-29 ~ 2026-10-10, 43일 42박 (숙박 41박 + 기내 1박).
빌드가 이 JSON 을 직접 읽고 8개 제약(연속성·박수 정합 등)을 강제한다.

| # | key | 거점 | 체크인→체크아웃 | 박수 | Day |
|---:|---|---|---|---:|---|
| 1 | barcelona | Barcelona | 08-29 → 09-01 | 3 | 1–3 |
| 2 | girona | Bàscara | 09-01 → 09-04 | 3 | 4–6 |
| 3 | nice | Nice | 09-04 → 09-09 | 5 | 7–11 |
| 4 | aix | Aix-en-Provence | 09-09 → 09-13 | 4 | 12–15 |
| 5 | luberon | Luberon | 09-13 → 09-16 | 3 | 16–18 |
| 6 | avignon | Avignon | 09-16 → 09-20 | 4 | 19–22 |
| 7 | lyon | Lyon | 09-20 → 09-24 | 4 | 23–26 |
| 8 | paris | Paris | 09-24 → 10-09 | 15 | 27–41 |

배분 문자열 `3/3/5/4/3/4/4/15박` — Phase 8 가드가 리터럴로 잠금.
Day 42 = 10/9 CDG 출국(OZ502 19:10, 기내박), Day 43 = 10/10 인천 도착.

장거리 이동일 8일: Day 4 (BCN→Bàscara, 렌터카 인수 Sants 07:00), Day 7 (Bàscara→Nice,
BCN 반납 + VY1521 15:30), Day 12 (Nice→Aix, Nice역 인수 09:00), Day 16 (Aix→Luberon),
Day 19 (Luberon→Avignon), Day 23 (Avignon→Lyon, 반납 09:00 + TGV 12176 10:22), Day 27
(Lyon→Paris, TGV 6618 13:04), Day 42 (Paris→CDG).

렌터카 2사이클(9/1–9/4, 9/9–9/20) · TGV 2회 · 항공 3회(OZ511 입국, VY1521, OZ502 출국).

**알려진 불일치 1건**: 03 마스터일정의 장거리 이동일 표가 Day 7 을 "이동수단·반납지
재확인 필요"로 두고 있으나 본문·예약 레지스터는 VY1521 확정 — 표가 구판이다.
Phase 2 니스 파일럿에서 표만 정정(사실 변경 아님, 정본 정합화).

## 5. 참고자료 분류

- 첨부 PDF·v1.13 계열 문서: **참고자료.** 현행 사이트·`source/CURRENT/` 와 충돌 시 현행 우선.
- `source/ARCHIVE/`: 여행 판단에 사용하지 않음.
- docs/ 의 기존 Phase 0–10 보고서: D-01 에 따라 근거에서 제외 — 수치는 코드·데이터에서 재실측.

## 6. Phase 0 변경 0건 확인

이번 단계에서 변경한 파일은 `docs/RS_RESTRUCTURE_*` 6건뿐이다.
`source/CURRENT/`·`source/ASSETS/`·`source/OPERATIONS/`·`build/`·`data/`·`templates/` 변경 0건.
`site/` 는 로컬 빌드 산출물(gitignore) 재생성만 있었고 커밋 대상이 아니다.
