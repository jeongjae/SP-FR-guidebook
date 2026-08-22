# FCR-03 Content & Food Photo Completion

기준 커밋 `a2905b1c` (FCR-02C). 브랜치 `feat/fcr03-content-closure`.
**푸시·머지·PR 하지 않았다.**

작업 도중 지시가 갱신됐다 — 식당·카페 사진을 **Google Maps 해당 업소 사진
우선**으로 다시 열라는 것이었다. 그 전에 내린 `NO_USABLE_IMAGE` 15건을
새 정책으로 전부 다시 처리했다.

---

## Overall Status

**PASS.** 종료 조건을 모두 만족한다.

| 종료 조건 | 결과 |
|---|---|
| 식당/카페 사진 전체 audit | **24/24 완료** |
| known gap 15건 재처리 | **15/15** — 14곳 사진 확보 · 1곳 NO_IMAGE |
| wrong-business photo | **0** |
| place-facts 미등재 86건 disposition | **86/86** |
| CSV 식당 5건 disposition | **5/5** |
| alias unresolved collision | **0** |
| unexpected content loss | **0** |
| 새 G1/G2 regression | **0** (G1 6→5 · G3 125→119 로 오히려 줄었다) |
| 전체 build | **PASS** |
| 기존 FCR guards | **PASS** |

**법적 성격은 숨기지 않았다.** Google Maps 사진은 업로더 저작권이 있고 자유
라이선스가 아니다. 카탈로그에 `google-maps-ugc` 로 적고 출처 URL·업소 신원을
함께 남겼다 — '자유 이용' 이라고 쓰지 않았다. 화면 크레딧도 그대로 나간다.

---

## 1. Food entity 총수

**24곳** — 식당 17 · 시장 3 · 푸드홀 2 · 카페 1 · 빵집 1.
지역별 barcelona 5 · girona 2 · nice 2 · aix 2 · avignon 4 · lyon 4 · paris 5.

## 2. Google Maps 사진 적용 수

**14곳.** 전부 신원 두 겹을 통과한 것만 받았다.

```
1 Maps 가 찾아 준 상호가 우리가 아는 이름과 겹치는가
2 우리가 아는 번지·도로명이 그 장소 페이지에 실제로 있는가
```

| 지역 | 업소 | Maps 가 돌려준 이름 | 주소 대조 |
|---|---|---|---|
| barcelona | Bar Cañete | Bar Cañete | Unió |
| barcelona | Bodega Joan | Bodega Joan | Rosselló |
| barcelona | La Zorra | Restaurant LaZorra | Marítim |
| nice | Le Figuier de Saint-Esprit | Le Figuier de Saint-Esprit | 14 · Saint · Esprit |
| nice | Restaurant Béatrice | Salon de thé - restaurant | 1 · Ephrussi · Rothschild |
| aix | Chez Gilbert | Chez Gilbert | 19 · Baux |
| aix | Pâtisserie Weibel | **Maison Weibel** | 2 · Chabrier |
| avignon | Fou de Fafa | Restaurant Fou de Fafa | 17 · Trois · Faucons |
| avignon | Le Gibolin | Le Gibolin | 13 · Porcelets |
| avignon | Les Cocottes Saint-Louis | Les Cocottes Saint Louis | 20 · Portail · Boquier |
| lyon | Café Comptoir Abel | Café Comptoir Abel | 25 · Guynemer |
| lyon | Chez Mamie Lise | Chez Mamie Lise | 11 · Grenette |
| paris | Boulangerie Pichard | **La Maison Pichard** | 88 · Cambronne |
| paris | Le Grand Pan | Le Grand Pan | 20 · Rosenwald |

상호가 바뀐 두 곳(Weibel → Maison Weibel, Pichard → La Maison Pichard)은
`acceptTitle` 에 새 이름을 적어 두고 주소로 한 번 더 대조했다.

기록한 것 — `source: Google Maps` · `sourcePage`(장소 URL) ·
`businessIdentity`(상호·Maps 상호·주소·placeKey) · `licenseCode:
google-maps-ugc` · 원본 URL · SHA-256. 같은 사진을 두 업소에 쓰지 않았다
(해시 중복 0).

