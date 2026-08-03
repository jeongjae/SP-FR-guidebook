# 콘텐츠 통합 변경기록

감사 근거: `docs/content-deduplication-audit.md` · 조치계획: `data/content-refactor-plan.csv`

## 2026-08-03 — 원고 사본 통합 (refactor/content-deduplication)

### Archived (source/ARCHIVE/ 로 이동 — 삭제 아님, 빌드 미사용 확인분만)

- `20_Regional_Chapters/` 구판 8개: Barcelona v1.6 · Girona v1.6 · Nice v1.8 ·
  Aix v1.7 · Luberon v1.8 · Avignon v1.6 · Lyon v1.7 · Paris v1.7
- `30_Reader_Edition/` 전체 9개 (Reader 8 + Master Index)
- `10_Core/42_TP_Europe_Travel_Guidebook_Master_v1.4.md` (8,888줄 통합 사본)
- `00_Governance/37_Source_of_Truth_and_Supersession_Matrix_v1.1.md` (사어 색인)
- `00_Governance/00_Current_Source_of_Truth_Index_v1.9.md` (v2.0으로 대체)

**효과**: source/ 원고 48,600줄 → 22,900줄 (-53%). 지역당 사본 3~4벌 → 1벌.
사이트 산출물 변화 없음 (전부 빌드 미사용 파일 — 가드 15종 통과로 증명).

### Merged — Lourmarin 장소 페이지

- 레지스트리 2행(`lourmarin` aix 경유 · `lourmarin-2` luberon 정본) → 1행
- Canonical: `places/lourmarin.html` (카뮈 도시어 포함 상세본)
- Redirect: `places/lourmarin-2.html` → `lourmarin.html`
- Preserved: Google Maps 링크(이름 대조 폴백으로 유지) · Aix 실행지도
  팝업의 장소 카드 링크(전환일 지도 핀 대조 확장) · Day 16 데일리 연결 ·
  두 챕터의 등급 헤딩과 본문
- 명명규칙 위반(`-2` 번호 슬러그) 해소. 장소 spot 82 → 81

### Updated

- `00_Current_Source_of_Truth_Index_v2.0.md` 신설 — v2 챕터를 정본으로 선언,
  부재 파일 참조 제거, "버전 파일을 늘리지 않는다" 규칙 명문화
- `source/README_START_HERE.md` — 정본 구성으로 갱신
- `91_Place_Registry` 꼬리말 집계 실측 일치화 (spot 83 표기 → 81)

### 하지 않은 것 (근거와 함께 기록)

- **v2 챕터 내부의 신구 섹션 병존 편집** — 헤딩이 가드 5곳에 로드베어링
  (CAT_OVERRIDES · phase9/10 리터럴 · 레지스트리 헤딩 · TOC 앵커).
  MANUAL_REVIEW로 분류, 출발 전 수기 편집 대상.
- **ASSETS 89·90 편람 통합** — phase9 가드가 구조를 강제(51도시어·8카드).
  가드 개편과 함께 별도 결정.
- **Phase 10 공식정보 원칙 등 반복 안내문 제거** — D10 의도적 반복.
  현장 안전·검증 안내는 페이지마다 있어야 하고 가드가 존재를 강제한다.
- **handoff/ 삭제** — 이미 격리된 인계 기록. 기록 가치 유지.
