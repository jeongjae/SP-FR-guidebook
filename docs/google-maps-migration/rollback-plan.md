# Rollback plan

파일럿은 기존 URL과 레거시 자산을 보존하므로 데이터 삭제 없이 되돌릴 수 있다.

1. `build/build.py`의 `GOOGLE_MAP_PILOT_DATES`를 빈 set으로 바꾼다.
2. `GOOGLE_MAP_PILOT_REGIONS`를 빈 dict로 바꾼다.
3. 빌드와 링크 가드를 실행한다.
4. `site/`를 다시 배포한다.

이렇게 하면 Day 1·2·3·5·6은 기존 `daily-map.js` 경로로, 8개 권역은 기존 Leaflet 생성 경로로 돌아간다. `google-map*.js/css`, 정규 JSON, 테스트와 문서는 남겨도 기존 페이지가 참조하지 않는다.

롤백하지 않는 항목:

- private 숙소 정확 주소·정밀 좌표 제거
- 안전한 근사 위치 정책
- tracker의 공개 예약 URL 제거

개인정보 보호 변경을 되돌리면 안 된다. Git 기록 재작성도 별도 승인과 백업 계획 없이 수행하지 않는다.
