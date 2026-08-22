# Claude Code 검증 요청 — Avignon 숙박·교통

## 대상

- 브랜치: `codex/avignon-transit`
- 검증 대상: 이 요청서가 포함된 브랜치 최신 커밋
- 격리 워크트리에 직접 체크아웃하고 코드는 수정하지 않는다.

## 핵심 변경

Avignon 시내 교통을 일정에 맞게 간결하게 정리했다. 성벽 안은 도보, Day 21은 렌터카, Day 22는 Arles TER가 정본이다. Day 23 차량 반납 세부는 사용자가 현장에서 처리하므로 변경 범위에서 제외했다.

## 독립 검증 항목

1. Orizo 2026–2027 공식 노선도·요금표에서 T1이 Gare Centre를 지나지만 Avignon TGV역까지 가지 않는지 확인한다.
2. P+R Piot–Porte de l’Oulle와 Italiens–Place Pie의 주차·지정 셔틀 무료 조건을 확인한다.
3. Day 22 Avignon Centre↔Arles TER를 Orizo와 혼동하지 않았는지 확인한다.
4. liO 115는 2026년 9월 시간표가 있지만 Day 21 Uzès+Pont du Gard 렌터카 일정을 그대로 대체한다고 쓰지 않았는지 확인한다.
5. 지역 원고, `region-essentials`, `transit-facts`, Day 19–23 카드가 서로 모순되지 않는지 확인한다.
6. 390px·1440px 지역 화면에서 가로 넘침·콘솔 오류·링크 누락을 확인하고 전체 사이트·UX·콘텐츠 손실·viewport·PWA 게이트를 실행한다.

## 특별 주의

- Day 23 차량 반납 시점과 방식은 검증·수정 범위가 아니다.
- Orizo 요금 숫자는 동적 공식 페이지에서 확정하지 못했으므로 임의 숫자를 추가하지 않는다.
- 기존 main의 Nice Day 10과 Nice 전용 테스트 불일치는 Avignon 판정과 분리한다.

## 판정 형식

- `PASS` 또는 `FAIL`
- 차단 이슈와 비차단 NOTE를 분리한다.
- 코드 수정 없이 검증 결과 문서만 작성한다.
