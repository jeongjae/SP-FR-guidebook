# AX01 — Aix-en-Provence Region 재통폐합 · Editorial Reconsolidation QA

**작성일** 2026-08-23 · **브랜치** `fix/aix-region-editorial-consolidation` · **대상** Aix-en-Provence (07)  
**상태** PASS (모든 자동 가드 및 QA 통과) — 외부 Editorial Review 승인 대기 (STOP)

---

## 1. Overall Status

**PASS.** 외부 지시서 AX01의 모든 편집 명세와 Canonical SOT 정렬을 완료했다.

1. **SOT 구조 정렬**: Region / Day / Place / Prepare / Archive 로 완전 분리.
2. **시각적·구조적 중복 해소**: 4중 일정표, 중복 장소/등급/리듬 표, 중복 식사표, ASCII 동선도, 숙소 후보 비교표 완전 제거.
3. **일정 모순 100% 해소**: Day 12(Nice 렌터카 인수 → Saint-Paul → Grasse → Aix 체크인), Day 13(Aix 목요 시장 · 구시가지 · Cézanne), Day 14(Cassis 당일치기), Day 15(Marseille TER 당일치기), Day 16(Lourmarin · Coustellet 시장 · Goult · Luberon 이동)으로 Day SOT 단일 진실 수렴.
4. **원고 흔적 0건**: 렌더 화면 및 승격 산출물에서 절 번호(`17. Day 1`, `18. Day 2` 등), `— 원고`, 메타데이터, 평가표 등 완전 제거.
5. **계획 잔재 아카이브**: 숙소 후보지 6곳 비교표, 숙소 평가 가중치표, 예산 설계표, 탈락 후보(Sainte-Victoire 장거리 하이킹, Arles, Saint-Tropez 등), 수영장 후보, 중복 식사표를 `07_Aix_Planning_Residue_v1.0.md`로 분리.
6. **자동 QA 전수 통과**: `site.py`, `pytest`, `region_structure_check`, `media_lookup_check`, `table_loss_check`, `manuscript_residue_check`, `ux_check`, `pwa_check`, `viewport_check` ALL PASS.

---

## 2. Before 실제 렌더 문제점

1. **내부 기획 및 평가 문체 노출**:
   - `Editor’s Verdict` 내 여행 적합도(`★★★★★`), 예산 체감, 일정 강도 평가표.
   - `여행의 역할`, `여행자 기준`, `가장 엑상다운 장면` 등의 편집 기획 어투.
2. **다중 중복 및 ASCII 일정표**:
   - `한눈에 보기` 12개 장소 우선순위 표.
   - `추천 체류 리듬` 내 ASCII 동선 흐름도 및 Day 12~16 점심/저녁 식사표 중복.
   - 본문 Day 번호가 `17. Day 1`, `18. Day 2`, `19. Day 3`, `20. Day 4`, `21. Day 5`로 여행 전체 일차(Day 12~16)와 불일치 및 절 번호 노출.
3. **숙소 확정 후에도 잔존한 후보지 비교표 및 가중치표**:
   - `권역별 성격과 숙소 적합성` 6개 권역 비교표(1순위, 2순위, 조건부, 신중 등).
   - `숙소 조건과 숙박예산` 가중치 평가표(20/20/15/15/10/10/10) 및 €800~1,050 예산 범위.
   - 이미 `Les Toits de Méjanes(Airbnb)`로 확정되었음에도 과거 선정 자료가 화면에 혼입됨.
4. **Place 수준의 장문 침범**:
   - `구역별 이해와 숙소 생활권` 안에 로마 온천(aquae 어원), 무쉬 분수, 쿠르 미라보 성벽 철거 역사(1649–1651), 세잔 3축 분석표(작품/작업실/풍경) 등 2,500자 이상의 장문 혼입.
5. **원고식 상호 참조 및 지시문체**:
   - `아래 '대안 루트'의 오르세 항목을 참조`, `Day 27부터 파리에 15박 한다`, `Day 12 저녁에 야심을 부리지 마라`, `차를 뺄 생각을 하지 마라` 등 원고 지시문체 노출.

---

