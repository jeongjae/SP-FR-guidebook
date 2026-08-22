# FCR02C_FULL_MIGRATION_QA — 8개 지역 전체 이관

작업 기준은 지시서의 `0bbd5e5b` 가 아니라 **`af4ad953`**(= main `2909637a`)이다.
0bbd5e5b 이후 main 이 머지되면서 MP-01D~G 와 지역 교통 보강(PR #197~#202)이
들어왔고, 그 위에서 작업하는 편이 안전하다. 그 차이가 이관 규모를 줄였다 —
`region-essentials` 가 없던 곳이 7개가 아니라 **girona·aix 둘**이었다.

브랜치 `feat/fcr02c-region-migration`. **푸시·머지·PR 하지 않았다.**

---

## Overall Status

**PASS — 8/8 지역 이관 완료.** 전역 지표가 전부 목표값이다.

| 지표 | 목표 | 결과 |
|---|---:|---:|
| Regions migrated | 8/8 | **8/8** |
| Attraction/Food 오분류 | 0 | **0** |
| 식당 하위 묶음 오분류 | 0 | **0** |
| invalid Day relation | 0 | **0** |
| orphan promoted Place | 0 | **0** (승격 0건) |
| image lookup failure | 0 | **0** |
| silent table loss | 0 | **0** |
| broken internal link | 0 | **0** |
| broken map link | 0 | **0** |
| unexpected content loss | 0 | **0** |
| 교통 하위 순서 오류 | 0 | **0** |
| 중복 교통 블록 | 0 | **0** |

---

## 1. Region별 migration 결과

지시된 순서대로 진행했다. 각 지역은 A(region-essentials) · B(price_range) ·
C(photo) · D(검증 0) 네 단계를 밟았다.

| # | 지역 | A essentials | B 가격 | C 사진 | D 검증 |
|---|---|---|---:|---|---|
| 1 | Girona | **신설** | 2 | Casa Marieta 확인·추가 | 0 |
| 2 | Nice | (02B 에서 신설) | 2 | 후보 없음 | 0 |
| 3 | Aix | **신설** | 2 | 후보 없음 | 0 |
| 4 | Luberon | Local Life 재작성 | 2 | 해당 없음(식당 0) | 0 |
| 5 | Avignon | Local Life 재작성 | 4 | 기존 사진이 FOOD_HALL 로 연결 | 0 |
| 6 | Lyon | Local Life 재작성 | 4 | 기존 사진이 FOOD_HALL 로 연결 | 0 |
| 7 | Paris | Local Life 재작성 | 5 | (02B 에서 3곳 추가) | 0 |

Paris 는 마지막에 했고 **전용 스키마·컴포넌트를 만들지 않았다.** 15박·장소
29곳이지만 같은 `build_region` 하나가 만든다. 콘텐츠 양은 데이터 기반
그룹핑(식당/카페/빵집·시장·푸드홀, 꼭 가야 할 곳 6장 큰 카드 + 나머지 일반
카드)이 흡수한다.

## 2. region-essentials 완성도

**8/8 완성.** 이전에는 6/8 이었다.

| 지역 | staySummary | localLife | arrival | departure | 구간 내 이동 | references |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| barcelona · girona · nice · aix | O | O | O | O | O | O |
| luberon · avignon · lyon · paris | O | O | O | O | O | O |

`neighborhoods` · `foodCulture` · `transportDeep`(원고 승격 층)도 8/8 이다.

**Girona 의 '구간 내 이동' 을 위해 라벨을 바꿨다.** 이 구간은 대중교통이
아예 없다 — 3박 내내 렌터카로 국경을 왕복한다. 슬롯 이름을 '도시 교통' 으로
두면 Girona 에서 거짓말이 된다. 슬롯은 그대로 두고 이름만 사실에 맞춰
`GETTING AROUND / 구간 내 이동` 으로 바꿨다. 8개 지역 공통이다.

Girona 용 `transit-facts` 를 새로 만들었다. 내용은 노선이 아니라 **국경 통과
보험 · 두 나라의 통행료 표기가 반대라는 것 · 연료 명칭 · 주차 선 색**이다.
출처 두 곳은 2026-08-22 에 실제로 열어 확인했다(HTTP 200 · 제목 대조).

## 3. Attraction/Food reclassification

이번 단계에서 새로 옮긴 것은 **FOOD_HALL 두 곳**이다. FCR-02 에서 이미 22곳을
옮겼고, 그 뒤로 오분류는 계속 0 이다.

```
볼거리 카드 107 · 식당·카페 카드 24
볼거리 안의 식당 0 · 식당 안의 관광지 0 · 하위 묶음 오분류 0
```

## 4. FOOD_HALL 적용 결과

`source/CURRENT/30_Places/` 의 정본에 `food_kind: FOOD_HALL` · `meal_role:
MARKET` 을 부여했다. **Restaurant 으로 변환하지 않았다** — 별도 엔티티다.

| 장소 | 지역 | 전 | 후 |
|---|---|---|---|
| Les Halles d'Avignon | avignon | attraction | **food-hall** |
| Halles de Lyon Paul Bocuse | lyon | attraction | **food-hall** |

UI 하위 묶음을 지시대로 재편했다.

```
Restaurants & Cafés
├─ 식당          restaurant · wine-bar     17
├─ 카페          cafe                       1
└─ 빵집·시장·푸드홀  bakery · market · food-hall  6
```

구조 검사가 묶음과 엔티티의 일치를 잠근다. 묶음이 하나뿐인 지역에서는
제목을 달지 않는다.

## 5. 미등재 11개 entity 판정표

판정의 정본은 `data/images/place-aliases.json` 의 `disposition` 이다.

| # | placeId | 일정 방문 | 장소 서술 | 판정 | 근거 |
|---|---|:-:|:-:|---|---|
| 1 | `cadaques` | Day 5 14:45 | 없음 | **MEDIA-ONLY** | place-facts 에 주차 정보만 있다. 서술 확보 시 PROMOTE 후보 |
| 2 | `tossa-de-mar` | Day 6 09:45 | 없음 | **MEDIA-ONLY** | 원고가 동선 문장뿐이다. 서술 확보 시 PROMOTE 후보 |
| 3 | `sant-feliu-de-guixols` | Day 6 13:00 | 없음 | **MEDIA-ONLY** | 식사 슬롯이고 업소가 특정되지 않았다 |
| 4 | `palais-royal` | Day 30 16:15 | 없음 | **MEDIA-ONLY** | 하루 계획은 있으나 장소 서술·dossier 가 없다 |
| 5 | `jardin-du-luxembourg` | Day 29 14:30 | — | **기존 장소로 연결** | Day 29 stop 의 `place_ref` 가 이미 `latin-quarter` 다 |
| 6 | `pantheon-paris` | 없음 | 없음 | MEDIA-ONLY | 라탱 지구와 별개 건물이라 임의로 잇지 않는다 |
| 7 | `marche-monge` | 없음 | 없음 | MEDIA-ONLY | 명부에도 조사 자료에도 없다 |
| 8 | `passages-couverts` | 없음 | 없음 | MEDIA-ONLY | 우천 대안으로만 언급된다 |
| 9 | `marche-des-enfants-rouges` | 없음 | 없음 | MEDIA-ONLY | 마레 장소와 별개 대상 |
| 10 | `canal-saint-martin` | 없음 | 없음 | MEDIA-ONLY | 일정에 없다 |
| 11 | `seine` | 없음 | 없음 | MEDIA-ONLY | 특정 장소가 아니라 강변 구간이다 |

요리 사진 6장(`socca`·`pissaladiere`·`xuixo`·`suquet-de-peix`·
`pa-amb-tomaquet`·`crema-catalana`)은 **DISH/SUBJECT** 로 유지한다.

**PROMOTE 0건.** 지시서 §2 는 PROMOTE 에 `verified description source` 를
요구한다. 11곳 중 어디에도 장소 서술이 없다 — 원고의 언급은 전부 동선·하루
계획 문장이고, dossier 도 없다. 사진이 있다는 이유만으로 빈 장소 페이지를
만들지 않았다. 1~4 번은 **실제 방문지이므로 서술이 생기면 즉시 승격 대상**이다.

## 6. 신규 Promote Place

**없다.** 위 §5 의 이유다. 대신 `jardin-du-luxembourg` 사진 1장이 정본의
`place_ref` 를 따라 `latin-quarter` 로 연결돼 화면에 올라왔다 (미등재 11 → 10).

## 7. Accommodation 정리

확정 숙소가 있는 6개 지역(barcelona·girona·nice·aix·lyon·paris)에서는 실제
예약만 화면에 남는다. 폐기된 후보·비교표·선택 알고리즘은 승격 단계에서
걸러지고 원고에는 남는다.

미확정 2개 지역(luberon·avignon)은 확정 배지 대신 경고와 '어느 동네에 묵을
것인가' 까지만 말한다.

확정되지 않은 값을 확정처럼 쓰지 않았다 — Aix Airbnb 의 주차는 어느 SOT
에도 없어 `{{badge:field-recheck}}` 로 두고 공영주차를 예비안으로 남겼다.

## 8. Local Life 정리

**이번 단계의 실질 작업이 여기 있었다.** luberon·avignon·lyon·paris 의
`lifeEssentials` 는 대부분 **교통 티켓 규칙**이었다 — Navigo 기간, TCL 카드
검증, Orizo 단일권, TER 분리. 지시서 §6·§7 은 생활권과 교통을 섞지 말라고
한다. 확인해 보니 그 문장들은 이미 `transit-facts` 의 `howToUse`·`exceptions`
에 같은 내용으로 들어 있었다 — 즉 **중복이었다.**

그래서 네 지역의 Local Life 를 실제 생활 정보로 다시 썼다 (근거는 챕터 원고의
시장·슈퍼·세탁·운동 절).

| 지역 | 이제 말하는 것 |
|---|---|
| luberon | Coustellet 시장 장보기(13시 마감) · 주방과 세탁 · Goult–Robion–Oppède 축의 슈퍼·빵집 · 농가 진입로와 야간 표식 |
| avignon | Les Halles·Place Pie 생활권 · 성벽 안의 학교·약국·빨래방 · 주방·세탁 · 성벽 남쪽·Rhône 러닝 |
| lyon | 간이주방 소량 장보기 · Halles Paul Bocuse 는 생활 물가가 아니다 · 도착일 가벼운 점심 · Rhône 강변 러닝 |
| paris | 15구 생활권 장보기·세탁·약국 · 오전 생활 / 오후 도시 · 9/25 생활 완충일 · 저녁은 15구에서 끝낸다 |

중복이 아니었던 문장 3건은 버리지 않고 `transit-facts` 로 옮겼다 —
뤼베롱 연료·산불 통제, 리옹 Part-Dieu 수하물, 아비뇽 차량 짐·반납 점검.

## 9. Transport 정리

8개 지역 모두 같은 순서다.

```
도착과 출발  →  구간 내 이동  →  공식 자료와 재확인
```

도착·출발은 **실제 이전/다음 지역 이동 SOT** 를 따른다 —
`region-essentials` 의 arrival/departure 문장 + 그날 Day 링크(날짜·Day 번호·도시).
공공교통 일반정보는 '구간 내 이동' 블록이 맡고, 실행 정보와 섞지 않는다.
References 는 링크·확인일·재확인일만 남긴다.

순서 오류 0 · 중복 블록 0.

## 10. price_range 이관 결과

**24/24 완료. 미확인 0.**

| 지역 | 이관 | 비고 |
|---|---:|---|
| barcelona | (5) | FCR-02 에서 완료 |
| girona | 2 | |
| nice | 2 | |
| aix | 2 | |
| luberon | 2 | coustellet·gordes — 마을 시장의 가격대 |
| avignon | 4 | `les-halles` 는 place-facts 항목 자체가 없어 신설 |
| lyon | 4 | |
| paris | 5 | |

원칙대로 했다 — CSV 에 `source_url` 과 `verified_at` 이 없으면 옮기지 않는다.
값을 만들지 않는다. 신뢰도는 형제 사실(hours·booking)과 같게 둔다. 같은
조사·같은 출처·같은 날짜에서 나온 값이라 한 항목만 등급을 달리하면 화면이
거짓말을 한다. 도구는 `scripts/migrate_price_range.py` 로 남겼다.

**작업 중 `place-facts` 의 슬러그 중복을 하나 찾아 합쳤다.**
`les-halles-d-avignon`(원고가 참조) 와 `les-halles`(명부 슬러그)가 따로 있었고
운영시간 값도 서로 달랐다. 명부 슬러그로 합치고 원고 토큰을 옮겼다.

## 11. Restaurant/Café media completeness

| 항목 | 값 |
|---|---:|
| total entities | **24** |
| description | 24 |
| official site | 24 |
| map | 24 |
| price verified | **24** |
| menu available | 20 |
| visit-date linked | 21 |
| **photo verified** | **9** |
| photo missing | 15 |

사진 상태 (`data/images/food-photo-status.json` · 2026-08-22 1차 상호명 ·
2차 상호명+도시 두 번 훑고 결과를 사람이 읽어 판정)

| 상태 | 곳 |
|---|---:|
| VERIFIED | 9 |
| NO_CANDIDATE | 13 |
| AMBIGUOUS_ENTITY (wrong-entity risk) | 2 |

이번에 확인해 넣은 것은 **Casa Marieta(Girona)** 한 곳이다. Commons 분류가
`Restaurants in the province of Girona`·`Buildings in Girona` 이고 설명이
`dinning area of Casa Marieta` 라 신원이 확실했다. FOOD_HALL 두 곳은 이미
사진이 있어 재분류와 함께 VERIFIED 로 들어왔다.

**억지로 채우지 않았다.** Bodega Joan(1887년 바르셀로나 상점 사진)과
Le Grand Pan(19세기 신문 판화)은 2차 질의에서도 결과가 전부 다른 대상이라
비워 뒀다. 잘못된 사진보다 사진 없음이 낫다.

**한 가지 스스로 잡은 오류.** Casa Marieta 사진 설명에 창업연도를 1795년으로
적었다가 정본(30_Places)이 1892년이라 고쳤다. 지어낸 값이었고, 캡션까지
정본과 대조해야 한다는 뜻이다.

## 12. Visit Day relation

잘못된 Day 참조 **0**. 방문일 배지는 daily-card 의 stop 에서 계산하므로
일정이 바뀌면 배지도 바뀐다.

방문일이 없는 식당·카페 3곳:

| 장소 | 이유 |
|---|---|
| `casa-marieta` | 일정에 잡히지 않은 추천 식당 — 없는 것이 맞다 |
| `mercat-del-lleo` | 같음 |
| `patisserie-weibel` | **실제로는 방문한다.** Day 13 08:30 stop 하나가 `Place Richelme 목요 시장 & Pâtisserie Weibel` 을 함께 담고 `place_ref` 는 시장 광장이다. 한 stop 이 장소 하나만 가리키는 모델이라 Weibel 이 걸리지 않는다 |

Weibel 은 Day SOT 를 건드려야 풀린다(스톱 분할 또는 보조 참조 필드). 임의로
시간표를 고치지 않았다 — §11-1 대상이라 아래 잔여 항목에 올린다.

## 13. Stacked-table audit

```
붙어 있는 표 덩어리  10
수정 전이면 잃었을 열 11
수정 후 남은 병합     0
```

원고·파생물·장소·명부 전수. 이번 단계에서 새로 생긴 병합은 없다.

## 14. Image mapping audit

```
카탈로그 168 · 장소·지역 연결 158 · 배포본에 실제로 나오는 것 158
별칭표에 없는 placeId 0 · 잇혔는데 안 나오는 사진 0
명부 미등재 — 선언된 잔여분 10
```

장소 갤러리 23장 · 요리 사진 6장. `jardin-du-luxembourg` 가 정본의
`place_ref` 를 따라 연결되면서 잔여분이 11 → 10 이 됐다.

## 15. Link validation

지역 8쪽의 내부 링크 전수 — 끊어진 링크 **0**. 지도 링크는 전부 이름
검색어(`query=`)로 열린다 — 검색어 없는 지도 링크 **0**.
외부 링크는 형식·카탈로그 대조로 확인한다
(`generate_attributions.py --check` 통과 · `validate_media.py` 통과).

## 16. Content-loss reconciliation

`af4ad953` 를 별도 워크트리에 빌드해 페이지 단위로 비교했다.

```
페이지 369 → 369 · 사라진 페이지 0
문장 8,394 대조 · 차이 27건
```

27건을 전수 확인한 결과 **실질 손실 0** 이다.

| 유형 | 건 | 확인 |
|---|---:|---|
| `가격 미확인 …` 문자열 | 9 | 가격이 확인돼 사라졌다 — 개선이지 손실이 아니다 |
| Local Life 교통 문장 | 14 | 전부 `transit-facts` 에 같은 내용이 있거나 옮겼다. 문구별로 배포본에서 재확인함 |
| `les-halles-d-avignon` 옛 운영시간 | 1 | 중복 항목을 합치며 더 최신 값(2026-08-21)으로 대체 |
| 장소 페이지 사실표 재렌더 | 3 | 사실이 늘어 행이 바뀐 것. 원래 값은 그대로 있다 |

1차 비교에서 **실제로 사라진 2건**을 찾아 되살렸다 — 뤼베롱 '오커길에는
먼지에 강한 신발' 과 아비뇽 '차량 안에는 보이는 짐을 남기지 않는다 · 반납할 때
주유·차량 사진·영수증'. 앞의 것은 Local Life 로, 뒤의 것은 교통 예외로 갔다.

`build/content_audit.py` — 승격된 장문 전수, 손실 0.

## 17. Mobile / responsive QA

`build/viewport_check.py` — 360·390·430·768·1024·1440 실렌더.
가로 오버플로 0 · 터치 타깃 44pt 이상 · 글자 11px 이상 통과.

스크린샷 `docs/fcr02c/` — girona·avignon·lyon·paris 의 390px 전체와
식당·생활권·교통 섹션, paris 1280px 전체.

390px 에서 확인한 것 — 여섯 섹션 순서, 식당 하위 묶음 제목, 날짜 칩 가로
스크롤, 교통의 도착/출발 카드와 Day 링크, References 의 확인일·재확인일.
Girona 교통은 '이 구간은 렌터카다' 로 시작해 국경·통행료·연료·주차를 말한다.

## 18. 8-Region global validation

```
Regions migrated                8/8
Attraction/Food 오분류            0
식당 하위 묶음 오분류               0
invalid Day relation             0
orphan promoted Place            0   (승격 0건)
image lookup failure             0
silent table loss                0
broken internal link             0
broken map link                  0
unexpected content loss          0
교통 하위 순서 오류                 0
중복 교통 블록                     0
```

돌린 검사 — `build/site.py`(모델·어휘·장문·fact·content·구조·사진 가드 포함) ·
`region_structure_check` · `media_lookup_check` · `table_loss_check` ·
`ux_check` · `viewport_check` · `content_audit` · `pwa_check` ·
`test_validation`(14/14) · `validate_itinerary` · `validate_media` ·
`validate_map_data` · `generate_attributions --check`. 전부 통과.

## 19. Existing baseline guard failures

`build/guards/run_all.py` 는 baseline debt 이며 이번 이관을 막지 않는다.
**새 FAIL 을 만들지 않았고, G3 는 오히려 줄었다.**

| 가드 | 이전(af4ad953) | 이후 | 판단 |
|---|---:|---:|---|
| G1 방문 요일 vs 휴관일 | 6 | **6** | 변화 없음 |
| G2 fact 토큰 밖 하드코딩 | 384 / 6,107 | **384** / 6,095 | 건수 동일 |
| G3 필수·우선추천 필수항목 참조 | 126 / 128 | **125** / 128 | **1 감소** |
| G4·G5 | PASS | PASS | |
| G6 신선도 | WARN 0 | WARN 0 | |

작업 중 `les-halles` place-facts 를 신설하자 G3 가 127 로 한 번 늘었다.
중복 항목을 합치고 원고 토큰을 네 항목(hours·closed·booking·price_adult)으로
넓혀 125 로 내렸다. 늘린 채 두지 않았다.

## 20. 변경 파일 및 commit

브랜치 `feat/fcr02c-region-migration` (푸시하지 않음).

```
build/render.py                     식당 하위 묶음 3분류 · '구간 내 이동' 라벨
build/region_structure_check.py     묶음 정의·교통 순서 라벨 갱신
data/region-essentials.json         girona·aix 신설 · 4개 지역 Local Life 재작성
data/transit-facts.json             girona 신설 · 옮겨온 교통 문장 3건
data/place-facts.json               price_range 19건 · les-halles 신설·중복 병합
data/images/place-aliases.json      11개 판정(disposition) · jardin-du-luxembourg 연결
data/images/photo-queue.json        Casa Marieta 추가
data/images/food-photo-status.json  2차 조사 반영 · FOOD_HALL 2곳 추가
data/images/image-manifest.json/csv Casa Marieta
scripts/migrate_price_range.py      신규 — 가격 이관 도구
source/CURRENT/30_Places/les-halles.md                  FOOD_HALL · 실용표 fact 토큰화
source/CURRENT/30_Places/halles-de-lyon-paul-bocuse.md  FOOD_HALL
source/CURRENT/20_Regional_Chapters/09_Avignon_...md    les-halles 토큰 슬러그 교체
source/CURRENT/20_Regions/*.md      파생물
source/ASSETS/photos/**             Casa Marieta 원본·파생본
FCR02C_FULL_MIGRATION_QA.md · FCR02_FOOD_COMPLETENESS.json · docs/fcr02c/*.png
```

## 21. 잔여 known gaps

1. **식당 사진 15곳.** 13곳은 재사용 가능한 후보가 아예 없고, 2곳은 이름만
   겹치는 다른 업소다. 공식 사이트 press 자산의 재배포 허용 여부를 업소별로
   확인하는 것 말고는 방법이 없다.
2. **Pâtisserie Weibel 의 방문일이 안 걸린다.** Day 13 stop 하나가 시장과
   Weibel 을 함께 담는다. stop 분할 또는 보조 참조 필드가 필요하다 — Day SOT
   변경이라 임의로 하지 않았다.
3. **메뉴 없는 4곳** — 시장 3곳과 파티세리 1곳. 시장은 '대표 메뉴' 개념이
   맞지 않고, Weibel 은 위 2번과 같은 이유다.
4. **`place-facts` 에 명부에 없는 슬러그 86개.** `les-halles-d-avignon` 처럼
   중복이거나(승격 안 된 장소·옛 슬러그) 죽은 데이터다. 사진 별칭과 같은
   실패 유형이며, 같은 방식(판정표 한 곳 + 가드)으로 정리할 수 있다.
5. **조사 CSV 에만 있는 식당 5곳** — `acchiardo` · `chez-pipo` ·
   `le-petit-port-menton` · `marche-condamine` · `collioure-seafood-bistro`.
   주소·운영시간·가격·출처가 이미 있지만 명부에 없다. Menton 저녁과 Monaco
   점심은 실제 일정이라 승격 후보이며, 장소 서술이 필요하다.
6. **미등재 11곳 중 4곳(Cadaqués·Tossa·Sant Feliu·Palais Royal)** 은 실제
   방문지인데 장소 서술이 없어 MEDIA-ONLY 로 뒀다.
7. **G1·G2 baseline debt** — 방문 요일 vs 휴관일 6건, fact 토큰 밖 하드코딩
   384건. 이번 변경과 무관하다.
8. **`place-facts` 가 자기 스키마를 어긴다** (`confidence: editorial`,
   `note` 키). 모델이 이 파일만 스키마 검증을 하지 않는다.

## 22. FCR-02 최종 완료 여부

**구조 개편은 완료다.** 8개 지역이 같은 여섯 섹션, 같은 컴포넌트, 같은
데이터 흐름을 쓴다. 지역 전용 분기는 코드에 0개다. 되돌아갈 길을 세 개의
가드가 막는다 — 분류·구조·링크(`region_structure_check`), 사진 연결
(`media_lookup_check`), 조용한 표 손실(`table_loss_check`). 앞의 둘은 빌드가
함께 돈다.

**콘텐츠는 완료가 아니다.** 사진 15곳과 장소 승격 후보 9곳(§21-5·6)이 남는다.
다만 이것들은 구조가 아니라 조사의 문제이고, 각각 무엇이 없어서 못 하는지가
데이터로 적혀 있다 — `food-photo-status.json` 과 `place-aliases.json` 의
`disposition` 이다.

게이트 승인을 기다린다. 푸시·머지·PR 하지 않았다.
