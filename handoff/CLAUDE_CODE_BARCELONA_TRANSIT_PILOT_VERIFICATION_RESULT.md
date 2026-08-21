# Barcelona 숙박·생활·공공교통 파일럿 — 독립 검증 결과

검증일 2026-08-21 · 대상 `codex/stay-transport-guards` @ `3ef061a7` · 기준 `origin/main` @ `527c1c4c`
검증 중 코드 변경 없음 (읽기 전용 + 별도 `SPFR_SITE_DIR` 빌드)

---

## 1. 최종 판정

# FAIL

차단 이슈 2건 때문이다. **공식 요금 사실 8개는 전부 일치했고 구조 설계도 타당하다** — 실패 원인은 사실 오류가 아니라 ① CI 게이트 회귀와 ② 같은 화면이 스스로 모순되는 것이다. 둘 다 국소 수정으로 해소 가능하며, 해소되면 이 파일럿은 Nice 확장 기반으로 승인할 만하다.

---

## 2. 차단 이슈

### B1 — 뷰포트 게이트 회귀. `text-link` 는 존재하지 않는 클래스다

`build/render.py:951,955` 가 도착·출발 카드의 Day 링크를 `<a class="text-link">` 로 렌더한다. **`text-link` 는 `build/assets/style.css` 어디에도 정의돼 있지 않다** (`grep -rn "text-link" build/` → render.py 두 줄이 전부).

정의가 없으니 기본 인라인 링크로 떨어지고 높이가 20px 가 된다. 실측 `128.6 × 20`.

```
360·390·430·768·1024·1440px  guide/barcelona.html
  터치 타깃 44pt 미만 — a.text-link 129x20      (6개 뷰포트 전부)
```

- `origin/main`: `python3 build/viewport_check.py` → **통과**
- 이 브랜치: **6건 실패**

`viewport_check.py` 는 CI 가 돌리는 게이트이므로(`​.github/workflows/pages.yml:74`) 이 상태로는 배포가 막힌다. 저장소 관례는 `class="btn btn-secondary"` 이고 `.btn` 이 `min-height: var(--tap)` (=44px)를 갖는다(`style.css:376-382`). **`text-link` → `btn btn-secondary` 로 바꾸면 해소된다.**

### B2 — 같은 페이지가 교통권을 두 번, 서로 반대로 권한다

`guide/barcelona.html` 한 장에 상반된 권고가 동시에 렌더된다.

| 위치 | 공항 이동 | 시내 교통권 |
|---|---|---|
| **신규 파일럿** (`transit-facts.json` → TRANSPORT 절) | "택시를 **기본안**으로 쓴다. Aerobús A1 은 택시 대기가 길 때의 **대안**" | "T-casual … 1인 10회권이라 **현재 일정에는 과다**" |
| **챕터 파생 층** (`04_Barcelona_Sitges_v2.0.md:102,325,338` → 추천 체류 리듬) | "공항→숙소는 **Aerobús 우선** … 짐이 많으면 택시", "**기본 권장** — 짐이 아주 많을 때만 택시" | "시내는 **각자 T-casual 1존 €13**", "각자 T-casual 1장을 산다. 2일 동안 5회 이상 타면 단일권보다 유리" |

렌더 확인: `guide/barcelona.html` 에 `Aerobús 우선` 1건, `T-casual 1존 €13` 1건, `T-casual` 총 3건.

현장에서 어느 쪽을 믿을지 사용자가 고르게 만드는 구조다. 파일럿이 daily card 만 정본으로 삼고 **챕터의 구(舊) 권고를 정정하지 않은 채 새 층을 얹었기 때문**에 생겼다. 챕터 쪽 권고에는 아직 `{{badge:unverified|요금 공식 확인}}` 이 붙어 있는데, 이번에 공식 확인이 끝났으므로 정정할 근거도 이미 있다.

완화 요소: 챕터 층은 `<details>` 로 기본 접혀 있다. 그래도 펼치면 그대로 보이므로 차단 사유로 둔다.

---

## 3. 사실 검증 표

공식 페이지를 새로 열어 확인했다. URL 5개 전부 생존, 404·리다이렉트 없음.