**작업 중 잡은 버그 셋.**
1. 신원 검사가 한글 제목에서 무조건 통과했다. `fold()` 가 라틴 문자만 남겨
   '푸에스토시요 해산물 요리' 가 빈 문자열이 되고, 빈 문자열은 무엇에나
   들어 있다. 이 구멍으로 **La Paradeta 자리에 다른 업소 사진이 붙을 뻔했다.**
2. 후보 필터가 **렌더된 썸네일 크기**를 봤다. 원본은 `=w1600` 으로 다시
   받는데 408×272 를 작다고 버려 Bodega Joan 이 빈칸이 됐다.
3. 852×316 파노라마는 480×320 썸네일 크롭이 안 된다 — 비율로 걸러냈다.

## 3. 기존 사진 유지 수

**9곳** (`VALID_EXISTING`). FCR-02B·02C 에서 Commons 로 확인한 것들이다 —
Mercat de la Concepció · Casa Marieta · Mercat del Lleó · Les Halles ·
Daniel et Denise · Halles de Lyon Paul Bocuse · Bouillon Chartier
Montparnasse · Café du Commerce · Marché Convention.

## 4. NO_IMAGE

**1곳 — La Paradeta Sagrada Família.**

Maps 가 그 주소(Passatge de Simó 18)에서 **`Puertecillo Sagrada Família`**
(Puertecillo Marisquerías, seafood restaurant)를 돌려준다. 상호가 다르므로
사진을 쓰지 않았다.

이건 사진 문제가 아니라 **일정 문제일 수 있다.** Day 2(8/30) 점심이 이
업소다. 폐업이라고 단정하지 않고, 확인한 사실만 `note` 로 남겼다 —
"2026-08-22 Google Maps 확인: 같은 주소가 'Puertecillo Sagrada Família' 로
나온다. 방문 전 영업 여부를 반드시 재확인한다." → **REQUIRES USER DECISION**

## 5. 제거한 wrong-business 사진

**0건.** 애초에 실린 적이 없다. FCR-02C 의 `missing-wrong-entity-risk` 2건은
'후보는 있었으나 다른 업소라 넣지 않았다' 는 상태였고, 카탈로그에 들어간
적이 없음을 이번에 전수 확인했다.

## 6. Place-facts 86건 disposition

| 판정 | 건수 |
|---|---:|
| ALIAS_OF_EXISTING_PLACE | 25 |
| OBSOLETE | 14 |
| ROUTE_OR_UTILITY_NOT_PLACE | 13 |
| RESTAURANT_OR_CAFE | 12 |
| VALID_PLACE_NEEDS_FACTS | 11 |
| REGION_OR_NEIGHBORHOOD | 6 |
| DAY_ONLY_REFERENCE | 5 |
| UNKNOWN | 0 |

정본은 `data/place-facts-disposition.json`. 86개를 일괄 승격하지 않았다.

**병합해 보니 판정이 틀린 곳이 나왔다.** 처음에 37건을 별칭으로 봤는데,
합치려니 `official` 끼리 운영시간이 다른 곳이 14건이었다. 그중 11건은
별칭이 아니라 **상위 장소의 하위 시설**이었다.

- `museu-de-maricel`(화–일 10–19시) ↔ `palau-de-maricel`(가이드투어 전용)
- `lugdunum`(박물관) ↔ `fourviere`(언덕)
- `marche-gordes`(화요장) ↔ `gordes`(마을)
- `chateau-royal-de-collioure`·`chemin-du-fauvisme`·`marche-collioure` ↔ `collioure`
- `sacre-coeur` ↔ `montmartre-south-pigalle`, `vieux-lyon-traboules` ↔ `vieux-lyon` 등

합쳤으면 **현장에서 닫힌 문 앞에 서게 된다.** 이 11건은
`VALID_PLACE_NEEDS_FACTS` 로 바꾸고 facts 를 그대로 뒀다.

## 7. 신규 Place 판정

**승격 0건.** 다섯 조건(반복 참조 · 독립 설명 가치 · Facts+Strategy+
Experience 근거 · 중복 아님 · thin page 아님)을 모두 만족하는 곳이 없었다.

