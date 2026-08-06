# Google Maps pilot design

- 상태: 승인 대기
- 범위: Barcelona 도보 파일럿 + Girona/Costa Brava 차량 파일럿
- 금지: 이 문서 승인 전 8개 지역·43일 전체 변환 시작 금지

## 공통 선행 조건

1. Bàscara 개인 숙소의 정확 주소·Google Maps URL·고정밀 좌표를 공개 소스와 생성 사이트에서 제거한다. 공개용 좌표가 필요하면 실제 위치와 300–500m 이상 떨어진 일반 기준점을 사용하고 `private=true`, `approximate=true`로 둔다.
2. `place-registry.json`, `daily-routes.json`, `region-groups.json`, `map-schema.json`과 검증 스크립트를 먼저 만든다.
3. GitHub Actions는 `GOOGLE_MAPS_API_KEY` 환경변수를 빌드에만 전달한다. 키는 결과 사이트에서 보일 수 있음을 전제로 GitHub Pages referrer, 허용 API, quota와 예산 알림을 제한한다.
4. API 키 누락·스크립트 차단·오프라인 상태에서도 서버 렌더 장소 목록과 사전 생성 Google Maps URL을 먼저 제공한다.
5. API는 사용자가 지도 펼치기 또는 지도 영역 진입을 했을 때 한 번만 지연 로드한다.

## Pilot A — Barcelona 도보 일정

### 대상

- 지역: Barcelona
- 일자: 2026-08-30 (Day 2)
- 장소: 공개 숙소 후보, Sagrada Família, Sant Pau Recinte Modernista
- 이동수단: 숙소 후보→Sagrada 구간은 실제 운영 판단 후 `walking` 또는 `transit`; Sagrada→Sant Pau는 `walking`

### 검증 기능

- 유형 필터와 전체 보기
- 번호 마커, 장소 카드, 키보드 선택의 양방향 동기화
- 후보 숙소 배지와 선택 일정 제외 규칙
- 현재 위치→첫 장소, 장소 보기, 다음 장소 길찾기
- 기본 경로 URL에서 optional 장소 제외
- 접힌 지도보다 먼저 보이는 모바일 실행 버튼과 장소 목록
- API 실패 시 동일한 목록·링크 유지

### 데이터 판단

- Praktik Garden은 상업 숙박시설이지만 현재 예약 후보이므로 “숙소에서 길찾기” 기본 버튼을 만들지 않는다.
- Sagrada와 Sant Pau의 Google Place ID는 승인 후 공식 Place 검색 결과로 채운다. 이름만으로 런타임 geocoding하지 않는다.

## Pilot B — Girona/Costa Brava 차량 일정

### 대상

- 지역: Girona / Costa Brava
- 일자: 2026-09-03 (Day 6)
- 기본 장소: Tossa de Mar, Sant Feliu de Guíxols, Peratallada
- 선택 장소: Pals
- 출발·복귀: 공개용 Bàscara 근사 기준점
- 이동수단: 구간별 `driving`; 마을 내부 보행은 별도 구간 또는 장소 카드 안내

### 구현 전 확인할 데이터

- Tossa, Sant Feliu, Pals, Peratallada에서 실제 사용할 공영 주차장과 진입 제한
- GI-682 해안도로의 당일 통행·기상 조건
- 선택 Pals를 뺀 기본 경로와 넣은 선택 경로
- Bàscara 정확 숙소가 URL origin/destination/waypoint에 들어가지 않는지

주차장 이름과 좌표는 추측으로 만들지 않는다. 공식 지자체·주차 운영 정보와 Google Maps 결과를 함께 확인한 뒤 `parking` 장소로 등록한다.

### 검증 기능

- `driving`이 URL에 유지되고 보행 모드로 강제되지 않음
- 관광지 대신 주차장을 차량 목적지로 사용
- 선택 장소가 기본 전체 일정 URL과 기본 지도 경로에서 제외됨
- 장거리 URL 길이·경유지 제한 시 오전/오후 또는 구간별 링크로 분리
- private 장소의 주소·Place ID·정확 좌표·숙소 출발 버튼이 HTML·JS·JSON·KML에 없음

## 공통 컴포넌트 경계

```text
build.py
  ├─ 해당 페이지용 최소 JSON을 인라인 또는 별도 파일로 생성
  ├─ 장소 목록·action URL을 서버 렌더
  └─ 지도 컨테이너와 지연 로더만 주입

google-map-loader.js
  └─ Maps JavaScript API 1회 로드, 성공/실패/timeout 상태 공유

google-map.js
  ├─ initRegionMap / initDailyMap
  ├─ AdvancedMarkerElement / InfoWindow
  ├─ 필터·목록 동기화
  └─ API 실패 시 기존 서버 렌더 fallback 유지
```

Google Maps URL 생성 함수는 DOM 렌더러와 분리해 Node 내장 테스트 러너로 검증 가능하게 만든다. 실제 도로선은 Routes API 응답이 있을 때만 표시하며, 실패하면 직선으로 대체하지 않고 구간 카드와 Google Maps 링크만 남긴다.

## 파일럿 합격 기준

- 정적 빌드·지도 데이터 검증·기존 링크 검사가 모두 통과한다.
- API 키 있음/없음, 스크립트 차단, 오프라인 네 경우에 페이지 본문과 장소 목록이 유지된다.
- 375·390·768·1024px에서 44px 터치 타깃, 초점 표시, 지도 영역 CLS 예약을 확인한다.
- 데스크톱 Chrome/Edge를 자동 검증하고, iPhone Safari/Android Chrome은 실기기 결과를 별도 기록한다.
- Google Maps 앱/웹에서 Barcelona 보행·대중교통과 Girona 운전 모드가 의도대로 열린다.
- 저장소와 생성 사이트를 검색했을 때 개인 숙소 정확 주소·정확 좌표가 0건이다.
- 파일럿 결과와 미해결 사항을 보고하고 별도 승인을 받은 뒤에만 8개 지역 전환을 진행한다.

## 승인 요청 항목

1. Phase 1에서 개인정보 차단을 최우선으로 처리하는가.
2. Barcelona Day 2와 Girona Day 6을 파일럿 대상으로 확정하는가.
3. 공개 Git 기록에 남은 개인 숙소 정보의 이력 정리까지 이번 마이그레이션 범위에 포함하는가.
