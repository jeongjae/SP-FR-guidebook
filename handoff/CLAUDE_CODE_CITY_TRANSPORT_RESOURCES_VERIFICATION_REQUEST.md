# Claude Code 독립 검증 요청 — 도시별 교통 지도·오프라인 자료

## 목적

사용자 제공 Barcelona PDF 2개와 다른 체류 지역의 공식 교통 자료를 가이드북에 연결한 변경을 독립적으로 검증한다. 구현 코드는 수정하지 말고 사실·자료 최신성·일정 적합성·링크·모바일 회귀를 반박 관점에서 확인한다.

## 대상

- 브랜치: `codex/stay-transport-guards`
- 기준: 이 문서가 포함된 최신 커밋
- 데이터: `data/transit-resources.json`, `data/transit-resources.schema.json`
- 모델·렌더: `build/model.py`, `build/render.py`
- 파일: `source/ASSETS/transport-guides/`
- 테스트: `tests/test_stay_transport_guards.py`

## 사용자 제공 자료

- `bcn-metro-network-2025-03.pdf`
  - 원본: `08291900 BCN Metro Map.pdf`
  - 확인 사항: TMB Metro network, Març 2025, Hostafrancs·Espanya·Sants Estació·Sant Pau Dos de Maig·Sagrada Família 등 표시
- `montjuic-cable-car-map-2025.pdf`
  - 원본: `08311700 Teleferic de Montjuic Map.pdf`
  - 확인 사항: Parc Montjuïc·Mirador·Castell 3개 정류장, funicular·Metro·bus 연결 표시

## 도시별 선택 자료

- Barcelona: 사용자 제공 PDF 2개
- Girona: ATM Girona 2026 통합망 PDF
- Nice: Lignes d’Azur 2026년 9월 주요 노선 PDF
- Aix: 일정이 도보·렌터카 중심이고 전체 PDF가 없어 공식 노선별 지도 페이지만 연결
- Luberon: ZOU Vaucluse·Bouches-du-Rhône 2026 지역망 PDF
- Avignon: Orizo 2026-2027 개략 노선 PDF
- Lyon: TCL 2026 PDF 지도 공식 페이지 연결
- Paris: Île-de-France Mobilités Metro PDF 및 공식 지도 페이지

## 검증 질문

각 항목을 `PASS`, `PASS WITH NOTES`, `FAIL`로 판정한다.

1. 8개 Region 모두 `교통 지도·오프라인 자료`가 표시되는가?
2. `localPath`가 있는 PDF는 빌드 결과에서 실제로 열리는가?
3. 모든 공식 최신판 링크가 해당 운영기관 또는 공공기관 소유인가?
4. edition 표기가 PDF 내부 또는 공식 페이지와 일치하는가?
5. Barcelona 두 PDF의 `usage` 설명이 지도 자체와 Day 1~4 일정에 부합하는가?
6. 일정에 사용하지 않는 교통수단을 확정 동선처럼 표현한 곳은 없는가?
7. Aix·Lyon의 외부 링크 방식이 파일 부재를 숨기지 않고 이해 가능한가?
8. 큰 PDF가 PWA 전체 용량을 과도하게 늘리거나 핵심 페이지 로딩을 막지 않는가?
9. 360·390·430·768·1024·1440px에서 가로 넘침과 44pt 미만 터치 타깃이 없는가?
10. 기존 Barcelona 교통권·daily card 링크·다른 Region 콘텐츠에 회귀가 없는가?

## 실행

```powershell
$env:PYTHONUTF8 = '1'
python -m unittest tests.test_stay_transport_guards -v
$env:SPFR_SITE_DIR = Join-Path $PWD '.claude-transport-site'
python build/site.py
python build/viewport_check.py
```

PDF는 파일명이나 텍스트 추출만 보지 말고 전 페이지를 렌더링해 육안 확인한다. 공식 링크는 새로 열어 생존 여부와 최신판 교체 여부를 확인한다.

## 결과

`handoff/CLAUDE_CODE_CITY_TRANSPORT_RESOURCES_VERIFICATION_RESULT.md`에 다음을 기록한다.

1. 최종 판정
2. 차단 이슈
3. 도시별 자료 검증 표
4. 일정 적합성
5. 파일·공식 링크 검증
6. 모바일·PWA 회귀 결과
7. 수정 권고

Hertz 관련 사항은 이번 검증 범위와 차단 사유에서 제외한다.
