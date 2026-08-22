# RC01 — Barcelona Region 재통폐합 · Editorial Cleanup QA

**작성일** 2026-08-23 · **브랜치** `fix/barcelona-region-reconsolidation` · **대상** Barcelona (04)
**상태** PASS (자동검사) — 외부 편집검토에서 HOLD.
후속 보정은 `RC01F_BARCELONA_EDITORIAL_REVIEW_FIX.md` 가 정본이다. 아래 §11 최종 구조와 §12 수치는 RC01 시점의 것이다.

---

## 1. Overall Status

**PASS.** 세 조건을 모두 확인했다.

1. SOT 구조 — Region/Day/Place/Prepare/Archive 로 갈랐고, 자동 가드가 통과한다.
2. 시각적 중복 — 아래 §3 의 중복군 9개 중 8개가 해소됐다. 남은 1건은 FCR-02 에서
   이미 내린 결정이라 이번 scope 에서 뒤집지 않고 §17 에 적었다.
3. 원고 흔적 — 렌더된 페이지에서 **0건**. 되돌아가지 못하게 빌드 가드를 새로 세웠다.

---

## 2. Before 페이지의 핵심 문제

문제는 버그가 아니라 **설계된 동작**이었다. `build/promote_regions.py` 가 챕터 원고의
아홉 개 층을 **원문 그대로** 뽑고, `build/render.py::build_region` 이 그것을 접이식에
그대로 부었다. 접이식 제목 두 개는 렌더러에 **문자열로 하드코딩된 `— 원고`** 였다.

그 결과 실제 화면은 이랬다.

- **`음식·시장·카페·생활체험 — 원고`** · **`지역 교통 심화 — 원고`** 라는 제목이 그대로 보였다
- **절 번호 헤딩 37개** — `13.2 Bodega Joan`, `15.4 슈퍼마켓 사용 원칙`, `20.3 현장 10분 점검`,
  `7.1 Dreta de l'Eixample 동부 — 가장 균형 잡힌 1순위` …
- **본문이 없는 제목 6개** — `시간대`, `레스토랑·카페`, `시장·슈퍼·제철`, `운동·수영`,
  `공항·시내교통 실용정보`, `렌터카 인수 실행 가이드`. 원고에서는 묶음의 머리였지만
  화면에서는 아무것도 없는 줄이었다
- **가리키는 대상이 없는 문장** — Sants 표의 `인수 시각 | 아래 실행표 기준 준수`.
  그 실행표는 이 페이지에 없다
- **확정된 뒤에도 남은 후보 비교** — `12.7 숙소 최종 선택 알고리즘`이 Praktik Garden ·
  SERHS Carlit · Hotel Glòries · Leonardo · Motel One 을 이름으로 부르고 있었다.
  **숙소는 이미 Occidental Barcelona 1929 로 선결제까지 끝난 상태다.** 현장에서 이 화면을
  보고 엉뚱한 호텔로 가는 것이 이 프로젝트가 가장 경계하는 사고다
- **예약이 끝난 렌터카의 예약 전 조사** — `20.1 인수지 권장`이 SIXT 기준으로 쓰여 있었다.
  실제 예약은 Hertz 다
- **모바일에서 깨지는 표** — 390px 에서 Editor's Verdict 표의 항목 열이 `여행 적 / 합도`,
  `예산 체 / 감` 으로 잘렸다 (before 스크린샷)
- **히어로의 반복** — 표 바로 아래 `여행의 역할` 콜아웃이 히어로 문장을 거의 그대로 되풀이했다

---

## 3. 실제 화면의 중복 인벤토리

