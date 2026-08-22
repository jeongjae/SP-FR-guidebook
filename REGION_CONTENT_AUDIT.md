# REGION_CONTENT_AUDIT — 지역 가이드 콘텐츠 인벤토리

`python3 build/region_audit.py` 가 만든다. 손으로 고치지 않는다.

판정은 제목이 아니라 엔티티로 한다. `점심`·`저녁`·`Lunch`·`Dinner` 가
제목에 있다는 이유로 식당으로 분류하지 않는다 — 30_Places 정본에
`food_kind`·`meal_role` 이 있어야 식당·카페·시장이다.

## 요약

| 항목 | 값 |
|---|---:|
| 지역 수 | 8 |
| 인벤토리 항목 | 459 |
| **장소 섹션에 있던 식당·카페·시장** | 22 |
| **먹거리 섹션에 있던 관광지** | 17 |
| 먹거리 섹션의 업소 아닌 식사 슬롯 | 7 |
| 제거 대상 일정 섹션 | 8 |
| 제거 대상 한눈에 보기 섹션 | 8 |
| 제거 대상 꼬리말 블록 | 14 |
| Day 에서 복사해 오던 교통 문자열 | 86 |
| 통합 후 남는 교통 블록 | 57 |
| 지역을 넘나든 식당 카드 | 5 |
| 식당·카페·시장 장소 | 22 |
| 사진 없는 식당·카페 | 16 |
| 가격 근거 없는 식당·카페 | 1 |
| 장소로 잇지 못한 사진 (명부 미등재) | 11 |

## Barcelona (`barcelona`)

| 항목 | 현재 위치 | 엔티티 | 이동할 위치 | 방문일 | 조치 | 메모 |
|---|---|---|---|---|---|---|
| Bar Cañete | 장소 — 그 밖의 장소 | restaurant | restaurantsCafes | D3 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Barcelona 역사도심 — Barri Gòtic·Rambla 권역 | (렌더하지 않는다) | walk | attractions.mustVisit | — | **KEEP** | 요약이 없어 카드를 만들지 않는다 |
| Barcelona Modernisme — Eixample 권역 | (렌더하지 않는다) | walk | attractions.mustVisit | — | **KEEP** | 요약이 없어 카드를 만들지 않는다 |
| Barcelona Sants | (렌더하지 않는다) | transport-node | (렌더하지 않는다) | D4 | **KEEP** | 이동 기준점 — 장소 페이지도 카드도 만들지 않는다 |
| Barri Gòtic | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D3 | **KEEP** |  |
| Biblioteca de Catalunya | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D3 | **KEEP** |  |
| Bodega Joan | 장소 — 놓치지 말 것 | restaurant | restaurantsCafes | D2 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Cau Ferrat | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D4 | **KEEP** |  |
| La Paradeta Sagrada Família | 장소 — 놓치지 말 것 | restaurant | restaurantsCafes | D2 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| La Zorra | 장소 — 그 밖의 장소 | restaurant | restaurantsCafes | D4 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| MACBA | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D3 | **KEEP** |  |
| Mercat de la Concepció | 장소 — 그 밖의 장소 | market | restaurantsCafes | D3 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Palau de Maricel | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Sagrada Família | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D2 | **KEEP** |  |
| Sant Pau Recinte Modernista | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D2 | **KEEP** |  |
| Sitges | (렌더하지 않는다) | attraction | attractions.recommended | — | **KEEP** | 요약이 없어 카드를 만들지 않는다 |
| La Paradeta Sagrada Família 점심 | 먹거리 — 카드 | restaurant | restaurantsCafes | D2 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Bodega Joan 저녁 | 먹거리 — 카드 | restaurant | restaurantsCafes | D2 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Bar Cañete 점심 | 먹거리 — 카드 | restaurant | restaurantsCafes | D3 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| La Zorra 점심 (시체스) | 먹거리 — 카드 | restaurant | restaurantsCafes | D4 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| La Paradeta · 제철 해산물 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Bodega Joan · 타파스 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Bar Cañete · 타파스·해산물 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 시장 장보기 · 과일·빵 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| La Zorra · arroz a banda | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 이 지역에 시간을 쓸 가치와 한계 | 개요 | editorial | overview | — | **KEEP** | Overview 의 첫 블록 |
| 꼭 경험할 세 장면 | 개요 | editorial | overview | — | **KEEP** | Overview 안 |
| 생략해도 되는 것 | 개요 | editorial | overview | — | **KEEP** | Overview 안 접이식 |
| 한눈에 보기 | 한눈에 보기 | editorial | overview | — | **MOVE** | '한눈에 보기' 섹션을 없애고 Overview 안 접이식으로 흡수한다 — 예상 체류·확정 일정·추천 이유는 다른 곳에 없다 |
| 여행 전체에서의 역할 | 꼬리말 | editorial | overview | — | **MOVE** | 페이지 하단 꼬리말에서 Overview 로 올린다 |
| 추천 체류 리듬 | 꼬리말 | editorial | overview | — | **MOVE** | 페이지 하단 꼬리말에서 Overview 로 올린다 |
| 이 지역의 날들 — Day 카드 4장 | 일정 | schedule-index | overview | D1,D2,D3,D4 | **MOVE** | 일정 섹션을 없앤다. Day 로 가는 길은 끊지 않는다 — Overview 의 날짜 칩과 카드의 방문일 배지가 같은 Day 를 가리킨다 |
| Occidental Barcelona 1929 | 숙박·생활 | stay | accommodation | D1,D2,D3 | **KEEP** | 확정 |
| 확정 숙소는 Plaça d’Espanya·Hostafrancs 생활권이다. 공항 도착일에는 바로 체크인하고, | 숙박·생활 | stay-note | accommodation | — | **KEEP** |  |
| Day 1은 19:10 공항 도착 뒤 체크인만 한다. 장보기와 산책은 다음 날 아침으로 넘긴다. | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 3박 일정이라 별도 세탁일은 두지 않는다. 객실 설비와 세탁 필요 여부만 체크인 때 확인한다. | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 약국·생필품점은 특정 상호를 고정하지 않는다. 필요할 때 숙소 주변의 현재 영업점을 지도에서 확인한다. | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 시내 일정은 대부분 도보권이다. 피로가 크거나 늦어지면 Hola Barcelona가 적용되는 가장 단순한 메 | 숙박·생활 | local-life | localLife | — | **MOVE** |  |
| BCN T1에서 Aerobús A1 편도권으로 Plaça Espanya까지 이동한 뒤 숙소까지 약 5분 걷는 | 교통 | transport | transport.arrival | — | **KEEP** |  |
| Day 4 아침 체크아웃 뒤 Barcelona Sants의 Hertz 영업소로 이동해 차량을 인수한다. Si | 교통 | transport | transport.departure | — | **KEEP** |  |
| Aerobús A1 편도 (BCN T1 → Plaça Espanya) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D1 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| Plaça Espanya → 숙소 도보 약 5분 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D1 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D2 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 버스/Metro · 현장 재계산 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D2 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 도보 (각 구간이 짧다) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D3 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 공항은 Aerobús A1, 시내는 각자 Hola Barcelona 48h | 교통 — 도시 공공교통 | transport | transport.publicTransport | — | **KEEP** |  |
| Hola Barcelona Travel Card 공식 상품·이용 범위 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Hola Barcelona·Aerobús 결합상품 조건 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Aerobús 공식 노선·정류장·운행시간 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Aerobús 공식 요금·구매 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Barcelona Metro network | 교통 — 교통 지도·공식 자료 | transport-reference | transport.references | — | **MOVE** |  |
| Telefèric de Montjuïc map | 교통 — 교통 지도·공식 자료 | transport-reference | transport.references | — | **MOVE** |  |

