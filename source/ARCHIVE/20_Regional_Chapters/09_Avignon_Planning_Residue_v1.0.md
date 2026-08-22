---
title: "아비뇽·아를·위제스·퐁뒤가르 — 계획 단계 자료 (통폐합 시 분리)"
chapter: 09
version: "1.0"
archived_at: "2026-08-23"
archived_from: "source/CURRENT/20_Regional_Chapters/09_Avignon_Alpilles_Pont_du_Gard_v2.0.md"
reason: "Avignon Region 통폐합 — 최종 여행가이드가 아니라 그 결정을 만든 과거 자료"
---

# 아비뇽·아를·위제스·퐁뒤가르 계획 단계 자료

여기 있는 것은 **폐기된 글이 아니라 결정의 근거**다. 2026-08-23 Avignon 지역
통폐합에서 챕터 원고 밖으로 옮겼다.

최종 가이드는 "무엇을 검토했는가"가 아니라 "무엇을 실제로 할 것인가"를 보여준다.
4박 체류와 렌터카 반납, TER/TGV 이동이 정돈된 뒤에는 후보지 채점표와 제외 후보
목록이 현장에서 혼선을 일으킬 수 있다.

결정이 뒤집히거나 대체안이 필요할 때 여기를 먼저 읽는다.

## 1. 생략해도 되는 것 및 후보 판단표

- **옮겨온 곳**: 챕터 §생략해도 되는 것
- **현재 정본**: `data/decisions.json` · `source/ASSETS/91_Place_Registry_v1.0.md` · Day 정본
- **분리 사유**: 제외 후보 평가는 기획 단계의 판정표다. 독자 화면에는 실제로 갈 장소만 남긴다.

| 장소·경험 | 판단 | 이유 |
|---|---|--- |
| **Collection Lambert** | 대체 | 현대미술 관심이 매우 강할 때만 선택적 방문 |
| **LUMA · Alyscamps · 고대박물관** | 선택 | Arles 핵심 동선(원형경기장·고대극장·포룸·생트로핌·라로케트)에 모두 더하면 과밀하므로 제외 |
| **Nîmes 과다 체류** | 주의 | Pont du Gard와 연계하되 2시간 핵심 유적(Arènes·Maison Carrée) 관람 후 15:45 Hard Stop 엄수 |

## 2. 한눈에 보기 — 우선순위·권역·소요시간 매트릭스

- **옮겨온 곳**: 챕터 §한눈에 보기, §놓치면 아쉬운 선택, §하루를 완성하는 네 가지 선택
- **현재 정본**: `data/place-facts.json` (duration, price) · Day 카드 (확정 일정) · 장소 카드 요약
- **분리 사유**: 장소 메타데이터, 우선순위 매트릭스, 장소 카드가 다중 중복 나열됨.

| 장소 | 등급 | 기획 단계 추천 이유 |
|---|---|--- |
| Palais des Papes | **필수** | 아비뇽의 도시정체성과 권력구조를 이해하는 핵심 |
| Les Halles | **필수** | 관광도시 안의 실제 식문화와 장보기 |
| Rocher des Doms | **우선 추천** | Rhône·Pont·Villeneuve를 한 번에 조망 |
| Pont Saint-Bénézet | **우선 추천** | 도시·강·교역의 관계를 상징 |
| Rue des Teinturiers | **우선 추천** | 축제도시 이전의 수공업·생활골목 |
| Uzès 구시가지·Place aux Herbes | **우선 추천** | 금요일에도 실행 가능한 지역도시와 생활광장 경험 |
| Pont du Gard | **필수** | 로마공학과 자연경관의 결합 |
| Arles·Arènes·Théâtre antique | **필수** | 로마유적과 생활도시가 분리되지 않는 핵심 당일치기 |
| Saint-Trophime / Fondation van Gogh | **우선 추천** | 중세와 반 고흐 중 관심사에 따라 선택 |
| Les Baux·Saint-Rémy·Glanum | 대체 | Arles를 완전히 교체하는 Alpilles 선택안 |
| Carrières des Lumières | 대체 | Alpilles 선택안에서 악천후·몰입형 전시 선호 시 |
| Petit Palais | 대체 | 비·폭염 시 중세회화 60분 |

## 3. 추천 체류 리듬 — 구버전 흐름도 및 식사표

- **옮겨온 곳**: 챕터 §추천 체류 리듬
- **현재 정본**: `data/daily-cards/day-19.json` ~ `day-23.json`
- **분리 사유**: Day SOT와 중복되는 ASCII 다이어그램 및 식사 일정표.

