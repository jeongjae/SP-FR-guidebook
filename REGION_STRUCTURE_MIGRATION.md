# REGION_STRUCTURE_MIGRATION — 지역 가이드 구조 이관

FCR-02. 지역 페이지를 **탐색 화면**으로 되돌린다. 하루의 정본은 Day 이고,
장소·식당의 정본은 Place 다. 지역은 그 둘을 가리키는 색인이지 사본이 아니다.

이 문서는 무엇을 어디로 옮겼는지의 기록이다. 수치의 정본은
`REGION_CONTENT_AUDIT.md`(이관 전 기준선)와
`build/region_structure_check.py`(이관 후 상태)다.

---

## 1. 구조

```
개편 전                              개편 후
────────────────────────────────    ────────────────────────────────
개요                                 개요        overview
한눈에 보기                            └ 한눈에 보기 · 역할 · 리듬 · 이해하는 층 (접이식)
장소  ├ 놓치지 말 것                  볼거리      attractions
      └ 그 밖의 장소                   ├ 꼭 가야 할 곳      MUST VISIT
일정  (Day 카드 43장)                  └ 권할 만한 곳      RECOMMENDED
먹거리 ├ 카드 (하루의 식사 슬롯)        식당·카페   food
      └ 목록 (지역 음식)                ├ 식당 카드 (사진·방문일·메뉴·가격·지도·공홈)
숙박·생활                              └ 이 지역에서 먹는 것 (접이식)
교통  ├ 자유문자열 목록                숙소        stay
      ├ 도착/출발                      생활권      life
      ├ 도시 공공교통                  교통        transport
      └ 교통 지도·공식 자료              ├ 도착과 출발
여행 전체에서의 역할 (꼬리말)             ├ 도시 교통
추천 체류 리듬 (꼬리말)                  └ 공식 자료와 재확인
```

상위 섹션은 여섯 개다. 순서는 `build/region_structure_check.py` 가 잠근다.

---

## 2. 분류 규칙 — 제목이 아니라 엔티티

`…점심`·`…저녁`·`Lunch`·`Dinner` 라는 **제목**으로 식당을 판정하지 않는다.
`source/CURRENT/30_Places/<slug>.md` 의 `food_kind`·`meal_role` 이 정본이다.

| 정본 값 | 엔티티 | 섹션 |
|---|---|---|
| `food_kind: RESTAURANT / CAFE / BAKERY / MARKET / FOOD_HALL / WINE_BAR` | restaurant · cafe · bakery · market · food-hall · wine-bar | 식당·카페 |
| `meal_role: PRIMARY / BACKUP` (food_kind 없음) | restaurant | 식당·카페 |
| `meal_role: MARKET / SELF_CATERING` | market | 식당·카페 |
| `kind: walk` | walk | 볼거리 |
| `kind: node` | transport-node | 렌더하지 않는다 |
| 그 외 | attraction | 볼거리 |

구현은 `model.Place.entity_type`. 지역 페이지는
`Region.must_visit` · `Region.recommended` · `Region.food_places` 만 읽는다.

**시장을 식당·카페에 넣은 이유.** 시장은 관광지이기도 하다. 그러나 명부가
이미 `meal_role: MARKET` 을 주고 있고 66끼 식사 슬롯 감사도 시장을 끼니로
세어 왔다. 한 쪽을 골라야 한다면 정본이 이미 말하고 있는 쪽을 따른다.
카드에는 `시장` 배지가 붙어 식당과 구분된다.

**'먹거리' 에 있던 관광지 17건은 카드가 아니었다.** `구시가지 점심 —
니스와즈 요리`(vieux-nice)·`Gordes 시장 재료 피크닉 점심`(gordes) 처럼
**관광지에서 먹는다는 하루의 식사 슬롯**이다. 업소가 아니므로 지역 페이지의
식당 카드가 되지 않는다 — 그 정보의 정본은 Day 페이지의 시간표다.

---

## 3. 옮긴 것과 옮긴 곳

| 없앤 것 | 어디로 갔나 | 잃은 것 |
|---|---|---|
| 장소 섹션의 식당·카페 22곳 | 식당·카페 섹션 (카드가 더 두꺼워졌다) | 없음 |
| 먹거리 섹션의 식사 슬롯 카드 24장 | Day 페이지 시간표 (원래 정본) | 없음 |
| 일정 섹션 (Day 카드 43장) | 개요의 날짜 칩 + 카드의 방문일 배지 | 없음 — 같은 Day 를 가리킨다 |
| 한눈에 보기 섹션 | 개요 안 접이식 | 없음 |
| 여행 전체에서의 역할 · 추천 체류 리듬 (꼬리말) | 개요 안 접이식 | 없음 |
| 교통 자유문자열 목록 86줄 | Day 페이지 '이동' 접이식 (원래 정본) | 없음 |
| 우천 전환 (꼬리말) | 개요 | 없음 |

**한눈에 보기를 지우지 않고 접은 이유.** 그 표에만 있는 값이 있다 —
예상 체류시간, 확정 일정 시각, '이 가이드북이 추천하는 이유'. 화면 밀도만
낮추고 내용은 남긴다. 콘텐츠 스키마 가드(`content_guard`)도 배포본에서
`한눈에 보기` 라는 말을 찾는다.