## Girona · Empordà (`girona`)

| 항목 | 현재 위치 | 엔티티 | 이동할 위치 | 방문일 | 조치 | 메모 |
|---|---|---|---|---|---|---|
| Calella de Palafrugell | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | — | **KEEP** |  |
| Casa Marieta | 장소 — 그 밖의 장소 | restaurant | restaurantsCafes | — | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Collioure | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D5 | **KEEP** |  |
| Girona Cathedral | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | — | **KEEP** |  |
| Girona 구시가지 — Call·성벽·대성당 권역 | (렌더하지 않는다) | walk | attractions.mustVisit | — | **KEEP** | 요약이 없어 카드를 만들지 않는다 |
| Mercat del Lleó | 장소 — 그 밖의 장소 | market | restaurantsCafes | — | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Onyar 강변 | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | — | **KEEP** |  |
| Pals | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D6 | **KEEP** |  |
| Passeig de la Muralla | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | — | **KEEP** |  |
| Peralada | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Peratallada | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D6 | **KEEP** |  |
| La Zorra 점심 (시체스) | 먹거리 — 카드 | restaurant | restaurantsCafes | D4 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Collioure 점심 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D5 | **DELETE** | 'Collioure' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Sant Feliu de Guíxols 점심 | 먹거리 — 카드 | meal-slot | (day page — 지역 페이지에 두지 않는다) | D6 | **DELETE** | 상호·메뉴가 있는 실제 업소가 아니다 — 하루의 식사 슬롯이다 |
| La Zorra · arroz a banda | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Collioure 시장·생선 점심 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Cadaqués 카페 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 이 지역에 시간을 쓸 가치와 한계 | 개요 | editorial | overview | — | **KEEP** | Overview 의 첫 블록 |
| 꼭 경험할 세 장면 | 개요 | editorial | overview | — | **KEEP** | Overview 안 |
| 생략해도 되는 것 | 개요 | editorial | overview | — | **KEEP** | Overview 안 접이식 |
| 한눈에 보기 | 한눈에 보기 | editorial | overview | — | **MOVE** | '한눈에 보기' 섹션을 없애고 Overview 안 접이식으로 흡수한다 — 예상 체류·확정 일정·추천 이유는 다른 곳에 없다 |
| 여행 전체에서의 역할 | 꼬리말 | editorial | overview | — | **MOVE** | 페이지 하단 꼬리말에서 Overview 로 올린다 |
| 추천 체류 리듬 | 꼬리말 | editorial | overview | — | **MOVE** | 페이지 하단 꼬리말에서 Overview 로 올린다 |
| 이 지역의 날들 — Day 카드 4장 | 일정 | schedule-index | overview | D4,D5,D6,D7 | **MOVE** | 일정 섹션을 없앤다. Day 로 가는 길은 끊지 않는다 — Overview 의 날짜 칩과 카드의 방문일 배지가 같은 Day 를 가리킨다 |
| 바스카라의 B&B | 숙박·생활 | stay | accommodation | D4,D5,D6 | **KEEP** | 확정 |
| 택시 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D4 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 렌터카 · C-32/AP-7 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D4 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| Sitges 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D4 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 렌터카 · 국경 통과 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D5 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| Collioure/Cadaqués 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D5 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 렌터카 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D6 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| GI-682 해안도로 회피 기본 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D6 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| ATM Girona integrated network | 교통 — 교통 지도·공식 자료 | transport-reference | transport.references | — | **MOVE** |  |

## Nice · Côte d'Azur (`nice`)

| 항목 | 현재 위치 | 엔티티 | 이동할 위치 | 방문일 | 조치 | 메모 |
|---|---|---|---|---|---|---|
| Cannes | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D9 | **KEEP** |  |
| Cannes Forville–Suquet–Croisette Walk | 장소 — 그 밖의 장소 | walk | attractions.mustVisit | — | **KEEP** |  |
| Colline du Château (성채 언덕) | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D8 | **KEEP** |  |
| Cours Saleya | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D8 | **KEEP** |  |
| Le Figuier de Saint-Esprit | 장소 — 그 밖의 장소 | restaurant | restaurantsCafes | D9 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Le Rocher — 모나코 구시가지 | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D10 | **KEEP** |  |
| Le Suquet — 칸 구시가지 | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D9 | **KEEP** |  |
| Marché de la Libération | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Marché Forville | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | — | **KEEP** |  |
| Menton (멘통) | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D10 | **KEEP** |  |
| Monaco | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D10 | **KEEP** |  |
| Monaco Rocher–Port–Monte Carlo Walk | 장소 — 그 밖의 장소 | walk | attractions.mustVisit | — | **KEEP** |  |
| NCE T2 | (렌더하지 않는다) | transport-node | (렌더하지 않는다) | D7 | **KEEP** | 이동 기준점 — 장소 페이지도 카드도 만들지 않는다 |
| Nice-Ville | (렌더하지 않는다) | transport-node | (렌더하지 않는다) | D9,D10,D11,D12 | **KEEP** | 이동 기준점 — 장소 페이지도 카드도 만들지 않는다 |
| Nice Old Town–Castle Hill Walk | 장소 — 그 밖의 장소 | walk | attractions.mustVisit | — | **KEEP** |  |
| Promenade des Anglais | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D7,D8 | **KEEP** |  |
| Restaurant & Salon de Thé Béatrice | 장소 — 그 밖의 장소 | restaurant | restaurantsCafes | D11 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Vieux Nice — 구시가지 | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D8 | **KEEP** |  |
| Villa Ephrussi de Rothschild | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D11 | **KEEP** |  |
| 구시가지 점심 — 니스와즈 요리 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D8 | **DELETE** | 'Vieux Nice — 구시가지' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Le Figuier de Saint-Esprit 점심 (WISH-01) | 먹거리 — 카드 | restaurant | restaurantsCafes | D9 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Monaco Port Hercule & Monte-Carlo 점심 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D10 | **DELETE** | 'Monaco' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Menton 저녁 — Le Petit Port | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D10 | **DELETE** | 'Menton (멘통)' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Restaurant & Salon de Thé Béatrice 점심 (WISH-02) | 먹거리 — 카드 | restaurant | restaurantsCafes | D11 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Grasse 점심 & Fragonard 역사공장 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D12 | **DELETE** | 'Grasse' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| 시장 조달 또는 구시가지 골목 식당 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 점심: Le Figuier de Saint-Esprit (WISH-01, 미쉐린 1스타) | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 점심: Monaco (Café de Paris Monte-Carlo 또는 Marché de la Condamine) | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 저녁: Menton (Le Petit Port 등) | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 아침: Villefranche 항구 카페 에스프레소 & 크루아상 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 점심: Restaurant & Salon de Thé Béatrice (WISH-02) | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Grasse 점심 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 이 지역에 시간을 쓸 가치와 한계 | 개요 | editorial | overview | — | **KEEP** | Overview 의 첫 블록 |
| 꼭 경험할 세 장면 | 개요 | editorial | overview | — | **KEEP** | Overview 안 |
| 생략해도 되는 것 | 개요 | editorial | overview | — | **KEEP** | Overview 안 접이식 |
| 한눈에 보기 | 한눈에 보기 | editorial | overview | — | **MOVE** | '한눈에 보기' 섹션을 없애고 Overview 안 접이식으로 흡수한다 — 예상 체류·확정 일정·추천 이유는 다른 곳에 없다 |
| 여행 전체에서의 역할 | 꼬리말 | editorial | overview | — | **MOVE** | 페이지 하단 꼬리말에서 Overview 로 올린다 |
| 추천 체류 리듬 | 꼬리말 | editorial | overview | — | **MOVE** | 페이지 하단 꼬리말에서 Overview 로 올린다 |
| 이 지역의 날들 — Day 카드 6장 | 일정 | schedule-index | overview | D7,D8,D9,D10,D11,D12 | **MOVE** | 일정 섹션을 없앤다. Day 로 가는 길은 끊지 않는다 — Overview 의 날짜 칩과 카드의 방문일 배지가 같은 Day 를 가리킨다 |
| Palais ALZIRA · 12 Rue Verdi | 숙박·생활 | stay | accommodation | D7,D8,D9,D10,D11 | **KEEP** | 확정 |
| 확정 숙소는 Masséna 광장 북서쪽 Verdi 가의 Palais ALZIRA(12 Rue Verdi)다. | 숙박·생활 | stay-note | accommodation | — | **KEEP** |  |
| Day 7 은 16:55 공항 도착이라 첫날은 체크인과 동네 산책까지만 한다. 장보기는 다음 날 아침으로 넘 | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 주방과 세탁기가 있다. 5박 중 세탁 1회를 넣을 수 있고 아침은 숙소에서 해결한다. | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 장보기는 Day 8 아침 Cours Saleya 시장이 기본이다. 슈퍼·약국은 상호를 고정하지 않고 필요할  | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 시내는 도보와 트램이다. 공항 T2 에서 La Carte(보증금 €2)에 Multi voyages 를 충전해 | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 당일치기는 TER 로 돌아온다. Day 10 은 망통에서 20:30 복귀라 낮에 막차 시각을 미리 확인한다. | 숙박·생활 | local-life | localLife | — | **MOVE** |  |
| Day 7 NCE 16:55 도착. 수하물 수령 뒤 트램 2호선으로 숙소 생활권까지 이동해 18:00–19: | 교통 | transport | transport.arrival | — | **KEEP** |  |
| Day 12 08:00 체크아웃. Nice-Ville 역 Hertz 영업소(Avenue Thiers)에서 0 | 교통 | transport | transport.departure | — | **KEEP** |  |
| 렌터카 — BCN T1 반납 12:30 (요청) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D7 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| VY1521 15:30→16:55 (확정 [CONFIRMED]) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D7 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| NCE 도착 후 트램 2호선 이동 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D7 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 니스 시내 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D8 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| TER 왕복 (Nice-Ville ↔ Antibes ↔ Cannes) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D9 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 앙티브 및 칸 시내 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D9 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| TER (Nice-Ville ➔ Monaco-Monte-Carlo ➔ Menton ➔ Nice-Ville) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D10 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 모나코 시내 공공 엘리베이터 및 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D10 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| TER (Nice ➔ Villefranche) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D11 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| Lignes d’Azur 15 (Villefranche ↔ Saint-Jean-Cap-Ferrat) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D11 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| Lignes d’Azur 83 / 82 (Èze ↔ Nice) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D11 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 공동 Multi voyages 12회로 시내·Èze 이동 준비 | 교통 — 도시 공공교통 | transport | transport.publicTransport | — | **KEEP** |  |
| Lignes d’Azur 여행권 요금 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Lignes d’Azur 공항 Tram·Aéro 조건 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Lignes d’Azur 환승·공동 사용법 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Lignes d’Azur 카드 안내 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Lignes d’Azur 공식 노선도 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Lignes d’Azur main lines | 교통 — 교통 지도·공식 자료 | transport-reference | transport.references | — | **MOVE** |  |

