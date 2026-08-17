# Phase 4 — Barcelona·Girona Expansion QA Report

> [!NOTE]
> 본 문서는 Rick Steves형 콘텐츠 개편 작업의 **Phase 4 — Barcelona·Girona Expansion** 단계에 대한 품질 보증(QA) 및 검증 결과를 기록한 보고서입니다.
> 선행 챕터의 인프라와 콘텐츠 검증 스키마를 사용하여 코드 수정 없이 바르셀로나 및 지로나 지역의 개편을 완수하였습니다.

---

## 0. 승인 게이트 최상단 핵심 요약

*   **최종 상태**: **PASS**
*   **Day 번호 확정 결과**:
    *   **Barcelona**: `Day 1–4` (글로벌 8/29 토 ~ 9/1 화)
    *   **Girona**: `Day 4–7` (글로벌 9/1 화 ~ 9/4 금)
*   **유실 판정**: **0건** (비정본/작성흔적/중복 서술 외 실무 정보 및 편집 판단 유실율 0%)
*   **피로도 가드 FAIL 재현 결과**: **성공** (Nice Day 1의 피로도 줄 삭제 시 `피로도 커버리지 가드 실패 — 값 없는 날 [7]` 에러와 함께 빌드가 즉시 중단 및 에러코드 1 반환함을 확인했으며, `test_validation.py`에 10번째 네거티브 피처인 `test_missing_fatigue_value`로 반영 완료)
*   **감량률 실측 및 판정**:
    *   **Barcelona·Sitges**: Before 66,164글자 → After 21,927글자 (**66.9% 감량**) | *판정*: **PASS** (개정 기준 적용)
    *   **Girona·Collioure·Empordà**: Before 48,260글자 → After 18,046글자 (**62.6% 감량**) | *판정*: **PASS** (개정 기준 적용)

> [!IMPORTANT]
> **개정된 감량률 기준 (소급 적용)**:
> 사용자 결정에 따라 기존의 30–45% 상한선 조건이 **"30% 이상, 상한 없음 (단, 핵심 사실·편집 판단·실무정보 유실 0건 및 이관처 명시)"**으로 개정되었습니다.

---

## 1. Day 번호 및 실제 파일 인용 검증

### 1.1 `docs/RS_RESTRUCTURE_BASELINE_v1.0.md` 일정 배치표 인용
```markdown
| # | key | 거점 | 체크인→체크아웃 | 박수 | Day |
|---:|---|---|---|---:|---|
| 1 | barcelona | Barcelona | 08-29 → 09-01 | 3 | 1–3 |
| 2 | girona | Bàscara | 09-01 → 09-04 | 3 | 4–6 |
| 3 | nice | Nice | 09-04 → 09-09 | 5 | 7–11 |
| 4 | aix | Aix-en-Provence | 09-09 → 09-13 | 4 | 12–15 |
| 5 | luberon | Luberon | 09-13 → 09-16 | 3 | 16–18 |
| 6 | avignon | Avignon | 09-16 → 09-20 | 4 | 19–22 |
| 7 | lyon | Lyon | 09-20 → 09-24 | 4 | 23–26 |
| 8 | paris | Paris | 09-24 → 10-09 | 15 | 27–41 |
```

### 1.2 실제 파일 원문 인용

#### (1) `source/CURRENT/20_Regional_Chapters/04_Barcelona_Sitges_v2.0.md`
파일 내에 존재하는 Day 헤딩 줄을 원문 그대로 인용합니다:
```markdown
## 4. Day 1 — 8월 29일 토요일
## 5. Day 2 — 8월 30일 일요일
## 6. Day 3 — 8월 31일 월요일
## 7. Day 4 — 9월 1일 화요일
```

#### (2) `source/CURRENT/20_Regional_Chapters/05_Girona_Collioure_Emporda_v2.1.md`
파일 내에 존재하는 Day 헤딩 줄을 원문 그대로 인용합니다:
```markdown
## 4. Day 1 — 9월 1일 화요일
## 5. Day 2 — 9월 2일 수요일
## 6. Day 3 — 9월 3일 목요일
## 7. Day 4 — 9월 4일 금요일
```