```text
[구버전 ASCII 동선 초안]
9/16 Luberon 체크아웃 → Avignon 체크인·생활권 적응
        ↓
9/17 Uzès 구시가지 → Pont du Gard → Nîmes (Arènes·Maison Carrée) → Avignon TGV Hertz 반납
        ↓
9/18 Arles (TER): Arènes → Théâtre antique → Forum → Saint-Trophime → La Roquette
        ↓
9/19 Avignon (도보): Les Halles → Palais des Papes → Rocher des Doms → Pont Saint-Bénézet
        ↓
9/20 Avignon TGV → Lyon Part-Dieu
```

| Day | 날짜 | 점심 | 저녁 |
|---|---|---|--- |
| 19 | 9/16 수 | 이동 중 간단식 | 아비뇽 첫 저녁 |
| 20 | 9/17 목 | Pont du Gard 간단한 점심 | 아비뇽 복귀 후 저녁 |
| 21 | 9/18 금 | Arles 구시가지 비스트로 | 아비뇽 |
| 22 | 9/19 토 | **Les Halles** | **프로방스 마지막 저녁** |
| 23 | 9/20 일 | 이동 중 또는 TGV | 리옹 도착 후 |

## 4. 구역별 역사·도시 구조 상세 분석

- **옮겨온 곳**: 챕터 §구역별 이해와 숙소 생활권
- **현재 정본**: `source/CURRENT/30_Places/palais-des-papes.md` · `pont-saint-benezet.md` · `uzes.md` · `pont-du-gard.md` · `arles.md`
- **분리 사유**: 아비뇽 유수기 68년 역사 해설, 론 강 다리 흥망사, 수력 인프라 분석을 개별 장소 정본으로 분리.

- 1309~1377년 68년간 가톨릭 교황청이 아비뇽에 머물며 인구가 5,000명에서 3만 명으로 급증. 성벽 4.5km와 유럽 최대 고딕 궁전은 종교·행정·방어의 인프라였음.
- 생베네제 다리는 건설 당시 리옹과 지중해를 잇는 론 강의 유일한 석조 교량이었으며, 17세기 붕괴 후 4개 아치만 잔존.
- 우제스 수원지-퐁뒤가르-님으로 이어지는 50km 고대 로마 수로 시스템은 고대 토목공학과 식민도시 번영의 축.

## 5. 숙소 권역 비교표 및 평가 가중치표

- **옮겨온 곳**: 챕터 §동네·숙소 생활권 비교, §14.1 숙소 평가 기준
- **현재 정본**: `data/region-essentials.json` (성벽 안 도보권 및 Gare Centre 접근성 기준)
- **분리 사유**: 기획 단계의 권역 비교표와 가중치 매트릭스 분리.

### 숙소 생활권 비교표

| 생활권 | 성격 | 장점 | 단점 | 권고 |
|---|---|---|---|:---:|
| **Porte Saint-Michel–Gare Centre–Corps Saints** | 남쪽 성벽·역·생활권 | 차량진입·TGV 연결·도보관광·식당 균형 최고 | Palais까지 15–20분 | **1순위 (추천 권역)** |
| **Carmes–Université·동쪽 성벽권** | 생활형·카페·Rue des Teinturiers | 조용한 골목, 주방형 숙소, 슈퍼 접근 | Gare Centre와 TGV 이동 한 단계 추가 | **2순위** |
| **Vernet–Oratoire 서부** | 조용한 고급주거·갤러리 | Palais·Pont·식당 접근, 비교적 차분 | 숙박비 높고 주방형 적음 | 2순위 |
| **Place Pie–Halles** | 시장·식당·중심 | 아침시장과 구시가지 이동 최고 | 야간소음·차량진입·주차 불편 | 조건부 |
| **Palais·Horloge 바로 주변** | 관광중심 | 핵심명소 접근 최고 | 관광혼잡·식당가격·주차·소음 | 후순위 |
| **Avignon TGV·Courtine** | 교통·신개발 | 차량반납·열차 편리 | 성벽도시 생활감 약함 | 이동편의 특화 |
| **Le Pontet·Montfavet** | 외곽 생활권 | 주차·대형슈퍼·가격 | 4박 도심관광에 매일 이동 필요 | 비추천 |

### 숙소 평가 가중치표