| # | 중복군 | 어디에서 몇 번 | 처리 |
|---|---|---|---|
| 1 | **장소 목록** | 한눈에 보기 표1 · 표3 · 생략해도 되는 것 등급표 · 장소 카드 7개 → **4중** | 카드만 남김. 표는 ARCHIVE, 예상 체류는 place-facts 로 MOVE |
| 2 | **식당 상세** | 장소 카드 · 13.1 표 · 13.2–13.5 장문 · La Zorra 필드 표 → **최대 4중** | 장소 정본 1곳으로 MOVE |
| 3 | **날짜별 일정** | 날짜 칩 · 추천 체류 리듬 흐름도 · 이 구간의 식사 전략 표 · 이 일정에서 쓰는 교통 → **4중** | 한눈에 보기 표 1개 + 날짜 칩으로 수렴 |
| 4 | **도시 소개** | 히어로 dek · Editor's Verdict 표 · 여행의 역할 콜아웃 · 여행 전체에서의 역할 · 이 지역을 이해하는 층 5블록 → **5중** | Verdict 산문 하나로 MERGE. 43일 안에서의 위치만 별도로 남김 |
| 5 | **교통권** | 교통권 카드 2 · 이용법 5줄 · 19.1 표 · 19.2 문단 · 추천 체류 리듬 '권장 교통권' 행 → **5중** | 카드·이용법만 남기고 ARCHIVE |
| 6 | **확정 숙소** | 숙소 카드 · staySummary · 추천 체류 리듬 '확정 숙소'·'숙박비' 행 · 준비 페이지 → **4중** | 카드·준비 페이지만 |
| 7 | **시장** | Mercat 장소 카드 · 15.1 장문 · 이 지역에서 먹는 것 목록 → **3중** | 구입 목록은 장소 정본으로 MOVE |
| 8 | **렌터카 인수** | 출발 카드 · Sants 표 · 20.1–20.4 · Day 4 카드 → **4중** | Day 4 정본, Region 은 3줄 요약 |
| 9 | **운동·수영** | 추천 체류 리듬 '운동' 행 · 16.1–16.4 · 17.1–17.3 → **3중** | 확정안만 생활권·숙소 섹션으로 |

**통폐합 전 중복 후보 블록 44개 · 통폐합 후 미해결 1건** (§17 참조).

---

## 4. Editorial Residue 인벤토리

| 유형 | Before | After |
|---|---:|---:|
| `— 원고` 편집용 제목 | 2 | **0** |
| 원고 절 번호 헤딩 (`13.2` `7.1` `20.3` …) | 37 | **0** |
| Commercial Guide / Regional Context | 0 | 0 |
| Layer / Phase / Research Pass | 0 | 0 |
| Section / Chapter 번호 | 0 | 0 |
| 초안 / draft / module | 0 | 0 |
| source 경로·파일명 | 0 | 0 |
| 문맥 없는 원고 조각 | 1 | **0** |
| 본문 없는 원고 묶음 제목 | 6 | **0** |

측정은 렌더된 `site/guide/barcelona.html` 의 **보이는 글자**만 본다. 원고에 절 번호가
남아 있는 것은 문제가 아니다 — 그것이 독자 화면에 나오는 것이 문제다.

---

## 5. Block Action Summary

| 판정 | 건수 | 비고 |
|---|---:|---|
| KEEP | 30 | Region 고유 정보 |
| MERGE | 12 | 같은 말을 하던 블록을 하나로 |
| MOVE | 9 | 다른 SOT 가 맞는 것 |
| ARCHIVE | 15 | 계획 단계 자료 |
| DELETE | 13 | 100% 복제이거나 본문 없는 제목·문맥 없는 조각 |
| **합계** | **79** | |

DELETE 13건 중 **정보를 담은 것은 하나도 없다** — 6건은 본문 없는 제목, 1건은 대상 없는
문장, 6건은 다른 정본에 같은 문장이 그대로 있는 복제다.

---

## 6. 실제로 통합한 주요 사례

- **한눈에 보기 3표** → 예상 체류시간은 `place-facts.json` 의 `duration` 으로, 확정 일정은
  Day 카드 배지로, 추천 이유는 장소 카드 요약으로. 표 자체는 ARCHIVE
- **꼭 경험할 세 장면** → 유지. Places 와 겹치지 않는다 (장소가 아니라 *장면*을 말한다)
- **추천 체류 리듬 12행 표** → 12행 중 6행이 준비·숙소·Day 의 복제였다. 남은 것은
  피로 관리·식사 시각·위험뿐이라 표를 없애고 세 문단으로