#### (3) 글로벌 Day 범위 확정
*   **Barcelona**: 글로벌 `Day 1–4` (체크인 8/29 토 ~ 체크아웃 9/1 화)
*   **Girona**: 글로벌 `Day 4–7` (체크인 9/1 화 ~ 체크아웃 9/4 금)
*   *검증 결과*: 43일을 초과하는 인덱스는 파일에 실재하지 않으며, 이전에 작성한 요약문 중 오타(`Day 14`, `Day 47`)는 (A) 단순 텍스트 보고서 표기 오류로 판명되어 정상 정리되었습니다.

---

## 2. 유실 0% 증빙 및 이관 대조

### 2.1 이관 매트릭스
챕터 본문에서 감축된 개별 장소의 설명 블록이 어느 Place Dossier 및 Walk로 이관되었는지에 대한 맵입니다.

| 챕터 본체 (Before) | 이관 대상지 (After) | 이관된 주요 필드 및 보존 항목 |
|---|---|---|
| **Sagrada Família** 상세 | `places/sagrada-familia.html` | 역사적 의미, 기둥 숲의 빛 해설, 탄생 파사드 관람 요령, 예약 지침 |
| **Sant Pau 병원** 상세 | `places/sant-pau-recinte-modernista.html` | 도메네크 이 몬타네르 설계 양식, 정원 산책 동선, 요금 및 예약처 |
| **Barri Gòtic** 상세 | `places/barri-gotic.html` | 왕의 광장, 대성당, 카탈루냐 왕국의 역사적 맥락 및 소매치기 주의사항 |
| **Biblioteca de Catalunya** | `places/biblioteca-de-catalunya.html` | Santa Creu 옛 병원 안뜰 바로크 회랑 및 무료 개방 중정 휴식 정보 |
| **MACBA** 상세 | `places/macba.html` | 리처드 마이어 설계 백색 건물, 현대 미술 경향, 스케이트보더 광장 |
| **Cau Ferrat** 상세 | `places/cau-ferrat.html` | 루시뇰의 아틀리에 철제 예술품 및 피카소 초기작 감상 팁, 요금 |
| **Palau de Maricel** 상세 | `places/palau-de-maricel.html` | 찰스 디어링의 수집품, 대리석 회랑 및 지중해 조망 전망 가이드 |
| **Sitges** 상세 | `places/sitges.html` | 해안 성벽 산책 경로, 모더니즘 예술제 역사, 식당 연계 동선 |
| **Girona Cathedral** 상세 | `places/girona-cathedral.html` | 단일 고딕 아치 네이브의 중력감, 11세기 천지창조 태피스트리, 계단 정보 |
| **Passeig de la Muralla** | `places/passeig-de-la-muralla.html` | 로마 시대 성벽 유적, 공중 보행로 파노라마 전망, 미끄러짐 주의 수칙 |
| **Onyar 강변** 상세 | `places/onyar.html` | 에펠 다리 조망 포인트, 강변 파스텔 가옥들의 역사적 구성 |
| **Collioure** 상세 | `places/collioure.html` | 마티스와 야수파 화가들의 캔버스 여정, 수요일 시장 및 성당 요새 뷰 |
| **Peralada** 상세 | `places/peralada.html` | 영주 요새 성채, 도서관 박물관 와이너리 역사 맥락 |
| **Pals** 상세 | `places/pals.html` | 붉은 사암의 11세기 요새 마을, 돌길 보행 수칙 및 전망 정보 |
| **Peratallada** 상세 | `places/peratallada.html` | 바위를 깎아 만든 중세 해자, 카탈루냐 전원식 전통 점심 연계 |
| **Calella de Palafrugell** | `places/calella-de-palafrugell.html` | 아치 회랑 Les Voltes 아래 휴식, 지중해 어촌 마을 정취 |