| 후보 | 판정 | 근거 |
|---|---|---|
| Cadaqués | KEEP_IN_REGION_DAY_CONTEXT | 원고 15건·facts 4개는 있으나 Experience 를 채울 서술이 없다. 언급은 전부 동선·시간 문장 |
| Tossa de Mar | KEEP_IN_REGION_DAY_CONTEXT | 원고 4건·facts 0. 조건 3 미충족 |
| Sant Feliu de Guíxols | KEEP_IN_REGION_DAY_CONTEXT | 업소가 특정되지 않은 식사 슬롯이고 서술도 없다 |
| Palais Royal | KEEP_IN_REGION_DAY_CONTEXT | 원고 13건 중 장소 서술은 0. Tuileries·Opéra 지구와 한 덩어리라 떼면 중복 |
| Jardin du Luxembourg | **KEEP_IN_LATIN_QUARTER** | Day 29 stop 이 이미 `latin-quarter` 를 가리킨다. 의도된 연결로 확인 |

`jardin-du-luxembourg` 사진은 그 연결을 따라 라탱 지구 갤러리에 나온다.

## 8. CSV 식당 5건 판정

| 업소 | 판정 | 근거 (2026-08-22 Maps 확인) |
|---|---|---|
| Chez Acchiardo | **CLOSED_OR_INVALID** | 장소 헤더에 `Temporarily closed` |
| Chez Pipo | KEEP_RESEARCH_ONLY | 영업 중. Day 8 점심은 `vieux-nice` 슬롯이며 업소를 고르지 않았다 |
| Marché de La Condamine | KEEP_RESEARCH_ONLY | Maps 가 `Place d'Armes`(광장)로 해석. 독립 업소가 아니다 |
| Le Petit Port | KEEP_RESEARCH_ONLY | 영업 중. Day 10 저녁 stop 이름에 있으나 `place_ref` 는 `menton`. **승격 후보로는 가장 강하다** — 서술이 생기면 PROMOTE |
| Collioure Port Seafood Bistro | OUT_OF_SCOPE | 상호가 아니라 '항구의 해산물 비스트로' 라는 범주다 |

## 9. Pâtisserie Weibel 판정

**PROPOSED_SOT_CHANGE.** 원인만 확정하고 Day SOT 는 고치지 않았다.

- **원인** — Day 13 08:30 stop 하나가 두 장소를 담는다. `id`·`place_ref` 는
  `place-richelme-place-des-precheurs` 이고 이름은
  `Place Richelme 목요 시장 & Pâtisserie Weibel` 이다. 모델은 stop 당 장소
  하나만 잇는다.
- **영향** — 일정의 의미는 잃지 않는다(08:30–10:00 한 블록에서 둘 다 본다).
  잃는 것은 표시다 — Weibel 카드에 방문일 배지가 없고 장소 페이지가 그날과
  이어지지 않는다.
- **선택지** — A: stop 분할(시간표가 바뀐다) · B: 보조 참조 필드 `also_ref`
  (시간표는 그대로, 모델·렌더러가 바뀐다).
- **권고** — B. 한 stop 이 시장+가게를 겸하는 형태가 다른 날에도 있을 수 있고,
  시간표를 건드리지 않는 쪽이 안전하다.

## 10. Alias / Facts 정리

`scripts/merge_fact_aliases.py` 로 **25건 병합**. 값이 달라 기록에 남긴 충돌
**14건** (`FCR03_FACT_MERGE_CONFLICTS.json`).

충돌 해결 순서는 지시대로 했다 — 신뢰도 → verifiedAt → 공식 출처 우선.
같은 시설의 중복 3건은 판정을 데이터에 명시했다.

| 중복 | 남긴 값 | 근거 |
|---|---|---|
| `mercat-de-la-concepcio` → `mercat-concepcio` | 2026-08-21 · 공식 URL | 옛 값은 2026-08-17 이고 hours 출처가 URL 이 아니다 |
| `fou-de-fafa` → `fou-de-fafa-avignon` | 2026-08-21 · 공식 URL | 옛 값 출처가 '복구본' 표기 |
| `daniel-et-denise-crequi` → `daniel-et-denise` | 2026-08-21 · 공식 URL | 옛 전화번호는 `note` 로 보존 |

