# Google Maps migration baseline

- 기준일: 2026-08-05 (Asia/Seoul)
- 작업 브랜치: `jeongjae/google-map`
- 상태: Phase 0 조사 완료, 파일럿 설계 승인 대기
- 범위: 추적 중인 소스 자산과 현재 빌드가 생성한 `site/` 결과

## Phase 0 완료 보고

### 수행 내용

- 작업지시서의 최초 명령을 실행했다. 조사 시작 시 작업 트리는 깨끗했고, `/tmp/all-files.txt`에는 314개 파일, `/tmp/map-references.txt`에는 448개 참조 행이 기록됐다.
- 8개 지역 지도의 HTML·GeoJSON·KML, 일자 지도 JSON, Leaflet 런타임, 정적 일자 schematic, 컨택트시트, 지도형 편집 도식을 목록화했다.
- 현재 빌드를 실행해 생성된 314개 HTML을 기준으로 지도 표시 페이지와 링크 페이지를 역추적했다.
- 지역 지도 68개 기준점과 일자 지도 16개 배치 레코드의 이름·ID·좌표 중복을 비교했다.
- 개인정보, 이동수단, fallback, 데이터 단일 원본, 문서 드리프트, 테스트 가드의 위험을 확인했다.

### 변경 파일

- `docs/google-maps-migration/map-inventory.csv`
- `docs/google-maps-migration/page-map-matrix.csv`
- `docs/google-maps-migration/duplicate-place-report.csv`
- `docs/google-maps-migration/migration-baseline.md`
- `docs/google-maps-migration/pilot-design.md`

### 테스트 결과

- `python3 build/build.py`: 성공. 현재 결과는 HTML 314개, 지역 지도 8개, GeoJSON 기준점 68개다.
- 지역 지도 triad 대조: 8개 모두 HTML·GeoJSON·KML 레코드 수는 일치한다. Girona는 좌표 자체는 이름별로 일치하지만 HTML과 GeoJSON/KML의 순서·분류·상태가 다르다.
- 좌표 기본 검사: 68개 GeoJSON 기준점과 16개 일자 배치 레코드에 전역 위·경도 범위 오류는 없다. 도시별 경계와 실제 출입구·주차장 정합성은 아직 검증하지 않았다.
- `python3 build/hig_check.py`: 실행했으나 Playwright Chromium의 `libnspr4.so` 누락으로 브라우저가 시작되지 않아 미완료다. 정적 빌드 성공과 브라우저/HIG 검증 성공은 구분한다.
- `python3 build/pwa_check.py`: 로컬 서버 권한을 허용해 재실행했으나 같은 `libnspr4.so` 누락으로 Playwright 브라우저 단계 1건이 실패했다.

### 발견된 문제

1. 공개 빌드에 개인 숙소 정보가 노출된다. Bàscara Airbnb의 정확 주소 또는 7자리 좌표가 13개 생성 파일에서 확인됐다. 원본 GeoJSON·KML·HTML, CURRENT 챕터, 운영 문서와 XLSX에도 같은 정보가 있어 단순 UI 숨김으로 해결되지 않는다.
2. `daily-maps.json`은 43일 정본이 아니라 Day 1·2·3·5·6의 5일만 가진 프로토타입이다. 16개 장소 배치와 13개 구간만 존재하며 Day 4와 Day 7–43은 인터랙티브 일자 지도가 없다.
3. 일자 지도 가드는 Barcelona 3일만 검사한다. 데이터에 들어 있는 Girona Day 5·6은 생성되지만 배포 계약 검증 대상이 아니다.
4. `daily-map.js`는 `routes[].mode`를 읽지 않고 모든 Google Maps 길찾기 URL을 `walking`으로 만든다. Girona 차량 일정도 보행 길찾기로 열린다.
5. 내부 경로선은 여전히 좌표 간 직선이다. 선택 장소 Pals도 기본 지도 직선에 포함된다.
6. Leaflet 로딩 실패 시 동적으로 만들 장소 목록과 링크까지 사라진다. 서버 렌더 fallback이 없어 “지도 없이도 장소 목록·길찾기 사용” 요구를 충족하지 못한다.
7. `daily-map-data.js`가 5일 전체 데이터를 모든 인터랙티브 지도 페이지에 싣는다. 날짜 페이지가 해당 날짜 데이터만 사용해야 한다는 목표와 다르다.
8. 68개 지역 기준점은 HTML·GeoJSON·KML 세 파일에 중복된다. 일자 데이터의 13개 물리적 장소도 같은 지역 데이터와 다시 겹친다.
9. 좌표 없는 Markdown 장소 레지스트리 84행, 지역 지도 68점, 일자 지도 16배치가 병렬 모델로 유지된다. 현재 `91_Place_Registry_v1.0.md`와 작업지시서의 신규 JSON 레지스트리 사이 역할 정리가 필요하다.
10. Girona HTML은 최신 일자 흐름을 반영해 Pals→Peratallada→Peralada 순서지만 GeoJSON/KML은 Peralada→Pals→Peratallada 순서다. 카테고리와 상태 문구도 다르다.
11. Google Place ID는 현재 지도 모델에 없고, 지역 지도 유형은 한국어 자유 분류라 목표의 닫힌 장소 유형 목록과 호환되지 않는다.
12. 빌드 검증 문구는 68개 기준점인데 `docs/PHASE6_EXECUTION_MAPS_REPORT_v1.0.md`는 65개로 기록해 문서가 뒤처졌다.
13. 목표 이동수단 `train`, `flight`, `manual`은 현재 데이터 검사기가 거부한다. `supermarket`, `gym`, `pool`, `viewpoint`, `event`, `other` 장소 유형도 현재 검사기가 허용하지 않는다.
14. Maps JavaScript API 로더, API 키 빌드 주입, Advanced Marker, 실제 Routes API 렌더링은 아직 없다.

