# FCR-04 — Day SOT 수정과 콘텐츠 종결 QA

기준 커밋 `fe3fa27e` (FCR-03). 작업 브랜치 `feat/fcr04-day-sot-corrections`.
푸시·머지·PR 은 하지 않았다.

---

## 1. Marché Convention 휴무일 충돌 수정 결과

**문제**  Day 29(2026-09-26 토) · Day 36(2026-10-03 토) 아침이 Marché Convention
장보기였다. 그런데 이 시장은 토요일에 열지 않는다.

**출처가 갈린다는 것부터 확인했다.**

| 출처 | 여는 요일 |
|---|---|
| Paris opendata `marches-decouverts` (구조화 등록부, 요일별 boolean) | 화·목·일 |
| paris.fr 편집 목록 | 화·목·토 |
| fact 가 인용하던 장비 페이지 URL | **404** |

두 공식 출처가 어긋난다. 그래서 **어느 한쪽을 정답으로 선언하지 않았다.**
일정은 두 출처가 **함께 인정하는 요일에만** 놓는다 — 화·목.

**조치**

| Day | 날짜 | 전 | 후 |
|---|---|---|---|
| 29 | 09-26(토) | Marché Convention 일요 시장 장보기 | **Marché Lecourbe** 토요 장보기 |
| 36 | 10-03(토) | Marché Convention 토요 장보기 | **Marché Lecourbe** 토요 장보기 |
| 39 | 10-06(화) | Standard Home Morning (일반) | **Marché Convention 화요 장보기** (`place_ref` 연결) |

빈 시간으로 두지 않았다. 두 토요일 모두 실제로 영업하는 시장 루틴이 들어갔고,
Convention 은 삭제된 것이 아니라 **실제로 여는 날로 옮겨 갔다**.

`data/place-facts.json` 의 `marche-convention.hours` · `closed` 는 두 출처의
불일치를 값 안에 남기고 재확인 안내를 붙였다. 확정처럼 쓰지 않았다.

## 2. 대체·재배치한 시장

**Marché Lecourbe** (48.8366, 2.2826 · 15구, 숙소권 안). 토요일 오전 영업.
Day 29·36 아침에 들어갔다. 명부에 없는 곳이라 `place_ref` 는 비웠다 —
장소 페이지를 새로 만들지 않았다(대량 승격 금지 조항).

**Marché Convention** 은 Day 39(화)로 옮겼고, 여기서만 `place_ref` 를 갖는다.
그래서 장소 페이지의 방문일 배지가 화요일 하나로 정리된다.

Paris 챕터 원고에도 토요일 대안 문장을 넣었다(11_Paris_Long_Stay L676).

## 3. La Paradeta Sagrada Família 최종 판정

**판정: RENAMED / 사업체 교체 — `REPLACED` 로 기록한다.**

근거

1. Google Maps 에서 같은 주소(Passatge de Simó 18)가 **Puertecillo Sagrada
   Família** 로 나온다 (2026-08-22 확인).
2. Puertecillo 공식 사이트가 **그 주소를 자기 지점으로 싣는다**
   — `puertecillo.es/puertecillo-sagrada-familia/`.
3. La Paradeta 공식 사이트(laparadeta.com)의 지점 목록에 **Sagrada Família 가
   없다**. Born 등 다른 지점만 남아 있다.
4. 업태(해산물 마리스케리아·즉석 조리)는 같지만 **상호·운영주체가 다르다.**

세 출처가 같은 방향을 가리키므로 AMBIGUOUS 가 아니다. Day SOT(Day 02 점심)와
명부·지도 질의·장소 원고의 표시 이름을 Puertecillo 로 바꿨다.
**슬러그와 원고 헤딩은 그대로 뒀다** — 옛 주소와 명부 대조가 깨지지 않게 한다.

옛 업소의 운영시간·가격은 **승계하지 않고 지웠다.** 새 업소의 값은 공식
페이지가 공개하지 않아 비어 있다(§6 참조). 사진은 신원 확인 후 새로 받았다.

