# NC01F — Nice 최종 사실 정합화

**작성일** 2026-08-23 · **브랜치** `fix/nice-region-editorial-consolidation`
**상태** 구현·QA 완료 · **merge/deploy 하지 않음** · 외부 Editorial Review 대기

NC01(구조) 은 PASS 수준이었다. 이 문서는 merge 전 남아 있던 canonical SOT 충돌
2건과 그에 딸린 문제들을 정리한다. NC01 보고서(`NC01_NICE_REGION_CONSOLIDATION_QA.md`)
는 그대로 두고, 이 문서가 최종 정합화 기록이다.

---

## 1. Overall Status

**PASS — 결정한 것 하나, 사용자 행동이 필요한 것 하나.**

- DEC-A03(Saint-Paul-de-Vence 날짜) — **해결.** Day SOT 를 유지하고 결정 레지스터를 뒤집었다.
- Palais ALZIRA 총액 — **증거상 확정됐지만 마지막 한 단계(트래커 반영)를 완료하지 못했다.**
  auto-mode 분류기가 xlsx 편집을 차단했다. 우회하지 않고 사용자 결정으로 넘긴다 (§6).

merge/deploy 하지 않았다. Girona/Aix/Luberon 이 이미 머지된 최신 main 을 반영했고
(§10), region-consolidation.json 충돌을 수동으로 해소했다.

---

## 2. DEC-A03 final decision

**결정: Day SOT 를 유지한다.** Saint-Paul-de-Vence 는 9/9(Day 12, Nice→Aix 이동일)에
Grasse 와 함께 있다. Day 11(9/8)에 Saint-Paul 을 추가하지 않았고, Day 12(9/9)에서
빼지도 않았다.

`data/decisions.json` 의 DEC-A03 을 갱신했다 — 새 레코드를 만들지 않고 레지스터
자신의 안내("결정이 뒤집히면 여기를 먼저 고친다")대로 이 레코드를 고쳤다.

| | Before | After |
|---|---|---|
| decision | "Saint-Paul-de-Vence → 9/8 Nice 당일치기" | "Saint-Paul-de-Vence 는 9/9 Nice→Aix 이동일(Day 12)에 Grasse 와 함께 있다. 9/8(Day 11)은 Villefranche-sur-Mer·Villa Ephrussi de Rothschild·Èze 당일치기다." |
| forbidden_patterns | `9/9 생폴` · `9/9 Saint-Paul` · `생폴드방스를 거쳐` | `9/8 Saint-Paul` · `9/8 생폴` · `Saint-Paul-de-Vence → 9/8` · `생폴드방스 → 9/8` · `생폴드방스는 9/8` |
| scope | `06_Nice_*.md` · `07_Aix_*.md` (그대로) | 그대로 |

### G5 가 원래 이 충돌을 놓친 이유

`build/guards/guard_decisions.py`(G5)는 `forbidden_patterns`의 **리터럴 부분 문자열**을
`chapter_files()`(= `source/CURRENT/20_Regional_Chapters/*.md`)에서만 찾는다.
실제 충돌은 `data/daily-cards/day-12.json`(가드가 안 보는 파일)이 9/9 에 Saint-Paul 을
두면서 생겼다 — 옛 forbidden_patterns(`9/9 생폴` 등)가 찾던 문구는 애초에 챕터
산문에 없었다(챕터는 항상 "생폴드방스"라고 썼지 "9/9 생폴"이라고 붙여 쓴 적이 없다).
즉 **패턴 자체가 처음부터 챕터 산문의 실제 표현과 맞지 않았다.**

### 추가한 회귀검사 (semantic scope 를 넓히지 않는 범위)

`guard_decisions.py`에 opt-in 필드 `also_check_daily_cards`를 추가했다. 이 필드가
`true`인 결정만 `data/daily-cards/day-*.json` 원문도 함께 스캔한다. DEC-A03 에만
켰다 — 다른 12건의 결정은 동작이 그대로다. 새로운 상시 크로스체크 프레임워크를
만들지 않았다.

**부정 픽스처로 확인했다.** `day-11.json` 사본에 `"생폴드방스는 9/8 Villefranche..."`
를 주입하고 실행:

```
[G5] FAIL · 확정 결정 잔재 — 1건 · 검사 대상 66
    · DEC-A03 day-11.json:42 '생폴드방스는 9/8' — Saint-Paul-de-Vence 는 9/9 Nice→Aix
```

파일은 즉시 원본으로 복원했다(`git diff` 로 확인, 변경 없음). 실제 빌드는:

```
[G5] PASS · 확정 결정 잔재 — 0건 · 검사 대상 66
```

### scope 밖에 남긴 것

챕터의 `## Day 5 — 9월 8일 화요일` 실행 섹션 표제가 여전히 "Nice 생활·회복일:
리베라시옹 시장…"이다. 이 섹션은 **어디에도 렌더되지 않는다**(promote_regions.py 의
추출 대상이 아니다) — NC01 QA §18 에서 이미 out-of-scope 로 기록했던 항목이고,
DEC-A03 의 새 forbidden_patterns 도 이 문자열을 잡지 않도록 일부러 좁혔다. Saint-Paul
날짜 문제와는 무관한 별개 결함이라 이번 정합화 범위 밖에 뒀다.

---

## 3. Day 11/12 final schedule

변경 없음 — Day SOT(`day-11.json`·`day-12.json`)가 이미 맞았다. 이번 작업은 **결정
레지스터를 Day SOT 에 맞춘 것**이지 일정 자체를 고친 것이 아니다.

| Day | 날짜 | 내용 |
|---|---|---|
| 11 | 9/8 | Villefranche-sur-Mer → Villa Ephrussi de Rothschild → Èze |
| 12 | 9/9 | Nice-Ville 역 Hertz 인수 → Saint-Paul-de-Vence → Grasse → Aix 체크인 |

---

## 4. Nice ↔ Aix transfer reconciliation

**이미 일치했다.** Aix 챕터(07, AX01/AX01F 로 이미 main 에 머지됨)를 직접 확인했다.

```
07_Aix_en_Provence_v2.0.md:42:  | 9/9 수 | Nice-Ville 렌터카 인수 · Saint-Paul-de-Vence · Grasse · Aix 체크인 |
07_Aix_en_Provence_v2.0.md:96:  #### Saint-Paul-de-Vence {{grade:priority|우선추천}}
07_Aix_en_Provence_v2.0.md:105: #### Grasse {{grade:optional|선택}}
```

Aix 세션은 Day SOT(9/9)를 그대로 따라 Saint-Paul-de-Vence·Grasse 를 둘 다 도착일
카드로 이미 갖고 있었다. **Nice↔Aix 간 실제 모순은 없었다** — 낡은 쪽은 오직
`decisions.json`의 DEC-A03 하나였다.

---

## 5. Palais ALZIRA amount evidence table

| 출처 | 값 | 성격 |
|---|---|---|
| Nice 챕터 / `build/confirmed_fact_manifest.json` CF006 | **€809.54** | 챕터 프로즈. 매니페스트 자체 설명 "니스 Airbnb 결제총액" |
| `TP_Europe_Travel_Master_Tracker_v1.2.xlsx` Reservations R003 | **총액 = 빈 값**, 결제액 = 0 | 비고: "총액 미기입은 기록 문제일 뿐 예약은 있다 · 실제총액 입력 시 예약완료로 잠근다" |
| git blame — commit `f32549a3` (2026-08-16) | "Nice Palais ALZIRA: 총액 €809.54 결제 완료·호스트 연락처 반영 ('총액 입력 결정' 배지 해소)" | **실제 예약서 대조 기록**. 커밋 메시지 제목이 "예약서 8건 대조 2차" — 이 라운드에서 8개 예약을 실물 확인서와 하나씩 맞춰봤다. Hertz·TGV 2편도 같은 라운드에서 확정됐다 |

**이전 NC01 보고서(직전 턴)의 주장은 오류였다.** "Prepare / 예약 트래커 = €433.82"라고
적었는데, €433.82 는 **Lyon**(Lagrange Aparthotel Lyon Lumière)의 확정 숙박비이지
Nice 와 무관하다 — `source/CURRENT/20_Regional_Chapters/10_Lyon_v2.0.md:142,146` 과
`TP_Europe_Travel_Guidebook_Decision_Register_v0.4.md` DEC-037 에 각각 있다. 렌더된
Prepare 페이지에서 두 지역의 숙소 카드가 나란히 나오는 것을 잘못 읽은 결과였다.
이 자리에서 정정한다.