## 3. External Editorial Decisions 반영 결과

- **Overview 통합**: 4개 분산 블록(가치와 한계, 꼭 경험할 세 장면, 여행 전체에서의 역할, 추천 체류 리듬)을 하나의 완성된 Overview로 통합 (`## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계`).
- **생략해도 되는 것 제거**: Sainte-Victoire 본격 하이킹, Arles, Saint-Tropez 등 제외 후보 분석을 `07_Aix_Planning_Residue_v1.0.md`로 이동.
- **한눈에 보기 재구성**: 12개 장소 중복표, ASCII 동선도, Day 식사표를 제거하고 Day SOT 기반 2열 일정 요약표 하나만 배치.
- **숙소와 생활권 정리**: 과거 후보지 비교표와 가중치표를 전면 Archive하고, 확정 숙소(Les Toits de Méjanes) 사용법 및 아침 러닝 가이드로 정돈.
- **교통 가이드 출판 문체화**: 시내 도보 원칙, Cassis 렌터카, Marseille TER, Luberon 이동, 프랑스 도로/주유 기본 수칙을 완성된 문체로 정리.
- **음식과 장보기 분리**: 프로방스 대표 요리 해설, Place Richelme 시장 장보기, 일정 식당(Pâtisserie Weibel, Chez Gilbert 등) 및 전략으로 역할 분리.

---

## 4. Schedule Reconciliation (일정 동기화)

| 일자 | Day SOT (`daily-cards`) | Nice / Luberon 연계 | After (Aix Region) |
|---|---|---|---|
| **9/9 수 (Day 12)** | Nice-Ville Hertz 렌터카 인수(09:00) → Saint-Paul-de-Vence → Grasse → Aix 체크인(16:45) | Nice NC01 인계점 및 Day 12 SOT와 100% 일치 | Nice-Ville 렌터카 인수 · Saint-Paul-de-Vence · Grasse · Aix 체크인 |
| **9/10 목 (Day 13)** | Place Richelme 목요 대형 시장 → Vieil Aix · 세잔 흔적 → Musée Granet → Atelier de Cézanne → Terrain des Peintres | Day 13 SOT와 100% 일치 | Aix 목요 시장(Place Richelme) · Vieil Aix · Cézanne 아틀리에 · Musée Granet |
| **9/11 금 (Day 14)** | Aix → Cassis 당일치기 (08:30 출발 → Calanques 유람선 투어 → Cassis 점심 → Port-Miou 산책) → Aix 복귀 | Day 14 SOT와 100% 일치 | Cassis · Calanques 당일치기 |
| **9/12 토 (Day 15)** | Aix역 TER → Marseille Saint-Charles → Vieux-Port(토요 어시장) → Le Panier → Mucem/Fort Saint-Jean → Notre-Dame | Day 15 SOT와 100% 일치 | Marseille 당일치기 (TER 이동) |
| **9/13 일 (Day 16)** | Aix 체크아웃(08:00) → Lourmarin → Coustellet 시장 → Goult 점심 → Luberon 농가 체크인 | Luberon LB01 인계점 및 Day 16 SOT와 100% 일치 | Aix 체크아웃 · Lourmarin · Coustellet 시장 · Goult · Luberon 이동 |

---

## 5. Transfer Reconciliation (인접 지역 연계 정합성)

1. **Nice → Aix (Day 12, 9/9 수)**:
   - Nice NC01 및 Day 12 SOT와 동일하게 09:00 Nice-Ville역 Hertz 렌터카 인수 → Saint-Paul-de-Vence → Grasse → A8 → Aix 숙소(Les Toits de Méjanes) 16:45 체크인으로 완벽히 정합.
2. **Aix → Luberon (Day 16, 9/13 일)**:
   - Day 16 SOT 및 Luberon 챕터 인계점과 동일하게 08:00 체크아웃 → Lourmarin → Coustellet 일요 파머스 마켓 → Goult → Luberon 농가 체크인으로 완벽히 정합.

---

## 6. Overview Before / After

