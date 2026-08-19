# Phase PC-10 QA & Validation Report: Luberon Place Content Enrichment

**작성일**: 2026-08-19  
**브랜치**: `feat/pc-10-luberon-enrichment`  
**대상 권역**: Luberon (Hill Villages, Ochre Landscape, Cistercian Abbey, Dry-stone Bories, Weekly Markets, Water Town)

---

## 1. Executive Summary
- **Phase PC-10 작업 완결**: Barcelona, Girona, Nice, Aix에 이어 **Luberon 권역 11개 Canonical Place**에 대해 Place Canonical SOT 및 5-Layer 콘텐츠 표준을 전면 적용 완료.
- **마을별 차별화(Village Differentiation) 극대화**:
  - *Gordes*: 드라마틱한 절벽 위 석조 요새와 진입로 전망대(Town View Point).
  - *Roussillon*: 17가지 타오르는 황토빛 오커 절벽과 센티에 데 오크르(Sentier des Ocres) 트레일.
  - *Bonnieux*: 최대 낙차 계단식 언덕 마을과 옛 성당 정상에서 마주 보는 라코스트 성채 조망.
  - *Ménerbes*: 피터 메일과 도라 마르의 자취가 깃든 길고 좁은 능선(Ridge) 위 성채와 와인/트러플 하우스.
  - *Lourmarin*: 평탄하고 세련된 카페 테라스, 르네상스 성, 알베르 카뮈의 소박한 로즈마리 묘소.
  - *Goult*: 관광버스가 닿지 않는 평화로운 17세기 예루살렘 풍차와 로컬 생활 마을.
  - *Oppède-le-Vieux*: 숲과 덩굴 속 중세 성채 폐허와 복원된 고딕 성당의 신비로운 유적.
  - *L'Isle-sur-la-Sorgue*: 15개 목조 물레바퀴와 300여 개 앤틱 상점이 밀집한 에메랄드 수로의 물의 도시 (신규 SOT 생성).
- **실전 운전 및 주차(Driving & Parking) 가이드 구축**:
  - Gordes 화요일 시장의 08:30 이전 도착 수칙 및 외곽 주차장 위치.
  - Coustellet 일요 생산자 시장의 10:00 이전 주차 권장.
  - Village des Bories 및 Sénanque 수도원의 좁은 1차선 도로 서행 및 교행 수칙.
  - Roussillon의 붉은 황토 먼지 복장 주의(흰옷/흰 신발 금지).
  - Oppède-le-Vieux의 숲길 15분 도보 및 거친 노면 주의.
- **Chapter Dedup 완료**: `08_Luberon_Farmhouse_v2.0.md` 내 장소 장문 중복 300여 줄을 제거하고 Editor's Verdict 기반 Compact Card 및 링크 구조로 전환.
- **Trip Layer 완전 분리**: 장소 본문 내 여행 날짜/일정 하드코딩 완전 배제.
- **전체 테스트 All PASS**: `site.py`, `ux_check.py`, `content_audit.py`, `validate_place_canonical_model.py` 100% 통과.

---

## 2. Inventory & Tier 분류 (11 Places)

| Slug | Place Name | Category | Tier | Priority | 5-Layer Coverage |
|---|---|---|---|---|---|
| `lourmarin` | Lourmarin | Village / Literature | **TIER_A** | MUST_SEE | 100% |
| `gordes` | Gordes | Village / Hilltop Fortress | **TIER_A** | MUST_SEE | 100% |
| `roussillon-sentier-des-ocres` | Roussillon · Sentier des Ocres | Nature / Geology | **TIER_A** | MUST_SEE | 100% |
| `abbaye-de-senanque` | Abbaye Notre-Dame de Sénanque | Architecture / Abbey | **TIER_A** | MUST_SEE | 100% |
| `coustellet` | Marché Paysan de Coustellet | Market / Food | **UTILITY** | MUST_SEE | 100% |
| `goult` | Goult | Village / Local Life | **TIER_B** | WORTHWHILE | 100% |
| `bonnieux` | Bonnieux | Village / Terraced Hill | **TIER_B** | WORTHWHILE | 100% |
| `village-des-bories` | Village des Bories | Heritage / Dry-stone | **TIER_B** | WORTHWHILE | 100% |
| `menerbes` | Ménerbes | Village / Ridge Settlement | **TIER_B** | WORTHWHILE | 100% |
| `oppede-le-vieux` | Oppède-le-Vieux | Historic Site / Ruins | **TIER_C** | OPTIONAL | 100% |
| `l-isle-sur-la-sorgue` | L’Isle-sur-la-Sorgue | Town / Antiques & Water | **TIER_B** | WORTHWHILE | 100% (**신규 생성**) |

---

## 3. 5-Layer 품질 검증 결과
1. **Layer 1 (Facts)**: 주소, 위도/경도, 개방시간, 요금, 공식 URL, 예약 규정 전수 완비.
2. **Layer 2 (Strategy & Planning)**: Best For, Best Time, 권장 체류시간, 시장일 혼잡 대응 전략 명시.
3. **Layer 3 (Experience & Atmosphere)**: 감각적 현장감, 역사적 배경 서사 입체화.
4. **Layer 4 (Deep Guide - 알아야 보인다)**:
   - *Gordes*: D15 진입로 전망대(Town View Point)의 시각적 입체감과 칼라봉 계곡 방어 지형학.
   - *Roussillon*: 1억 1천만 년 전 해저 퇴적층에서 생겨난 침철석(Goethite) 17가지 색조 지질학 및 파스텔톤 가옥 미장.
   - *Sénanque*: 장식을 배제한 성 베네딕토 청빈 건축과 로마네스크 비례, 현재도 이어지는 시토회 수도사들의 침묵 기도.
   - *Bories*: 모르타르 없이 납작한 석회암 판석을 층층이 내어쌓은(Corbelling) 가짜 돔 공법과 농민 생활사.
   - *Lourmarin*: 알베르 카뮈의 소박한 로즈마리 무덤과 프로방스 최초의 르네상스 성채 구조.
   - *L'Isle-sur-la-Sorgue*: 소르그 강의 수력을 이용한 15개 이끼 낀 목조 물레바퀴와 유럽 3대 앤틱 시장의 역사.
5. **Layer 5 (Practical & Driving/Parking)**: 마을별 공식 주차장, 좁은 도로 교행 수칙, 시장일 혼잡 피하기, 복장 주의사항 완비.

---

## 4. 파이프라인 무결성 검증
- `site.py`: HTML 337쪽 정상 렌더링 완료 (Place 단독 페이지, Region 카드, Day 카드 링크).
- `validate_place_canonical_model.py`:
  - Canonical SOT 파일 보존: PASS (빌드 전후 SHA-256 해시 100% 불변).
  - 장문 중복 검사: PASS (중복 시그니처 0건).
  - Trip Layer 분리: PASS (장소 본문 내 날짜 하드코딩 0건).
  - Day stop 참조 정합성: PASS (`day-16`, `day-17`, `day-18` 전수 일치).
- `content_audit.py`: 0 Error, 0 Content Loss PASS.
- `ux_check.py`: 모든 UI/UX 무결성 가드 PASS.
