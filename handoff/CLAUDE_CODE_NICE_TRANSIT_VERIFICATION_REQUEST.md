# Claude Code 독립 검증 요청 — Nice 공공교통 확장

## 목적

Barcelona에서 승인된 구조를 Nice에 확장한 변경을 독립 검증한다. 구현 코드는 수정하지 말고 공식 요금, 일정별 승차 횟수, 시내권·TER·ZOU 분리, 기존 챕터 충돌, 화면 회귀를 확인한다.

## 대상

- 브랜치: `codex/stay-transport-guards`
- 기준: 이 문서가 포함된 최신 커밋
- `data/transit-facts.json`
- `data/transit-facts.schema.json`
- `build/render.py`
- `source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md`
- `tests/test_stay_transport_guards.py`
- daily card Day 7~12

## 구현 결론

- Day 7: NCE T2→도심 Tram 2, 두 사람 각 1회
- Day 8: 도보
- Day 9: Antibes·Cannes 별도 TER
- Day 10: TER와 광역 bus/ZOU를 구간별 확인
- Day 11: Tram 1→15번 bus와 귀환, 두 사람 각 2회 여정
- Day 12: 렌터카
- Lignes d’Azur 예상 사용량: 두 사람 합계 약 6회
- 추천: 공항 T2에서 익명 La Carte(보증금 €2)에 공동 Multi voyages 6회 충전
- Aéro €10 왕복권은 공항 귀환이 없는 일정이라 비추천

## 공식 사실 재검증

저장된 문구를 믿지 말고 공식 페이지를 새로 열어 확인한다.

1. Solo 1회 €1.70, 74분 환승
2. Multi voyages 1~100회, 여러 사람 동시 사용 가능
3. 첫 탑승과 환승마다 인원수만큼 검증
4. 버스는 왕복·동일 노선 연장 불가, tram은 왕복 불가
5. La Carte 익명 카드 보증금 €2와 환급 조건
6. Aéro 왕복 €10, 유효기간 제한 없음
7. 충전된 일반 Lignes d’Azur 카드로 공항 접근 가능
8. Tram 2의 T1·T2·Jean Médecin·Port Lympia 연결

## 일정 검증

- Day 7과 Day 11만 Lignes d’Azur 횟수에 넣은 것이 맞는지
- Day 11 Tram 1→15번 bus가 74분 환승 한 여정으로 가능한지
- Day 9 TER와 Day 10 TER·ZOU가 시내권에서 정확히 분리됐는지
- Day 10 `602` 및 Villefranche→Èze 구간의 운영 주체·표현이 과도하게 단정되지 않았는지
- 기존 챕터의 폐기 요금 €1.80·1일권 €5가 렌더 결과에 남지 않았는지

## 실행

```powershell
$env:PYTHONUTF8 = '1'
python -m unittest tests.test_stay_transport_guards -v
$env:SPFR_SITE_DIR = Join-Path $PWD '.claude-nice-site'
python build/site.py
python build/viewport_check.py
```

Nice 지역 페이지에서 상품 카드, Day 7~12 링크, 공식 출처, 교통 PDF를 데스크톱·모바일에서 확인한다.

## 결과

`handoff/CLAUDE_CODE_NICE_TRANSIT_VERIFICATION_RESULT.md`에 `PASS`, `PASS WITH NOTES`, `FAIL` 판정과 다음을 기록한다.

1. 차단 이슈
2. 공식 사실 표
3. 일정·승차 횟수 검증
4. 시내권·TER·ZOU 경계
5. 화면·회귀 결과
6. 다음 도시 확장 전 권고

Hertz 관련 사항은 검증 범위와 차단 사유에서 제외한다.
