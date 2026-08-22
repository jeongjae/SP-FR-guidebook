# FCR02B_STABILIZATION_QA — 7개 지역 이관 전 안정화

기준 커밋 `5f673080` (Barcelona 파일럿 게이트 승인본) 위에서 작업했다.
**7개 지역의 실제 이관은 시작하지 않았다.**

---

## Overall Status

**PASS.** 종료 조건 일곱 가지를 모두 만족한다.

| 종료 조건 | 결과 |
|---|---|
| Aix SOT conflict = resolved | 원고를 확정 숙소로 갱신, 폐기 후보 제거 |
| Nice source deficiency = resolved | 구역별 이해 확장 + `region-essentials` 신설 |
| image exists but lookup fails = 0 | 미매핑 0 · 조용히 사라진 사진 0 |
| silent stacked-table loss = 0 | 원고 전수 검사, 수정 후 잔여 0 |
| Barcelona regression = 0 | 카드·Day 링크·접이식 동일, 의도한 변경만 |
| shared Region template = ready | 지역 전용 분기 0 |
| shared validation = ready | 세 검사 모두 8개 지역 전수 |

---

## 1. Aix SOT reconciliation

**정본은 daily-card 다.** DEC-039(2026-08-15) '프로방스 3거점 현지 결정' 방침은
2026-08-19 실제 예약으로 끝났다 — `docs/D5_CONFIRMED_BOOKING_REPLAN.md` 가
그날 확정 3건(Sagrada · Aix 숙소 · Paris 숙소)을 기록한다. 원고만 옛 방침에
남아 있었다.

일치시킨 다섯 곳:

| 층 | 상태 |
|---|---|
| daily-card (day-12) | `Les Toits de Méjanes (Airbnb)` · confirmed · 주소·체크인/아웃 |
| 챕터 원고 | **갱신** — '확정 숙소' 표 신설, 현지 결정 방침 문단 제거 |
| 지역 페이지 | 확정 배지 + 주소 (SOT 에서 자동) |
| 숙소 데이터 | 변경 없음 — 원래 맞았다 |
| 방문일 관계 | 변경 없음 — Day 12 체크인 16:45 / Day 16 체크아웃 08:00 |

원고에서 뺀 것 — 현지 결정 방침 블록, 후보 3곳(Adagio Centre · Odalys
Les Floridianes · Maison Dauphine, **전화번호·참고요금 포함**), 숙소 선택
알고리즘, 폐기 호텔 공식사이트 링크 7개.

**추정하지 않은 것 하나.** 이 Airbnb 의 주차 가능 여부는 어느 SOT 에도 없다.
확정으로 쓰지 않고 `{{badge:field-recheck}}` 로 두고, 공영주차(Rotonde ·
Mignet)를 예비안으로 남겼다.

## 2. Nice source-content repair

**앞선 보고를 정정한다.** Nice 의 `구역별 이해`·`도착·출발` 절이 "사실상
비어 있다"고 썼는데, 줄 수(각 6줄)로만 잰 판단이었다. 실제로는 필요한 사실이
다 있었다 — 확정 숙소, 트램 2호선, TER 소요시간, 렌터카 인수 시각. 없던 것은
**생활권 이해의 깊이**와 **구조화된 데이터**였다.

채운 것:

- 챕터 `구역별 이해와 숙소 생활권` — 확정 숙소 블록을 표제 아래로 올리고,
  이 일정이 실제로 쓰는 6개 구역(숙소권 · Vieux Nice · Cours Saleya ·
  Colline du Château · Promenade·Port Lympia · Nice-Ville)의 역할과 성격을
  표로 정리. 근거는 Day 7–12 카드와 장소 명부뿐이다 — 새 관광 서술을
  지어내지 않았다.
- `data/region-essentials.json` 에 `nice` 신설 — staySummary · lifeEssentials
  4항목 · arrivalStrategy · departureStrategy · lateReturnRule.
  이것이 지역 페이지의 숙소·생활권·도착/출발 블록을 채운다.

일정 충돌 검증 — `validate_itinerary.py` 통과(43일·42박), Cours Saleya 월요일
전환은 place-facts 의 공식 출처(2026-08-17 검증)와 일치, Day 8 은 토요일이라
영향 없음.

