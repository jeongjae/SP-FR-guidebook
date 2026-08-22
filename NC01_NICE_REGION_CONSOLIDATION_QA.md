# NC01 — Nice / Côte d'Azur Region 편집 통폐합 QA

**작성일** 2026-08-23 · **브랜치** `fix/nice-region-editorial-consolidation` (base `origin/main` `c3a935b4`)
**상태** 구현·QA 완료 · **merge/deploy 하지 않음** · 외부 Editorial Review 대기 · Aix 시작하지 않음

---

## 1. Overall Status

**PASS — 다만 결정이 필요한 사실 충돌 2건이 남는다** (§18).

자동 게이트는 전부 통과했고 §36 의 PASS 조건도 모두 0 이다. 그러나 이번 작업에서
**canonical 대 canonical 충돌** 을 두 건 발견했고, §33 에 따라 임의로 고치지 않았다.
하나(교통 데이터)는 Day SOT 기준 정규화가 가능해 해소했고, **DEC-A03 은 해소하지 못했다.**

### §0 시작 조건에 대한 기록

명세 §0 은 "Girona 승인·머지·배포 PASS 후 시작" 을 전제한다. 실제로는 **Girona 통폐합이
아직 진행 중**이고(다른 세션), 직전에 완료·배포된 것은 Barcelona 다. 사용자가 진행을
승인해 착수했다. Girona 세션과 충돌하지 않도록 **별도 워크트리
`SP-FR-nice` 에서 작업**했고 `site/` 를 공유하지 않았다.

---

## 2. Before 실제 렌더의 문제

배포본(`gh-pages @ c3a935b4`) 기준으로 확인한 것들이다.

- **개요가 다섯 덩어리로 흩어져 같은 말을 반복** — 평가표(★·예산·강도) → 개요 문단 →
  `꼭 경험할 세 장면` → `여행 전체에서의 역할` → `추천 체류 리듬` 이 이어졌다.
- **일정이 세 번** — `한눈에 보기` 의 Day 7–12 목록, `추천 체류 리듬` 의 전·중·후반부,
  교통의 `이 일정에서 쓰는 교통`.
- **확정 숙소인데 재선정 기준이 남아 있었다** — "숙소를 다시 고를 일이 생기면…".
- **`[CONFIRMED]` 자리표시자가 화면에 세 번 노출** — 숙소 상세 블록의 예약번호·호스트 자리.
- **내부 코드 노출** — 교통 설명의 `(DEC-A03)`, 먹거리 목록의 `WISH-01`·`WISH-02`,
  업장 체계의 `Status: USER_CONFIRMATION_REQUIRED`, 제목의 `Regional Recommended Foods`.
- **생활권 표에 관광지가 섞여 있었다** — Cours Saleya·Colline du Château·Promenade 는
  '어디서 생활하는가' 가 아니라 '무엇을 보는가' 다. 표의 Day 번호도 로컬(Day 2·3…)이라
  화면의 글로벌 Day 배지와 어긋났다.
- **먹거리 목록이 Day 식사 슬롯 그대로** — `점심: Le Figuier de Saint-Esprit (WISH-01,
  미쉐린 1스타)` 처럼 끼니 라벨과 업소 이름이 식당 카드와 겹쳤다.
- **과장 문체** — "가장 긴 무이동 구간", "완벽한 완충 구간", "풍성한 인트로",
  "최적의 방사형 여정", "철저히 배제", "극적인 겹", "산뜻하게 다녀온다".

### 그리고 사실이 틀려 있었다

- `생략해도 되는 것` 이 **Èze·Villefranche-sur-Mer 를 '제외 후보'로 설명**했다.
  두 곳 모두 **Day 11(9/8) 확정 일정**이다.
- `한눈에 보기` 와 히어로 문구가 **9/8 을 "Nice 생활·회복일"** 로 적었다.
  Day SOT 는 Villefranche → Villa Ephrussi → Èze 다.
- `추천 체류 리듬` 이 **"다음 날 아침 공항 렌터카를 인수해"** 라고 적었다.
  인수지는 **Nice-Ville 역** 이다.

---

## 3. 9/8–9/9 Schedule reconciliation

`data/daily-cards/day-07~12.json` 을 정본으로 삼아 정규화했다(§7).