- **이 지역을 이해하는 층 (역사·경제·사회·문화·의미)** → Editor's Verdict 한 문단으로 MERGE
- **동네별 숙소 적합성 7.1–7.6** → 순위와 후보 호텔명은 ARCHIVE, 동네 성격 4개만 남김
- **지역 교통 심화 — 원고** → `이 지역에서 이동하기` 로 재편집. 19.x·20.1·20.2·21.x 는
  Day 4 와 중복이거나 예약 전 조사라 ARCHIVE
- **음식·시장·카페·생활체험 — 원고** → `이 지역의 음식과 시장` 으로 재편집. 식당 장문 4개는
  장소 정본으로 MOVE

---

## 7. Editorial Rewrite 사례

사실은 바꾸지 않았다. 표현과 위치만 바꿨다.

**(1) 원고 제목 → 여행자의 말**

| Before | After |
|---|---|
| `지역 교통 심화 — 원고` | `이 지역에서 이동하기` |
| `음식·시장·카페·생활체험 — 원고` | `이 지역의 음식과 시장` |
| `묵을 만한 동네 — 생활권 비교` | `동네와 생활권` |
| `13.2 Bodega Joan — 예산과 전통의 균형` | (장소 정본) `3. 예산에 맞춘 2인 주문 예시` |
| `15.4 슈퍼마켓 사용 원칙` | `슈퍼마켓과 제철 과일` |
| `16.1 러닝: Passeig de Sant Joan–Ciutadella (Eixample 대안)` | `아침 운동` |
| `20.3 현장 10분 점검` | `차를 받는 날` |

**(2) 표 → 문장** — Editor's Verdict

> Before: `| 여행 적합도 | ★★★★★ Jason·Julia의 생활형 여행에 최적화 |` `| 예산 체감 | 중상 |`
> `| 일정 강도 | 보통 |` + 히어로를 반복하는 콜아웃 2개
>
> After: "…**이번 3박은 뒤쪽이다.** 그래서 유료 가우디 명소는 사그라다 파밀리아 하나로
> 줄이고, 나머지는 산책과 시장, 도서관과 현대미술, 책방과 현지 음식으로 채운다.
> **일정 강도는 보통, 예산 체감은 중상이다.**"

**(3) 판정표 → 독자에게 하는 말** — 생략해도 되는 것

> Before: Essential/Priority/Optional/Alternative/Not recommended 5행 배분표
>
> After: "3박에 가우디를 모으려 하면 줄만 서다 끝난다. **Park Güell과 Casa Batlló·La
> Pedrera의 유료입장은 넣지 않았다.** 입장료와 대기시간에 비해, 이번 여행이 보려는 것 —
> 도시의 구조 — 을 더 보여주지 않기 때문이다." + 넣지 않은 선택지 5개를 소요시간과 함께

**(4) 문맥 없는 조각 제거** — Sants 표

> Before: `| 인수 시각 | 아래 실행표 기준 준수 |` — 그 실행표는 이 페이지에 없다
>
> After: "Barcelona Sants가 인수 지점이다. 서류 확인과 차량 점검, 주차장 출차까지
> **60–90분을 잡아 둔다.**" (실제 인수 시각 09:00 은 Day 4 정본)

**(5) 절 번호 묶음 → 하나의 흐름** — 시체스 주차

> Before: `21.1 1순위: Can Robert` / `21.2 2순위: Plaça del Pou Vedre 지하주차장` /
> `21.3 주차비 판단` (Day 4 카드가 이미 Can Robert 를 정본으로 갖고 있다)
>
> After: "시체스 구시가지는 **주차가 어렵다.** 외곽 주차장에 세우고 걸어 들어간다. 어느
> 주차장을 쓰든 노트북·여권·카메라를 차 안 보이는 곳에 두지 않는다." + 상세는 ARCHIVE

**(6) 여행 전체에서의 역할** — 추천 체류 리듬과 겹치던 둘째 문단

> Before: "도착 당일부터 밀어붙이면 이후 40일이 무너진다. **Day 1을 도착·정착으로
> 비워두는 것이 옳다.**" ← 바로 아래 접이식이 같은 말을 한다
>
> After: "여기서 몸이 유럽 시간에 맞으면 남은 40일이 편해지고, 여기서 밀어붙이면 남은
> 40일이 무너진다."

