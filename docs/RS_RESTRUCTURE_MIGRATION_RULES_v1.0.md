# RS 개편 마이그레이션 규칙 및 파일럿 계획 v1.0

본 문서는 콘텐츠 구조 개편 마이그레이션 중에 준수해야 할 구체적인 규칙, 기계적 가드 및 앵커에 미치는 영향 분석, 그리고 **Phase 2 니스 파일럿(Nice Pilot)**의 실행 계획을 담고 있다.

---

## 1. 헤딩 의존성 및 빌드 가드 영향 분석

지역 원고의 헤딩은 단순히 텍스트 형태가 아니라 빌드 시스템의 데이터 파싱을 위한 **로드베어링(Load-bearing)** 구조물이다. 헤딩 수정 시 다음 사항을 반드시 동기화해야 한다.

### 1.1 `build/build.py` 내부 가드 목록
1. **Day 가드 (`check_day_sections`)**: 
   * *내용*: 각 지역 챕터 파일 내에 `### Day NN` 헤딩이 누락 없이 존재하며, 43일 전체 일정이 순차적으로 기술되어 있는지 확인.
   * *영향*: Day 명칭이나 순서를 임의로 변경하면 데일리 페이지 생성 단계에서 빌드가 중단된다. Day의 서술형식 및 헤딩 위치는 고정한다.
2. **Phase 9 가드 (`check_phase9`)**:
   * *내용*: 8개 지역 챕터별로 특정 헤딩 목록이 정확히 매치하는지 검사.
   * *영향*: "Commercial Guide Module", "Regional Context" 등의 토큰 헤딩이 존재해야 한다. 의사결정 `RS-D3`에 따라, 이 토큰들을 한글화하려면 8개 챕터 일괄 치환과 가드 코드의 수정이 동시에 이루어지는 **선행 PR**을 실행해야 한다.
3. **Phase 10 가드 (`check_phase10`)**:
   * *내용*: `## Phase 10 공식정보 원칙` 또는 이와 동등한 내용이 각 지역 챕터의 부록에 들어가 있는지 강제 검사.
   * *영향*: 이를 삭제하면 빌드가 중단된다. 해당 정보는 부록 또는 `OPERATIONS/`로의 이동 규칙을 준수하며 가드와 조율하여 개편을 진행해야 한다.

### 1.2 카테고리 매핑 및 앵커 영향
* H2 헤딩 수정 시 `CAT_RULES` 키워드 매핑에 따라 해당 카테고리가 엉뚱한 페이지로 넘어갈 수 있다. 템플릿의 H2 제목 규격을 준수하고, 필요한 경우 `CAT_OVERRIDES`에 수동 매핑 쌍을 추가 등록해야 한다.
* 다른 마크다운 파일이나 인덱스에서 지역 내 특정 앵커(`#heading-anchor`)를 가리키는 내부 링크가 파손될 수 있으므로, 헤딩 정리 후 반드시 `python3 build/build.py`를 실행하여 `Broken links: 0`을 확인해야 한다.

---

## 2. 콘텐츠 이사 및 감량 규칙 (MIGRATION RULES)

1. **중복 시간표의 단일화**: Region 본문 내의 중복되는 시간표 표(2~3중 중복)는 제거하고, 챕터 내부의 `Day` 절 링크로만 렌더링되게 한다.
2. **장소 서사의 통합**: Region 내의 개별 장소 묘사는 장소 페이지(`places/slug.html`)로 일원화하고, Region에서는 장소의 가치 판단 한 줄 및 링크만 남긴다.
3. **Walk의 신설**: Walk는 `91_Place_Registry_v1.0.md`에 `walk` 등급으로 등재한 후 별도의 장소 마크다운으로 구현해 `places/` 내에 생성한다.
4. **제작 용어 및 초안의 격리**: 독자 대상이 아닌 아카이브/취소 기록, "기존 원고가 ~했다"와 같은 제작 서사, 미결정 권고 사항 등은 `docs/` 또는 `source/OPERATIONS/`로 추출하여 기록하며 본문에서는 보이지 않게 제거한다.

---

## 3. Phase 2 니스 파일럿 (Nice Pilot) 실행 계획

*니스 파일럿의 목적은 전 지역으로의 구조 재편을 확대하기 전에 실제 구조, 가독성, 모바일 뷰, 빌드 가드의 안정성을 사전 검증하는 데 있다.*

### 3.1 파일럿 대상 범위
* **지역(Region)**: Nice (06 챕터)
* **데일리(Daily)**: Day 7 – Day 11 (총 5일분)
* **장소(Place)**: 약 8개 주요 장소 Dossier
* **도보 가이드(Walk)**: 다음 3개 신설
  1. `nice-old-town-castle-hill` (Nice Old Town–Castle Hill Walk)
  2. `cannes-forville-suquet` (Cannes Forville–Suquet–Croisette Walk)
  3. `monaco-rocher-port` (Monaco Rocher–Port–Monte Carlo Walk)

### 3.2 파일럿 대상 수정 파일 목록

| 역할 | 수정 파일 경로 | 변경 내용 |
|---|---|---|
| Region 원본 | `source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md` | H2 구조 템플릿화, 중복 시간표 및 장소 서사 제거, Walk 절 연계 |
| 장소 레지스트리 | `source/ASSETS/91_Place_Registry_v1.0.md` | 신규 Walk 3종을 `walk` 타입으로 등록 |
| 장소 dossier | `source/ASSETS/90_Regional_Context_and_Place_Dossier_Compendium_v1.0.md` | 니스 관련 장소(약 8곳) 서사 심화 보강 및 템플릿 정합화 |
| 빌드 가드 | `build/build.py` | `RS-D1`(Walk 유형), `RS-D3`(가드 토큰 치환) 관련 예외 규칙 및 빌드 렌더러 조정 |
| 트래커 | `source/OPERATIONS/100_Phase5_43_Day_Execution_Audit_Report_v1.0.md` | Day 7 이동일 불일치 정보(VY1521 편) 정합화 반영 |

### 3.3 예상 감량률 (Nice Chapter 기준)
* **현재 니스 챕터 원고 규모**: 44,282글자 (wc -m)
* **목표 감량 범위**: 30% ~ 45% 감량
* **파일럿 목표 글자수**: **24,000자 ~ 30,000자** 이내로 슬림화 및 장소/Walk로의 분배 완료.

### 3.4 파일럿 통과 판단 스코어카드 (Gate 조건)
니스 파일럿 변경 완료 후, 아래의 기준을 검토하여 단 하나라도 만족하지 못하면 타 지역으로 확대하지 않고 작업을 즉시 중단한다.
* Region 본문 감량률 30~45% 달성 및 핵심 사실 소실 0건.
* 독자 화면에 기획/제작 관련 내부 placeholder 노출 0건.
* 신설 Walk 3종의 모든 정차점 번호가 지도 KML/JSON 번호와 100% 일치.
* 모바일 해상도(390px) 실기 검사 시 표/텍스트 영역의 가로 스크롤 발생 0건.
* 빌드(`build.py`) 및 HIG 검사(`hig_check.py`)가 오류 없이 100% PASS를 통과할 것.
