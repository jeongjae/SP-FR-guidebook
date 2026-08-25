# Provence 출발 전 확정 점검 · Daily Card Validator

- 점검일: 2026-08-25
- 일정 잠금: Day 12–15 변경 없음, Day 16–19 실행 정보만 보강, Day 20+ 일정 의미 변경 없음
- 작업 시작 `origin/main`: `8ea45fb6`
- 승인 Provence 커밋: `01415bd8` ancestor 확인

## Provence 실행 상태

| 항목 | 상태 | 처분 |
|---|---|---|
| Gordes 9/13–9/15 숙소 | ACTION REQUIRED | 저장소 Master Tracker에 `미예약`. 후보 주소·좌표를 확정 숙소로 사용하지 않음. |
| Avignon 9/15–9/20 숙소 | ACTION REQUIRED | Master Tracker에 `미예약`. `La Terrasse du Clocher`는 후보일 뿐. |
| La Récréation | CONFIRMED / ACTION REQUIRED / FALLBACK | 영업시간·요금은 공식 확인. 9/13 실제 좌석은 미확인. 실패 시 같은 점심 창의 Lourmarin 현장 식사. |
| Bistrot Le 5 | CONFIRMED / FALLBACK | 공식 사이트상 월요일 휴무. Day 17은 식당에 의존하지 않음. |
| Sénanque | CONFIRMED / ACTION REQUIRED / FALLBACK | 9/14 15:00·16:00·17:00 HistoPad 회차 표시 확인. 16:00 예약·오프라인 저장 필요. 미예약 시 외관·계곡만 MUST. |
| Orange | FALLBACK | OPTIONAL BONUS 유지, 미예약, 기본 경로 미포함. |

## Daily Card validator 분류

작업 직전 실행 결과는 안내문의 31건과 달리 **33건**이었다. 현재 validator 출력을 기준선으로 사용했다.

| 유형 | 시작 | 수정 | 잔여 | 처분 |
|---|---:|---:|---:|---|
| A. Schema-only / formatting | 3 | 3 | 0 | `related_place_refs` 허용, 기존 9-stop card 허용. 일정 변경 없음. |
| B. Generated-data drift | 16 | 16 | 0 | Day 9–11·15의 표시 도시명 변경 후 기존 렌더 artifact slug를 재사용. |
| C. Missing reference / link | 0 | 0 | 0 | 해당 없음. |
| D. Legacy optional/status representation | 14 | 14 | 0 | 주소가 확정된 숙소의 좌표 미확인, 저녁 후 숙소 귀환, Day 43 귀국·자택 종료를 정상 표현으로 판정. |
| E. Actual itinerary/content contradiction | 0 | 0 | 0 | 일정 변경이 필요한 항목 없음. |
| **합계** | **33** | **33** | **0** | Day 16–19 오류 0, 전체 오류 0. |

## Semantic guard

Day 20–43 Daily Card의 day/date/city/title/time, stop 순서·시각·장소·optional, leg, transport, highlights, backup과 Master/Avignon Day 20+ 본문을 해시 비교한다. 작업 전 해시는 `48844d19d98300926bbe7b5e974906cca9f56f028b24e5615d3cf4dbd5629047`이다.

## QA 결과

- production-equivalent full build: PASS · 376 pages · Daily Card 43일
- pytest: PASS · 57 tests
- build validation unittest: PASS · 20 tests
- Daily Card validator: PASS · 43일 · 오류 0 · 경고 0
- Canonical Place validation/content audit: PASS · 139 files · reference 오류 0
- internal broken link: 0
- HIG: PASS · contrast 위반 0
- viewport: PASS · 360/390/430/768/1024/1440 px · horizontal overflow 0
- targeted Playwright smoke: PASS · index/schedule/Day 16–19 × 360/390/430/1440 px · console error 0
- PWA offline: PASS · critical/deep navigation 유지
- Day 20+ semantic guard: PASS · `origin/main`과 일정 의미 동일

## Production 기준선

- Pages workflow는 `main` push를 build/deploy source로 사용한다.
- 점검 시 `main`과 `gh-pages`는 `8ea45fb6` 기준이다.
- production Day 16 Lourmarin/Gordes, Day 17 Roussillon/Sénanque, Day 18 L'Isle-sur-la-Sorgue, Day 19 Saint-Rémy/Les Baux smoke test는 모두 통과했다.
- 이 작업은 Git 정책에 따라 로컬 커밋까지만 수행하며 push·merge·PR·신규 배포는 하지 않는다.
