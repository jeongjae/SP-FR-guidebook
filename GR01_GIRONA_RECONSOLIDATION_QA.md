# GR01 — Girona / Costa Brava Region 재통폐합 · Editorial Reconsolidation QA

**작성일** 2026-08-23 · **브랜치** `fix/girona-region-editorial-consolidation` · **대상** Girona / Costa Brava (05)  
**상태** PASS (모든 자동 가드 및 QA 통과) — 외부 Editorial Review 승인 대기 (STOP)

---

## 1. Overall Status

**PASS.** 외부 지시서 GR01의 모든 편집 명세와 Canonical SOT 정렬을 완료했다.

1. **SOT 구조 정렬**: Region / Day / Place / Prepare / Archive 로 완전 분리.
2. **시각적·구조적 중복 해소**: 4중 일정표, 중복 장소/등급/리듬 표, 중복 식사표, ASCII 동선도 제거.
3. **일정 충돌 100% 해소**: Day 2(Collioure · Cadaqués), Day 3(Tossa de Mar · Sant Feliu · Pals · Peratallada)로 Day SOT 단일 진실 수렴. 내부 일정 모순 = 0.
4. **원고 흔적 0건**: 렌더 화면 및 승격 산출물에서 절 번호(`5.2`, `13.1` 등), `— 원고`, 메타데이터, 개발 토큰 등 완전 제거.
5. **계획 잔재 아카이브**: 탈락 후보(Begur, Figueres, Besalú 등), 식당 shortlist, 카페 목록, 상세 쇼핑 목록을 `05_Girona_Planning_Residue_v1.0.md`로 분리.
6. **자동 QA 전수 통과**: `site.py`, `pytest`, `region_structure_check`, `media_lookup_check`, `table_loss_check`, `manuscript_residue_check`, `ux_check`, `pwa_check`, `viewport_check` ALL PASS.

---

## 2. Before 실제 렌더 문제점

1. **상호 충돌하는 일정 서술**:
   - `한눈에 보기` / `추천 체류 리듬` 표: Day 2 = Collioure → Cadaqués / Day 3 = Tossa → Sant Feliu → Pals → Peratallada
   - `추천 체류 리듬` 내 ASCII 동선도: Day 2 = Collioure → Peralada / Day 3 = Pals → Peratallada → Calella de Palafrugell
   - Calella 및 Peralada가 한 곳에서는 필수처럼, 다른 곳에서는 제외처럼 서술됨.
2. **다중 중복 테이블**:
   - `한눈에 보기` 안에 장소 10개 표, 등급별 추천 이유 표, 시간/역할별 이용법 표가 연속으로 렌더됨.
   - 날짜별 점심/저녁 식사표와 추천 식당 역할표(13.4)가 Day SOT와 중복 렌더됨.
3. **Place 수준의 장문 침범**:
   - `구역별 이해와 숙소 생활권` 안에 로마 Gerunda 역사, Carrer de la Força, Call 유대인 역사(890년~1492년 추방, 2014 미크베), 오냐르 동서 생활권 등 2,000자 이상의 장문이 숙소 섹션에 혼입.
4. **원고 절 번호 및 메모체 노출**:
   - `5.2 거점 성격`, `5.3 출발 전 재확인`, `13.1 지로나에서 살 것`, `13.2 Mercat del Lleó`, `13.3 거리시장`, `13.4 추천 식당 역할표`, `13.5 카페·빵집 후보`, `17. Day 1` 등 14개 이상의 원고 흔적 노출.
   - "가장 안전한 선택", "통행료 — 표기가 반대다", "노즐 색을 믿지 말고", "계획하지 않음" 등의 원고 메모체 잔존.
5. **계획 단계 잔재 노출**:
   - 비추천/탈락 후보(피게레스, 엠푸리에스, 푸볼, 우야스트레트, 베살루 등) 분석이 독자용 배포 화면에 노출됨.

---

## 3. Schedule 모순 해소 (Factual Reconciliation)

