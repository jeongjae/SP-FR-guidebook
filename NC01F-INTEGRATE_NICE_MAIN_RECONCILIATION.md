# NC01F-INTEGRATE — Nice 최종 main 통합

**작성일** 2026-08-23 · **브랜치** `fix/nice-region-editorial-consolidation`
**상태** 구현·QA 완료 · **merge/deploy 하지 않음** · 외부 Editorial Review 최종 승인 대기

Nice 의 editorial 내용(NC01·NC01F)은 이미 PASS 다. 이 문서는 그 뒤로 두 번 더
앞서 나간 main(Girona→Aix→**Luberon**→**Avignon**)과의 Git/SOT 통합 기록이다.

---

## 1. latest origin/main SHA

`a6f8886bf8db443e2c9e89dfd08262fac1a749cc`
(`Merge pull request #214 from jeongjae/fix/avignon-region-editorial-consolidation`)

직전 NC01F 라운드 때 반영했던 `86e479b9`(Luberon 까지) 보다 한 지역(Avignon,
AV01+AV01F) 더 앞서 있었다.

---

## 2. Conflict 발생 파일

**2건 — 둘 다 예상된 지점이었다.**

1. `data/region-consolidation.json` — 매 지역 세션이 자기 항목을 추가하는 파일이라
   구조적으로 매번 충돌한다.
2. `source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md` — **이번에
   처음 충돌했다.** 이유: `DEC-A02`/`DEC-A08`의 `scope`에 `"06_Nice_*.md"`가
   포함돼 있어서, Avignon 세션(AV01F, "렌터카 반납 SOT 정규화")이 렌터카 반납
   시각을 고칠 때 **Avignon 자기 챕터뿐 아니라 scope 에 걸린 Nice 챕터의 해당
   문장까지 함께 고쳤다.** 내 브랜치는 그 문장을 옛 날짜(9/19)인 채로 갖고
   있었으므로 같은 두 줄에서 충돌했다.

`data/decisions.json`은 **자동 병합됐다** — DEC-A02/A08(main 이 고친 레코드)과
DEC-A03(내가 고친 레코드)이 서로 다른 위치라 텍스트 겹침이 없었다.

---

## 3. 각 conflict 해결 내용

### 3.1 `data/region-consolidation.json`

`consolidated` 배열·`layerTitles`·`notes` 세 곳 모두 **양쪽을 합쳤다** — 어느
쪽도 ours/theirs 전체선택하지 않았다.

- `consolidated`: `barcelona, girona, aix, luberon, avignon, nice` (기존 5개 보존
  + nice 추가)
- `layerTitles`: girona·aix·luberon·avignon 4개 항목을 그대로 옮기고 `nice` 항목만
  NC01F 의 §8 정규화 값으로 추가
- `notes`: 같은 방식. **luberon 의 note 는 main 쪽 최신값을 썼다** — 내 쪽 문구는
  LB01F 반영 이전의 오래된 문구였다("외부 편집 검토 반영(LB01F)" 이 없었다).
  구버전으로 되돌리지 않기 위해 main 값을 그대로 채택했다.

### 3.2 `source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md`

**두 지점 모두 main(9/17) 쪽을 채택했다.** 지시문 §2 가 명시적으로 "Nice branch
의 오래된 9/19 18:15… 절대 main 위로 되돌리지 않는다"고 지정했다.

| 위치 | Before(내 쪽, 9/19) | After(main 쪽, 채택) |
|---|---|---|
| §예약·비용·안전·주차·귀가 렌터카 반납 줄 | "9/19(토) 18:15까지 Avignon TGV (토요일 영업 09:00–19:00, 버퍼 45분)" | "9/17(목) 저녁 Avignon TGV (목요일 영업 08:00–21:00, 18:30 이전 반납 완료, Parking Loueurs P0) — 계획상 9/17 저녁 반납 확정(DEC-A08), 기존 예약은 9/20으로 되어 있어 출발 전 변경 필요." |
| Day 6(9/9) 실행표 "반납" 셀 | "9/19(토) 18:15까지 조기 반납" | "9/17(목) 저녁 조기 반납(DEC-A08, 기존 예약 변경 필요)" |