## 4. Weibel 처리 (B안)

Day 13 의 stop 은 **분할하지 않았다.** `Stop.related_place_refs[]` 를
모델에 추가하고 시장 stop 에 `patisserie-weibel` 을 붙였다.

- 타임라인은 한 줄 그대로다. 아래에 `함께 보는 곳 — Maison Weibel` 링크만 붙는다.
- Weibel 장소 페이지는 Day 13 방문 배지를 받는다 (`place_visits` 가
  `related_places` 도 센다).
- 지역 가이드의 메뉴 카드도 관련 stop 의 메뉴를 읽는다.

**Barcelona·Aix 전용 분기는 없다.** `related_place_refs` 는 43일 전체가 쓰는
일반 필드이고, `model.validate` 가 (a) 없는 슬러그 (b) `place_ref` 와 같은 값을
막는다.

## 5. fold() 빈 정규화 구멍 — 수정과 검증

**구멍**  Google Maps 가 상호 대신 번역된 분류명('푸에스토시요 해산물 요리')을
돌려주면 `fold()` 결과가 빈 문자열이 되고, `"" in x` 는 항상 참이라 신원 대조가
**무조건 통과**했다. 그 구멍으로 다른 업소 사진이 La Paradeta 자리에 붙을 뻔했다.

**수정**  `build/identity_match.py` 로 규칙을 한 곳에 모았다.

```
MIN_TOKEN = 3
접힌 제목이 3자 미만 → 매치 실패 (판단 불가는 통과가 아니다)
접힌 후보가 3자 미만 → 그 후보는 버린다
부분일치는 양방향, 양쪽 모두 비어 있지 않을 때만
```

**회귀 테스트 6종** (`build/test_validation.py::TestIdentityMatch`)

| 테스트 | 검증 |
|---|---|
| 빈 fold 는 절대 매치 안 된다 | 한글 전용 제목 → False |
| 빈 후보는 무시된다 | 후보에 한글만 있어도 통과 안 됨 |
| 악센트·대소문자 접기 | `Maison Weibel` ↔ `MAISON WEIBEL` |
| 확인된 개명만 accept list 로 | `La Maison Pichard` |
| 다른 업소는 매치 안 된다 | La Paradeta ↔ Puertecillo → False |
| 짧은 잡음은 매치 안 된다 | 2자 토큰 → False |

전체 20 테스트 OK.

## 6. 남은 완결성 빈칸의 판정

`data/food-completeness-disposition.json` 에 전부 적었고,
`build/research_closure_check.py` 가 **판정 없는 빈칸 0** 을 강제한다.

| 항목 | 슬러그 | 판정 | 이유 |
|---|---|---|---|
| menu | mercat-concepcio | NOT_APPLICABLE | 공설 생활시장 — 고정 메뉴가 없다 |
| menu | mercat-del-lleo | NOT_APPLICABLE | 같은 이유 (60여 가판대 시립시장) |
| menu | casa-marieta | INTENTIONALLY_UNRESOLVED | 일정에 없는 추천 식당, stop 이 없어 출처가 없다 |
| price | la-paradeta-sagrada-familia | BLOCKED_WITH_EVIDENCE | 상호 교체로 옛 가격 승계 불가 · 새 업소는 가격 비공개 |
| visit_day | casa-marieta | INTENTIONALLY_UNRESOLVED | 일정에 잡히지 않은 추천 |
| visit_day | mercat-del-lleo | INTENTIONALLY_UNRESOLVED | 장보기 후보로만 든다 |
| photo | (전체) | RESOLVED | 24/24 · Maps 15 + 기존 검증 9 |

현재 상태 — 사진 24/24 · 설명 24/24 · 웹사이트 24/24 · 지도 24/24 ·
가격 23/24 · 메뉴 21/24 · 방문일 22/24. **무조건 24/24 를 만들지 않았다.**

