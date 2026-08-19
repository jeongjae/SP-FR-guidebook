# Phase PC-11 QA & Validation Report: Avignon, Pont du Gard, Arles & Alpilles Place Content Enrichment

**작성일**: 2026-08-19  
**브랜치**: `feat/pc-11-avignon-enrichment`  
**대상 권역**: Avignon, Pont du Gard, Uzès, Arles, Alpilles (Les Baux, Saint-Rémy)

---

## 1. Executive Summary
- **Phase PC-11 작업 완결**: Barcelona, Girona, Nice, Aix, Luberon에 이어 **Avignon / Pont du Gard / Arles / Alpilles 권역 18개 Canonical Place**에 대해 Place Canonical SOT 및 5-Layer 콘텐츠 표준을 전면 적용 완료.
- **네 가지 핵심 축의 완벽한 구현**:
  1. *Avignon (Papal / Medieval City)*: 14세기 교황청 요새 궁전(Palais des Papes, 구궁전/신궁전, 마테오 조바네티 프레스코화, 히스토패드 3D 증강현실 관람 전략), 론 강 소빙하기 기후사의 상징 생베네제 다리(Pont Saint-Bénézet), 돔 바위 전망대(Rocher des Doms), 파트리크 블랑 수직 식물벽의 레 잘(Les Halles).
  2. *Pont du Gard (Roman Engineering & Landscape)*: 50km 구간을 1km당 34cm의 초정밀 자연 유하 경사로 연결한 기원 1세기 3단 로마 수도교의 토목 공학, 건식 석조 결구, 양안 4대 뷰포인트 및 좌안 방문자 센터/주차장 가이드.
  3. *Uzès (Ducal Elegance & Market)*: 프랑스 제1공작의 공작성(Le Duché), 12세기 로마네스크 원형 피네스트렐 탑, 에르브 광장 석조 아케이드와 플라타너스 분수의 품격 있는 도시 산책.
  4. *Arles (Roman City / Van Gogh / Walk)*: 서기 90년 2만 명 규모 원형경기장(Arènes)의 중세 요새 마을 변천사, 기원전 12년 고대 극장(Théâtre Antique)의 '두 과부' 기둥, 12세기 생트로핌(Saint-Trophime) 파사드 팀파눔과 복합 회랑, 포룸 광장(Place du Forum) 반 고흐 카페 테라스와 벽면 속 로마 신전 기둥, 론 강변 어부 마을 라 로케트(La Roquette), 3.5km 시티 워크 동선.
  5. *Alpilles (Landscape & Heritage)*: 해발 245m 바위산 독수리 요새 레보(Les Baux), 지하 석회암 채석장의 몰입형 미디어 아트(Carrières des Lumières), 노스트라다무스의 생레미(Saint-Rémy), 반 고흐 『별이 빛나는 밤』 탄생지 생폴 드 모졸(Saint-Paul-de-Mausole), 켈트-그리스-로마 3중 고고학 유적 글라눔(Glanum).
- **Chapter Dedup 완료**: `09_Avignon_Alpilles_Pont_du_Gard_v2.0.md` 내 장소 장문 중복 400여 줄을 제거하고 Editor's Verdict 기반 Compact Card 및 링크 구조로 전환.
- **Trip Layer 완전 분리**: 장소 본문 내 여행 날짜/일정 하드코딩 완전 배제.
- **전체 테스트 All PASS**: `site.py`, `ux_check.py`, `content_audit.py`, `validate_place_canonical_model.py` 100% 통과.

---

## 2. Inventory & Tier 분류 (18 Places)