## 3. Image slug mismatch — 근본 원인

**정규화 버그가 아니다.** 카탈로그의 `placeId` 는 사진 프로그램이 명부보다
먼저 쓰던 **주제 키**다 — `socca`(요리) · `monaco-ville`(장소의 일부) ·
`versailles-gardens`(장소의 구역) · `aix-en-provence`(도시). 명부는 그 뒤에
다른 이름 공간으로 자랐다. 두 이름은 문자열이 아니라 **의미**가 다르므로
어떤 정규화 규칙으로도 이어지지 않는다. `mercat-de-la-concepcio` 하나만
철자 근접이었고, 그래서 하나만 고쳐졌던 것이다.

고친 방식 — **한 곳의 판정표**. `data/images/place-aliases.json` 이
placeId 마다 판정 하나를 갖는다.

```
place        명부의 이 슬러그를 찍은 사진이다   (근거를 why 에 적는다)
dish         요리 사진 — 장소가 아니다
unregistered 실재하지만 명부에 없다 — 승격 후보
```

잇는 코드도 한 곳으로 모았다. 예전에는 `model.load_images` 와
`render.load_image_index` 두 곳에 같은 로직이 있었다 — 별칭을 한쪽만 고치면
다른 쪽이 조용히 옛 규칙으로 돈다. 이제 렌더러는 모델의 결과를 그대로 쓴다.

## 4. Image mismatch fixed count

| 판정 | 건수 | 처리 |
|---|---:|---|
| place | 22 | 장소·지역에 연결. 대표 사진이 이미 있으면 **장소 페이지 갤러리**로 나온다 |
| dish | 6 | 지역의 식당·카페 섹션에 요리 사진 띠로 나온다 |
| unregistered | 11 | 장소 승격이 있어야 화면에 올라간다 — 선언된 잔여분 |
| unmapped | **0** | 별칭표에 없는 placeId 는 빌드를 세운다 |

추가로 히어로로 쓰이지 않아 조용히 사라져 있던 지역 사진 2장
(`barcelona-city-aerial-01` · `luberon-valley-01`)을 개요에 실었다.

```
카탈로그 167 · 연결 156 · 배포본에 실제로 나오는 것 156
잇혔는데 안 나오는 사진 0 · 별칭표에 없는 placeId 0
```

`build/media_lookup_check.py` 가 빌드에서 함께 돈다.

## 5. Stacked-table corpus audit

`build/table_loss_check.py` — 원고·파생물·장소·명부 전수.

```
붙어 있는 표 덩어리   10
수정 전이면 잃었을 열  11
수정 후 남은 병합      0
```

| 파일 | 잃었을 열 |
|---|---:|
| 04_Barcelona_Sitges_v2.0.md (+ 파생 barcelona.md) | 3 |
| 05_Girona_Collioure_Emporda_v2.1.md (+ 파생 girona.md) | 2 |
| 07_Aix_en_Provence_v2.0.md | 1 |
| 11_Paris_Long_Stay_v2.0.md (+ 파생 paris.md) | 0 (열 수가 같아 손실 없음) |

Girona 에서 되살아난 것은 `추천 체류 리듬` 의 **날짜별 테마 표 전체**
(날짜·요일·테마·핵심 동선 4열)다. Barcelona 와 같은 유형의 손실이 다른
지역에도 있었다는 뜻이다. `ux_check` 의 표 검사는 여전히 통과한다 — 열이
일정하게 잘리기 때문에 그 검사로는 잡히지 않는다.

## 6. Market classification 확인

**SOT 를 바꾸지 않았다.** `meal_role: MARKET` · `food_kind: MARKET` 은 그대로고,
시장은 계속 식당·카페 영역의 엔티티다. 화면에서만 하위 묶음으로 나눴다.

```
Restaurants & Cafés
├─ 식당        restaurant · wine-bar
├─ 카페·빵집    cafe · bakery
└─ 시장·푸드홀  market · food-hall
```

묶음이 하나뿐이면 제목을 달지 않는다. 구조 검사가 **묶음과 엔티티의 일치**를
잠근다 (`식당 하위 묶음 오분류 = 0`).

