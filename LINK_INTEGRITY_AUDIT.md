# 링크 무결성 전수감사 — 내외부 참조와 링크 가시성

감사일 2026-08-21 · 기준 `origin/main` `b4fe708b` · 브랜치 `audit/link-integrity`
재현 명령: `SPFR_SITE_DIR=<빌드경로> python3 scripts/link_integrity_audit.py`

> **수정 반영본.** 아래 표의 "감사 시점"은 수정 전 값이고, "수정 후"는 같은
> 스크립트를 고친 코드로 다시 돌린 값이다. 본문의 진단은 원인 기록으로 남긴다.

| 축 | 감사 시점 | 수정 후 | 조치 |
|---|---:|---:|---|
| A 고아 장소 | 34 | **4** | `place_ref` 반영 + 가이드 상한 제거 + `nce-t2` 연결 |
| B 미실현 `place_ref` | 89 | **0** | `model.py` 가 `place_ref` 를 읽는다 |
| C 무밑줄 본문 인라인 | 53 | **0** | `.tl-name a` 기본 밑줄 복원 |
| D 가이드 누락 필수 | 38 | **0** | 넘치는 필수를 `그 밖의 장소` 에 싣는다 |
| E 끊긴 내부 링크 | 1 | **0** | 원고의 중첩 링크 수정 |
| E' `noopener` 누락 | 37 | **0** | 마크다운 외부 링크에 `rel` 일괄 적용 |
| — 빌드 가드 | 없음 | **추가** | `place_ref` 미실현·오참조 시 빌드 중단 |

남은 고아 4개는 링크 문제가 아니라 **원고가 없는 빈 페이지**다 —
`sitges` · `barcelona-historic-walk` · `barcelona-modernisme-walk` ·
`girona-old-town-walk` 는 `source/CURRENT/30_Places/` 에 원고 파일 자체가
없다. 빈 페이지로 독자를 보내는 것이 링크가 없는 것보다 나쁘므로 연결하지
않았다. 원고를 쓰거나 명부에서 내리는 것이 옳은 조치다.

---

## 종합

전수 대상은 **실페이지 207쪽 · 본문 링크 1,630개 · 외부 링크 1,549개 · 렌더 링크 3,444개**다.
끊긴 링크는 1건뿐이라 **링크의 "정확도"는 건강하다.** 문제는 **연결의 "누락"과 "가시성"** 두 축이다.

| 축 | 결함 | 규모 | 심각도 |
|---|---|---:|---|
| A | 장소 페이지가 있는데 본문 어디서도 링크되지 않음 | **34 / 138** | 높음 |
| B | `place_ref` 가 링크로 실현되지 않음 | **89 / 140** | 높음 (A의 원인) |
| C | 밑줄·색이 없어 링크로 보이지 않음 (본문 인라인) | **53** (25쪽) | 높음 |
| C' | 카드 전체가 클릭 대상인 링크 | 945 | 설계 의도 — 별건 |
| D | 가이드 페이지가 상한 때문에 빠뜨린 필수 장소 | **38** | 중간 |
| E | 끊긴 내부 링크 | **1** | 중간 |
| E' | 외부 링크 `rel=noopener` 누락 | **37** | 낮음 |

---

## A. 고아 콘텐츠 — 장소 34개

`places/*.html` 138개 중 **34개가 본문 어디에서도 링크되지 않는다.** 내비게이션(상단바·하단탭·꼬리말·탭 스트립)은 모든 페이지에 있으므로 집계에서 제외했다 — 축에서만 닿는 것은 연결이 아니다.

`places/index.html` 은 **존재하지 않는다.** 장소로 가는 길은 가이드·데일리·지도·장소 간 링크 넷뿐이고, 이 34개는 그 어느 쪽에서도 닿지 않는다.

| 지역 | 고아 |
|---|---:|
| paris | 14 |
| avignon | 6 |
| nice | 5 |
| barcelona | 3 |
| girona | 2 · aix 2 · lyon 2 |

식당·빵집·시장이 특히 많다 — `bouillon-chartier-montparnasse`, `boulangerie-pichard`, `cafe-du-commerce`, `chez-gilbert-cassis`, `chez-mamie-lise`, `daniel-et-denise`, `fou-de-fafa-avignon`, `le-gibolin-arles`, `le-grand-pan`, `les-cocottes-saint-louis`, `casa-marieta`, `patisserie-weibel`, `marche-convention`. 파리 미술관 7곳(`musee-de-l-orangerie`·`musee-marmottan-monet`·`musee-picasso-paris` 등)과 `versailles`·`notre-dame-de-paris`·`arles`·`sitges` 같은 큰 장소도 포함된다.

