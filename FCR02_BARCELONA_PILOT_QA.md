# FCR02_BARCELONA_PILOT_QA — Barcelona 파일럿 게이트 보고

작성 2026-08-22 · 브랜치 `feat/mp03-photo-recovery` · 게이트 대상: Barcelona
(구조 변경 자체는 8개 지역 전부에 적용됐다 — 콘텐츠 보강만 Barcelona 에 했다)

---

## Overall Status

**PASS — 승인 요청.** 구조·분류·검증은 8개 지역 전부 통과했고, 콘텐츠
보강은 Barcelona 만 했다. 지시대로 나머지 7개 지역의 콘텐츠 이관은 하지
않고 여기서 멈춘다.

세 가지를 먼저 보고한다.

1. **원고에만 있고 배포본에 없던 덩어리를 찾았다.** `카페 5곳`·
   `슈퍼마켓 사용 원칙`·`저배출구역(ZBE)`·`시체스 주차` 를 개편 전 배포본에서
   찾으면 한 건도 나오지 않았다. 지역 페이지가 챕터의 여섯 층만 쓰고 있었기
   때문이다. 다섯 층을 더 승격시켜 새 섹션의 내용으로 썼다.
2. **표 세 개가 하나로 합쳐지며 열이 잘리는 콘텐츠 손실을 고쳤다.**
   Barcelona `한눈에 보기` 의 `확정 일정`·`예상 체류`·`핵심 이유` 세 열이
   화면에서 통째로 사라져 있었다. 열이 일정하게 잘려서 표 검사도 못 잡았다.
3. **저장소에 있는데 화면에 영영 안 나오는 사진 40장을 찾았다.** 슬러그가
   명부와 어긋나 있다. Barcelona 의 `mercat-de-la-concepcio` 하나를 고쳐
   Mercat de la Concepció 사진이 처음으로 화면에 나온다. 나머지 39장은
   `REGION_CONTENT_AUDIT.md` 에 목록으로 남겼다.

---

## 1. Audit 결과

`python3 build/region_audit.py` — 개편 전 렌더 규칙 기준, 인벤토리 412행.

| 항목 | 값 |
|---|---:|
| 지역 | 8 |
| 인벤토리 항목 | 412 |
| 장소 섹션에 있던 식당·카페·시장 | **22** |
| 먹거리 섹션에 있던 관광지 | **17** |
| 먹거리 섹션의 업소 아닌 식사 슬롯 | 7 |
| 제거 대상 일정 섹션 | 8 |
| 제거 대상 한눈에 보기 섹션 | 8 |
| 제거 대상 꼬리말 블록 (역할·리듬) | 14 |
| Day 에서 복사해 오던 교통 문자열 | 86 |
| 지역을 넘나든 식당 카드 | 5 |
| 어느 장소도 가리키지 않는 사진 | 39 |

산출물 — `REGION_CONTENT_AUDIT.json` · `REGION_CONTENT_AUDIT.md` ·
`REGION_RECLASSIFICATION_MAP.json`

## 2. 오분류 발견 건수

**39건** (식당→볼거리 22 + 관광지→먹거리 17).

판정은 제목이 아니라 엔티티로 했다. `Bar Cañete 점심`·`Bodega Joan 저녁`은
제목에 끼니가 있어도 실제 업소라 식당이고, `구시가지 점심 — 니스와즈 요리`는
제목이 같은 모양이어도 `vieux-nice`(관광지)를 가리키는 하루의 식사 슬롯이다.

## 3. Attraction → Food 이동

22곳. Barcelona 5곳(`bodega-joan` · `la-paradeta-sagrada-familia` ·
`bar-canete` · `mercat-concepcio` · `la-zorra`) 포함. 전체 목록은
`REGION_RECLASSIFICATION_MAP.json` 의 `attractionToFood`.

## 4. Food → Attraction 이동

**0건.** 먹거리 섹션에 있던 관광지 17건은 옮길 것이 아니라 **지역 페이지에
둘 것이 아니었다.** 업소가 아니라 `(날짜, 시각, 장소, 메모)` 의 조합인
식사 슬롯이고, 그 정본은 이미 Day 페이지 시간표다. 해당 관광지 자체는
볼거리 섹션에 카드로 있다 — 잃은 정보가 없다.
(`foodToDayOrAttraction` 24건 = 관광지 17 + 업소 없는 슬롯 7)

## 5. Schedule 제거 및 정보 이전

일정 섹션(Day 카드 43장)을 없앴다. 고유 정보는 없었다 — 카드가 들고 있던
날짜·도시·제목·피로도는 전부 Day 페이지의 것을 복사한 것이다.

