# PC-08B Menton Canonical Place Gap Check & Completion QA Report

**작성일**: 2026-08-19  
**상태**: **ALL PASS (Menton Canonical SOT Established & Gap Closed)**  
**브랜치**: `feat/pc-08b-menton-canonical`  

---

## 1. Menton Previous Status & Investigation (조사 결과)

| 조사 항목 | 기존 상태 (Previous Status) | 판정 및 현황 |
|---|---|---|
| **`30_Places/menton.md` 존재 여부** | 부재 (`False`) | **GAP 발견** (SOT 파일 미생성 상태) |
| **`PLACE_TAXONOMY_AND_TIERS.csv`** | 미등록 (0건) | **GAP 발견** (Nice 15개 목록에 미포함) |
| **Day 10 Card (`day-10.json`)** | `id: "menton-old-town"`, `name: "Menton 구시가지 & 해변 산책"` | Stop 존재하나 canonical Place 파일 미연결 |
| **Region Chapter (`06_Nice_Cote_d_Azur`)** | 셀프 가이드 H4 목록에 부재 | Day 4 섹션에만 텍스트로 언급 |
| **Search / Map** | Menton 독립 Place 페이지 미생성 | 검색 색인 누락 |

---

## 2. Root Cause of Omission (누락 근본 원인 규명)

1. **Taxonomy & Tier CSV 추출 범위 한계**:
   - PC-08 초기에 Nice 권역 Place 목록을 작성할 때, `06_Nice_Cote_d_Azur_v2.0.md`의 기존 H4 헤딩(11개) 위주로 인벤토리를 구성함.
   - 당시 챕터 원고에는 Nice 도심, Monaco, Cannes만 H4로 등록되어 있었고, Menton은 Day 10 일정 본문에만 기재되어 있어 H4 인벤토리에서 누락됨.
2. **Day Stop ID와 Canonical Slug 불일치**:
   - `day-10.json`의 stop ID가 `menton-old-town`이라는 임의의 ID로 기재되어 있었으나, 이에 대응하는 `menton-old-town.md`나 `menton.md`가 생성되지 않고 단순 카드 텍스트로만 소비됨.
3. **Validator의 Scope Gap**:
   - `validate_place_canonical_model.py`가 사전에 지정된 `check_slugs` 배열에 대해서만 무결성을 검사하여 `menton`의 누락을 사전에 포착하지 못함.

---

## 3. Canonical Place Decision & Content Tier

- **Entity 구조 결정**:
  - `Menton`, `Vieille Ville`, `Basilique Saint-Michel-Archange`, `Plage des Sablettes`를 개별 파일로 과도하게 쪼개지 않고, **단일의 통합된 `source/CURRENT/30_Places/menton.md`**로 완결.
  - 하나의 밀도 높은 지중해 국경 마을 경험으로 소비되므로 통합 모델이 가장 적합.
- **Content Tier**: **Tier B (Core / MUST SEE)**
- **Editor's Verdict & 핵심 가치**:
  > "모나코(Monaco)의 과시적인 자본과 긴장감 넘치는 왕궁 뒤에 이어지는, **더 느리고 이탈리아적이며 따뜻한 색채 중심의 리비에라 마을 경험**이다. 모나코에서 TER로 10분 만에 닿아 가파른 돌계단을 올라 생 미셸 성당 앞 자갈 광장(Calade)에서 바다를 내려다보고, 사블레트 해변 방파제에서 파스텔 구시가지 전경을 감상한 뒤 항구에서 해산물 저녁을 즐기는 오후~저녁(3~4시간) 일정이 모나코와의 극적인 대비를 완성한다."

---

## 4. 5-Layer 표준 콘텐츠 완비 내역

1. **Facts**:
   - 주소: Menton, 06500 Alpes-Maritimes, France
   - 교통: Monaco-Monte-Carlo ↔ Menton (TER 10~12분), Nice-Ville ↔ Menton (TER 35~40분)
   - 성당 운영: 매일 10:00–12:00, 15:00–18:00 (무료)
   - 공식 사이트 및 확인일자: `verified_at: 2026-08-17`