| 날짜 | Day SOT (정본) | 통폐합 전 Region 서술 |
|---|---|---|
| 9/4 | Nice 도착 · 체크인 | 같음 |
| 9/5 | Cours Saleya · Vieux Nice · Colline du Château · Promenade · Port Lympia | 같음 |
| 9/6 | **Antibes + Cannes** | "Cannes 당일치기" — 앙티브 누락 |
| 9/7 | Monaco + Menton | 같음 |
| 9/8 | **Villefranche-sur-Mer · Villa Ephrussi · Èze** | "Nice 생활·회복일" ❌ |
| 9/9 | Nice-Ville역 인수 → **Saint-Paul-de-Vence → Grasse** → Aix | 같음 (단, 교통 절은 "생폴은 전날" ❌) |

**Region 내부 일정 모순 0.** 일정 표현은 `한눈에 보기 — 일정` 표 하나로 수렴했다.

### 교통 데이터의 Day 배정도 어긋나 있었다 — 해소

`data/transit-facts.json` 이 Villefranche·Èze 를 **Day 10** 에, Libération 시장을
**Day 11** 에 배정하고 있었다. Day SOT 와 어긋난다. **횟수·요금은 건드리지 않고 Day
배정만** 정본에 맞췄다 — 같은 이동(공항 2회 + Èze 83번 왕복 4회 + Cap-Ferrat 왕복 4회)의
날짜만 바뀌므로 총 10회(+여유 2회)는 그대로다.

---

## 4. Rental pickup reconciliation

| 출처 | 인수지 | 판정 |
|---|---|---|
| `data/daily-cards/day-12.json` | Nice-Ville역 Hertz 09:00 | **정본** |
| 챕터 §도착·출발·지역 내 교통 | Nice-Ville 역 Hertz (Avenue Thiers) | 일치 |
| 챕터 §추천 체류 리듬 | **"공항 렌터카"** | ❌ 낡은 문자열 |
| `data/transit-facts.json` | Nice역에서 인수 | 일치 |

`추천 체류 리듬` 블록 자체를 제거하면서 해소됐다. **사용자 화면의 인수지 표기 충돌 0**
— Nice-Ville 역만 2회 나온다.

---

## 5. External Editorial Decisions 반영 결과

| § | 결정 | 반영 |
|---|---|---|
| 4 | Overview 4블록 통합, 지정 문안 | ✅ 지정 문안 기반. **Day SOT 대조 후 세 곳을 고쳤다** (아래) |
| 5 | `꼭 경험할 세 장면` 제거 | ✅ 개요 `이번 5박의 핵심` 으로 흡수 |
| 6 | `생략해도 되는 것` 제거 | ✅ 블록 제거 · Archive |
| 7 | Schedule 하나만 | ✅ `일정` 표 1개, Day SOT 기준 |
| 8 | `여행 전체에서의 역할` 제거 | ✅ |
| 9 | `추천 체류 리듬` 제거 | ✅ |
| 10 | `한눈에 보기` 재구성 | ✅ 숙소→Stay, 교통→Transport, 날짜→Schedule |
| 11 | `숙소와 생활권` + 지정 문안 | ✅ |
| 12 | 숙소 재선정 문구 제거 | ✅ Archive |
| 13 | 생활권 표에서 관광지 분리 | ✅ 표 제거, 관광 구역은 장소 카드가 맡는다 |
| 14–17 | Transport 3역할 + 상세 이관 | ✅ 공항/TER/렌터카 |
| 18–21 | Food 재편집·문체 수정 | ✅ |
| 22 | 시장 정리 | ✅ 역할 2문단 + 운영시간은 장소·Day 로 |
| 23 | 식당·카페 후보 정리 | ✅ 예약 2곳만 남기고 후보는 Archive |
| 24 | 운동·수영·회복은 Stay & Local Life | ✅ `생활과 회복` |
| 25 | Place 장문 감사 | ✅ Region 은 카드 수준만. **Day 방문지 21곳 전부 이미 dossier·명부 보유** — 승격 필요 없음 |
| 26 | 도시 설명 중복 제거 | ✅ 개요에서 한 줄씩 |
| 27 | 원고·내부 표현 제거 | ✅ 렌더 0건 (§13) |
| 28 | 과장 문체 | ✅ 히어로 태그라인 포함 |

### §4 지정 문안에서 고친 세 곳

§4 자체가 "사실값과 일정은 current Day / Stay SOT 와 충돌하지 않는지 먼저 확인한다"고
지시했고, 대조 결과 지정 문안이 Day SOT 와 어긋나 아래만 조정했다.