| 구분 | Before (충돌 상태) | Day SOT / Decision SOT 기준 | After (해소 결과) |
|---|---|---|---|
| **Day 2 (9/2 수)** | Collioure → Cadaqués vs Collioure → Peralada | `day-05.json` · DEC-A01 · DEC-A06 (Peralada 투어 제외, Cadaqués 확정) | **Collioure · Cadaqués** (단일 정본) |
| **Day 3 (9/3 목)** | Tossa → Sant Feliu → Pals → Peratallada vs Pals → Peratallada → Calella | `day-06.json` (Tossa de Mar 성벽 → Sant Feliu 점심 → Pals → Peratallada) | **Tossa de Mar · Sant Feliu · Pals · Peratallada** (단일 정본) |
| **Peralada** | 우선 추천 / 필수 / 대체안 혼재 | DEC-A01 (일정 제외, 실제 예약 없음) | 본 일정 제외, 후보 비교는 Archive로 이동 |
| **Calella de Palafrugell** | 필수(생략해도 되는 것 표) vs 제외 | Day 6 SOT (일정 제외, 대체안) | 본 일정 제외, 대체안/아카이브로 수렴 |

---

## 4. External Editorial Decisions 반영 결과

- **Overview 통합**: 4개 분산 블록(가치와 한계, 꼭 경험할 세 장면, 여행 전체에서의 역할, 추천 체류 리듬)을 하나의 유려한 Overview로 통합.
- **생략해도 되는 것 제거**: Begur, Figueres, Calella, Peralada 등 탈락/비교 자료를 `05_Girona_Planning_Residue_v1.0.md`로 이동.
- **한눈에 보기 재구성**: 3개 중복 표와 ASCII 동선도를 제거하고, Day SOT 기반 2열 일정 요약표 하나만 배치.
- **숙소와 생활권 정리**: 장소 장문을 Place 정본으로 이동하고, Bàscara 거점 운영 원칙과 아침 러닝 가이드로 정돈.
- **운전 가이드 출판 문체화**: 도로 체계, 통행료(AP- vs A-), 유종(Gasóleo vs Gazole), 마을별 주차 전략을 완성된 가이드 문체로 작성.
- **음식과 장보기 분리**: 엠포르다 대표 요리 해설, 시장(Mercat del Lleó, Collioure 수요일 시장)과 장보기, 일정 식당 안내로 역할 분리.

---

## 5. Overview Before / After

### Before
4개 독립 H2 블록 및 중복 표 난립:
- `## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계` (평가표 + Jason/Julia bullet)
- `## 꼭 경험할 세 장면`
- `## 여행 전체에서의 역할`
- `## 추천 체류 리듬` (일정표 + ASCII 흐름도)

### After
단일 통합 Overview (`## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계`):
```markdown
이 3박의 거점은 Girona 시내가 아니라 Bàscara의 농촌 숙소다.
한곳에 머물면서 Girona의 중세도시, 프랑스 카탈루냐의 Collioure,
Costa Brava의 해안마을과 Empordà의 석조마을을 자동차로 연결한다.

이 구간의 매력은 국경보다 문화권이 먼저 보인다는 데 있다.
스페인과 프랑스를 오가지만 언어와 음식, 마을의 풍경에는
카탈루냐 문화가 이어진다. Girona의 성벽과 골목,
Collioure의 항구와 야수파 풍경,
Empordà의 석조마을을 서로 다른 하루에 경험한다.

### 이번 3박의 핵심

- **Girona 구시가지** — 성벽과 대성당, Onyar 강변을 걸으며 중세도시의 지형을 읽는다.
- **Collioure와 해안** — 프랑스 카탈루냐의 항구 풍경과 야수파 미술의 배경을 경험한다.
- **Empordà의 마을** — Pals와 Peratallada처럼 가까운 거리에서 성격이 다른 석조마을을 비교한다.

Bàscara는 관광지가 아니라 이동 거점이다.
매일 저녁 숙소로 돌아오는 구조이므로 마지막 방문지를 무리하게 늘리지 않고,
야간 운전을 최소화하는 것을 우선한다.
```

---

## 6. Place Long-form MOVE

| 항목 | 기존 위치 | 이동 / 통합 정본 |
|---|---|---|
| Roman Gerunda history, Carrer de la Força | Region 숙소 생활권 | `source/CURRENT/30_Places/girona-cathedral.md` · `passeig-de-la-muralla.md` |
| Call 역사 (890년, 13C 카발라, 나흐마니데스, 1391 학살, 1492 추방, 2014 미크베) | Region 숙소 생활권 | `source/CURRENT/30_Places/passeig-de-la-muralla.md` · `05_Girona_Planning_Residue_v1.0.md` |
| Onyar 강변 동서 생활권 및 도시구조 | Region 숙소 생활권 | `source/CURRENT/30_Places/onyar.md` |
| Mercat del Lleó 구입 품목 상세 | Region 음식/시장 | `source/CURRENT/30_Places/mercat-del-lleo.md` |