### Before
평가표 + 세 장면 + 여행 역할 + 체류 리듬 4중 분산:
- `## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계` (평가표 ★★★★★)
- `## 꼭 경험할 세 장면`
- `## 여행 전체에서의 역할`
- `## 추천 체류 리듬` (ASCII 동선도 + 식사표)

### After
단일 통합 Overview (`## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계`):
```markdown
Aix-en-Provence에서는 프로방스의 시장과 구시가지 생활, 그리고 Cézanne의 흔적을 중심으로 천천히 도시를 본다. Nice까지 이어졌던 해안 중심 일정에서 벗어나 내륙 프로방스의 일상으로 들어가는 첫 거점이기도 하다.

Aix 자체는 대부분 걸어서 보고, 하루는 Cassis의 항구와 Calanques를, 하루는 Marseille의 항구도시 풍경을 별도 일정으로 다녀온다. 도시 안에서는 장소의 수를 늘리기보다 시장에서 장을 보고, Vieil Aix와 Quartier Mazarin을 걷고, Cézanne이 작업했던 공간과 풍경을 연결하는 데 집중한다.

### 이번 체류의 핵심

- **시장과 Vieil Aix** — Place Richelme와 구시가지 골목을 걸으며 관광지보다 생활도시의 리듬을 본다.
- **Cézanne의 Aix** — 작업실과 도시 주변 풍경을 통해 작품보다 먼저 그가 보았던 환경을 이해한다.
- **Cassis와 Marseille** — 작은 지중해 항구와 대도시 항구를 서로 다른 날에 경험한다.

Aix에 머무는 날에는 차를 세워 두고 걸어 다니며, 당일치기 뒤에는 일정의 밀도를 더 높이지 않는다.
```

---

## 7. Place Long-form MOVE

| 항목 | 기존 위치 | 이동 / 통합 정본 |
|---|---|---|
| 로마 온천 역사, aquae 어원, 무쉬 분수 온천수 | Region 숙소 생활권 | `source/CURRENT/30_Places/cours-mirabeau.md` · `rotonde.md` |
| Cours Mirabeau 1651년 성벽 철거사, Vieil Aix vs Mazarin 격자 대비 | Region 숙소 생활권 | `source/CURRENT/30_Places/cours-mirabeau.md` · `vieil-aix.md` |
| 세잔 3축 분석표 (작품 / 작업실 / 풍경) | Region 숙소 생활권 | `source/CURRENT/30_Places/atelier-des-lauves.md` · `07_Aix_Planning_Residue_v1.0.md` |
| Cassis Calanques 유람선 운항/화재 통제 상세 | Region 교통/장소 | `source/CURRENT/30_Places/calanques.md` · `cassis.md` · Day 14 SOT |
| Marseille 구항구·르파니에·Mucem 세부 해설 | Region 장소 | `source/CURRENT/30_Places/mucem.md` · `vieux-port-marseille.md` · `le-panier.md` |

---

## 8. Schedule / Day Consolidation

- Region 내 일정표: 1개로 단일화 (`## 한눈에 보기 — 일정`)
  ```markdown
  | 날짜 | 핵심 일정 |
  |---|---|
  | 9/9 수 | Nice-Ville 렌터카 인수 · Saint-Paul-de-Vence · Grasse · Aix 체크인 |
  | 9/10 목 | Aix 목요 시장(Place Richelme) · Vieil Aix · Cézanne 아틀리에 · Musée Granet |
  | 9/11 금 | Cassis · Calanques 당일치기 |
  | 9/12 토 | Marseille 당일치기 (TER 이동) |
  | 9/13 일 | Aix 체크아웃 · Lourmarin · Coustellet 시장 · Goult · Luberon 이동 |
  ```
- 상세 시간표와 실행 포인트는 `data/daily-cards/day-12.json` ~ `day-16.json`이 단일 진실 유지.

---

## 9. Food Cleanup

- **먹을 것**: `Tapenade`, `Aïoli`, `Ratatouille`, `Daube provençale`, `Soupe au pistou`, `Calissons d'Aix`, `Panisse`, `Rosé 와인` 8종 정형화.
- **식당 섹션 분리**:
  - `### 방문 업소`: `Pâtisserie Weibel (Aix)`, `Chez Gilbert (Cassis)` 실제 방문 업소만 명시.
  - `### 일정별 식사 전략`: Aix 점심, Cassis 점심, Marseille 점심, 저녁 식사 원칙으로 분리.