**길은 끊지 않았다.**
- 개요 맨 위 날짜 칩이 그 지역의 모든 Day 로 간다 (가로 스크롤, 44pt 타깃)
- 카드의 방문일 배지가 그 장소를 실제로 들르는 Day 로 간다
- 교통의 도착·출발 카드가 첫날·마지막 날로 간다

날짜 문자열은 템플릿에 없다. `render.place_visits()` 가 daily-card 의 stop
에서 계산하므로 **일정이 바뀌면 배지도 바뀐다.** 잘못된 Day 참조 0건.

## 6. At-a-glance 제거

섹션으로는 없앴고 **개요 안 접이식으로 흡수**했다. 지우지 않은 이유는 그
표에만 있는 값이 있기 때문이다 — 예상 체류시간, 확정 일정 시각, 추천 이유.
그 세 열이 렌더 버그로 이미 사라져 있었고(§Overall 2) 이번에 되살아났다.

## 7. Restaurant / Café completeness

`FCR02_FOOD_COMPLETENESS.json` · 전체 22곳.

| 항목 | 빠진 곳 |
|---|---:|
| 소개 | 0 |
| 공식 홈페이지 | 0 |
| 지도 | 0 |
| 추천 메뉴 | 4 |
| 가격(사실 레코드) | 17 |
| 방문일 연결 | 3 |
| **사진** | **21** |

Barcelona 5곳은 사진 1곳을 빼고 전부 채웠다.

| 장소 | 사진 | 소개 | 공홈 | 지도 | 메뉴 | 가격 | 확인일 | 방문일 |
|---|:-:|:-:|:-:|:-:|:-:|---|---|---|
| Bodega Joan | — | O | O | O | O | €25-€35/인 | 2026-08-21 | Day 2 저녁 |
| La Paradeta Sagrada Família | — | O | O | O | O | €18-€28/인 | 2026-08-21 | Day 2 점심 |
| Bar Cañete | — | O | O | O | O | €30-€45/인 | 2026-08-21 | Day 3 점심 |
| Mercat de la Concepció | **O** | O | O | O | — | €5-€15 | 2026-08-21 | Day 3 아침 |
| La Zorra | — | O | O | O | O | €30-€45/인 | 2026-08-21 | Day 4 점심 |

가격은 `FCR02_RESTAURANT_CAFE_MARKET_RESEARCH.csv` 의 기록을
`data/place-facts.json` 의 `price_range` 사실로 옮긴 것이다. 출처는 각 업소
공식 사이트, 확인일 2026-08-21 — **이번 세션에서 새로 확인한 값이 아니라
FCR-02 조사 기록의 이관**이다. 추정치는 넣지 않았다. 가격 사실이 없는
17곳은 카드에 `미확인` 배지가 나온다. 빈칸은 '싸다'로 읽히기 때문이다.

**메뉴별 사진·설명·가격은 넣지 않았다.** 요리 단위 사진을 재사용 가능한
라이선스로 구할 수 없고, 요리별 가격은 Bodega Joan 한 곳에만 원고에 있다
(카넬로니 약 €10.50 등). 그 값은 장소 페이지 `더 깊이` 에 그대로 있다.
지어내지 않았다.

## 8. Accommodation / Local Life 변경

`숙박·생활` 을 두 섹션으로 갈랐다.

- **숙소** — 확정 숙소 카드(Occidental Barcelona 1929, 확정 배지) +
  `staySummary` + 접이식 `묵을 만한 동네`(원고의 6개 생활권 비교) +
  접이식 `숙소 예산과 확인 기준`
- **생활권** — `lifeEssentials` 3항목 + 늦은 귀가 규칙

**폐기된 숙소 후보 6곳(Hotel SERHS Carlit 외)은 화면에서 뺐다.** 확정
숙소가 있는 6개 지역에 같은 규칙이 걸린다. 원고에는 그대로 남는다.

Barcelona `lifeEssentials` 는 "약국·생필품점은 특정 상호를 고정하지 않는다"
고 명시한다. 슈퍼·약국·체육시설을 새로 지어내지 않았다 — 검증 안 된 사실을
쓰지 않는다는 기준을 그대로 지켰다.

## 9. Transport deduplication

`도착과 출발 → 도시 교통 → 공식 자료와 재확인` 하나의 순서로 합쳤다.
중복 교통 블록 0건.

- Day 에서 복사해 오던 자유문자열 86줄을 뺐다 (Day 의 `이동` 접이식이 정본)
- Aerobús A1 · Hola Barcelona 48h 는 도시 교통의 상품 카드 하나로 모였다
- 렌터카 인수(Sants)·ZBE·시체스 주차는 접이식 `지역 교통 심화` 로 처음
  화면에 나왔다
