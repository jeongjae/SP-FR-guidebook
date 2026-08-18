# PLACE TAXONOMY NORMALIZATION REPORT (Phase PC-01)

**작성일**: 2026-08-18
**대상**: 104개 Canonical Places 및 Day Stops 정규화

## 1. 정규화 Taxonomy 체계 정의

기존의 단순 `spot` 위주(101개) 분류에서 여행자 관점의 명확한 목적별 9대 표준 Taxonomy로 정규화하였습니다.

| Normalized Type | 설명 | 수량 | 대표 장소 |
|---|---|---|---|
| `architecture` | 역사적 기념비, 성당, 궁전 등 핵심 건축물 | 13개 | 사그라다 파밀리아, 교황청, 베르사유 |
| `museum` | 미술관, 박물관, 갤러리 | 13개 | 루브르, 오르세, 세잔 아틀리에, MUCEM |
| `historic_site` | 유적지, 원형경기장, 수도원 등 | 15개 | 퐁뒤가르, 아를 원형경기장, 세낭크 |
| `neighborhood` | 역사 지구, 주요 거리, 구시가지 구역 | 14개 | 고딕지구, 비외니스, 르마레, 비외리옹 |
| `village` | 근교 소도시, 거점 마을 | 21개 | 시체스, 생폴드방스, 고르드, 아를, 안시 |
| `market` | 상설 홀, 야외 마켓, 식료품 시장 | 6개 | 살레야 마켓, 리옹 폴보퀴즈 홀, 리셸름 광장 |
| `viewpoint` | 전망대, 파노라마 뷰 포인트, 주요 광장 | 10개 | 니스 성 언덕, 마르세유 구항구, 벨쿠르 광장 |
| `nature` | 국립공원, 피오르드 해안, 자연 명소 | 3개 | 칼랑크 국립공원, 루시용 황토길, 테트도르 공원 |
| `walk` | 선별된 테마 도보/산책 코스 | 6개 | 바르셀로나 고딕 도보, 니스 해안 도보 |
| `transit` | 공항, 주요 철도역 노드 (유틸리티) | 3개 | 산츠역, 니스빌역, 니스공항 T2 |

## 2. 기존 Type vs 정규화 Type 비교

| 기존 Type (Legacy) | 수량 | → 정규화 Type (Normalized) | 수량 |
|---|---|---|---|
| `spot` | 101개 | `architecture`, `museum`, `historic_site`, `neighborhood`, `village`, `market`, `viewpoint`, `nature` | 95개 |
| `walk` | 2개 | `walk` | 6개 |
| `node` | 1개 | `transit` | 3개 |

## 3. Day Stops 중 Place Taxonomy 편입 권장 맛집/카페

43일 일정표(`data/daily-cards/`)의 231개 정차점 중 향후 독립 장소로 승격을 권장하는 핵심 미식 거점:
- **바르셀로나**: Bar Cañete (`bar-canete`), Bodega Joan (`bodega-joan`), La Paradeta (`la-paradeta-sagrada`)
- **니스/코트다쥐르**: Chez Pipo (소카 명가), René Socca, Fenocchio (아이스크림)
- **엑상프로방스/뤼베롱**: Les Deux Garçons, Maison Weibel
- **리옹**: Café des Fédérations (전통 부숑), Daniel & Denise
- **파리**: Stohrer (가장 오래된 파티세리), Breizh Café (크레프리), Bouillon Chartier