### 미해결 사항

- 개인 숙소 정보는 공개 Git 기록에도 이미 포함됐을 가능성이 높다. 다음 단계에서 현재 파일을 정리하는 것과 과거 커밋 이력 처리 범위를 별도로 결정해야 한다.
- 68개 기준점의 실재 장소, 입구, 주차장, 도시 진입 제한, 보행 가능성은 공식 출처와 실사용 지도에서 검증하지 않았다.
- iPhone Safari와 Android Chrome 실기기 검증 환경은 확보되지 않았다.
- Google Cloud 프로젝트, referrer 제한 API 키, 사용 API와 예산 알림 설정은 저장소에서 확인할 수 없다.

### 다음 단계

- `pilot-design.md`의 Barcelona와 Girona 파일럿 범위, 개인정보 선행 조치, API 사용 방식을 승인받는다.
- 승인 후 Phase 1에서 공개 개인정보를 먼저 차단하고, 네 JSON/Schema 및 `scripts/validate_map_data.py`를 만든다.
- Phase 1 검증을 통과한 뒤 Phase 2 공통 컴포넌트와 두 파일럿만 구현한다. 8개 지역 및 43일 전체 변환은 파일럿 승인 전 시작하지 않는다.

## 1. 현재 지도 구조 요약

```text
지역 지도: 8 HTML + 8 GeoJSON + 8 KML
  build_maps() → site/maps/{region}.html
               → site/maps/data/*.{geojson,kml}
  build_offline_maps() → site/maps/kml/{region}.kml

일자 지도: daily-maps.json(5일)
  build_daily() → 해당 5개 daily 페이지에 Leaflet 컨테이너 삽입
  main()        → 5일 전체를 site/assets/daily-map-data.js 한 파일로 출력
  daily-map.js → OSM 타일 + 마커 + 직선 + Google Maps URL

정적 fallback: 일자 카드 43개 빌드 출력
  Day 12–24는 Phase4 우선본 사용
  Day 4–6은 예약 전 제작본이라 페이지에서 숨김
```

현재 Google Maps는 사이트 내부 지도 엔진이 아니라 외부 검색·길찾기 링크로만 사용된다.

## 2. 지도 파일 전체 목록

전체 개별 목록은 `map-inventory.csv`에 있다.

| 분류 | 수량 | 비고 |
|---|---:|---|
| 지역 지도 원본 | 24 | 8지역 × HTML·GeoJSON·KML |
| 지역 기준점 | 68 | HTML·GeoJSON·KML에 반복 |
| 일자 지도 데이터 | 1 | 5일·16배치·13구간 |
| 지도 빌드/런타임 | 2 | `build.py`, `daily-map.js` |
| Leaflet 로컬 자산 | 7 | JS·CSS·마커 이미지 |
| 정적 일자 schematic PNG | 60 | 기존 43 + Phase4 13 + PassB 샘플 4 |
| 컨택트시트 JPG | 9 | 기존 5 + Phase4 4 |
| 정적 전체경로 도식 | 1 | 여행 전체 경로·숙박 구조 |
| 레지스트리·색인·보고 문서 | 5 | 장소·지도·일자·라우팅·Phase 6 보고 |
| 합계 | 109 | 생성된 `site/` 사본은 제외 |

`source/CURRENT`에는 `strategy=execution-map`인 지도 자리표시자 ID도 20개 남아 있다. 별도 지도 파일이 아니라 현재 8개 지역 실행지도로 연결되는 서술용 참조이므로 자산 수량에는 넣지 않았다.

