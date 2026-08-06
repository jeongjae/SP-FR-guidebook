# Migration report

## Phase 1 완료 보고

### 수행 내용

- 8개 GeoJSON, KML, 5일 daily 데이터를 72개 고유 장소 레지스트리로 정규화
- 날짜·권역 데이터를 placeId 참조 구조로 전환
- Girona 차량 일정에 공식 주차 근거가 있는 주차 노드 4개 추가
- private 숙소를 공개용 근사 권역으로 전환하고 현재 트리에서 정확 위치 제거

### 변경 파일

- `source/ASSETS/maps/*.json`
- `scripts/validate_map_data.py`
- 개인정보가 있던 CURRENT·ARCHIVE·OPERATIONS·지도 자산과 tracker XLSX

### 테스트 결과

- 고유 ID 72/72, 존재하지 않는 placeId 0, 좌표 오류 0
- private 공개필드 오류 0
- Python validator 단위 테스트 3개 통과

### 발견된 문제

- 공개 장소 71곳의 Google Place ID가 아직 없다.
- Git 과거 기록은 정리되지 않았다.

### 미해결 사항

- API 키 또는 승인된 수동 검증 절차로 Place ID를 채워야 Phase 1의 모든 작업 항목이 닫힌다.

### 다음 단계

- 파일럿 live API 검수와 Place ID 보강

## Phase 2 완료 보고

### 수행 내용

- lazy singleton loader, URL·필터·마커·InfoWindow·목록 동기화 공통 컴포넌트 구현
- 서버 렌더 fallback과 API 오류 격리
- PWA 자산 포함, 빌드 환경변수 및 GitHub Secrets 연결

### 테스트 결과

- JavaScript 단위 테스트 5개 통과
- 키 누락 상태에서 목록·링크·필터·선택·정적 카드 유지

### 미해결 사항

- 실제 API 키를 사용한 Advanced Marker와 InfoWindow 검수

## Phase 3 파일럿 보고

### 수행 내용

- Barcelona 권역과 Day 2 도보 파일럿
- Girona 권역과 Day 6 주차 우선 차량 파일럿
- 기존 URL 유지, 나머지 Leaflet 자산 보존

### 테스트 결과

- 전체 빌드 314 HTML, 모든 정적 회귀 가드 통과
- Edge·Chrome에서 375·390·768·1440px, 필터·카드 선택·키 누락 fallback 통과
- 기본 Day 6 운전 URL은 공개·필수 주차장 3곳만 포함

### 발견된 문제

- Linux Playwright Chromium은 실행환경의 `libnspr4.so` 부재로 시작하지 못했다.

### 미해결 사항

- API 키 기반 live map, 마커 클릭, InfoWindow
- iPhone Safari·Android Chrome 실기기와 Google Maps 앱 전환

### 다음 단계

- 위 미해결 검수를 마치고 파일럿 승인을 받은 뒤에만 Phase 4를 시작한다.