---

## 8. Place 로 이동한 장문

| 원고 | 목적지 | 옮긴 내용 |
|---|---|---|
| 13.2 | `source/CURRENT/30_Places/bodega-joan.md` | 예산별 2인 주문 예시 A/B, 일요일 저녁 예약 |
| 13.3 | `source/CURRENT/30_Places/puertecillo-sagrada-familia.md` **(신규)** | 무게 주문 방식, 2인 주문 요령, 상호 변경 경고, 가격 미공개 |
| 13.4 | `source/CURRENT/30_Places/bar-canete.md` | 네 축 주문 원칙, 카운터 vs 테이블 판단 |
| 13.5 | `source/CURRENT/30_Places/la-zorra.md` | 13:00 첫 회전, 75–85분 통제, 추천 주문, 대체 후보 |
| 15.1 | `source/CURRENT/30_Places/mercat-concepcio.md` | 사흘치 구입 목록(과일·햄·치즈·빵), 8월 말 휴가 주의 |
| 한눈에 보기 표3 | `data/place-facts.json` | 예상 체류 4건 — sagrada-familia 105분 · sant-pau 80분 · macba 120분 · llibreria-finestres 55분 (`confidence: editorial`) |

**Puertecillo Sagrada Família 는 정본이 없어 장소 페이지가 1,324자짜리 껍데기였다.**
이제 식당 카드로도 나온다 (Day 2 점심 확정 업소인데 카드가 없던 것이 이번에 드러났다).

---

## 9. Day 로 수렴한 일정

Region 에서 없앤 날짜 반복 UI:

- **추천 체류 리듬 흐름도** (8/29 → 8/30 → 8/31 → 9/1 코드블록) — 한눈에 보기 표로 흡수
- **이 구간의 식사 전략 표** (Day 1–4 × 성격 × 판단) — "어느 날 무엇을 먹는지는 그날의
  Day 페이지가 정본이다" 한 줄로
- **추천 체류 리듬 '음식 패턴' 행** (날짜별 식사) — 삭제, Day 정본
- **Sants 표 '인수 시각' 행** — 삭제, Day 4 가 09:00 을 갖는다

**Day 카드 파일은 하나도 고치지 않았다.** 일정·예약·시각을 건드리지 않기 위해서다.

---

## 10. Archive 한 Planning Residue

목적지는 전부 `source/ARCHIVE/20_Regional_Chapters/04_Barcelona_Planning_Residue_v1.0.md`
(13.9KB, 9개 묶음). 각 묶음에 **옮겨온 곳 · 현재 정본 · 분리 사유**를 적었다.

| # | 자료 | 원본 | 사유 |
|---|---|---|---|
| 1 | 등급 배분표 | §생략해도 되는 것 | 판정표는 계획 산물. 등급 정본은 명부와 place-facts |
| 2 | 한눈에 보기 3표 | §한눈에 보기 | 장소 카드·Day·place-facts 가 이미 말한다 |
| 3 | 동네 숙소 적합성 7.1–7.6 | §구역별 이해와 숙소 생활권 | 숙소가 확정된 뒤에는 독자의 질문이 아니다 |
| 4 | 예산 산식·후보 6곳·선택 알고리즘 11.1–12.7 | §숙소 예산과 확정 숙소 | **후보 호텔명이 확정 숙소 페이지에 남아 있었다** |
| 5 | 공항·시내교통 19.1–19.2 | §도착·출발·지역 내 교통 | transit-facts 카드와 100% 중복 |
| 6 | 렌터카 사전조건·주차 조사 20.1–21.3 | §도착·출발·지역 내 교통 | 예약 완료. 실행은 Day 4 정본 |
| 7 | 예약 레스토랑 표·추가 후보 13.1·13.6 | §음식·시장·카페·생활체험 | 카드 중복 + 예약 실패 대비 조사 |
| 8 | 식당 카드 La Zorra 필드표 | §음식·시장·카페·생활체험 | 같은 식당의 세 번째 설명 |
| 9 | 운동·수영 후보 16.2·16.4·17.1–17.3 | §음식·시장·카페·생활체험 | 확정안은 러닝과 CEM 뿐 |

