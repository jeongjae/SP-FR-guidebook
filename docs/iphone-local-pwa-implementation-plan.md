# iPhone 로컬 PWA 구현 계획

- 작성일: 2026-08-04
- 상태: 구현 전 계획
- 대상: 2026 유럽 여행 가이드북 정적 웹사이트

## 1. 목표

기존 가이드북을 별도 네이티브 앱이나 App Store 배포 없이 다음 형태로 확장한다.

- GitHub Pages의 HTTPS 주소에서 iPhone 홈 화면에 설치한다.
- Safari UI 없이 독립 앱처럼 실행한다.
- 전체 가이드북을 iPhone에 저장해 비행기 모드에서도 열람한다.
- 온라인일 때는 최신 예약·일정 정보를 우선 표시한다.
- 기존 PC 브라우저, 같은 Wi-Fi 접속, `file://` 직접 열람 방식도 유지한다.

이 문서에서 **로컬 PWA**는 GitHub Pages에서 한 번 설치한 뒤 콘텐츠를 기기 내부에
저장하는 방식을 뜻한다. Service Worker는 `file://`이나 iPhone에서 접속한 PC의
일반 `http://<IP>` 주소에서는 동작하지 않으므로 PWA 설치 경로는 GitHub Pages의
HTTPS 주소로 한정한다.

## 2. 현재 기준선

- 프레임워크 없는 Python 정적 사이트 생성 방식이다.
- `site/`는 빌드 산출물이므로 직접 편집하지 않는다.
- 런타임 서드파티 의존성은 0개이며 이 원칙을 유지한다.
- 현재 산출물은 HTML 313개를 포함한 총 436개 파일, 약 13.9 MiB다.
- 본문, 검색 데이터, 폰트, 대표 이미지, Leaflet 라이브러리는 로컬 자산이다.
- Google Maps와 OpenStreetMap 배경 타일은 네트워크가 필요하다.
- 기존 `build/hig_check.py`가 터치 타깃, 글자 크기, 명암비, 안전영역,
  320 px 리플로와 뷰포트를 검사한다.

## 3. 범위

### 포함

- Web App Manifest와 iPhone 홈 화면 아이콘
- Service Worker 등록과 버전 관리
- 핵심 화면 자동 캐시
- 전체 가이드북 수동 다운로드와 진행 상태
- 오프라인 탐색과 명확한 실패 화면
- 새 배포 버전의 안전한 업데이트
- 자동 검증, iPhone 실기기 검수, 사용 안내

### 제외

- App Store용 네이티브 앱 또는 IPA
- Web Push, 백그라운드 동기화, 로그인
- OpenStreetMap 타일의 자체 오프라인 배포
- 외부 Google Maps 및 기타 제3자 응답의 캐시
- PWA만을 위한 런타임 패키지나 프레임워크 추가

## 4. 설계 원칙

1. **정본에서 생성한다.** PWA 파일과 공통 `<head>`는 `build/`에서 생성한다.
2. **점진적 향상이다.** Service Worker를 지원하지 않거나 `file://`로 열어도 기존
   사이트 기능이 유지되어야 한다.
3. **최신 운영 정보를 우선한다.** 온라인에서는 HTML을 네트워크에서 먼저 확인한다.
4. **완료를 과장하지 않는다.** 모든 파일이 검증되기 전에는 오프라인 준비 완료로
   표시하지 않는다.
5. **업데이트 실패가 기존 사본을 파괴하지 않는다.** 새 전체 패키지가 완성된 뒤에만
   이전 패키지를 제거한다.
6. **같은 출처의 공개 자산만 저장한다.** 외부 요청과 비공개 숙소 정보는 캐시 대상에
   추가하지 않는다.

## 5. 단계별 구현

### 단계 1. PWA 메타데이터와 아이콘

`build/build.py`의 공통 페이지 템플릿에 다음을 추가한다.

- `manifest.webmanifest` 링크
- `apple-touch-icon` 180×180
- `apple-mobile-web-app-capable=yes`
- `apple-mobile-web-app-title`
- 라이트·다크 모드별 `theme-color`

Manifest에는 다음 필드를 둔다.