## 7. G1/G2/G3 변화

| 가드 | FCR-03 기준 | FCR-04 | 변화 |
|---|---|---|---|
| G1 방문 요일 vs 휴관일 | 5 | **0 (PASS)** | −5 |
| G2 fact 토큰 밖 하드코딩 | 384 | 382 | −2 |
| G3 필수항목 참조 | 119 | 119 | 0 |
| G4 / G5 | 0 / 0 | 0 / 0 | PASS 유지 |

**새 회귀 0.**

G1 이 0 이 된 경위는 값을 지워서가 아니라 **판정 출처를 고쳐서**다.

1. `data/place-days.json` 이 **얼어붙은 진단 CSV**에서만 나왔다. 그래서
   일정을 고쳐도 옛 날을 들고 있었고, Convention 은 Day 39 로 옮긴 뒤에도
   CSV 의 Day 29(토) 기준으로 휴무 충돌을 냈다. 생성기를 고쳐 **명부에 있는
   장소는 Day SOT 가 CSV 를 덮게** 했다 (`build/build_place_days.py`).
   일정에서 빠진 19곳은 항목 자체를 지웠다.
2. 여러 날 가는 곳에서 **첫 날만 보고** 충돌을 부르던 헛경보를 고쳤다.
   Le Marais 는 월(지구 산책)·화(카르나발레) 둘 다 가는데 첫 날이 월이라는
   이유로 박물관 휴관을 충돌로 냈다. 이제 **예정된 날이 전부 닫혀 있을 때만**
   충돌로 본다 (`build/guards/guard_weekday.py`).
3. 남은 실제 충돌 하나를 고쳤다 — Day 08(09-05 토) 점심 요약이 주말 휴무인
   **Chez Acchiardo** 를 지목했다. Day SOT 요약과 Nice 챕터의 요리 목록을
   "월–금만 영업이라 토요일에는 불가" 로 바로잡았다. 대체 업소를 지어내지
   않았고, 챕터가 이미 검증해 둔 토요일 영업처(Chez Pipo)만 가리킨다.

## 8. 콘텐츠 손실 QA

기준 커밋 `fe3fa27e` 를 별도 워크트리에 빌드해 369쪽 전수 비교했다.

```
페이지: base 369 · new 369 · 사라진 페이지 0 · 새 페이지 0
문장이 사라진 페이지 12 · 사라진 문장 47
```

47건 전수 분류 — **의도치 않은 손실 0**.

| 분류 | 건수 | 페이지 |
|---|---|---|
| La Paradeta → Puertecillo 상호 교체 (옛 업소의 시간·가격·소개문 제거) | 26 | places/la-paradeta-…, guide/barcelona, daily/day-02, map/×2 |
| Marché Convention 재배치 (토요일 문구 제거·Day 39 이동) | 13 | daily/day-29·36·39, guide/paris, places/marche-convention |
| Acchiardo 토요일 충돌 문구 수정 | 5 | daily/day-08, guide/nice |
| 방문일 배지 문자열 변경 (9.26/10.3 → 10.6) | 3 | guide/paris, places/marche-convention |

전부 이번 작업이 의도한 교체다. 각 자리에는 대체 문장이 들어갔다(§1·§3).
`content_audit` 은 별도로 **승격 장문 손실 0** 을 확인한다.

## 9. 변경 파일

**모델·렌더·가드**
- `build/model.py` — `Stop.related_place_refs` · `Stop.related_places` · 검증
- `build/render.py` — 타임라인 '함께 보는 곳' · `place_visits` 가 관련 장소 포함
- `build/identity_match.py` *(신규)* — 업소 신원 대조 한 곳
- `build/build_place_days.py` — Day SOT 우선
- `build/guards/guard_weekday.py` — 예정일 전부 충돌일 때만 실패
- `build/research_closure_check.py` — 완결성 빈칸 판정 강제
- `build/region_structure_check.py` — 메뉴 집계가 관련 장소 포함
- `build/test_validation.py` — `TestIdentityMatch` 6종