| # | 주장 | 공식 근거 | 판정 | 수정 제안 |
|---|---|---|---|---|
| 1 | TMB 단일권 €2.90 | tmb.cat `/transport-ticket-fares` 2026 요금(2026-01-15 시행) 1존 €2.90 · ATM 보도자료 교차확인 | **일치** | 근거일에 "2026-01-15 시행" 병기 |
| 2 | T-familiar €11.50 · 공동 · 8회 | `/single-and-integrated/t-familiar` "8 journeys in 30 consecutive days" · terms "as long as you travel together… validations must match the number of people" | **일치** | **누락 조건 2개 추가**: 첫 검표 후 **30일** 유효 · **동행할 때만** 공유(따로 이동 불가) |
| 3 | T-casual €13.00 · 1인 · 10회 | `/t-casual` "10 journeys", "Single-person" · terms "cannot be used simultaneously by more than one person, but… by different people at different times" | **일치** | "1인 전용" 은 *동시* 사용 금지 — 시간차 사용은 허용됨을 명시하면 정확 |
| 4 | T-casual·T-familiar 공항 L9 Sud 불가 | 두 상품 페이지 "Not valid at the metro stations Aeroport T1 i Aeroport T2 on line L9 Sud" · `/aeroport-ticket` 은 "single-person, non-integrated", 2026 **€5.90** | **일치** | Airport ticket **€5.90 · 비통합(환승 불가)** 을 예외 항목에 함께 표기 |
| 5 | 1존 통합권 75분 · 최대 3회 환승 | terms "With an integrated pass (**not a single ticket**), you can transfer up to 3 times… single-zone… **75 minutes**" | **일치** | 본문이 "통합권은" 으로 이미 한정해 표현은 정확. 다만 §5 노트 참조(배치상 오독 위험) |
| 6 | 은행카드 단일권 구매·검증 | `/bank-card-validation` 버스는 앞문 리더, 메트로는 "**In some metro accesses**" · "hold the card close to the reader as many times as there are people" · 증빙은 카드 끝 4자리 | **일치** | 본문이 "일부 메트로 개찰구" 로 이미 정확히 한정함. 공식 문서는 은행카드 단일권의 **환승 가능 여부를 명시하지 않는다** — 단정 서술을 피할 것 |
| 7 | Rodalies 승차 전 구매·검증·보관 | rodalies.gencat.cat "must be validated before boarding", "Keep your ticket until you have left the station" | **일치** | 같은 페이지의 추가 사실 반영 권장: 1존 **€2.55** · 검증 후 **2시간** · 메트로·버스 **환승 불가** |
| 8 | 2인 4회 시 T-familiar €11.50 < 단일권 €11.60 | 4 × €2.90 = €11.60 | **일치(실익 미미)** | 차액 **€0.10**. 8회권이라 4회만 쓰면 절반을 버린다. "8회를 다 쓰면 1회당 €1.44" 가 현장에서 더 쓸모 있는 문장 |

추가 확인: 50% 할인은 **T-usual·T-jove 한정**이며 T-casual·T-familiar 에는 적용되지 않는다. 데이터에 할인 서술이 없어 문제 없음.

**확인불가 0건.** 다만 공식 문서가 침묵하는 두 가지 — 은행카드 단일권의 환승 가능 여부, 은행카드 검증 가능한 메트로 역 목록("some metro accesses") — 은 단정하지 말 것.

---

## 4. 일정 · daily card 연결 검증

### 링크 (전수 확인, 모두 정상)

| 링크 | 대상 | 결과 |
|---|---|---|
| 도착 — Day 1 / 출발 — Day 4 | `../daily/day-01.html` · `day-04.html` | OK |
| Day 1 실행 보기 / Day 4 실행 보기 | 동일 | OK (단 B1 의 터치 타깃 문제) |
| 이 일정에서 쓰는 교통 Day 1~4 | `../daily/day-01~04.html` | OK |
| 공식 출처 5건 | tmb.cat · rodalies.gencat.cat | 외부, 형식 정상 |

콘솔 오류·경고 **0건** (390px·1024px 실렌더).

### `itineraryUses` 4줄 대조