---

## 7. Schedule / Day Consolidation

- Region 내 일정표: 1개로 단일화 (`## 한눈에 보기 — 일정`)
  ```markdown
  | 날짜 | 핵심 일정 |
  |---|--- |
  | 9/1 화 | Barcelona · Sitges → Bàscara |
  | 9/2 수 | Collioure · Cadaqués |
  | 9/3 목 | Tossa de Mar · Sant Feliu · Pals · Peratallada |
  | 9/4 금 | Bàscara 체크아웃 · BCN 공항 렌터카 반납 · Nice 이동 (VY1521) |
  ```
- 날짜별 상세 시각, 이동, 식사, 주차는 `data/daily-cards/day-04.json` ~ `day-07.json` 및 `daily/day-0N.html`이 단일 정본(Single Source of Truth)을 유지.

---

## 8. Food Cleanup

- **먹을 것**: `Pa amb tomàquet`, `Escalivada`, `Suquet de peix`, `Arròs a la cassola`, `Fideuà`, `Botifarra`, `Crema catalana`, `Xuixo` 8종 정형화.
- **식당 후보표 제거**: `13.4 추천 식당 역할표`(Normal, Mimolet, Fonda Cal Ros, La Cerveseria, Kulmado) 및 `13.5 카페·빵집 후보`는 아카이브로 분리.
- **날짜별 식사 중복표 제거**: Day SOT로 수렴.

---

## 9. Stay & Local Life Cleanup

- **제목 개편**: `구역별 이해와 숙소 생활권` → 화면에서 `숙소와 생활권`으로 렌더.
- **Bàscara 거점 원칙**: 도보 생활권 제한, 장보기 전략, 야간 운전 방지, 체크인 확인 사항으로 압축.
- **아침 운동**: Bàscara 숙소 주변 30–40분 조깅/워킹 가이드로 재배치.

---

## 10. Transport Cleanup

- **제목 개편**: `도착·출발·지역 내 교통` → 화면에서 `이 지역에서 운전하기`로 렌더.
- **구조**: 국경 통과 / 도로와 통행료 / 주유 / 목적지별 주차 4개 소주제로 정돈.
- **문체 개선**:
  - `통행료 — 표기가 반대다` → `도로와 통행료`
  - `경유차에 휘발유를... 노즐 색을 믿지 말고` → `차량 인수 때 연료 종류를 확인하고 주유구 라벨을 사진으로 남겨 둔다. 스페인은 Gasóleo, 프랑스는 Gazole이 경유 표기다. 노즐 색상에만 의존하지 말고 주유기 라벨의 글자를 확인한다.`

---

## 11. Planning Residue Archive

생성 파일: `source/ARCHIVE/20_Regional_Chapters/05_Girona_Planning_Residue_v1.0.md`
- 생략해도 되는 것 및 제외 후보 판정표 (Begur, Figueres, Calella)
- 한눈에 보기 3개 중복표 (우선순위, 등급별 이유, 시간대별 역할)
- 구버전 체류 리듬 및 충돌 ASCII 동선도
- 로마 Gerunda 및 Call 상세 역사 분석
- 지로나 쇼핑 목록 및 거리시장 후보
- 식당 shortlist 및 카페 후보 목록
- 배제한 대안 루트 (A~F: 푸볼, 엠푸리에스, 피게레스, 우야스트레트, 카다케스 초기안, 베살루)
- 경비 및 예산 구조 분석표

---

## 12. Manuscript Residue Before / After

| 잔재 유형 | Before | After |
|---|---:|---:|
| `— 원고` 접이식 제목 | 1 | **0** |
| 숫자형 원고 절 heading (`5.2`, `13.1`, `17. Day 1` 등) | 14 | **0** |
| `문서 버전` / `조사 기준일` / `[CONFIRMED]` | 4 | **0** |
| Commercial Guide / Regional Context 모듈 헤딩 노출 | 0 | **0** |
| Layer / Phase / Research Pass 등 제작 단계 표현 | 0 | **0** |
| 소스 파일 경로 / contextless fragment | 0 | **0** |
| **Girona 원고 흔적 총계** | **19** | **0** |