- `id`, `name`, `short_name`, `description`
- `start_url: "./index.html"`
- `scope: "./"`
- `display: "standalone"`
- `lang: "ko"`
- `background_color`, `theme_color`
- 192×192, 512×512 일반 아이콘
- 안전 여백을 둔 512×512 마스커블 아이콘

아이콘 원본은 `source/ASSETS/pwa/`에 두고 빌드가 `site/assets/pwa/`로 복사한다.
화면 방향은 본문과 지도 모두를 고려해 잠그지 않는다. iOS 시작 화면 이미지는 기기별
규격이 많고 핵심 기능이 아니므로 1차 범위에서 제외한다.

### 단계 2. 빌드 기반 오프라인 파일 목록

모든 콘텐츠 생성이 끝난 뒤 빌드가 `site/`를 열거해 다음 파일을 만든다.

- `site/offline-files.json`
  - 배포 상대경로
  - 파일 크기
  - SHA-256
  - 총 파일 수와 총용량
  - 전체 콘텐츠 버전 해시
- `site/sw.js`
  - 버전 해시가 삽입된 Service Worker
- `site/offline-fallback.html`
  - 아직 저장하지 않은 심층 페이지의 명시적 오프라인 오류 화면

자기 참조를 피하기 위해 `sw.js`, `offline-files.json`, 배포 단계에서 추가되는
`.nojekyll`은 전체 콘텐츠 해시 대상에서 제외한다. 파일 목록은 항상 상대경로로
만들어 `/SP-FR-guidebook/` 같은 GitHub Pages 프로젝트 경로를 하드코딩하지 않는다.

### 단계 3. 2단계 캐시

436개 파일을 Service Worker 설치 이벤트에서 한꺼번에 `cache.addAll()`로 저장하지
않는다. 일부 요청 실패로 설치 전체가 깨지는 것을 피하기 위해 다음처럼 나눈다.

#### 핵심 캐시: 자동 설치

- 홈
- 전체 일정, 지역, 데일리 목록
- 비상·오프라인 준비 화면
- CSS, 내비게이션 JS, PWA JS, 검색 데이터
- 로컬 폰트와 앱 아이콘
- 오프라인 실패 화면

#### 전체 캐시: 사용자 실행

- 사용자가 `전체 가이드북 저장`을 누르면 `offline-files.json`을 읽는다.
- 작은 배치 또는 순차 요청으로 전체 파일을 저장한다.
- 완료 파일 수, 전체 파일 수, 내려받은 용량을 화면에 보고한다.
- 중단된 다운로드는 이미 검증된 항목을 재사용해 이어받는다.
- 각 응답 성공과 최종 파일 수를 확인한 뒤에만 완료 상태를 기록한다.

### 단계 4. 요청별 캐시 정책

| 요청 | 정책 | 이유 |
|---|---|---|
| 같은 출처 HTML 탐색 | Network first, 실패 시 정확한 캐시, 마지막으로 fallback | 온라인에서는 최신 예약·일정을 우선한다. |
| CSS·JS·폰트·이미지 | Cache first + 백그라운드 갱신 | 오프라인 성능과 새 자산 반영을 함께 확보한다. |
| Manifest·오프라인 목록 | Network first | 새 배포 버전을 빠르게 감지한다. |
| Google Maps·외부 링크 | 캐시하지 않음 | 외부 응답, 라이선스와 실패 상태를 통제할 수 없다. |
| OSM 배경 타일 | 캐시하지 않음 | 자체 오프라인 지도 범위가 아니다. |

Service Worker는 자신의 scope 안에 있는 같은 출처의 `GET` 요청만 처리한다. 기존
`navigator.onLine` 기반 외부 링크 안내는 그대로 유지한다.

### 단계 5. 설치·저장·업데이트 화면

기존 `maps/offline.html`을 **오프라인 준비** 허브로 확장하고 Organic Maps 안내는
그 안의 독립 섹션으로 유지한다. 홈의 `비상 · 오프라인` 링크와 꼬리말 링크는 이
페이지를 계속 가리킨다.

화면에는 다음을 제공한다.

- iPhone 설치 절차
  1. Safari에서 GitHub Pages 열기
  2. 공유 메뉴 열기
  3. 홈 화면에 추가
  4. `웹 앱으로 열기` 활성화
