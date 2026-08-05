# SP-FR-guidebook

Barcelona to Paris through Côte d'Azur and Provence

**Jason과 Julia의 2026 유럽 장기여행 가이드북** (2026-08-29 ~ 2026-10-10 · 43일)을
PC와 모바일 브라우저에서 조회할 수 있는 로컬 웹사이트.

```text
Barcelona 3박 → Bàscara 3박 → Nice 5박 → Aix 4박
→ Luberon 4박 → Avignon 4박 → Lyon 4박 → Paris 15박
```

## 구성

| 경로 | 내용 |
|---|---|
| `site/` | **빌드된 정적 웹사이트** — 이 폴더만 있으면 열람 가능 |
| `source/40_Master_Guidebook/` | 리더 에디션 원본 MD 11챕터 + 마스터 인덱스 |
| `source/maps/` | Nice·Lyon 실행지도 원본 HTML (Leaflet) |
| `source/TP_Europe_Travel_Master_Tracker_v1.1.xlsx` | 마스터 트래커 원본 |
| `build/build.py` | MD·xlsx → 정적 HTML 빌드 스크립트 |
| `serve.sh` / `serve.bat` | 로컬 서버 실행 스크립트 |

사이트에는 가이드북 11챕터, 실행지도 2종(Leaflet 로컬 번들), 트래커 5개 시트
(일정·예약·이동·숙소·대시보드)가 포함된다.

## 사용법

### 웹으로 보기 (GitHub Pages)

어느 기기에서든 브라우저로 접속: **<https://jeongjae.github.io/SP-FR-guidebook/>**

`gh-pages` 브랜치에서 서빙되며, `main`에 원본·빌드 변경이 푸시되면
`.github/workflows/pages.yml`이 자동으로 다시 빌드·배포한다.

### PC에서 보기

```bash
./serve.sh          # macOS·Linux (기본 포트 8000)
serve.bat           # Windows
```

실행 후 브라우저에서 <http://localhost:8000> 접속.
서버 없이 `site/index.html`을 브라우저로 직접 열어도 동작한다.

### 모바일에서 보기 (같은 Wi-Fi)

1. PC에서 `serve.sh`(또는 `serve.bat`) 실행 — 시작 메시지에 PC의 IP 주소가 표시된다.
2. 휴대폰 브라우저에서 `http://<PC IP 주소>:8000` 접속.
   - IP 확인: macOS `ipconfig getifaddr en0` / Windows `ipconfig` (IPv4 주소) / Linux `hostname -I`
3. 접속이 안 되면 PC 방화벽에서 8000 포트 허용 여부와 두 기기가 같은 네트워크인지 확인.

이 주소는 일반 HTTP이므로 모바일 열람용이다. iPhone 홈 화면 앱 설치와 전체
오프라인 저장은 아래 GitHub Pages HTTPS 주소에서 진행한다.

### iPhone에 앱으로 설치하고 오프라인 저장

1. iPhone의 Safari에서 <https://jeongjae.github.io/SP-FR-guidebook/>를 연다.
2. 공유 메뉴에서 **홈 화면에 추가**를 선택하고, 표시되면 **웹 앱으로 열기**를 켠다.
3. 홈 화면의 **유럽 가이드북** 아이콘으로 다시 연다.
4. **비상 · 오프라인 → 전체 가이드북 저장**을 누르고 완료 상태와 저장 시각을 확인한다.
5. 출발 전에 앱을 강제 종료한 뒤 비행기 모드에서 홈·일정·지역·트래커가 열리는지 확인한다.

전체 가이드북은 약 14 MiB다. iOS는 저장 공간이 부족하거나 앱을 오래 사용하지 않으면
웹 데이터를 정리할 수 있으므로 장거리 이동 전 오프라인 준비 화면을 다시 확인한다.
Google Maps 링크와 OpenStreetMap 배경 타일은 저장 대상이 아니며 연결이 필요하다.

### 폴더 사본으로 오프라인 보기

`site/` 폴더를 통째로 휴대폰·태블릿에 복사한 뒤 `index.html`을 브라우저로 열면 된다.
본문·트래커·지도 마커와 경로 목록은 완전 오프라인으로 동작하며,
지도 배경 타일(OpenStreetMap)만 인터넷 연결 시 표시된다.

