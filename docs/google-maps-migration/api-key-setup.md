# API key setup

1. Google Cloud 프로젝트에서 Maps JavaScript API를 활성화하고 결제 계정을 연결한다.
2. JavaScript용 Map ID를 만든다. Advanced Markers는 Map ID가 필요하다. 로컬 확인만 할 때 코드는 Google의 `DEMO_MAP_ID`로 fallback하지만 운영 배포에는 전용 Map ID를 쓴다.
3. 브라우저 API 키에 Website application restriction을 걸고 실제 GitHub Pages origin만 허용한다.
4. API restriction은 Maps JavaScript API로 제한한다.
5. GitHub 저장소 Secrets에 `GOOGLE_MAPS_API_KEY`, `GOOGLE_MAPS_MAP_ID`를 저장한다.

GitHub Actions의 `Build site` 단계가 환경변수를 읽어 파일럿 페이지 meta에 주입한다. 키를 소스, JSON, 문서, 테스트 fixture에 직접 쓰지 않는다.

브라우저용 키는 빌드 산출물에서 보일 수밖에 없으므로 “비밀 문자열”로 보호하는 대신 referrer와 API 제한으로 오용을 막는다. 허용 referrer는 경로보다 origin 중심으로 설정한다.

공식 참고:

- https://developers.google.com/maps/api-security-best-practices
- https://developers.google.com/maps/documentation/javascript/load-maps-js-api
- https://developers.google.com/maps/documentation/javascript/advanced-markers/start
- https://developers.google.com/maps/documentation/urls/get-started

키 없이 빌드해도 오류가 아니다. 이 상태는 fallback 검수용이며 인터랙티브 마커 검수 완료를 뜻하지 않는다.
