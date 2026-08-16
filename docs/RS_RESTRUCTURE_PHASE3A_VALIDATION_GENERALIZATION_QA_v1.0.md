# Rick Steves Restructuring: Phase 3A Validation Generalization QA Report

This report documents the completion of **Phase 3A — 콘텐츠 검증 인프라 일반화 (Validation Generalization)**. All hardcoded validation guards, magic numbers, and region-specific heading rules have been replaced with a generalized, schema-driven verification system. Regression protection tests have been introduced, and the build compiles cleanly with exit code `0`.

---

## 1. 콘텐츠 검증 일반화 개요 (Generalization Overview)

Nice Pilot에서 사용되던 하드코딩 검증 규칙들을 제거하고, 기계가 쉽게 읽고 쓸 수 있는 단일 스키마 파일(`build/content_schema.json`)을 정본으로 구성하여 빌드 시스템을 리팩토링했습니다.

*   **스키마 정의 파일**: [`build/content_schema.json`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-content-dev/build/content_schema.json)
*   **검증 엔진 리팩토링**: [`build/build.py:check_phase9_commercial_depth_guards`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-content-dev/build/build.py#L5655-L5846)

### 주요 개선 사항
1.  **명시적 콘텐츠 스키마 선언**:
    *   Nice 챕터 원고([`06_Nice_Cote_d_Azur_v2.0.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-content-dev/source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md))의 front matter에 `content_schema: rs-region-v1`을 추가했습니다.
    *   선언이 없는 기존 7개 지역은 스키마 검증 시 기본값인 `legacy-region-v1` 검증 규칙을 적용받습니다.
    *   존재하지 않거나 정의되지 않은 스키마를 선언하는 경우 즉시 빌드가 오류(`SystemExit: 1`)로 실패합니다.
2.  **데이터 구동형 빌드 차단**:
    *   특정 지역에 대한 H2 헤딩 조건이나 기대 파일 수와 같은 정보들을 코드 외부의 스키마 및 매핑 데이터로 이관하여 향후 신규 챕터 개편 시 코드 변경 없이 명시적 설정 선언만으로 검증이 기능하도록 설계했습니다.

---

## 2. 레지스트리-Dossier 상호 검증 (Registry-Dossier Cross-Validation)

장소 레지스트리([`91_Place_Registry_v1.0.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-content-dev/source/ASSETS/91_Place_Registry_v1.0.md))와 장소 심화 컴펜디움([`90_Regional_Context_and_Place_Dossier_Compendium_v1.0.md`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-content-dev/source/ASSETS/90_Regional_Context_and_Place_Dossier_Compendium_v1.0.md)) 간의 ID 연결성과 정합성을 상호 매핑 데이터 기반으로 다음과 같이 차단 및 개선했습니다.

### 검증 지표 및 무모순성 검증 결과
*   **중복 ID**: `0건` (성벽-대성당 간 복사-붙여넣기 오기입으로 중복되었던 `Girona Cathedral`을 `Passeig de la Muralla`로 분리 교정)
*   **누락 dossier**: `0건` (`dossier_mapping`에 정의된 슬러그가 레지스트리에 존재하며, 해당 헤딩이 컴펜디움에 존재함을 확인)
*   **Orphan dossier**: `0건` (레지스트리 매핑이 없는 쓰이지 않는 dossier 헤딩이 없음을 확인)
*   **필수 필드 결측**: `0건`
    *   **Spot 타입**: `방문`, `관람`, `체류`, `요금·예약` (및 그 변형), `주의`, `공식정보` 6대 요소를 강제 검증.
    *   **Walk 타입**: 셀프가이드 도보 경로 타입으로 `공식정보` 필수성 검증 적용.
*   **공식 출처 존재성**: `0건` (모든 dossier 레코드가 유효한 `https?://\S+` 형식의 `- 공식정보:` 값을 보유하는지 확인)

> [!NOTE]
> Girona 성벽인 `Passeig de la Muralla`를 장소 레지스트리에 정식 등록하고 컴펜디움의 타이틀 중복을 수정하여 0 Orphan / 0 Duplicates 상태를 실현했습니다.

---

## 3. 회귀 보호 검증 (Regression Protection & Negative Tests)

검증 가드들이 기능적 퇴보(Regression)를 일으키지 않고 비정상 파일을 확실히 잡아내는지 보장하기 위해 9가지 실패 유즈케이스에 대응하는 네거티브 테스트 픽스처를 자동화 단위 테스트로 작성하여 동작을 입증했습니다.

*   **테스트 스크립트**: [`build/test_validation.py`](file:///mnt/c/Users/NB-24021500/source/worktrees/SP-FR-content-dev/build/test_validation.py)

### 9가지 실패 유즈케이스와 테스트 결과
단위 테스트 스크립트 실행을 통해 9가지 네거티브 테스트 픽스처가 의도한 빌드 차단을 성공적으로 재현하고 정상 자료에서 PASS 함을 증명했습니다:

1.  **필수 H2 누락**: `## 꼭 경험할 세 장면`을 제거 시 가드 오류 발생 (PASS)
2.  **필수 H2 순서 오류**: `Editor’s Verdict`와 `꼭 경험할 세 장면`의 순서를 뒤집을 시 가드 오류 발생 (PASS)
3.  **필수 H2 중복**: 중복 헤딩이 금지된 새 스키마에서 헤딩 중복 시 가드 오류 발생 (PASS)
4.  **알 수 없는 content_schema**: 존재하지 않는 스키마 선언 시 즉시 빌드 차단 (PASS)
5.  **Registry 항목의 dossier 누락**: 레지스트리에는 있으나 컴펜디움에 dossier가 없는 경우 차단 (PASS)
6.  **Registry에 없는 orphan dossier**: 컴펜디움에 있으나 레지스트리 매핑이 되지 않은 경우 차단 (PASS)
7.  **중복 place/walk ID**: dossier 헤딩이 중복 존재할 시 차단 (PASS)
8.  **walk의 필수 필드 누락**: walk 타입 dossier에서 `공식정보` 누락 시 차단 (PASS)
9.  **필수 공식 출처 누락**: spot 타입 dossier에서 `공식정보` 누락 시 차단 (PASS)

```bash
$ python3 build/test_validation.py
..........
----------------------------------------------------------------------
Ran 10 tests in 11.102s

OK
```

---

## 4. 빌드 및 배포 상태 (Build & Deployment Status)

최종 릴리즈 빌드 프로세스가 모두 PASS하며 정상적으로 빌드를 완료했습니다.

```bash
$ python3 build/build.py && python3 build/hig_check.py
...
Phase 9 상용편집·장소심화 가드: 스키마 및 레지스트리-Dossier 검증 이상 없음
...
완료: .../site (332개 HTML 페이지)
...
HIG 검사: 19쪽 × 3폭(320·390·430) × 라이트/다크 — 터치타깃 · 글자크기 · 명암비 · 안전영역 · 리플로 · 뷰포트 이상 없음
```

*   **생성 페이지 수**: `332개` HTML 페이지
*   **종합 빌드 결과**: **SUCCESS** (Exit Code: `0`)