| 평가항목 | 가중치 |
|---|---:|
| 확정 가능한 안전한 주차·차량진입 | 25 |
| 성벽도시 도보 접근 | 20 |
| 주방·냉장고·세탁 | 15 |
| 야간 귀가·생활권 | 15 |
| 객실 크기·엘리베이터·냉방 | 10 |
| Avignon TGV 반납동선 | 10 |
| 비용 | 5 |

## 6. 실제 숙소 후보 비교 및 채점표 (2026-08 기획안)

- **옮겨온 곳**: 챕터 §14.2 실제 숙소 후보, §14.2b 추가 후보, §14.3 최종 선택순서, §14.4 계획예산

| 후보 | 위치·형태 | 핵심 강점 | 주의·확인사항 | 적합도 |
|---|---|---|---|---: |
| **Hôtel Le Magnan** | 성벽 안 남부, 호텔 | 조용한 정원, Gare Centre 5분권, 보안주차 | 주방·세탁 없음, 주차 조기예약 | **91/100** |
| **Résidence Les Cordeliers** | 성벽 안 남동, 아파트호텔 | kitchenette, 세탁, Gare Centre 약 600m | 안뜰주차 당일 배정 | 89/100 |
| **Apart’Hôtel Sainte-Marthe** | 동쪽 성벽 밖, 아파트호텔 | 완비 kitchenette, 유료주차, 세탁실, 슈퍼 | Palais까지 도보 15–20분 | 88/100 |
| **Avignon Grand Hotel** | 남쪽 성벽 밖·역 앞, 4성급 | 35㎡ 넓은 객실, 24시간 프런트, TGV 연결 | kitchenette 없음, 가격 상단 | 87/100 |
| **Novotel Avignon Centre** | 남서 성벽 밖, 4성급 | 보안 지하주차, 역·구시가지 접근 | 주방 없음, 비즈니스 호텔 | 85/100 |
| **ibis budget Avignon Centre** | 서남 성벽 밖, 예산호텔 | 유료주차 가능, 24시간 프런트, 예산 절감 | 객실 협소, 장기체류감 약함 | 78/100 |
| **Hôtel Cloître Saint-Louis** | 성벽 안 남부, 역사호텔 | 16세기 수도원 안뜰 정원, Gare Centre 접근 | 주차·리노베이션 상태 재확인 | 조건부 |
| **Appartements des Teinturiers** | Rue des Teinturiers, 아파트 | 완전 아파트형, 시장·식당 도보 접근 | 구옥 엘리베이터·냉방 확인 | 추가 후보 |
| **Dream Avignon** | Carnot–Carmes, 아파트 그룹 | 생활권+주방+구시가지 조합 | 물건별 설비 편차 큼 | 추가 후보 |
| **Hôtel Mercure Pont d'Avignon** | Palais des Papes 옆, 호텔 | 교황청 접근 최상, 지하주차장 연결 | 관광객 밀집, 생활형 불리 | 추가 후보 |

## 7. 배제한 대안 루트 및 Alpilles 후보

- **옮겨온 곳**: 챕터 §생략해도 되는 것, §핵심 셀프가이드

### Alpilles 대체 당일치기 (Les Baux / Saint-Rémy / Glanum / Carrières des Lumières / Saint-Paul-de-Mausole)
Arles 대신 알피유 산맥 석회암 요새 마을(Les Baux), 로마 유적(Glanum), 반 고흐 요양원(Saint-Paul-de-Mausole)을 선택할 수 있는 대체 코스로 기획되었으나, 본 일정은 Arles 로마·중세 유적 집중으로 확정되어 대체안으로 분리 보존.

## 8. 프랑스 일반 도로 및 지역 교통 매뉴얼

- **옮겨온 곳**: 챕터 §도착·출발·지역 내 교통 (아비뇽 주차, 렌터카 반납 실무, 셔틀버스)
- **분리 사유**: 일반 교통 및 주차 매뉴얼은 Prepare 및 Day SOT로 수렴.

- 아비뇽 성벽 내부는 일방통행과 보행자 통제가 많으므로 성벽 안 노상주차를 피하고 관리주차장(Centre Gare, Jean Jaurès, Halles 등) 이용.
- 9/17 렌터카 반납 시 D999/N100 도로 경유하여 아비뇽 TGV역 인근에서 만유 주유 후 P0 Parking Loueurs 입차, 18:30 이전 반납 완료.
- 9/20 TGV 이용 시 Avignon Centre역에서 TER 'La Virgule'(4분 소요) 또는 택시를 이용해 TGV역으로 이동.