## 7. Restaurant/Café photo gap status

차단 사유로 다루지 않았다. 대신 상태를 네 갈래로 기록한다 —
`data/images/food-photo-status.json` (2026-08-22 Commons 검색 API 전수 22곳,
결과는 사람이 하나씩 읽어 판정).

| 상태 | 곳 | 뜻 |
|---|---:|---|
| verified | **6** | 사진 설명이 그 업소를 가리킨다 |
| missing-no-candidate | 7 | 재사용 가능한 후보가 아예 없다 |
| missing-wrong-entity-risk | 9 | 이름이 겹치는 결과가 있으나 **전부 다른 대상**이다 |

이번에 확인해 넣은 5곳 — Mercat del Lleó(Girona) · Daniel et Denise(Lyon) ·
Bouillon Chartier Montparnasse · Café du Commerce · Marché Convention(Paris).
사진 없는 식당이 21곳에서 **16곳**으로 줄었다.

**지점까지 대조했다.** 리옹의 Daniel & Denise 는 같은 이름이 여러 곳이다.
파일명이 `Lyon 3e - Rue de Créqui` 인 것만 썼다 — 장소 정본의 주소
(156 Rue de Créqui, 69003)와 같은 지점이다. Café du Commerce 도 사진 설명의
`51 Rue du Commerce, 75015` 가 정본 주소와 일치한다.

넣지 않은 것 — Bar Cañete(검색 결과가 칠레 인구 그래프), La Zorra(하바나
재즈클럽·세고비아 등산로), Bodega Joan(1887년 바르셀로나 상점 사진),
Chez Gilbert(사이공 지점). 이름이 겹칠 뿐 다른 대상이다.

## 8. Template generalization

지역 전용 조건은 코드에 **0개**다. 확인 방법 — `build/render.py` ·
`build/model.py` · `build/region_structure_check.py` 에서 지역 슬러그 문자열
검색. 남은 것은 `model.load_registry` 의 챕터번호→지역 매핑 하나뿐이고,
그것은 조건이 아니라 명부 파서의 인덱스다.

이번에 데이터로 내린 것:

| 코드에 있던 것 | 어디로 |
|---|---|
| `link_food_text` 의 slug 분기 30여 개 | `data/place-name-aliases.json` |
| 사진 placeId 판정 | `data/images/place-aliases.json` |
| 사진 추가 대상 | `data/images/photo-queue.json` |
| 사진 상태 판정 | `data/images/food-photo-status.json` |
| `GENERIC_FOOD_NOTES` 두 벌 | 렌더러 것 하나를 감사가 import |

흐름은 이제 이렇다.

```
정본 데이터 (명부 · daily-card · place-facts · region-essentials · 별칭표)
      ↓
공유 모델 (Place.entity_type · Region.must_visit/recommended/food_places)
      ↓
공유 템플릿 (build_region 하나 · food_card · attraction_card · visit_badges)
      ↓
지역별 콘텐츠
```

## 9. Shared schema / component 변경

| 파일 | 무엇 |
|---|---|
| `build/model.py` | `load_images(known)` 가 별칭을 통과시켜 by_place·extras·heroes·dishes·unregistered·unmapped 를 돌려준다 · `IMAGE_ALIASES` |
| `build/render.py` | 사진 색인은 모델 결과를 그대로 사용 · 장소 페이지 '다른 사진' 갤러리 · 지역 요리 사진 띠 · 지역 사진 개요 노출 · 식당/카페/시장 하위 묶음 · `load_name_aliases` |
| `build/region_structure_check.py` | 하위 묶음 일치 · 교통 하위 순서 · 지도 링크 · 지역 준비 매트릭스 · 사진 상태 |
| `build/media_lookup_check.py` | 신규 — 사진 연결 가드 |
| `build/table_loss_check.py` | 신규 — 연속 표 병합 전수 감사 |
| `build/site.py` | 두 가드를 빌드에 연결 |
| `build/assets/style.css` | `.gallery-item` · `.gallery-shot` |
| `scripts/add_commons_photo.py` | 신규 — 대기열 기반 사진 추가 (카탈로그 전체 재인코딩 없이) |
| `data/region-essentials.json` | `nice` 신설 |

