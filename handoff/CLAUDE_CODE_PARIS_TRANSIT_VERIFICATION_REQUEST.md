# Claude Code 검증 요청 — Paris 숙박·교통

## 대상

- 브랜치: `codex/paris-transit`
- 검증 대상: 이 요청서가 포함된 브랜치 최신 커밋
- 격리 워크트리에 직접 체크아웃하고 코드는 수정하지 않는다.

## 핵심 변경

15박 일정의 실제 이동량과 확정 CDG 택시를 기준으로 승차권 조합을 다시 계산했다. 9/24–27 개별권, 9/28–10/4 Navigo Weekly all zones 한 번, 10/5–8 개별권, 10/9 공식 택시가 정본이다. 기존 Weekly 2주 연속 권고는 제거했다.

## 독립 검증 항목

1. 2026년 Metro‑Train‑RER Ticket €2.55, Bus‑Tram Ticket €2.05, Navigo Weekly all zones €32.40, Airport Ticket €14가 IDFM 공식 자료와 일치하는지 확인한다.
2. Navigo Weekly가 구매일부터 7일이 아니라 월요일–일요일 고정인지 확인한다.
3. Weekly를 Navigo Easy에 넣을 수 없고 Navigo/Navigo Découverte 또는 호환 휴대전화가 필요한지 확인한다.
4. Metro‑Train‑RER Ticket의 2시간 내부 환승과 bus·tram 비연계 설명이 정확한지 확인한다.
5. Day 34 Versailles RER C가 9/28–10/4 all-zones Weekly 기간에 포함되는지 확인한다.
6. Day 42가 공식 택시 확정이므로 두 번째 Weekly와 Airport Ticket을 미리 사지 않는 판단이 일정과 비용 면에서 타당한지 확인한다.
7. Day 37의 mode가 `{bus, metro}`이고 Porte d’Auteuil까지 Metro 10, 이후 France Galop 무료 셔틀이라는 설명과 맞는지 확인한다.
8. `region-essentials`, `transit-facts`, Paris 원고, Day 27–42 카드가 서로 모순되지 않는지 확인한다.
9. Paris 지역 화면 390px·1440px에서 가로 넘침·콘솔 오류·Day 링크 누락을 확인하고 사이트·UX·콘텐츠 손실·viewport·PWA 게이트를 실행한다.

## 특별 주의

- 두 사람은 각자 승차 매체가 필요하다. Navigo Easy 한 장을 동시에 돌려 쓰는 안내가 없어야 한다.
- CDG 철도권은 비상안일 뿐 확정 동선이 아니다.
- 기존 main의 Nice Day 10과 Nice 전용 테스트 불일치는 Paris 판정과 분리한다.

## 판정 형식

- `PASS` 또는 `FAIL`
- 차단 이슈와 비차단 NOTE를 분리한다.
- 코드 수정 없이 검증 결과 문서만 작성한다.