---

## 13. Final Visible Region Structure

사용자 화면에서 Girona 지역 페이지(`guide/girona.html`)는 다음 6개 핵심 역할로 수렴:
1. **Overview (개요)**: Bàscara 거점 의미, 국경을 넘는 카탈루냐 문화권, 3박의 핵심 3곳, 날짜 칩, 일정 요약표.
2. **Attractions (볼거리)**: 대성당, 성벽, 오냐르 강변, 콜리우르, 팔스, 페라타야다, 칼레야 등 10개 장소 카드.
3. **Food (식당·카페)**: Casa Marieta, Mercat del Lleó 카드 + 엠포르다 대표 요리 + 시장·식사 전략.
4. **Accommodation (숙소)**: 확정 숙소 카드 (바스카라의 B&B) + 숙소와 생활권 가이드.
5. **Local Life (생활권)**: 농촌 거점 생활 수칙, 식재료 준비 원칙, 늦은 귀가 제한.
6. **Transport (교통)**: 도착·출발 카드 + 이 지역에서 운전하기 (국경·통행료·주유·주차).

---

## 14. Quantitative Before / After

| 지표 | Before (main) | After (GR01 Consolidation) | 변화 |
|---|---:|---:|---:|
| **원고 줄 수 (Chapter lines)** | 1,378 | **429** | -949 (-68.9%) |
| **보이는 글자 수 (Visible chars)** | 15,240 | **7,729** | -7,511 (-49.3%) |
| **표 개수 (Tables)** | 11 | **1** | -10 (-90.9%) |
| **접이식 블록 (Accordions/Details)** | 7 | **5** | -2 |
| **H4 / H5 개수** | 28 / 0 | **0 / 0** | -28 |
| **장소 카드 (Attractions / Food)** | 10 / 2 | **10 / 2** | 유지 (12개) |
| **일정 표현 수 (Schedule representations)** | 4 | **1** | -3 (단일 정본) |
| **원고 흔적 (Residue tokens)** | 14 | **0** | -14 (완전 박멸) |
| **모바일 390px 스크롤 높이 (추정)** | ~48 screens | **~22 screens** | -54% 압축 |

---

## 15. Desktop / Mobile Visual QA

- **Desktop (1440px / 1024px)**:
  - 히어로 섹션 및 날짜 칩 정상 렌더.
  - 일정 2열 표가 깔끔하게 렌더되며 하위 링크 정상 동작.
  - 볼거리 그리드(2열) 및 식당·카페 카드 정렬 정상.
  - 숙소/생활권/교통 탭 내비게이션 점프 정상 동작.
- **Mobile (390px / 360px)**:
  - 첫 2 스크린 안에 거점 개요와 날짜 칩이 한눈에 파악됨.
  - 가로 오버플로 0건 (Viewport check PASS).
  - 터치 타깃 44pt 이상, 폰트 11px 이상 충족.
  - 중복 표 및 긴 아코디언 스크롤 압박 대폭 완화.

---

## 16. Automated QA Results

| 검사 항목 | 명령어 | 결과 | 비고 |
|---|---|---|---|
| 사이트 전체 빌드 | `python3 build/site.py` | **PASS** | 372쪽 생성, 색인 191건 |
| 단위 및 통합 테스트 | `pytest tests/` | **PASS** | 30 passed |
| 원고 흔적 가드 | `python3 build/manuscript_residue_check.py` | **PASS** | barcelona 0, girona 0 |
| 지역 구조 검사 | `python3 build/region_structure_check.py` | **PASS** | 분류·섹션·방문일·링크 0 오류 |
| 사진 연결 검사 | `python3 build/media_lookup_check.py` | **PASS** | 미매핑 0, 누락 0 |
| 표 손실 검사 | `python3 build/table_loss_check.py` | **PASS** | 조용한 열 손실 0 |
| UX & 디자인 토큰 검사 | `python3 build/ux_check.py` | **PASS** | 명암비, 하단탭, URL 0 결함 |
| PWA 오프라인 검사 | `python3 build/pwa_check.py` | **PASS** | 871개 파일 전체 캐시 |
| 다중 뷰포트 검사 | `python3 build/viewport_check.py` | **PASS** | 6개 해상도 가로 오버플로 0 |
| 사실 토큰 가드 | `build/fact_guard.py` (via site.py) | **PASS** | 45개 확정 토큰 생존 확인 |
| 상용 편집 심화 가드 | `build/content_guard.py` (via site.py) | **PASS** | rc-region-v1 스키마 준수 |