두 지점 다 **렌더되지 않는 절**이다(§예약·비용… 은 promote 대상이 아니고, Day
실행표는 promote_regions 의 추출 대상이 아니다) — 어느 쪽을 택하든 Region 화면에는
안 나오지만, 정본 원고 자체가 낡은 값을 담고 있으면 안 되므로 main 값을 채택했다.

---

## 4. 최종 DEC-A02/A08/A03 값

| ID | 값 |
|---|---|
| DEC-A02 | 렌터카 9/17(목) 저녁 조기 반납 — Avignon TGV Hertz (18:30 이전) |
| DEC-A08 | Hertz Avignon TGV 렌터카 9/17(목) 저녁 반납 확정 (여행계획 SOT: 9/17 저녁 반납, Hertz 예약은 출발 전 변경 필요) |
| DEC-A03 | Saint-Paul-de-Vence 는 9/9 Nice→Aix 이동일(Day 12)에 Grasse 와 함께 있다. 9/8(Day 11)은 Villefranche-sur-Mer·Villa Ephrussi de Rothschild·Èze 당일치기다. (`also_check_daily_cards: true` 유지, 검사 대상 66건) |

세 레코드 모두 원문 그대로 확인했다(`python3 -c` 로 직접 로드해 출력, 아래 §6 에
근거).

---

## 5. PR mergeable 여부

**MERGEABLE.** `git merge-base --is-ancestor origin/main HEAD` 통과 — 최신
`origin/main`(`a6f8886b`)이 이 브랜치의 조상이다. push 후 GitHub 쪽 `mergeStateStatus`
도 확인한다(§ 완료 후 실행 로그 참조).

---

## 6. 전체 QA

### 지시문 §6 필수 확인 항목

| 조건 | 결과 | 근거 |
|---|---|---|
| PR mergeable = true | ✅ | §5 |
| DEC-A02 = 9/17 | ✅ | "렌터카 9/17(목) 저녁 조기 반납" |
| DEC-A08 = 9/17 | ✅ | "9/17(목) 저녁 반납 확정" |
| DEC-A03 = Saint-Paul 9/9 | ✅ | "9/9 Nice→Aix 이동일(Day 12)" |
| Day 11 = Villefranche/Ephrussi/Èze | ✅ | `day-11.json` stops 직접 확인, 변경 없음 |
| Day 12 = Saint-Paul/Grasse/Aix | ✅ | `day-12.json` stops 직접 확인, 변경 없음 |
| Nice-Ville rental pickup 유지 | ✅ | Day 12 stop "Nice-Ville역 Hertz 렌터카 인수" 그대로 |
| Nice Region 에 Palais ALZIRA 금액 노출 = 0 | ✅ | `site/guide/nice.html` 에서 `809.54` 검색 0건 |
| Barcelona/Girona/Aix/Luberon/Avignon entry 손실 = 0 | ✅ | `region-consolidation.json` 6개 지역 키 전부 존재, `set(consolidated)==set(layerTitles)==set(notes)` 확인 |
| broken links = 0 | ✅ | 사이트 전체 HTML 전수 스캔(372쪽), 깨진 내부 링크 0건 |
| manuscript residue = 0 | ✅ | `manuscript_residue_check.py` PASS — 통폐합 완료 6지역(aix·avignon·barcelona·girona·luberon·nice) 전부 흔적 0 |
| viewport overflow = 0 | ✅ | Nice 페이지 6개 뷰포트(360~1440px) 직접 측정, 전부 overflow=false |
| Nice 변경으로 인한 신규 guard failure = 0 | ✅ | 아래 §7 |

### 자동 검사 전체

