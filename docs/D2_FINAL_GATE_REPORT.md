# D2 최종 게이트 보고서

**작성:** 2026-08-18 · 출발 **2026-08-29** (D-11) · 커밋 `43f1f107`
**원칙:** 완결성보다 안전성. 못 채운 것은 "미확인"으로 정직하게 뒀다.

---

## 1. 가드 6종 + 커버리지

```
G1  PASS  방문 요일 vs 휴관일      0건 · 검사 221 / 후보 906
          건너뜀 87(closed 값 없음) + 498(주간 휴무 없음) + 10(방문일 판정 실패) + 73(회피 서술)
          판정 출처 literal 70 · day-heading 36 · place-days 115 · hours 여집합 2
G1c PASS  Day 헤딩 ↔ itinerary     0건
G1e WARN  closed 판정 불가         6곳 (원고 참조 17줄)
G2  PASS  하드코딩 (확정 등급)      0건 · 검사 318 / 전체 8260 (3.8%)
G2  FAIL  하드코딩 (전체 코퍼스)    371건 · 검사 7095 / 전체 8260 (85.9%)
G3  WARN  필수·우선추천 항목 참조   91건 · 검사 109 / 전체 160 (68.1%) · 08-22 실패 승격
G4  PASS  같은 사실 다중 하드코딩   0건 · 검사 52
G5  PASS  확정 결정 잔재            0건 · 검사 23
G6  WARN  신선도 (기준 08-29)       0건 · 검사 582 · unreachable 82건은 전화 대상
빌드 335p · HIG 검사 통과 (터치타깃·글자크기·명암비·안전영역·리플로·뷰포트)
```

**T5 기준 "G1~G5 ALL GREEN" 은 G2 전체 코퍼스에서 충족하지 못했다.** 371건은 확정 등급
101곳 **밖**의 서술(대안·참고·아카이브성 표)에 남은 하드코딩이고, 확정 등급 범위(G2 grade)는
0건이다. 이 371건을 토큰으로 옮기려면 그만큼의 값을 조사해야 하는데 이번 세션은 조사 범위가
아니었다 — **없는 값을 채운 척하는 것보다 남겨 두는 편이 안전하다.**

## 2. 정보 충족률 — 대리지표

진단 v2.0 의 49.1% 는 사람이 191곳·124곳을 판정한 수치라 재현할 수 없다. 아래는 기계로
셀 수 있는 대리지표다.

| confidence | 건수 | 뜻 |
|---|---:|---|
| official | 408 | 공식 소스 확인 |
| editorial | 32 | 이 가이드북의 편집 판단 (체류시간 등) |
| secondary | 27 | 2차 출처·파생 |
| unverified | 33 | 미확인 |
| unreachable | 82 | 공식 확인 불가 — 전화 대상 |

장소 160곳 · 확정 등급 109곳.
**렌더되는 `{{fact:}}` 토큰 373건 중 "미확인"으로 뜨는 것은 0건이다** — 값이 없는 토큰은
원고에서 지웠기 때문이고, 지운 항목은 §4 에 있다.

**95% 기준은 충족하지 못했다.** `getting_there`·`price_range`·`address` 가 여전히 비어 있고,
이 셋은 S2 가 P0(closed·hours·booking)만 조사했기 때문에 남은 것이다.

---

## 3. ★ 현장 확인 목록 — 날짜순

**여행 중 실제로 쓰는 목록이다.** 값이 확인되지 않은 것만 모았다 — 확인된 것은 여기 없다.
대상 62곳 · 115건.