**실제로는 두 값이 충돌하는 게 아니다.** 트래커의 총액 칸이 비어 있을 뿐, 그 칸이
"€809.54 가 아닌 다른 값"을 주장한 적이 없다. 트래커 스스로 이것을 데이터 갭이라고
적어 뒀다.

---

## 6. Canonical booking amount 판정

**Case A — €809.54 가 실제 예약 총액이다. 트래커의 빈 칸은 관리적 누락이다.**

근거: commit `f32549a3` 이 실물 예약서(2026-08 예약서) 대조로 이 값을 확정했다고
명시하고, 같은 라운드에서 확정된 다른 예약들(TGV 12176 PNR 4YMAGT, Hertz
L672E080313 등)도 전부 실제 확인 가능한 예약번호·세부조건을 동반한다 — 이 라운드
전체가 신뢰할 수 있는 대조 작업이었다.

### 완료한 것

- Nice 챕터 "구역별 이해와 숙소 생활권"(렌더되는 절)에서 €809.54 문장 제거
- 렌더되지 않는 "예약·비용·안전·주차·귀가" 절에 근거와 함께 남겨 `fact_guard`의
  CF006 요구(독자 정본 어딘가에 토큰이 살아 있어야 함)를 계속 충족시킨다:

  > **숙소 예약 (Airbnb — Palais ALZIRA)**: 총액 €809.54 결제 완료. 2026-08 예약서
  > 대조로 확인된 값이다(commit f32549a3, 2026-08-16). 호스트 Catherine
  > +33 6 21 70 18 70. 재확인: 트래커 R003 의 총액·결제액 칸이 비어 있다 — 예약
  > 자체는 있고 트래커 반영만 남았다. Prepare 정본이 채운다.

### 완료하지 못한 것 — 사용자 행동 필요

`TP_Europe_Travel_Master_Tracker_v1.2.xlsx`의 R003 행(총액·결제액 칸)을 €809.54 로
채우려 시도했으나, **auto-mode 분류기가 이 파일에 대한 쓰기를 차단했다.** 다른
방법으로 우회하지 않았다 — 이 xlsx 는 실명·전화번호·예약번호를 담은 예약 기록
파일이라 보호 대상으로 분류된 것으로 보인다.

**Region 은 이미 금액을 표시하지 않는다.** 다만 Prepare 페이지(`site/prepare/index.html`)
도 여전히 Palais ALZIRA 행에 "금액" 필드를 렌더하지 않는다 — 트래커가 비어 있는
그대로다. **사용자가 직접 트래커의 R003 행 총액·결제액을 809.54 로 채워야
Prepare 페이지에 반영된다.** 아래 편집을 대신 제안한다(위치는 `Reservations` 시트,
`ID=R003` 행, 열 K/M):

- 총액(K열): `809.54`
- 결제액(M열): `809.54`

---

## 7. Region 에서 숙박비 제거 여부

**제거했다.** `site/guide/nice.html`에서 `809.54` 문자열 검색 결과 0건.

---

## 8. Final visible headings

`data/region-consolidation.json`의 `layerTitles.nice`를 barcelona/girona/aix/luberon
과 같은 방식으로 맞췄다 — verdict 키를 추가하고(생성된 `20_Regions/nice.md`의 H2
텍스트에만 영향, 렌더된 페이지에는 영향 없음 — verdict 층은 render.py 에서 제목 없이
prose 로만 나온다), 나머지 넷을 §3 지정값으로 교체했다.

| 층 | Before | After |
|---|---|---|
| verdict | (없음) | Nice와 Côte d'Azur를 이렇게 본다 |
| overview | 일정 | 일정 (변화 없음) |
| neighborhoods | 숙소와 생활권 | 숙소와 생활권 (변화 없음) |
| transport_deep | 니스와 코트다쥐르에서 이동하기 | **Nice와 Côte d'Azur에서 이동하기** |
| food_culture | 니스에서 먹고 장보기 | **먹고 장보기** |

렌더된 페이지의 실제 접이식 제목(확인됨):

