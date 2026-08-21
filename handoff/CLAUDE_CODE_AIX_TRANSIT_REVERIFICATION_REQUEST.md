# Aix-en-Provence · Marseille 공공교통 재검증 요청

대상 브랜치: `codex/aix-transit`  
대상 커밋: `7bb3a4b8eaa2c80692e369aa25791d6cc4832265`  
이전 판정: `handoff/CLAUDE_CODE_AIX_TRANSIT_VERIFICATION_RESULT.md` — **FAIL (차단 1건)**

## 검증 원칙

- 검증자는 코드를 수정하지 않는다.
- 공식 출처, daily card, 지역 원고, 실제 렌더 결과를 독립적으로 교차 대조한다.
- 이전 보고서를 그대로 신뢰하지 말고 대상 커밋에서 다시 확인한다.
- 결과는 `handoff/CLAUDE_CODE_AIX_TRANSIT_REVERIFICATION_RESULT.md`에 기록한다.

## 1. 이전 차단 이슈 재검증

`data/daily-cards/day-15.json`의 `food`와 `highlights`가 Marseille 전일 일정과 일치하는지 확인한다.

필수 확인:

- `08:50 전후 Aix Centre발 TER`
- `Vieux-Port·Le Panier·Mucem 도보축`
- `RTM 60번으로 Notre-Dame de la Garde`
- `토요 큰 시장`, `Atelier 예약`, `스케치·수영`이 Day 15 데이터와 렌더 화면에 없어야 한다.
- 음식 안내가 Vieux-Port 점심과 Aix 귀환 후 가벼운 저녁으로 일치해야 한다.

## 2. 폐기 원고 재유입 검사

`source/CURRENT/20_Regional_Chapters/07_Aix_en_Provence_v2.0.md`에서 다음 현재 구조가 일관적인지 확인한다.

- Day 13 / 9월 10일: Aix 시장·Atelier·Granet, 도보
- Day 14 / 9월 11일: Cassis·Calanques, 렌터카
- Day 15 / 9월 12일: Marseille, TER·RTM
- Day 16 / 9월 13일: Lourmarin·Luberon, 렌터카

다음 폐기 표현은 없어야 한다.

- `9/11 Marseille`
- `Marseille — 오래된 항구`
- `시장, Atelier de Cézanne`
- `Day 15 스케치`
- `Marseille 버스`
- Day 15의 시장·Atelier·수영·스케치 일정

## 3. Day 12–16 이동수단 직접 대조

각 daily card의 모든 `legs[].mode`를 직접 읽어 아래와 일치하는지 확인한다.

| Day | 허용 mode 집합 |
|---|---|
| 12 | `car`, `walk` |
| 13 | `walk` |
| 14 | `car`, `walk` |
| 15 | `train`, `bus`, `walk` |
| 16 | `car` |

Day 15에서는 다음도 확인한다.

- 세 도보 leg의 `line`이 모두 `null`
- Vieux-Port→Notre-Dame은 RTM 60
- Vallon des Auffes→Saint-Charles는 RTM 83 + Metro M1
- L50은 확정 leg가 아니라 TER 장애 시 대안으로만 존재

## 4. 회귀검사·실렌더

```bash
python3 -m unittest tests.test_stay_transport_guards -v
python3 build/site.py
python3 build/viewport_check.py
python3 build/pwa_check.py
```

실제 화면을 최소 390px와 1440px에서 확인한다.

- `guide/aix.html`
- `daily/day-14.html`
- `daily/day-15.html`

검사 항목:

- Day 15 `오늘의 핵심`이 Marseille 일정인지
- 과거 Aix 토요일 생활일 문구가 노출되지 않는지
- 가로 넘침, 겹침, 잘린 버튼, 콘솔 오류가 없는지
- Day 12–16 링크가 모두 정상인지

## 5. 최종 판정

- 이전 차단 이슈가 남거나 현재 일정과 충돌하는 문구가 노출되면 `FAIL`.
- 공식 사실·일정·렌더·회귀검사가 모두 일치하면 `PASS`.
- 비차단 개선점은 `NOTE`로 분리하고 배포 차단 여부를 명시한다.
