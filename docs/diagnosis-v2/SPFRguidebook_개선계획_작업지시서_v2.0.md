# SP-FR-guidebook — 단계적 개선계획 및 작업지시서 v2.0

**작성:** 2026-08-17 · **기준 진단:** `SP-FR-guidebook_콘텐츠_전수진단_v2.0.md`
**기준 커밋:** main @ `f0403b3` (PR #146 병합 후)
**실행 주체:** Claude Code (S0–S4) · Jason (§9)
**남은 기간:** 출발 2026-08-29까지 **12일**

---

## 0. 이 문서를 실행하기 전에 — 금지사항 5가지

이전 두 세션이 실제로 밟은 지뢰다. **읽지 않고 원고를 고치면 맞는 것을 틀리게 바꾼다.**

1. **`site/`를 직접 편집하지 말 것.** CI가 `source/`에서 재생성한다. main 직접 푸시 금지 — 브랜치 + PR.
2. **일정의 단일 진실은 `source/CURRENT/10_Core/03_Whole_Trip_Master_Itinerary_v1.2.md` 와 `itinerary.json` 이다.** `data/itinerary-places.csv`는 구간 전환일 4개(Day 19·23·27·43)가 밀려 있다. **CSV를 날짜 근거로 쓰지 말 것.**
3. **확인한 것만 확정으로 쓴다.** 공식 소스로 못 본 값은 추정하지 않는다. `{{badge:unverified}}` 로 둔다.
4. **일정을 바꾸는 판단은 Jason 확인을 받는다.** 임의 결정 금지.
5. **S1(오류 수정)을 S0(인프라)보다 먼저 하지 말 것.** 8/16 진단이 찾은 값 31건이 PR #146 재편 과정에서 사라진 것이 이 순서를 어긴 결과다. 그릇 없이 물을 부으면 또 샌다.

---

## 1. 전체 구조

```
S0  사실 인프라       place-facts.json · 토큰 · 가드 6종        8/17–8/18   ★선행
S1  P0 오류 22건 + critical 6건       인프라 위에서 수정 · 요일충돌 52건        8/18–8/21
S2  조사 큐 · 미검증    큐 생성 → 미검증만 조사 → DB 적재         8/21–8/24
S3  정보항목 공란       Cost·Hours 블록 · 식당 정보줄            8/24–8/27
S4  사진 · 등급 정리    라이선스 사진 · 등급 토큰 통일           병행
S5  D-2 최종 게이트     전 가드 GREEN · 신선도 검사              8/27–8/28
```

**각 단계 종료 조건은 "작업했다"가 아니라 "가드가 통과했다"이다.**

---

## 2. S0 — 사실 인프라 구축 (선행, 2일)

### T0-1. `data/place-facts.json` 생성

**스키마**

```json
{
  "$schema": "./place-facts.schema.json",
  "version": "1.0",
  "places": {
    "<placeId>": {
      "displayName": "표시명",
      "region": "avignon",
      "address": "주소 (Lonely Planet 정보줄용)",
      "phone": "+33 ...",
      "url": "공식 사이트",
      "facts": {
        "hours":       {"value":"", "source":"", "verified_at":"YYYY-MM-DD", "confidence":"official|secondary|unverified", "ttl_days":90},
        "closed":      {"value":"", "...":""},
        "price_adult": {"value":"", "...":""},
        "booking":     {"value":"", "...":""},
        "getting_there":{"value":"", "...":""},
        "duration":    {"value":"", "...":""}
      }
    }
  }
}
```

**시드 데이터 (그대로 적재할 것 — 재조사 금지)**

| 출처 | 건수 | 위치 |
|---|---:|---|
| 2026-08-16 확정 원장 | 약 90 | 진단 v2.0 §4-2 정답 열 + 핸드오프 §6 |
| 2026-08-17 신규 검증 | 75 | 별첨 `SP-FR_신규확정사실_v2.0.csv` (소스 URL·확인일 포함) |

`confidence`는 공식 사이트 확인분만 `official`. 접근 실패 8건은 **레코드를 만들되 `confidence:"unverified"` + `blocked_reason` 기록** — 다음 세션이 같은 도메인을 또 두드리지 않게 한다.

### T0-2. 토큰 참조 전환

빌드에 `{{fact:<placeId>.<key>}}` 치환기를 추가한다. 출력 형식:

```
{{fact:palais-des-papes.price_adult}}
→ €16 (통합권 €19.50)                          ← official, TTL 이내
→ €16 (통합권 €19.50) ⟳출발 전 재확인            ← official, TTL 초과
→ 미확인 — 현장 확인 필요                        ← unverified
→ 공식 확인 불가 — +33 4 90 27 50 00 문의        ← unreachable (전화 자동 삽입)
```

**전환 범위 (S0에서는 여기까지만)**: 필수·우선추천 등급 101곳의 `hours` / `closed` / `price_adult` / `booking`. 나머지는 S3에서 확장한다.

### T0-3. `data/decisions.json` — Jason 확정 결정 레지스터

```json
[
 {"id":"DEC-A01","date":"2026-08-16","decision":"Peralada 일정 제외",
  "forbidden_patterns":["페랄라다 17:30","Peralada 투어 예약","페랄라다 예약"],
  "required_patterns":["Day 5 오후 = Cadaqués"],
  "scope":["05_Girona_*.md"]},
 {"id":"DEC-A02","decision":"렌터카 9/19(토) 조기 반납",
  "forbidden_patterns":["9/20 09:00 반납","9월 20일 09:00 반납","무인 키드롭"],
  "scope":["06_Nice_*.md","09_Avignon_*.md","10_Lyon_*.md"]},
 {"id":"DEC-A03","decision":"Saint-Paul-de-Vence → 9/8 Nice 당일치기",
  "forbidden_patterns":["9/9 생폴","Aix 챕터 Saint-Paul"], "scope":["06_Nice_*.md","07_Aix_*.md"]},
 {"id":"DEC-A04","decision":"Philharmonie de Paris 제외", "forbidden_patterns":["필하모니 밤","Philharmonie 공연"], "scope":["11_Paris_*.md"]},
 {"id":"DEC-A05","decision":"Bourse de Commerce 편입 (€15·화요일 휴관)", "scope":["11_Paris_*.md"]},
 {"id":"DEC-A06","decision":"Cadaqués 확정 방문지", "forbidden_patterns":["카다케스 — 본 일정에서 제외","왜 뺐나: 거리다"], "scope":["05_Girona_*.md"]},
 {"id":"DEC-A07","decision":"Avignon 체류 9/16–9/20", "forbidden_patterns":["9/17–9/21","9월 17일–9월 21일"], "scope":["09_Avignon_*.md"]}
]
```

### T0-4. 가드 6종 (`build/guards/`)

| ID | 스크립트 | 검사 | 실패 처리 |
|---|---|---|---|
| G1 | `guard_weekday.py` | `itinerary.json`으로 Day↔요일 표 생성 → 각 엔트리 방문일 요일 vs `closed` 대조 | **빌드 실패** |
| G2 | `guard_hardcode.py` | `{{fact:}}` 밖의 `€\d`, `\d{1,2}:\d{2}`, 요일 리터럴 검출 (허용목록 `build/guards/allow_hardcode.txt`) | **빌드 실패** |
| G3 | `guard_required_fields.py` | 필수·우선추천 등급인데 hours/closed/price/booking 미참조 | 경고 → **8/22부터 실패** |
| G4 | `guard_conflict.py` | 같은 `placeId.fact_key`가 원고에 2개 이상 다른 값 | **빌드 실패** |
| G5 | `guard_decisions.py` | `decisions.json`의 `forbidden_patterns` 잔존 검출 | **빌드 실패** |
| G6 | `guard_freshness.py` | `verified_at + ttl_days` 초과 사실 목록 출력, 배지 자동 강등 | 경고 |

**TTL 기본값**: 요금 180 · 정규 운영시간/휴관 90 · 특별전·이벤트 30 · 교통 시각표/운임 30 · 식당 영업일 60.

### T0-5. 배포 파이프라인 수정 (미완 항목)

`.github/workflows/pages.yml`:
- `paths:` 필터에 **`data/**` 추가** (없으면 데이터만 바꾼 커밋이 배포되지 않는다 — S0~S2가 전부 데이터 작업이다)
- `workflow_dispatch`에 **브랜치 가드 추가** (아무 브랜치에서 수동 실행 시 라이브가 덮인다)
- `concurrency`에 `cancel-in-progress: false`
- 푸터에 빌드 SHA 노출

### S0 완료 조건

```bash
python3 build/build.py && python3 build/hig_check.py
python3 build/guards/run_all.py --report
```
- `place-facts.json`에 시드 165건 적재 · 스키마 검증 통과
- 가드 6종 실행 가능 (이 시점 FAIL은 정상 — S1이 해소한다)
- G2가 검출한 하드코딩 건수를 baseline으로 기록

---

## 3. S1 — P0 오류 22건 + critical 6건 + 요일 충돌 52건 (3일)

**작업 단위는 "지역"이 아니라 "결함 유형"이다.** 유형별로 전 챕터를 한 번에 훑어야 같은 사실의 다중 하드코딩을 다 잡는다.

### T1-1. 날짜 체계 통일 (최우선)

| 대상 | 작업 |
|---|---|
| Avignon | 예약카드·확인목록·대체안의 **9/17–9/21 → 9/16–9/20**. **본문 일정표는 이미 옳으므로 건드리지 말 것** |
| Paris | **Day 번호 이중화 해소** — 여행 전체 Day 27–42 단일 체계로. 파리 내부 Day 1–17 표기를 전량 변환. 이것이 '필수 4곳 실종'의 원인 |
| Paris | 10/1·10/6 이중 배치 해소 — 도시에 절과 실행표 중 하나로 확정 (Jason 확인 필요) |
| 전 챕터 | `data/itinerary-places.csv` 재생성 — `scripts/extract_itinerary_places.py`의 전환일 배정 버그 수정 (도착 구간에 배정) |

**검증**: G1 통과 + `itinerary.json` ↔ 마스터 일정표 ↔ 각 챕터 Day 헤딩 3자 대조 스크립트 신설.

### T1-2. 렌터카 반납 (Avignon·Nice·Lyon 3개 챕터)

- **9/19(토) 18:15까지 Hertz Avignon TGV 반납** (토 09:00–19:00, 버퍼 45분). 주차 = Parking Loueurs P0
- **"무인 키드롭" 서술 전량 삭제** — 제공 여부 미확인
- **9/20(일) 아침**: TER "Virgule" Avignon Centre → TGV, 5–6분 €4, 일요일 08:44/09:13/10:13/10:44 → **09:13 권장**. 예비 택시 €12–15(전날 예약)
- **"Avignon TGV 셔틀 없음" 서술 삭제** — Virgule 실재. Orizo 10번은 일요일 무운행이 맞음
- **전제**: Jason의 Hertz 전화 확정(§9-1)이 선행. 미확정이면 `{{badge:unverified}}` 처리 후 진행

### T1-3. Jason 확정 결정 잔재 제거 (G5로 검출)

| 결정 | 잔존 위치 |
|---|---|
| Peralada 제외 | Girona '한눈에 보기' 표, 체류 리듬 "필수 예약: 17:30 투어", Day 2 동선도, 예약 카드, 우천 대체 |
| Cadaqués 확정 | Girona '배제한 대안 루트' E "왜 뺐나: 거리다", 대안표 "Day 3 전체 교체". **전용 dossier 신규 작성 필요** |
| Saint-Paul → 9/8 Nice | Aix 챕터 dossier·Day 12 경로(L74·89·254·349–386·1414–1422) 제거, Nice 9/8로 이설. **Grasse는 9/9 유지** |
| Philharmonie 제외 | Paris L978 "9/30 BnF 오전 + 필하모니 밤" 잔재 |
| Bourse 편입 | Paris — €15·화요일 휴관 명기. **8/26–10/5 전시 준비기간** 확인 필요 (10/3 배치 시 충돌) |

### T1-4. 요일 충돌 52건 (G1으로 일괄 검출)

**확정 충돌 — 즉시 교체**

| 지역 | 항목 | 조치 |
|---|---|---|
| Lyon | 9/22(화) 우천 대안 = Beaux-Arts (화 휴관) | 다른 실내 시설로 교체 |
| Lyon | 9/21(월) 우천 대안 = Gadagne (월·화 휴관) | 교체 |
| Lyon | Cathédrale Saint-Jean 월요일 13:15 방문 | 14:00 이후로 이동. 천문시계 작동시각 추가 |
| Barcelona | Palau de Maricel 9/1(화) | **관람 불가** — 가이드투어 전용·9–6월 일요일만. 일정에서 제외하거나 Museu de Maricel로 대체 |
| Girona | Pals 시간의 탑 15:20–16:10 | 점심 휴관대. 10:30–14:30 또는 17:00–20:00으로 이동 |
| Nice | Acchiardo 9/5(토) 저녁 | 월–금만 영업 — 다른 식당으로 교체 |
| Paris | 10/5(월) Marché Convention 권유 | 화·목·일 운영 — 시장 교체 또는 날짜 이동 |
| Paris | Marché d'Aligre 월요일 배치 | 월 휴무 |
| Paris | Orsay 9/29·10/6 이중 배치 | 본문 원칙("같은 미술관 두 번 안 간다")과 충돌 — 하나로 |
| Paris | L1557 교체표 "화요일 Orsay 또는 Orangerie 택1" | 오랑주리 화요일 휴관 — 잔존 오류 삭제 |
| Luberon | 9/16 농가 체류 전제 서술 (식사·러닝·수영) | 9/16은 Avignon 체크인일 — 전량 삭제 |
| Aix | Cassis Gorguettes 셔틀 9/11(금) | 9월 평일 미운행 — 대체 주차안 신설 |
| Aix | Atelier Cézanne 11:00 + €9.50 자율 | 존재하지 않는 조합. 가이드 €12·90분으로 확정 + 시간블록 85분→90분 |

**나머지 39건은 "영업일 미확인"** — S2 조사 큐 P0로 이관.

### T1-5. 2026 요금 갱신 (`place-facts.json`에만 기입)

| 시설 | 원고 | 확정값 |
|---|---|---|
| Palais des Papes 결합권 | €17 | **€19.50** |
| Palais des Papes 단독 | €14.50 / €12 | **€16** |
| Pont du Gard | "야외 €8" | **부지·다리 무료 / 주차 €9 / 실내 €8** |
| Lignes d'Azur (Nice) | €1.80 / €5 / €15 / €40 | **€1.70(74분) / 1일 €7 / 7일 €20** |
| Navigo | €88.80 / €32.40·€2.55·€14 (3값) | **Mois €90.80 / Semaine €32.40 / 단발 €2.55** (IDFM 2026-01-01) |
| Versailles | 공란 | **Passport 고시즌 €35 · 트리아농 €15 · 분수쇼일 정원 €15** |
| Musée Granet | €7 | **€14 단일** (7/4–11/1, 상설 단독권 없음) |
| ZBE Barcelona | €7 · 과태료 €1,800 | **€5 등록 · €2/일 · 과태료 100유로부터** |
| Louvre | — | **비EEA €32 · 화요일 휴관** |
| Sacré-Cœur 돔 | pending | **10:30 개방 · €8 · 현장판매만 · 계단 300개** |
| Bourse de Commerce | pending | **€15 · 화요일 휴관 · 11:00–19:00(금 21:00)** |
| Sant Pau | pending | **09:30–18:30 · €18(14시 전)/€17(14시 후)** |
| Girona 성벽 | "상시 개방" | **9–5월 08:00–21:00** |
| Halles Paul Bocuse | "09:00–22:00" | **대부분 월–토 07:30–19:30 · 월요일 다수 휴무** |
| Musée des Tissus | "비엔날레 예외 개관 ✓" | **확정 서술 삭제** — 공식은 "폐관 중"만 안내 |

### T1-6. 문서 내부 충돌 해소 (G4로 검출)

Girona Day 3 동선 2버전 · Day 3 점심 장소 충돌 · Calella 지위 3중 충돌 · Lyon 저녁 오프바이원 · Barcelona 사그라다 타워 권고 4중 상충 · Paris 근교 편성 충돌 · Bourse 확인상태 모순.

> **이 유형은 값 수정이 아니라 "어느 쪽이 맞나"를 정하는 일이다. 일정이 바뀌는 것은 Jason 확인 후 진행.**

### S1 완료 조건

- **G1·G4·G5 ALL GREEN**
- G2 하드코딩 건수가 S0 baseline 대비 **필수·우선추천 101곳에서 0건**
- P0 오류 22건 전량 `place-facts.json` 반영 + 원고 토큰 참조 확인

---

## 4. S2 — 조사 큐 · 미검증 항목 (3일)

### T2-1. `data/verify-queue.csv` 자동 생성

```bash
python3 build/build_verify_queue.py
```

| 열 | 값 |
|---|---|
| `placeId` · `fact_key` | 대상 |
| `status` | `MISSING` / `STALE`(TTL 초과) / `CONFLICT` / `BLOCKED`(접근 실패 기록) / `FRESH` |
| `priority` | P0(확정 일정 영향: 확정 등급 + 휴관·영업일·예약의무) / P1 / P2 |
| `last_attempt` · `blocked_reason` · `phone` | 재시도 억제용 |

**생성 규칙: `FRESH`와 `BLOCKED`는 조사 대상에서 자동 제외한다.** 이것이 중복 조사를 막는 지점이다.

### T2-2. 조사 실행 — 3원칙

1. **큐에 없으면 조사하지 않는다.** 큐 밖 항목을 조사했다면 그것은 중복이다.
2. **P0부터.** 예상 P0 약 45건 — 요일 충돌 미확인 39건 + 접근 실패 재시도 대상.
3. **공식 소스만.** 실패 시 `BLOCKED` + `blocked_reason` 기록하고 **우회 시도 금지.** 전화번호가 있으면 `phone` 열에 넣어 §9로 넘긴다.

**조사 배분**: 지역별 병렬 에이전트. 각 에이전트에게 **`place-facts.json`과 자기 지역 큐만** 준다. 원고 전문을 다시 읽히지 않는다 — 그 자체가 중복이다.

### T2-3. 적재

조사 결과는 원고가 아니라 **`place-facts.json`에만** 쓴다. 원고는 이미 토큰을 참조하므로 자동 반영된다.

### S2 완료 조건

- 큐의 P0 전량이 `official` 또는 `BLOCKED`(사유·전화번호 기록)
- **같은 사실을 두 번 조회한 로그가 0건** — `verify_log.csv`로 검사
- 신규 조사 건수를 기록 (다음 세션의 baseline)

---

## 5. S3 — 정보항목 공란 채움 (3일)

### T3-1. 관광지 — Cost·Hours 블록 강제

필수·우선추천 **101곳** 전체에 Rick Steves형 블록을 생성한다. **값이 없어도 블록은 만든다** — 빈 칸이 보여야 채워진다.

```markdown
> **요금** {{fact:x.price_adult}} · **운영** {{fact:x.hours}} · **휴관** {{fact:x.closed}}
> **예약** {{fact:x.booking}} · **소요** {{fact:x.duration}} · **가는 법** {{fact:x.getting_there}}
```

**목표**: A5·A6·A7·A8을 41%·37%·44%·32% → **필수·우선추천 등급에서 100% 블록 존재** (값 미확인은 배지로 명시).

### T3-2. 식당·시장 — Lonely Planet형 정보줄

**124곳** 전체에 한 줄 정보줄. 현재 최악 구간이다(B3 12.5% · B5 14.8% · B4 27.4%).

```markdown
> 📍 {{fact:x.address}} · 🚶 {{fact:x.getting_there}} · 🕐 {{fact:x.hours}} · 휴무 {{fact:x.closed}} · {{fact:x.booking}} · {{fact:x.price_range}}
```

**우선순위**: ① 확정 예약 있는 곳 ② 일정에 고정 배치된 곳 ③ 후보군.

### T3-3. 서술 보강 — 400자 미만 확정 엔트리

Cadaqués(dossier 없음) · Tossa de Mar · Sant Feliu de Guíxols · Les Baux · Sacré-Cœur · Cathédrale Saint-Jean · Passages couverts 등. **A2·A10은 이미 강점이므로 이곳들만 평균 수준으로 올리면 된다.**

### S3 완료 조건

- **G3 ALL GREEN** (필수·우선추천 등급 필수항목 블록 100%)
- 식당·시장 124곳 정보줄 100% 존재
- 전체 정보항목 충족률 49.1% → **75% 이상**

---

## 6. S4 — 사진·등급 정리 (병행)

### T4-1. 사진 102곳 누락

`data/images/image-manifest.csv`는 115장뿐이다. **필수(60) + 우선추천(41) 중 미보유분 우선**으로 Wikimedia Commons 등 라이선스 확보. 라이선스·저작자·변경사항 기록은 기존 매니페스트 형식을 따른다.

목표: 필수 등급 60곳 **사진 100%**.

### T4-2. 등급 표기 통일

80종 이상으로 흩어진 표기를 **`{{grade:essential|priority|optional|alternative|excluded}}` 5종**으로 정규화한다.
- **Girona 챕터는 `{{grade:}}` 토큰이 0개** — 헤딩 접미사 전량 토큰화
- 무등급 60곳: 등급을 부여하거나 데이터에서 제외 (Rick Steves식 선별)
- 완료 후 G3가 등급 기준으로 동작 가능해진다

### T4-3. 배지 3분할

`{{badge:pending}}` 282건을 `unverified` / `unreachable` / `field-recheck`로 분리. **"복수 출처 확인 완료"로 쓰인 pending은 전량 재검토** — Nice 교통요금 사고의 원인이다.

---

## 7. S5 — D-2 최종 게이트 (8/27–8/28)

```bash
python3 build/build.py
python3 build/hig_check.py
python3 build/guards/run_all.py --strict
python3 build/guard_freshness.py --trip-start 2026-08-29
```

| 검사 | 기준 |
|---|---|
| G1–G5 | ALL GREEN |
| G6 신선도 | TTL 초과 사실 전량 배지 강등 또는 재확인 |
| 정보 충족률 | 필수·우선추천 등급 ≥ 95% |
| `BLOCKED` 항목 | 전량 전화번호 + 현장확인 안내 문구 부착 |
| 배포 | `gh-pages` 반영 확인 + 빌드 SHA 일치 |
| 오프라인 | PWA 캐시에 최신 반영 |

---

## 8. 단계별 산출물

| 단계 | 산출물 |
|---|---|
| S0 | `data/place-facts.json` · `data/decisions.json` · `build/guards/*.py` · `pages.yml` 수정 |
| S1 | 8개 챕터 수정 PR · `S1_ERROR_FIX_REPORT.md` (21건 × 전후 값) |
| S2 | `data/verify-queue.csv` · `verify_log.csv` · `place-facts.json` 증분 |
| S3 | 챕터 블록·정보줄 PR · 충족률 전후 비교표 |
| S4 | `image-manifest.csv` 증분 · 등급 정규화 diff |
| S5 | `D2_FINAL_GATE_REPORT.md` |

---

## 9. Jason 직접 처리 항목 — Claude 불가

**전부 D-12 시점에서 지연 중이다. §3 T1-2가 9-1에 의존한다.**

| # | 항목 | 마감 | 상태 |
|---|---|---|---|
| 1 | **Hertz Avignon TGV 9/19(토) 조기 반납 확정** — +33 4 32 74 62 80. 계약 반납일이 9/20이면 변경 필요 | **즉시** | S1 블로커 |
| 2 | **Hertz Nice 인수지 확정** — 공항 T2 vs Nice-Ville (문서에 두 값 공존). 공식 위치 페이지 404로 확인 불가 | **즉시** | |
| 3 | **Luberon 농가 숙소 문의** — 문의문이 **4박 기준으로 남아 있다**("13 to 17 September", "four-night stay"). **3박(9/13–16)으로 고쳐 발송** | **즉시** | |
| 4 | **Abbaye de Sénanque** — 자유관람은 예약 불필요(€3.50)로 확인됐다. **가이드 투어를 원하면** tickeasy 예약 필요 | 즉시 | 방침 확인 |
| 5 | **Versailles 티켓 종류 확정** — Passport €35 vs 궁전 단독 | 즉시 | |
| 6 | **Paris 10/1·10/6 이중 배치 결정** — 세잔전/카사트전을 도시에 절 날짜로 갈지 실행표 날짜로 갈지 | 즉시 | S1 블로커 |
| 7 | **식당 전화 확정** — JU(미슐랭 1스타, 26석) · La Mérenda(SevenRooms, 월–금) · Daniel et Denise Créqui · Bar Cañete(8/31 월요일 영업 확인 불가) · Casa Marieta(화요일 저녁 영업 미확인) · La Roca Peratallada | 출발 전 | |
| 8 | Barcelona 공항 Groundforce 파업 상황 확인 (야간 도착 19:10) | D-2 | |

---

## 10. 완료 판정 — "했다"가 아니라 "통과했다"

| 단계 | 판정 명령 | 기준 |
|---|---|---|
| S0 | `guards/run_all.py --report` | 6종 실행 성공 · 시드 165건 적재 |
| S1 | `guards/run_all.py` | G1·G4·G5 GREEN · 필수등급 하드코딩 0 |
| S2 | `verify_queue_report.py` | P0 잔여 0 (official 또는 BLOCKED) · 중복 조회 0 |
| S3 | `guards/run_all.py --strict` | G3 GREEN · 충족률 ≥ 75% |
| S5 | `D2_FINAL_GATE` | 전 항목 GREEN |

**보고 원칙**: 검사한 항목만 보고한다. 빌드 통과를 "정보 충실도 확보"로 말하지 않는다. 진단 결과를 정정할 때는 정정 이력을 남긴다.

---

## 11. 시간이 부족할 때 — 자르는 순서

D-12는 넉넉하지 않다. 잘라야 한다면 이 순서로 자른다.

| 우선 | 절대 자르지 말 것 |
|---|---|
| 1 | S1 T1-1(날짜) · T1-2(렌터카) · T1-4(요일 충돌 확정분) — **현장에서 문이 잠기거나 차를 못 돌려주는 항목** |
| 2 | S0 T0-4 G1·G5 — 위 항목의 재발 방지 |
| 3 | S2 P0 조사 (식당 영업일) |

| 후순위 | 잘라도 여행은 된다 |
|---|---|
| 1 | S4 T4-1 사진 (읽는 재미의 문제) |
| 2 | S3 T3-3 서술 보강 (이미 강점 영역) |
| 3 | S4 T4-2 등급 통일 (여행 후 가능) |

**단, S0 T0-1(place-facts.json)만은 자르지 말 것.** 이것을 자르면 이번 진단의 결과도 다음 구조 변경에서 또 사라진다.