1. "Cannes와 Monaco·Menton을 다녀오면서" → **"Antibes·Cannes와 Monaco·Menton"** (9/6 은 앙티브부터다)
2. "별다른 목표 없이 생활하는 날을 섞어" → 삭제. **Day SOT 에 자유일이 없다** (9/5–9/8 이
   모두 일정이 있는 날이다). 대신 "매일 저녁에는 니스로 돌아와 장을 보거나 쉬면서"로 바꿨다
3. 9/8 의 Villefranche·Cap-Ferrat·Èze 를 둘째 문단에 추가 — 지정 문안에 빠져 있었다

`이번 5박의 핵심` 두 번째 항목도 같은 이유로 **앙티브를 포함**하도록 넓혔다.

---

## 6. Overview before / after

**Before** — 평가표 5행 + 개요 문단 + 세 장면 3항목 + 역할 블록 + 리듬 블록 (5개 덩어리)

**After** — 문단 2 + `이번 5박의 핵심` 3항목 + 마무리 1문단 (한 덩어리) + 접이식 `일정` 1개

문체 예:

> Before: "43일간의 장기 유럽 여정 중 **가장 긴 무이동 구간**(5박 6일)이다. … **핵심적인 회복 구간**이자 … **풍성한 인트로 역할**을 한다."
>
> After: "니스는 이번 여행에서 처음으로 며칠 동안 짐을 풀어놓고 생활 리듬을 회복하는 해안 거점이다."

---

## 7. Place 장문 MOVE

**이관한 장문 0건.** Region 에 남아 있던 것은 이미 카드 수준(요약 1–2문장)이었고,
Day 가 방문하는 21개 지점 전부가 `30_Places/<slug>.md` 정본과 명부 등재를 갖고 있다.
(Barcelona 에서 Puertecillo 가 정본 없이 카드도 없던 것과 대비된다.)

Region 에서 뺀 장소 서술은 §13 의 생활권 표뿐이고, 그 관광 구역들(Vieux Nice ·
Cours Saleya · Colline du Château · Promenade des Anglais)은 이미 각자 카드와 장소
페이지를 갖고 있다. **장소 링크 17개 전부 카드가 잇는다 — 산문에서만 이어지던 경로 0.**

---

## 8. Schedule / Day 수렴

Region 에서 없앤 날짜 반복:

- `한눈에 보기` 의 Day 7–12 목록 (숙소·교통까지 함께 나열)
- `추천 체류 리듬` 의 전·중·후반부 서술
- 생활권 표의 로컬 Day 번호(Day 2·3·4·5·6)

남은 것은 `일정` 표 하나와 개요 위의 날짜 칩(Day 링크)이다.

---

## 9. Food 정리

- 제목 `음식·시장·카페·생활체험` → **`니스에서 먹고 장보기`**
- 역할 분리: `니스에서 먹어볼 것`(음식만) · `시장과 장보기` · `일정에서 이용하는 식당과 카페`
- 대표 음식 9종에서 **업소명·Day 번호·`Best:` 표기를 전부 제거**하고 설명문으로 재작성
- `희망 vs 추천 업장 체계`(WISH/RECOMMENDED) 블록 전체 Archive
- **Day 식사 슬롯 목록(`이 지역에서 먹는 것`)을 통폐합 지역에서는 렌더하지 않는다** (§10 참조)

문체 수정 예:

| Before | After |
|---|---|
| 사보이 공국의 역사와 지중해 해안선이 빚어낸 **독립적인 미식 체계(Cuisine Nissarde)를 자랑한다** | 프로방스와 가까우면서도 이탈리아 리구리아의 영향을 강하게 받은 별도의 지역 전통을 갖고 있다 |
| 니스 **최고의** 길거리 음식 | 니스의 **대표적인** 길거리 음식 |
| (익힌 감자나 껍질콩이 들어가면 **변형**) | 전통적인 니스식은 생채소 중심이지만 **식당마다 구성은 조금씩 다르다** |

---

## 10. 다른 지역에 미친 영향 — Barcelona