## 10. Validation generalization

세 검사 모두 8개 지역 전수로 돈다. Barcelona 에서만 통과하는 것은 없다.

```
python3 build/region_structure_check.py
  분류 · 섹션 6개와 순서 · 식당 하위 묶음 · 교통 하위 순서 · 중복 교통 블록
  · 방문일 참조 · 지도 링크 · 내부 링크 · 식당 완결성 · 지역 준비 매트릭스
python3 build/media_lookup_check.py
  별칭 미매핑 · 잇혔는데 안 나오는 사진
python3 build/table_loss_check.py
  연속 표 병합과 열 손실 (원고 전 코퍼스)
```

현재 값 — 지역 8 · 볼거리 카드 109 · 식당·카페 카드 22 ·
볼거리 안의 식당 0 · 식당 안의 관광지 0 · 식당 하위 묶음 오분류 0 ·
되살아난 옛 섹션 0 · 잘못된 Day 참조 0 · 교통 하위 순서 오류 0 ·
중복 교통 블록 0 · 검색어 없는 지도 링크 0 · 끊어진 내부 링크 0.

**지역 데이터 준비 매트릭스** (구조가 아니라 콘텐츠다 — 빌드를 세우지 않는다)

main 을 브랜치로 들여오면서 값이 바뀌었다. 그사이 머지된 PR #197~#202 가
luberon·avignon·lyon·paris 의 essentials 를 채웠다. **남은 것은 두 지역뿐이다.**

| 지역 | staySummary | localLife | arrival | departure | publicTransport | references |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| barcelona | O | O | O | O | O | O |
| girona | · | · | · | · | · | O |
| nice | O | O | O | O | O | O |
| aix | · | · | · | · | O | O |
| luberon | O | O | O | O | O | O |
| avignon | O | O | O | O | O | O |
| lyon | O | O | O | O | O | O |
| paris | O | O | O | O | O | O |

`neighborhoods` · `foodCulture` · `transportDeep`(원고 승격 층)은 8개 지역 전부 O.

## 11. Barcelona regression test

게이트 커밋을 별도 워크트리에 체크아웃해 빌드하고 페이지 단위로 비교했다.

| 항목 | 결과 |
|---|---|
| 섹션 구성 | 하위 묶음 제목 2개(`식당` · `시장·푸드홀`) 추가 — 의도한 변경 |
| 장소 카드 | 12개 **동일** (순서까지) |
| Day 링크 | Day 1–4 **동일** |
| 접이식 블록 | 10개 **동일** |
| 본문 글자수 | 18,369 → 18,486 (시장 사진 설명·저작자 표시) |
| 페이지 수 | 369 → 369, 사라진 페이지 0 |

사이트 전체 문장 대조 — 8,132문장 중 사라진 것 7건. 전수 확인 결과
Aix 후보 삭제 2건(의도)과 Nice 재작성 5건(같은 사실을 다시 씀)이었다.
Nice 의 €809.54 · 12 Rue Verdi · 체크인 18:00 · 주방과 세탁기 · 호스트 표기는
모두 새 문장에 살아 있다. **실질 손실 0.**

## 12. Changed files

```
build/model.py  build/render.py  build/site.py  build/region_audit.py
build/region_structure_check.py  build/assets/style.css
build/media_lookup_check.py (신규)  build/table_loss_check.py (신규)
scripts/add_commons_photo.py (신규)
data/images/place-aliases.json (신규)  data/images/photo-queue.json (신규)
data/images/food-photo-status.json (신규)
data/images/image-manifest.json  data/images/image-manifest.csv
data/place-name-aliases.json (신규)  data/region-essentials.json
source/ASSETS/photos/originals/*.jpg (신규 5)
source/ASSETS/photos/processed/**/*.webp (신규 10)
source/ASSETS/photos/metadata/image-manifest.json
source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md
source/CURRENT/20_Regional_Chapters/07_Aix_en_Provence_v2.0.md
source/CURRENT/20_Regions/*.md (파생물)
REGION_CONTENT_AUDIT.{md,json}  FCR02_FOOD_COMPLETENESS.json
FCR02B_STABILIZATION_QA.md  docs/fcr02/*.png
```

