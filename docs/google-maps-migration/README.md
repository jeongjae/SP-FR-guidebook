# Google Maps migration

이 디렉터리는 기존 Leaflet 실행지도를 Google Maps 기반 실행도구로 옮기는 작업의 데이터·설계·검수 기록이다. 현재 범위는 Phase 1 데이터 정규화, Phase 2 공통 컴포넌트, Barcelona Day 2와 Girona Day 6 파일럿까지다. 전체 8개 권역과 43일 전환은 파일럿 승인 전 시작하지 않는다.

## 데이터 흐름

`place-registry.json`과 `daily-routes.json`, `region-groups.json`이 지도 표시의 단일 원본이다. `build/build.py`가 페이지별 최소 JSON, 정적 장소 목록, Google Maps 링크를 HTML에 생성한다. 사용자가 지도를 펼칠 때만 Maps JavaScript API를 불러온다.

## 데이터 수정

- 장소 수정: `source/ASSETS/maps/place-registry.json`의 기존 ID 행을 수정한다.
- 장소 추가: kebab-case 고유 ID, 유형, 좌표, 상태, 개인정보 플래그와 Google Maps URL을 추가한 뒤 필요한 region/day에서 그 ID를 참조한다.
- 날짜 추가: `daily-routes.json`에 날짜, 중심점, 기본 이동수단, 정렬된 stops, 구간별 segments를 추가한다.
- 차량 일정: 관광지가 아니라 실제 주차 노드를 운전 목적지로 둔다.
- Google Place ID: 공식 장소 확인 후 `googlePlaceId`에 넣는다. 개인 장소에는 넣지 않는다.

## API 키

로컬 빌드는 환경변수에서만 키를 읽는다.

```bash
export GOOGLE_MAPS_API_KEY='...'
export GOOGLE_MAPS_MAP_ID='...'
python3 build/build.py
```

키가 없으면 인터랙티브 캔버스만 비활성화되고 목록과 Maps URL은 유지된다. 상세 설정은 `api-key-setup.md`를 본다.

## 빌드와 검증

```bash
python3 scripts/validate_map_data.py
node --test tests/google-map.test.js
python3 -m unittest discover -s tests -p 'test_*.py'
python3 build/build.py
python3 build/pwa_check.py
python3 build/hig_check.py
```

브라우저 대체 검수 스크립트 `tests/browser-qa.mjs`는 CDP가 열린 Chrome/Edge와 `http://127.0.0.1:8765` 로컬 서버를 전제로 한다.

## 배포

GitHub 저장소 Secrets에 `GOOGLE_MAPS_API_KEY`, `GOOGLE_MAPS_MAP_ID`를 등록한다. Pages 워크플로가 두 값을 빌드 단계에만 주입한다. 브라우저 키는 최종 HTML에 노출되는 것이 정상이며, 반드시 웹사이트 referrer 제한과 Maps JavaScript API 제한을 함께 건다.

배포 전 순서:

1. 지도 데이터 검증
2. 전체 정적 빌드와 링크 가드
3. API 키가 있는 preview에서 마커·InfoWindow 검수
4. iPhone Safari와 Android Chrome 실기기 검수
5. 파일럿 승인
6. 다음 배치 진행

관련 문서: `architecture.md`, `data-model.md`, `privacy-policy.md`, `testing-report.md`, `rollback-plan.md`.
