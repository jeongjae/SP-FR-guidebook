# Aix-en-Provence · Marseille 공공교통 — 독립 재검증 결과

재검증일 2026-08-22 · 대상 커밋 `7bb3a4b8` (`fix(guide): align Aix Day 15 with Marseille plan`)
이전 판정 `CLAUDE_CODE_AIX_TRANSIT_VERIFICATION_RESULT.md` = **FAIL** (차단 1건)
검증 중 코드 수정 없음 · 일회용 worktree 에서 대상 커밋을 직접 체크아웃해 실행

---

## 최종 판정

# PASS

**차단 이슈가 해소됐고 신규 회귀는 없다.** 이전 검증이 지적한 가드 구멍 3개까지 함께 메워졌다.

| 항목 | 이전 | 이번 |
|---|---|---|
| Day 15 화면 자기모순 | 「오늘의 핵심」이 구안(시장·아틀리에·스케치) | **해소** |
| 챕터 일별 섹션 구안 | `9/11 Marseille` · `9/12 아틀리에` | **해소** |
| Day 12–16 mode 대조 | 가드 사각 | **가드가 직접 검사** |
| 도보 leg `line=null` | 1개 검사 누락 | **3개 전부 검사** |
| 회귀 | — | **0건** |

---

## 1. 이전 차단 이슈 재검증 (해소)

`data/daily-cards/day-15.json` 이 마르세유 전일 일정으로 교체됐다.

```
highlights:
  08:50 전후 Aix Centre발 TER
  Vieux-Port·Le Panier·Mucem 도보축
  RTM 60번으로 Notre-Dame de la Garde

food:
  Vieux-Port에서 생선·해산물 점심
  Aix 귀환 후 숙소권에서 가벼운 저녁

totalDistance: 약 74km · TER 왕복 + 마르세유 시내 대중교통·도보
```

요청서가 명시한 5개 필수 항목이 모두 충족된다. `totalDistance` 도 이전에 지적한 "거리값이 아닌 문장" 에서 거리값을 포함한 형태로 바뀌었다(NOTE-5 반영).

**구안 문구는 데이터에서 0건이다.**

| 문구 | `day-15.json` |
|---|---:|
| 토요 큰 시장 | **0** |
| Atelier 예약 | **0** |
| 스케치 | **0** |
| 수영 | **0** |

### 렌더 화면 확인

`daily/day-15.html` 의 「오늘의 핵심」이 실제로 이렇게 나온다.

```
오늘의 핵심
  08:50 전후 Aix Centre발 TER
  Vieux-Port·Le Panier·Mucem 도보축
  RTM 60번으로 Notre-Dame de la Garde
```

같은 페이지 전체 텍스트에서 `토요 큰 시장` · `Atelier 예약` · `스케치` · `수영` 이 **각 0회**이고, `Marseille` 27회 · `Mucem` 14회 · `RTM 60` 2회다. **페이지가 더 이상 자기 자신과 모순되지 않는다.**

---

## 2. 폐기 원고 재유입 검사 (통과)

`07_Aix_en_Provence_v2.0.md` 의 일별 섹션이 현재 일정과 일치한다.

| 섹션 | 제목 | 정본 일정 | 판정 |
|---|---|---|---|
| `## 18. Day 2 — 9월 10일` | 시장, Vieil Aix와 Musée Granet | Day 13 도보 | **일치** |
| `## 19. Day 3 — 9월 11일` | **Cassis·Calanques 차량 당일치기** | Day 14 렌터카 | **일치** |
| `## 20. Day 4 — 9월 12일` | **Marseille — Vieux-Port·Le Panier·Mucem·Notre-Dame** | Day 15 TER·RTM | **일치** |
| `## 21. Day 5 — 9월 13일` | Aix 체크아웃, Lourmarin을 거쳐 Luberon 농가로 | Day 16 렌터카 | **일치** |