---

## 11. 최종 Barcelona 페이지 구조 (실제 visible section)

```
개요      날짜 칩 4 · 도시와 이번 3박 (3문단) · 꼭 경험할 세 장면 · 우천 전환 · 사진
          [접이식] 생략해도 되는 것 · 한눈에 보기 · 여행 전체에서의 역할 · 추천 체류 리듬
볼거리    꼭 가야 할 곳 4 · 권할 만한 곳 3
식당·카페 식당 4 · 빵집·시장·푸드홀 1 · 요리 사진 2
          [접이식] 이 지역에서 먹는 것 · 이 지역의 음식과 시장
숙소      확정 숙소 카드 · 생활권 요약  [접이식] 동네와 생활권
생활권    생활 수칙 4 · 늦은 귀가
교통      도착·출발 · 구간 내 이동(교통권 2·이용법·예외·일정별)
          [접이식] 이 지역에서 이동하기 · 공식 자료와 재확인
```

여섯 역할로 수렴한다. 접이식은 10개 → 8개.

---

## 12. Before / After Metrics

렌더된 `site/guide/barcelona.html` 기준. 같은 자로 두 번 쟀다.

| 지표 | Before | After | 변화 |
|---|---:|---:|---:|
| Visible content blocks | 1,017 | 486 | −52.2% |
| Visible characters | 22,488 | 11,399 | −49.3% |
| H2 | 13 | 13 | — |
| H3 | 40 | 32 | −8 |
| H4 | 39 | **0** | −39 |
| H5 | 1 | **0** | −1 |
| Tables | 17 | 4 | −13 |
| Accordion (details) | 10 | 8 | −2 |
| Article cards | 18 | 19 | +1 (Puertecillo) |
| 목록 항목 (li) | 99 | 47 | −52 |
| Day navigation 링크 | 21 | 22 | +1 |
| Place 링크 | 15 | 16 | +1 |
| Editorial residue 합계 | 40 | **0** | −40 |
| 모바일 390px 전개 높이 | 48,225px (57.1화면) | 25,937px (30.7화면) | **−46.2%** |
| 모바일 390px 접힘 높이 | 15,687px | 16,457px | +4.9% |

접힘 높이가 조금 늘어난 것은 **식당 카드가 하나 늘었기 때문**이다 (Puertecillo). 정보가
늘었지 밀도가 나빠진 것이 아니다. 감량률은 참고지표이며 PASS 기준으로 쓰지 않았다.

### 파일 영향 범위

**Canonical source (실질 변경)**
- `source/CURRENT/20_Regional_Chapters/04_Barcelona_Sitges_v2.0.md` — 1,356줄 → 902줄
- `source/CURRENT/30_Places/bodega-joan.md` · `bar-canete.md` · `la-zorra.md` · `mercat-concepcio.md`
- `source/CURRENT/30_Places/puertecillo-sagrada-familia.md` **(신규)**
- `data/place-facts.json` — duration 4건 추가
- `data/region-essentials.json` — barcelona lifeEssentials 4번째 항목, sourceRefs
- `source/ARCHIVE/20_Regional_Chapters/04_Barcelona_Planning_Residue_v1.0.md` **(신규)**

**Renderer / build**
- `build/render.py` — 접이식 제목 4개 (문자열만, 8개 지역 공통 — §15 회귀검사 참조)
- `build/manuscript_residue_check.py` **(신규 가드)** · `build/site.py` (가드 호출)
- `data/region-consolidation.json` **(신규)** — 가드를 강제할 지역 목록

**Generated (직접 수정 안 함 — 빌드 결과를 그대로 커밋)**
- `source/CURRENT/20_Regions/barcelona.md` — `promote_regions.py` 가 매 빌드 재생성.
  저장소가 추적하는 파일이라 재생성 결과를 함께 커밋한다