- 현재 실행 모드: Safari / 홈 화면 앱
- 전체 가이드북 저장 버튼
- `저장 전 / 저장 중 / 완료 / 업데이트 필요 / 실패` 상태
- 파일 수, 전체 용량, 진행률
- 저장된 버전과 저장 시각
- 재시도, 업데이트, 로컬 데이터 삭제
- `navigator.storage.estimate()` 기반 저장소 사용량
- 완료 후 `navigator.storage.persist()` 요청과 결과

iOS에서는 일반 브라우저의 설치 프롬프트를 전제로 하지 않는다. 실제 홈 화면 추가
절차를 안내하고 `display-mode: standalone`과 `navigator.standalone`으로 설치 실행
상태를 판별한다.

PWA 로직은 `build/assets/pwa.js`에 분리한다. 기존 `nav.js`는 검색, 오늘 버튼,
온라인 상태와 내비게이션만 담당한다.

### 단계 6. 안전한 업데이트

- 콘텐츠 해시로 버전별 핵심 캐시와 전체 캐시 이름을 만든다.
- 새 Service Worker 발견 시 `새 버전 사용 가능` 상태를 표시한다.
- 사용자가 업데이트를 선택하면 새 캐시에 먼저 다운로드한다.
- 새 전체 패키지가 완성되기 전에는 기존 완료 캐시를 삭제하지 않는다.
- 활성화 후 한 차례만 페이지를 새로고침한다.
- 실패 시 기존 패키지와 저장 완료 상태를 유지하고 재시도 경로를 제공한다.
- 온라인 HTML은 항상 network first이므로 전체 재다운로드 전에도 최신 화면을 볼 수
  있다. 오프라인 사본이 이전 버전이면 그 사실을 화면에 표시한다.

## 6. 예상 변경 파일

| 경로 | 변경 내용 |
|---|---|
| `build/build.py` | 공통 PWA head, 아이콘 복사, Manifest·목록·Service Worker 생성 |
| `build/assets/pwa.js` | 등록, 설치 안내, 전체 다운로드, 상태·업데이트 제어 |
| `build/assets/service-worker.js` | Service Worker 템플릿과 캐시 정책 |
| `build/assets/style.css` | 설치·저장 상태 UI와 standalone 안전영역 |
| `source/ASSETS/pwa/*` | 앱 아이콘 원본과 파생 규격 |
| `build/pwa_check.py` | Manifest, 파일 목록, HTTP 오프라인 동작 검사 |
| `build/hig_check.py` | 오프라인 준비 UI를 표본 또는 전체 검사에 포함 |
| `.github/workflows/pages.yml` | 배포 전 PWA 검사 단계 추가 |
| `README.md` | iPhone 설치, 업데이트, 오프라인 확인 절차 정정 |

`site/` 아래 파일은 위 빌드 과정의 결과로만 생성한다.

## 7. 자동 검증

`build/pwa_check.py`는 임시 로컬 HTTP 서버와 기존 Playwright 환경을 사용해 다음을
검사한다.

- Manifest 필수 필드와 상대경로
- 모든 아이콘의 존재, MIME과 PNG 실제 크기
- Service Worker가 사이트 루트에 생성되는지
- 오프라인 목록과 실제 `site/` 파일 간 누락·중복
- 파일 크기와 SHA-256 일치
- 외부 URL이 사전 캐시 목록에 없는지
- localhost에서 Service Worker 등록 성공
- 전체 저장 후 브라우저를 offline으로 전환
- 홈, 데일리 심층 페이지, 지역, 트래커, 검색, 로컬 Leaflet 지도 열람
- 저장되지 않은 경로에서 명시적 fallback 표시
- 중단된 다운로드가 완료로 기록되지 않는지

필수 검증 명령은 다음과 같다.

```bash
python3 build/build.py
python3 build/pwa_check.py
python3 build/hig_check.py --all
```

GitHub Actions 배포 작업에도 `pwa_check.py`를 필수 게이트로 추가한다.

## 8. iPhone 실기기 검수

지원 기준은 우선 iOS 17 이상, 최신 iOS 26을 주 대상으로 하고 착수 시 실제 여행에
사용할 iPhone 모델과 iOS 버전을 확정한다.

