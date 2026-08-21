# 지도 링크 이름 검색 전환 — 사전 전수조사

조사일 2026-08-22 · 기준 `origin/main` `4c80f12f` · 브랜치 `feat/map-name-links`
산출물: `MAP_NAME_LOOKUP_AUDIT.csv` (147행)

> 이 문서는 **전환 전 사전조사**다. 코드는 아직 바꾸지 않았다.
> 어떤 대상을 이름으로 바꿀 수 있고 어떤 것을 좌표로 남겨야 하는지 먼저 확정한다.

---

## 1. 현재 상태

| 항목 | 값 |
|---|---:|
| 구글맵 링크 총계 | **778** |
| — 검색 링크 `maps/search` | 675 (`map/` 419 · `daily/` 248 · `guide/` 8) |
| — 길찾기 링크 `maps/dir` | 103 (장소 페이지) |
| **좌표형** | **777** |
| 이름·주소형 | 1 (Aix 숙소, 주소) |
| 지도 링크가 **하나도 없는** 장소 페이지 | **36 / 138** |

생성 지점은 세 곳뿐이다.

```
build/render.py:518  maps_url()      좌표 우선 → 주소 폴백
build/render.py:495  map_card()      지도·데일리 페이지의 핀 목록
build/render.py:566  build_place()   장소 페이지 '길찾기' 버튼 — p.lat 없으면 버튼 자체가 없다
```

---

## 2. 조사 방법과 한계

`GOOGLE_MAPS_API_KEY` 는 CI 시크릿이라 로컬에 없다. Places API 로 place_id 를 받을 수 없어 **웹 검색으로 실재·위치를 교차 확인**했다. 각 행에 `evidence_url` 을 남겨 제3자가 같은 근거를 다시 열 수 있다.

판정 기준.

| 판정 | 뜻 |
|---|---|
| `FOUND` | 이름(+도시)으로 검색하면 단일하고 올바른 장소로 특정된다 |
| `AMBIGUOUS` | 검색은 되지만 동명·다지점·면(面) 단위라 한 곳으로 좁혀지지 않는다 |
| `NOT_FOUND` | 구글맵에 그 이름의 장소가 없다 (산책 코스명·상품명·추상 묶음) |

---

## 3. 결과

| 판정 | 건수 | 조치 |
|---|---:|---|
| **FOUND** | **123** | 이름 검색으로 전환 |
| **AMBIGUOUS** | **13** | 앵커 지점을 정하거나 좌표 유지 |
| **NOT_FOUND** | **11** | 좌표 유지 (좌표도 없으면 링크 없음) |

지역별 FOUND 비율 — luberon 12/12 · paris 26/30 · avignon 20/22 · aix 18/22 · nice 16/20 · barcelona 14/17 · girona 11/12 · **lyon 6/11**.
리옹이 낮은 이유는 `Vieux Lyon`·`Fourvière`·`Croix-Rousse` 처럼 **면 단위 구역**이 많고 `Daniel et Denise` 가 다지점이기 때문이다.

---

## 4. 이름으로 찾지 못한 11건 (좌표 유지 대상)

| slug | 이름 | 이유 |
|---|---|---|
| `barcelona-historic-walk` | Barcelona 역사도심 권역 | 도보 권역 개념 — POI 아님 |
| `barcelona-modernisme-walk` | Barcelona Modernisme 권역 | 〃 |
| `girona-old-town-walk` | Girona 구시가지 권역 | 〃 |
| `nice-walk` | Nice Old Town–Castle Hill Walk | 〃 |
| `cannes-walk` | Cannes Forville–Suquet–Croisette Walk | 〃 |
| `monaco-walk` | Monaco Rocher–Port–Monte Carlo Walk | 〃 |
| `montmartre-south-pigalle` | Montmartre · South Pigalle | 18구+9구 두 지구를 묶은 편집 명칭 |
| (숙소) | Les Toits de Méjanes (Airbnb) | Airbnb 상품명 — POI 없음. **주소로 검색** |
| (숙소) | La Terrasse du Clocher (후보) | 임대 아파트 상품명. 지도에는 운영사 `Les Appartements du Clocher` |
| (숙소) | Palais ALZIRA · 12 Rue Verdi | 사설 주거건물 — 상호 POI 없음. **주소로 검색** |
| (숙소) | 기내 (OZ502) — 숙소 없음 | 지리적 장소가 아님 — 지도 대상에서 제외 |

