# Phase 9 — 상용 편집·지역/장소 심화 완료보고서 v1.0

**완료일:** 2026-08-03  
**범위:** Phase 9A Commercial Content, 9B Commercial Editorial, 9C Regional Context, 9D Place Dossiers

## 완료 판정

Phase 9A~9D의 선행 원고를 최신 Regional Chapter와 정적 웹사이트에 연결하고, 누락·구버전 회귀를 차단하는 빌드 게이트로 고정했다. 과거 버전 원고가 아니라 `build/build.py`의 최신 챕터 매니페스트에 지정된 8개 파일만 완료 판정의 근거로 사용한다.

| 구분 | 완료 기준 | 결과 |
|---|---|---:|
| 9A 지역 경험 카드 | 8개 거점의 정체성·예산·강도·예약·우천대안·촬영 기준 | 8/8 |
| 9B 상용 편집모듈 | Editor’s Verdict, 추천 선택, 하루 구성, Top 10, 현장 메모 | 8/8 |
| 9C 지역 맥락 | 역사·경제·사회·문화·여행해석의 다섯 층 | 8/8 |
| 9D 장소 dossier | 일정상 장소의 의미·동선·관람법·체류·주의·공식정보 | 51/51 |
| 배포 확인 | 8개 최신 챕터의 분할 HTML에 Phase 9 콘텐츠 노출 | 8/8 |
| 공식 출발점 | 기준 compendium의 dossier별 공식정보 링크 | 51/51 |

## 빌드 게이트

다음 결함이 생기면 전체 정적 빌드가 실패한다.

- Phase 9 기준 문서 4종의 누락 또는 손상
- 지역 경험 카드가 8개가 아닌 경우
- 최신 Regional Chapter에서 상용 편집모듈 또는 지역 맥락 모듈이 빠진 경우
- 장소 dossier가 총 51개 또는 지역별 6/7/6/6/6/7/5/8개와 일치하지 않는 경우
- dossier의 공식정보 링크가 51개보다 적은 경우
- 웹 배포본에서 Editor’s Verdict, Top 10 또는 지역 맥락이 사라진 경우

## 편집 판단

Phase 9는 장소 수를 늘리는 단계가 아니라, Jason과 Julia의 생활형 장기여행에 맞춰 선택 이유와 삭제 우선순위를 명확히 하는 단계다. 변동 가능한 운영시간·요금은 dossier 본문만으로 확정하지 않고 공식정보 링크 및 Phase 10 재검증 체계로 넘긴다. 실제 숙소·교통·티켓 예약값은 계속 Phase 8B 입력 대기 상태다.

## 결론

- Phase 9A Commercial Content: **완료**
- Phase 9B Commercial Editorial: **완료**
- Phase 9C Regional Context: **완료**
- Phase 9D Place Dossiers: **완료**
- Phase 8B Actual-Booking Lock: **사용자 예약자료 대기**
- 다음 단계: **Phase 10 공식정보 최종 검증 게이트 점검·잠금**

## 검증 기록

- 전체 정적 빌드: 313개 HTML
- 내부 링크: 오류 0건
- Phase 0~9 빌드 게이트: 통과
- 선택적 Playwright 모바일 표본검사: 현재 실행환경에 Chromium 바이너리가 없어 미실행. Phase 9에서는 CSS·레이아웃·내비게이션을 변경하지 않았으며, Phase 7의 기존 시각검수 결과를 유지한다.