## 13. Remaining risks

1. **`region-essentials` 가 없는 곳은 girona·aix 둘이다.** (main 머지 후 값.
   luberon·avignon·lyon·paris 는 PR #197~#202 가 채웠다.) 두 지역의 숙소
   요약·생활권·도착/출발 블록이 그만큼 얇다.
2. **명부 미등재 장소 11곳의 사진이 대기 중이다.** Cadaqués · Tossa de Mar ·
   Sant Feliu de Guíxols · 팡테옹 · 뤽상부르 공원 · 몽주 시장 · 팔레 루아얄 ·
   아케이드 · 앙팡 루주 시장 · 생마르탱 운하 · 센강변. 전부 일정에 실제로
   있는 곳이라 장소 승격 후보이지만, 승격에는 검증된 서술이 필요하다.
3. **식당 사진 16곳은 여전히 없다.** 9곳은 '넣으면 안 되는' 상태(다른 업소
   결과만 있음)라 시간이 해결하지 않는다. 공식 사이트 press 자산의 재배포
   허용 여부를 업소별로 확인해야 한다.
4. **가격 사실이 Barcelona 5곳뿐이다.** 나머지 17곳은 지역별 조사 CSV 에
   `price_range`·`source_url`·`verified_at` 이 이미 있다 — 옮기기만 하면 된다.
5. **`data/place-facts.json` 이 자기 스키마를 어긴다** (`confidence: editorial`
   가 enum 밖, `note` 키 비허용). 모델이 이 파일만 스키마 검증을 하지 않아
   드러나지 않는다. 기존 상태이며 손대지 않았다.
6. **`guards/run_all.py` 의 G1·G2·G3 는 계속 FAIL.** fact-infra 프로그램의
   미착수 잔여분이며 이번 변경과 무관하다.
7. **Aix Airbnb 주차 미확인.** 확정으로 쓰지 않았고 예비안을 남겼지만,
   출발 전 호스트에게 확인할 항목이다.

## 14. Recommendation for 7-region rollout

**순서** — Girona → Aix 가 먼저다. `region-essentials` 가 없는 두 곳이라
이관 4단계를 다 밟아야 한다. 나머지 다섯(Nice·Luberon·Avignon·Lyon·Paris)은
essentials 가 이미 있으므로 가격 사실 이관·사진·검수만 남는다.

**지역 하나당 할 일은 넷이고 순서가 있다.**

1. `data/region-essentials.json` 에 그 지역을 추가한다 (staySummary ·
   lifeEssentials · arrival · departure · lateReturn). 근거는 daily-card 다.
   → 숙소·생활권·도착/출발 블록이 채워진다.
2. 지역 조사 CSV 의 `price_range` 를 `data/place-facts.json` 으로 옮긴다.
   → 식당 카드의 가격 칸이 채워진다.
3. `data/images/photo-queue.json` 에 **설명으로 신원이 확인된** 사진만 넣고
   `scripts/add_commons_photo.py` 를 돌린다. 시장·푸드홀·랜드마크가 성공률이
   높다. 개별 식당은 기대하지 않는다.
4. `region_structure_check.py` · `media_lookup_check.py` · `table_loss_check.py`
   가 0 을 유지하는지 본다. 그다음 CI 순서 그대로 게이트를 돌린다.

**먼저 결정해야 할 것 둘.**

- `les-halles`(Avignon) · `halles-de-lyon-paul-bocuse`(Lyon) 에 `food_kind:
  FOOD_HALL` 을 줄 것인가. 주면 두 곳이 볼거리에서 시장·푸드홀 묶음으로
  옮겨간다. Mercat de la Concepció 와 같은 성격이라 일관성으로는 줘야 한다.
- 명부 미등재 11곳 중 승격할 곳을 고를 것인가. 사진이 이미 있으므로
  승격하면 바로 화면에 올라간다. 다만 장소 페이지에는 검증된 서술이 필요하다.

**하지 말 것.** 지역 전용 분기를 코드에 넣는 것. 지금 0 이고, 한 번 열리면
지역마다 다른 페이지가 된다 — FCR-02 가 되돌린 상태가 정확히 그것이었다.