| 명령 | 결과 |
|---|---|
| `build/site.py` | PASS — 372쪽 · 색인 191건 |
| `pytest tests/` | PASS — 30 |
| `build/region_structure_check.py` | PASS |
| `build/media_lookup_check.py` | PASS |
| `build/table_loss_check.py` | PASS |
| `build/content_audit.py` | PASS — 콘텐츠 손실 0 |
| `build/manuscript_residue_check.py` | PASS |
| `build/ux_check.py` | PASS |
| `build/viewport_check.py` | PASS |
| `scripts/generate_attributions.py --check` | PASS |
| `scripts/validate_map_data.py` | PASS |
| `unittest test_validation` | PASS — 20 |
| `scripts/validate_itinerary.py` | PASS — 43일 · 42박 |
| `scripts/validate_media.py` | PASS |
| `build/pwa_check.py` | PASS |
| `build/guards/run_all.py` | FAIL `['G2','G3','G4']` — §7 참조 |

---

## 7. Pre-existing main failures (Nice 무관)

`guards/run_all.py`가 `['G2','G3','G4']`로 실패한다.

- **G2·G3** — main 에서도 기존 FAIL(사실 인프라 S0~S3 진행 중). Nice 이전부터
  반복 확인된 상태.
- **G4 — Luberon 세션의 결함, Nice scope 아님.**
  `08_Luberon_Farmhouse_v2.0.md:270 Village des Bories — 원고 ['6.00'] vs facts
  ['4.00', '8.00']`.

  **diff 로 확인**: `git diff a6f8886b HEAD -- source/CURRENT/20_Regional_Chapters/
  08_Luberon_Farmhouse_v2.0.md data/place-facts.json` → **0줄**. 이 두 파일은
  merge 전후로 `origin/main`과 바이트 단위로 완전히 동일하다 — 내 브랜치가
  Luberon 챕터나 관련 facts 를 단 한 줄도 건드리지 않았다는 뜻이다. 최신
  `origin/main` 자체에 이미 있던 실패이고, 지시문 §5 에 따라 **고치지 않았다.**

- **G1·G1c·G4(이전)·G5·G6는 무관하거나 PASS.** G5는 DEC-A03 회귀검사를 포함해
  PASS — 검사 대상이 53건(NC01F 이전) → 66건(daily-cards opt-in 스캔 추가 후)으로
  늘었을 뿐 실패는 없다.

**Nice 변경으로 인한 신규 실패는 0건이다** — G4 하나가 FAIL 목록에 있지만
Nice 이전(main 자체)부터 있던 것이지 이번 통합으로 새로 생긴 것이 아니다.

---

## 8. Changed files

**이번 NC01F-INTEGRATE 라운드에서 실제로 고친 파일**

- `data/region-consolidation.json` — conflict 수동 해소(6개 지역 항목 보존 + 정렬)
- `source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md` — conflict
  해소, 렌터카 반납 두 문장을 main(9/17) 값으로 통일
- `source/CURRENT/20_Regions/nice.md` — 생성물 재생성(빌드 커밋)

**최신 main 반영(병합)으로 함께 들어온 파일** — Avignon 세션 산출물. 직접
수정하지 않았다: `AV01_AVIGNON_RECONSOLIDATION_QA.md` · `data/decisions.json`
(자동 병합, §2) · `data/region-essentials.json` ·
`source/ARCHIVE/20_Regional_Chapters/09_Avignon_Planning_Residue_v1.0.md` ·
`source/CURRENT/20_Regional_Chapters/09_Avignon_Alpilles_Pont_du_Gard_v2.0.md` ·
`source/CURRENT/20_Regions/avignon.md`

---

## 9. New head SHA

커밋 이력(이번 라운드):

1. `d962888b` — Merge remote-tracking branch 'origin/main' (Avignon 반영,
   region-consolidation.json + Nice 챕터 conflict 수동 해소)

이 보고서 커밋을 포함한 최종 head 는 push 로그에 기록한다(아래).

---

## STOP

merge/deploy 하지 않는다. 다음 지역(Lyon·Paris)도 시작하지 않는다.
외부 Editorial Review 최종 승인을 기다린다.