place-facts 의 명부 밖 슬러그가 **86 → 61** 로 줄었다. 남은 61건은 전부
판정이 붙어 있고, 별칭은 0 이다.

## 11. G1 / G2 분석

| 가드 | FCR-02C | 지금 | 판단 |
|---|---:|---:|---|
| G1 방문 요일 vs 휴관일 | 6 | **5** | 별칭 병합으로 1건 해소 |
| G2 fact 토큰 밖 하드코딩 | 384 | **384** | 변화 없음 |
| G3 필수항목 참조 | 125 | **119** | 병합으로 6건 감소 |
| G4·G5 | PASS | PASS | |

**G1 5건의 분류 — 전부 `true defect` 다.**

| 건 | 내용 | 분류 |
|---|---|---|
| 1 | Nice 원고가 2026-09-05(토)에 Acchiardo 를 든다. 이 업소는 토·일 휴무이고 **지금은 Temporarily closed** | true defect (후보 서술) |
| 2–5 | **Marché Convention 이 Day 29(9.26 토)·Day 36(10.3 토) 아침 일정에 있다** | **true defect (Day SOT)** |

두 번째가 중요하다. 이 시장의 공식 정보(paris.fr, 2026-08-21 확인)는
`화·목 07:00–13:30 · 일 07:00–14:30` 이고 **월·수·금·토 휴무**다.
그런데 Day 29 의 stop 이름은 `Marché Convention 일요 노천시장 장보기` 인데
그날은 **토요일**이고, Day 36 은 `토요 장보기` 라고 이름에 적혀 있다.
**두 번의 아침이 닫힌 시장 앞으로 잡혀 있다.** 휴관일 사실에는 대안까지
적혀 있다 — 인근 토요 시장 `Marché Grenelle`.

Day SOT 변경이라 고치지 않았다. → **REQUIRES USER DECISION**

**G2 384건 분류** (표본 확인)

| 분류 | 성격 | 대략 |
|---|---|---|
| legacy debt | 계획가·환율·예산 범위 등 fact 로 만들 대상이 아닌 서술 (`money`) | 다수 |
| expected exception | 식사 시간대·체류시간·촬영 시각 같은 편집 판단 (`time`) | 다수 |
| true defect | 시설의 휴관일·요금을 토큰 없이 하드코딩한 것 (`weekday`) | 일부 |
| false positive | 배지가 이미 붙은 미검증 표기 | 일부 |

건수가 그대로이고 대규모 원고 수정이 필요하므로 FCR-03 범위 밖으로 둔다.

## 12. 콘텐츠 손실 QA

`a2905b1c` 를 별도 워크트리에 빌드해 비교했다.

```
페이지 369 → 369 · 사라진 페이지 0
문장 8,472 대조 · 차이 6건
```

6건 전수 분류 — **unexpected loss 0.**

| 유형 | 건 | 확인 |
|---|---:|---|
| intentional merge | 2 | 옛 별칭의 운영시간 줄이 최신 공식값으로 대체됐다. 전화번호는 `note` 로 살아 있음을 배포본에서 확인 |
| render-only change | 4 | `note` 사실이 늘어 장소 페이지 사실표의 행 순서가 바뀐 것. 소요시간 값은 그대로 있음을 4곳 모두 확인 |

`content_audit.py` — 승격된 장문 전수, 손실 0.

## 13. 변경 파일

```
build/research_closure_check.py (신규)   조사 종결 가드
build/site.py                            가드 연결
build/region_structure_check.py          사진 상태 어휘
scripts/add_google_maps_photo.py (신규)  Maps 사진 파이프라인
scripts/merge_fact_aliases.py (신규)     별칭 병합·충돌 기록
data/images/google-maps-photo-queue.json (신규)
data/images/food-photo-status.json       FCR-03 어휘로 재작성
data/images/image-manifest.json/csv      Maps 사진 14장
data/place-facts.json                    별칭 25건 병합 · la-paradeta note
data/place-facts-disposition.json (신규) 86건 판정
source/ASSETS/photos/originals/*-gm01.jpg          신규 14
source/ASSETS/photos/processed/**                  파생본 28
source/CURRENT/20_Regional_Chapters/*.md           fact 토큰 슬러그 이동
FCR03_CONTENT_FOOD_PHOTO_QA.md · FCR03_DISPOSITIONS.json
FCR03_FOOD_PHOTO_AUDIT.json · FCR03_FACT_MERGE_CONFLICTS.json
docs/fcr03/*.png
```