두 섹션 모두 "Day 14 실행카드를 정본으로 사용한다" · "Day 15 실행카드를 정본으로 사용한다" 로 시작해 **카드를 정본으로 명시**한다 — 챕터와 카드가 갈라지는 구조 자체를 없앴다.

요청서가 지정한 폐기 표현 전수 검사.

| 표현 | 챕터 |
|---|---:|
| `9/11 Marseille` | **0** |
| `Marseille — 오래된 항구` | **0** |
| `시장, Atelier de Cézanne` | **0** |
| `Day 15 스케치` | **0** |
| `Marseille 버스` | **0** |

이전 검증이 렌더되지 않는 잔재로 지적한 `:1086` · `:1114` 가 실제로 정리됐다(챕터 77줄 삭제·재작성).

---

## 3. Day 12–16 이동수단 직접 대조 (전부 일치)

각 카드의 `legs[].mode` 를 직접 읽어 대조했다.

| Day | 날짜 | 실제 mode | 허용 집합 | 판정 |
|---|---|---|---|---|
| 12 | 9/9 | `car`, `walk` | `car`, `walk` | **일치** |
| 13 | 9/10 | `walk` | `walk` | **일치** |
| 14 | 9/11 | `car`, `walk` | `car`, `walk` | **일치** |
| 15 | 9/12 | `train`, `bus`, `walk` | `train`, `bus`, `walk` | **일치** |
| 16 | 9/13 | `car` | `car` | **일치** |

### Day 15 leg 정밀 검사

| leg | mode | line | 요구사항 | 판정 |
|---|---|---|---|---|
| aix-station → vieux-port | train | `TER Aix-en-Provence Centre ↔ Marseille Saint-Charles` | — | 적정 |
| vieux-port → le-panier | walk | **null** | 도보 `line=null` | **충족** |
| le-panier → fort-saint-jean | walk | **null** | 〃 | **충족** |
| fort-saint-jean → marseille-lunch | walk | **null** | 〃 | **충족** |
| marseille-lunch → notre-dame | bus | `RTM 60 Vieux-Port → Notre-Dame de la Garde` | RTM 60 | **충족** |
| notre-dame → vallon-des-auffes | bus | `RTM bus … · 당일 경로 확인` | — | 미확정을 헤지 |
| vallon-des-auffes → marseille-station | bus | `RTM 83 + Metro M1 → Marseille Saint-Charles` | RTM 83 + M1 | **충족** |
| marseille-station → aix-stay-return | train | `TER …` | — | 적정 |

**L50** — `day-15.json` 전체 등장 1회이고, **`legs` 안에는 0회**이며 `backup` 의 "TER 지연/파행 시" 항목에만 있다. 확정 동선이 아니다. **충족.**

### 공식 근거 (이전 검증에서 확인, 이번에도 유효)

- Notre-Dame 접근 **60번** — 바실리카 공식 "prendre le bus N° 60 … 20분 간격"
- Aix en Bus **€1.20** · 최대 5명 · 매 승차·환승 검증 — aixenbus.fr
- RTM **€1.70** · 최대 5명 · 60분 환승 · 같은 결제수단 재검증 — rtm.fr
- L50 **€7**, TER 와 별개 체계 — 메트로폴 공식 PDF
- 83번은 Corniche·Vieux-Port 축이며 **Notre-Dame 접근 노선이 아니다** — 데이터가 83 을 Vallon des Auffes→Saint-Charles 에만 쓰므로 오용 없음

---

## 4. 회귀검사 결과

대상 커밋을 그대로 체크아웃해 실행했다.

```
python3 -m unittest tests.test_stay_transport_guards -v
  Ran 13 tests — OK          (이전 12건 → 13건)

python3 build/site.py         완료: 369쪽 · 검색 색인 189건
python3 build/pwa_check.py    0
python3 build/ux_check.py     0
python3 build/content_audit.py 0
python3 build/viewport_check.py
  뷰포트 [360, 390, 430, 768, 1024, 1440] × 페이지 11개
  가로 오버플로 0 · 터치 타깃 44pt 이상 · 글자 11px 이상 — 통과
```

