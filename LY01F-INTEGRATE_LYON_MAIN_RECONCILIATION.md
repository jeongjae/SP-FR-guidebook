# LY01F-INTEGRATE — Lyon Final Main Reconciliation QA Report

---

## 1. Executive Summary

- **작업 목적**: 최신 `origin/main`(`9743aee4`, Nice NC01/NC01F 반영 완료)의 모든 결정 및 데이터와 Lyon 재편본(`fix/lyon-region-editorial-consolidation`)의 의미 단위 통합 및 전체 QA 전수 검증.
- **작업 브랜치**: `fix/lyon-region-editorial-consolidation`
- **Reconciliation Head SHA**: `b1584d2c` (최신 commit: `b1584d2c`)
- **결과**:
  - `data/region-consolidation.json`의 7개 지역(`barcelona`, `girona`, `aix`, `luberon`, `avignon`, `nice`, `lyon`) 정상 통합.
  - Nice 최신 결정(DEC-A03 `also_check_daily_cards: true`, 9/8 Èze / 9/9 Saint-Paul, Nice-Ville Hertz 인수) 100% 보존.
  - Avignon 렌터카 반납(9/17 저녁 Avignon TGV Hertz) 및 Lyon 도착일 무차량 TGV 이동 100% 보존.
  - Lyon LY01F 최종 정정사항(식당 Day 귀속, Bellecour 우선추천, Monplaisir 아침운동) 100% 보존.
  - 10개 빌드 & QA 검사 전수 PASS (원고 흔적 0, pytest 30 passed, PWA 871 cached).

---

## 2. Latest origin/main SHA 및 반영 내역

- **Base origin/main SHA**: `9743aee4` (Merge pull request #211 from jeongjae/fix/nice-region-editorial-consolidation)
- **통합 커밋**: `b1584d2c`

---

## 3. Conflict 발생 파일 및 해결 내용

| 파일명 | 충돌 내용 | 해결 방법 |
|---|---|---|
| `data/region-consolidation.json` | `consolidated` 배열 및 `layerTitles`, `notes`에 Nice와 Lyon이 각 브랜치에서 추가되어 발생 | `barcelona`, `girona`, `aix`, `luberon`, `avignon`, `nice`, `lyon` 7개 지역을 모두 포함하도록 수동 병합 |

---

## 4. 타 Region 최신 결정 보존 확인

1. **Nice (NC01F-INTEGRATE)**:
   - DEC-A03: `also_check_daily_cards: true`, `9/8 Villefranche·Villa Ephrussi·Èze`, `9/9 Saint-Paul-de-Vence·Grasse·Aix` 정상 보존.
   - Nice-Ville Hertz 렌터카 인수 정상 보존.
   - `06_Nice_Cote_d_Azur_v2.0.md` 및 `nice.md` 상용편집본 보존.
2. **Avignon (AV01F)**:
   - 렌터카 반납일 2026-09-17(목) 저녁 Avignon TGV Hertz (18:30 이전) 확정 보존.
   - 기존 Hertz 예약 변경 필요 상태 정상 보존.
   - Day 23 아침 이동에 차량 반납 절차 없는 TGV 이동 정합.
3. **Luberon (LB01F) / Aix (AX01F) / Girona (GR01F) / Barcelona (RC01F)**:
   - consolidation 및 essentials 항목 100% 보존.

---

## 5. Lyon LY01F 정정사항 보존 확인

| 항목 | 내용 | 상태 |
|---|---|:---:|
| **Café Comptoir Abel** | Day 23 (9/20 일 저녁) | **보존** |
| **Daniel et Denise** | Day 24 (9/21 월 저녁) | **보존** |
| **Halles Paul Bocuse** | Day 25 (9/22 화 점심 & 시장) | **보존** |
| **Chez Mamie Lise** | Day 26 (9/23 수 점심) | **보존** |
| **Bellecour 등급** | `{{grade:priority|우선추천}}` (Day 23 actual stop) | **보존** |
| **Day 25 대표 부숑 stale 표현** | 완전 제거 (0건) | **보존** |
| **아침 운동** | `Monplaisir 숙소 주변에서 가볍게 걷거나 뛰고...` | **보존** |
| **Avignon ➔ Lyon Handoff** | 렌터카 반납 없는 TGV 이동 (Avignon TGV 10:22 ➔ Lyon Part-Dieu 11:28) | **보존** |
| **Lyon ➔ Paris Handoff** | Part-Dieu역 TGV INOUI 6618 탑승 | **보존** |

---

## 6. Final Place Registry 상태

- **Lyon 등록 엔티티**: 10개 (`annecy`, `bellecour`, `croix-rousse`, `fourviere`, `halles-de-lyon-paul-bocuse`, `parc-de-la-tete-d-or`, `vieux-lyon`, `cafe-comptoir-abel`, `daniel-et-denise`, `chez-mamie-lise`)
- **Bellecour 등급**: `우선 추천` (spot, Priority)
- **타 Region Place 손실**: 0건

---

## 7. 전체 QA 결과

| 검사 항목 | 명령어 | 결과 | 비고 |
|---|---|---|---|
| 사이트 전체 빌드 | `python3 build/site.py` | **PASS** | 372쪽 생성, 색인 191건 |
| 단위 및 통합 테스트 | `pytest tests/` | **PASS** | 30 passed |
| 원고 흔적 가드 | `python3 build/manuscript_residue_check.py` | **PASS** | aix 0, avignon 0, barcelona 0, girona 0, luberon 0, lyon 0, nice 0 |
| 지역 구조 검사 | `python3 build/region_structure_check.py` | **PASS** | 분류·섹션·방문일·링크 0 오류 |
| 사진 연결 검사 | `python3 build/media_lookup_check.py` | **PASS** | 미매핑 0, 누락 0 |
| 표 손실 검사 | `python3 build/table_loss_check.py` | **PASS** | 조용한 열 손실 0 |
| UX & 디자인 토큰 검사 | `python3 build/ux_check.py` | **PASS** | 명암비, 하단탭, URL 0 결함 |
| PWA 오프라인 검사 | `python3 build/pwa_check.py` | **PASS** | 871개 파일 전체 캐시 |
| 다중 뷰포트 검사 | `python3 build/viewport_check.py` | **PASS** | 6개 해상도 가로 오버플로 0 |
| 사실 토큰 가드 | `build/fact_guard.py` (via site.py) | **PASS** | 45개 확정 토큰 생존 확인 |
| 조사 종결 검사 | `python3 build/research_closure_check.py` | **PASS** | 0 unclassified |

---

## 8. Pre-existing Main Failures

- **신규 발생 Failure**: **0건** (전체 10개 검사 모두 클린 패스)
- **Pre-existing Failure**: 없음

---

## 9. Changed Files

1. `data/region-consolidation.json` (7개 지역 병합 완료)
2. `data/region-essentials.json` (nice 및 lyon 아카이브 레퍼런스 유지)
3. `source/CURRENT/20_Regional_Chapters/10_Lyon_v2.0.md` (LY01F 정합본)
4. `source/CURRENT/20_Regions/lyon.md` (LY01F 승격본)
5. `source/ASSETS/91_Place_Registry_v1.0.md` (Bellecour 우선추천 등급)
6. `source/ARCHIVE/20_Regional_Chapters/10_Lyon_Planning_Residue_v1.0.md` (Lyon 기획 잔재 아카이브)
7. `LY01_LYON_RECONSOLIDATION_QA.md` (LY01F QA 문서)
8. `LY01F-INTEGRATE_LYON_MAIN_RECONCILIATION.md` (최신 main 통합 보고서)