| 주장 | 판정 | 근거 |
|---|---|---|
| Day 1 "택시 기본, Aerobús 대안" | **일치** | `day-01.json` leg mode=`taxi`, totalDistance "약 12km · 택시" |
| Day 2 "Sagrada Família→Gràcia **구간만** 버스·Metro 선택" | **불일치(과소)** | `day-02.json` totalDistance = "약 10km · **메트로+도보**", needsReview = "**숙소→사그라다 아침 이동수단(Metro/버스) 현장 확정**". 숙소(Hostafrancs)→Sagrada 는 약 5km 로 실질 승차 구간인데 leg 로 모델링만 안 돼 있다. "구간만" 은 데이터가 뒷받침하지 않는다 |
| Day 3 "도보 중심" | **부분 일치** | leg 6개 전부 walk 이나 totalDistance = "약 6.5km · **도보+메트로**", needsReview = "확정 숙소 기준 Concepció 아침 동선 재검토" |
| Day 4 "Sants 렌터카 인수 후 이동" | **일치** | leg mode=`car`, C-32 / AP-7 |

**연쇄 영향**: `recommendation.summary` 의 "선택적으로 **한 번**" 이 과소집계 위에 서 있다. 실제 승차 후보는 최소 2~3회(Day 2 아침·Gràcia, Day 3 귀가)다. 그 위에 "합계 4회 이상일 때만 T-familiar" 라는 결론이 얹혀 있어, **전제가 바뀌면 결론도 바뀐다.** 4회는 이미 손에 닿는 수치다.

### 근거 없는 서술

`exceptions[2]` 의 "Day 4 의 Sitges 이동을 **철도로 바꾸면** Rodalies 승차권을…" — `day-04.json` 에 철도 backup·leg·needsReview 가 하나도 없다(day-01~04 통틀어 rail 키워드 0건). 대안이 일정에 존재하지 않으므로 **삭제하거나, day-04 에 실제 backup 을 추가한 뒤 남길 것.**

### 교차 지역 혼입 (회귀 기준)

커밋 `14de29e1` 의 `render.py:932` `if d.region != r.slug: continue` 로 **차단됐다.** 실측:

```
barcelona  전체 8 → 렌더 5   제외: 택시 / 렌터카·C-32/AP-7 / Sitges 도보
girona    전체 10 → 렌더 7   nice     13→11   aix 11→9
luberon     8→6   avignon 10→7   lyon 11→9   paris 32→32
```

`modes[:10]` 절단은 **제거 확인** (`render.py:944` 가 `for m in modes`). 파리가 32개 전부 렌더된다 — 이전에 22개가 조용히 사라지던 문제가 해소됐다.

**다만 드리프트는 방향만 바뀌었다.** Day 4 의 `region` 은 자는 곳 기준 girona 라서, Barcelona 출발 항목인 "택시 · 렌터카 C-32/AP-7 · **Sitges 도보**" 가 **Girona 지역 페이지에 자기 항목으로** 실린다. 코드 주석이 "도착·출발 상세는 Day 링크가 맡는다"로 의도된 트레이드오프를 선언하고 있으나, Barcelona 페이지 안에서도 비대칭이 남는다 — 출발 링크와 `itineraryUses` 는 Day 4 를 싣는데 교통 요약 목록만 Day 4 를 뺀다.

부수: `day-04.json` transport[0] "택시" 는 대응하는 leg 이 없다(체크아웃→Sants 는 walk 0.8km). 챕터 "도보 10분 안팎, 아니면 택시" 의 잔재로 보인다.

---

## 5. 중복 제거와 실행성 평가 (§7 7문항)