**이 중 8건은 좌표조차 없다.** walk 6건 + Méjanes 숙소 + 기내. 즉 이름도 좌표도 없어 **지도 링크를 만들 수 없다.**
walk 6건은 애초에 원고 파일도 없는 빈 페이지다(앞선 링크 감사에서 확인). 지도가 아니라 콘텐츠 문제다.

---

## 5. 앵커가 필요한 13건 (AMBIGUOUS)

이름은 실재하지만 **점이 아니라 면**이거나 다지점이라 핀이 임의가 된다. 권장 앵커를 함께 적는다.

| slug | 문제 | 권장 앵커 |
|---|---|---|
| `latin-quarter` | 지구 | Place de la Sorbonne |
| `le-marais` | 지구 | Place des Vosges |
| `vieil-aix` | 관용 호칭 | Place de l'Hôtel de Ville, Aix |
| `la-roquette` | 아를 구역 · 동명 지명 다수 | Église Saint-Césaire, Arles |
| `croix-rousse` | 구역 · 동명 역·병원 | Place de la Croix-Rousse |
| `vieux-lyon` | 구역 + 트라불 총칭 | Cathédrale Saint-Jean-Baptiste |
| `fourviere` | 바실리카 + 로마극장(400m 이격) | Basilique Notre-Dame de Fourvière |
| `annecy` | 구시가 + 호수 | Palais de l'Île |
| `calanques` | 칼랑크 3곳을 한 항목에 | 3개로 분리 |
| `place-richelme-place-des-precheurs` | 광장 2곳을 한 항목에 | 2개로 분리 |
| `daniel-et-denise` | 리옹 다지점 | Daniel et Denise **Créqui** |
| `bodega-joan` | 동명 2곳 | 번지 병기 (Rosselló 164) |
| (숙소) 78 Rue de Lourmel | 업소명 없는 주소형 | 주소로 검색 |

---

## 6. 조사하다 드러난 것 — 현재 좌표가 상당히 틀렸다

이름 검증의 부산물로 **좌표 오류 31건**이 확인됐다. 이름 전환의 근거가 되는 발견이다.

### 6.1 숙소 좌표가 식당에 복사됐다 (최악)

| 복사된 좌표 | 오염된 항목 | 실제와의 오차 |
|---|---|---|
| `48.8472, 2.2894` (파리 숙소) | Bouillon Chartier Montparnasse · Boulangerie Pichard · Café du Commerce · Le Grand Pan · Marché Convention | 최대 **약 2.5km** |
| `45.746467, 4.868933` (리옹 숙소) | Café Comptoir Abel · Daniel et Denise | **약 3km** |
| `43.94993, 4.81302` (아비뇽 숙소) | Fou de Fafa · Les Cocottes Saint-Louis | 수백 m |
| `43.6865, 7.3323` (빌라) | Restaurant Béatrice | 부속 시설이라 정상 |

**Bouillon Chartier Montparnasse 는 애초에 6구인데 15구 숙소 좌표를 달고 있다.** 좌표를 믿고 이동하면 엉뚱한 곳에 도착한다.

### 6.2 그 밖의 좌표 오차

`Palais des Papes` 약 700m · `Versailles` 약 700m · `Les Halles d'Avignon` 약 400m · `La Paradeta` 약 400m · `Café du Commerce` 약 400m · `Marché Convention` 약 900m · `La Zorra` 약 300m · `Halles de Lyon` 약 230m · `Mercat de la Concepció` 약 200m · `Bar Cañete` 약 180m · `Ménerbes` 반올림 오차.
`Calanques` 좌표는 칼랑크가 아니라 **Cassis 항구 근처**를 가리킨다.

### 6.3 좌표가 아예 없는 37건

이름 검색으로 바꾸면 **29건이 지도를 갖게 된다**(현재는 링크 자체가 없다). 나머지 8건은 §4 의 이름·좌표 모두 없는 항목이다.

---

## 7. `region` 을 검색어에 쓰면 안 된다 — 최소 28건이 틀어진다

`region` 은 **체류 거점**이지 그 장소의 도시가 아니다.

| region | 실제 도시 | 항목 수 |
|---|---|---:|
| avignon | Arles · Les Baux · Saint-Rémy · Uzès · Vers-Pont-du-Gard | 14 |
| aix | Marseille · Cassis · Grasse · Saint-Paul-de-Vence | 9 |
| nice | Antibes · Cannes · Monaco · Menton · Saint-Jean-Cap-Ferrat | 6 |
| lyon | Annecy | 2 |
| barcelona | Sitges · **Collioure(프랑스)** | 4 |
| paris | **Giverny(노르망디, 75km)** | 1 |

