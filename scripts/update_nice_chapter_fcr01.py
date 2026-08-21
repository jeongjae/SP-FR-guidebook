from pathlib import Path

path = Path("source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md")
content = path.read_text(encoding="utf-8")

# 1. Update self-guide entries before ## 음식·시장·카페·생활체험
new_self_guides = """#### Monaco Rocher–Port–Monte Carlo Walk {{grade:essential|필수}}

> **요약**: 절벽 위 왕궁 마을에서 위병 교대식을 보고 랑프 마요르 돌계단을 내려와 에르퀼 항구 F1 서킷을 지나 몬테카를로 카지노 광장으로 이어지는 모나코 핵심 도보 코스.

- **상세 가이드**: [Monaco Walk 전체 코스 안내 보기](../places/monaco-walk.html)

---
#### Le Figuier de Saint-Esprit {{grade:essential|필수}}

> **Editor's Verdict**: 앙티브 옛 성벽 안쪽 무화과나무 중정에서 즐기는 미쉐린 1스타 파인다이닝. 셰프 크리스티앙 모리세의 오징어 먹물 카넬로니와 알피유 양등심 구이.

- **체류/가격**: 90–105분 · **점심 포뮬러 €55~€75** (일요일 12:15 점심 영업, 사전 예약 필수)
- **상세 가이드**: [Le Figuier de Saint-Esprit 전체 가이드 보기](../places/le-figuier-de-saint-esprit.html)

---
#### Restaurant & Salon de Thé Béatrice {{grade:essential|필수}}

> **Editor's Verdict**: 에프뤼시 드 로스차일드 분홍빛 저택 테라스에서 빌프랑슈 만을 내려다보며 즐기는 로맨틱 오션뷰 런치 & 살롱 드 테.

- **체류/가격**: 60–80분 · **단품/플레이트 €24~€48** (12:00–15:00 런치, 빌라 입장객 전용)
- **상세 가이드**: [Restaurant Béatrice 전체 가이드 보기](../places/restaurant-beatrice.html)

---
#### Villa Ephrussi de Rothschild {{grade:priority|우선추천}}

> **Editor's Verdict**: 생장캅페라 반도 절경 위의 벨 에포크 팔라초와 9개 테마 정원, 20분 간격 클래식 음악 분수 쇼가 어우러진 리비에라 정원 예술의 절정.

- **체류/요금**: 2–2.5시간 · **€17** (연중무휴 10:00–18:00, 15번 버스 연계)
- **상세 가이드**: [Villa Ephrussi de Rothschild 전체 가이드 보기](../places/villa-ephrussi-de-rothschild.html)"""

content = content.replace(
"""#### Monaco Rocher–Port–Monte Carlo Walk {{grade:essential|필수}}

> **요약**: 절벽 위 왕궁 마을에서 위병 교대식을 보고 랑프 마요르 돌계단을 내려와 에르퀼 항구 F1 서킷을 지나 몬테카를로 카지노 광장으로 이어지는 모나코 핵심 도보 코스.

- **상세 가이드**: [Monaco Walk 전체 코스 안내 보기](../places/monaco-walk.html)""",
new_self_guides
)

# 2. Update Food section
old_food_section = """## 음식·시장·카페·생활체험

- **니스 요리의 문법**: 500년간 이어진 사보이 통치의 영향으로 파스타·올리브 오일 같은 이탈리아계 식재료가 프랑스 식문화와 섞여 있다.
- **반드시 먹을 세 가지**:
  1. **Socca (소카)**: 병아리콩 가루로 만든 부드럽고 바삭한 갈레트로, 화덕에서 나오자마자 손으로 찢어 후추를 뿌려 로제 와인과 함께 먹는다. (Chez Pipo, 셰 테레자 추천)
  2. **Pissaladière (피살라디에르)**: 두툼한 빵 반죽 위에 캐러멜라이즈한 양파, 안초비, 블랙 올리브를 올린 타르트다. 페이스트리 도우는 피하는 것이 현지식이다.
  3. **Salade Niçoise (니수아즈 샐러드)**: 익힌 감자나 그린빈 없이 오직 토마토, 피망, 오이 등 생채소와 참치, 안초비, 올리브, 달걀만 들어가는 것이 정본이다. 감자가 들어가면 관광객용 변형이다.
- **식당 전략**:
  - **Acchiardo**: Vieux Nice의 오랜 가족식당으로 Petits Farcis(속을 채운 채소 구이)와 소고기 스튜 라비올리가 잘 알려져 있다. 영업은 {{fact:acchiardo.hours}} — 휴무 {{fact:acchiardo.closed}} 라 주말 저녁에는 쓸 수 없다.
  - **La Table Alziari**: 올리브유와 제철 생선 요리 (€35–55, 권장). 속 편한 저녁을 원할 때 알맞다."""