| # | 질문 | 판정 | 근거 |
|---|---|---|---|
| 1 | 숙박·생활 요약이 원고 반복·에세이 없이 현장 행동을 바꾸는가 | **PASS WITH NOTES** | 4줄 전부 행동 언어다("Day 1 은 체크인만", "3박이라 세탁일을 두지 않는다"). 다만 같은 페이지에 숙소명 3회·주소 2회가 나온다 — STAY 카드 + staySummary + 챕터 리듬 표. 리듬 표는 접혀 있어 완화되나 정보 소유권은 정리되지 않았다 |
| 2 | 쉽게 낡는 정보를 고정하지 않으면서 실행 가능한가 | **PASS** | "약국·생필품점은 특정 상호를 고정하지 않는다. 필요할 때 숙소 주변의 현재 영업점을 지도에서 확인한다" — 규칙 4 와 실행성을 동시에 만족한 좋은 처리다 |
| 3 | 교통권 추천이 실제 일정·2인 조건에 맞는가 | **FAIL** | 승차 횟수 과소집계(§4) 위에 결론이 서 있고, 챕터의 "각자 T-casual" 권고와 정면 충돌한다(B2) |
| 4 | 요금 체계를 오해하게 만들 표현이 없는가 | **PASS WITH NOTES** | 공항/시내/근교 분리는 정확하고 "통합권은"·"일부 메트로 개찰구" 같은 한정도 정확하다. 다만 ① 단일권을 사라고 권한 직후 "통합권은 75분 3회 환승" 이 이어져 자기 표에 환승이 붙는다고 읽힐 여지 ② Airport ticket 가격(€5.90)과 비통합 성격 미표기 ③ T-familiar 30일·동행 조건 미표기 |
| 5 | 모바일에서 결론→비교→이용법→예외→Day 링크 순서가 이해되는가 | **PASS WITH NOTES** | 390px 실렌더 확인 — 순서 정확, 가로 오버플로 0, 콘솔 오류 0. 상품 카드가 한 장씩 쌓여 읽기 좋다. 다만 Day 링크가 44pt 미만이다(B1) |
| 6 | 중복보다 연결인가 | **FAIL** | 연결(Day 링크 8개)은 잘 됐으나, 같은 페이지가 교통권을 두 번 서로 반대로 말한다(B2) |
| 7 | Nice 등으로 확장해도 출처·일정 귀속을 검증할 수 있는가 | **PASS WITH NOTES** | 구조는 일반화된다(지역 슬러그 키 · 스키마 · 출처+확인일). 확장 전 보완 필요 — §8 참조 |

---

## 6. 데스크톱 · 모바일 화면 검증

| 확인 항목 | 결과 |
|---|---|
| `도시 공공교통` 섹션 표시 | OK |
| 상품 카드 3개 + 공항 L9 불가 표기 | OK — 3장 모두 "공항 L9 불가" 배지 |
| 공식 출처 접기 영역 | OK — `<details>` 기본 접힘, 5건 + 확인일·재확인일 |
| Day 1~4 링크 | OK (B1 제외) |
| 콘솔 오류 | **0건** (390px·1024px) |
| 교통 섹션이 기존 숙박·장소·일정 섹션을 가리는가 | 가리지 않음 — STAY 뒤, 아코디언 앞에 삽입 |
| 가로 오버플로 | 0건 (6개 뷰포트) |
| 글자 11px 하한 | 통과 |
| 터치 타깃 44pt | **실패 6건** (B1) |

---

## 7. 회귀 테스트 결과

| 검사 | 이 브랜치 | origin/main | 판정 |
|---|---|---|---|
| `tests/test_stay_transport_guards.py` | **7 passed** | (없음) | 신규 |
| `build/site.py` | 통과 (356쪽) | 통과 | — |
| `scripts/generate_attributions.py --check` | 0 | 0 | — |
| `scripts/validate_map_data.py` | 0 | 0 | — |
| `scripts/validate_itinerary.py` | 0 | 0 | — |
| `scripts/validate_media.py` | 0 | 0 | — |
| `build/ux_check.py` | 0 | 0 | — |
| `build/content_audit.py` | 0 | 0 | **기저 실패 해소됨** |
| `build/pwa_check.py` | 0 | 0 | — |
| `build/viewport_check.py` | **6건 실패** | 통과 | **신규 회귀 (B1)** |
| `build/guards/run_all.py` G1 | FAIL 1건 | FAIL 1건 | 기저, 동일 |
| `build/guards/run_all.py` G2 | FAIL 381건 | FAIL 381건 | 기저, 동일 |

§9 요청대로 구분하면 — **G1·G2 는 기저 실패로 이번 변경과 무관**하다(수치까지 동일). `content_audit` 는 과거 `1f8bc8ed` 에서 exit 1 이었으나 현재는 양쪽 다 통과한다. **이번 변경이 새로 만든 실패는 `viewport_check` 하나뿐이다.**