`Collioure` 는 `city_hint` 가 "Girona, Spain" 인데 **프랑스** 마을이다. 검색어를 기계적으로 만들면 국경을 넘어 틀린다.
따라서 검색어는 `region` 이 아니라 **검증으로 확인한 실제 도시**(CSV 의 `recommended_query`)를 써야 한다.

---

## 8. 이름 검색에도 규칙이 필요하다

FOUND 여도 이름을 그대로 넣으면 틀리는 것이 많다. CSV 의 `recommended_query` 는 아래 규칙을 이미 반영했다.

| 규칙 | 예 |
|---|---|
| 시설 종류 접두를 붙인다 | `Nice-Ville` → **Gare de** Nice-Ville · `Versailles` → **Château de** Versailles · `Rotonde` → **Fontaine de la** Rotonde · `Peralada` → **Castell de** Peralada |
| 다지점은 지점명을 붙인다 | `La Paradeta` → **Sagrada Família** · `Bouillon Chartier` → **Montparnasse** · `Daniel et Denise` → **Créqui** |
| 동명 충돌은 도시를 붙인다 | `Fort Saint-Jean, **Marseille**` · `Théâtre antique **d'Arles**` · `Les Halles **d'Avignon**` · `Musée Rodin, **Paris**` |
| 별칭·괄호는 뺀다 | `Vieux Nice`(Babazouk 제외) · `Cannes`(Le Suquet & La Croisette 제외) |
| 한국어 별칭은 정식 상호로 | `바스카라의 B&B` → **Casa Bascara** |
| 공식 개명은 새 이름으로 | `Terrain des Peintres` → **Jardin des Peintres** |

---

## 9. 곁가지로 확인된 사실 오류 (지도 밖)

| 내용 | 근거 |
|---|---|
| **Centre Pompidou 는 2025-09-22 ~ 2030 전면 휴관** — 여행 기간 방문 불가 | centrepompidou.fr |
| **Marché Convention 개장일은 화·목·일** — 원고 표기 확인 필요 | paris.fr |
| **Pâtisserie Weibel 주소는 2 rue Chabrier** — `local_name` 의 'rue Méjanes' 근거 없음 | maisonweibel.com |
| Bastide du Jas de Bouffan · Atelier de Cézanne 는 2026 재개관·예약 필수 | cezanne-en-provence.com |
| Carrières de Bibémus 는 가이드투어만 (셔틀 주차) | 〃 |

---

## 10. 권고 전환 방침

1. **`FOUND` 123건** → `recommended_query` 로 이름 검색 링크를 만든다.
2. **`AMBIGUOUS` 13건** → 앵커 지점을 데이터에 명시하고 그 이름으로 검색한다. 앵커를 정하기 전까지는 좌표를 유지한다.
3. **`NOT_FOUND` 11건** → 좌표를 유지한다. 좌표도 없는 8건은 링크를 만들지 않는다(빈 지도로 보내지 않는다).
4. **숙소 3건**(Méjanes · Lourmel · ALZIRA)은 이름이 아니라 **주소**로 연다. 이미 `maps_url` 이 주소 폴백을 갖고 있다.
5. 이름을 정본 데이터에 필드로 넣는다 — 렌더 시점에 문자열을 조립하면 §7·§8 의 규칙이 코드에 흩어진다.
6. **좌표는 지우지 않는다.** 지도 핀·거리 계산·오프라인 지도가 좌표를 쓴다. 다만 §6 의 오염 31건은 별건으로 정정해야 한다 — 이름 링크로 가리더라도 핀은 여전히 틀린 자리에 찍힌다.

---

## 11. 제3자 검증 방법

`MAP_NAME_LOOKUP_AUDIT.csv` 각 행에 `evidence_url` 이 있다. 다음을 확인하면 된다.

1. `recommended_query` 를 구글맵에 그대로 넣어 단일 장소로 특정되는가
2. 그 결과가 `resolved_name` · `resolved_address` 와 일치하는가
3. `current_lat`/`current_lng` 와 실제 위치의 거리 (§6 오차 주장 확인)

| 열 | 뜻 |
|---|---|
| `verdict` | FOUND / AMBIGUOUS / NOT_FOUND |
| `recommended_query` | 구글맵에 넣을 최종 검색어 (FOUND 만) |
| `resolved_name` / `resolved_address` | 검증으로 확인한 실제 상호·주소 |
| `current_lat` / `current_lng` / `has_coords` | 현재 저장된 좌표 |
| `evidence_url` | 근거 URL |
| `note` | 좌표 오차·도시 오류·다지점 등 특기사항 |