## Aix-en-Provence (`aix`)

| 항목 | 현재 위치 | 엔티티 | 이동할 위치 | 방문일 | 조치 | 메모 |
|---|---|---|---|---|---|---|
| Atelier des Lauves | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D13 | **KEEP** |  |
| Bastide du Jas de Bouffan | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Calanques | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D14 | **KEEP** |  |
| Carrières de Bibémus | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Cassis 항구 | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D14 | **KEEP** |  |
| Chez Gilbert | 장소 — 그 밖의 장소 | restaurant | restaurantsCafes | D14 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Cours Mirabeau | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D13 | **KEEP** |  |
| Fort Saint-Jean | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Grasse | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D12 | **KEEP** |  |
| Le Panier | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D15 | **KEEP** |  |
| Marseille | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D15 | **KEEP** |  |
| Montagne Sainte-Victoire · Terrain des Peintres | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Mucem | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D15 | **KEEP** |  |
| Musée Granet | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D13 | **KEEP** |  |
| Notre-Dame de la Garde | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D15 | **KEEP** |  |
| Pâtisserie Weibel | 장소 — 그 밖의 장소 | cafe | restaurantsCafes | — | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| 시장 — Place Richelme · Place des Prêcheurs | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D13 | **KEEP** |  |
| Rotonde | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D12 | **KEEP** |  |
| Saint-Paul-de-Vence | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D12 | **KEEP** |  |
| Vieil Aix — 구시가지 | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D13 | **KEEP** |  |
| Vieux-Port | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D15 | **KEEP** |  |
| Grasse 점심 & Fragonard 역사공장 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D12 | **DELETE** | 'Grasse' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Vieil Aix 구시가지 점심 식사 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D13 | **DELETE** | 'Vieil Aix — 구시가지' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Chez Gilbert 점심 (Cassis 항구) | 먹거리 — 카드 | restaurant | restaurantsCafes | D14 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Vieux-Port 마르세유 항구 점심 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D15 | **DELETE** | 'Vieux-Port' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Grasse 점심 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 시장 조달·카페 Weibel | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 19:30 Coucou 또는 La Brocherie | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Cassis 항구 생선 식당 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 카시스 화이트와인 — 원산지 현지 확인 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Vieux-Port에서 생선·해산물 점심 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Coustellet 시장 점심 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 이 지역에 시간을 쓸 가치와 한계 | 개요 | editorial | overview | — | **KEEP** | Overview 의 첫 블록 |
| 꼭 경험할 세 장면 | 개요 | editorial | overview | — | **KEEP** | Overview 안 |
| 생략해도 되는 것 | 개요 | editorial | overview | — | **KEEP** | Overview 안 접이식 |
| 한눈에 보기 | 한눈에 보기 | editorial | overview | — | **MOVE** | '한눈에 보기' 섹션을 없애고 Overview 안 접이식으로 흡수한다 — 예상 체류·확정 일정·추천 이유는 다른 곳에 없다 |
| 여행 전체에서의 역할 | 꼬리말 | editorial | overview | — | **MOVE** | 페이지 하단 꼬리말에서 Overview 로 올린다 |
| 추천 체류 리듬 | 꼬리말 | editorial | overview | — | **MOVE** | 페이지 하단 꼬리말에서 Overview 로 올린다 |
| 이 지역의 날들 — Day 카드 5장 | 일정 | schedule-index | overview | D12,D13,D14,D15,D16 | **MOVE** | 일정 섹션을 없앤다. Day 로 가는 길은 끊지 않는다 — Overview 의 날짜 칩과 카드의 방문일 배지가 같은 Day 를 가리킨다 |
| Les Toits de Méjanes (Airbnb) | 숙박·생활 | stay | accommodation | D12,D13,D14,D15 | **KEEP** | 확정 |
| 렌터카 — Nice역 09:00 인수 (확정 [CONFIRMED]) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D12 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| A8 고속도로 및 프로방스 국도 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D12 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| Aix 시내 도보 (구시가지 및 북부 아틀리에 도보권) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D13 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 차량 왕복 (Aix ↔ Cassis, A52/A50 고속도로 48km) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D14 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| Cassis Presqu'île 또는 Gorguettes 주차 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D14 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 칼랑크 유람선 (Cassis 항구 출발) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D14 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| TER 기차 왕복 (Aix-en-Provence ↔ Marseille Saint-Charles, 36~45분) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D15 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| RTM 버스 60번 (Vieux-Port ↔ Notre-Dame de la Garde 직통) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D15 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 마르세유 시내 도보 (Vieux-Port ➔ Le Panier ➔ Fort Saint-Jean ➔ Mucem) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D15 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| Aix는 도보, Marseille에서는 같은 카드로 바로 태그 | 교통 — 도시 공공교통 | transport | transport.publicTransport | — | **KEEP** |  |
| Aix en Bus 비접촉 결제·공동 검증 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Aix en Bus 검증·1시간 환승 규칙 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| RTM 비접촉 결제·L50 요금 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| La Métropole Mobilité 노선·시간표 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Aix en Bus line maps | 교통 — 교통 지도·공식 자료 | transport-reference | transport.references | — | **MOVE** |  |