**34개 전부 `days == []`** 다. 즉 어느 Day 에도 묶이지 않았고, 그래서 데일리에서 링크가 나가지 않는다. 32개는 `grade=essential` 인데도 그렇다.

완화 요소 하나 — **34개 모두 검색 색인에는 있다**(색인 189건, 장소 138개 전부 포함). 검색으로는 찾을 수 있으나, 링크로는 닿을 수 없다.

전수: `LINK_AUDIT_ORPHAN_PLACES.csv`

---

## B. 미실현 참조 — `place_ref` 89건 (A의 직접 원인)

`data/daily-cards/*.json` 의 stop 은 `place_ref` 필드로 장소를 가리킨다. 140개 stop 이 이 값을 갖고 있다. 그런데 **빌드는 이 필드를 읽지 않는다.**

```
build/model.py:573    p = places.get(s.id)      # ← stop.id 로만 잇는다
```

`grep -rn "place_ref" build/` 결과가 **0건**이다. 링크는 `stop.id` 가 장소 슬러그와 **정확히 같을 때만** 생긴다.

| place_ref 상태 | 건수 | 링크 생성 |
|---|---:|---|
| `place_ref == stop.id` | 51 | 생김 |
| `place_ref != stop.id` | **89** | **안 생김** |
| `place_ref` 없음 | 108 | — |

89건이 가리키는 장소는 **전부 실재한다**(존재하지 않는 ref 0건). 고유 장소 63곳, 영향 Day 36일이다.

```
Day  2  sant-pau            → sant-pau-recinte-modernista
Day  4  cau-ferrat-maricel  → cau-ferrat
Day  7  promenade           → promenade-des-anglais
Day  9  cannes-transfer     → cannes
Day 10  monaco-port-lunch   → monaco
Day 34  (베르사유 3 stop)    → versailles
```

즉 EX-11A 가 `place_ref` 를 채워 넣었지만 렌더러가 그것을 소비하지 않아 **140개 중 89개가 죽은 데이터**로 남았다. 이 하나를 고치면 A의 34개 중 **23개가 자동으로 해소된다.**

전수: `LINK_AUDIT_UNREALIZED_PLACEREF.csv`

---

## C. 링크 가시성 — 밑줄 없는 링크

390px 실렌더로 3,444개 링크의 계산된 `text-decoration-line` 과 색을 측정했다. **밑줄이 없고 부모와 같은 색**이면 본문과 구분되지 않는다.

| 유형 | 건수 | 판정 |
|---|---:|---|
| 밑줄 있음 | 2,446 | 정상 |
| 밑줄 없음 · `card-link` | 945 | **설계 의도** — 카드 전체가 클릭 대상이고 카드 테두리가 어포던스를 준다 |
| 밑줄 없음 · **클래스 없는 본문 인라인** | **53** | **결함** |

53건은 전부 **데일리 페이지 타임라인의 장소 링크**이며 25쪽에 걸쳐 있다. 원인은 한 줄이다.

```
build/assets/style.css:739   .tl-name a { color: inherit; text-decoration: none; }
build/assets/style.css:740   .tl-name a:hover { text-decoration: underline; }
```

색을 상속하고 밑줄을 지운다. 밑줄은 **hover 에서만** 돌아오는데, 이 가이드북의 주 사용 환경인 터치 화면에는 hover 가 없다. 현장에서 "Sagrada Família" 가 눌리는 글자인지 알 방법이 없다.

```
daily/day-02.html  'Sagrada Família'             → ../places/sagrada-familia.html
daily/day-03.html  'Bar Cañete 점심'              → ../places/bar-canete.html
daily/day-04.html  'Barcelona Sants'             → ../places/barcelona-sants.html
```

`.card-title a`(464행)·`.crumbs a`(523행)도 밑줄을 지우지만, 각각 카드 어포던스와 빵부스러기 관례가 있어 별개로 본다.

전수: `LINK_AUDIT_INVISIBLE_LINKS.csv` (`cls` 열이 비어 있는 행이 결함 53건)

---

## D. 가이드 페이지가 빠뜨린 필수 장소 38개

지역 페이지의 장소 노출은 두 블록뿐이다.

```
build/render.py   must   = [p for p in r.essential_places if p.summary][:6]
build/render.py   others = [p for p in r.places if p.grade != "essential" ...]
```

`놓치지 말 것` 은 **상한 6개**, `그 밖의 장소` 는 **essential 을 제외**한다. 그래서 7번째부터의 필수 장소는 **두 블록 어디에도 들어가지 못한다.**