new_food_section = """## 음식·시장·카페·생활체험

니스와 코트다쥐르의 식문화는 500년간 이어진 사보이 공국의 역사와 지중해 해안선이 빚어낸 **독립적인 미식 체계(Cuisine Nissarde)**를 자랑한다. 프로방스 내륙의 허브·마늘 문화와 이탈리아 리구리아의 올리브유·파스타 전통이 결합되어 프랑스 여타 지역과 뚜렷이 구별된다.

### 1. 니스·코트다쥐르 대표 추천 음식 (Regional Recommended Foods)
물리적 식당과 독립된 이 지역 고유의 핵심 음식 목록이다:

1. **Socca (소카)**: 병아리콩(Pois chiches) 가루와 올리브유를 섞어 대형 구리 팬에서 장작 화덕으로 구워낸 니스 최고의 길거리 음식. 겉은 바삭하고 속은 부드러우며 갓 구웠을 때 굵은 흑후추를 듬뿍 뿌려 먹는다. (Best: Cours Saleya, Chez Pipo / Day 08)
2. **Pissaladière (피살라디에르)**: 빵 도우 위에 장시간 캐러멜라이징한 양파, 앤초비(또는 피살라 페이스트), 니스 블랙 올리브(Cailletier)를 올려 구운 짭조름한 전통 타르트. (Best: Vieux Nice 제과점 / Day 08, 11)
3. **Salade Niçoise (살라드 뉘수아즈)**: 완숙 생토마토, 니스 올리브, 앤초비 또는 참치, 삶은 달걀, 래디시, 피망 등 신선한 생채소에 올리브유와 소금으로만 맛을 낸 정통 샐러드. (익힌 감자나 껍질콩이 들어가면 변형)
4. **Pan Bagnat (팡 바냐)**: '적신 빵'이라는 뜻의 둥근 통밀 빵 샌드위치. 니스와즈 샐러드 재료를 채워 올리브유와 토마토 즙이 빵에 촉촉이 배어들게 먹는 피크닉의 정석. (Best: Promenade 해변 벤치 / Day 08, 11)
5. **Petits Farcis (프티 파르시)**: 둥근 주키니, 토마토, 가지, 피망의 속을 파내고 다진 고기와 허브, 파르메산 치즈를 채워 오븐에 노릇하게 구워낸 가정식 요리. (Best: Chez Acchiardo / Day 08)
6. **Daube Niçoise (도브 뉘수아즈)**: 소고기를 프로방스 레드 와인, 토마토, 말린 포르치니(Cèpes)와 함께 뭉근하게 끓여낸 스튜로, 수제 라비올리와 함께 곁들여 먹는다.
7. **Tourte de Blettes (투르트 드 블레트)**: 근대 잎, 사과, 잣, 건포도, 파르메산 치즈를 달콤하게 배합하여 파이 크러스트 속에 구워낸 니스의 독특한 전통 디저트/전채.
8. **Barbajuan (바르바주앙)**: 근대(또는 시금치), 리코타 치즈, 리크를 반죽에 싸서 바삭하게 튀겨낸 모나코·리비에라 전통 전채. (Best: Monaco Marché de La Condamine / Day 10)
9. **Tarte au Citron de Menton (망통 레몬 타르트)**: 풍부한 일조량의 망통 특산 IGP 레몬으로 만든 상큼하고 진한 전통 레몬 커스터드 타르트. (Best: Menton 구시가지 / Day 10)

### 2. 희망 vs 추천 업장 체계 (WISH vs RECOMMENDED)
일정에 연결된 주요 식당과 카페는 여행자 직접 지정(WISH)과 편집부 추천(RECOMMENDED)으로 구분하여 운영한다:

- **[희망][Primary] Le Figuier de Saint-Esprit (Antibes)**: 앙티브 구시가지 미쉐린 1스타 파인다이닝 (셰프 크리스티앙 모리세). 일요일 런치(12:15~13:30)에 방문하여 무화과나무 안뜰에서 오징어 먹물 카넬로니와 알피유 양등심 런치 코스 만끽 (Day 09).
- **[희망][Primary] Restaurant & Salon de Thé Béatrice (Saint-Jean-Cap-Ferrat)**: 로스차일드 저택 내부 및 빌프랑슈 만 전망 테라스 런치. 샐러드 베아트리스와 제철 생선 요리, 살롱 드 테 디저트 (Day 11).
- **[희망 후보·확인필요] Salon de Thé - Île de Beauté (Nice Port Lympia)**: 니스 림피아 항구의 살롱 드 테 후보로 여행자 확정 대기 중 (Status: USER_CONFIRMATION_REQUIRED).
- **[추천][Primary/Backup] Chez Acchiardo (Nice Vieux Nice)**: 1927년부터 4대째 이어오는 구시가지 정통 니스 가정식. 프티 파르시와 도브 라비올리 명가. ({{fact:acchiardo.hours}} / {{fact:acchiardo.closed}} 월–금 영업, 주말 휴무 주의 / Day 08 백업).
- **[추천][Primary] Marché de La Condamine (Monaco)**: 모나코 서민과 로컬들의 중심 시장. 즉석 바르바주앙(Barbajuan), 수제 파스타, 포카치아를 가볍게 맛보기 최적 (Day 10 점심).
- **[추천][Primary] Le Petit Port (Menton)**: 망통 구항구 테라스의 신선한 해산물 및 지중해 생선 구이 전문점 (Day 10 저녁).
- **[추천][Primary] Chez Pipo & Chez Thérésa (Nice)**: 갓 구운 바삭하고 고소한 소카(Socca)의 전설적인 명소 (Day 08).

### 3. 시장과 식재료 문화
- **Cours Saleya (니스)**: 화~일 06:00~13:30 꽃과 식품시장. 즉석 소카와 과일 조달.
- **Marché de la Libération (니스)**: 화~일 06:00~13:00 현지인 중심 대형 생활시장. 치즈, 건과일, 차량 간식 조달 (Day 11).
- **Marché Provençal (앙티브)**: 화~일 06:00~13:00 구시가지 성벽 안 아케이드 시장 (Day 09)."""