## Luberon (`luberon`)

| 항목 | 현재 위치 | 엔티티 | 이동할 위치 | 방문일 | 조치 | 메모 |
|---|---|---|---|---|---|---|
| Abbaye de Sénanque | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D18 | **KEEP** |  |
| Bonnieux | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Coustellet 생산자 시장 | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D16 | **KEEP** |  |
| Gordes | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D18 | **KEEP** |  |
| Goult | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D16,D17 | **KEEP** |  |
| L’Isle-sur-la-Sorgue | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Lourmarin | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D16 | **KEEP** |  |
| Ménerbes | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D18 | **KEEP** |  |
| Oppède-le-Vieux | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Roussillon · Sentier des Ocres | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D17 | **KEEP** |  |
| Village des Bories | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D18 | **KEEP** |  |
| Gordes 시장 재료 피크닉 점심 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D18 | **DELETE** | 'Gordes' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Les Halles d'Avignon 주변 점심 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D19 | **DELETE** | 'Les Halles' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Fou de Fafa 아비뇽 첫 저녁 | 먹거리 — 카드 | restaurant | restaurantsCafes | D19 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Coustellet 시장 점심 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 시장 재료 피크닉 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Fou de Fafa 또는 Les Cocottes Saint-Louis | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 이 지역에 시간을 쓸 가치와 한계 | 개요 | editorial | overview | — | **KEEP** | Overview 의 첫 블록 |
| 꼭 경험할 세 장면 | 개요 | editorial | overview | — | **KEEP** | Overview 안 |
| 생략해도 되는 것 | 개요 | editorial | overview | — | **KEEP** | Overview 안 접이식 |
| 한눈에 보기 | 한눈에 보기 | editorial | overview | — | **MOVE** | '한눈에 보기' 섹션을 없애고 Overview 안 접이식으로 흡수한다 — 예상 체류·확정 일정·추천 이유는 다른 곳에 없다 |
| 추천 체류 리듬 | 꼬리말 | editorial | overview | — | **MOVE** | 페이지 하단 꼬리말에서 Overview 로 올린다 |
| 이 지역의 날들 — Day 카드 4장 | 일정 | schedule-index | overview | D16,D17,D18,D19 | **MOVE** | 일정 섹션을 없앤다. Day 로 가는 길은 끊지 않는다 — Overview 의 날짜 칩과 카드의 방문일 배지가 같은 Day 를 가리킨다 |
| Domaine des Peyre (후보) | 숙박·생활 | stay | accommodation | D16,D17,D18 | **KEEP** | 미확정 — 확정처럼 보이면 안 된다 |
| 3박 거점은 대중교통 정류장이 아닌 농가 숙소다. Day 16–19의 마을 순회는 예약 렌터카를 정본으로 삼 | 숙박·생활 | stay-note | accommodation | — | **KEEP** |  |
| 식료품과 물은 Day 16 Coustellet에서 확보한다. 농가 도착 뒤 도보 장보기는 전제로 두지 않는다 | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 연료는 절반 아래로 내리지 않는다. 특히 일요일 도착 전과 Avignon 출발 전 유인 주유 가능 시간을 확 | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 석조마을은 외곽 지정 주차장에 세우고 골목으로 진입하지 않는다. Roussillon 오커길에는 먼지에 강한  | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 강풍·폭우·산불 통제가 있으면 오커길과 수도원 접근을 줄이고 숙소 또는 한 마을 일정으로 축소한다. | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 가로등 없는 좁은 도로를 피하려고 일몰 전 귀환을 원칙으로 한다. 늦어지면 마지막 방문지를 생략하고 바로 숙 | 숙박·생활 | local-life | localLife | — | **MOVE** |  |
| Day 16 Aix 체크아웃 뒤 렌터카로 Lourmarin·Coustellet·Goult를 거쳐 농가로 들어 | 교통 | transport | transport.arrival | — | **KEEP** |  |
| Day 19 체크아웃 뒤 렌터카로 Avignon에 이동한다. ZOU! 915·907은 차량 장애 때 일정을  | 교통 | transport | transport.departure | — | **KEEP** |  |
| 렌터카 (Aix ➔ Lourmarin ➔ Coustellet ➔ Goult ➔ Domaine des Peyre) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D16 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 차량 내 수하물 완전 은폐 (가림막 장착, 짐 노출 금지) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D16 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 렌터카 (Domaine des Peyre ↔ Roussillon ↔ Goult ↔ 숙소) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D17 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 황토길 오커 트레일 도보 (30분/50분 코스) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D17 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 렌터카 (Domaine des Peyre ↔ Gordes ↔ Village des Bories ↔ Sénanque ➔ Ménerbes ➔ 숙소) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D18 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 외곽 주차 후 도보 접근 (Parking Bel-Air / Parking Charles de Gaulle) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D18 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 교통권은 사지 않는다 — 렌터카 고정, ZOU!는 차량 장애 때만 | 교통 — 도시 공공교통 | transport | transport.publicTransport | — | **KEEP** |  |
| ZOU! Vaucluse 공식 노선별 시간표 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Pays d’Apt Luberon 관광청 버스 노선 안내 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Pays d’Apt Luberon 관광청 무차량 이동 안내 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| ZOU! Vaucluse 노선별 시간표 | 교통 — 교통 지도·공식 자료 | transport-reference | transport.references | — | **MOVE** |  |

## Avignon · Alpilles (`avignon`)