**신규 회귀 0건.**

### 이전 검증이 지적한 가드 구멍 3개가 모두 메워졌다

| 이전 지적 | 이번 |
|---|---|
| day-12/13/14/16 카드를 읽지 않는다 | **`assertEqual(expected, {leg["mode"] for leg in payload["legs"]})`** — 다섯 날 mode 집합을 직접 대조 |
| `fort-saint-jean → marseille-lunch` walk leg 이 `None` 검사에서 빠졌다 | **`assertIsNone(lines[("fort-saint-jean", "marseille-lunch")])`** 추가 |
| stale 목록이 diff 에 과적합됐다 | **`day15_text` 에 대한 `assertNotIn(stale, ...)`** 추가 · `assertEqual(day15["highlights"], [...])` 로 highlights 자체를 고정 |

`highlights` 를 `assertEqual` 로 고정한 것은 이번 차단 이슈의 재발을 구조적으로 막는다.

---

## 5. 실렌더 화면 확인

| 폭 | 페이지 | 가로 넘침 | 콘솔 오류 |
|---|---|---:|---|
| 390px | guide/aix.html · daily/day-14.html · daily/day-15.html | **0px** | 없음 |
| 1440px | 동일 | **0px** | 없음 |

- Day 15 「오늘의 핵심」이 **마르세유 일정**이다(§1).
- 과거 Aix 토요일 생활일 문구 노출 **0건**.
- 겹침·잘린 버튼 없음(`viewport_check` 가 6개 폭에서 터치 타깃 44pt·글자 11px 하한 통과).
- 지역 가이드의 Day 링크 **12·13·14·15·16 전부** 존재.

---

## 6. NOTE (배포 비차단)

이전 검증의 NOTE 중 미해결분과 이번에 확인된 것.

| # | 내용 | 차단 여부 |
|---|---|---|
| N1 | Aix 1시간 환승은 **비접촉 전용 페이지에 분 단위 명시가 없다**. 일반 승차권 규정 + CGVU 준용이 근거다 | 비차단 |
| N2 | **L50 시각표 PDF 가 2026-07-10 까지만 유효**하다. 여행일(9/12)이 범위 밖이므로 9월 개정판 확인 필요 | 비차단 · **출발 전 확인** |
| N3 | RTM 비접촉 **CGVU(2023-08-09 판)가 아직 "1인 1카드"** 로 되어 있어 현행 5인 안내와 어긋난다. 현장 분쟁 여지 | 비차단 · **출발 전 확인** |
| N4 | **RTM 은 매년 9월 망을 개편한다**(83번이 2025-09 에 82번 대체). 2026-09 개편 공지 확인 | 비차단 · **출발 전 확인** |
| N5 | Day 14 `sourceStatus` 가 `candidate-latest-needs-review` 인데 챕터는 Cassis 를 기본안으로 쓴다. 등급과 상태가 어긋난다 | 비차단 |
| N6 | `notre-dame → vallon-des-auffes` 의 헤지 문구("당일 경로 확인")는 가드가 검사하지 않아, 나중에 확정형으로 바뀌어도 통과한다 | 비차단 |

N2·N3·N4 는 콘텐츠 결함이 아니라 **출발 전 재확인 대상**이다. 배포를 막지 않는다.

---

## 7. 요약

| 축 | 결과 |
|---|---|
| 이전 차단 이슈 | **해소** — 데이터·화면 모두 0건 |
| 폐기 원고 재유입 | **0건** — 챕터 일별 섹션이 카드를 정본으로 선언 |
| Day 12–16 mode | **전부 일치** |
| Day 15 leg 정밀 | 도보 3개 `null` · RTM 60 · 83+M1 · L50 격리 — **전부 충족** |
| 회귀 | **0건** (테스트 13종 · 게이트 5종 · 뷰포트 6폭) |
| 가드 강화 | 이전 지적 구멍 **3개 모두 해소** |

배포를 막을 사유가 없다.
