# PLACE MASTER INVENTORY SUMMARY (Phase PC-00)

**조사 시점**: 2026-08-18 (실측 데이터 기반, 사전 수량 고정 없음)

## 1. 전체 수량 요약

- **총 조사된 엔티티 수**: 335개
  - **정식 장소(Canonical Place) 후보군**: **259개** (Registry / 30_Places / Generated Pages 기반)
  - **일정표 세부 정차점/식당 후보 (Day Stop Entities)**: **76개** (타임라인 상의 개별 활동 및 식당 등)

## 2. Region별 분포 (Canonical Place 후보 기준)

| Region | 수량 | 주요 거점/도시 |
|---|---|---|
| `aix` | 18 | Aix 권역 장소 |
| `avignon` | 18 | Avignon 권역 장소 |
| `barcelona` | 11 | Barcelona 권역 장소 |
| `girona` | 9 | Girona 권역 장소 |
| `luberon` | 11 | Luberon 권역 장소 |
| `lyon` | 7 | Lyon 권역 장소 |
| `nice` | 15 | Nice 권역 장소 |
| `paris` | 16 | Paris 권역 장소 |
| `unknown` | 154 | Unknown 권역 장소 |

## 3. Type(유형)별 분포

| Type | 수량 | 설명 |
|---|---|---|
| `---` | 1 | 장소 명부 kind 분류 |
| `node` | 3 | 장소 명부 kind 분류 |
| `spot` | 249 | 장소 명부 kind 분류 |
| `walk` | 6 | 장소 명부 kind 분류 |

## 4. Dedicated Place Page 보유 현황

- **독립 장소 페이지 생성(`places/<slug>.html`)**: 104개 (40.2%)
- **독립 페이지 미생성**: 155개

## 5. 현재 콘텐츠 깊이(Content Depth) 분포

| Depth 등급 | 수량 | 비율 | 정의 기준 |
|---|---|---|---|
| `DEEP_GUIDE` | 19 | 7.3% | 2,500자 이상 및 전략/경험/심화 가이드 완비 |
| `MEDIUM_GUIDE` | 19 | 7.3% | 1,200자 이상 및 핵심 가이드 보유 |
| `SHORT_DESCRIPTION` | 53 | 20.5% | 400자 이상 기본 설명 구비 |
| `FACTS_ONLY` | 3 | 1.2% | 실용 정보/토큰 위주 간략 기술 |
| `NONE` | 165 | 63.7% | 독립 장문 MD 원고 미작성 (Registry만 존재) |

## 6. Duplicate / Alias / Orphan / Archive 분석

### 6.1 Duplicate Candidates (중복 후보)
- 현재 정식 장소(Canonical Places) 104개 내에서 동일 장소의 중복 엔티티는 0건으로 정돈되어 있음.

### 6.2 Alias Candidates (별칭/표기 변형 후보)
- `onyar` ↔ Cases de l'Onyar / Ponts de l'Onyar
- `croix-rousse` ↔ Croix-Rousse Slopes (비탈길 트라불) / Croix-Rousse Plateau
- `day-cards` 내 축약 ID ↔ 정식 slug 매핑 (예: `sant-pau` → `sant-pau-recinte-modernista`, `orsay` → `musee-d-orsay` 등)

### 6.3 Orphan Candidates (고립 후보)
- **Day 미참조 장소**: 40개 (지역 탐색 및 자유일정 선택지용 장소이나 특정 Day 일정표에 명시되지 않음. 의도된 지역 탐색 카탈로그이므로 정상 유지)

### 6.4 Archive Candidates (폐기 후보)
- 0건 (모든 정식 장소가 실제 일정 또는 지역 탐색 카탈로그에 유효하게 연결됨)

## 7. Facts Completeness 현황

- `data/place-facts.json` 및 장소 실용 정보(Facts) 감사 결과, 필수 기본정보(좌표, 구글맵 링크 등)는 100% 구축되어 있으나, 세부 개관시간/입장료 등의 최신 검증 메타데이터 확충이 Phase PC-01 이후 단계에서 필요함.