- **날짜별 식사 중복표 제거**: Day SOT로 수렴.

---

## 10. Stay & Local Life Cleanup

- **제목 개편**: `구역별 이해와 숙소 생활권` → 화면에서 `숙소와 생활권`으로 렌더.
- **확정 숙소 안내**: Les Toits de Méjanes (Airbnb) 거점 운영 원칙 (도보 생활권, 차량 주차 보관, 장보기)으로 압축.
- **아침 운동**: Rotonde–Cours Mirabeau–Parc Jourdan 방향 30–40분 조깅/워킹 가이드로 재배치.
- **후보 비교표/가중치표 제거**: 아카이브로 분리.

---

## 11. Transport Cleanup

- **제목 개편**: `도착·출발·지역 내 교통` → 화면에서 `Aix에서 이동하기`로 렌더.
- **구조**: 시내에서는 걷기 / Cassis는 렌터카 / Marseille는 TER / Luberon으로 출발하는 날 / 프랑스 도로와 운전 기본 5개 소주제로 정돈.
- **명령형 어투 rewrite**: `차를 뺄 생각을 하지 마라` → `시내 일정에는 차를 움직이지 않고 숙소 주차장에 두는 것이 기본이다. 구시가지는 보행자 전용 구역과 일방통행이 많으므로 차량으로 진입하지 않는다.`

---

## 12. Planning Residue Archive

생성 파일: `source/ARCHIVE/20_Regional_Chapters/07_Aix_Planning_Residue_v1.0.md`
- 생략해도 되는 것 및 제외 후보 판정표 (Sainte-Victoire 장거리 하이킹, Arles, Saint-Tropez)
- 한눈에 보기 12개 장소 우선순위 표
- 구버전 체류 리듬 흐름도 및 Day별 식사표
- 구역별 상세 역사·문화 분석 및 세잔 3축 분석표
- 숙소 후보지 6개 권역 비교표
- 숙소 평가 가중치표 및 예산 설계 범위표 (€800~1,050)
- 수영장 및 피트니스 시설 후보 (Piscine Yves Blanc 등)
- 대안 루트 검토 자료 (Jas de Bouffan, Bibémus, Sainte-Victoire, Vasarely)

---

## 13. Optional / Excluded Place Reconciliation

- **Bastide du Jas de Bouffan**: `선택` (`{{grade:optional|선택}}`) — `Editor's Verdict (일정 미포함·대체안)`
- **Carrières de Bibémus**: `선택` (`{{grade:optional|선택}}`) — `Editor's Verdict (일정 미포함·대체안)`
- **Fondation Vasarely**: 우천 대체 옵션으로 아카이브/대체안 분류.

---

## 14. Manuscript Residue Before / After

| 잔재 유형 | Before | After |
|---|---:|---:|
| `— 원고` 접이식 제목 | 2 | **0** |
| 숫자형 원고 절 heading (`17. Day 1`, `18. Day 2` 등) | 16 | **0** |
| 평가표 및 내부 기획 라벨 (`★★★★★`, `프로젝트 취향` 등) | 5 | **0** |
| Commercial Guide / Regional Context 모듈 헤딩 노출 | 0 | **0** |
| 원고식 상호 참조 (`대안 루트 참조`, `파리에 15박` 등) | 4 | **0** |
| 내부 명령형 어투 (`야심을 부리지 마라`, `차를 뺄 생각 마라`) | 4 | **0** |
| **Aix 원고 흔적 총계** | **31** | **0** |

---

## 15. Final Visible Region Structure

