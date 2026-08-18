# PLACE INVENTORY AUDIT QA REPORT (Phase PC-00)

## 1. 조사 대상 소스 (Sources Inspected)

1. **장소 정본 명부**: `source/ASSETS/91_Place_Registry_v1.0.md` (104개 엔티티)
2. **장소 장문 마크다운**: `source/CURRENT/30_Places/*.md` (94개 정식 장문 파일)
3. **지역 편집 마크다운 & 메타**: `source/CURRENT/20_Regions/*.md`, `source/CURRENT/10_Core/regions.json`
4. **일정 정본 데이터**: `data/daily-cards/day-01~43.json` (43일 전수 stops & legs)
5. **사실 데이터베이스**: `data/place-facts.json` (운영시간, 요금, 예약 사실 토큰)
6. **지도 데이터**: `source/ASSETS/maps/*.json` (daily-routes, 8개 지역 실행지도)
7. **빌드 파이프라인 및 모델**: `build/model.py`, `build/site.py`, `build/render.py`
8. **생성 산출물 크로스체크**: `site/places/*.html` (104개 정적 HTML) 및 `site/search-index.json`

## 2. 장소 후보 판정 규칙 (Identification Rules)

- **Canonical Place**: `91_Place_Registry_v1.0.md`에 등재되어 있고 `build/model.py`를 통해 `places/<slug>.html`로 생성되는 104개 엔티티.
- **Spot vs Walk vs Node**: 독립 방문지(`spot`: 101개), 이동/산책 코스(`walk`: 2개), 교통 허브(`node`: 1개 - barcelona-sants).
- **Day Stops vs Place**: 일정표의 일상 활동(식사, 휴식, 버퍼, 체크인 등)은 장소 엔티티에서 제외하고, 구체적인 식당/카페/스팟은 Day Stop Entity로 분리하여 기록.

## 3. 생성 산출물과의 대조 (Reconciliation with Generated Output)

- `build/model.py` 및 `build/site.py` 실행 결과 생성되는 `site/places/*.html`은 **정확히 104개**임.
- `source/CURRENT/30_Places/*.md`에 존재하는 장문 파일은 **94개**이며, 나머지 10개는 Registry 기반의 간략 장소(Spot/Node/Walk)로 정상 렌더링됨.
- 불일치(Inconsistency) 0건, 고아 링크(Broken Link) 0건 확인 완료.

## 4. 미해결 모호성 (Unresolved Ambiguities)

1. **Walk 엔티티의 범위**: `barcelona-historic-walk`, `barcelona-modernisme-walk` 등은 독립 장소 페이지를 가지고 있으나, 향후 Walk 데이터 모델과 Place 데이터 모델의 분리 필요성 검토 필요.
2. **식당/카페(Food Stops)의 Place 편입 여부**: 현재 43일 일정표 내 다수의 식당/카페가 `daily-cards`에만 존재하고 독립 Place Page가 없음. PC-01에서 식당 엔티티의 장소 정본화 기준 확립 필요.

## 5. 다음 Phase (PC-01 / PC-02) 결정 및 추천사항

### PC-01 Taxonomy Normalization 추천사항
- 유형 분류를 `attraction`, `architecture`, `museum`, `market`, `viewpoint`, `walk`, `food`, `transit` 등으로 세분화 표준화.
- Day stops에만 존재하는 검증된 맛집(식당/카페) 중 보강 가치가 높은 대상을 선별하여 Place Taxonomy에 정식 등록.

### PC-02 Priority / Content Tier Classification 추천사항
- 현재 `DEEP_GUIDE`(22개), `MEDIUM_GUIDE`(47개), `SHORT_DESCRIPTION`(22개), `FACTS_ONLY`(3개), `NONE`(10개)로 분포된 장소들을 여행 필수도에 따라 Tier A(Must See), Tier B(Core), Tier C(Supporting/Optional)로 체계적 재분류 제안.