```
일정 · 먹고 장보기 · 숙소와 생활권 · Nice와 Côte d'Azur에서 이동하기
```

barcelona·girona·aix·luberon 과 완전히 같은 명명 규칙이다. 지역 전용 코드
분기는 만들지 않았다 — 전부 `data/region-consolidation.json`의 데이터다.

---

## 9. Barcelona side-effect reconciliation

**재검증 결과: 실질 정보 손실이 없다. 코드 변경 불필요.**

이전 NC01 보고서(직전 턴)는 "Nice의 `region_dishes()` 변경이 Barcelona의 '이 지역에서
먹는 것' 접이식 하나를 없앤다"고 보고했다. 이번에 다시 확인했다.

### 실제로 확인한 것

1. **`region_dishes()`는 이미 완전히 일반화돼 있다** — `is_consolidated(r.slug)` 하나만
   보고, 지역 이름을 하드코딩하지 않는다. barcelona·girona·aix·luberon·nice **다섯
   지역 모두** 렌더된 페이지에서 "이 지역에서 먹는 것" 접이식이 0건이다(직접 확인).
   이건 Nice 만의 예외가 아니라 통폐합을 끝낸 모든 지역에 적용되는 일관된 규칙이다.

2. **잃은 것으로 보였던 정보는 전부 다른 canonical 위치에 이미 있다.**
   - Barcelona 의 옛 목록 `제철 해산물 · 타파스 · 타파스·해산물 · 시장 장보기 · 과일·빵 ·
     arroz a banda`는 각 항목이 **식당 카드의 '추천 메뉴' 필드**(예: Bar Cañete 카드
     "추천 메뉴: 소꼬리 샌드위치, 풋고추 튀김…", La Zorra 카드 "추천 메뉴: arroz a banda
     · 2인 공유")와 **챕터의 '카탈루냐에서 먹어볼 것'·'시장과 장보기' 절**(과일·햄·치즈·빵
     구입 목록 포함)에 이미 더 상세하게 있다.
   - girona·aix·luberon·nice 도 같은 구조다 — 각 챕터가 `~에서 먹어볼 것`(girona:
     "Empordà에서 먹어볼 것", aix: "프로방스에서 먹어볼 것", luberon: "농가에서 먹기",
     nice: "니스에서 먹어볼 것") 절을 이미 갖고 있고, 모든 식당 카드가 '추천 메뉴'를
     보여준다.

3. **이 원칙(§4 지시문)이 명시한 조건을 그대로 충족한다**: "'시장 장보기 · 과일·빵' 한
   줄이 다른 canonical 위치에 이미 존재하면 현 구조 유지 가능." — 존재를 확인했으므로
   구조를 그대로 둔다.

### 왜 다시 붙이지 않았나

옛 "이 지역에서 먹는 것" 목록의 각 항목은 사실 **바로 위 식당 카드의 '추천 메뉴'를
압축·재진술한 것**이었다(Bar Cañete 카드 "추천 메뉴: 소꼬리 샌드위치…" vs 목록의
"타파스·해산물"; La Zorra 카드 "추천 메뉴: arroz a banda" vs 목록의 "arroz a banda" —
동일 문구). 다시 붙이면 오히려 RC01~LB01 전체가 없애려 한 **정보 반복**을 되살린다.
Nice 를 위해 Barcelona 정보를 지운 것이 아니라, 다섯 지역이 이미 공유하던 일반
규칙이 Barcelona 에서도 정확히 같은 이유로 유효했다.

### 검증 방법

```
barcelona: '이 지역에서 먹는 것' 접이식 개수 = 0
girona:    '이 지역에서 먹는 것' 접이식 개수 = 0
aix:       '이 지역에서 먹는 것' 접이식 개수 = 0
luberon:   '이 지역에서 먹는 것' 접이식 개수 = 0
nice:      '이 지역에서 먹는 것' 접이식 개수 = 0
```

`content_audit.py`(콘텐츠 손실 감사)도 **손실 0**으로 통과했다 — 원문과 렌더 결과의
문단 대조가 이 결론과 독립적으로 같은 답을 낸다.

---

## 10. Latest-main integration / conflict result