사용자 화면에서 Aix 지역 페이지(`guide/aix.html`)는 다음 6개 핵심 역할로 수렴합니다:
1. **Overview (개요)**: 내륙 프로방스 첫 거점의 의미, 3박의 핵심 3곳, 날짜 칩, 일정 요약표.
2. **Attractions (볼거리)**: Cours Mirabeau, Vieil Aix, Place Richelme 시장, Musée Granet, Atelier de Cézanne, Terrain des Peintres, Cassis & Calanques, Marseille 등 장소 카드.
3. **Food (식당·카페)**: Pâtisserie Weibel, Chez Gilbert 카드 + 프로방스 대표 요리 + 시장 장보기 + 일정별 식사 전략.
4. **Accommodation (숙소)**: 확정 숙소 카드 (Les Toits de Méjanes) + 숙소와 생활권 가이드.
5. **Local Life (생활권)**: 생활 수칙 4개, 늦은 귀가 기준.
6. **Transport (교통)**: 도착·출발 카드 + Aix에서 이동하기 (시내 도보·Cassis 렌터카·Marseille TER·Luberon 출발·도로 기본).

---

## 16. Quantitative Before / After

| 지표 | Before (main) | After (AX01) | Final (AX01F Cleanup) | 총 변화 |
|---|---:|---:|---:|---:|
| **원고 줄 수 (Chapter lines)** | 1,078 | 374 | **354** | -724 (-67.2%) |
| **보이는 글자 수 (Visible chars)** | 19,840 | 10,526 | **9,455** | -10,385 (-52.3%) |
| **표 개수 (Tables)** | 18 | 1 | **1** | -17 (-94.4%) |
| **접이식 블록 (Accordions/Details)** | 8 | 5 | **5** | -3 |
| **H4 / H5 개수** | 35 / 0 | 2 / 0 | **2 / 0** | -33 |
| **장소 카드 (Attractions / Food)** | 21 / 2 | 21 / 2 | **21 / 2** | 유지 |
| **일정 표현 수 (Schedule representations)** | 4 | 1 | **1** | -3 (단일 정본) |
| **원고 흔적 (Residue tokens)** | 31 | 0 | **0** | -31 (완전 박멸) |
| **모바일 390px 스크롤 높이 (추정)** | ~52 screens | ~25 screens | **~22 screens** | -58% 압축 |

---

## 17. AX01F 외부 편집검토 4건 보정 반영

1. **Transport 압축**:
   - `Aix에서 이동하기` 하위를 4개 핵심 소주제(시내 도보 / Cassis 렌터카 / Marseille TER / Luberon 출발)로 압축.
   - 구체적인 주차장명, TER/운전 편도 분/km, RTM 60번 버스, 일반 도로 매뉴얼(`프랑스 도로와 운전 기본`)은 Day/Archive로 이전하고 Region 허브 수준으로 간소화.
2. **Food 밀도 축소**:
   - 7종 대표 요리 해설을 1문장 담백한 설명으로 축소하고 홍보형 수식어(소울 푸드, 유서 깊은, 신선한 지중해 해산물 등) 제거.
3. **Day별 식사전략 중복 제거**:
   - `일정별 식사 전략`의 Day 13/14/15별 세부 실행 문장을 제거하고 generic한 `### 식사 원칙` 1문장으로 정돈.
4. **Rosé 와인 분류 분리**:
   - `프로방스에서 먹어볼 것` 목록에서 Rosé 와인을 음식 리스트에서 제외하고, 별도 음주/식문화 안내 문장(`프로방스에서는 지역 로제 와인도 대표적인 식문화 요소다. 운전하는 날에는 마시지 않고 저녁 식사 때 선택한다.`)으로 분리.

---

## 18. Desktop / Mobile Visual QA

- **Desktop (1440px / 1024px)**:
  - 히어로 섹션 및 5개 날짜 칩 정상 렌더.
  - 일정 2열 표가 깔끔하게 렌더되며 하위 링크 정상 동작.
  - 볼거리 그리드 및 식당·카페 카드 정렬 정상.
  - 숙소/생활권/교통 탭 내비게이션 점프 정상 동작.
- **Mobile (390px / 360px)**:
  - 첫 2 스크린 안에 거점 개요와 날짜 칩이 한눈에 파악됨.
  - 가로 오버플로 0건 (Viewport check PASS).
  - 터치 타깃 44pt 이상, 폰트 11px 이상 충족.
  - 복잡한 숙소 비교표 및 가중치표 제거로 스크롤 압박 대폭 완화.

