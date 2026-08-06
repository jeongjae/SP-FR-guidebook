# 상용 가이드북 개편 — 실행계획 v1.1

- **원본:** Desktop `SP-FR_Commercial_Guidebook_Redesign_Work_Order.md` (v1.0)
- **개정일:** 2026-08-06 · 기준 커밋 `c274d42`
- **개정 사유:** 원 지시서는 부분개선이 "모두 끝난 뒤" 착수를 전제했으나, 실제로는
  세 개의 부분개선 스트림이 병행 진행 중이고 그중 하나(Google Maps 이행)가
  원 지시서 §7·Phase E 를 이미 다른 설계로 구현하고 있다. 충돌을 피하려면
  Phase 정의와 착수 게이트를 재설정해야 한다.

---

## 1. 병행 스트림 현황과 착수 게이트

| 스트림 | 진행 (2026-08-06) | 남은 것 | 막는 Phase |
|---|---|---|---|
| ① 액션맵 카드 (43장) | Day 1–15 머지 (PR #52·54·58) | Day 16–43, 약 6배치 | D (데일리) |
| ② 사진 콘텐츠 | Barcelona 파일럿 + Girona·Nice 40장 (PR #53·60) | Batch 2 프로방스~리옹 · Batch 3 파리 + PWA 번들·LFS 결정 | H (시각·성능) |
| ③ Google Maps 이행 | Phase 0–4 완료: 장소 72곳 JSON 정규화 · 공통 컴포넌트 · 지역지도 8/8 전환 (PR #49·59·62) | 일자별 지도 43개 · Place ID 71곳 · Leaflet 정리 | — (E를 대체) |

**게이트 원칙:** 각 리디자인 Phase 는 자신을 막는 스트림이 끝난 뒤에만 코드를
만진다. 문서·설계·데이터 정리는 스트림과 파일이 겹치지 않는 한 병행한다.

## 2. Phase 재정의 (v1.0 → v1.1)

| v1.0 | v1.1 | 변경 |
|---|---|---|
| Phase A 기준선·설계 | **A. 설계 (지금 진행)** | 유지. 산출물에 베이스라인 추기 포함. 코드 무변경 |
| — | **A'. 구판 문서 정리 (지금 진행 가능)** | 신설. 베이스라인 §7의 12건 — 스트림과 파일 안 겹침 |
| Phase B 파일럿 | **B. 파일럿** | 착수를 게이트 뒤로. 대상 재선정: 지역 1(스트림이 이미 완성한 Barcelona 권장) · 데일리 3일 · dossier 5 |
| Phase C 홈·내비 | **C. 홈·전역 내비** | 유지. 단 하단탭 개편은 결정 로그 D-03 (사용자 결정 대기) |
| Phase D 데일리 | **D. 데일리 템플릿 통합** | 축소: 카드 배치가 만든 43장 위에 템플릿 통일만. 카드 재생성 금지 |
| Phase E 지도 | **삭제 — ③이 대체** | 원 지시서 §7의 `DailyMapData` 확장안 폐기. 지도 정본은 `source/ASSETS/maps/*.json` (place-registry 72곳 · daily-routes · region-groups) |
| Phase F 지역·장소 편집 | **E. 지역·장소 편집** | 유지 (번호만 당김) |
| Phase G 검색·준비 | **F. 검색·준비** | 유지 |
| Phase H QA | **G. 통합 QA** | 유지. ② 의 PWA 번들·LFS 결정 결과를 전제로 수행 |

## 3. 원 지시서에서 폐기·대체된 조항

| 조항 | 처분 | 근거 |
|---|---|---|
| §7.3 `DailyMapData` 확장 | 폐기 | ③ 이 placeId 참조 모델로 대체 구현 (docs/google-maps-migration/data-model.md) |
| §14 `data/` YAML 트리 | 폐기 | 정본은 기존 구조 유지: itinerary.json · 91_Place_Registry(MD) · maps/*.json · 트래커 XLSX. §14 자체 단서("기존 구조 안에서 책임 분리") 적용 |
| §18.1 `feat/commercial-guidebook-redesign` 브랜치 | 대체 | 현행 관례 `jeongjae/*` 사용. 이 브랜치가 그것 |
| §2.3 문서 4종 명명 | 유지하되 URL_MAP 은 실측 생성본으로 대체 | PHASE0_URL_REDIRECT_MAP_v0.1.csv 는 미구현 설계안이라 승계하지 않음 |
| §5.1 하단탭 `오늘·일정·지도·가이드·준비` | **보류 — 사용자 결정** | 현행 5탭은 가드로 고정. 결정 로그 D-03 |

## 4. 불변 조건 (모든 Phase 공통)

1. 완료 기준에 항상 포함: `build.py` 전 가드 + `hig_check.py` + `pwa_check.py` 통과.
2. 명암비 본문 7:1 · 보조 4.5:1 (HIG 최소치 아님 — 프로젝트 기준).
3. URL 변경 시 `docs/COMMERCIAL_REDESIGN_URL_MAP_v1.0.csv` 에 redirect 행 추가. 삭제 금지.
4. 미확정 예약을 확정처럼 표시하지 않는다 (실예약 잠금률 0% 상태 — 베이스라인 §6).
5. 스트림 ①②③ 이 만든 산출물(카드·사진·지도)을 재생성하지 않는다.
6. 설계 판단은 `docs/COMMERCIAL_REDESIGN_DECISION_LOG_v1.0.md` 에 기록한다.

## 5. Phase A 산출물 (이번 작업)

```text
docs/COMMERCIAL_REDESIGN_PLAN_v1.1.md                    ← 이 문서
docs/COMMERCIAL_REDESIGN_BASELINE_v1.0.md                ← 추기(v1.0.1) 반영
docs/COMMERCIAL_REDESIGN_DECISION_LOG_v1.0.md
docs/COMMERCIAL_REDESIGN_INFORMATION_ARCHITECTURE_v1.0.md
docs/COMMERCIAL_REDESIGN_DATA_MODEL_v1.0.md
docs/COMMERCIAL_REDESIGN_DESIGN_TOKENS_v1.0.md
docs/COMMERCIAL_REDESIGN_URL_MAP_v1.0.csv                ← 실측 생성 (keep 266 · redirect 62)
```

## 6. 순서와 검수 지점

```text
A 설계 문서 (지금) ──┐
A' 구판 문서 정리     ├─ 사용자 검수 ①: 설계 승인 + D-01~D-05 결정
                      │
[게이트: 스트림 ③ 완료] → B 파일럿 → 사용자 검수 ② → C 홈·내비
[게이트: 스트림 ① 완료] → D 데일리 통합
                      → E 지역·장소 → F 검색·준비
[게이트: 스트림 ② 완료] → G 통합 QA → 최종 검수
```

우선순위는 원 지시서 §17 유지 (P0: 일정 정합·데일리·지도·예약 반영·오프라인·개인정보).
P0 중 "실제 숙소·교통·예약 반영"은 사이트 작업이 아니라 **예약 행위 자체**가
병목이다 — 베이스라인 §6 (잠금률 0%, 여행 87일 전).