| 시나리오 | 확인 내용 |
|---|---|
| Safari 온라인 | 기존 사이트 탐색과 외부 링크가 정상이다. |
| 홈 화면 추가 | 앱 이름과 아이콘이 정확하고 standalone으로 열린다. |
| 전체 저장 | 약 14 MiB 저장이 끝나고 버전·시각·완료 상태가 표시된다. |
| 비행기 모드 | 홈, 일정, 데일리, 지역, 트래커, 검색과 로컬 지도 목록이 열린다. |
| 강제 종료 후 오프라인 실행 | 네트워크 오류 화면 대신 저장된 홈이 열린다. |
| iPhone 재시작 후 실행 | 저장 상태와 오프라인 열람이 유지된다. |
| 다운로드 중단 | 완료로 오인하지 않으며 다시 이어받을 수 있다. |
| 새 배포 버전 | 업데이트 안내가 나오고 실패 시 이전 패키지가 유지된다. |
| 외부 지도 | 연결 필요 상태가 명확하며 OSM 타일을 오프라인으로 오인하지 않는다. |
| 기존 방식 | PC, 모바일 브라우저, `file://` 열람이 깨지지 않는다. |

## 9. 완료 조건

- GitHub Pages에서 iPhone 홈 화면 추가가 된다.
- 앱 아이콘 실행 시 Safari 주소창이 없는 독립 화면으로 열린다.
- 전체 가이드북 저장 상태를 사용자가 확인할 수 있다.
- 앱 강제 종료 후 비행기 모드에서도 주요 경로가 열린다.
- 전체 저장 대상 내부 링크에 누락이 없다.
- 업데이트 실패가 기존 오프라인 패키지를 삭제하지 않는다.
- 외부 요청은 오프라인 캐시에 들어가지 않는다.
- 기존 정적 사이트와 JavaScript 없는 기본 탐색이 유지된다.
- 전체 빌드 검사, PWA 검사와 HIG 전체 검사가 통과한다.
- 실제 여행용 iPhone에서 출발 전 최종 오프라인 점검을 마친다.

## 10. 위험과 대응

| 위험 | 대응 |
|---|---|
| iOS가 저장 공간 압박이나 장기간 미사용으로 데이터를 제거 | 앱에 저장 상태를 표시하고 출발 전 재확인 절차를 README와 화면에 둔다. |
| 436개 요청 중 일부 실패 | 핵심·전체 캐시를 분리하고 배치 저장, 재시도와 최종 검증을 사용한다. |
| GitHub Pages 프로젝트 하위 경로에서 scope 오류 | `sw.js`는 사이트 루트에 두고 모든 URL을 scope 상대경로로 생성한다. |
| 최신 예약 정보와 오프라인 구버전 충돌 | HTML network first, 캐시 버전과 저장 시각 표시, 명시적 업데이트를 사용한다. |
| 자체 지도가 완전 오프라인이라는 오해 | OSM 타일은 제외하고 Organic Maps 역할을 같은 화면에서 구분한다. |
| PWA 실패가 기존 열람을 막음 | 프로토콜·기능 감지 후 등록하고 모든 기능을 점진적 향상으로 구현한다. |

## 11. 일정 추정

| 단계 | 예상 소요 |
|---|---:|
| Manifest·아이콘·공통 head | 0.5일 |
| 파일 목록·Service Worker·캐시 버전 | 1일 |
| 설치·전체 저장·업데이트 UI | 1일 |
| 자동 검사와 오류 보완 | 1일 |
| 실기기 QA·문서·배포 확인 | 0.5일 |
| **합계** | **3.5~4일** |

## 12. 참고 자료

- [Apple: iPhone 홈 화면에 웹사이트 추가](https://support.apple.com/guide/iphone/bookmark-a-website-iph42ab2f3a7/ios)
- [WebKit: Safari 26의 iOS·iPadOS 웹 앱 동작](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/)
- [WebKit: iOS 홈 화면 웹 앱과 Manifest·아이콘](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/)
- [WebKit: 저장 공간과 데이터 제거 정책](https://webkit.org/blog/14403/updates-to-storage-policy/)
