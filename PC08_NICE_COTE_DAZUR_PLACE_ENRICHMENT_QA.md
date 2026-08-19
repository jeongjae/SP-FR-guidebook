# PC-08 Nice & Côte d'Azur Place Content Enrichment QA Report

**작성일**: 2026-08-19  
**상태**: **ALL PASS (Nice & Côte d'Azur Rollout Complete)**  
**브랜치**: `feat/pc-08-nice-enrichment`  

---

## 1. Canonical Place Inventory & Tier Map (Nice & Côte d'Azur 권역 장소 현황)

| Place Slug | Name | Type | Priority | Content Tier | 주요 테마 및 핵심 가치 |
|---|---|---|---|---|---|
| `promenade-des-anglais` | Promenade des Anglais (영국인의 산책로) | promenade | **MUST SEE** | **Tier A** | 7km 천사의 만 해안 산책로, 벨 에포크 호텔 네그레스코, 파란 의자(Chaises Bleues) |
| `vieux-nice` | Vieux Nice (비외 니스 구시가지) | district | **MUST SEE** | **Tier A** | 500년 사보이 통치의 이탈리아적 미로 골목, 트롱프뢰유 벽화, 생트 레파라트 성당, 로세티 광장 |
| `le-rocher` | Le Rocher (모나코 구시가지) | district | **MUST SEE** | **Tier A** | 60m 절벽 위 왕궁 마을, 11:55 위병 교대식, 모나코 대성당(그레이스 켈리의 묘) |
| `monaco` | Monaco (모나코 공국 전체) | city / region | **MUST SEE** | **Tier A** | 르 로셰-에르퀼 항구-몬테카를로 3대 레이어의 수직적 대비, F1 서킷, 카지노 광장 |
| `colline-du-chateau` | Colline du Château (성채 언덕) | viewpoint | **MUST SEE** | **Tier B** | 해발 92m 절벽 위 천사의 만과 림피아 항구 360도 양방향 조망, 1885년 인공폭포 |
| `cours-saleya` | Cours Saleya (쿠르 살레야 시장) | market | **MUST SEE** | **Tier B** | 지중해 꽃과 프로방스 제철 농산물, 화덕에서 갓 구운 바삭한 니스 전통 소카(Socca) |
| `le-suquet` | Le Suquet (칸 구시가지) | district | **WORTHWHILE** | **Tier B** | 11세기 레랭 수도사 요새 어촌, 가파른 돌계단 골목, 노트르담 드 레스페랑스 전망대 |
| `cannes` | Cannes (칸 도시 전체) | city | **WORTHWHILE** | **Tier B** | 영화제 상징 크루아제트 대로와 레드카펫, 구항구와 르 쉬케 어촌의 대비 |
| `nice-walk` | Nice Old Town–Castle Hill Walk | walk | **WORTHWHILE** | **Tier B** | 쿠르 살레야 시장 → 비외 니스 → 성채 언덕 지중해 낙조 완결 코스 |
| `marche-forville` | Marché Forville (칸 포르빌 시장) | market | **MUST SEE** | **Utility** | 1934년 칸 철골 재래시장, 지중해 해산물과 피살라디에르, 제철 과일 |
| `marche-de-la-liberation` | Marché de la Libération (리베라시옹 시장) | market | **WORTHWHILE** | **Utility** | 니스 북부 최대 현지인 생활시장, 가르 뒤 쉬드(Gare du Sud) 푸드홀 |
| `nce-t2` | NCE T2 (니스 공항 터미널 2 & 트램 L2) | transport | **WORTHWHILE** | **Utility** | 니스 공항 ↔ 도심 25분 직결 트램 L2 노선, 발권 및 태그(Validation) 가이드 |
| `nice-ville` | Nice-Ville (니스 빌 중앙역) | transport | **WORTHWHILE** | **Utility** | 모나코·멘통·칸 방면 TER 코트다쥐르 해안선 열차 관문 및 좌석 뷰 팁 |
| `cannes-walk` | Cannes Forville–Suquet–Croisette Walk | walk | **OPTIONAL** | **Tier C** | 포르빌 시장 → 르 쉬케 언덕 → 구항구 → 크루아제트 75분 도보 코스 |
| `monaco-walk` | Monaco Rocher–Port–Monte Carlo Walk | walk | **OPTIONAL** | **Tier C** | 르 로셰 위병 교대식 → 랑프 마요르 계단 → 에르퀼 항구 → 카지노 광장 코스 |

---

## 2. 최신 Trip Layer와의 정합성 보증 (Itinerary Consistency)

1. **Nice 도착일 (Day 3 / 도착편)**:
   - 항공 도착 16:55 → 트램 2호선(L2, `nce-t2`) 탑승 → 도심 숙소 체크인 18:00~19:00 → 프롬나드 데 장글레/구시가지 가벼운 저녁 산책 흐름 완벽 정합.
2. **Monaco + Menton 당일치기 (Day 4)**:
   - 오전: Nice-Ville (`nice-ville`) → Monaco-Monte-Carlo (TER 20분) → Le Rocher (`le-rocher`, `monaco`) 11:55 위병 교대식 및 콩다민 시장 점심.
   - 오후: Monaco → Menton (TER 10분) → 구시가지 및 생미셸 성당 언덕, 해변 산책 및 멘통 저녁 식사.
   - 밤: Menton → Nice-Ville (TER 35분, 21:00~22:00 귀환) 흐름 완벽 정합.
   - Place 본체에는 일자/시간 하드코딩이 일절 배제되어 Trip Layer와 독립적으로 유지됨.

---

## 3. 5-Layer 표준 적용 및 품질 평가 (Editorial QA)

- **Editor's Verdict의 판단성**:
  - *Promenade des Anglais*: 단순 해변 도로가 아닌 유럽 근대 휴양 문화의 발상지로서의 일몰 산책 가치 제시.
  - *Monaco*: 단순 화려함 대신 르 로셰의 왕궁 역사와 몬테카를로의 과시적 현대성의 수직적 대비를 반나절에 걷는 핵심 전략 제시.
  - *Vieux Nice*: 500년 사보이 통치가 남긴 '프랑스 안의 이탈리아' 정체성 해설.
- **Deep Guide (“알아야 보인다”)**:
  - 트롱프뢰유 벽화의 창문세 회피 및 대칭미 구현 역사.
  - 샤를 가르니에의 호텔 네그레스코와 카지노 데 몬테카를로 건축사.
  - 1706년 루이 14세의 니스 요새 폭파 평탄화와 19세기 공원화 과정.

---

## 4. Region 원고 중복 제거 (Region Dedup Result)

- **Region 원고 ([`06_Nice_Cote_d_Azur_v2.0.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-2/source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md))**:
  - 장문 텍스트를 제거하고 **Compact Summary / Verdict / 체류시간 / [상세 가이드 보기] 링크**로 전환 완료.
- **콘텐츠 손실**: **0건 (Content Loss = 0)** — 상세 맵핑은 [`PLACE_DEDUP_MIGRATION_MAP_NICE.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-2/PLACE_DEDUP_MIGRATION_MAP_NICE.md)에 기록 완료.

---

## 5. 검증 결과 요약 (Validation Suite ALL PASS)

| 검증 항목 | 대상 도구 | 결과 | 세부 내용 |
|---|---|---|---|
| **Place Overwrite Protection** | `validate_place_canonical_model.py` | **PASS** | 빌드 전후 99개 Place 파일 SHA-256 해시 100% 불변 |
| **Duplicate Long-Form Detection** | `validate_place_canonical_model.py` | **PASS** | Barcelona, Girona, Nice 챕터 내 중복 장문 0건 |
| **Trip Layer Separation** | `validate_place_canonical_model.py` | **PASS** | 대상 27개 장소 본체 내 일자 하드코딩 0건 |
| **Reference Integrity** | `validate_place_canonical_model.py` | **PASS** | Day Stops 및 Region 참조 무결성 100% |
| **Content Audit Guard** | `build/content_audit.py` | **PASS** | 99개 장소 637개 문단 검사, **콘텐츠 손실 0건** |
| **UX & Outdoor Contrast** | `build/ux_check.py` | **PASS** | 335개 정적 페이지 야외 가독성 ALL PASS |
| **Static Site Build** | `build/site.py` | **PASS** | 335개 정적 페이지 정상 빌드 |

---

## 6. 최종 판정 및 다음 권역 추천

- **최종 판정**: **PASS (Nice & Côte d'Azur Rollout Complete)**
- **후속 단계 (Next Region Rollout)**:
  - Nice & Côte d'Azur 권역 확장이 성공적으로 완료되었으므로, 다음 권역인 **Aix-en-Provence & Luberon 권역 Place Content Enrichment (Phase PC-09)**로 확장이 가능합니다.