2. **Strategy**:
   - Best Time: 늦은 오후 14:30~19:30 (서향광이 파스텔 벽면에 닿을 때)
   - Recommended Duration: 3~4시간 (오후 구시가지 산책 + 성당 언덕 + 방파제 엽서 뷰 + 항구 저녁 식사)
3. **Experience (Don't Miss)**:
   - 사블레트 방파제(Quai Bonaparte) 파스텔 구시가지 엽서 뷰
   - 생 미셸 대성당 지그재그 이중 나선 계단(Les Rampes Saint-Michel)
   - 구 성채 묘지(Cimetière du Vieux-Château) 정상 테라스 360도 국경 바다 뷰
4. **Deep Guide**:
   - 1619년 모나코 대공 오노레 2세 착공 제노바 바로크 성당과 흑백 조약돌 모자이크(La Calade)
   - 1848년까지 모나코 영토였던 멘통의 프랑스·이탈리아 국경 문화사
   - 연중 300일 온난한 미기후와 멘통 레몬(Citron de Menton PGI)
5. **Practical**:
   - Menton 기차역에서 구시가지 도보 12~15분 평탄 이동
   - 구항구 해산물 식당(Le Petit Port 등) 저녁 및 Nice 야간 TER 귀환 팁

---

## 5. Day & Region Integration (연동 완료)

- **Day 10 (`data/daily-cards/day-10.json`)**:
  - Stop ID를 canonical `menton`으로 정돈 (`order: 5`, `start: 14:30`, `end: 18:30`).
  - Legs 연결 (`monte-carlo` → `menton` → `menton-dinner`) 정상화.
- **Region Chapter ([`06_Nice_Cote_d_Azur_v2.0.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-2/source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md))**:
  - `Le Rocher` 바로 뒤에 `Menton (멘통) {{grade:essential|필수}}` Compact Reference 및 `[상세 가이드 보기]` 링크 추가.
- **Taxonomy CSV ([`PLACE_TAXONOMY_AND_TIERS.csv`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-2/PLACE_TAXONOMY_AND_TIERS.csv))**:
  - `menton` 레코드 (Tier B / MUST SEE) 정식 등록.

---

## 6. Validation Improvement (재발 방지 가드 강화)

- `scripts/validate_place_canonical_model.py`의 `check_slugs`에 `menton`을 추가하여 Overwrite Protection, Dedup, Trip Layer Separation을 전수 자동 검증.
- Day Stops 참조 무결성 검증을 통해 향후 권역에서도 누락된 Place가 즉각 포착되도록 보강.

---

## 7. 검증 결과 요약 (Validation Suite ALL PASS)

| 검증 항목 | 대상 도구 | 결과 | 세부 내용 |
|---|---|---|---|
| **Menton Canonical SOT** | `30_Places/menton.md` | **PASS** | 5-Layer 표준 완비 및 단일 SOT 확립 |
| **Place Overwrite Protection** | `validate_place_canonical_model.py` | **PASS** | 빌드 전후 100개 Place 파일 SHA-256 해시 100% 불변 |
| **Duplicate Long-Form Detection** | `validate_place_canonical_model.py` | **PASS** | Barcelona, Girona, Nice 챕터 내 중복 장문 0건 |
| **Trip Layer Separation** | `validate_place_canonical_model.py` | **PASS** | 28개 장소 본체 내 일자 하드코딩 0건 |
| **Reference Integrity** | `validate_place_canonical_model.py` | **PASS** | Day 10 및 Region 챕터 참조 무결성 100% |
| **Content Audit Guard** | `build/content_audit.py` | **PASS** | 100개 장소 685개 문단 검사, **콘텐츠 손실 0건** |
| **UX & Outdoor Contrast** | `build/ux_check.py` | **PASS** | 335개 정적 페이지 야외 가독성 ALL PASS |
| **Static Site Build** | `build/site.py` | **PASS** | 335개 정적 페이지 정상 빌드 |

---

## 8. 최종 판정

- **최종 판정**: **PASS (Menton Canonical Gap Resolved & Completed)**
- **후속 단계**: Menton 누락 갭이 완전히 해소되었으므로 **Aix-en-Provence & Luberon 권역 Place Content Enrichment (Phase PC-09)**로 안전하게 확장이 가능합니다.
