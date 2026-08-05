# Phase 8 — 예약·운영 잠금 완료보고서 v1.0

## 결론

Phase 8A **Known-Facts Lock**을 완료했다. 여행기간·숙박배분·확정된 일정 골격은 잠갔고, 사용자가 제공하지 않은 예약번호·정확한 주소·편명·열차번호·결제금액은 생성하거나 추정하지 않았다.

Phase 8B **Actual-Booking Lock**은 실제 예약서 입력 전까지 의도적으로 차단한다. 이 상태는 실패가 아니라, 미확정 정보를 확정값처럼 현장에서 사용하는 사고를 막기 위한 운영 통제다.

## 잠금된 기준값

| 항목 | 확정값 |
|---|---|
| 여행기간 | 2026-08-29~2026-10-10 · 43일/42박 |
| 거점별 숙박 | Barcelona 3 / Girona 3 / Nice 5 / Aix 4 / Luberon 3 / Avignon 4 / Lyon 4 / Paris 16박 |
| Nice/Aix 배분 | Nice 5박 · Aix 4박 |
| 운영 골격 | 9/8 Nice 회복일 · 9/9 NCE 출발 · 9/16 Avignon 체크인 · 9/20 Avignon TGV→Lyon · 9/24 Lyon→Paris |
| 시간계획 | Sagrada Família 8/30 10:30 · Peralada 9/2 17:30 · Paris 10/10 19:10 출국 계획 |

## 자동검사 계약

- Tracker 필수 시트 6개 존재
- 예약 레코드 `R001`~`R024` 24건 및 ID 고유성
- P0 예약항목 정확히 13건
- 8개 숙소의 체크인·체크아웃·박수 일치
- `예약완료` 표기 시 예약번호·사업자·출처·최종확인일 필수
- 숙소 `예약완료` 표기 시 실제총액·예약번호·주소·출처 필수
- `PARTIAL`·`BLOCKED` 항목에는 필요한 사용자 입력을 반드시 명시
- Tracker와 웹 배포본의 Known-Facts Lock 및 실제 예약 잠금률 일치

## Phase 8B 입력 대기

1. 국제선과 Girona→Nice 이동 예약서
2. Barcelona/Girona 및 Nice/Provence 렌터카 예약서
3. Avignon→Lyon, Lyon→Paris 열차표
4. 8개 숙소의 확정명·주소·예약번호·총액·취소기한
5. 핵심 입장권·Paris 공연·축구 예약정보
6. 여행자보험·통신 구매정보

> **2026-08-04 변경 게이트:** Luberon 기존 4박, Avignon·Lyon 체크인일, France 렌터카 반납일, Lyon행·Paris행 열차, Paris 기존 15박 예약은 자동 변경된 것으로 보지 않는다. 예약서가 갱신될 때까지 Tracker에서 `재확인` 및 `예약 변경 필요`로 유지한다.

입력값을 받으면 `TP_Europe_Travel_Master_Tracker_v1.2.xlsx`를 갱신하고 동일한 빌드 게이트를 통과시켜 Phase 8B를 잠근다.

## 판정

- Phase 8A Known-Facts Lock: **완료**
- Phase 8B Actual-Booking Lock: **사용자 예약자료 대기**
- 미확정값의 확정값 오인 방지: **자동검사 적용**