## 다시 빌드하기

원본 MD나 트래커를 수정한 뒤:

```bash
pip install markdown openpyxl   # 최초 1회
python3 build/build.py
python3 build/pwa_check.py
python3 build/hig_check.py
```

빌드는 내부 링크 무결성 검사를 포함하며, `site/`를 전부 새로 생성한다.

## 날짜별 인터랙티브 실행지도

Day 1–3(2026-08-29~31)은 기존 Barcelona 실행지도와 일정 원고를 결합한
인터랙티브 지도 프로토타입을 제공한다. 새 프레임워크나 런타임 의존성 없이,
이미 로컬 번들된 Leaflet과 OpenStreetMap 타일을 사용한다. 지도 아래에는
터치 가능한 장소 목록과 Google Maps 보기·길찾기 링크가 있고, 기존 세로형
카드 이미지는 접을 수 있는 fallback으로 그대로 남는다.

### 구조

| 경로 | 역할 |
|---|---|
| `source/ASSETS/76_Daily_Execution_Maps/daily-maps.json` | 날짜별 `DailyMapData` 정본 |
| `build/assets/daily-map.js` | 지도·핀·팝업·목록·Google Maps 링크 공통 UI |
| `build/assets/style.css` | 모바일 우선 지도·목록·터치 상태 스타일 |
| `build/build.py` | 데이터 검증, 정적 페이지 삽입, 브라우저용 데이터 생성 |

`DailyMapData`는 `date`, `city`, `title`, `center`, `zoom`, `places[]`,
`routes[]`를 가진다. `Place`는 `id`, `type`, `name`, `lat`, `lng`, `order`,
`plannedTime`, `description`, `googleMapsUrl`, `optional`, `private`,
`approximate`를 가진다. 지원 유형은 `accommodation`, `attraction`,
`restaurant`, `cafe`, `market`, `parking`, `station`, `airport`다.

### 날짜와 장소 추가

1. 일정 원고와 기존 검증 자산에 실제로 있는 장소만 선택한다.
2. `daily-maps.json`의 `days`에 날짜 객체를 하나 추가한다.
3. 장소 `id`는 날짜 안에서 고유하게, `order`는 당일 실행 순서로 둔다.
4. `routes`의 `from`과 `to`에는 같은 날짜의 장소 `id`만 사용한다.
5. `python build/build.py`와 `python build/hig_check.py`를 실행한다. 빌드는
   날짜·필수 필드·좌표 범위·장소 유형·경로 참조·개인정보 규칙을 검사한다.

### Google Maps URL 규칙

- 장소 보기: `https://www.google.com/maps/search/?api=1&query=<장소명>`
- 길찾기: 공통 UI가 `https://www.google.com/maps/dir/?api=1`에 좌표,
  `travelmode`, 필요하면 `origin`과 `waypoints`를 붙여 생성한다.
- 웹사이트의 점선은 방문 순서 개요일 뿐 실제 경로가 아니다. 실제 경로와
  교통상황은 Google Maps에서 다시 계산한다.

### 개인정보 처리

- 호텔·공공 숙박업소 후보는 `optional=true`, 필요하면
  `approximate=true`로 표시하고 예약 확정 전임을 설명한다.
- Airbnb·B&B·개인 숙소는 공개 저장소에 이름이나 정확한 주소를 넣지 않는다.
  `private=true`, `approximate=true`를 함께 사용하고 `googleMapsUrl`은 빈
  문자열로 둔다. 빌드가 이 규칙을 위반한 데이터를 거부한다.
- 실제 예약 확정 후에도 개인 숙소의 정확한 좌표는 공개 데이터에 커밋하지 않는다.

## 콘텐츠 기준

- 리더 에디션은 통합 패키지 v1.24의 `40_Master_Guidebook`(Nice 5박·Aix 4박 반영 최신본) 기준.
- 구버전·작업문서는 사이트에 포함하지 않는다 (`37_Source_of_Truth_and_Supersession_Matrix_v1.1` 기준).
