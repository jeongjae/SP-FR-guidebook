# RC01F — Barcelona 외부 편집검토 반영

**작성일** 2026-08-23 · **브랜치** `fix/barcelona-region-reconsolidation` · **PR** [#208](https://github.com/jeongjae/SP-FR-guidebook/pull/208)
**상태** 반영 완료 · **merge/deploy 하지 않음** · 다음 지역 시작하지 않음

RC01 은 기술적으로 PASS 했으나 외부 편집검토에서 HOLD 됐다. 이 문서는 그 검토가
확정한 편집 명세 10건의 반영 결과다.

---

## 1. Editorial decisions 반영 여부

| § | 결정 | 반영 |
|---|---|---|
| 1 | Overview 4블록(가치와 한계·세 장면·전체에서의 역할·체류 리듬)을 하나로 재통합, 지정 문안 사용 | ✅ 지정 문안 그대로. `이번 3박은 뒤쪽이다` · `43일 중 유일한 대도시 구간이다` 삭제 |
| 2 | `생략해도 되는 것` 제거, 제외 후보는 Archive, 실제 Plan B 는 해당 Day 로 | ✅ 블록 제거. Disseny Hub·Museu Picasso·Fundació Joan Miró 는 Day 2 `backup` 으로, 나머지는 Archive |
| 3 | `한눈에 보기` → `일정`, 2열 표로 단순화 | ✅ 날짜·핵심 일정 2열. 상세는 Day 정본으로 위임 |
| 4 | `숙소 생활권과 동네` → `숙소와 생활권`, 후보 평가 어투 제거 | ✅ 동네 4곳을 **일정에서 실제로 걷는 곳** 기준으로 재작성 |
| 5 | `지역 교통 심화` → `바르셀로나에서 이동하기`, 3역할 정리 + 문안 교체 | ✅ 시내 도보·메트로 / 9월 1일 렌터카 인수 / Sitges를 거쳐 Girona로. 소매치기·귀중품 문장 지정 문안으로 교체 |
| 6 | `음식·시장·카페·생활체험` → `먹고 장보기`, What-to-eat/Where-to-eat 분리, 메모식 표현 rewrite, 카페 재검토 | ✅ 요리 표 7행 전부 설명문으로 재작성. 업소명 중복 0. 카페 5곳은 Archive (아래 §4) |
| 7 | 식사시간 문안의 과도한 단정 삭제 | ✅ 지정 문안으로 교체 |
| 8 | Puertecillo/La Paradeta · La Zorra 주차 해소 | ✅ 아래 §5·§6 |
| 9 | CLAUDE.md SOT 문서 정정 | ✅ 아래 §7 |
| 10 | 내부 제작 heading 누출 가능성 확인 | ✅ 아래 §8 |

---

## 2. 최종 visible section 구조

```
개요       날짜 칩 4
           도시와 이번 3박 (2문단) · 이번 3박의 핵심 (3항목) · 하루의 기본 (1문단)
           우천 전환 · 지역 사진
           [접이식] 일정 — 날짜 × 핵심 일정 2열
볼거리     꼭 가야 할 곳 4 · 권할 만한 곳 3
식당·카페  식당 4 · 빵집·시장·푸드홀 1 · 요리 사진 2
           [접이식] 이 지역에서 먹는 것 (요리만) · 먹고 장보기
숙소       확정 숙소 카드 · 생활권 요약  [접이식] 숙소와 생활권
생활권     생활 수칙 4 · 늦은 귀가
교통       도착·출발 · 구간 내 이동  [접이식] 바르셀로나에서 이동하기
           공식 자료와 재확인
```

접이식 **10 → 5개.** 표 **17 → 3개.**

---

## 3. Before / After visible character count

| | main | RC01 | **RC01F** |
|---|---:|---:|---:|
| 보이는 글자 | 22,488 | 11,399 | **9,635** |
| 보이는 블록 | 1,017 | 486 | **397** |
| 표 | 17 | 4 | **3** |
| 접이식 | 10 | 8 | **5** |
| H2 / H3 / H4 | 13 / 40 / 39 | 13 / 32 / 0 | **12 / 29 / 0** |
| 원고 흔적 | 40 | 0 | **0** |
| 모바일 390px 전개 높이 | 57.1화면 | 30.7화면 | **26.5화면** |

main 대비 **−57.2%**, RC01 대비 **−15.5%**.

**장소 링크는 12개 전부 카드가 잇는다** — 산문에서만 이어지던 경로 0. 길은 끊기지 않았다.

---

## 4. Unresolved duplicates

**0건.** RC01 에서 남겨 두었던 `이 지역에서 먹는 것` ↔ 식당 카드의 업소명 중복이 해소됐다.

Day 의 식사 슬롯은 `업소 · 요리` 형식이다. 통폐합을 끝낸 지역에서는 렌더러가 **그 업소가
카드로 나오고 있으면 이름을 떼고 요리만 남긴다** (`region_dishes`). 지역 전용 분기가 아니라
`data/region-consolidation.json` 이 판정한다.

- Before: `Bodega Joan · 타파스` · `Bar Cañete · 타파스·해산물` · `La Zorra · arroz a banda`
- After: `제철 해산물` · `타파스` · `타파스·해산물` · `시장 장보기 · 과일·빵` · `arroz a banda`

카페 5곳(Three Marks · Nomad ×2 · Federal Café Gòtic · Granja M. Viader)은 **확정 일정과
Day Plan B 어디에도 연결되지 않아** Archive 로 내렸다 (§6 판정 기준 "단순 조사 후보").
실제로 쓰이게 되면 그때 해당 Day 로 올린다.

---

## 5. Puertecillo / La Paradeta reconciliation

**해소. 새 조사는 하지 않았다.**

기존 canonical evidence — `FCR04_DAY_SOT_CORRECTIONS_QA.md §3` 이 이미 **RENAMED /
사업체 교체(`REPLACED`)** 로 판정해 두었다. 근거 셋: ① 같은 주소(Passatge de Simó 18)가
Google Maps 에서 Puertecillo 로 나온다 ② Puertecillo 공식 사이트가 그 주소를 자기 지점으로
싣는다 ③ La Paradeta 공식 사이트의 지점 목록에 Sagrada Família 가 없다.

그 판정이 Day stop·명부·지도 질의·place-facts 에는 반영됐는데 **`day-02.json` 의 `food`
요약 배열에만 옛 상호가 남아 있었다.** 잔여 문자열 하나를 현재 정본에 맞췄다.

```
- "La Paradeta · 제철 해산물"
+ "Puertecillo Sagrada Família · 제철 해산물"
```

사용자 화면의 `La Paradeta` 노출 **0건.**

---

## 6. La Zorra parking reconciliation

**같은 목적이었다 — SOT 를 하나로 정규화했다.**

두 값의 성격을 확인한 결과, 둘 다 "시체스에서 차를 세우고 걸어 들어간다"는 **같은 목적**이다.
역할이 다른 것이 아니라 답이 둘이었다.

| | 값 | 근거 |
|---|---|---|
| Day 4 (확정 동선) | `Aparcament Can Robert` | `day-04.json` stop · `map-queries.json` 해석 주소 · 챕터가 시 공식 안내 1순위로 기록 |
| 장소 정본 (이전) | `Parking El Retiro` 또는 `Parking Nou Mercat` | 출처 없음. `FCR02_VOLATILE_RECHECK_REGISTER.csv` 에 **ACTIVE 재확인 대상**으로 등록된 미검증 값 |

10:20 Can Robert 주차 → Cau Ferrat·Maricel → 해안로 → 13:00 La Zorra 는 **하나의 동선**이라
식당만 다른 주차장을 가리킬 이유가 없다. 장소 정본을 Day 정본에 맞췄고, 재확인 등록은
그대로 뒀다. 분리 기록은 Archive §12.

---

## 7. CLAUDE.md correction

코드를 근거로 확인한 뒤 최소 수정했다.

- **`30_Places/` 는 정본이다.** `build/site.py` 가 `load_place_bodies()` 로 직접 읽고,
  `promote_places.py` 는 "한 번만 돌린다"고 명시돼 있다. 챕터를 고쳐도 아무 일이 없다.
- **파생물은 `20_Regions/` 하나뿐이다.** `promote_regions.regenerate()` 가 매 빌드 재생성한다.
- 챕터 h2 구성을 강제하는 스키마(`rs-region-v1` / `rc-region-v1`)와, 통폐합 완료 지역의
  정본이 `data/region-consolidation.json` 이라는 사실을 함께 적었다.

RC01 이전의 CLAUDE.md 는 30_Places 를 "빌드가 다시 뽑는 파생물"이라고 적고 있었다.
그 문장을 믿고 챕터만 고쳤다면 장소 글은 바뀌지 않았을 것이다.

---

## 8. 내부 heading 누출 가능성

**문자열을 숨기지 않고 구조로 해결했다.**

1. **경로 확인** — `# Commercial Guide Module` · `# Regional Context & Scheduled Place Dossiers`
   는 h1 이다. `promote_regions.extract()` 는 h2 에서만 시작하고 하위는 level>2 만 담으며,
   `extract_deep()` 의 `_is_boundary()` 는 level==1 을 항상 경계로 보고 경계 자체는 담지
   않는다. **현재 승격 규칙으로는 h1 이 새어나올 수 없다.**
2. **원고 자체 정리** — 챕터에 남아 있던 절 번호 23개를 전부 뗐다. `8.6 Museu Picasso` 등
   제외 후보 4곳과 `10.3` 요금 정정 기록은 Archive 로 옮겼고, `10.1`·`10.2` 는 위쪽 절과
   중복이라 병합했다. `22.x`·`26.`·`17.~20. Day N` 은 제목을 다시 지었다.
   **챕터에 남은 절 번호 heading 0개.**
3. **가드가 승격 산출물까지 본다** — `manuscript_residue_check` 가 이제 렌더된 화면뿐 아니라
   `source/CURRENT/20_Regions/<slug>.md` 도 스캔한다. 화면만 보면 "지금은 안 보인다"까지만
   알 수 있고, 승격 산출물까지 보면 **새어나올 수 있는 상태인가**를 안다.
4. **Day 헤딩 파서 수정** — `## 17. Day 1 —` 의 번호를 떼려면 `guards/common.py` 의
   `DAY_RE` 가 번호를 필수로 요구하는 것을 먼저 고쳐야 했다. 번호를 선택으로 바꿨다.
   안 고치고 번호만 뗐으면 **G1/G1c 의 요일·달력 대조가 그 챕터에서 통째로 조용히
   건너뛰었을 것이다.**

### 층을 합치면서 가드가 약해지지 않게 한 것

`rs-region-v1` 은 `꼭 경험할 세 장면`·`한눈에 보기` 같은 **제목이 배포본에 있는지**로
"편집 층이 사라지지 않았는가"를 확인했다. 층을 합치면 그 제목이 없어진다 — 여기서 토큰
검사를 끄면 가드를 약화시키는 것이다. 대신 두 가지를 했다.

- 통폐합 챕터용 스키마 **`rc-region-v1`** 을 새로 만들고 챕터가 그것을 선언한다.
  h2 구성과 순서는 여전히 강제된다 (요구 h2 10개).
- 제목 대신 **내용의 양**을 보는 검사를 추가했다 — 통폐합 지역의 개요가 400자 미만이면
  빌드를 세운다. 부정 픽스처로 확인했다 (개요를 비우면 rc=1).

---

## 9. Automated QA

| 명령 | 결과 |
|---|---|
| `build/site.py` | PASS — 372쪽 · 색인 191건 |
| `pytest tests/` | PASS — 30 |
| `build/region_structure_check.py` | PASS |
| `build/media_lookup_check.py` | PASS |
| `build/table_loss_check.py` | PASS |
| `build/content_audit.py` | PASS — **콘텐츠 손실 0** |
| `build/manuscript_residue_check.py` | PASS — barcelona 흔적 0 (화면 + 승격본) |
| `build/ux_check.py` | PASS |
| `build/viewport_check.py` | PASS — 6뷰포트 × 12쪽 |
| `scripts/generate_attributions.py --check` | PASS |
| `scripts/validate_map_data.py` | PASS |
| `unittest test_validation` | PASS — 20 |
| `scripts/validate_itinerary.py` | PASS — 43일 · 42박 |
| `scripts/validate_media.py` | PASS |
| `build/pwa_check.py` | PASS |
| `build/guards/run_all.py` | FAIL `['G2','G3']` — **main 에서도 같다.** G2 는 384 → 356(RC01) → **346** 으로 계속 줄었다. G1 은 PASS |

**G1 이 한 번 깨졌고 고쳤다.** 지정 문안의 `… MACBA의 현대미술 …` 과 `9월 1일에는 렌터카를
인수해 …` 가 한 줄에 있어, 가드가 그 줄의 날짜 리터럴을 같은 줄의 MACBA 방문일로 읽고
**"9/1(화)는 MACBA 휴관일"** 을 잡았다. 문장은 그대로 두고 줄만 나눠 해소했다. 가드가
제 일을 한 사례다.

### 추가 PASS 조건 (§11)

| 조건 | 결과 |
|---|---|
| excluded-candidate list visible | **0** |
| separate `여행 전체에서의 역할` block | **0** |
| separate `추천 체류 리듬` block | **0** |
| manuscript `지역 교통 심화` heading | **0** |
| manuscript `음식·시장·카페·생활체험` heading | **0** |
| restaurant names duplicated in What-to-eat | **0** |
| Puertecillo/La Paradeta user-facing conflict | **0** |
| La Zorra parking unexplained conflict | **0** |
| known factual contradictions | **0** |
| raw internal heading capable of leaking | **0** (§8) |

---

## 10. Desktop / Mobile Visual QA

- **Desktop 1280px** — 접힘 10,504px · 전개 13,762px · 가로 오버플로 없음.
  섹션·카드·표 반복 없음. 개요가 표가 아니라 문장으로 시작한다.
- **Mobile 390px** — 접힘 16,166px · 전개 **22,359px (26.5화면, RC01 대비 −13.8%)** ·
  가로 오버플로 없음. 두 번째 화면이 도시 설명 문단 → `이번 3박의 핵심` 으로 이어진다.
- `viewport_check` — 360·390·430·768·1024·1440 × 12쪽 실렌더 통과 (터치 타깃 44pt · 글자 11px).

**다른 7개 지역** — RC01F 로 인한 렌더 변화 **0** (모든 지표 동일). RC01 에서 접이식 제목
4개가 바뀐 것이 전부다.

---

## 11. Scope 밖 Factual Issue (기록만)

1. **Palau de Maricel 카드 요약** — `권할 만한 곳` 에 있으면서 설명문이
   `⚠ 9/1(화)에는 관람할 수 없다.` 다. 사실은 맞지만 카드 설명 자리에 경고만 있다.
2. **Can Robert 주소 표기 차이** — 챕터(현재 Archive)는 `Avinguda del Camí dels Capellans`,
   `data/map-queries.json` 은 `Passeig de Vilafranca` 로 적는다. 같은 주차장의 다른 진입
   표기인지 확인이 필요하다. 이번 scope 밖이라 손대지 않았다.