| 항목 | 현재 위치 | 엔티티 | 이동할 위치 | 방문일 | 조치 | 메모 |
|---|---|---|---|---|---|---|
| Arènes d’Arles | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D22 | **KEEP** |  |
| Arles | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | — | **KEEP** |  |
| Carrières des Lumières | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Cloître Saint-Trophime | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D22 | **KEEP** |  |
| Fondation Vincent van Gogh Arles | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Fou de Fafa | 장소 — 그 밖의 장소 | restaurant | restaurantsCafes | D19 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Glanum | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| La Roquette | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D22 | **KEEP** |  |
| Le Gibolin | 장소 — 그 밖의 장소 | restaurant | restaurantsCafes | D22 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Les Baux-de-Provence | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Les Cocottes Saint-Louis | 장소 — 그 밖의 장소 | restaurant | restaurantsCafes | D20 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Les Halles | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D19,D20 | **KEEP** |  |
| Palais des Papes | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D19,D20 | **KEEP** |  |
| Place du Forum | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Pont du Gard | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D21 | **KEEP** |  |
| Pont Saint-Bénézet | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D20 | **KEEP** |  |
| Rocher des Doms | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D20 | **KEEP** |  |
| Saint-Paul-de-Mausole | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Saint-Rémy-de-Provence | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Théâtre antique | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D22 | **KEEP** |  |
| Uzès Place aux Herbes·구시가지 | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D21 | **KEEP** |  |
| Les Halles d'Avignon 주변 점심 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D19 | **DELETE** | 'Les Halles' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Fou de Fafa 아비뇽 첫 저녁 | 먹거리 — 카드 | restaurant | restaurantsCafes | D19,D20,D21,D22 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| 교황청 광장 비스트로 점심 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D20 | **DELETE** | 'Palais des Papes' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Les Cocottes Saint-Louis 저녁 식사 | 먹거리 — 카드 | restaurant | restaurantsCafes | D19,D20,D21,D22 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Uzès Place aux Herbes 광장 테라스 점심 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D21 | **DELETE** | 'Uzès Place aux Herbes·구시가지' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Le Gibolin 점심 (아를 로케트 지구) | 먹거리 — 카드 | restaurant | restaurantsCafes | D22 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Café Comptoir Abel 부숑 첫 저녁 | 먹거리 — 카드 | restaurant | restaurantsCafes | D23 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Fou de Fafa 또는 Les Cocottes Saint-Louis | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Les Halles 조달 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Place du Forum 점심 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Café Comptoir Abel 저녁 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 이 지역에 시간을 쓸 가치와 한계 | 개요 | editorial | overview | — | **KEEP** | Overview 의 첫 블록 |
| 꼭 경험할 세 장면 | 개요 | editorial | overview | — | **KEEP** | Overview 안 |
| 생략해도 되는 것 | 개요 | editorial | overview | — | **KEEP** | Overview 안 접이식 |
| 한눈에 보기 | 한눈에 보기 | editorial | overview | — | **MOVE** | '한눈에 보기' 섹션을 없애고 Overview 안 접이식으로 흡수한다 — 예상 체류·확정 일정·추천 이유는 다른 곳에 없다 |
| 추천 체류 리듬 | 꼬리말 | editorial | overview | — | **MOVE** | 페이지 하단 꼬리말에서 Overview 로 올린다 |
| 이 지역의 날들 — Day 카드 5장 | 일정 | schedule-index | overview | D19,D20,D21,D22,D23 | **MOVE** | 일정 섹션을 없앤다. Day 로 가는 길은 끊지 않는다 — Overview 의 날짜 칩과 카드의 방문일 배지가 같은 Day 를 가리킨다 |
| La Terrasse du Clocher (후보) | 숙박·생활 | stay | accommodation | D19,D20,D21,D22 | **KEEP** | 미확정 — 확정처럼 보이면 안 된다 |
| 4박 거점은 성벽 안 도보권과 Avignon Centre역 접근성을 우선한다. 렌터카는 숙소 또는 관리주차장 | 숙박·생활 | stay-note | accommodation | — | **KEEP** |  |
| Day 19 체크인 뒤 Les Halles·Place Pie 생활권에서 물과 아침거리를 마련한다. | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| Day 20 성벽 안은 전부 걷고 차량을 꺼내지 않는다. 피로할 때만 무료 도심 셔틀이나 Orizo 단일권을 | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| Day 21은 Uzès·Pont du Gard 렌터카 왕복, Day 22는 Avignon Centre↔Arl | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 차량 안에는 보이는 짐을 남기지 않고, 반납할 때 주유·차량 사진·영수증을 확인한다. | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 성벽 안은 도보 귀환이 기본이다. 늦거나 피로하면 Orizo 실시간 경로를 확인하되, T1이 Avignon  | 숙박·생활 | local-life | localLife | — | **MOVE** |  |
| Day 19 Luberon에서 렌터카로 숙소 주차장 또는 지정 관리주차장에 바로 들어간다. 성벽 안 골목을  | 교통 | transport | transport.arrival | — | **KEEP** |  |
| Day 23 Avignon TGV에서 차량 반납과 10:22 Lyon행 확정 열차 탑승을 처리한다. 반납 방 | 교통 | transport | transport.departure | — | **KEEP** |  |
| 렌터카 (Domaine des Peyre ➔ Avignon 성벽 주차장) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D19 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 아비뇽 시내 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D19 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 아비뇽 구시가지 도보 (성벽 내 압축권) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D20 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 렌터카 (Avignon ↔ Uzès ↔ Pont du Gard ↔ Avignon) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D21 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 외곽 전용 주차장 (Parking Cordeliers / Pont du Gard Rive Gauche) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D21 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| SNCF TER 기차 왕복 (Avignon Centre ↔ Arles, 단 17분 소요) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D22 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 아를 시내 도보 (원형경기장 ➔ 고대극장 ➔ 포룸 광장 ➔ 생트로핌 ➔ 라 로케트) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D22 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 성벽 안은 도보 — Orizo 정기권 없이 TER 두 구간만 분리 구매 | 교통 — 도시 공공교통 | transport | transport.publicTransport | — | **KEEP** |  |
| Orizo 공식 요금표 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Orizo 2026–2027 공식 노선도 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Orizo 공식 P+R·무료 셔틀 안내 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| liO 115 공식 2026년 9월 시간표 목록 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| SNCF TER Avignon–Arles 공식 여정 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Orizo schematic network | 교통 — 교통 지도·공식 자료 | transport-reference | transport.references | — | **MOVE** |  |

## Lyon (`lyon`)