- `site/**` — 빌드 산출물, 저장소에 커밋되지 않음
- `REGION_CONTENT_AUDIT.{json,md}` · `REGION_RECLASSIFICATION_MAP.json` ·
  `FCR02_FOOD_COMPLETENESS.json` — `region_audit.py` 재생성. **diff 는 전부 Barcelona
  기인**이다 (Puertecillo 정본 신설로 식당·카페·시장 장소 23 → 24). 다른 지역 항목 변경 0

**Day / Prepare** — 변경 없음. 일정·예약·시각을 건드리지 않았다.

---

## 13~14. Canonical / Generated 관계

작업 전 확인한 파이프라인:

```
20_Regional_Chapters/04_*.md   ← 정본. content_guard 가 h2 14개의 존재와 순서를 강제
        │ promote_regions.py (매 빌드)
        ▼
20_Regions/barcelona.md        ← 파생물. 직접 편집 금지
        │ render.build_region
        ▼
site/guide/barcelona.html

30_Places/<slug>.md            ← 정본 (site.py:51 "매 빌드마다 덮어쓰지 않는다")
```

**CLAUDE.md 는 `30_Places/` 를 파생물이라고 적고 있으나 사실이 아니다.** `build/site.py`
51–53행이 명시적으로 정본이라고 말하고, `promote_places.py` 는 "한 번만 돌린다"고
적혀 있다. 장소 장문은 그 파일을 직접 고치는 것이 맞다. → §17 후속 과제.

---

## 15. Desktop / Mobile Visual QA

**Desktop 1280px** — top→bottom 확인. 섹션 반복 없음, 같은 카드/표의 재등장 없음,
Places·Food·Local Life·Transport 밀도 균일. 접이식 8개가 모두 닫힌 상태로 시작한다.

**Mobile 390px** — 첫 2화면 비교 (스크린샷 보관: `scratchpad/shots/`)

| | Before | After |
|---|---|---|
| 화면 2 | 항목 열이 `여행 적 / 합도`, `예산 체 / 감` 으로 잘리는 5행 표 → 히어로를 반복하는 콜아웃 | 도시를 설명하는 3문단. 표 없음 |
| 화면 3 | 표가 계속됨 | 꼭 경험할 세 장면 → 우천 전환 → 사진 → 접이식 |

`build/viewport_check.py` — 360·390·430·768·1024·1440 × 12쪽 실렌더:
**가로 오버플로 0 · 터치 타깃 44pt 이상 · 글자 11px 이상 통과** (guide/barcelona.html 포함).

**다른 7개 지역 회귀검사** — 렌더 결과의 변화는 **지역당 정확히 −30자**뿐이고, 전부
접이식 제목 4개의 이름 변경이다. 구조·표·카드·링크·문단 수 변화 0.

| 지역 | visible chars | 그 밖의 지표 |
|---|---|---|
| girona | 13,119 → 13,089 | 변화 없음 |
| nice | 11,954 → 11,924 | 변화 없음 |
| aix | 17,879 → 17,849 | 변화 없음 |
| luberon | 17,653 → 17,623 | 변화 없음 |
| avignon | 21,779 → 21,749 | 변화 없음 |
| lyon | 15,318 → 15,288 | 변화 없음 |
| paris | 22,380 → 22,350 | 변화 없음 |

제목 변경은 의도한 것이다 — `— 원고` 는 8개 지역 전부에서 보이던 제작 흔적이었다.
**내용은 한 글자도 바꾸지 않았다.**

---

## 16. Automated QA

