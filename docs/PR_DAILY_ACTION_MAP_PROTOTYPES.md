# PR: Daily Action Map 자동 생성 시스템과 시제품 3개

## Summary

- 43일을 날짜별 JSON으로 구조화하고 JSON Schema를 추가했습니다.
- 공통 HTML/CSS/JS 템플릿, OSM 타일 캐시, OSRM 차량 경로 캐시,
  PNG/WebP/썸네일 렌더러를 구현했습니다.
- 자동 라벨 배치로 지도 라벨과 마커 충돌을 방지합니다.
- 서로 다른 유형의 시제품 Day 02, 04, 05만 생성했습니다.
- 날짜 페이지에는 480×640 썸네일을 표시하고 전체 WebP와 검수용 PNG를
  연결했습니다.

## Source of Truth finding

`main`의 선언된 정본(v1.2, 2026-08-01)과 더 최신이지만 미병합인
`feat/itinerary-marseille-arles`(문서 v1.3, 2026-08-04)가 충돌합니다.
43일 데이터는 최신 후보 브랜치에서 만들었지만 승인으로 간주하지 않고
`candidate-latest-needs-review`를 유지했습니다. 자세한 내용은
`docs/DAILY_CARD_SOURCE_OF_TRUTH.md`에 있습니다.

## Prototypes

| Day | Type | Output |
|---:|---|---|
| 02 | 도시 도보·대중교통 | Barcelona · Sagrada/Sant Pau |
| 04 | 장거리 도시 간 이동 | Barcelona→Sitges→Bàscara |
| 05 | 렌터카 근교 순환 | Bàscara→Collioure→Cadaqués→Bàscara |

## QA

- Dataset: 43/43 consecutive DAY/date files
- Prototype PNG: 1440×1920
- Full WebP: 1440×1920, quality 86
- Thumbnail WebP: 480×640, quality 82
- Map label overlaps: 0 / 0 / 0
- DOM text overflow: 0 / 0 / 0
- Website thumbnail/full-WebP/PNG links: all present
- HIG sample: 19 pages × 2 widths × light/dark, machine-checkable issues 0

Commands:

```bash
python3 scripts/daily-cards/validate.py --visual-dom --write-report
python3 build/build.py
python3 build/hig_check.py
```

## Review focus

1. 5초 안에 시간순 일정과 이동 방향을 이해할 수 있는가?
2. 지도 확대 수준이 도시형·광역형·순환형에 적절한가?
3. 장소명·시각·식사·교통·숙소 출발/귀환이 충분히 읽히는가?
4. Day 04의 광역 지도 단순화와 Day 05의 국경 순환 표현이 적절한가?
5. 이 시각 언어를 나머지 40일에 적용해도 되는가?

## Intentionally deferred

- 시제품 승인 전 5개 단위 배치 생성
- 미병합 최신 일정의 정본 승격
- Day 07 Bàscara→Nice 이동수단 확정
- 나머지 40일 숙소·시각·좌표·경로 검증
- 미확정 보행·대중교통 구간의 검증된 라우터 경로 교체