`이 지역에서 먹는 것` 목록은 Day 의 식사 슬롯에서 뽑는다. Nice 에서는 그것이
`점심: Le Figuier de Saint-Esprit (WISH-01, 미쉐린 1스타)` 처럼 **끼니 라벨 + 업소명 +
내부 코드**로 나왔다. §20 이 "What to eat 에는 음식만" 이라고 못 박았고, 통폐합한 챕터는
이미 자기 `먹어볼 것` 목록을 갖는다. 그래서 **통폐합 완료 지역에서는 이 목록을 만들지
않도록** 했다 (등록부 기반, 지역 전용 분기 아님).

그 결과 **Barcelona 도 이 접이식 하나를 잃는다.**

- 잃은 항목: 제철 해산물 · 타파스 · 타파스·해산물 · 시장 장보기 · 과일·빵 · arroz a banda
- 이 중 넷은 바로 위 식당 카드(Puertecillo·Bar Cañete·La Zorra)가 그대로 말한다
- 순수하게 사라진 것은 **"시장 장보기 · 과일·빵" 한 줄**이고, Barcelona 의
  `카탈루냐에서 먹어볼 것`·`시장과 장보기` 절이 같은 내용을 더 자세히 다룬다
- Barcelona 렌더 변화: 9,635 → 9,582자, 접이식 5 → 4, 장소 링크 12개 유지(모두 카드)

RC01F 외부검토가 지적한 "업소명이 카드와 반복된다" 의 연장선이라 판단해 적용했다.
되돌리길 원하면 `region_dishes()` 의 통폐합 지역 분기 한 줄만 빼면 된다.

---

## 11. Stay & Local Life 정리

- 제목 `숙소 생활권과 동네` → **`숙소와 생활권`**
- 지정 문안 적용 · 숙소 선택 조언과 재선정 기준 제거
- 확정 숙소 상세 블록(예약번호·호스트·`[CONFIRMED]`) 제거 → 숙소 카드와 준비 페이지가 정본
- 생활권 표 제거 → 관광 구역은 장소 카드로
- `생활과 회복` 신설 (§24) — 세탁·장보기·운동·수영을 실행 가능한 수준으로만

**한 가지 남긴 것**: 5박 총액 **€809.54**. 이 값이 챕터에만 있어서 지우면
`fact_guard`(확정 사실 토큰 생존)가 빌드를 세운다 — 실제로 한 번 세웠다. §18-2 참조.

---

## 12. Transport 정리

- 제목 `지역 교통 심화` → **`니스와 코트다쥐르에서 이동하기`**
- 3역할: `공항에서 숙소로` · `Antibes·Cannes·Monaco·Menton은 TER` · `렌터카를 받는 날`
- Region 에서 뺀 것: 도착 시각·체크인 시각, La Carte/Multi voyages 구매 실행법,
  이용 횟수 계산, `Aéro €10 왕복권은 사지 않는다`(과거 선택 과정), 구간별 소요시간,
  `(DEC-A03)`
- 남긴 것: 왜 철도가 기본인가, 인수가 이후 구간의 시작점이라는 것, 내륙 주차 원칙

---

## 13. Manuscript / internal residue before → after

| 항목 | Before | After |
|---|---:|---:|
| `-- 원고` 편집용 제목 | 0 | 0 |
| 원고 절 번호 heading (렌더) | 0 | 0 |
| **챕터 canonical 의 절 번호 heading** | **7** | **0** |
| `DEC-A03` / `DEC-A08` 등 결정 코드 (렌더) | 1 | **0** |
| `DEC-` 코드 (챕터 canonical) | 3 | **0** |
| `[CONFIRMED]` 자리표시자 | 3 | **0** |
| `WISH-01` / `WISH-02` | 2 | **0** |
| `USER_CONFIRMATION_REQUIRED` | 1 | **0** |
| `Regional Recommended Foods` | 1 | **0** |
| 과장 문체 표현 | 7 | **0** |
| 제외 후보 목록 | 3항목 | **0** |

`manuscript_residue_check` 가 이제 **nice 를 강제 대상으로** 본다 (화면 + 승격 산출물 양쪽).

---

## 14. 최종 visible 구조

```
개요       날짜 칩 6
           도시와 이번 5박 (2문단) · 이번 5박의 핵심 (3항목) · 하루의 원칙 (1문단)
           우천 전환
           [접이식] 일정 — 날짜 × 핵심 일정 2열
볼거리     꼭 가야 할 곳 11 · 권할 만한 곳 4
식당·카페  식당 2 · 요리 사진 2
           [접이식] 니스에서 먹고 장보기 (먹어볼 것 · 시장과 장보기 · 이용하는 식당)
숙소       확정 숙소 카드 · 생활권 요약  [접이식] 숙소와 생활권 (+ 생활과 회복)
생활권     생활 수칙 4 · 늦은 귀가
교통       도착·출발 · 구간 내 이동  [접이식] 니스와 코트다쥐르에서 이동하기
           공식 자료와 재확인
```