| 명령 | 결과 |
|---|---|
| `python3 build/site.py` | **PASS** — 372쪽 · 검색 색인 191건 · 정본 장소 136 (장문 134) |
| `python3 -m pytest tests/` | **PASS** — 30 passed |
| `python3 build/region_structure_check.py` | **PASS** — 분류·섹션·방문일·링크 이상 없음 |
| `python3 build/media_lookup_check.py` | **PASS** — 미매핑 0 · 유실 0 |
| `python3 build/table_loss_check.py` | **PASS** — 조용한 열 손실 0 |
| `python3 build/content_audit.py` | **PASS** — 장소 136 · 문단 1,173 · **콘텐츠 손실 0** |
| `python3 build/manuscript_residue_check.py` | **PASS** — barcelona 흔적 0 (신규) |
| `python3 build/ux_check.py` | **PASS** — 명암비·하단탭·43일·표 열 |
| `python3 build/viewport_check.py` | **PASS** — 6뷰포트 × 12쪽 |
| `python3 scripts/generate_attributions.py --check` | **PASS** |
| `python3 scripts/validate_map_data.py --quiet-warnings` | **PASS** (경고 113, 기존) |
| `python3 -m unittest discover -s build -p test_validation.py` | **PASS** — 20 tests |
| `python3 scripts/validate_itinerary.py` | **PASS** — 43일 · 42박 · 거점 연결 7건 |
| `python3 scripts/validate_media.py` | **PASS** |
| `python3 build/pwa_check.py` | **PASS** — 871파일 · 오프라인 심층 탐색 |
| `python3 build/guards/run_all.py` | FAIL `['G2','G3']` — **main 에서도 같다** (S0~S3 사실 인프라 진행 중). G2 는 오히려 384 → **356** 으로 줄었다 (하드코딩된 가격·시각이 원고에서 빠졌다) |

### 새 가드 — `build/manuscript_residue_check.py`

렌더된 지역 페이지의 **보이는 글자**에서 원고 흔적 8종을 찾는다. 통폐합이 끝난 지역만
빌드를 세우고(`data/region-consolidation.json`), 나머지는 세어서 보여 준다.

```
원고 흔적 가드: 통폐합 완료 barcelona — 흔적 0
  아직 통폐합하지 않은 지역 (세기만 한다): avignon 16 · girona 7 · luberon 17 · paris 18
```

부정 픽스처로 확인했다 — `consolidated` 에 paris 를 넣으면 18건을 잡고 **rc=1** 로 멈춘다.

---

## 17. Scope 밖 Factual Issues

이번 작업에서 **고치지 않고 기록만 한다.**

1. **Day 2 식사 슬롯의 옛 상호** — `data/daily-cards/day-02.json` 의 `food` 가
   `"La Paradeta · 제철 해산물"` 이다. 이 자리는 지금 **Puertecillo Sagrada Família** 이고
   원고와 place-facts 는 이미 그렇게 적고 있다. 지역 페이지의 `이 지역에서 먹는 것`
   목록에 옛 상호가 그대로 보인다. → Day SOT 수정이 필요하다.
2. **La Zorra 주차 안내 충돌** — 장소 정본 `la-zorra.md` 실용표는
   `Parking El Retiro 또는 Parking Nou Mercat` 인데, Day 4 카드와 챕터는 **Can Robert** 다.
   현장에서 서로 다른 주차장으로 안내한다.
3. **미해결 중복 1건 (결정 대기)** — `이 지역에서 먹는 것` 목록이 식당 카드와 업소명을
   겹쳐 보여준다 (Bodega Joan · Bar Cañete · La Zorra). FCR-02 감사가 "업소가 아니라
   '무엇을 먹는가' 이므로 목록으로 남긴다"고 판정한 건이라 이번에 뒤집지 않았다.
   목록을 요리 이름 중심으로 바꿀지는 별도 결정이 필요하다.
4. **Palau de Maricel 카드 요약** — `권할 만한 곳` 에 있으면서 요약문이
   `⚠ 9/1(화)에는 관람할 수 없다.` 다. 사실은 맞지만 카드 설명 자리에 경고만 있다.
5. **CLAUDE.md 의 낡은 서술** — `30_Places/` 를 파생물로 적고 있으나 정본이다 (§13).

---

## 18. Git

- **브랜치** `fix/barcelona-region-reconsolidation` (base `origin/main` `41d888fd`)
- **커밋** `95a7505a`
- **PR** [#208](https://github.com/jeongjae/SP-FR-guidebook/pull/208)
- **변경 파일** 12개 (신규 4 · 수정 8) + 재생성된 audit 4개

---

## 19. STOP

**Barcelona 만 했다.** 다른 7개 지역은 시작하지 않았다. 배포도 하지 않았다.

다음 지역으로 넘어가려면 그 지역을 `data/region-consolidation.json` 의 `consolidated` 에
올리는 것으로 가드가 따라온다.