content = content.replace(old_food_section, new_food_section)

# 3. Update Day 9 section
old_day9 = """## 6. Day 3 — 9월 6일 일요일
### Cannes 당일치기: 시장, 구시가지, 항구, Croisette

*   **오늘의 결론**: Cannes의 어촌 역사와 리조트의 화려함을 순서대로 걸으며 Nice와 다른 도시의 결을 읽는다.
*   **상태**: **고정** | 날씨 의존성: 유
*   **첫 행동·첫 예약**: 08:40 Nice-Ville역 열차 탑승 | **마지막 귀가**: 17:30 Nice 귀환 및 저녁

**피로도 4/5.**

#### 핵심 행동 (최대 3개)
1. **Marché Forville**: 칸의 전통 생활시장을 돌아보며 현지인들의 식탁 분위기 체험.
2. **Le Suquet 골목길**: 칸이 시작된 언덕 마을을 올라 전망대에서 크루아제트 대로 조망.
3. **Vieux-Port & Croisette 산책**: 호화 요트 항구를 거쳐 붉은 카펫과 종려나무 해변길 걷기.

#### 실행 시간표
| 시간 | 일정 | 실행 포인트 |
|---|---|--- |
| 08:40 전후 | Nice-Ville → Cannes TER | 당일 운행 재확인 |
| 09:30–10:20 | **Marché Forville** | [Cannes Forville–Suquet–Croisette Walk](../../places/cannes-walk.html) 시작. **개보수 중 — 기존 홀 주소로 가면 헛걸음이다** ({{fact:marche-forville.note}}) |
| 10:20–11:20 | **Le Suquet** | 골목·전망 |
| 11:20–12:00 | **Vieux-Port** | 항구 보행 |
| 12:00–13:00 | 가벼운 점심 | 시장식 또는 간단한 해산물 |
| 13:00–15:40 | Palais·Croisette·해변 선택 | 쇼핑연장은 삭제 가능 |
| 16:00 전후 | Nice 귀환 | 저녁 전 숙소휴식 |
#### 오늘 지도
{{VISUAL:VIS-MAP-043|type=map|status=linked|strategy=execution-map}}

#### 식사 및 카페
*   **점심**: Forville 시장 주변 캐주얼 해산물 또는 간단한 포장 요리 - 예산 €15–30/인
*   **저녁**: Nice 복귀 후 가벼운 로컬 레스토랑 또는 자가 조리 - 예산 €20–40/인"""