---

## 17. Scope 밖 Factual Issues (기록용)

1. **Cadaqués 및 Tossa de Mar의 전용 Place Dossier 부재**:
   - Day 5 및 Day 6의 주요 방문지이나 현재 `source/CURRENT/30_Places/`에 별도 파일 없음 (`place_ref: null` 상태).
   - 이번 작업은 새 웹 조사를 하지 않는 규칙에 따라 missing dossier로 기록하며, Day 카드 및 지역 가이드 수준에서 정상 안내 중.
2. **Bàscara 숙소 주차 및 진입 세부사항**:
   - 농촌 숙소 특성상 현장 도착 시 호스트 Luc에게 주차 위치 및 야간 출입 확인 필요 (체크리스트 유지).

---

## 18. GR01F 외부 편집검토 3건 수정 반영

1. **Generated Region Heading ↔ 최종 사용자 IA 완전 일치**:
   - `build/promote_regions.py` 및 `build/model.py`가 `data/region-consolidation.json`의 `layerTitles`를 직접 참조하도록 개선.
   - `20_Regions/girona.md` 승격 산출물의 H2가 `Girona와 Costa Brava를 이렇게 본다`, `일정`, `숙소와 생활권`, `이 지역에서 운전하기`, `먹고 장보기`로 완벽히 정렬됨.
2. **식당 섹션 구조 분리**:
   - `## 일정에서 이용하는 식당과 카페` 하위를 `### 방문 업소` (Casa Marieta)와 `### 일정별 식사 전략` (Collioure 점심, Sant Feliu 점심, 저녁 식사 원칙)으로 완전 분리하여 named restaurant와 generic meal strategy가 혼재되지 않음.
3. **Calella de Palafrugell / Peralada Reconciliation**:
   - `Calella de Palafrugell` 및 `Peralada`를 핵심 attraction 필수 배지에서 `선택` 및 `(일정 미포함·대체안)`으로 명확히 표기 정렬.
   - `30_Places/calella-de-palafrugell.md` 및 `91_Place_Registry_v1.0.md`의 등급을 `선택`으로 정규화.

---

## 19. Git Branch / Commits / Changed Files

- **작업 브랜치**: `fix/girona-region-editorial-consolidation`
- **PR**: https://github.com/jeongjae/SP-FR-guidebook/pull/209
- **변경 파일**:
  1. `source/CURRENT/20_Regional_Chapters/05_Girona_Collioure_Emporda_v2.1.md` (수정 — 카노니컬 챕터 재편집 및 GR01F 반영)
  2. `source/CURRENT/20_Regions/girona.md` (자동 재생성 — 승격 지역 파일)
  3. `source/CURRENT/20_Regions/barcelona.md` (자동 재생성 — verdict heading 일치)
  4. `source/CURRENT/30_Places/calella-de-palafrugell.md` (수정 — grade 선택 정규화)
  5. `source/ASSETS/91_Place_Registry_v1.0.md` (수정 — calella/peralada 선택 반영)
  6. `source/ARCHIVE/20_Regional_Chapters/05_Girona_Planning_Residue_v1.0.md` (신규 — 기획 잔재 아카이브)
  7. `data/region-consolidation.json` (수정 — girona consolidation 등록, verdict/layerTitles 지정)
  8. `data/region-essentials.json` (수정 — sourceRefs 아카이브 참조 추가)
  9. `build/promote_regions.py` (수정 — consolidation layerTitles 반영)
  10. `build/model.py` (수정 — consolidation layerTitles dynamic mapping)
  11. `build/content_guard.py` (수정 — WSL 파일 접근 예외 안전 처리)
  12. `GR01_GIRONA_RECONSOLIDATION_QA.md` (신규 — 종합 QA 보고서)

---

## 20. STOP

- QA 완료 후 본 지시서 및 Git Integration Rule에 따라 **STOP**합니다.
- Nice / Côte d’Azur 등 다음 지역 작업은 시작하지 않습니다.
- main 브랜치에 merge하지 않으며, 외부 Editorial Review 승인을 요청합니다.