| 항목 | 현재 위치 | 엔티티 | 이동할 위치 | 방문일 | 조치 | 메모 |
|---|---|---|---|---|---|---|
| Annecy 구시가지 | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D26 | **KEEP** |  |
| Bellecour | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D23 | **KEEP** |  |
| Café Comptoir Abel | 장소 — 놓치지 말 것 | restaurant | restaurantsCafes | D23 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Chez Mamie Lise | 장소 — 그 밖의 장소 | restaurant | restaurantsCafes | D26 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Croix-Rousse | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D25 | **KEEP** |  |
| Daniel et Denise | 장소 — 그 밖의 장소 | restaurant | restaurantsCafes | D24 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Fourvière | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D24 | **KEEP** |  |
| Halles de Lyon Paul Bocuse | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D25 | **KEEP** |  |
| Parc de la Tête d'Or | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D25 | **KEEP** |  |
| Vieux Lyon · 트라불 | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D24 | **KEEP** |  |
| Café Comptoir Abel 부숑 첫 저녁 | 먹거리 — 카드 | restaurant | restaurantsCafes | D23,D25 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Vieux Lyon 구시가지 점심 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D24 | **DELETE** | 'Vieux Lyon · 트라불' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Daniel et Denise 정통 부숑 만찬 | 먹거리 — 카드 | restaurant | restaurantsCafes | D24 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Halles Paul Bocuse 미식 점심 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D25 | **DELETE** | 'Halles de Lyon Paul Bocuse' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Chez Mamie Lise 점심 (안시) | 먹거리 — 카드 | restaurant | restaurantsCafes | D26 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Part-Dieu역 점심 & TGV 플랫폼 대기 | 먹거리 — 카드 | meal-slot | (day page — 지역 페이지에 두지 않는다) | D27 | **DELETE** | 상호·메뉴가 있는 실제 업소가 아니다 — 하루의 식사 슬롯이다 |
| Café Comptoir Abel 저녁 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Daniel et Denise 특별 저녁 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Halles Paul Bocuse 2차 리옹 미식 경험 (12:30~14:15 점심) | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| Chez Mamie Lise 점심 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 이 지역에 시간을 쓸 가치와 한계 | 개요 | editorial | overview | — | **KEEP** | Overview 의 첫 블록 |
| 꼭 경험할 세 장면 | 개요 | editorial | overview | — | **KEEP** | Overview 안 |
| 생략해도 되는 것 | 개요 | editorial | overview | — | **KEEP** | Overview 안 접이식 |
| 한눈에 보기 | 한눈에 보기 | editorial | overview | — | **MOVE** | '한눈에 보기' 섹션을 없애고 Overview 안 접이식으로 흡수한다 — 예상 체류·확정 일정·추천 이유는 다른 곳에 없다 |
| 여행 전체에서의 역할 | 꼬리말 | editorial | overview | — | **MOVE** | 페이지 하단 꼬리말에서 Overview 로 올린다 |
| 추천 체류 리듬 | 꼬리말 | editorial | overview | — | **MOVE** | 페이지 하단 꼬리말에서 Overview 로 올린다 |
| 이 지역의 날들 — Day 카드 5장 | 일정 | schedule-index | overview | D23,D24,D25,D26,D27 | **MOVE** | 일정 섹션을 없앤다. Day 로 가는 길은 끊지 않는다 — Overview 의 날짜 칩과 카드의 방문일 배지가 같은 Day 를 가리킨다 |
| Lagrange Aparthotel Lyon Lumière | 숙박·생활 | stay | accommodation | D23,D24,D25,D26 | **KEEP** | 확정 |
| 확정 숙소는 Monplaisir·Sans Souci 생활권의 Lagrange Aparthotel Lyon L | 숙박·생활 | stay-note | accommodation | — | **KEEP** |  |
| 간이주방이 있으므로 체크인 뒤 숙소 주변에서 물·아침거리만 소량 산다. | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| Day 24·25는 같은 비접촉 카드로 두 사람을 검증하고, 환승 때도 같은 매체를 유지한다. | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| Day 26 Annecy는 SNCF TER 별도 왕복이다. TCL 결제나 일일 상한에 포함되지 않는다. | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| Part-Dieu에서는 휴대전화보다 수하물 관리가 우선이다. 플랫폼 확인 뒤 짐을 시야 안쪽에 둔다. | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 관광일에는 TCL 실시간 경로로 가장 단순한 Metro·tram·bus 귀환편을 고른다. Annecy 귀환  | 숙박·생활 | local-life | localLife | — | **MOVE** |  |
| Day 23 Lyon Part-Dieu 도착 뒤 큰 짐을 들고 Metro B→D로 환승하지 않고 택시로 확정 | 교통 | transport | transport.arrival | — | **KEEP** |  |
| Day 27 체크아웃 뒤 택시로 Lyon Part-Dieu에 이동해 13:04 Paris행 확정 TGV를 탄 | 교통 | transport | transport.departure | — | **KEEP** |  |
| 렌터카 반납 (Avignon TGV역 Hertz [CONFIRMED] — 반납 시점 재확인, 일요일 영업 10:00 시작) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D23 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| TGV INOUI 12176 (Avignon TGV 10:22 ➔ Lyon Part-Dieu 11:28, 1등석 확정) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D23 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| Lyon 택시/지하철 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D23 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| TCL 대중교통 (Metro D + Funicular F2 푸니쿨라) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D24 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 리옹 구시가지 및 손 강변 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D24 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| TCL 대중교통 (Metro D ➔ Metro C선 실크 언덕 상행, Croix-Rousse ➔ Bus C13 직통 Halles 이동, Metro B ➔ Metro D 숙소 복귀) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D25 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 크루아루스 실크 공방 및 테트도르 공원 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D25 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| SNCF TER 기차 왕복 (Lyon Part-Dieu ↔ Annecy, 직통 약 1시간 58분) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D26 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 안시 구시가지 및 호숫가 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D26 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| TCL은 같은 비접촉 카드로 두 사람 검증 — 1시간 환승·일일 상한 자동 적용 | 교통 — 도시 공공교통 | transport | transport.publicTransport | — | **KEEP** |  |
| TCL 비접촉 결제·공동 검증·일일 상한 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| TCL Zone 1·2 1회권 공식 요금 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| TCL F2 공식 노선·시간표 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| SNCF TER Lyon–Annecy 공식 운임·운행 안내 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| TCL Lyon·Villeurbanne network | 교통 — 교통 지도·공식 자료 | transport-reference | transport.references | — | **MOVE** |  |

## Paris (`paris`)

