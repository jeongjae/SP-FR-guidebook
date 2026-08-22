# Lyon 공공교통 차단 이슈 재검증 요청

## 목적

`CLAUDE_CODE_LYON_TRANSIT_VERIFICATION_RESULT.md`의 FAIL 차단 2건이 해소됐는지 독립 검증한다. 검증 과정에서는 코드를 수정하지 않는다. Hertz 관련 사항은 사용자 지시에 따라 범위에서 제외한다.

## 필수 확인

1. 여행일(2026-09-21·22)에 적용되는 TCL Zone 1·2 비접촉 일일 상한과 Pass 24h가 €7.10으로 표시되는가.
2. €2.10 1회 요금은 유지되고, “패스 선구매 없이 비접촉 결제”라는 결론이 보존되는가.
3. Day 24의 실제 수단이 Metro D와 F2이며 `tram`이 일정 설명·자료 usage에 남지 않았는가.
4. Day 24 F2 leg가 `funicular`로 모델링되고 화면에서 “푸니쿨라”로만 표시되는가.
5. Lyon 교통 출처·자료의 `recheckBy`가 2026-09-02이며, 모델이 지역 체크인 전 재확인을 허용하면서 다른 지역의 기한도 계속 차단하는가.
6. 매체 혼용 시 €20 가능성과 Annecy 하루 12편 중 직행 3편 안내가 데이터·원고에서 일치하는가.
7. 지역 화면, Day 24 카드, 스키마, 뷰포트, PWA에 신규 회귀가 없는가.

## 실행 권장

```powershell
$env:PYTHONUTF8='1'
python -m unittest tests.test_stay_transport_guards.StayTransportGuards.test_lyon_contactless_and_annecy_ter_match_itinerary tests.test_stay_transport_guards.StayTransportGuards.test_region_essentials_and_transit_facts_follow_schema tests.test_stay_transport_guards.StayTransportGuards.test_transit_sources_are_official_and_scheduled_for_recheck tests.test_stay_transport_guards.StayTransportGuards.test_every_region_has_official_transport_resources
python build/site.py
python build/ux_check.py
python build/content_audit.py
python build/viewport_check.py
python build/pwa_check.py
```

전체 `tests.test_stay_transport_guards`의 Nice Day 10 `Gare d’Èze` 실패는 기존 기준선 이슈이므로 Lyon 판정과 분리해 기록한다.

## 판정

- 위 두 차단 문제가 남거나 여행일 요금·수단이 화면에서 틀리면 `FAIL`.
- 차단 문제가 해소되고 신규 회귀가 없으면 `PASS`.
- 비차단 개선점은 `NOTE`로 분리한다.
