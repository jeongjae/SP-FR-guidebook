# Stage A-D — Walk dossier 사실값 감사

**대상:** R1 때 오염 브랜치에서 인수한 Walk dossier 3종
**감사 기준:** 총괄 지시문 §3 Stage A-D — 정차점의 사실값(운영시간·요금·지명·경로)을 main·공식 출처와 대조, 확인 불가 항목은 `{{badge:pending}}` + REVERIFY 등재

---

## 1. 감사 대상과 실물

`git diff main -- source/ASSETS/90_…Compendium…md` 로 추출한 실제 내용은 다음이 전부다.

| Walk | 레지스트리 ID | 컴펜디움 본문 | 사실값 |
|---|---|---|---|
| Barcelona 역사도심 — Barri Gòtic·Rambla 권역 | `barcelona-historic-walk` | 설명 1문장 + 공식정보 URL | **없음** |
| Barcelona Modernisme — Eixample 권역 | `barcelona-modernisme-walk` | 설명 1문장 + 공식정보 URL | **없음** |
| Girona 구시가지 — Call·성벽·대성당 권역 | `girona-old-town-walk` | 설명 1문장 + 공식정보 URL | **없음** |

## 2. 대조 결과

### 2.1 정차점 사실값 — 해당 없음

세 dossier 모두 **정차점 목록·운영시간·요금·소요시간을 담고 있지 않다.** 각 항목은 "무엇을 잇는 도보 경로인지" 한 문장과 공식 관광기구 URL 하나로 끝난다. 따라서 창작된 운영정보가 유입될 표면 자체가 없다.

챕터 본문 쪽에도 이 세 Walk의 정차점 절은 없다 (04·05 챕터의 `핵심 셀프가이드` 절은 main 원문 dossier만 담는다). Nice의 Walk 3종이 챕터 본문에 정차점 5개씩을 가진 것과 다른 상태다.

### 2.2 지명·경로 서술 대조

| 항목 | 서술 | 판정 |
|---|---|---|
| Barri Gòtic·Rambla 권역 | 04 챕터 `Day 3 — 고딕 지구·시장·도서관` 동선과 일치 | 정합 |
| Eixample 모더니즘 | 04 챕터 Sagrada Família·Sant Pau 축과 일치 | 정합 |
| Call·성벽·대성당 | 05 챕터 지로나 대성당·성벽·유대인 지구 dossier와 일치 | 정합 |

### 2.3 공식정보 URL

세 URL 모두 공식 관광기구 도메인(`barcelonaturisme.com`, `girona.cat/turisme`)이며, 빌드의 Phase 9 가드가 walk 타입 dossier에 `공식정보` 필드의 `http` 시작을 요구해 이미 기계 검증된다.

## 3. 함께 확인된 것 — main 헤딩 오기 정정 1건

레지스트리·컴펜디움 diff에서 브랜치가 main을 **정정**한 항목을 발견했다.

```
main:  80:## Girona Cathedral
main:  90:## Girona Cathedral      ← 중복 헤딩
브랜치: 90:## Passeig de la Muralla
```

main 90행의 본문은 "로마·중세 방어선이 산책로로 바뀐 곳으로 도시의 지형을 가장 잘 이해할 수 있다"로, **대성당이 아니라 성벽 산책로 설명**이다. main의 헤딩이 오기였고 브랜치의 `Passeig de la Muralla` 가 옳다. 레지스트리에도 같은 ID(`passeig-de-la-muralla`)로 등록돼 있어 정합한다.

→ **유지한다.** 신규 창작이 아니라 main 오기의 정정이며, 이 정정 덕분에 Phase 9 가드의 "Dossier 중복 헤딩" 검사도 통과한다.

## 4. REVERIFY 등재

정차점 사실값이 없으므로 이번 감사에서 신규 등재할 REVERIFY 항목은 **없다.**

다만 아래를 결정 대기 큐로 이관한다.

| 항목 | 내용 |
|---|---|
| Walk 3종의 콘텐츠 깊이 | 현재는 레지스트리·지도 배선만 있고 실제 셀프가이드(정차점 8–15개)는 없다. Nice 3종과 비대칭이다. 작성하려면 main에 재료가 없어 신규 서술이 되므로, 이동-전용 원칙상 이번 재작업 범위 밖이다. |

## 5. 판정

**PASS** — 오염 브랜치산 신규 콘텐츠이지만 사실값을 담지 않아 창작 위험이 없고, 지명·경로 서술은 챕터 본문과 정합하며, 공식 URL은 빌드 가드가 검증한다.