요청 §8 지시에 따라 `build/test_validation.py` 는 실행하지 않았다.

### 신규 가드 품질

| 테스트 | 실질성 |
|---|---|
| `test_model_accommodation_consistency` | **실질적** — 숙소 값(주소·좌표·status)의 날짜 간 드리프트를 값으로 검사 |
| `test_region_transport_has_no_silent_truncation_or_cross_region_items` | **실질적** — 절단·혼입 회귀를 값으로 잡는다. 약점: 섹션 끝을 마커 첫 등장으로 자르므로 essentials/transit 이 없는 7개 지역에서는 부재 단언이 헐거워질 수 있다 |
| `test_transit_sources_are_official_and_scheduled_for_recheck` | 호스트 화이트리스트 + `recheckBy ≥ verifiedAt` 만 본다. **요금 값 자체와 `verifiedAt` 의 미래 날짜 여부는 검사하지 않는다** |
| `test_..._follow_schema` | 형식만 |
| `test_barcelona_public_transit_pilot_is_rendered` | 스모크 |
| 나머지 2건 | 링크 형식·day 귀속 |

**총평**: 레이아웃·귀속 회귀 가드로는 실질적이다. 그러나 **이번 검증이 찾은 결함 — B2 의 챕터 충돌, `itineraryUses` 라벨의 사실성, 근거 없는 Rodalies 문장 — 은 어느 테스트도 잡지 못한다.** 귀속 가드는 있고 사실 정합 가드는 없다.

---

## 8. Nice 확장 전에 반드시 바꿔야 할 것

1. **`text-link` 를 `btn btn-secondary` 로.** 지금 확장하면 도시 수만큼 뷰포트 실패가 늘어난다. (B1)
2. **챕터의 구 교통권·공항 권고를 먼저 정정한다.** 새 층을 얹기 전에 챕터를 정리하지 않으면 도시마다 자기모순이 복제된다. Nice 챕터의 Lignes d'Azur 서술을 착수 전에 점검할 것. (B2)
3. **승차 횟수를 leg 에서 기계적으로 세고, 그 수를 근거로 권고를 만든다.** 지금은 사람이 센 "한 번" 이 결론을 지탱한다. `needsReview` 에 남은 미확정 이동수단을 승차 후보로 집계해야 한다.
4. **일정에 없는 대안을 예외로 쓰지 않는다.** Rodalies 문장처럼 daily card 에 backup 이 없는 서술은 금지하고, 가드로 검사한다(`exceptions` 가 언급한 수단이 해당 지역 daily card 에 존재하는가).
5. **`itineraryUses` 링크를 `Day.url` 로 생성한다.** 현재 `render.py:987` 이 `day-{n:02d}.html` 을 하드코딩해 URL 규칙이 바뀌면 조용히 깨진다. 존재하지 않는 day 번호도 빌드를 통과한다.
6. **스키마 검증을 빌드 경로로 옮긴다.** 현재 `jsonschema` 검사는 테스트에만 있어 `build/site.py` 만 돌리면 스키마 위반이 통과한다.
7. **요금 값 가드를 추가한다.** 출처 호스트만이 아니라 `verifiedAt` 이 미래가 아닌지, `recheckBy` 가 여행 시작일(2026-08-29) 이전인지 검사할 것. 현재 재확인일 2026-08-28 은 적절하나 규칙으로 강제되지 않는다.
8. **공식 문서가 침묵하는 것은 쓰지 않는다.** 은행카드 단일권의 환승 가능 여부, 은행카드 검증 가능 역 목록은 공식 근거가 없다.

---

## 9. 요약

| 축 | 판정 |
|---|---|
| 사실 정확도 | 8/8 공식 출처 일치 — **강점** |
| 구조·확장성 | 스키마·출처·확인일 분리 타당 — **강점** |
| 일정 귀속 | 혼입 차단·절단 제거 확인 — **개선됨** |
| 일정 정합 | 승차 횟수 과소, 근거 없는 대안 1건 — **수정 필요** |
| 화면 일관성 | 같은 페이지가 반대 조언 — **차단** |
| CI | viewport_check 신규 실패 — **차단** |

차단 2건은 모두 국소 수정으로 해소된다. 해소 후 재검증을 권고한다.
