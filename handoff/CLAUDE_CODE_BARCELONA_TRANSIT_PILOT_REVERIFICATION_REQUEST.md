# Claude Code 재검증 요청 — Barcelona 파일럿 차단 이슈 해소

## 대상

- 브랜치: `codex/stay-transport-guards`
- 이전 검증: `CLAUDE_CODE_BARCELONA_TRANSIT_PILOT_VERIFICATION_RESULT.md`
- 기준: 이 문서가 포함된 최신 커밋
- 검증 중에는 코드 수정 없이 결과만 기록한다.

## 수정한 차단 이슈

### B1 터치 타깃

- 도착·출발 Day 링크를 존재하지 않는 `text-link`에서 저장소 표준 `btn btn-secondary`로 변경했다.
- 로컬 `build/viewport_check.py` 결과: 6개 뷰포트, 가로 오버플로 0, 터치 타깃 44pt 이상, 글자 11px 이상 통과.

### B2 상충 권고

- Barcelona 챕터의 `Aerobús 우선`, `각자 T-casual` 구 권고를 제거했다.
- daily card와 신규 교통 데이터가 모두 다음 결론을 말하도록 통일했다.
  - 공항 도착은 택시 기본, Aerobús 대안
  - Day 2·3의 숙소 출발·귀환까지 승차 후보에 포함
  - 두 사람이 함께 2구간 이상 타면 T-familiar, 그보다 적으면 단일권

## 함께 수정한 검증 지적

- Day 2의 `한 구간만` 및 Day 3의 `도보 중심` 과소 표현을 실제 승차 후보로 교체했다.
- 일정에 없는 Rodalies 대안을 제거했다.
- T-familiar의 30일·8회·동행 공유 조건을 추가했다.
- Airport ticket의 €5.90·비통합 조건을 추가했다.
- `itineraryUses` 링크를 하드코딩하지 않고 실제 `Day.url`에서 생성한다.
- 구조화 JSON Schema 검증을 테스트뿐 아니라 사이트 모델 로딩에도 적용했다.
- 공식 출처의 확인일이 미래가 아닌지, 재확인일이 여행 시작 전인지 빌드와 테스트에서 검사한다.
- 챕터에 폐기된 권고가 다시 들어오지 못하도록 회귀 테스트를 추가했다.

## 재검증 명령

```powershell
$env:PYTHONUTF8 = '1'
python -m unittest tests.test_stay_transport_guards -v
$env:SPFR_SITE_DIR = Join-Path $PWD '.claude-reverify-site'
python build/site.py
python build/viewport_check.py
```

## 판정 요청

1. B1이 동일한 6개 뷰포트에서 해소됐는가?
2. 같은 Barcelona 페이지에 반대되는 공항·교통권 권고가 남아 있는가?
3. Day 2·3 승차 후보가 daily card의 `totalDistance`, `legs`, `needsReview`와 일치하는가?
4. T-familiar 추천 경계가 두 사람의 검증 횟수와 가격 비교에 맞는가?
5. 신규 빌드 경로 검증이 스키마·날짜 오류를 실제로 차단하는가?
6. 기존 기능의 신규 회귀가 있는가?

결과는 `handoff/CLAUDE_CODE_BARCELONA_TRANSIT_PILOT_REVERIFICATION_RESULT.md`에 `PASS`, `PASS WITH NOTES`, `FAIL` 중 하나로 기록한다. Hertz 관련 사항은 이번에도 범위와 차단 사유에서 제외한다.