| Day | 날짜 | 지역 | 장소 | 전화 | 확인할 것 |
|---:|---|---|---|---|---|
| 2 | 08/30(일) | Barcelona·Sitges | Gràcia 저녁 산책 | — | closed(전화 문의) · hours(전화 문의) · booking(전화 문의) |
| 2 | 08/30(일) | Barcelona·Sitges | La Paradeta Sagrada Família | +34 934 500 191 | booking(전화 문의) |
| 3 | 08/31(월) | Barcelona·Sitges | Bar Cañete | +34 932 703 458 | hours(전화 문의) |
| 3 | 08/31(월) | Barcelona·Sitges | Barri Gòtic | — | closed(전화 문의) · hours(전화 문의) · booking(전화 문의) |
| 3 | 08/31(월) | Barcelona·Sitges | Biblioteca de Catalunya | +34 93 270 23 00 | hours(전화 문의) · closed(전화 문의) · booking(전화 문의) |
| 3 | 08/31(월) | Barcelona·Sitges | CEM Joan Miró | +34 934 234 350 | closed(전화 문의) · booking(전화 문의) |
| 3 | 08/31(월) | Barcelona·Sitges | Llibreria Finestres | +34 933 840 809 | booking(전화 문의) |
| 3 | 08/31(월) | Barcelona·Sitges | Mercat de la Concepció | — | booking(전화 문의) |
| 3 | 08/31(월) | Barcelona·Sitges | 고딕지구 핵심 산책 (Plaça del Rei–Carrer | — | closed(전화 문의) · hours(전화 문의) · booking(전화 문의) |
| 4 | 09/01(화) | Barcelona·Sitges | Museu del Cau Ferrat | +34 93 894 03 64 | booking(전화 문의) |
| 4 | 09/01(화) | Barcelona·Sitges | Museu de Maricel | +34 93 894 03 64 | booking(전화 문의) |
| 4 | 09/01(화) | Barcelona·Sitges | 시체스 2시간 30분 핵심 동선 | — | closed(전화 문의) · hours(전화 문의) · booking(전화 문의) |
| 4 | 09/01(화) | Girona·Collioure | Casa Marieta | +34 972 201 016 | closed(전화 문의) |
| 4 | 09/01(화) | Girona·Collioure | Call (유대인 지구) | +34 972 216 761 | closed(미확인) · hours(미확인) · booking(미확인) |
| 4 | 09/01(화) | Girona·Collioure | Onyar 강변 | +34 972 010 001 | closed(미확인) · hours(미확인) · booking(미확인) |
| 4 | 09/01(화) | Girona·Collioure | 성벽 (Passeig de la Muralla) | +34 972 010 001 | booking(미확인) |
| 5 | 09/02(수) | Girona·Collioure | Cadaqués | +34 972 258 315 | closed(미확인) |
| 6 | 09/03(목) | Girona·Collioure | La Roca (Peratallada) | +34 972 634 172 / +34 606 911 243 | hours(전화 문의) · closed(미확인) |
| 6 | 09/03(목) | Girona·Collioure | Pals | +34 972 637 380 | booking(미확인) |
| 6 | 09/03(목) | Girona·Collioure | Peratallada | +34 872 987 030 | closed(미확인) · hours(미확인) · booking(미확인) |
| 8 | 09/05(토) | Nice·Côte d'Azur | La Table Alziari | +33 4 93 80 34 03 | closed(미확인) |
| 14 | 09/11(금) | Aix·Marseille | Cassis 항구 | +33 4 28 01 01 03 | closed(미확인) |
| 14 | 09/11(금) | Aix·Marseille | Le Panier | — | closed(미확인) · hours(미확인) · booking(미확인) |
| 15 | 09/12(토) | Aix·Marseille | Montagne Sainte-Victoire · Terra | — | closed(미확인) · hours(미확인) · booking(미확인) |
| 17 | 09/14(월) | Luberon | Goult | — | hours(미확인) |
| 20 | 09/17(목) | Avignon·Arles | Le Goût du Jour | 04 32 76 32 16 | hours(전화 문의) |
| 21 | 09/18(금) | Avignon·Arles | Uzès Place aux Herbes·구시가지 | — | booking(전화 문의) |
| 22 | 09/19(토) | Avignon·Arles | Arènes d'Arles | — | closed(전화 문의) · hours(전화 문의) · booking(전화 문의) |
| 22 | 09/19(토) | Avignon·Arles | Arles (도시) | — | hours(전화 문의) · closed(전화 문의) · booking(전화 문의) |
| 22 | 09/19(토) | Avignon·Arles | La Roquette | — | closed(전화 문의) · hours(전화 문의) · booking(전화 문의) |
| 22 | 09/19(토) | Avignon·Arles | Théâtre antique | — | closed(전화 문의) · hours(전화 문의) · booking(전화 문의) |
| 22 | 09/19(토) | Avignon·Arles | Cloître Saint-Trophime | — | closed(전화 문의) · hours(전화 문의) · booking(전화 문의) |
| 22 | 09/19(토) | Avignon·Arles | Place du Forum | — | closed(전화 문의) · hours(전화 문의) · booking(전화 문의) |
| 22 | 09/19(토) | Avignon·Arles | Restaurant SEVIN | — | closed(전화 문의) |
| 23 | 09/20(일) | Lyon·Annecy | Café Comptoir Abel | — | closed(전화 문의) · address(전화 문의) |
| 23 | 09/20(일) | Lyon·Annecy | Saône·Rhône 강변 산책 | — | closed(미확인) · hours(미확인) · booking(미확인) |
| 25 | 09/22(화) | Lyon·Annecy | Musée des Tissus | — | hours(전화 문의) |
| 29 | 09/26(토) | Paris | Latin Quarter (Panthéon 외관·Rue M | — | closed(전화 문의) · hours(전화 문의) · booking(전화 문의) |
| 29 | 09/26(토) | Paris | Notre-Dame de Paris | — | hours(전화 문의) · closed(전화 문의) |
| 32 | 09/29(화) | Paris | Montmartre · South Pigalle (Sacr | +33 1 53 41 89 00 | booking(전화 문의) |
| 32 | 09/29(화) | Paris | Musée d'Orsay | — | booking(전화 문의) |
| 36 | 10/03(토) | Paris | Montorgueil · Les Halles | — | closed(전화 문의) · hours(전화 문의) · booking(전화 문의) |
| 36 | 10/03(토) | Paris | Musée de l'Orangerie — 'Monet, p | — | booking(전화 문의) |
| 38 | 10/05(월) | Paris | 월요일 모듈 A–D (Aligre·Butte-aux-Cai | — | closed(전화 문의) · hours(전화 문의) · booking(전화 문의) |
| 41 | 10/08(목) | Paris | Giverny — Fondation Claude Monet | — | closed(전화 문의) · hours(전화 문의) · booking(전화 문의) · address(전화 문의) |
| — | 미배정 | Aix·Marseille | RTM lecar (Aix↔Marseille) | — | closed(전화 문의) |
| — | 미배정 | Avignon·Arles | Hertz Avignon TGV (AVNX92) | — | note(전화 문의) · closed(미확인) |
| — | 미배정 | Avignon·Arles | Nocturnes d'Avignon Musées | 04 90 80 80 00 | closed(미확인) |
| — | 미배정 | Avignon·Arles | Saint-Paul-de-Mausole | +33 4 90 92 77 00 | booking(미확인) |
| — | 미배정 | Avignon·Arles | 택시 (Avignon Centre→TGV) | — | closed(미확인) |
| — | 미배정 | Avignon·Arles | TER Virgule (Avignon Centre↔TGV) | — | closed(전화 문의) |
| — | 미배정 | Barcelona·Sitges | Aerobús | +34 900 92 96 92 | price_adult(전화 문의) |
| — | 미배정 | Barcelona·Sitges | CN Atlètic-Barceloneta | +34 93 221 00 10 | booking(전화 문의) |
| — | 미배정 | Barcelona·Sitges | ZBE (Barcelona 저배출구역) | — | closed(전화 문의) |
| — | 미배정 | Lyon·Annecy | Annecy 호수 크루즈 | 04 50 51 08 40 | hours(전화 문의) · closed(미확인) |
| — | 미배정 | Lyon·Annecy | TCL (Lyon 시내교통) | — | closed(전화 문의) |
| — | 미배정 | Nice·Côte d'Azur | Castle Hill 무료 엘리베이터 | 3906 | hours(전화 문의) · closed(미확인) |
| — | 미배정 | Nice·Côte d'Azur | Colline du Château (성채 언덕) | 3906 | note(미확인) |
| — | 미배정 | Nice·Côte d'Azur | Hertz Nice-Ville (Avenue Thiers) | +33 4 97 03 01 20 | hours(전화 문의) |
| — | 미배정 | Paris | Musée de l'Orangerie | — | price_adult(전화 문의) · closed(전화 문의) · hours(전화 문의) · booking(전화 문의) |
| — | 미배정 | Paris | Musée Marmottan Monet | +33 1 44 96 50 33 | note(미확인) |
| — | 미배정 | Paris | Navigo · IDFM (Paris 교통) | — | closed(전화 문의) |

---

## 4. 미해결 항목과 이유

| 항목 | 상태 | 이유 |
|---|---|---|
| **T4-3 사진** | **완료** | 장소 페이지 사진 **68 → 96 / 103**. Wikimedia Commons 에서 28장을 새로 받아 처리했다. 크레딧 143장 (`about/photo-credits.html`) |
| **T3-6 서술 보강** | 미착수 | 자르는 순서 2번 |
| G2 전체 코퍼스 371건 | 미해결 | 확정 등급 밖. 토큰화하려면 값 조사가 선행돼야 한다 |
| G3 91건 | WARN | 값이 없는 필드의 토큰을 지웠기 때문이다. 참조를 되살리려면 값이 있어야 한다 |
| `address` 148 / 160 비어 있음 | 미해결 | S2 가 이미 방문한 URL 에서 8건만 확보. 나머지는 새 조사가 필요하다 |
| `getting_there` 159 / 160 비어 있음 | 의도적 | 원고에서 수확을 시도했으나 **세 장소에 같은 버스 노선을 붙였다.** 틀린 길안내는 현장 사고라 수확을 철회했다 |
| BLOCKED 45곳 중 29곳 전화번호 없음 | 부분 해결 | 상당수가 지구·산책로·교통시스템이라 전화 대상이 아니다. 실제 시설은 §3 에 번호와 함께 있다 |
| 디자인 PDF 일부 | 부분 반영 | §6 참조 |

---

## 5. 여행 중 재확인 캘린더

그 날 방문하는 곳의 미확인 항목을 **전날 저녁에** 확인한다.

| 전날 | 대상일 | 확인할 것 |
|---|---|---|
| 08/29(토) 저녁 | Day 2 08/30(일) | Gràcia 저녁 산책(closed·hours·booking) · La Paradeta Sagrada Famíli(booking ☎+34 934 500 191) |
| 08/30(일) 저녁 | Day 3 08/31(월) | Bar Cañete(hours ☎+34 932 703 458) · Barri Gòtic(closed·hours·booking) · Biblioteca de Catalunya(hours·closed·booking ☎+34 93 270 23 00) · CEM Joan Miró(closed·booking ☎+34 934 234 350) · Llibreria Finestres(booking ☎+34 933 840 809) · Mercat de la Concepció(booking) · 고딕지구 핵심 산책 (Plaça del Rei–(closed·hours·booking) |
| 08/31(월) 저녁 | Day 4 09/01(화) | Museu del Cau Ferrat(booking ☎+34 93 894 03 64) · Museu de Maricel(booking ☎+34 93 894 03 64) · 시체스 2시간 30분 핵심 동선(closed·hours·booking) · Casa Marieta(closed ☎+34 972 201 016) · Call (유대인 지구)(closed·hours·booking ☎+34 972 216 761) · Onyar 강변(closed·hours·booking ☎+34 972 010 001) · 성벽 (Passeig de la Muralla)(booking ☎+34 972 010 001) |
| 09/01(화) 저녁 | Day 5 09/02(수) | Cadaqués(closed ☎+34 972 258 315) |
| 09/02(수) 저녁 | Day 6 09/03(목) | La Roca (Peratallada)(hours·closed ☎+34 972 634 172 / +34 606 911 243) · Pals(booking ☎+34 972 637 380) · Peratallada(closed·hours·booking ☎+34 872 987 030) |
| 09/04(금) 저녁 | Day 8 09/05(토) | La Table Alziari(closed ☎+33 4 93 80 34 03) |
| 09/10(목) 저녁 | Day 14 09/11(금) | Cassis 항구(closed ☎+33 4 28 01 01 03) · Le Panier(closed·hours·booking) |
| 09/11(금) 저녁 | Day 15 09/12(토) | Montagne Sainte-Victoire ·(closed·hours·booking) |
| 09/13(일) 저녁 | Day 17 09/14(월) | Goult(hours) |
| 09/16(수) 저녁 | Day 20 09/17(목) | Le Goût du Jour(hours ☎04 32 76 32 16) |
| 09/17(목) 저녁 | Day 21 09/18(금) | Uzès Place aux Herbes·구시가지(booking) |
| 09/18(금) 저녁 | Day 22 09/19(토) | Arènes d'Arles(closed·hours·booking) · Arles (도시)(hours·closed·booking) · La Roquette(closed·hours·booking) · Théâtre antique(closed·hours·booking) · Cloître Saint-Trophime(closed·hours·booking) · Place du Forum(closed·hours·booking) · Restaurant SEVIN(closed) |
| 09/19(토) 저녁 | Day 23 09/20(일) | Café Comptoir Abel(closed·address) · Saône·Rhône 강변 산책(closed·hours·booking) |
| 09/21(월) 저녁 | Day 25 09/22(화) | Musée des Tissus(hours) |
| 09/25(금) 저녁 | Day 29 09/26(토) | Latin Quarter (Panthéon 외관(closed·hours·booking) · Notre-Dame de Paris(hours·closed) |
| 09/28(월) 저녁 | Day 32 09/29(화) | Montmartre · South Pigalle(booking ☎+33 1 53 41 89 00) · Musée d'Orsay(booking) |
| 10/02(금) 저녁 | Day 36 10/03(토) | Montorgueil · Les Halles(closed·hours·booking) · Musée de l'Orangerie — 'Mo(booking) |
| 10/04(일) 저녁 | Day 38 10/05(월) | 월요일 모듈 A–D (Aligre·Butte-a(closed·hours·booking) |
| 10/07(수) 저녁 | Day 41 10/08(목) | Giverny — Fondation Claude(closed·hours·booking·address) |

---

## 6. 디자인개선 PDF — 반영·보류

**반영한 것** (주석 텍스트가 명확한 것)

- 일자 축 제목 `43일 일정` → **전체 일정**
- 지역 축 제목 `지역` → **가이드** (하단탭 이름과 맞췄다)
- 지역 목록의 **국경 구분선 삭제** — 지역을 순서대로만 놓는다
- 준비 화면 제목 `마스터 트래커` → **준비**, 홈 카드 레이블 → **여행 준비 상태를 점검**

**보류한 것 — 지시가 좌표만 있고 대상이 특정되지 않는다**

| 페이지 | 주석 | 내 읽기 | 왜 보류했나 |
|---|---|---|---|
| p1 | `삭제` | "다음 여행일 · 오늘 일정 열기" 카드 | 하단탭 '오늘'과 중복이라는 뜻으로 보이나, 홈의 주 진입점이라 지우면 동선이 바뀐다 |
| p2·p7 | `삭제` | 좌표 바(일정 43일 / 지역 8곳 / 주제 분류·상태) | CLAUDE.md 가 좌표 바를 L1 내비게이션으로 규정한다. 지우면 축 간 이동 경로가 끊긴다 — 링크 그래프 확인이 선행돼야 한다 |
| p3 | `삭제` | 지역 카드의 실행지도·첫날 카드 버튼(추정) | 좌표가 카드 그리드 우측이라 대상이 불확실하다 |
| p5 | "이 세 메뉴는 통합하고 중복 내용 삭제" | 지역소개·여행정보·(먹거리?) | **어느 셋인지 특정되지 않는다** |
| p6 | Barcelona 3개 메뉴 재구성 | 지역소개에서 숙소 관련 제거 · 숙박에 확정 숙소+교통 · 여행정보를 장소 카드로 통합 | 지시는 명확하나 챕터 8개에 같은 구조 변경을 적용하는 작업이고, 남은 세션 안에서 안전하게 끝낼 수 없다 |

**보류한 것은 지우지 않았다.** 잘못 지우면 되돌리는 비용이 크고, 출발이 11일 남았다.


---

## 7. T4-3 사진 (2026-08-18 추가)

**장소 페이지 사진 68 → 96 / 103.** Wikimedia Commons 에서 28장을 새로 받았다.
파이프라인은 기존 것을 그대로 썼다 — search → download → process → build.

**판정에서 걸러낸 것**

- **회화를 장소 사진으로 쓰지 않았다.** 첫 검색이 Place du Forum 에 반 고흐를,
  Glanum 에 위베르 로베르를, Bibémus·Sainte-Victoire·Jas de Bouffan 에 세잔을,
  Marmottan 에 모네를 물어 왔다. 현장에서 장소를 알아보는 용도라 그림은 못 쓴다.
  화가 이름·작품 표기로 걸러 재검색했다.
- **엉뚱한 장소 2건을 뺐다** — Bourse de Commerce 자리에 다른 교회 사진이,
  Marmottan 자리에 시슬레 회화가 잡혔다.
- **Centre Pompidou 는 제외했다.** 프랑스는 파노라마의 자유가 없어 1977년 건축이
  주 피사체인 사진은 사진가 라이선스로 건축 저작권이 해소되지 않는다.

**라이선스 강제를 경고로 내렸다 (Jason 지시 2026-08-18)**

`search_commons_images.py` 와 `build/media.py` 에서 라이선스·저작자 **차단**을 없앴다.
다만 두 가지는 사실로 남겨 둔다.

- 이 사이트는 gh-pages 로 **공개 배포**된다. '개인 사용만' 라이선스는 검사를 없앤다고
  쓸 수 있게 되는 것이 아니라 **빌드가 알려주지 않게** 되는 것이다.
- 저작자 표시는 CC BY·CC BY-SA 의 **이용 조건**이다. 그래서 저작자가 비면 거부하는 대신
  "저작자 미상"으로 채워 크레딧 페이지에 그대로 드러낸다 — 그 목록이 곧 채워야 할 목록이다.

실제로 받은 143장은 전부 PD·CC0·CC BY·CC BY-SA 이고 저작자가 있다. 경고는 0건이었다.

**아직 사진이 없는 7곳**

`centre-pompidou`(파노라마의 자유) · `carrieres-de-bibemus`·`musee-marmottan-monet`
(현장 사진 없음, 회화만) · `marche-de-la-liberation`(Commons 에 적격 사진 없음) ·
`bourse-de-commerce-pinault-collection`(검색이 엉뚱한 곳을 냄) ·
`lourmarin-2`(T3-1 에서 병합한 옛 중복 페이지의 잔재) · `index`(장소 아님)