접이식 **8 → 4개.**

---

## 15. 정량 before / after

| 지표 | Before | After | 변화 |
|---|---:|---:|---:|
| Visible characters | 11,924 | **9,049** | −24.1% |
| Visible blocks | 424 | **328** | −22.6% |
| Tables | 2 | **1** | −1 |
| H2 / H3 / H4 | 11 / 26 / 5 | **10 / 34 / 0** | H4 소멸 |
| Accordion (details) | 8 | **4** | −4 |
| 목록 항목 (li) | 66 | **35** | −31 |
| Place cards (article) | 24 | 24 | — |
| Place 링크 | 21 | 17 | 전부 카드가 잇는다 |
| Schedule 표현 | 3 | **1** | −2 |
| Planning candidate list | 3 | **0** | −3 |
| Manuscript / internal residue | 11 | **0** | −11 |
| Duplicate candidates | 9군 | — | — |
| Unresolved duplicates | — | **0** | |
| User-facing factual contradiction | **4** | **0** | −4 |
| 모바일 390px 전개 높이 | 28.6화면 | **22.6화면** | −21.0% |
| 데스크톱 전개 높이 | 15.4화면 | **13.3화면** | −13.6% |

### Action

| 판정 | 건수 |
|---|---:|
| KEEP | 21 |
| MERGE | 9 |
| MOVE | 7 |
| ARCHIVE | 10 |
| DELETE | 8 |

### 파일 영향

**Canonical source**
- `source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md` (543 → 513줄, 스키마 `rc-region-v1`)
- `source/CURRENT/10_Core/regions.json` — nice `dek`·`tagline`
- `source/ARCHIVE/20_Regional_Chapters/06_Nice_Planning_Residue_v1.0.md` **(신규, 10묶음)**

**Data**
- `data/transit-facts.json` — nice 의 Day 배정 정규화 (요금·횟수 불변)
- `data/region-consolidation.json` — `consolidated` 에 nice, `layerTitles.nice`

**Build / render**
- `build/render.py` — `region_dishes()` 가 통폐합 지역에서 Day 식사 슬롯 목록을 만들지 않는다

**Place / Day / Prepare** — **변경 없음.** Day 카드와 예약 데이터는 건드리지 않았다.

**Generated** — `source/CURRENT/20_Regions/nice.md` (매 빌드 재생성분 커밋)

---

## 16. Desktop / Mobile Visual QA

- **Desktop 1280px** — 접힘 9,125px · 전개 11,237px · 가로 오버플로 없음.
  개요가 표가 아니라 문장으로 시작하고, 섹션·카드·표 반복이 없다.
- **Mobile 390px** — 접힘 14,764px · 전개 19,048px(22.6화면) · 가로 오버플로 없음.
  두 번째 화면이 날짜 칩 → 도시 설명 문단으로 이어지고, 세 번째 화면에서
  `이번 5박의 핵심` 이 나온다.
- `viewport_check` — 360·390·430·768·1024·1440 × 12쪽 실렌더 통과.
- before/after 스크린샷 보관: `scratchpad/shots/nice-{before,after}-*.png`

---

## 17. Automated QA

| 명령 | 결과 |
|---|---|
| `build/site.py` | PASS — 372쪽 · 색인 191건 |
| `pytest tests/` | PASS — 30 |
| `build/region_structure_check.py` | PASS |
| `build/media_lookup_check.py` | PASS |
| `build/table_loss_check.py` | PASS |
| `build/content_audit.py` | PASS — **콘텐츠 손실 0** |
| `build/manuscript_residue_check.py` | PASS — barcelona·nice 흔적 0 |
| `build/ux_check.py` | PASS |
| `build/viewport_check.py` | PASS |
| `scripts/generate_attributions.py --check` | PASS |
| `scripts/validate_map_data.py` | PASS |
| `unittest test_validation` | PASS — 20 |
| `scripts/validate_itinerary.py` | PASS — 43일 · 42박 |
| `scripts/validate_media.py` | PASS |
| `build/pwa_check.py` | PASS |
| `build/guards/run_all.py` | FAIL `['G2','G3']` — **main 에서도 같다.** G2 는 346 → **345**. G1·G1c·G4·G5 PASS |

