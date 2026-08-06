# Batch 2 (Provence·Lyon) 사진 QA 보고서

작성일: 2026-08-06  
범위: Day 12–27, Aix·Luberon·Avignon·Lyon 4개 챕터의 place dossier·카드, 사진 크레딧

## 결과 요약

- 신규 승인: 원본 38장 (aix 9 · luberon 8 · avignon 9 · lyon 12) → 누적 78장, 파생본 245개
- 라이선스 (누적 78장): CC BY-SA 55 · CC BY 16 · Public Domain 6 · CC0 1
- 챕터 07–10 place 카드 23곳을 CARD_PLACE_SLUGS에 연결 — 카드 썸네일 렌더
- 라이선스 필드 누락·private 참조·중복 이미지: 모두 0
- Marseille·Mucem: 최신 일정에서 supporting/reference → 지시서 원칙대로 이번 배치 제외

## 선정 방식

- 4개 병렬 조사로 후보를 모으고 라이선스·작가를 Commons API로 검증, 전 선정본 38장을
  썸네일 대조 시트로 직접 검수했다.
- **계절 교체 1건**: lake-annecy — 최초 선정본이 설산·늦가을 풍경이라 9월 말 방문과 어긋나
  여름 촬영본(`Lac Annecy été.JPG`)으로 교체. 세낭크 수도원도 만개 라벤더 사진을 피하고
  9월에 실제로 보게 될 초록 라벤더 밭 사진을 채택했다.
- 시각 중복 방지: 아비뇽(도시 hero/궁전 정면/다리), 안시(운하 hero/티우/호수/구시가),
  리옹(도시 hero/대성당 건물)을 서로 다른 구도로 강제했다.

## 파생본 생성 정책 변경 (용량 절감)

hero 변형(800/1280/1920)은 **hero 역할·지역 hero 이미지에만** 생성한다. major·supporting은
day 갤러리·카드·dossier에서 thumbnail/content로만 렌더되므로 hero 변형이 사용되지 않았다.
이 변경으로 파생본 총량이 54.6MB → **31.8MB**로 줄어 지시서 목표(35–50MB) 안에 들어왔다.
극단적 고디테일 프레임(aix-city 항공샷)은 품질 하한에서도 450KB를 넘겨 1920 변형을 생략하고
1280까지 제공한다.

## 용량과 성능

| 항목 | 결과 |
|---|---:|
| 배포 파생본 합계 (누적 78장) | 31,767,200 bytes |
| Hero 평균 | 185,391 bytes (기준 400KB) |
| Content 평균 | 169,501 bytes (기준 250KB) |
| Thumbnail 평균 | 26,233 bytes (기준 60KB) |
| Batch 2 원본 (4000px 축소 저장) | 150.8MB → 원본 누적 294.6MB |
| 빌드 사이트 | 82,320,878 bytes (사진 31.8MB + Daily Action Map PNG ~42MB) |
| PWA 전체 저장 | 731개 파일 · 78.4 MiB |

Day 12–27 초기 전송 추정치(HTML+공통 CSS/JS+eager hero): 466KB–732KB, 전부 기준 2MB 이하.
최대는 Day 12(732KB).

## 자동 검사

- `python3 build/build.py`: 328 HTML, 전체 가드 통과
- `python3 build/image_check.py`: 78 originals · 245 derivatives · errors 0
- `python3 scripts/validate_image_licenses.py`: 78장, 누락 0 · private 0
- `python3 scripts/detect_duplicate_images.py`: exact/near duplicate 0
- `python3 scripts/generate_photo_credits.py --check`: manifest 일치
- `python3 build/pwa_check.py`: 731개 파일 · 78.4 MiB 전체 저장·오프라인 심층 탐색 통과
- `python3 build/hig_check.py`: 19쪽 × 2폭 × 라이트/다크 전부 통과

## 화면 검수

- [Day 18 desktop](screenshots/day-18-desktop.png) — Gordes hero·Luberon 갤러리
- [Day 21 mobile](screenshots/day-21-mobile.png) — Palais des Papes hero + 갤러리 3장
- [Day 27 mobile](screenshots/day-27-mobile.png) — Annecy hero + 갤러리
- [Avignon places desktop](screenshots/avignon-places-desktop.png) — 카드 썸네일

## 남은 결정 (Batch 3 Paris 전)

- **PWA 전체 저장 78.4 MiB.** 사진 몫은 31.8MB이고 Daily Action Map PNG가 ~42MB를 차지한다.
  Paris 배치(+~28장, 예상 +10–12MB)를 넣으면 ~90 MiB. 전체 저장 유지 결정은 "Paris 전 재검토"
  조건부였으므로, Batch 3 전에 (a) 지역별 오프라인 묶음, (b) Daily Action Map PNG 경량화,
  (c) 현행 유지 중 선택이 필요하다.
- 원본 누적 294.6MB — Git LFS 분리 여부 계속 열려 있음.