## 3. 실제 사이트 페이지와 지도 연결

개별 153개 페이지 행은 `page-map-matrix.csv`에 있다.

| 페이지 유형 | 페이지 수 | 현재 연결 |
|---|---:|---|
| 지역 지도 표시 | 8 | Leaflet/OSM 지도와 기준점 목록 직접 렌더 |
| 일자 페이지 | 43 | 모두 1개 이상 지역 지도 링크; 전환일 7개는 2개 링크 |
| 일자 인터랙티브 임베드 | 5 | Day 1·2·3·5·6 |
| 일자 정적 schematic 표시 | 40 | Day 4–6은 오래된 카드라 숨김 |
| 지역 챕터 | 17 | 해당 지역 지도 링크 |
| 장소 상세 | 81 | 소속 지역 지도 링크 |
| 홈·지역·지도 색인 | 4 | 8개 지역 지도 탐색 |
| 오프라인 지도 | 1 | 생성된 KML 8개 다운로드 |

## 4. 데이터 중복 및 위험요소

개별 중복은 `duplicate-place-report.csv`에 있다. 핵심은 다음과 같다.

- 지역 기준점 68개는 동일 장소를 HTML·GeoJSON·KML에 각각 보관한다.
- 일자 지도의 물리적 장소 13개는 모두 지역 지도에도 있으며, 숙소 두 곳은 날짜마다 다시 반복된다.
- Girona는 이미 세 지역 원본 간 드리프트가 발생했다.
- Day 12–24는 구형·Phase4 PNG가 나란히 있어 빌드 규칙을 모르면 정본을 오인할 수 있다.
- `private=true`가 데이터 노출을 막지 않는다. 현재 UI와 전체 일정 URL은 좌표를 사용할 수 있고 다른 생성 산출물은 정확 주소를 직접 포함한다.
- 공개 사이트를 고쳐도 공개 저장소 원본과 Git 기록은 별도 대응이 필요하다.

## 5. Phase 0 상세 실행계획과 상태

| 단계 | 작업 | 상태 | 증거 |
|---|---|---|---|
| P0-1 | 브랜치·작업 트리·전체 파일 기준선 | 완료 | 최초 명령 결과와 `/tmp` 목록 |
| P0-2 | Leaflet·OSM·Google Maps·GeoJSON·KML 참조 검색 | 완료 | `/tmp/map-references.txt` |
| P0-3 | 지역·일자·정적·런타임 자산 분류 | 완료 | `map-inventory.csv` |
| P0-4 | 빌드 후 실제 페이지 연결 역추적 | 완료 | `page-map-matrix.csv` |
| P0-5 | 이름·ID·좌표·원본 드리프트 분석 | 완료 | `duplicate-place-report.csv` |
| P0-6 | 개인정보·fallback·모드·성능·가드 위험 분석 | 완료 | 이 문서의 발견된 문제 |
| P0-7 | 두 파일럿 범위와 합격 조건 설계 | 완료 | `pilot-design.md` |
| P0-8 | 사용자 승인 | 대기 | 승인 전 Phase 1·전체 변환 금지 |

## 6. 변경 예상 파일 목록

Phase 0에서 실제로 추가한 파일은 위의 5개 문서뿐이다. 승인 후 예상 변경은 다음과 같다.

### Phase 1 — 데이터와 개인정보

- `source/ASSETS/maps/place-registry.json`
- `source/ASSETS/maps/daily-routes.json`
- `source/ASSETS/maps/region-groups.json`
- `source/ASSETS/maps/map-schema.json`
- `scripts/validate_map_data.py`
- `build/build.py`
- `source/ASSETS/91_Place_Registry_v1.0.md` 또는 그 역할을 대체하는 안내
- Bàscara 정확 주소가 있는 CURRENT 챕터·운영 문서·지도 자산·트래커 원본

### Phase 2·파일럿 — 공통 UI

- `build/assets/google-map-loader.js`
- `build/assets/google-map.js`
- `build/assets/google-map.css`
- `build/assets/service-worker.js`
- `.github/workflows/pages.yml`
- 표준 라이브러리만 쓰는 URL·필터·privacy·fallback 단위 테스트

### 후속 단계

- `README.md`, `CLAUDE.md`
- `docs/google-maps-migration/{README,architecture,data-model,api-key-setup,privacy-policy,migration-report,testing-report,rollback-plan}.md`
- 검증 후 `source/ARCHIVE/legacy-maps/`로 이동할 Leaflet·구형 지도 자산

43개 `site/daily/day-NN.html`은 직접 편집하지 않고 `build/build.py`가 계속 생성한다.
