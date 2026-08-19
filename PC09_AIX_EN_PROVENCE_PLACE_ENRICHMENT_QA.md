# Phase PC-09 QA & Validation Report: Aix-en-Provence Place Content Enrichment

**작성일**: 2026-08-19  
**브랜치**: `feat/pc-09-aix-enrichment`  
**대상 권역**: Aix-en-Provence (Aix Urban, Cézanne Sites, Markets/Utility, Marseille Day-Trip, En-Route/Option Places)

---

## 1. Executive Summary
- **Phase PC-09 작업 완결**: Barcelona(PC-06B/C), Girona(PC-07), Nice(PC-08/08B)에서 확립된 **Place Canonical SOT 및 5-Layer 콘텐츠 표준**을 Aix-en-Provence 권역 19개 Canonical Place에 전면 적용 완료.
- **Inventory 전수 조사 및 Gap 완결**: `day-13.json`에서 사용된 구시가지 `vieil-aix`의 누락을 식별하고 5-Layer Tier A 정본으로 신규 생성 및 Registry(`91_Place_Registry_v1.0.md`), Taxonomy(`PLACE_TAXONOMY_AND_TIERS.csv`)에 정식 등록.
- **Cézanne 핵심 Place 심화**: 세잔의 4대 핵심 명소(`atelier-des-lauves`, `montagne-sainte-victoire-terrain-des-peintres`, `bastide-du-jas-de-bouffan`, `carrieres-de-bibemus`)에 '알아야 보이는 시선' (북향 채광창, 벽면 캔버스 슬릿, 1:1 산과 화판 겹쳐보기, 큐비즘의 사암 절벽) 전면 보강.
- **Marseille Day-Trip 정합성 확보**: 6개 핵심 명소(`vieux-port-marseille`, `le-panier`, `mucem`, `fort-saint-jean`, `notre-dame-de-la-garde`, `marseille`)의 5-Layer 표준화 및 Ligne 50 고속버스 실용 정보 구축.
- **Chapter Dedup 완료**: `07_Aix_en_Provence_v2.0.md` 내의 모든 장소 장문 중복을 제거하고 Editor's Verdict 기반 Compact Card 및 링크 구조로 전환.
- **Trip Layer 완전 분리**: 장소 본문 내 여행 일자/일정 하드코딩 완전 제거.
- **전체 테스트 All PASS**: `site.py`, `ux_check.py`, `content_audit.py`, `validate_place_canonical_model.py` 100% 통과.

---

## 2. Inventory & Tier 분류 (19 Places)

| Slug | Place Name | Category | Tier | Priority | 5-Layer Coverage |
|---|---|---|---|---|---|
| `cours-mirabeau` | Cours Mirabeau | Urban / Axis | **TIER_A** | MUST_SEE | 100% |
| `vieil-aix` | Vieil Aix (구시가지) | Urban / Quarter | **TIER_A** | MUST_SEE | 100% (신설) |
| `atelier-des-lauves` | Atelier de Cézanne | Cézanne / Art | **TIER_A** | MUST_SEE | 100% |
| `montagne-sainte-victoire-terrain-des-peintres` | Terrain des Peintres | Cézanne / Nature | **TIER_A** | MUST_SEE | 100% |
| `place-richelme-place-des-precheurs` | 시장 (리셸므 & 프레셰르) | Market / Square | **TIER_B** | MUST_SEE | 100% |
| `musee-granet` | Musée Granet | Museum / Art | **TIER_B** | WORTHWHILE | 100% |
| `bastide-du-jas-de-bouffan` | Bastide du Jas de Bouffan | Cézanne / Heritage | **TIER_B** | WORTHWHILE | 100% |
| `carrieres-de-bibemus` | Carrières de Bibémus | Cézanne / Nature | **TIER_B** | WORTHWHILE | 100% |
| `rotonde` | Fontaine de la Rotonde | Urban / Landmark | **TIER_B** | WORTHWHILE | 100% |
| `vieux-port-marseille` | Vieux-Port de Marseille | Marseille / Port | **TIER_B** | MUST_SEE | 100% |
| `le-panier` | Le Panier | Marseille / Quarter | **TIER_B** | WORTHWHILE | 100% |
| `mucem` | Mucem | Marseille / Museum | **TIER_A** | MUST_SEE | 100% |
| `fort-saint-jean` | Fort Saint-Jean | Marseille / Fort | **TIER_B** | MUST_SEE | 100% |
| `notre-dame-de-la-garde` | Notre-Dame de la Garde | Marseille / Church | **TIER_A** | MUST_SEE | 100% |
| `marseille` | Marseille (도시 전체) | Marseille / City | **TIER_B** | MUST_SEE | 100% |
| `saint-paul-de-vence` | Saint-Paul-de-Vence | En-Route / Village | **TIER_A** | MUST_SEE | 100% |
| `grasse` | Grasse | En-Route / Town | **TIER_B** | WORTHWHILE | 100% |
| `cassis` | Cassis 항구 | Option / Coast | **TIER_B** | WORTHWHILE | 100% |
| `calanques` | Parc National des Calanques | Option / Nature | **TIER_B** | WORTHWHILE | 100% |

---

## 3. 5-Layer 품질 검증 결과
1. **Layer 1 (Facts)**: 주소, 위도/경도, 개방시간, 요금, 예약 규칙 100% 완비.
2. **Layer 2 (Strategy & Planning)**: Best For, Best Time, 권장 체류시간 명확화.
3. **Layer 3 (Experience & Atmosphere)**: 감각적 현장감, 역사적 서사 입체화.
4. **Layer 4 (Deep Guide - 알아야 보인다)**:
   - *Cézanne*: 북향 균일광의 원리, 대형 캔버스 벽면 홈의 이유, 9개 복제 화판 1:1 현장 대조법, 큐비즘 직각 사암.
   - *Marseille*: 노먼 포스터 거울 천장의 역상, 루이 14세 요새 포문이 도시를 향한 이유, 비에이 샤리테 자선과 격리의 지층, 뤼디 리치오티 UHPC 레이스 콘크리트 및 공중 보도교, 뱃사람들의 수호 성모 모형배.
   - *Aix Urban*: 1651년 옛 성벽 조성과 남북 비대칭, 4대 역사 분수(18℃ 온천수 이끼분수 등).
5. **Layer 5 (Practical & Transport)**: 접근 동선, 대중교통(L50 버스, M1 지하철, 60번 버스), 도심 주차 통제 수칙, 산불 통제 예보 연계 팁 완비.

---

## 4. 파이프라인 무결성 검증
- `site.py`: HTML 렌더링 정상 완료 (Place 단독 페이지, Region 카드, Day 카드 링크).
- `validate_place_canonical_model.py`:
  - Canonical SOT 파일 보존: PASS (빌드 전후 SHA-256 해시 100% 불변).
  - 장문 중복 검사: PASS (중복 시그니처 0건).
  - Trip Layer 분리: PASS (장소 본문 내 날짜 하드코딩 0건).
  - Day stop 참조 정합성: PASS (`day-13`, `day-14`, `day-15` 전수 일치).
- `content_audit.py`: 0 Error, 0 Content Loss PASS.
- `ux_check.py`: 모든 UI/UX 무결성 가드 PASS.
