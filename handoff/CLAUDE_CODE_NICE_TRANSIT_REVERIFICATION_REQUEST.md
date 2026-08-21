# Nice 공공교통 확장 — Claude Code 독립 재검증 요청

## 목적

`CLAUDE_CODE_NICE_TRANSIT_VERIFICATION_RESULT.md`의 `FAIL` 차단 사유 2건이 실제로 해소됐는지 독립 검증한다. 구현자의 설명을 전제로 삼지 말고 저장소, 빌드 산출물, 공식 출처를 직접 대조한다.

Hertz 관련 사항은 사용자가 이미 인지하고 차량 인수 시 확인할 예정이므로 이번 재검증 범위에서 제외한다.

## 반드시 확인할 차단 사유

### B1 — Day 10 Villefranche → Èze 동선

- `data/daily-cards/day-10.json`과 니스 안내가 Villefranche 항구에서 602번을 바로 탈 수 있는 것처럼 쓰지 않는지 확인한다.
- 현재 계획이 `Villefranche-sur-Mer → Èze-sur-Mer` TER, `Gare d’Èze → Èze Village` Lignes d’Azur 83번으로 명확히 분리되는지 확인한다.
- Èze Village → Monaco도 83번으로 Gare d’Èze 하산 후 TER를 이용하도록 일관되게 연결되는지 확인한다.
- 602번이 Day 10 확정 동선과 승차 횟수 계산에서 완전히 빠졌는지 확인한다.
- 여행일 TER/83 연결 확인과 연결 불량 시 Villefranche 또는 Èze 생략이라는 실행 안전장치가 보이는지 확인한다.

### B2 — 공식 PDF 재배포 권리

- 재배포 근거가 없는 교통 PDF 7건이 저장소와 공개 사이트/PWA에 더 이상 동봉되지 않는지 확인한다.
- 원문 접근은 각 교통기관의 `officialUrl`로 계속 제공되는지 확인한다.
- `transit-resources.schema.json`이 향후 `localPath`를 쓸 경우 `rightsHolder`, `license`, `redistributionBasis`를 필수로 요구하는지 확인한다.
- 빌드 결과에 `assets/transport-guides/*.pdf`가 존재하거나 PWA가 캐시하지 않는지 확인한다.

## 비차단 지적 후속 확인

- 니스 챕터의 폐기 요금 `€1.80`, `€12.60`, `1일권 €5` 및 잘못된 1시간 환승 표현이 제거됐는지 확인한다.
- stale-price 테스트가 마크다운 강조 표기에도 실제 값을 잡는지 확인한다.
- 테스트가 `data/daily-cards/day-10.json`을 직접 읽어 602 부재와 Gare d’Èze/83 존재를 검증하는지 확인한다.
- 두 사람의 실제 사용량이 Day 7 2회 + Day 10 4회 + Day 11 4회 = 10회로 설명되고, 12회 충전과 2회 여유분 및 추가 충전 대응이 일관적인지 확인한다.
- Day 11 숙소→Libération은 도보 기본이라는 가정이 명시되는지 확인한다.

## 회귀 검사

다음을 직접 실행하고 결과를 기록한다.

```powershell
python -m unittest tests.test_stay_transport_guards -v
$env:SPFR_SITE_DIR='.claude-nice-reverify-site'
python build/site.py
python build/viewport_check.py
```

추가로 `guide/nice.html`, `guide/day-10.html`, `guide/day-11.html`을 모바일과 데스크톱 폭에서 확인한다. 가로 넘침, 깨진 링크, 읽기 순서, 버튼 크기, 콘솔 오류를 기록한다.

## 판정과 결과 파일

- B1 또는 B2가 남아 있으면 `FAIL`.
- 차단 사유가 모두 해소되고 신규 회귀가 없으면 `PASS`.
- 사소한 개선은 `NOTE`로 분리하며 차단 사유와 섞지 않는다.

결과를 다음 파일에 작성한다.

`handoff/CLAUDE_CODE_NICE_TRANSIT_REVERIFICATION_RESULT.md`

결과에는 검증한 커밋 해시, 공식 근거, 실행 명령 결과, 화면 확인 결과, 최종 `PASS`/`FAIL`을 포함한다. 검증 과정에서는 코드를 수정하지 않는다.
