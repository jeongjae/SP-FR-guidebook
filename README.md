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

### 오프라인으로 보기 (여행 중)

`site/` 폴더를 통째로 휴대폰·태블릿에 복사한 뒤 `index.html`을 브라우저로 열면 된다.
본문·트래커·지도 마커와 경로 목록은 완전 오프라인으로 동작하며,
지도 배경 타일(OpenStreetMap)만 인터넷 연결 시 표시된다.

## 다시 빌드하기

원본 MD나 트래커를 수정한 뒤:

```bash
pip install markdown openpyxl   # 최초 1회
python3 build/build.py
```

빌드는 내부 링크 무결성 검사를 포함하며, `site/`를 전부 새로 생성한다.

## 콘텐츠 기준

- 리더 에디션은 통합 패키지 v1.24의 `40_Master_Guidebook`(Nice 5박·Aix 4박 반영 최신본) 기준.
- 구버전·작업문서는 사이트에 포함하지 않는다 (`37_Source_of_Truth_and_Supersession_Matrix_v1.1` 기준).
