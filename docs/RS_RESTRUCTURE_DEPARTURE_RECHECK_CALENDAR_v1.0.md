# 출발 전 재검증 캘린더

**생성:** `build/reverify_register.py`
**기준:** 여행 시작 2026-08-29. 날짜가 걸린 pending 을 방문일 역산으로 배치한다.

| 시점 | 할 일 | 근거 |
|---|---|---|
| D-14 (2026-08-15) | 숙소·렌터카 확정 예약 재확인, 미확정 숙소(Aix·Luberon) 현지 결정 자료 갱신 | 재작업 QA |
| D-7 (2026-08-22) | 미술관·전시 예약창 확인 (세잔 사이트·Granet·Mucem·Orsay·Grand Palais) | REVERIFY 레지스터 |
| D-3 (2026-08-26) | 시장 요일·휴관일 최종 확인, 파업·공사 공지 확인 | 요일 충돌 감사 |
| D-1 (2026-08-28) | 첫 3일(항공·숙소·사그라다) 최종 확인 | CF001·CF002 |
| 각 지역 도착 전날 | 해당 지역 pending 항목 일괄 확인 (아래 지역별 건수) | 레지스터 |

| 지역 | 도착일 | pending 건수 |
|---|---|---:|
| 04_Barcelona_Sitges_v2.0.md | 2026-08-29 | 28 |
| 05_Girona_Collioure_Emporda_v2.1.md | 2026-09-01 | 12 |
| 06_Nice_Cote_d_Azur_v2.0.md | 2026-09-04 | 5 |
| 07_Aix_en_Provence_v2.0.md | 2026-09-09 | 45 |
| 08_Luberon_Farmhouse_v2.0.md | 2026-09-13 | 32 |
| 09_Avignon_Alpilles_Pont_du_Gard_v2.0.md | 2026-09-16 | 54 |
| 10_Lyon_v2.0.md | 2026-09-20 | 41 |
| 11_Paris_Long_Stay_v2.0.md | 2026-09-24 | 64 |


## Day 별 실행 가능성 판정 (Stage C)

`build/reverify_register.py` 기계 판정. **FAIL 0건.**

| 판정 | 일수 | 기준 |
|---|---:|---|
| PASS | 29 | 요일 충돌 없음 · 밀도 상한 이내 · 피로도 3 이하 |
| CONDITIONAL | 14 | 피로도 4–5 이거나 하루 강조 항목 22개 초과 |
| FAIL | 0 | 방문 요일과 휴관일 충돌 |

CONDITIONAL 14일은 전부 **트리거와 대안이 본문에 있는 날**이다 — 각 Day 섹션의 `삭제 및 단축 순서`·`대안 대책`이 트리거를 정의한다.

| Day | 사유 |
|---:|---|
| 4 | 하루 강조 항목 29개 — 시체스 경유 이동일, 삭제 순서 적용 |
| 5 | 피로도 4 — 국경 당일치기 |
| 7 | 하루 강조 항목 25개 — Girona→Nice 전환일 |
| 9, 10 | 피로도 4 — 칸·모나코 당일치기 |
| 12 | 피로도 5 — Nice→Aix 이동 + 경유 2곳 |
| 14 | 피로도 4 — Marseille 당일치기 |
| 21, 22 | 피로도 4 — Uzès·Pont du Gard / Arles |
| 23, 24 | 피로도 4 — Avignon→Lyon 이동 / Fourvière·Vieux Lyon |
| 26 | 피로도 4 — Annecy 당일치기 |
| 37 | 피로도 5 — Arc de Triomphe |
| 42 | 피로도 4 — 귀국일 |