- Metro 노선도 · Telefèric de Montjuïc 지도와 공식 출처 링크는 References 로

## 10. Overview 통합

`여행 전체에서의 역할` · `추천 체류 리듬` 꼬리말을 개요 안 접이식으로
올렸다. 우천 전환 경고도 개요로 옮겼다. 페이지 하단에는 이제 교통
References 가 마지막이다.

## 11. Schema / Template 변경

| 파일 | 무엇 |
|---|---|
| `build/model.py` | `Place.entity_type` · `Region.attractions/must_visit/recommended/food_places/has_confirmed_stay` · 승격 층 5개 매핑 |
| `build/promote_regions.py` | 심화 층 5개 승격(앵커·경계 방식) · 폐기 숙소 후보 필터 |
| `build/render.py` | `build_region` 재작성 · `food_card`/`attraction_card`/`visit_badges`/`place_visits` · **`split_stacked_tables` (표 병합 손실 수정)** |
| `build/region_audit.py` | 신규 — 이관 기준선 |
| `build/region_structure_check.py` | 신규 — 구조·분류 가드 + 완결성 리포트 |
| `build/site.py` | 구조 가드를 빌드에 연결 |
| `build/assets/style.css` | `.badge-day` · `.day-chips` |
| `data/place-facts.json` | Barcelona 식당 5곳 `price_range` |
| `data/images/image-manifest.json` | `mercat-de-la-concepcio` → `mercat-concepcio` |
| `source/CURRENT/20_Regions/*.md` | 파생물 — 빌드가 다시 뽑는다 |

`build/content_schema.json` 은 **바꾸지 않았다.** 원고 h2 구성·순서와
배포 토큰(`Editor's Verdict`·`꼭 경험할 세 장면`·`한눈에 보기`) 요구가
그대로 지켜지기 때문이다 — 한눈에 보기를 지우지 않고 접었으므로 통과한다.

## 12. Validation 결과

```
python3 build/site.py                     통과 (모델 검증 · 어휘 가드 · 장문 가드
                                          · fact_guard · content_guard · 구조 가드)
python3 build/region_structure_check.py   통과
python3 build/ux_check.py                 통과 (명암비 · 하단탭 369쪽 · 데일리 43일 · 표)
python3 build/viewport_check.py           통과 (360·390·430·768·1024·1440)
python3 build/content_audit.py            콘텐츠 손실 0
python3 build/pwa_check.py                826파일 58.6MiB · 오프라인 심층 탐색 통과
python3 build/test_validation.py          14/14 OK
python3 scripts/validate_itinerary.py     43일 · 42박 통과
python3 scripts/validate_media.py         라이선스·참조·용량 이상 없음
python3 scripts/generate_attributions.py --check   카탈로그와 일치
python3 scripts/validate_map_data.py --quiet-warnings  통과
```

구조 가드 수치 — 볼거리 카드 109 · 식당·카페 카드 22 · 볼거리 안의 식당 0 ·
식당 안의 관광지 0 · 되살아난 옛 섹션 0 · 잘못된 Day 참조 0 · 중복 교통 블록 0 ·
끊어진 내부 링크 0.

`build/guards/run_all.py` 는 **G1·G2·G3 FAIL** 이다. 이번 변경과 무관한
기존 상태다 (G3 필수항목은 hours/closed/price_adult/booking 이고 이번에 넣은
것은 price_range 라 대상이 아니다). 근거: fact-infra S0~S5 프로그램의 미착수
잔여분.

## 13. Barcelona screenshots / responsive QA

`docs/fcr02/` — `barcelona-390.png`(모바일 전체) ·
`barcelona-1280.png`(데스크톱 전체) · `barcelona-390-overview.png` ·
`barcelona-390-food.png` · `paris-390-overview.png`(칩 16개 스크롤 확인).

390px 에서 확인한 것 — 여섯 섹션 순서대로, 날짜 칩 가로 스크롤(세로로
쌓이지 않는다), 식당 카드의 사진·배지·메뉴·가격·운영시간·예약·버튼이 한 카드
안에서 읽힌다, 접이식 5개가 개요를 짧게 유지한다. 가로 오버플로 0.

## 14. Broken links

지역 8쪽의 내부 링크 전수 — 끊어진 링크 0건. 외부 링크는 형식만 본다
(`generate_attributions.py --check` 통과, `validate_media.py` 통과).
지도 링크는 좌표가 아니라 **이름 검색어**로 연다.

## 15. Content-loss check