| 지역 | 필수(요약 보유) | 표시 | 누락 |
|---|---:|---:|---:|
| paris | 25 | 6 | **19** |
| nice | 13 | 6 | **7** |
| avignon | 12 | 6 | **6** |
| aix | 8 | 6 | 2 |
| lyon | 8 | 6 | 2 |
| barcelona | 7 | 6 | 1 |
| girona | 7 | 6 | 1 |
| luberon | 4 | 4 | 0 |
| **합계** | | | **38** |

파리는 필수 25곳 중 19곳이 지역 페이지에서 사라진다. 절단이 조용해서(경고 없음) 편집자도 알 수 없다.

전수: `LINK_AUDIT_GUIDE_DROPPED_ESSENTIAL.csv`

---

## E. 끊긴 링크와 외부 링크

**끊긴 내부 링크 1건** — 마크다운 링크가 링크 안에 중첩돼 href 가 깨졌다.

```
places/restaurant-beatrice.html
  href="[공식 웹사이트](https://www.villa-ephrussi.com/)fr/preparer-sa-visite/le-restaurant-salon-de-the"
```

원고에서 `[텍스트](url)` 안에 다시 `[...](...)` 를 넣은 것으로 보인다. 원고를 고쳐야 한다.

**외부 링크 1,549건 · 고유 569개.** 호스트는 google.com 220(지도), commons.wikimedia.org 143(사진 출처), en.wikipedia.org 93(참고)이 대부분이다.
그중 **37건에 `rel="noopener"` 가 없다.** 대부분 식당·시설 공식 홈페이지다(`casamarieta.com`, `maisonweibel.com`, `bouillon-chartier.com` 등).

전수: `LINK_AUDIT_BROKEN_LINKS.csv` · `LINK_AUDIT_EXTERNAL_LINKS.csv`

---

## 권고 (우선순위)

| # | 조치 | 해소 |
|---|---|---|
| 1 | `build/model.py` 가 `place_ref` 를 읽게 한다 — `places.get(s.place_ref or s.id)` | B 89건 · A 23건 |
| 2 | `.tl-name a` 의 `text-decoration: none` 을 걷어낸다(또는 hover 아닌 기본 상태에 밑줄) | C 53건 |
| 3 | 가이드의 `[:6]` 상한을 없애거나, 넘치는 필수 장소를 `그 밖의 장소` 에 포함시킨다 | D 38건 |
| 4 | 나머지 고아 11개를 원고에서 링크하거나 Day 에 묶는다 | A 잔여 |
| 5 | `restaurant-beatrice` 원고의 중첩 링크를 고친다 | E 1건 |
| 6 | 외부 링크 렌더에 `rel="noopener"` 를 일괄 적용한다 | E' 37건 |
| 7 | 위 검사를 빌드 가드로 승격한다 — 고아·미실현 ref·끊긴 링크는 빌드가 멈춰야 한다 | 재발 방지 |

1·2·3 은 각각 코드 한두 줄이고, 셋을 합치면 A·B·C·D 의 대부분이 해소된다.

---

## 제3자 검증 방법

```bash
python3 build/site.py                                   # 또는 SPFR_SITE_DIR=<경로>
SPFR_SITE_DIR=<경로> python3 scripts/link_integrity_audit.py --out <출력경로>
```

스크립트는 빌드 산출물만 읽고 아무것도 수정하지 않는다. 위 표의 모든 수치는 그 출력으로 재현된다.
`playwright` 가 없으면 C(가시성)만 건너뛰고 나머지는 그대로 나온다.

| 파일 | 행수 | 내용 |
|---|---:|---|
| `LINK_AUDIT_ORPHAN_PLACES.csv` | 34 | 고아 장소 + 지역·등급·종류·연결된 Day |
| `LINK_AUDIT_UNREALIZED_PLACEREF.csv` | 89 | 링크되지 않은 `place_ref` (Day·stop·대상) |
| `LINK_AUDIT_INVISIBLE_LINKS.csv` | 998 | 밑줄 없는 링크 전수 (`cls` 빈 행 53건이 결함) |
| `LINK_AUDIT_GUIDE_DROPPED_ESSENTIAL.csv` | 38 | 가이드에서 잘린 필수 장소 |
| `LINK_AUDIT_EXTERNAL_LINKS.csv` | 1549 | 외부 링크 전수 + `noopener` 여부 |
| `LINK_AUDIT_BROKEN_LINKS.csv` | 1 | 끊긴 내부 링크 |
| `LINK_AUDIT_LINK_GRAPH.csv` | 1630 | 본문 링크 그래프 전체 (source→target) |
