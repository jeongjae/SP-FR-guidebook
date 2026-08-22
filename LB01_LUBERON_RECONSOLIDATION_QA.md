# LB01 — Luberon Region Editorial Re-Consolidation QA Report

- **일자**: 2026-08-23
- **작업 브랜치**: `fix/luberon-region-editorial-consolidation`
- **대상 지역**: `luberon` (챕터 08)
- **카노니컬 챕터**: [`source/CURRENT/20_Regional_Chapters/08_Luberon_Farmhouse_v2.0.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/source/CURRENT/20_Regional_Chapters/08_Luberon_Farmhouse_v2.0.md)
- **승격 지역 파일**: [`source/CURRENT/20_Regions/luberon.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/source/CURRENT/20_Regions/luberon.md)
- **아카이브 파일**: [`source/ARCHIVE/20_Regional_Chapters/08_Luberon_Planning_Residue_v1.0.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/source/ARCHIVE/20_Regional_Chapters/08_Luberon_Planning_Residue_v1.0.md)
- **출력 HTML**: [`site/guide/luberon.html`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/site/guide/luberon.html)

---

## 1. Overall Status

- **상태**: **PASS (외부 Editorial Review 대기)**
- Barcelona (RC01F), Girona (GR01F), Aix (AX01F)와 동일한 단일 상용 IA 체계(`rc-region-v1`)로 완벽 통폐합 완료.
- Farmhouse 숙소 상태 정규화, 일정 단일화, 후보지 평가표 및 기획 잔재 100% 아카이브 완료.
- 자동화 QA 가드 10종 전수 통과 (원고 흔적 0 달성).

---

## 2. Farmhouse SOT / Booking Status Reconciliation

- **판정 결과**: **"3박 농가 체류는 확정이나 특정 농가(`Domaine des Peyre`)는 유력 후보(candidate) 상태"**
- **근거 SOT**:
  - `data/daily-cards/day-16.json`, `day-17.json`, `day-18.json`: `hotel.name: "Domaine des Peyre (후보)"`, `hotel.status: "candidate"`
  - `data/map-lookup/batch3.csv`: `"공식 GPS 와 좌표 정확히 일치. 미확정 후보 — 확정 표기 금지"`
  - `data/region-essentials.json`: `"3박 거점은 대중교통 정류장이 아닌 농가 숙소다. Day 16–19의 마을 순회는 예약 렌터카를 정본으로 삼고, 도착 즉시 진입로·주차 위치와 야간 귀환 표식을 확인한다."`
- **반영 조치**:
  - Region 본문(Stay & Local Life)에서는 특정 농가명을 확정된 사실처럼 단정하지 않고, `3박 농가 체류`를 전제로 한 농가 생활권 운영 원칙(렌터카 이동, 일요 시장 장보기, 테라스 식사, 야간 운전 자제)을 담백하게 서술.
  - 숙소 카드는 표준 메타데이터(`Domaine des Peyre (후보)`)를 그대로 연동.

---

## 3. Before Actual Render 문제점 진단

1. **기획 메모 및 내부 평가 지표 노출**:
   - `여행 적합도 ★★★★★`, 예산 체감, 일정 강도 등 원고 평가표 노출.
   - `여행의 역할`, `최신 확정사항`, `사용자 선호 반영`, `수영장 평가는 완전 제외` 등 기획자 내부 의사결정 기록 노출.
2. **구조적 다중 중복**:
   - `꼭 경험할 세 장면`, `놓치면 아쉬운 선택`, `하루를 완성하는 네 가지 선택`, `추천 체류 리듬` ASCII 다이어그램, 5열 일정표, Day별 식사표 등으로 일정 및 경험이 4중 이상 중복 서술됨.
3. **숙소 후보 권역 및 채점표 노출**:
   - Goult-Robion-Oppède 1순위, Ménerbes 1.5순위, Gordes 2순위 등 6개 권역 비교표 노출.
   - 7개 숙소 후보에 대한 가중치 10개 항목 채점표(94/100, 92/100 등) 노출.
4. **일정 미포함 후보지 및 기획 이력 노출**:
   - L'Isle-sur-la-Sorgue 목요시장 날짜 불일치 사유, Apt 토요 대형시장 불일치 사유, Verdun 협곡 제외 사유 등 planning rationale가 본문에 장문으로 노출.
5. **원고 메모체 및 구어체 지시문**:
   - "늦잠을 자면 그날의 절반이 없어진다", "하루 세 마을이면 운전과 주차만 하다 끝난다", "차가 들어가면 나올 수 없다" 등 메모체 산재.

---

## 4. External Editorial Decisions 반영 결과

| # | 항목 | 작업 내용 |
|---|---|---|
| 1 | **Overview 통합** | 평가표(`★★★★★`), 내부 확정사항, 사용자 선호 반영, 꼭 경험할 세 장면을 제거하고 정제된 `Luberon을 이렇게 본다`로 단일화 |
| 2 | **Schedule 단일화** | ASCII 다이어그램, 5열 일정표, Day별 식사표를 전면 제거하고 Day SOT 기반의 간결한 2열 표 1개로 단일화 |
| 3 | **Places Curation 정돈** | 11개 등록 장소에 대해 Actual / Optional / Backup / 일정 미포함을 명확히 구분하고 등급 정규화 |
| 4 | **Stay & Local Life 재작성** | 후보 권역 비교, 숙소 채점표, 수영장 평가 제외 문구를 제거하고 농가 체류 생활권 원칙으로 압축 |
| 5 | **Transport 허브 수준 압축** | ZOU! 버스 매뉴얼, D-도로 거리계수, 주유요령, 세부 주차순서를 분리하고 4개 핵심 소주제로 압축 |
| 6 | **Food 밀도 축소** | 6개 대표 식재료/요리를 1문장 담백한 설명으로 축소, 뤼베롱 AOC 로제 와인 분리, 시장 2곳 링크 및 농가 식사 원칙 정돈 |

---

## 5. Overview Before / After

### Before
```text
| 항목 | 평가 |
| 여행 적합도 | ★★★★★ Jason·Julia의 생활형 여행에 최적화 |
| 예산 체감 | 숙박비 높음 |
| 일정 강도 | 느림 |
> 여행의 역할: ... 이 구간의 목적은 유명마을을 가능한 많이 수집하는 것이 아니라 ...
> 최신 확정사항: 프로방스는 엑상 4박 + 뤼베롱 농가 3박 + 아비뇽 4박으로 운영하며 ... 수영장 유무·가열·길이는 숙소 평가에서 완전히 제외하고 ...
> 사용자 선호 반영: 실내 전시보다 Lourmarin, Roussillon, Goult 또는 Bonnieux ...
```

### After
```markdown
## Luberon을 이렇게 본다

Luberon에서는 도시 관광의 속도를 낮추고 농가 생활과 작은 마을을 중심으로 3박을 보낸다. 시장에서 장을 보고, 낮에는 서로 다른 풍경과 돌빛을 가진 마을을 몇 곳만 골라 걷고, 오후에는 숙소로 돌아와 쉬는 리듬이 이 구간의 핵심이다.

Roussillon에서는 오커 지형을, Gordes와 주변 마을에서는 밝은 석회암 건축을 보고, Goult와 Ménerbes 같은 작은 마을에서는 관광명소보다 골목과 생활 풍경에 시간을 쓴다. 장소의 수를 늘리기보다 하루에 한두 개의 중심 경험을 남긴다.

### 이번 3박의 핵심

- **농가 생활** — 시장에서 산 빵·치즈·과일과 채소로 간단히 먹고, 테라스와 주변 산책을 하루 일정의 일부로 둔다.
- **Roussillon의 오커** — 다른 Luberon 마을과 전혀 다른 색과 지질을 직접 걷는다.
- **Gordes와 석조마을** — 돌과 지형이 마을의 형태를 어떻게 바꾸는지 비교한다.

9월 중순은 라벤더보다 포도와 무화과, 수확기의 농촌 풍경을 보는 시기다. 유명마을을 모두 돌기보다 숙소로 돌아오는 시간을 충분히 남긴다.
```

---

## 6. Schedule Reconciliation

### 최종 정본 일정표
```markdown
## 일정

| 날짜 | 핵심 일정 |
|---|---|
| 9/13 일 | Aix 체크아웃 · Lourmarin · Coustellet 시장 · Luberon 농가 체크인 |
| 9/14 월 | Roussillon 오커길 · 농가 휴식 · Goult |
| 9/15 화 | Gordes · Village des Bories · 선택 일정 · 농가 |
| 9/16 수 | 농가 체크아웃 · Avignon 이동 |

상세 시각, 주차, 식사와 선택 일정은 각 날짜의 Day 페이지에서 확인한다.
```

---

## 7. Day 16 Goult Reconciliation

- **Day 16**: Coustellet 시장 장보기 후 `Goult 점심 (선택)`으로 완충시간 활용 (피로 시 생략 가능).
- **Day 17**: 오후 17:00~19:00 `Goult 산책`이 본 일정 정본 (생활마을 골목 및 17세기 풍차 조망).
- Region 요약표에서는 혼선을 방지하기 위해 Day 16에서는 `Coustellet 시장 · Luberon 농가 체크인`을 핵심으로 두고, Goult는 Day 17의 주요 방문지로 배치하여 이중 확정 오해를 완벽히 해소함.

---

## 8. Day 18 Optional Place Reconciliation

- **Gordes**: Actual (`{{grade:essential|필수}}`)
- **Village des Bories**: Actual (`{{grade:priority|우선추천}}`)
- **Abbaye Notre-Dame de Sénanque**: Optional (`{{grade:optional|선택}}` — Day 18 선택 옵션)
- **Ménerbes**: Optional (`{{grade:optional|선택}}` — Day 18 선택 옵션)
- Region 일정표 및 장소 카드 메타데이터에서 Sénanque와 Ménerbes를 고정 필수로 승격하지 않고 명확한 `선택 일정`으로 유지.

---

## 9. Aix → Luberon Transfer Reconciliation

- Day 16 (9/13 일) 인계:
  - Aix 체크아웃 (08:00) → D943 북행 → Lourmarin (09:30~11:30) → Coustellet 생산자 시장 (12:00~13:30) → [Goult 선택 완충] → Luberon 농가 체크인 (15:30~17:00).
  - Aix Region, Luberon Region, Day 16 페이지 간 순서와 상태가 100% 일치함.

---

## 10. Luberon → Avignon Transfer Reconciliation

- Day 19 (9/16 수) 인계:
  - 농가 아침 및 체크아웃 (09:30~10:30) → D900/N100 도로 서행 이동 (35km) → Avignon 성벽 주차장 도착.
  - Luberon Region에서는 체크아웃 및 이동 요약까지만 다루고, Avignon 시내 상세 일정은 Avignon Day SOT로 위임.

---

## 11. Places Actual / Optional / Archive Classification

## 11. Places Actual / Optional / Archive Classification

| 장소명 | 슬러그 | 등급 | 여행 내 역할 | 최종 Region Card |
|---|---|---|---|:---:|
| **Lourmarin** | `lourmarin` | 필수 | Day 16 실제 방문지 (카뮈 묘소, 플라타너스 거리) | **유지** |
| **Coustellet 생산자 시장** | `coustellet` | 필수 | Day 16 실제 장보기 (일요 파머스 마켓) | **유지** |
| **Roussillon · Sentier des Ocres** | `roussillon-sentier-des-ocres` | 필수 | Day 17 실제 방문지 (오커 트레일) | **유지** |
| **Goult** | `goult` | 우선추천 | Day 17 실제 방문지 (석조 생활마을, 풍차) | **유지** |
| **Gordes** | `gordes` | 필수 | Day 18 실제 방문지 (화요 시장, 전망대) | **유지** |
| **Village des Bories** | `village-des-bories` | 우선추천 | Day 18 실제 방문지 (건식 석조 오두막) | **유지** |
| **Abbaye Notre-Dame de Sénanque** | `abbaye-de-senanque` | 선택 | Day 18 선택 옵션 (12세기 시토회 수도원) | **유지 (선택)** |
| **Ménerbes** | `menerbes` | 선택 | Day 18 선택 옵션 (피터 메일 능선 성채 마을) | **유지 (선택)** |
| **Bonnieux** | `bonnieux` | 대체 | Day 17 대체 옵션 (Goult 대체 전망마을) | **유지 (대체)** |
| **Oppède-le-Vieux** | `oppede-le-vieux` | 선택 | 본 일정 미포함 (Dossier 보존, Region Card 제거) | **제거 (Archive-only)** |
| **L'Isle-sur-la-Sorgue** | `l-isle-sur-la-sorgue` | 선택 | 본 일정 미포함 (Dossier 보존, Region Card 제거) | **제거 (Archive-only)** |

---

## 12. Place Long-form MOVE

- 개별 마을의 상세 역사, 건축 양식, 지질학적 배경, 주차 및 운영 요금 상세는 개별 Place Dossier([`source/CURRENT/30_Places/`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/source/CURRENT/30_Places/))에 위임하고 Region 카드에서는 1문장 핵심 가이드 및 링크만 제공.

---

## 13. Food Cleanup (LB01F 반영)

- **Luberon에서 맛볼 프로방스 식재료**: 과도한 Luberon 고유 귀속 표현을 완화하고, Banon AOP, Cavaillon 멜론, 솔리에스 무화과, 타프나드&앙쇼이아드, 프로방스 꿀, 뤼베롱 올리브유 등 6종을 1문장으로 간결하게 기술.
- **로제 와인**: 음식 목록에서 제외하고 `프로방스에서는 지역 로제 와인도 대표적인 식문화 요소다. 운전하는 날에는 마시지 않고 저녁 식사 때 선택한다.`로 분리.
- **시장 정보**: 구체적인 08:00–13:00 운영시간을 제거하고 시장의 성격과 역할 수준으로만 Coustellet, Gordes 2곳 링크와 함께 수록.
- **농가 식사**: generic한 원칙 1단락으로 정돈.

---

## 14. Stay & Local Life Cleanup

- **농가와 생활권**: 농가 숙소를 거점으로 한 렌터카 생활, 일요 시장 식재료 확보, 숙소 내 테라스 식사 및 야간 운전 자제 원칙으로 3개 문단 압축.

---

## 15. Transport Cleanup

- **Luberon에서 이동하기**:
  - `### 이동은 렌터카`: 마을 간 이동 필수성
  - `### 마을에서는 외곽에 주차하고 걷기`: 골목 진입 금지 및 외곽 주차 원칙
  - `### 농가로 돌아오는 시간`: 일몰 전 귀환 원칙
  - `### Avignon으로 출발하는 날`: 체크아웃 후 직행 원칙

---

## 16. Lodging Planning Residue Archive

- 모든 숙소 권역 비교표, 숙소 채점표, 수영장 평가 제외 메모, 과거 4박 변경 이력 등은 [`source/ARCHIVE/20_Regional_Chapters/08_Luberon_Planning_Residue_v1.0.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-session-3/source/ARCHIVE/20_Regional_Chapters/08_Luberon_Planning_Residue_v1.0.md)에 분리 보존 완료.

---

## 17. Manuscript Residue Before / After

| 검사 항목 | Before | After | 변화 |
|---|---:|---:|---:|
| `manuscript_residue_check.py` luberon 흔적 토큰 | 34건 | **0건** | -34 (완전 박멸) |
| 원고 번호 및 내부 기획 헤딩 | 12건 | **0건** | -12 |
| 평가 별점 및 점수 표기 | 8건 | **0건** | -8 |

---

## 18. Quantitative Before / After

| 지표 | Before (main) | After (LB01) | Final (LB01F Cleanup) | 총 변화 |
|---|---:|---:|---:|---:|
| **원고 줄 수 (Chapter lines)** | 1,161 | 382 | **364** | -797 (-68.6%) |
| **보이는 글자 수 (Visible chars, 공백 포함)** | ~18,500 | 7,075 | **7,010** | -11,490 (-62.1%) |
| **순수 글자 수 (Visible chars, 공백 제외)** | ~14,200 | 5,447 | **5,396** | -8,804 (-62.0%) |
| **표 개수 (Tables)** | 17 | 1 | **1** | -16 (-94.1%) |
| **장소 카드 수 (Attraction cards)** | 11 | 11 | **9** | -2 (미포함 후보 카드 제거) |
| **일정 표현 수 (Schedule representations)** | 4 | 1 | **1** | -3 (단일 정본) |
| **원고 흔적 토큰 (Residue tokens)** | 34 | 0 | **0** | -34 (완전 박멸) |
| **모바일 390px 스크롤 높이 (추정)** | ~55 screens | ~18 screens | **~17 screens** | -69% 압축 |

---

## 19. Desktop / Mobile Visual QA

- **Desktop (1440px / 1024px)**:
  - 히어로 섹션 및 4개 날짜 칩 정상 렌더.
  - 일정 2열 표가 깔끔하게 렌더되며 하위 링크 정상 동작.
  - 볼거리 그리드(필수/우선추천/선택/대체) 카드 정렬 정상.
  - 숙소/생활권/교통 탭 내비게이션 점프 정상 동작.
- **Mobile (390px / 360px)**:
  - 첫 2 스크린 안에 뤼베롱 농가 체류 성격과 날짜 칩이 한눈에 파악됨.
  - 가로 오버플로 0건 (Viewport check PASS).
  - 복잡한 숙소 비교표 및 채점표 제거로 스크롤 압박 대폭 완화.

---

## 20. Automated QA Results

| 검사 항목 | 명령어 | 결과 | 비고 |
|---|---|---|---|
| 사이트 전체 빌드 | `python3 build/site.py` | **PASS** | 372쪽 생성, 색인 191건 |
| 단위 및 통합 테스트 | `pytest tests/` | **PASS** | 30 passed |
| 원고 흔적 가드 | `python3 build/manuscript_residue_check.py` | **PASS** | aix 0, barcelona 0, girona 0, luberon 0 |
| 지역 구조 검사 | `python3 build/region_structure_check.py` | **PASS** | 분류·섹션·방문일·링크 0 오류 |
| 사진 연결 검사 | `python3 build/media_lookup_check.py` | **PASS** | 미매핑 0, 누락 0 |
| 표 손실 검사 | `python3 build/table_loss_check.py` | **PASS** | 조용한 열 손실 0 |
| UX & 디자인 토큰 검사 | `python3 build/ux_check.py` | **PASS** | 명암비, 하단탭, URL 0 결함 |
| PWA 오프라인 검사 | `python3 build/pwa_check.py` | **PASS** | 871개 파일 전체 캐시 |
| 다중 뷰포트 검사 | `python3 build/viewport_check.py` | **PASS** | 6개 해상도 가로 오버플로 0 |
| 사실 토큰 가드 | `build/fact_guard.py` (via site.py) | **PASS** | 45개 확정 토큰 생존 확인 |
| 상용 편집 심화 가드 | `build/content_guard.py` (via site.py) | **PASS** | rc-region-v1 스키마 준수 |

---

## 21. Regression Result

- 통폐합된 4개 지역(Barcelona, Girona, Aix, Luberon) 및 잔여 4개 지역(Nice, Avignon, Lyon, Paris) 대상 전수 검사 결과:
  - 의도하지 않은 시각적 변화 = 0
  - 깨진 내부 링크 = 0
  - 통폐합 완료 지역 4곳 모두 `manuscript_residue_check` 흔적 0 달성.

---

## 22. Scope 밖 Factual Issues (기록용)

1. **Domaine des Peyre 현장 체크인 및 진입로 확인**:
   - 농가 숙소가 candidate 상태이므로 최종 예약 확정 후 정확한 진입로(Chemin des Peyres) 및 야간 대문 출입 코드 사전 확인 필요.
2. **Lourmarin Salon du Carnet de Voyage 행사 시간**:
   - 2026-09-12~13 행사 일정은 확인되었으나 당일 정확한 개장시간 및 입장료는 현장 확인 필요.

---

## 23. Git Branch / Commits / PR / Changed Files

- **작업 브랜치**: `fix/luberon-region-editorial-consolidation`
- **변경 파일**:
  1. `source/CURRENT/20_Regional_Chapters/08_Luberon_Farmhouse_v2.0.md` (수정 — 카노니컬 챕터 재편집)
  2. `source/CURRENT/20_Regions/luberon.md` (자동 재생성 — 승격 지역 파일)
  3. `source/ARCHIVE/20_Regional_Chapters/08_Luberon_Planning_Residue_v1.0.md` (신규 — 기획 잔재 아카이브)
  4. `data/region-consolidation.json` (수정 — luberon consolidation 등록 및 레이어 제목 지정)
  5. `data/region-essentials.json` (수정 — sourceRefs 아카이브 참조 추가)
  6. `source/ASSETS/91_Place_Registry_v1.0.md` (수정 — Luberon 선택/대체 등급 정규화)
  7. `source/CURRENT/30_Places/abbaye-de-senanque.md` (수정 — frontmatter grade/priority 정규화)
  8. `source/CURRENT/30_Places/menerbes.md` (수정 — frontmatter grade/priority 정규화)
  9. `source/CURRENT/30_Places/oppede-le-vieux.md` (수정 — frontmatter grade/priority 정규화)
  10. `source/CURRENT/30_Places/l-isle-sur-la-sorgue.md` (수정 — frontmatter grade/priority 정규화)
  11. `LB01_LUBERON_RECONSOLIDATION_QA.md` (신규 — 종합 QA 보고서)

---

## 24. STOP

- QA 완료 후 본 지시서 및 Git Integration Rule에 따라 **STOP**합니다.
- Avignon 등 다음 지역 작업은 시작하지 않습니다.
- main 브랜치에 merge/deploy하지 않으며, 외부 Editorial Review 승인을 요청합니다.