**Day SOT·데이터**
- `data/daily-cards/day-02.json` (Puertecillo) · `day-08.json` (Acchiardo)
  · `day-13.json` (Weibel 참조) · `day-29.json` · `day-36.json` (Lecourbe)
  · `day-39.json` (Convention 화요)
- `data/place-facts.json` · `data/place-days.json` · `data/map-queries.json`
- `data/food-completeness-disposition.json` *(신규)*
- `data/images/*` · `source/ASSETS/photos/*` (Puertecillo 사진 1장)

**원고·명부**
- `source/ASSETS/91_Place_Registry_v1.0.md`
- `source/CURRENT/20_Regional_Chapters/04_Barcelona_Sitges_v2.0.md`
  · `06_Nice_Cote_d_Azur_v2.0.md` · `11_Paris_Long_Stay_v2.0.md`
- 파생물 재생성: `20_Regions/barcelona.md` · `nice.md` ·
  `30_Places/la-paradeta-sagrada-familia.md`

## 10. 빌드·테스트·가드 결과

| 검사 | 결과 |
|---|---|
| `build/site.py` | PASS · 369쪽 · 데일리 43 · 지역 8 · 검색 189건 |
| 인빌드 가드 (model.validate · vocabulary · place_prose · fact_guard · content_guard) | PASS |
| `region_structure_check` | PASS — 분류·섹션·방문일·링크 이상 없음 |
| `media_lookup_check` | PASS — 미매핑 0 · 조용히 사라진 사진 0 |
| `table_loss_check` | PASS — 조용한 열 손실 0 |
| `research_closure_check` | PASS — 잘못된 업소 사진 0 · 미분류 0 · 판정 없는 빈칸 0 |
| `guards/run_all.py` | G1 **PASS 0** · G2 382 · G3 119 · G4 0 · G5 0 · G6 WARN 0 |
| `test_validation.py` | 20 tests **OK** |
| `validate_itinerary.py` | PASS — 43일 · 42박 · 누락 0 · 중복 0 |
| `validate_media.py` | PASS |
| `validate_map_data.py` | PASS (경고 113 — 기존 Place ID 미확인) |
| `generate_attributions.py --check` | PASS |
| `ux_check.py` | PASS |
| `viewport_check.py` | PASS — 6뷰포트 오버플로 0 · 44pt · 11px |
| `content_audit.py` | PASS — 장소 134 · 문단 1142 · 손실 0 |
| `pwa_check.py` | PASS — 868개 파일 · 61.9 MiB · 전체 저장/오프라인 심층 탐색 통과 |

## 11. 남은 user decision

1. **Marché Convention 의 여는 요일** — opendata(화·목·일)와 paris.fr(화·목·토)가
   어긋난다. 지금은 겹치는 화·목만 쓴다. 일요일 또는 토요일 장보기를 넣고
   싶으면 현장 전화·구청 확인이 필요하다. 지어내서 채우지 않았다.
2. **Puertecillo 의 가격·운영시간** — 공식 페이지가 공개하지 않고 Google
   프로필로 넘긴다. Day 02 점심을 이대로 갈지, 다른 곳으로 바꿀지는 결정이 필요하다.
   업태는 같지만 **같은 가게가 아니다.**
3. **Le Marais 의 방문일이 원고와 Day SOT 사이에서 어긋난다** — 챕터는
   "Day 30(9/27 일) · Day 35(10/2 금)", Day SOT 는 Day 31·39 다. 이번 범위
   (Paris 일정 재작성 금지)에서 손대지 않았다. 어느 쪽이 맞는지 결정이 필요하다.
4. **G2 382 · G3 119 는 기존 부채다.** 이번에 늘리지 않았다. 별도 라운드로 뺀다.

---

여기서 중단한다.