### §36 PASS 조건

content loss 0 · unintended Day change 0 · reservation change 0 · broken link 0 ·
media loss 0 · table loss 0 · manuscript residue 0 · raw numbered heading 0 ·
internal decision code 0 · `[CONFIRMED]` 0 · duplicate schedule 0 ·
Region 내부 일정 모순 0 · 9/8–9/9 모순 0 · 렌터카 인수지 모순 0 ·
duplicate Place long-form 0 · visible planning shortlist 0 ·
food/day meal duplication 0 · unresolved structural duplicate 0 — **전부 충족**

---

## 18. Factual Issues — 결정이 필요하다

### 1. `DEC-A03` ↔ `day-12.json` (canonical 대 canonical) — **미해소**

| 출처 | 내용 |
|---|---|
| `data/decisions.json` `DEC-A03` | "Saint-Paul-de-Vence → **9/8** Nice 당일치기 (Fondation Maeght 와 함께)" · 금지 패턴 `9/9 생폴`·`9/9 Saint-Paul`·`생폴드방스를 거쳐` · scope `06_Nice_*.md`·`07_Aix_*.md` |
| `data/daily-cards/day-12.json` (9/9) | 10:15 **Saint-Paul-de-Vence** → 13:15 Grasse → Aix |
| `data/daily-cards/day-11.json` (9/8) | Villefranche · Villa Ephrussi · Èze — **Saint-Paul 없음** |

§7 이 "Day SOT 만 최종 일정으로 채택" 이라고 지시해 **Region 은 Day SOT(9/9)를 따랐다.**
G5(결정 잔재 가드)는 통과하는데, 금지 패턴이 리터럴 문자열이라 표 형식의 문장에는
걸리지 않기 때문이다 — **가드 통과가 충돌 해소를 뜻하지 않는다.**

결정 등록부를 Day SOT 에 맞출지, Day SOT 를 DEC-A03 에 맞출지는 **사용자 결정 사항**이다.
어느 쪽이든 `decisions.json` 또는 `day-11/12.json` 중 하나를 고쳐야 한다.

### 2. Palais ALZIRA 결제 금액이 두 값이다 — **미해소**

| 출처 | 값 |
|---|---|
| 챕터(현재 Region 숙소 절) · 확정 사실 매니페스트 CF006 | **€809.54** |
| 준비 페이지(예약 트래커 xlsx) | **€433.82** |

같은 숙소의 결제 총액이 두 곳에서 다르다. 예약 데이터라 §33 에 따라 손대지 않았다.
`fact_guard` 가 €809.54 의 생존을 요구해 Region 숙소 절에 한 문장으로 남겼는데,
**원래 이 값은 Prepare 가 가져야 한다.** 금액이 정리되면 Region 에서 뺄 수 있다.

### 3. 챕터 Day 5(9/8) 서술이 낡았다 — 화면에는 안 나온다

챕터의 `## Day 5 — 9월 8일 화요일` 절이 아직 "Nice 생활·회복일: 리베라시옹 시장,
로스차일드 빌라 런치, 프롬나드 해변 휴식" 으로 시작한다. Day SOT(Villefranche·Ephrussi·
Èze)와 어긋나지만 **이 절은 어디에도 렌더되지 않고**, 실행 시간표를 다시 쓰는 것은
Day SOT 작업이라 §33 에 따라 손대지 않았다.

### 4. Villefranche-sur-Mer · Èze 는 명부에 없다

Day 11 의 두 방문지가 `place_ref` 없이 stop 이름으로만 있다. 장소 페이지가 없어
`일정` 표에서 링크되지 않는다. 새 조사 금지(§33)라 이번 scope 에서 만들지 않았다.

---

## 19. Git

- **브랜치** `fix/nice-region-editorial-consolidation` (base `origin/main` `c3a935b4`)
- **워크트리** `/mnt/c/Users/NB-24021500/source/worktrees/SP-FR-nice` (Girona 세션과 격리)
- **merge/deploy 하지 않았다.** 외부 Editorial Review 승인 대기
- **주의**: `data/region-consolidation.json` 은 진행 중인 Girona 작업도 건드리는 파일이다.
  머지 시점에 conflict 가 예상되며, Git Integration Rule 에 따라 **자동 해결하지 않고
  보고한다.**