- `build/content_audit.py` — 승격된 장소 장문 1,142문단 전수, 손실 0
- 편집 층 문구 대조 1,638건 — 미검출 73건을 전수 확인한 결과 전부
  `{{badge:a|b}}` 토큰이 검사기의 파이프 분리로 잘린 것과 옛 주소 재작성
  1건이었다. **실제 손실 0**
- 표 병합으로 이미 사라져 있던 열 3개를 **되살렸다** (순증)

## 16. 변경 파일

```
build/model.py  build/promote_regions.py  build/render.py  build/site.py
build/region_audit.py (신규)  build/region_structure_check.py (신규)
build/assets/style.css
data/place-facts.json  data/images/image-manifest.json  data/images/image-manifest.csv
source/ASSETS/photos/metadata/image-manifest.json
source/CURRENT/20_Regions/*.md (8개 · 파생물)
REGION_CONTENT_AUDIT.{md,json}  REGION_RECLASSIFICATION_MAP.json
REGION_STRUCTURE_MIGRATION.md  FCR02_BARCELONA_PILOT_QA.md
FCR02_FOOD_COMPLETENESS.json  docs/fcr02/*.png
```

## 17. 미해결 항목

1. **식당·카페 사진 21곳.** Commons 에 실제로 있는 것은 시장·푸드홀 정도다.
   `Bar Cañete`·`La Zorra` 는 검색 결과가 전부 다른 업소였다 — 이름이 비슷한
   사진을 붙이면 현장에서 엉뚱한 곳을 찾게 되므로 붙이지 않았다. 공식
   사이트의 press/media 자산은 업소별 재배포 허용 여부를 개별 확인해야 한다.
2. **화면에 안 나오는 사진 39장.** 슬러그가 명부와 어긋난다. 요리 사진
   (`socca`·`xuixo`·`crema-catalana` 등)은 장소가 아니라 정상이고, 나머지는
   오타이거나 승격되지 않은 장소다. 전 지역 대상이라 이번 범위 밖.
3. **`data/place-facts.json` 에 슬러그 중복.** `mercat-concepcio` 와
   `mercat-de-la-concepcio` 가 둘 다 있고 운영시간이 서로 다르다
   (08-21 / 08-17). 명부에 없는 쪽은 읽히지 않는 죽은 데이터다.
4. **place-facts 가 자기 스키마를 어긴다.** `confidence: "editorial"` 이
   enum 밖이고 `note` 키가 허용 목록 밖이다. 모델이 이 파일만 스키마 검증을
   하지 않아 드러나지 않았다. 기존 상태이며 손대지 않았다.
5. **Aix 원고와 SOT 충돌.** 원고는 "이 구간 숙소는 사전 예약하지 않고
   현지에서 결정한다(DEC-039, 2026-08-15)" 인데 daily-card 는
   `Les Toits de Méjanes (Airbnb) · confirmed` 다. 화면은 SOT 를 따르고
   후보 목록은 뺐지만, **원고를 갱신해야 한다.**
6. **Nice 챕터의 `구역별 이해와 숙소 생활권`·`도착·출발` 절이 사실상 비어
   있다** (각 6줄). 다른 7개 지역은 70~150줄이다. Nice 지역 페이지의 숙소·
   교통 심화가 얇은 이유다.
7. `les-halles`(Avignon)·`halles-de-lyon-paul-bocuse`(Lyon) 는 시장·푸드홀인데
   `food_kind` 가 없어 볼거리로 분류된다. 승격 여부는 해당 지역 이관 때 결정.

## 18. Full migration 권고사항

1. **템플릿은 이미 8개 지역에 걸렸다.** 남은 것은 콘텐츠다. 지역 전용
   우회로는 만들지 않았고 만들 필요도 없다.
2. 지역별로 `FCR0*_RESTAURANT_CAFE_*RESEARCH.csv` 의 `price_range` ·
   `source_url` · `verified_at` 을 `data/place-facts.json` 으로 옮긴다.
   Barcelona 와 같은 방식이고 5분이면 된다.
3. 사진은 **시장·푸드홀·랜드마크부터** 채운다. 개별 식당은 Commons 에 거의
   없다. 먼저 §17-2 의 슬러그 어긋남 39건을 훑으면 새로 받지 않고도 몇 장이
   화면에 올라온다.
4. Nice(§17-6)·Aix(§17-5) 는 원고 자체를 손봐야 한다. 이관 전에 처리한다.
5. 이관 순서는 지시대로 Girona → Nice → Aix → Luberon → Avignon → Lyon →
   Paris. 각 지역마다 `region_structure_check.py` 가 0 을 유지하는지 본다.
6. 지역 하나를 옮길 때마다 CI 순서 그대로 게이트를 돌린다 — 로컬이 전부
   초록이어도 `validate_itinerary.py` 에서 깨진 적이 있다.
