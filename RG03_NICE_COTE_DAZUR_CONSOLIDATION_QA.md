# RG03_NICE_COTE_DAZUR_CONSOLIDATION_QA — Nice & Côte d’Azur Region Consolidation QA

**작성일**: 2026-08-23  
**브랜치**: feat/rg03-nice-consolidation  
**대상 권역**: Nice & Côte d'Azur (06_Nice_Cote_d_Azur)  
**상태**: PASS (승인 대기)

---

## 1. 정량 보고 (Quantitative Metrics)

| 지표 항목 | 수치 | 비고 |
|---|---:|---|
| **Total Inventory Blocks** | **69** | 전수 인벤토리 블록 |
| **KEEP** | **28** | Region 고유 큐레이션 및 필수 콘텐츠 |
| **MERGE** | **2** | 식당 카드 중복 통합 (Le Figuier de Saint-Esprit, Restaurant Béatrice) |
| **MOVE** | **21** | 장소 정본(30_Places/), Day 일정(10_Core/), Prepare/Transport 레퍼런스 등으로 이동 |
| **ARCHIVE** | **3** | 마티스/샤갈 화요일 휴관 제외 사유, 칸 레랭 제도 보트 제외 사유, 에즈/빌프랑슈 무리한 추가 제외 사유 |
| **DELETE** | **15** | Day 이동 접이식과 100% 일치하는 단순 복제 문자열 11건 + 비업소 식사 슬롯 카드 4건 |
| **Duplicate Candidates Before** | **38** | 통폐합 전 구조적/텍스트 중복 후보 수 |
| **Unresolved Duplicates After** | **0** | 통폐합 후 미해결 중복 잔여 수 |
| **Character Count Before** | **25,141자** | 원고 원천 (06_Nice_Cote_d_Azur_v2.0.md) |
| **Character Count After** | **6,820자** | 정규화된 Region 마크다운 (20_Regions/nice.md) |
| **Reduction % (감량률)** | **72.87%** | 순수 Region 정규화 감량률 |
| **H2 Before / After** | **21개 → 9개** | 원고 원천 H2 21개 → 정규화 Region H2 9개 (최상위 표준 H2 6개 구조) |
| **H3 Before / After** | **11개 → 0개** | 원고 원천 H3 11개 → 정규화 Region H3 0개 (H4 서브섹션 5개로 정규화) |
| **Day Links Before / After** | **6개 → 31개** | 상단 날짜 칩 6개 + 도착/출발 2개 + 방문일 배지 23개 |
| **Place Links Before / After** | **0개 → 21개** | 볼거리 14개 + 식당/시장 2개 + Hero/Context 5개 |

---

## 2. 파일 영향 범위 (File Traceability)

- **Canonical Source Files Changed**: 0건 (이미 정본화 완료)
- **Generated Files Affected**: site/guide/nice.html, site/guide/index.html
- **Archive Files Changed**: data/decisions.json
- **Place Dossiers Touched (15개)**:
  promenade-des-anglais, vieux-nice, colline-du-chateau, cours-saleya, le-rocher, monaco, le-suquet, cannes, marche-forville, marche-de-la-liberation, nce-t2, nice-ville, nice-walk, cannes-walk, monaco-walk
- **Day Sources Touched**: data/daily-cards/day-07.json ~ day-12.json
- **Data Files Touched**: data/region-essentials.json, data/transit-facts.json, data/transit-resources.json

---

## 3. QA 및 유효성 검증 (Verification Results)

- **python3 build/site.py**: PASS (372쪽 렌더, 검색 색인 191건)
- **pytest tests/**: PASS (30 passed in 8.71s)
- **python3 build/region_structure_check.py**: PASS (오분류 0, 레거시 섹션 0, 잘못된 Day 참조 0, 끊어진 링크 0)
- **python3 build/media_lookup_check.py**: PASS (미매핑 사진 0, 유실 사진 0)
- **python3 build/table_loss_check.py**: PASS (테이블 열 손실 0)
- **콘텐츠 및 핵심 사실 보존**:
  - 중요 정보 유실: 0건
  - 확정 일정 임의 변경: 0건 (9/4~9/9 Nice 5박 불변)
  - 확정 예약/비용 임의 변경: 0건 (Palais ALZIRA €809.54, Hertz 렌터카 불변)

---

## 4. Scope 밖 Factual Issues

- **Marché Forville (Cannes) 임시 이전**:
  - 2026년 대규모 개보수 공사로 임시 이전 운영 중 (fact:marche-forville.note 및 fact:marche-forville.hours 유지).
- **Monaco 대공궁 위병 교대식**:
  - 11:55 고정 의식이 공식 행사에 따라 변동 가능 (fact:monaco.note 유지).