| 항목 | 현재 위치 | 엔티티 | 이동할 위치 | 방문일 | 조치 | 메모 |
|---|---|---|---|---|---|---|
| BnF Richelieu | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Bouillon Chartier Montparnasse | 장소 — 그 밖의 장소 | restaurant | restaurantsCafes | D30 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Boulangerie Pichard | 장소 — 그 밖의 장소 | bakery | restaurantsCafes | D28,D31,D35,D38 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Bourse de Commerce — Pinault Collection | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D40 | **KEEP** |  |
| Café du Commerce | 장소 — 그 밖의 장소 | restaurant | restaurantsCafes | D28,D32,D42 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Centre Pompidou | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Giverny | 장소 — 그 밖의 장소 | attraction | attractions.recommended | — | **KEEP** |  |
| Grand Palais | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D28,D33 | **KEEP** |  |
| Latin Quarter | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D29 | **KEEP** |  |
| Le Grand Pan | 장소 — 그 밖의 장소 | restaurant | restaurantsCafes | D34,D41 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Le Marais | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D31,D39 | **KEEP** |  |
| Marché Convention | 장소 — 그 밖의 장소 | market | restaurantsCafes | D29,D36 | **MOVE** | 정본에 food_kind/meal_role 이 있다 — 식당·카페 섹션이 제자리다 |
| Montmartre · South Pigalle | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D40 | **KEEP** |  |
| Montorgueil | 장소 — 그 밖의 장소 | attraction | attractions.recommended | D40 | **KEEP** |  |
| Musée Carnavalet | 장소 — 놓치지 말 것 | attraction | attractions.mustVisit | D39 | **KEEP** |  |
| Musée d'Art Moderne de Paris | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D41 | **KEEP** |  |
| Musée d'Orsay | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D32 | **KEEP** |  |
| Musée de l'Orangerie | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D30 | **KEEP** |  |
| Musée du Louvre | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D35 | **KEEP** |  |
| Musée du Luxembourg | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D29 | **KEEP** |  |
| Musée Guimet | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D41 | **KEEP** |  |
| Musée Gustave Moreau | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D31 | **KEEP** |  |
| Musée Jacquemart-André | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D38 | **KEEP** |  |
| Musée Marmottan Monet | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D36 | **KEEP** |  |
| Musée Picasso Paris | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D39 | **KEEP** |  |
| Musée Rodin | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D32 | **KEEP** |  |
| Notre-Dame de Paris | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D29 | **KEEP** |  |
| Petit Palais | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D33 | **KEEP** |  |
| Versailles | 장소 — 그 밖의 장소 | attraction | attractions.mustVisit | D34 | **KEEP** |  |
| Part-Dieu역 점심 & TGV 플랫폼 대기 | 먹거리 — 카드 | meal-slot | (day page — 지역 페이지에 두지 않는다) | D27 | **DELETE** | 상호·메뉴가 있는 실제 업소가 아니다 — 하루의 식사 슬롯이다 |
| Café du Commerce 15구 브라세리 첫 저녁 | 먹거리 — 카드 | restaurant | restaurantsCafes | D27,D28,D29,D30,D31,D32 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Bouillon Chartier Montparnasse 저녁 | 먹거리 — 카드 | restaurant | restaurantsCafes | D27,D28,D29,D30,D31,D32 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| 9구 누벨 아테네 / 오페라 점심 | 먹거리 — 카드 | meal-slot | (day page — 지역 페이지에 두지 않는다) | D31 | **DELETE** | 상호·메뉴가 있는 실제 업소가 아니다 — 하루의 식사 슬롯이다 |
| 7구 Rue du Bac 점심 식사 | 먹거리 — 카드 | meal-slot | (day page — 지역 페이지에 두지 않는다) | D32 | **DELETE** | 상호·메뉴가 있는 실제 업소가 아니다 — 하루의 식사 슬롯이다 |
| Café du Commerce 동네 저녁 | 먹거리 — 카드 | restaurant | restaurantsCafes | D27,D28,D29,D30,D31,D32 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| 샹젤리제 인근 비스트로 점심 | 먹거리 — 카드 | meal-slot | (day page — 지역 페이지에 두지 않는다) | D33 | **DELETE** | 상호·메뉴가 있는 실제 업소가 아니다 — 하루의 식사 슬롯이다 |
| 베르사유 대운하 인근 점심 식사 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D34 | **DELETE** | 'Versailles' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| Le Grand Pan 15구 비스트로 저녁 | 먹거리 — 카드 | restaurant | restaurantsCafes | D27,D28,D29,D30,D31,D32 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| 레 알 / 몽토르게이 점심 식사 | 먹거리 — 카드 | attraction | (day page — 지역 페이지에 두지 않는다) | D40 | **DELETE** | 'Montorgueil' 은 관광지다. 이 카드는 그 장소에서 먹는다는 하루의 식사 슬롯이지 식당이 아니다 |
| 이에나 / 윌슨 대로변 점심 식사 | 먹거리 — 카드 | meal-slot | (day page — 지역 페이지에 두지 않는다) | D41 | **DELETE** | 상호·메뉴가 있는 실제 업소가 아니다 — 하루의 식사 슬롯이다 |
| Le Grand Pan 파리 15박 고별 만찬 | 먹거리 — 카드 | restaurant | restaurantsCafes | D41 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Café du Commerce 15구 마지막 점심 | 먹거리 — 카드 | restaurant | restaurantsCafes | D42 | **MERGE** | 장소 카드와 같은 대상 — 식당 카드 하나로 합친다 |
| Palais Royal 주변 점심 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 송별 저녁 (상향) — 장소 검토 중 | 먹거리 — 목록 | regional-dish | restaurantsCafes.regionalDishes | — | **KEEP** | 업소가 아니라 '무엇을 먹는가'. 카드가 아니라 목록으로 남긴다 |
| 이 지역에 시간을 쓸 가치와 한계 | 개요 | editorial | overview | — | **KEEP** | Overview 의 첫 블록 |
| 꼭 경험할 세 장면 | 개요 | editorial | overview | — | **KEEP** | Overview 안 |
| 생략해도 되는 것 | 개요 | editorial | overview | — | **KEEP** | Overview 안 접이식 |
| 한눈에 보기 | 한눈에 보기 | editorial | overview | — | **MOVE** | '한눈에 보기' 섹션을 없애고 Overview 안 접이식으로 흡수한다 — 예상 체류·확정 일정·추천 이유는 다른 곳에 없다 |
| 여행 전체에서의 역할 | 꼬리말 | editorial | overview | — | **MOVE** | 페이지 하단 꼬리말에서 Overview 로 올린다 |
| 추천 체류 리듬 | 꼬리말 | editorial | overview | — | **MOVE** | 페이지 하단 꼬리말에서 Overview 로 올린다 |
| 이 지역의 날들 — Day 카드 16장 | 일정 | schedule-index | overview | D27,D28,D29,D30,D31,D32 | **MOVE** | 일정 섹션을 없앤다. Day 로 가는 길은 끊지 않는다 — Overview 의 날짜 칩과 카드의 방문일 배지가 같은 Day 를 가리킨다 |
| 78 Rue de Lourmel (파리 15구) | 숙박·생활 | stay | accommodation | D27,D28,D29,D30,D31,D32 | **KEEP** | 확정 |
| 15박 확정 숙소는 15구 78 Rue de Lourmel이다. 9월 24일 Gare de Lyon 도착과  | 숙박·생활 | stay-note | accommodation | — | **KEEP** |  |
| 9월 24–27일과 10월 5–8일은 개별 승차권, 9월 28일–10월 4일만 Navigo Weekly al | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| Metro·Train·RER 단일권과 Bus·Tram 단일권은 서로 다른 상품이다. 환승 체계를 섞어 한 여 | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 장기체류 장보기·세탁·약국은 숙소 반경 생활권에서 해결하고, 박물관일에는 귀가 동선을 추가 관광으로 늘리지  | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 10월 9일은 체크아웃·가벼운 점심·공식 택시로 CDG 이동만 한다. Weekly를 소진하려고 RER B로  | 숙박·생활 | local-life | localLife | — | **MOVE** | 숙박과 생활을 두 섹션으로 가른다 |
| 야간에는 환승 수가 적고 밝은 출구로 연결되는 경로를 우선한다. 행사·경마 귀환 때 혼잡하면 다음 열차를 기 | 숙박·생활 | local-life | localLife | — | **MOVE** |  |
| Day 27 Paris Gare de Lyon 도착 뒤 큰 짐을 들고 Metro로 환승하지 않고 택시로 15 | 교통 | transport | transport.arrival | — | **KEEP** |  |
| Day 42에는 14:00 이전 공식 택시로 15구 숙소에서 CDG Terminal 1으로 출발한다. Par | 교통 | transport | transport.departure | — | **KEEP** |  |
| TGV INOUI 6618 (Lyon Part-Dieu 13:04 ➔ Paris Gare de Lyon 15:00, 1등석 13호차 356·357 확정 [CONFIRMED]) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D27 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| Paris Gare de Lyon ➔ 15구 숙소 택시 이동 (약 35분 소요) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D27 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| Tootbus / Big Bus 파리 시티투어 버스 (2층 파노라마 풀 루프 2시간 15분) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D28 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 메트로 8호선 (Lourmel ↔ Concorde/Champs-Élysées) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D28 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 메트로 10호선 (La Motte-Picquet ➔ Mabillon/Odéon) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D29 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 파리 좌안(Left Bank) 역사문화 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D29 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 메트로 8호선 (Lourmel ↔ Concorde) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D30 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 파리 우안 고전 예술·정원 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D30 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 메트로 12호선 / 8호선 (15구 ↔ 9구 / 마레) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D31 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 누벨 아테네 및 마레 지구 패션 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D31 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 메트로 8호선 / 12호선 (Lourmel ➔ Solférino) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D32 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 파리 7구 오르세·로댕 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D32 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 메트로 8호선 / 9호선 (15구 ↔ 샹젤리제/알마) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D33 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 몽테뉴 대로 및 센 강변 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D33 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| RER C선 (Javel역 ↔ Versailles Château Rive Gauche역, 직통 25분) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D34 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 베르사유 광활한 영지 도보 (궁전 ➔ 정원 ➔ 대운하 ➔ 트리아농) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D34 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 메트로 8호선 + 1호선 (Lourmel ➔ Palais Royal - Musée du Louvre) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D35 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 루브르 박물관 회랑 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D35 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 메트로 9호선 (La Muette역) 또는 32번 버스 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D36 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 파리 16구 라늘라 정원 및 파시 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D36 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 메트로 10호선 (Porte d'Auteuil역) + France Galop 공식 무료 셔틀버스(Navette) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D37 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 파리롱샹 경마장 보행 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D37 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 메트로 8호선 + 9호선 (Lourmel ➔ Miromesnil) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D38 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 8구 오스만·몽소 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D38 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 메트로 8호선 (Lourmel ↔ Saint-Sébastien - Froissart / Saint-Paul) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D39 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 마레 지구 17세기 귀족 저택 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D39 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 메트로 8호선 / 1호선 / 12호선 (15구 ↔ 레 알 ↔ 몽마르트르 Abbesses) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D40 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 몽마르트르 언덕 돌계단 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D40 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 메트로 9호선 / 6호선 (15구 ↔ Iéna / Trocadéro) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D41 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 이에나 광장 및 트로카데로 도보 | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D41 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 파리 공식 택시 (15구 ➔ CDG 터미널 1 정액제 약 60분, €65) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D42 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| 아시아나항공 OZ502 (CDG 터미널 1 19:10 ➔ ICN 터미널 2 10/10 14:10, 확정 · 48G·48H) | 교통 — 자유문자열 목록 | transport | transport.publicTransport | D42 | **DELETE** | Day 가 정본이다. 같은 문자열이 Day 페이지 '이동' 접이식에 이미 있고 지역 페이지가 그것을 복사해 왔다 |
| Weekly는 9/28–10/4 한 번만 — 앞뒤는 각자 개별권, CDG는 확정 택시 | 교통 — 도시 공공교통 | transport | transport.publicTransport | — | **KEEP** |  |
| Île-de-France Mobilités 2026 공식 요금 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Navigo Weekly 공식 유효기간·매체 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Metro‑Train‑RER Ticket 공식 범위·환승 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Paris Region Airports Ticket 공식 조건 | 교통 — 공식 출처 접이식 | transport-reference | transport.references | — | **MOVE** | 참고 링크는 Transport 맨 아래 References 로 모은다 |
| Île-de-France Mobilités Metro map | 교통 — 교통 지도·공식 자료 | transport-reference | transport.references | — | **MOVE** |  |

## 식당·카페 카드 완결성

| 지역 | 장소 | 종류 | 사진 | 소개 | 장문 | 공홈 | 지도 | 메뉴 | 가격 | 가격확인일 | 운영시간 | 예약 | 방문일 |
|---|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|:-:|:-:|---|
| aix | Chez Gilbert | restaurant | **X** | O | O | O | O | O | O | — | O | O | D14 |
| aix | Pâtisserie Weibel | cafe | **X** | O | O | O | O | O | O | — | O | O | **없음** |
| avignon | Fou de Fafa | restaurant | **X** | O | O | O | O | O | O | — | O | O | D19 |
| avignon | Le Gibolin | restaurant | **X** | O | O | O | O | O | O | — | O | O | D22 |
| avignon | Les Cocottes Saint-Louis | restaurant | **X** | O | O | O | O | **X** | O | — | O | O | D20 |
| barcelona | Bar Cañete | restaurant | **X** | O | O | O | O | **X** | O | 2026-08-21 | O | O | D3 |
| barcelona | Bodega Joan | restaurant | **X** | O | O | O | O | O | O | 2026-08-21 | O | O | D2 |
| barcelona | La Paradeta Sagrada Família | restaurant | **X** | O | O | O | O | **X** | O | 2026-08-21 | O | O | D2 |
| barcelona | La Zorra | restaurant | **X** | O | O | O | O | O | O | 2026-08-21 | O | O | D4 |
| barcelona | Mercat de la Concepció | market | O | O | O | O | O | **X** | O | 2026-08-21 | O | O | D3 |
| girona | Casa Marieta | restaurant | **X** | O | O | O | O | O | O | — | O | O | **없음** |
| girona | Mercat del Lleó | market | O | O | O | O | O | **X** | **X** | — | O | O | **없음** |
| lyon | Café Comptoir Abel | restaurant | **X** | O | O | O | O | O | O | — | O | O | D23 |
| lyon | Chez Mamie Lise | restaurant | **X** | O | O | O | O | **X** | O | — | O | O | D26 |
| lyon | Daniel et Denise | restaurant | O | O | O | O | O | O | O | — | O | O | D24 |
| nice | Le Figuier de Saint-Esprit | restaurant | **X** | O | O | O | O | O | O | — | O | O | D9 |
| nice | Restaurant & Salon de Thé Béatrice | restaurant | **X** | O | O | O | O | O | O | — | O | O | D11 |
| paris | Bouillon Chartier Montparnasse | restaurant | O | O | O | O | O | O | O | — | O | O | D30 |
| paris | Boulangerie Pichard | bakery | **X** | O | O | O | O | **X** | O | — | O | O | D28,D31,D35,D38 |
| paris | Café du Commerce | restaurant | O | O | O | O | O | O | O | — | O | O | D28,D32,D42 |
| paris | Le Grand Pan | restaurant | **X** | O | O | O | O | O | O | — | O | O | D34,D41 |
| paris | Marché Convention | market | O | O | O | O | O | **X** | O | — | O | O | D29,D36 |

## 장소로 잇지 못한 사진

판정의 정본은 `data/images/place-aliases.json` 하나다.
`unmapped` 는 0 이어야 한다 — 별칭표에 없는 placeId 가 들어오면
빌드가 선다. `unregistered` 는 실재하지만 명부에 없는 장소로,
장소 승격이 있어야 화면에 올라간다.

| placeId | imageId | 판정 | 이유 |
|---|---|---|---|
| `cadaques` | girona-cadaques-01 | unregistered | Cadaqués 는 명부에 없다. Day 5 동선에 있으나 장소로 승격되지 않았다 |
| `tossa-de-mar` | girona-tossa-01 | unregistered | Tossa de Mar 는 명부에 없다 |
| `sant-feliu-de-guixols` | girona-sant-feliu-01 | unregistered | Day 6 점심 슬롯이 가리키는 곳인데 장소로 승격되지 않았다 |
| `pantheon-paris` | paris-pantheon-01 | unregistered | 팡테옹은 명부에 없다. 라탱 지구 장소와 별개 건물이라 임의로 잇지 않는다 |
| `jardin-du-luxembourg` | paris-luxembourg-01 | unregistered | 뤽상부르 공원은 명부에 없다. 뤽상부르 미술관과 다른 대상이다 |
| `marche-monge` | paris-marche-monge-01 | unregistered | 몽주 시장은 명부에 없다 |
| `palais-royal` | paris-palais-royal-01 | unregistered | 팔레 루아얄은 명부에 없다 |
| `passages-couverts` | paris-passages-01 | unregistered | 갤러리 비비엔 등 아케이드는 명부에 없다 |
| `marche-des-enfants-rouges` | paris-enfants-rouges-01 | unregistered | 앙팡 루주 시장은 명부에 없다. 마레 장소와 별개 대상이다 |
| `canal-saint-martin` | paris-canal-saint-martin-01 | unregistered | 생마르탱 운하는 명부에 없다 |
| `seine` | paris-seine-01 | unregistered | 센강변 부키니스트는 명부에 없다 |