| Slug | Place Name | Category | Tier | Priority | 5-Layer Coverage |
|---|---|---|---|---|---|
| `palais-des-papes` | Palais des Papes | Architecture / Papal Palace | **TIER_A** | MUST_SEE | 100% |
| `pont-saint-benezet` | Pont Saint-Bénézet | Historic Site / Bridge | **TIER_B** | MUST_SEE | 100% |
| `rocher-des-doms` | Rocher des Doms | Viewpoint / Public Park | **TIER_B** | WORTHWHILE | 100% |
| `les-halles` | Les Halles d'Avignon | Market / Covered Hall | **TIER_B** | WORTHWHILE | 100% |
| `pont-du-gard` | Pont du Gard | Historic Site / Roman Aqueduct | **TIER_A** | MUST_SEE | 100% |
| `uzes` | Uzès Place aux Herbes · 구시가지 | Town / Ducal Heritage | **TIER_A** | MUST_SEE | 100% |
| `arles` | Arles (도시 개관 & 워크) | City / Roman & Van Gogh Walk | **TIER_A** | MUST_SEE | 100% |
| `arenes-d-arles` | Arènes d’Arles | Historic Site / Amphitheatre | **TIER_A** | MUST_SEE | 100% |
| `theatre-antique-arles` | Théâtre Antique d'Arles | Historic Site / Roman Theatre | **TIER_B** | WORTHWHILE | 100% |
| `place-du-forum-arles` | Place du Forum | Viewpoint / Square | **TIER_B** | WORTHWHILE | 100% |
| `cloitre-saint-trophime` | Cloître Saint-Trophime | Architecture / Cloister | **TIER_B** | WORTHWHILE | 100% |
| `la-roquette` | La Roquette | Neighborhood / Riverside | **TIER_C** | OPTIONAL | 100% |
| `fondation-vincent-van-gogh-arles` | Fondation Vincent van Gogh Arles | Museum / Contemporary Art | **TIER_B** | WORTHWHILE | 100% |
| `les-baux-de-provence` | Les Baux-de-Provence | Historic Site / Hilltop Fortress | **TIER_A** | MUST_SEE | 100% |
| `carrieres-des-lumieres` | Carrières des Lumières | Museum / Immersive Media Art | **TIER_A** | MUST_SEE | 100% |
| `saint-remy-de-provence` | Saint-Rémy-de-Provence | Town / Culture & Nostradamus | **TIER_A** | MUST_SEE | 100% |
| `saint-paul-de-mausole` | Saint-Paul-de-Mausole | Historic Site / Monastery Hospital | **TIER_A** | MUST_SEE | 100% |
| `glanum` | Glanum | Historic Site / Ancient City | **TIER_B** | WORTHWHILE | 100% |

---

## 3. 5-Layer 품질 검증 결과
1. **Layer 1 (Facts)**: 주소, 위도/경도, 개방시간, 요금, 공식 URL, 예약 규정 전수 완비.
2. **Layer 2 (Strategy & Planning)**: Best For, Best Time, 권장 체류시간, 시장일 및 관람 순서 최적화.
3. **Layer 3 (Experience & Atmosphere)**: 역사적 서사와 현장감 극대화.
4. **Layer 4 (Deep Guide - 알아야 보인다)**:
   - *Palais des Papes*: 아비뇽 유수의 배경, 요새 군사 건축의 특징, 구궁전(검소) vs 신궁전(화려)의 대비, 히스토패드 3D 증강현실 관람 전략.
   - *Pont du Gard*: 50km 중력 자연 유하의 원리와 1km당 34cm 초정밀 측량, 3단 아치 건식 석조 결구(Opus quadratum), 양안 4대 뷰포인트.
   - *Arènes vs Théâtre*: 맹수 사냥/검투사용 원형투기장(O자형) vs 연극/음악용 고대 극장(D자형)의 기능적 차이 및 2,000년 역사적 변천사.
   - *Van Gogh in Arles & Saint-Rémy*: 『밤의 카페 테라스』, 『별이 빛나는 밤』의 실제 현장과 작품 비교, 사실 수준의 엄격한 구분.
5. **Layer 5 (Practical & Transport/Parking)**: Avignon Centre역 TER 철도 이용, Pass Monument Avantage (€13.00), 공식 주차장 좌표 완비.

---

## 4. 파이프라인 무결성 검증
- `site.py`: HTML 337쪽 정상 렌더링 완료 (Place 단독 페이지, Region 카드, Day 카드 링크).
- `validate_place_canonical_model.py`:
  - Canonical SOT 파일 보존: PASS (빌드 전후 SHA-256 해시 100% 불변).
  - 장문 중복 검사: PASS (중복 시그니처 0건).
  - Trip Layer 분리: PASS (장소 본문 내 날짜 하드코딩 0건).
  - Day stop 참조 정합성: PASS (`day-20`, `day-21`, `day-22` 전수 일치).
- `content_audit.py`: 0 Error, 0 Content Loss PASS.
- `ux_check.py`: 모든 UI/UX 무결성 가드 PASS.