## 14. Build / Test 결과

```
build/site.py                    PASS (모델·어휘·장문·fact·content·구조·사진·조사 가드)
build/research_closure_check.py  PASS  잘못된 업소 사진 0 · 미분류 0 · 미병합 별칭 0
build/region_structure_check.py  PASS  오분류 0 · Day 참조 0 · 링크 0
build/media_lookup_check.py      PASS  미매핑 0 · 조용히 사라진 사진 0
build/table_loss_check.py        PASS  잔여 병합 0
build/ux_check.py                PASS
build/viewport_check.py          PASS  360·390·430·768·1024·1440
build/content_audit.py           PASS  콘텐츠 손실 0
build/pwa_check.py               PASS  866파일 61.8MiB 오프라인 심층 탐색
build/test_validation.py         14/14 OK
scripts/validate_itinerary.py    PASS  43일·42박
scripts/validate_media.py        PASS
scripts/validate_map_data.py     PASS
scripts/generate_attributions.py --check  PASS
```

식당·카페 완결성 — 사진 23/24 · 소개 24/24 · 공홈 24/24 · 지도 24/24 ·
가격 24/24 · 메뉴 20/24 · 방문일 21/24.

## 15. 남은 unresolved items

**REQUIRES USER DECISION**

1. **Marché Convention 토요일 일정 2건** (Day 29 · Day 36). 공식 휴관일과
   충돌한다. 대안은 사실 레코드에 이미 있다 — Marché Grenelle. Day SOT 변경.
2. **La Paradeta Sagrada Família** (Day 2 점심). 같은 주소가 다른 상호로
   나온다. 방문 전 확인이 필요하고, 바뀌었다면 대체 업소를 골라야 한다.
3. **Pâtisserie Weibel 방문일 연결** — 위 §9 의 A/B 선택.

**CONTENT INTENTIONALLY UNRESOLVED**

4. 사진 없는 식당 1곳 (La Paradeta — 위 2번과 같은 사안).
5. 메뉴 없는 4곳 — 시장 3곳(대표 메뉴 개념이 맞지 않는다)과 Weibel.
6. 방문일 없는 3곳 — Casa Marieta·Mercat del Lleó 는 일정에 없는 추천이고,
   Weibel 은 위 3번.
7. 승격하지 않은 장소 후보 4곳 + 식당 후보 4곳. 전부 '무엇이 없어서 못
   하는지' 가 판정 파일에 적혀 있다.
8. `VALID_PLACE_NEEDS_FACTS` 11곳 — 상위 장소의 하위 시설. facts 는 유효하고
   화면에도 나오지만 명부에는 없다. 승격하려면 서술이 필요하다.

**BASELINE DEBT**

9. G1 5건 · G2 384건. 새 regression 은 없다.
10. `place-facts` 가 자기 스키마를 어긴다 (`confidence: editorial`, `note` 키).
    모델이 이 파일만 스키마 검증을 하지 않는다.

---

## 최종 구분

```
STRUCTURE COMPLETE            8개 지역 · 지역 전용 분기 0 · 가드 4종
CONTENT RESOLVED              사진 23/24 · 가격 24/24 · 86건 판정 · 별칭 병합 25
CONTENT INTENTIONALLY         승격 0건 · 사진 1곳 비움 · 메뉴 4곳 없음
  UNRESOLVED                  (전부 근거 기록)
REQUIRES USER DECISION        Marché Convention 토요일 2건 ·
                              La Paradeta 상호 변경 · Weibel stop 구조
```

여기서 중단한다. 다음 단계로 자동 진행하지 않는다.