new_day9 = """## 6. Day 3 — 9월 6일 일요일
### 앙티브 요새마을, Le Figuier 미쉐린 런치 & 칸 당일치기

*   **오늘의 결론**: 앙티브 구시가지와 시장을 산책한 뒤 무화과나무 중정에서 미쉐린 1스타 런치를 즐기고, 오후에 칸의 르 쉬케와 크루아제트를 압축 조망한 뒤 니스에 조기 복귀한다.
*   **상태**: **고정** | 날씨 의존성: 유
*   **첫 행동·첫 예약**: 08:15 숙소 출발 (08:28 TER 앙티브행) | **마지막 귀가**: 17:30~18:00 Nice 귀환 및 저녁

**피로도 3/5.**

#### 핵심 행동 (최대 3개)
1. **Vieil Antibes & Marché Provençal (08:50~12:00)**: 앙티브 성벽길 산책, 활기찬 프로방스 전통시장과 포르 보방 조망.
2. **Le Figuier de Saint-Esprit 런치 (12:15~14:00)**: 크리스티앙 모리세 셰프의 미쉐린 1스타 파인다이닝 점심 (WISH-01).
3. **Cannes 압축 관람 (14:45~16:50)**: TER 이동 후 르 쉬케(Le Suquet) 전망대와 크루아제트 대로 산책 후 17:00 TER 니스 복귀.

#### 실행 시간표
| 시간 | 일정 | 실행 포인트 |
|---|---|--- |
| 08:15–08:46 | Nice-Ville → Antibes TER | 08:28 TER 탑승 (18분 소요, 앙티브역 하차) |
| 08:50–12:00 | **앙티브 구시가지 & 프로방스 시장** | 성벽길(Promenade Amiral de Grasse), Marché Provençal, 피카소 미술관 외관 |
| 12:15–14:00 | **Le Figuier de Saint-Esprit 점심** | **[희망][Primary]** 미쉐린 1스타 무화과나무 중정 런치 (사전예약 12:15 필수) |
| 14:15–14:35 | Antibes → Cannes TER | 14:15 TER 탑승 (12분 소요, 칸 역 하차) |
| 14:45–15:45 | **Le Suquet 구시가지 언덕** | 옛 어촌 자갈길 등정, 성채 광장에서 칸 만 파노라마 조망 |
| 15:50–16:50 | **Boulevard de la Croisette** | 팔레 데 페스티발 외관 및 야자수 해안 산책로 벤치 휴식 |
| 17:00–17:30 | Cannes → Nice-Ville TER | 칸 역 복귀 및 니스행 TER 탑승 |
| 17:35–18:00 | 숙소 복귀 및 완충 휴식 | 12 Rue Verdi 숙소 복귀 |
#### 오늘 지도
{{VISUAL:VIS-MAP-043|type=map|status=linked|strategy=execution-map}}

#### 식사 및 카페
*   **점심 (앙티브)**: **Le Figuier de Saint-Esprit** (14 Rue Saint-Esprit, WISH-01 미쉐린 1스타 런치 코스 €55~€118)
*   **저녁 (니스)**: Nice 복귀 후 숙소 근처 가벼운 카페 식사 또는 숙소 자가 조리 - 예산 €15–30/인"""

content = content.replace(old_day9, new_day9)

# 4. Update Day 11 section
old_day11 = """## 8. Day 5 — 9월 8일 화요일
### Nice 생활·회복일: 시장, 사진미술관 선택, 세탁과 해변

*   **오늘의 결론**: 장거리 당일치기 후 누적된 피로를 니스 생활밀착형 동선으로 해소하고, 다음 날 차량 이동을 준비한다.
*   **상태**: **자유** | 날씨 의존성: 무
*   **첫 행동·첫 예약**: 09:20 Marché de la Libération 생활시장 장보기 | **마지막 귀가**: 자가 조리 저녁

**피로도 2/5.**

#### 핵심 행동 (최대 3개)
1. **Marché de la Libération**: 주민들이 애용하는 부엌 시장에서 저녁 조리용 식재료와 차량 간식 구매.
2. **Musée de la Photographie**: 화요일 유일하게 운영되는 사진미술관 선택적 관람 (Matisse, Chagall 휴관).
3. **숙소 휴식 및 세탁**: 빨래방 이용 및 짐 재분류, 다음 날 렌터카 서류 등 확인.

#### 실행 시간표
| 시간 | 일정 | 실행 포인트 |
|---|---|--- |
| 07:30–08:15 | Jason 선택 러닝 또는 늦잠 | 다리 피로가 있으면 완전휴식 |
| 09:20–10:30 | **Marché de la Libération** | 실제 장보기·9/9 차량간식 준비 |
| 10:45–12:30 | **Musée de la Photographie Charles Nègre 선택** | 화요일 10:00–18:00 운영. 피로하면 생략 |
| 12:45–13:30 | 가벼운 점심 | 시장재료 또는 숙소권 점심 |
| 13:30–15:30 | 숙소 휴식·세탁 | 체크아웃·렌터카 서류·짐 재분류 |
| 15:30–17:30 | 선택 모듈 | Promenade 카페, 해변산책, Julia 수영 중 1개 |
| 17:30–18:30 | 9/9 준비 | 물·간식·면허·예약번호·주유/보험 확인 |
| 19:30–21:00 | Nice 마지막 저녁 | 과식하지 않고 이동일 전 음주 최소화 |
#### 오늘 지도
{{VISUAL:VIS-MAP-045|type=map|status=linked|strategy=execution-map}}

#### 식사 및 카페
*   **점심**: Libération 시장 조달 푸드 또는 숙소권 간단식 - 예산 €10–20/인
*   **저녁**: **숙소 자가 조리** (시장 식재료 활용한 건강식 및 피로 회복)"""