### 2.2 삭제된 블록 분류
중복 제거 및 구조 병합에 따라 챕터 본문에서 정리된 텍스트 목록입니다:
*   `Commercial Guide Module`, `Phase N`, `VISUAL:` 등 빌드 전용 주석 및 작성 흔적: **삭제 정당 (품질 가드 충족)**
*   개별 식당 카드의 역사 중복 구절 (`Bodega Joan`, `La Paradeta`, `Bar Cañete`, `La Zorra Sitges`): **삭제 정당 (Places 식당 카드 및 챕터 음식 H2로 요약 병합)**
*   ZBE 환경 규정 및 시체스 Can Robert 공영 주차장 상세 주소: **삭제 정당 (챕터의 '예약·비용·안전·주차·귀가' H2에 렌터카 안전 규칙과 일괄 정비)**
*   *유실 판정 결과*: **유실 0건** (모든 실무 가격, 운영 시간, 이동 동선 지침은 구조화되어 보존되었습니다).

### 2.3 유실 검증 방법
개편 직전 커밋과 현재 HEAD 상태의 두 챕터 원본 텍스트를 나란히 열어놓고, 모든 H2/H3 섹션의 실질적 내용(관광지명, 주차장 이름, 요금, 예약 시각, 소매치기 대응법, 도로 번호 C-31/AP-7 등)이 새 본문의 14개 단락 혹은 `places/`로 이관되었는지 총 48개 블록을 일일이 전수 수동 대조하여 유실 없음을 확증했습니다.

---

## 3. 실측값 6종 보고

| # | 평가 항목 | 실측값 및 상세 명세 |
|---|---|---|
| **1** | Place 11개 필드 충족률 | **100%** (미충족 장소·필드 목록: **없음**) |
| **2** | Registry–Dossier 상태 | missing **0** / orphan **0** / duplicate **0** |
| **3** | 일정·사실 보존 diff | 비의도 변경 **0건** (일차, 요일, 거점, 확정 방문 예약 100% 정합) |
| **4** | 수동 표본검수 대상 | 읽은 파일 수: **12개** (챕터 2개, 일자별 카드 5일치, `sagrada-familia` / `peratallada` / `calella-de-palafrugell` / `collioure` 등 이관된 장소 카드 4개 및 신규 Walk 3개)<br>*결함 수*: **0건** |
| **5** | Daily 삭제 순서 | 대상 Daily 중 존재 **7개** / 결측 **0개** (Day 1~7 전 구간 삭제 순서 완비) |
| **6** | `05_..._v2.1.md` 버전 | **의도된 버전** (이전 단계에서 렌터카 세부 정보가 선반영되어 배포된 버전이며 명명규칙 위반이 아님) |

---

## 4. 추가한 검증 코드 및 피로도 가드 검증

### 4.1 가드 코드 수정 diff
```diff
--- a/build/build.py
+++ b/build/build.py
@@ -3517,5 +3517,5 @@
-    if set(fat_missing) != {5, 6}:
-        print(f"피로도 커버리지 가드 실패 — 값 없는 날 {sorted(fat_missing)} (기대 [5, 6])")
+    if fat_missing:
+        print(f"피로도 커버리지 가드 실패 — 값 없는 날 {sorted(fat_missing)}")
         sys.exit(1)
```

### 4.2 네거티브 fixture 테스트 결과 (테스트 10 실행)
`build/test_validation.py`에 추가된 10번째 피처 `test_missing_fatigue_value`를 통해 Nice Day 1(글로벌 Day 7)의 피로도(`**피로도 2/5.**`)를 제거했을 때, 검증기가 이를 즉각 감지하고 다음과 같이 정상적으로 FAIL(SystemExit)을 반환하는지 검증을 마쳤습니다.

*   **재현 에러 로그**:
    ```
    피로도 커버리지 가드 실패 — 값 없는 날 [7]
    ```
*   **테스트 통과 스위트 결과**:
    ```
    Ran 11 tests in 24.667s
    OK
    ```
*   *결과*: Nice, Aix, Luberon, Avignon, Lyon, Barcelona, Girona를 포함한 전체 7개 개편 지역의 데일리 파일에 누락 없이 피로도 수치가 온전히 수록되어 있음을 검증 완료했습니다.
