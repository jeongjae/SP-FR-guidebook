# Testing report

검수 대상 흐름: `daily/day-02.html → 필터 → 장소 선택 → 지도 펼치기 → API 실패 시 목록 유지`, `daily/day-06.html → 주차 필터 → 주차 우선 다중 경유 URL → private 복귀 수동 처리`.

## 자동 테스트

| 검사 | 결과 |
|---|---|
| `scripts/validate_map_data.py` | 통과, 오류 0, Place ID 경고 71 |
| Node URL·privacy 테스트 | 5/5 통과 |
| Python validator 테스트 | 3/3 통과 |
| `build/build.py` | 통과, 314 HTML |
| 링크·날짜·기존 Phase 1~10 빌드 가드 | 통과 |
| PWA 오프라인 목록 | 451개 파일, 새 JS/CSS/JSON 포함 |
| 정확 주소·정밀 좌표 current-tree scan | 일치 0 |

## 브라우저 테스트

브라우저 플러그인은 이 환경에 제공되지 않았다. Linux Playwright Chromium과 기존 `pwa_check.py`, `hig_check.py`의 브라우저 단계는 `libnspr4.so` 누락으로 실행되지 않았다. 대신 Windows Edge 151과 Chrome을 headless CDP로 연결해 같은 정적 사이트를 검수했다.

- 375px: 가로 넘침 0, 최소 타깃 44px
- 390px: Day 2 관광지 필터 2곳, 선택 `aria-pressed=true`, 오류 fallback
- 768px: Girona 권역 목록, 가로 넘침 없음, 최소 타깃 44px
- 1440px: Day 6 주차 필터 4곳, Barcelona 권역 목록, 오류 fallback
- 브라우저 page exception 및 console error 0
- private 숙소 카드에 공개 지도 링크 없음

스크린샷은 로컬 임시 폴더 `C:/Users/NB-24021500/AppData/Local/Temp/spfr-map-qa`에 생성했다.

## 미검수

- 실제 API 키로 로드된 지도와 AdvancedMarkerElement
- 마커 클릭과 InfoWindow 상호작용
- Safari iPhone, Chrome Android 실기기
- Google Maps 모바일 앱 딥링크
- Linux 환경의 원래 PWA/HIG Playwright 브라우저 단계

따라서 Phase 3은 구현 완료가 아니라 승인 대기 상태다.