new_day11 = """## 8. Day 5 — 9월 8일 화요일
### Nice 생활·회복일: 리베라시옹 시장, 로스차일드 빌라 런치, 프롬나드 해변 휴식

*   **오늘의 결론**: 아침 리베라시옹 로컬 시장 후 생장캅페라 로스차일드 저택에서 여유로운 오션뷰 런치를 즐기고, 오후 프롬나드 해변 휴식과 세탁으로 익일 프로방스 렌터카 이동을 완벽히 준비한다.
*   **상태**: **자유** | 날씨 의존성: 무
*   **첫 행동·첫 예약**: 08:45 Marché de la Libération 장보기 | **마지막 귀가**: 18:00 숙소 귀환 및 렌터카 준비

**피로도 2/5.**

#### 핵심 행동 (최대 3개)
1. **Marché de la Libération (08:45~10:15)**: 니스 시민들의 부엌 시장에서 과일·치즈 탐방 및 아침 에스프레소.
2. **Villa Ephrussi & Restaurant Béatrice 런치 (11:00~14:30)**: 분홍빛 벨 에포크 팔라초와 9개 테마 정원 산책, 테라스 점심 (WISH-02).
3. **숙소 휴식·세탁 & 프롬나드 산책 (15:30~18:00)**: 빨래방/세탁기 이용, 프롬나드 해변 벤치 휴식, 9/9 렌터카 인수 서류 최종 점검.

#### 실행 시간표
| 시간 | 일정 | 실행 포인트 |
|---|---|--- |
| 08:45–10:15 | **Marché de la Libération** | 로컬 식재료 탐방, 과일·차량간식 구매, Gare du Sud 카페 |
| 10:30–11:00 | Nice → Saint-Jean-Cap-Ferrat | 15번 버스 탑승 (약 25분, Passable / Villa Ephrussi 하차) |
| 11:00–12:15 | **Villa Ephrussi de Rothschild** | 베아트리스 남작부인의 팔라초 및 9개 테마 정원 산책 (€17) |
| 12:15–13:45 | **Restaurant Béatrice 점심** | **[희망][Primary]** 저택 테라스에서 빌프랑슈 만 조망 런치 (WISH-02) |
| 13:45–14:30 | **에프뤼시 분수 음악쇼** | 20분 간격 클래식 음악 분수 관람 후 15번 버스 니스 복귀 |
| 15:30–17:30 | **숙소 휴식 & Promenade des Anglais** | 세탁기 가동, 짐 정리, 프롬나드 해변 벤치 휴식 및 카페 |
| 18:00–19:00 | **9/9 프로방스 렌터카 준비** | 09:00 Hertz 니스역 인수 동선·서류·보험 확인 및 조기 취침 |
#### 오늘 지도
{{VISUAL:VIS-MAP-045|type=map|status=linked|strategy=execution-map}}

#### 식사 및 카페
*   **아침**: Marché de la Libération 신선 과일 및 에스프레소
*   **점심**: **Restaurant & Salon de Thé Béatrice** (Villa Ephrussi 내 테라스, WISH-02 샐러드·생선요리 €24~€45)
*   **저녁**: **숙소 자가 조리** 또는 숙소 인근 가벼운 니스식 샐러드·파니니 - 예산 €10–20/인"""

content = content.replace(old_day11, new_day11)

path.write_text(content, encoding="utf-8")
print("Updated 06_Nice_Cote_d_Azur_v2.0.md successfully")