**일정 섹션을 없애면서 길을 끊지 않았다.** 개요의 날짜 칩이 그 지역의 모든
Day 로, 카드의 방문일 배지가 그 장소를 실제로 들르는 Day 로 간다. 날짜
문자열은 템플릿에 박지 않는다 — `render.place_visits()` 가 daily-card 의
stop 에서 계산하므로 일정이 바뀌면 배지도 바뀐다.

---

## 4. 원고에만 있던 것을 화면으로

개편 전 지역 페이지는 챕터 원고의 여섯 층(verdict · scenes · skip ·
overview · role · rhythm)만 썼다. **나머지는 배포본 어디에도 없었다.**
`Barcelona 카페 5곳`·`슈퍼마켓 사용 원칙`·`저배출구역(ZBE)`·`시체스 주차`를
배포본에서 찾으면 한 건도 나오지 않았다.

`build/promote_regions.py` 에 다섯 층을 더했다.

| 층 | 원고 앵커 | 지역 페이지 |
|---|---|---|
| `context` | 지역을 이해하는 다섯 개의 층 | 개요 접이식 |
| `neighborhoods` | 구역별 이해와 숙소 생활권 · 동네별 성격과 숙소 적합성 | 숙소 — 묵을 만한 동네 |
| `stay_budget` | 숙소 예산과 확정 숙소 | 숙소 — 예산과 확인 기준 |
| `transport_deep` | 도착·출발·지역 내 교통 | 교통 심화 |
| `food_culture` | 음식·시장·카페·생활체험 | 식당·카페 심화 |

원고는 하위 주제에도 h2 를 쓴다. 그래서 "다음 h2" 가 아니라
**스키마가 정한 척추 제목과 하위 앵커**를 경계로 잘라낸다.

**폐기된 숙소 후보는 올리지 않는다.** 숙소가 확정된 지역
(barcelona · girona · nice · aix · lyon · paris)에서는 `N순위: 호텔이름` ·
`숙소 후보` · `숙소 선택 결론` 절을 렌더에서 뺀다. 후보 주소·전화·요금을
확정으로 믿고 이동하는 것이 이 프로젝트 최악의 사고다. 원고에는 그대로
남는다 — 그게 기록이다. 동네 순위(`7.1 Dreta de l'Eixample … 1순위`)는
남긴다. 그건 '어디에 묵을 만한가' 라는 Accommodation 의 답이다.

---

## 5. 검증

```
python3 build/region_audit.py            # 이관 기준선 (개편 전 규칙)
python3 build/region_structure_check.py  # 개편 후 상태 + 식당 완결성 리포트
python3 build/site.py                    # 빌드가 구조 가드를 함께 돈다
```

구조 가드가 보는 것 — 여섯 섹션과 순서 · 볼거리 안의 식당(0) · 식당 안의
관광지(0) · 되살아난 옛 섹션(0) · 잘못된 Day 참조(0) · 중복 교통 블록(0) ·
끊어진 내부 링크(0). 식당 완결성은 **빌드를 세우지 않는다** — 사진이 없다는
것은 구조가 틀렸다는 뜻이 아니라 아직 못 구했다는 뜻이라, 세어서 보여 준다.

---

## 6. 남은 7개 지역

템플릿과 모델은 이미 8개 지역 전부에 적용됐다. 구조는 같은 코드가 만든다 —
**지역 전용 분기는 코드에 0개다.** 남은 것은 콘텐츠다.

FCR-02B(안정화)에서 Aix SOT 충돌·Nice 원고 결손·사진 슬러그 어긋남·연속 표
열 손실을 정리했다. 상세는 `FCR02B_STABILIZATION_QA.md`.

| 지역 | 식당·카페 | 사진 | 가격 사실 | region-essentials | 비고 |
|---|---:|---:|---:|:-:|---|
| barcelona | 5 | 1 | 5 | O | 파일럿 완료 |
| girona | 2 | 1 | 0 | · | |
| nice | 2 | 0 | 0 | O | FCR-02B 에서 보강 |
| aix | 2 | 0 | 0 | · | 확정 숙소로 원고 갱신 완료 |
| luberon | 0 | — | — | O | 사 먹는 구간이 아니다 (자가취사) |
| avignon | 3 | 0 | 0 | O | `les-halles` 를 FOOD_HALL 로 승격 검토 |
| lyon | 3 | 1 | 0 | O | `halles-de-lyon-paul-bocuse` 승격 검토 |
| paris | 5 | 3 | 0 | O | |

지역 하나당 할 일은 넷이다 — ① `region-essentials` 추가 ② 조사 CSV 의
`price_range` 를 place-facts 로 이관 ③ 신원이 확인된 사진만
`photo-queue.json` 에 넣고 `scripts/add_commons_photo.py` 실행
④ 세 검사가 0 을 유지하는지 확인.

## 7. 검사 세 개

```
python3 build/region_structure_check.py   구조 · 분류 · 방문일 · 링크 · 완결성
python3 build/media_lookup_check.py       사진이 조용히 사라지지 않는가
python3 build/table_loss_check.py         붙어 있는 표가 열을 잃지 않는가
```

앞의 둘은 `build/site.py` 가 함께 돈다. 셋 다 8개 지역 전수로 돈다 —
Barcelona 에서만 통과하는 검사는 없다.