`git fetch origin` 두 번 — 처음엔 Girona/Aix(PR #209/#210/#212)까지, 재확인 시
**Luberon(PR #213)까지** 추가로 머지돼 있었다. 최신 `origin/main`(`86e479b9`)을
반영했다.

### Conflict

**`data/region-consolidation.json` 1건 — 예상대로, 수동 해소.**

- `consolidated` 배열: `barcelona`(공통) 뒤에 내 쪽은 `nice`, main 쪽은
  `girona·aix·luberon`을 추가해 충돌. **양쪽을 모두 보존**하고 `nice`를 마지막에
  붙였다 — `barcelona, girona, aix, luberon, nice`.
- `layerTitles`·`notes`: 같은 구조로 병합. **girona·aix·luberon 의 기존 항목을
  하나도 지우거나 덮어쓰지 않았다** — 값 그대로 옮기고 `nice` 항목만 새로 추가했다
  (§8 의 정규화 반영).

### 그 외 파일

`build/render.py`·`build/model.py`·`build/promote_regions.py`·
`build/content_guard.py`·`data/region-essentials.json`·`source/ASSETS/91_Place_Registry_v1.0.md`
등은 **자동 병합**됐다 — 내 브랜치가 건드리지 않은 파일이라 충돌이 없었다.
`build/render.py` 자동병합을 직접 열어 확인했다: girona/aix/luberon 세션이 추가한
`layerTitles` 동적 로딩(`promote_regions.py`)과 `region_dishes()` 는 그대로 살아
있고, 내가 §2 에서 손댄 `guard_decisions.py`(가드 디렉터리, 별도 파일)와는 겹치지
않는다.

병합 후 `git status`에 `UU`/`AA`/`DD`(미해결 충돌) 0건 확인 후 커밋했다.

**다른 지역 브랜치의 변경사항을 cherry-pick 하지 않았다** — 전부 이미 main 에
머지된 상태를 그대로 반영(merge)한 것이지, 개별 커밋을 골라온 것이 아니다.

---

## 11. Full QA

| 명령 | 결과 |
|---|---|
| `build/site.py` | PASS — 372쪽 · 색인 191건 |
| `pytest tests/` | PASS — 30 |
| `build/region_structure_check.py` | PASS |
| `build/media_lookup_check.py` | PASS |
| `build/table_loss_check.py` | PASS |
| `build/content_audit.py` | PASS — **콘텐츠 손실 0** |
| `build/manuscript_residue_check.py` | PASS — barcelona·girona·aix·luberon·nice 흔적 0 |
| `build/ux_check.py` | PASS |
| `build/viewport_check.py` | PASS (표본 12쪽) |
| **Nice 전용 가로 오버플로 직접 측정** | PASS — 360/390/430/768/1024/1440px 전부 overflow=false |
| **사이트 전체 내부 링크 무결성** | PASS — 깨진 링크 0건 (전체 HTML 전수 스캔) |
| `scripts/generate_attributions.py --check` | PASS |
| `scripts/validate_map_data.py` | PASS |
| `unittest test_validation` | PASS — 20 |
| `scripts/validate_itinerary.py` | PASS — 43일 · 42박 |
| `scripts/validate_media.py` | PASS |
| `build/pwa_check.py` | PASS |
| `build/guards/run_all.py` | FAIL `['G2','G3','G4']` — 아래 참조 |

### guards/run_all.py 상세

- **G2·G3** — main 에서도 이미 FAIL(사실 인프라 S0~S3 진행 중, 여러 QA 문서에서
  반복 확인된 기존 상태). 내 변경과 무관.
- **G4 — 새로 FAIL, 그러나 내 변경과 무관.** `08_Luberon_Farmhouse_v2.0.md:270
  Village des Bories — 원고 ['6.00'] vs facts ['4.00', '8.00']`. 이건 **Luberon
  세션의 결함**이다. 내 브랜치는 Luberon 챕터를 한 줄도 건드리지 않았다(`git log
  86e479b9..HEAD -- .../08_Luberon_Farmhouse_v2.0.md` 결과 없음 확인). Git
  Integration Rule("다른 Region 브랜치의 변경사항을 임의로 수정하지 않는다")에 따라
  **고치지 않았다** — Luberon 은 내 담당 지역이 아니다. 다음 지역 작업이나 Luberon
  세션이 처리해야 한다.
- **G5 — PASS.** DEC-A03 회귀검사 포함해서 검사 대상 66건(이전 53건에서 증가 —
  daily-cards 스캔이 opt-in 으로 추가됐기 때문).

### §6 PASS 조건 (사용자 지시문 원문)

| 조건 | 결과 |
|---|---|
| Saint-Paul date contradiction = 0 | ✅ |
| DEC-A03 / Day 11 / Day 12 contradiction = 0 | ✅ |
| Nice / Aix transfer contradiction = 0 | ✅ (원래부터 없었음, §4) |
| Palais ALZIRA conflicting total visible in Region = 0 | ✅ (Region 에서 금액 자체를 뺐다) |
| booking SOT ambiguity = 0 또는 명시적 HOLD | **명시적 HOLD** — 증거는 Case A 를 가리키나 xlsx 반영이 분류기에 막혔다 (§6) |
| generated heading mismatch = 0 | ✅ |
| Barcelona content loss = 0 | ✅ (§9, 재검증 완료) |
| other consolidated Region regression = 0 | ✅ (girona·aix·luberon 렌더 확인, 접이식 개수 동일) |
| manuscript residue = 0 | ✅ |
| broken links = 0 | ✅ (전체 사이트) |
| horizontal overflow = 0 | ✅ (Nice 직접 측정) |

---

## 12. Changed files

**이번 NC01F 라운드에서 실제로 고친 파일 (3개 + 재생성 1개)**

- `data/decisions.json` — DEC-A03 갱신
- `build/guards/guard_decisions.py` — opt-in daily-cards 스캔 추가
- `source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md` — €809.54 문장을
  렌더되는 절에서 안 렌더되는 절로 이동
- `source/CURRENT/20_Regions/nice.md` — 생성물 재생성 (빌드 커밋)

**최신 main 반영(병합)으로 함께 들어온 파일** — Girona/Aix/Luberon 세션의 산출물.
직접 수정하지 않았다: `AX01_AIX_RECONSOLIDATION_QA.md` · `GR01_GIRONA_RECONSOLIDATION_QA.md`
· `LB01_LUBERON_RECONSOLIDATION_QA.md` · `build/content_guard.py` · `build/model.py`
· `build/promote_regions.py` · `build/render.py` · `data/region-essentials.json` ·
`source/ARCHIVE/20_Regional_Chapters/{05_Girona,07_Aix,08_Luberon}_Planning_Residue_v1.0.md`
· `source/ASSETS/91_Place_Registry_v1.0.md` · `source/CURRENT/20_Regional_Chapters/
{05_Girona_Collioure_Emporda_v2.1,07_Aix_en_Provence_v2.0,08_Luberon_Farmhouse_v2.0}.md`
· `source/CURRENT/20_Regions/{aix,barcelona,girona,luberon}.md` ·
`source/CURRENT/30_Places/{abbaye-de-senanque,calella-de-palafrugell,l-isle-sur-la-sorgue,
menerbes,oppede-le-vieux}.md`

**수동으로 병합 충돌을 해소한 파일 1개**: `data/region-consolidation.json`
(barcelona·girona·aix·luberon 항목 보존 + nice 항목 §8 정규화로 추가)

**시도했으나 분류기에 막혀 완료하지 못한 것**: `source/OPERATIONS/
TP_Europe_Travel_Master_Tracker_v1.2.xlsx`(R003 총액·결제액 칸) — §6 참조.

---

## 13. Head SHA

작업 중 커밋 두 개:

1. `42c0b8bb` — fix(nice): DEC-A03 를 Day SOT 에 맞춰 뒤집고 숙박 총액을 Region
   밖으로 뺀다 (NC01F)
2. `b84c2686` — Merge remote-tracking branch 'origin/main' (girona/aix/luberon 반영,
   region-consolidation.json 충돌 해소)

이 문서 커밋을 포함한 **최종 head SHA는 push 후 확정**한다 (§14).

---

## STOP

merge/deploy 하지 않는다. 다음 지역(Avignon·Lyon·Paris)도 시작하지 않는다.
외부 Editorial Review 승인을 기다린다.
