# Data model

## place-registry.json

장소는 한 번만 정의한다.

- `id`: kebab-case 고유 ID
- `name`, `city`, `type`: 표시명, 도시, 표준 유형
- `lat`, `lng`: 공개 가능한 좌표
- `googlePlaceId`: 확인된 Google Place ID. 현재 공개 장소 71곳은 미확인 경고 상태다.
- `googleMapsUrl`: 키 없이 작동하는 Maps URL
- `private`, `approximate`, `optional`: 개인정보·근사·선택 플래그
- `status`: `confirmed`, `planned`, `candidate`, `alternative`
- `sourceUrl`: 주차장처럼 운영 검증이 필요한 장소의 근거

개인 장소는 `address`, `googleMapsUrl`, `googlePlaceId`가 비어 있어야 하고 좌표는 소수점 3자리 이하의 근사 권역만 허용한다.

## daily-routes.json

`stops`는 `placeId`, `order`, `plannedTime`, `note`만 가진다. `segments`는 `from`, `to`, `mode`와 선택·수동 플래그를 가진다. private 목적지 구간은 `manual: true`여야 한다.

운전 다중 경유 URL은 private·optional 장소를 제외하고 `type=parking`인 노드만 사용한다. Day 6의 기본 운전 동선은 Tossa 주차 권역 → La Corxera → Aparcament Baix다. Pals 주차는 선택 일정이라 기본 URL에서 빠진다.

## region-groups.json

권역 ID, 표시명, 중심점, zoom, `placeIds`를 가진다. Barcelona 8곳, Girona 15곳(기존 11곳과 주차 4곳), 나머지 49곳으로 정규 레지스트리는 총 72곳이다.

## 검증

`map-schema.json`은 JSON Schema 문서이며, 실제 빌드 게이트는 외부 패키지 없는 `scripts/validate_map_data.py`가 수행한다. 중복 ID, 좌표 범위, 참조 무결성, 이동수단, private 공개 필드를 오류로 처리하고 Place ID 누락·근사·선택 상태는 경고로 남긴다.
