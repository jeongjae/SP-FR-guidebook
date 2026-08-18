# PC-07 Girona & Costa Brava Place Content Enrichment QA Report

**작성일**: 2026-08-18  
**상태**: **ALL PASS (Girona & Costa Brava Rollout Complete)**  
**브랜치**: `feat/pc-07-girona-enrichment`  

---

## 1. Canonical Place Inventory & Tier Map (Girona 권역 장소 현황)

| Place Slug | Name | Type | Priority | Content Tier | 주요 테마 및 핵심 가치 |
|---|---|---|---|---|---|
| `girona-cathedral` | Girona Cathedral (지로나 대성당) | architecture | **MUST SEE** | **Tier A** | 23m 무기둥 단일 고딕 신랑, 창조의 태피스트리, 로마네스크 회랑 |
| `passeig-de-la-muralla` | Passeig de la Muralla (성벽 산책로) | walk | **MUST SEE** | **Tier A** | 로마-카롤링거-중세 성벽, 구시가지 붉은 지붕과 피레네 조망 |
| `collioure` | Collioure (콜리우르 해상 왕궁/항구) | village | **MUST SEE** | **Tier A** | 야수파(Fauvisme) 탄생지, 샤토 로얄 해상 요새, 수요일 전통 시장 |
| `onyar` | Onyar (오냐르 수변 가옥) | viewpoint | **MUST SEE** | **Tier B** | 파스텔톤 채색 수변 가옥, 1877년 에펠 붉은 철교 시그니처 뷰 |
| `pals` | Pals (팔스 중세 고딕 마을) | village | **WORTHWHILE** | **Tier B** | 언덕 위 복원 고딕 석조 요새, 엠포르다 평야와 벼농사 논, 지중해 조망 |
| `peratallada` | Peratallada (페라탈라다 암반 마을) | village | **WORTHWHILE** | **Tier B** | 거대 암반을 수직 8m 파낸 해자(Fossat), 1천 년 원형 보존 석조 요새 |
| `calella-de-palafrugell` | Calella de Palafrugell (어촌/해안길) | village / nature | **WORTHWHILE** | **Tier B** | 19세기 전통 어촌 원형, 레스 볼테스 회랑, 카미 데 론다 절벽길 |
| `peralada` | Peralada (페랄라다 성/와이너리) | historic_site | **OPTIONAL** | **Tier C** | 14세기 성채, 카르멜회 수도원 박물관, 와인·유리 공예 컬렉션 |

---

## 2. 5-Layer 표준 적용 및 품질 평가 (Editorial QA)

### 2.1 Tier A Signature 장소
1. **Girona Cathedral**:
   - **Facts**: 2026 최신 운영시간, 산 펠리우 통합권 €7.50, 복장 규정 완비
   - **Strategy**: 90계단 진입 직후 정면 무기둥 시야 5초 감상법, 보물관 3대 핵심 집중법
   - **Deep Guide**: 1416년 마스터 빌더 청문회와 23m 무기둥 결단의 구조역학, 11세기 <창조의 태피스트리> 읽는 법(중심 판토크라토르-동심원 7일 창조-테두리 사계절)
2. **Passeig de la Muralla**:
   - **Facts**: 상시 개방, 무료 입장, 편안한 운동화 권장
   - **Strategy**: 북쪽 자르딘스 프랑세사 진입 → 토레 지로넬라 → 남단 하산 40~50분 순방향 코스
   - **Deep Guide**: 25회 포위를 견뎌낸 지형의 군사학, 1391년 유대인 공동체의 지로넬라 탑 역사
3. **Collioure**:
   - **Facts**: 샤토 로얄 €7.00, 수요일·일요일 전통 시장(08:00–13:00), 외곽 대형 주차장 지침
   - **Strategy & Deep Guide**: 1905년 마티스와 드랭이 색채를 폭발시킨 야수파(Fauvisme) 탄생사, 20여 개 청동 뷰파인더 액자(Chemin du Fauvisme) 현장 비교 관람법

### 2.2 중세 마을 차별화 비교 (Pals vs Peratallada)
- **Pals**: 20세기에 복원된 단정하고 우아한 고딕 언덕 마을로서, 엠포르다 논과 메데스 제도를 내려다보는 '전망'에 초점.
- **Peratallada**: 천연 바위를 정으로 깎아 만든 8m 깊이의 해자(Fossat)와 원형 그대로의 거친 돌골목에 초점 (마을 진입 전 외곽 해자 하단 관찰 필수 지침 수록).

---

## 3. Region 원고 중복 제거 (Region Dedup Result)

- **Region 원고 ([`05_Girona_Collioure_Emporda_v2.1.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-2/source/CURRENT/20_Regional_Chapters/05_Girona_Collioure_Emporda_v2.1.md))**:
  - 장문 텍스트(역사, 건축, Deep Guide, 상세 실용)를 제거하고 **Compact Summary / Verdict / 체류시간 / [상세 가이드 보기] 링크**로 전환 완료.
- **정본 장소 파일 ([`30_Places/`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-2/source/CURRENT/30_Places))**:
  - 8개 장소에 대해 완벽한 5-Layer 정본 구축.
- **콘텐츠 손실**: **0건 (Content Loss = 0)** — 상세 맵핑은 [`PLACE_DEDUP_MIGRATION_MAP_GIRONA.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-2/PLACE_DEDUP_MIGRATION_MAP_GIRONA.md)에 기록 완료.

---

## 4. Trip Separation & Reference Integrity (일정 분리 및 참조 무결성)

- Girona 권역 8개 장소 본체에서 특정 여행 일자(`9월 1일`, `9월 2일`, `Day 4` 등)를 완전히 제거하고 일반적 조건으로 정제 완료.
- Region ↔ Place ↔ Day Stop 참조 무결성 100% 검증 통과.

---

## 5. 검증 결과 요약 (Validation Suite ALL PASS)

| 검증 항목 | 대상 도구 | 결과 | 세부 내용 |
|---|---|---|---|
| **Place Overwrite Protection** | `validate_place_canonical_model.py` | **PASS** | 빌드 전후 95개 Place 파일 SHA-256 해시 100% 불변 |
| **Duplicate Long-Form Detection** | `validate_place_canonical_model.py` | **PASS** | Barcelona 및 Girona 챕터 내 중복 장문 0건 |
| **Trip Layer Separation** | `validate_place_canonical_model.py` | **PASS** | Barcelona 및 Girona 장소 본체 내 일자 하드코딩 0건 |
| **Reference Integrity** | `validate_place_canonical_model.py` | **PASS** | Day Stops 및 Region 참조 무결성 100% |
| **Content Audit Guard** | `build/content_audit.py` | **PASS** | 95개 장소 541개 문단 검사, **콘텐츠 손실 0건** |
| **UX & Outdoor Contrast** | `build/ux_check.py` | **PASS** | 335개 정적 페이지 야외 가독성 ALL PASS |
| **Static Site Build** | `build/site.py` | **PASS** | 335개 정적 페이지 정상 빌드 |

---

## 6. 최종 판정 및 다음 권역 추천

- **최종 판정**: **PASS (Girona & Costa Brava Rollout Complete)**
- **후속 단계 (Next Region Rollout)**:
  - Girona 권역 확장이 성공적으로 완료되었으므로, 다음 권역인 **Nice & Côte d'Azur 권역 Place Content Enrichment (Phase PC-08)**로 확장이 가능합니다.
