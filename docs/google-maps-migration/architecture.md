# Architecture

## 구성

```text
place-registry.json ─┬─ region-groups.json
                     └─ daily-routes.json
                              │
                     scripts/validate_map_data.py
                              │
                        build/build.py
                              │
      서버 렌더 목록·Maps URL·페이지별 JSON
                              │
                 google-map-loader.js (lazy singleton)
                              │
                  google-map.js + google-map.css
```

정적 목록과 링크가 기본 화면이다. `<details>`를 펼칠 때만 loader가 Maps JavaScript API를 한 번 요청한다. 키 누락, 네트워크 실패, 타임아웃 시 상태 메시지를 표시하고 빈 캔버스를 접는다. 재시도 루프는 없다.

## 지도 동작

- `google-map-loader.js`: 페이지의 meta에서 키와 map ID를 읽고 하나의 Promise를 공유한다.
- `google-map.js`: URL 생성, 필터, 카드 선택, AdvancedMarkerElement, InfoWindow, 목록/마커 동기화를 담당한다.
- `google-map.css`: 기존 Nanum Gothic·색상 토큰·44px 타깃을 재사용한다.
- 실제 경로선은 그리지 않는다. 장소·구간·다중 경유 동선은 Google Maps URL에서 계산한다.
- InfoWindow는 문자열 HTML 삽입 대신 DOM과 `textContent`로 만든다.

## 파일럿과 레거시 공존

- Google 권역 파일럿: `maps/barcelona.html`, `maps/girona.html`
- Google 일자 파일럿: `daily/day-02.html`, `daily/day-06.html`
- 기존 Leaflet: 나머지 6개 권역과 Day 1·3·5에 한 릴리스 이상 보존

기존 URL은 바뀌지 않는다. PWA는 새 JSON·CSS·JS를 캐시하지만 Google 지도 타일은 캐시하지 않는다.
