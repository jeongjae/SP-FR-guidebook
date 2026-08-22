# Paris 숙박·교통 차단 이슈 재검증 요청

## 목적

`CLAUDE_CODE_PARIS_TRANSIT_VERIFICATION_RESULT.md`의 FAIL 차단 2건이 해소됐는지 독립 검증한다. 검증 중 코드를 수정하지 않는다.

## 필수 확인

1. Metro‑Train‑RER Ticket €2.55가 Versailles에서도 유효하고 공항역 진출입만 제외한다고 표시되는가.
2. Weekly가 없어도 Versailles RER C에 개별권으로 갈 수 있다는 설명이 보이는가.
3. Bus‑Tram Ticket이 이번 확정 일정에서는 필요 없으며, 개별권 기간에 계획이 바뀔 때만 구매한다고 안내하는가.
4. Day 36의 32번 bus는 9/28–10/4 Weekly에 포함된다는 기존 일정 설명과 모순이 없는가.
5. Weekly 손익분기 1인 13회와 일정 축소 시 재계산 안내가 과도한 구매를 막는가.
6. Liberté+를 권하지 않는 이유가 프랑스 은행계좌 요건으로 명시되는가.
7. Day 27–42 링크, Day 37 mode, Day 42 공식 택시, 요금 4종에 신규 회귀가 없는가.

## 실행 권장

```powershell
$env:PYTHONUTF8='1'
python -m unittest tests.test_stay_transport_guards.StayTransportGuards.test_paris_uses_one_weekly_pass_and_individual_tickets_around_it tests.test_stay_transport_guards.StayTransportGuards.test_region_essentials_and_transit_facts_follow_schema
python build/site.py
python build/ux_check.py
python build/content_audit.py
python build/viewport_check.py
python build/pwa_check.py
```

Nice Day 10의 기존 `Gare d’Èze` 기준선 실패와 Lyon 후속 수정 PR은 Paris 판정에서 분리한다.

## 판정

- 두 상품 카드의 모순이 남거나 다른 일정·요금 회귀가 생기면 `FAIL`.
- 차단 문제가 해소되고 신규 회귀가 없으면 `PASS`.
- 나머지는 비차단 `NOTE`로 분리한다.