---

## 19. Automated QA Results

| 검사 항목 | 명령어 | 결과 | 비고 |
|---|---|---|---|
| 사이트 전체 빌드 | `python3 build/site.py` | **PASS** | 372쪽 생성, 색인 191건 |
| 단위 및 통합 테스트 | `pytest tests/` | **PASS** | 30 passed |
| 원고 흔적 가드 | `python3 build/manuscript_residue_check.py` | **PASS** | aix 0, barcelona 0, girona 0 |
| 지역 구조 검사 | `python3 build/region_structure_check.py` | **PASS** | 분류·섹션·방문일·링크 0 오류 |
| 사진 연결 검사 | `python3 build/media_lookup_check.py` | **PASS** | 미매핑 0, 누락 0 |
| 표 손실 검사 | `python3 build/table_loss_check.py` | **PASS** | 조용한 열 손실 0 |
| UX & 디자인 토큰 검사 | `python3 build/ux_check.py` | **PASS** | 명암비, 하단탭, URL 0 결함 |
| PWA 오프라인 검사 | `python3 build/pwa_check.py` | **PASS** | 871개 파일 전체 캐시 |
| 다중 뷰포트 검사 | `python3 build/viewport_check.py` | **PASS** | 6개 해상도 가로 오버플로 0 |
| 사실 토큰 가드 | `build/fact_guard.py` (via site.py) | **PASS** | 45개 확정 토큰 생존 확인 |
| 상용 편집 심화 가드 | `build/content_guard.py` (via site.py) | **PASS** | rc-region-v1 스키마 준수 |

---

## 20. Regression Result

- 다른 7개 지역(Barcelona, Girona, Nice, Luberon, Avignon, Lyon, Paris) 대상 전수 검사 결과:
  - 의도하지 않은 시각적 변화 = 0
  - 깨진 내부 링크 = 0
  - 통폐합된 지역(Barcelona, Girona, Aix) 모두 `manuscript_residue_check` 흔적 0 달성.

---

## 21. Scope 밖 Factual Issues (기록용)

1. **Les Toits de Méjanes 현장 주차 확인 필요**:
   - 숙소 예약은 확정되었으나 건물 현장 주차장 사용 가능 여부 및 주차 리모컨 수령은 체크인 시 호스트와 확인 필요 (체크리스트 유지).
2. **2026 Cézanne 120주년 관련 시설 개방**:
   - Atelier des Lauves(사전 예약 필수) 및 Terrain des Peintres는 정상 운영 중이며, Jas de Bouffan 및 Bibémus는 본 일정에서 제외하고 선택 옵션으로 분류.

---

## 22. Git Branch / Commits / PR / Changed Files

- **작업 브랜치**: `fix/aix-region-editorial-consolidation`
- **PR**: https://github.com/jeongjae/SP-FR-guidebook/pull/210
- **변경 파일**:
  1. `source/CURRENT/20_Regional_Chapters/07_Aix_en_Provence_v2.0.md` (수정 — 카노니컬 챕터 재편집 및 AX01F 반영)
  2. `source/CURRENT/20_Regions/aix.md` (자동 재생성 — 승격 지역 파일)
  3. `source/ARCHIVE/20_Regional_Chapters/07_Aix_Planning_Residue_v1.0.md` (신규 — 기획 잔재 아카이브)
  4. `data/region-consolidation.json` (수정 — aix consolidation 등록 및 레이어 제목 지정)
  5. `data/region-essentials.json` (수정 — sourceRefs 아카이브 참조 추가)
  6. `build/render.py` (수정 — WSL DrvFs 파일 복사 안정화)
  7. `AX01_AIX_RECONSOLIDATION_QA.md` (신규 — 종합 QA 보고서)

---

## 23. STOP

- QA 완료 후 본 지시서 및 Git Integration Rule에 따라 **STOP**합니다.
- Luberon 등 다음 지역 작업은 시작하지 않습니다.
- main 브랜치에 merge/deploy하지 않으며, 외부 Editorial Review 승인을 요청합니다.
