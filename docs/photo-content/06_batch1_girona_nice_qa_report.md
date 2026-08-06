# Batch 1 (Girona·Nice) 사진 QA 보고서

작성일: 2026-08-06  
범위: Day 4–11, Girona·Nice 지역 허브·place dossier·food 페이지, 사진 크레딧

## 결과 요약

- 신규 승인: 원본 27장 (girona 10 · nice 16 · barcelona 1), 반응형 파생본 134개
- 누적 manifest: 원본 40장 · 파생본 194개 (Pilot 13장 포함)
- 라이선스 (누적 40장): CC BY-SA 29 · CC BY 6 · Public Domain 5 · CC0 0
- 레거시 media-catalog의 girona·nice 16장 중 15장을 manifest로 이관, 렌더 파이프라인을 barcelona와 동일하게 통일 (한 페이지 한 파이프라인)
- 라이선스 필드 누락·private place 참조·중복 이미지: 모두 0
- 한국어 alt·caption·크레딧 앵커·width/height·lazy/eager 정책: 전부 통과

## 원본 보관 정책 (이번 배치부터)

신규 다운로드 원본은 최장변 4000px로 축소 저장한다 (`download_images.py --max-side 4000`).
Commons 원치수는 manifest `originalWidth/Height`에, 저장본 치수는 `storedWidth/Height`에 기록되고,
진짜 원본은 `originalFile` URL로 항상 재취득 가능하다. Pilot의 기존 13장은 손대지 않았다.

- 신규 원본 27장 합계: 81.3MB (장당 평균 약 3.0MB — 축소 전 추정 대비 약 40% 절감)
- 원본 폴더 합계: 143,820,962 bytes (Pilot 62.5MB 포함)

## 선정 방식

- 레거시 카탈로그에 이미 검증돼 있던 파일은 원칙적으로 유지하고, Commons API로 라이선스·작가를 재검증했다.
- 신규 장소는 후보 3개씩 조사해 라이선스(PD/CC0/CC BY/CC BY-SA + 작가 명시)와 해상도를 확인하고, 썸네일을 직접 열어 대표성·구도·워터마크·인물 노출을 검수한 뒤 선정했다.
- 교체 1건: Collioure — 레거시 원본이 1024px로 기준 미달이라 동일 구도의 4264px CC BY-SA 3.0 파일로 교체.
- 채택 1건: Monaco — 레거시 4:1 파노라마는 세로 크롭이 불가능해 2:1 신규 파노라마 채택.

## 제외 (기술하지 않은 것)

| 대상 | 사유 |
|---|---|
| marche-de-la-liberation | Commons에 시장이 실제 운영 중인 모습을 담은 허용 라이선스 사진이 없음. 광장만 나온 사진에 시장 캡션을 붙이는 것은 규칙 위반이라 text-only 유지 |
| girona-city-walls | 이동일(Day 4)에 사진 6장이 몰려 보조 사진을 감축. 성벽은 다른 게재면이 없어 이번 배치 제외 |

## 용량과 성능

| 항목 | 결과 |
|---|---:|
| 배포 파생본 합계 (누적) | 23,418,860 bytes |
| 파생본 순증가 | +16,968,158 bytes |
| Hero 평균 | 146,436 bytes (기준 400KB) |
| Content 평균 | 145,817 bytes (기준 250KB) |
| Thumbnail 평균 | 22,310 bytes (기준 60KB) |
| 빌드 사이트 | 49,810,826 bytes |
| PWA 전체 저장 | 650개 파일 · 47.4 MiB |

대표 일자 초기 전송 추정치 (HTML + 공통 CSS/JS + eager hero만 합산, 기준 2MB):

| 페이지 | 추정 초기 전송량 |
|---|---:|
| Day 4 | 516,639 bytes |
| Day 5 | 481,539 bytes |
| Day 6 | 471,429 bytes |
| Day 7 | 500,853 bytes |
| Day 8 | 521,614 bytes |
| Day 9 | 438,554 bytes |
| Day 10 | 585,246 bytes |
| Day 11 | 417,793 bytes |

## 자동 검사

- `python3 build/build.py`: 328 HTML, Phase 1–10·링크·날짜·장소 가드 전부 통과
- `python3 build/image_check.py`: 40 originals · 194 derivatives · errors 0
- `python3 scripts/validate_image_licenses.py`: 40장, 누락 0 · private 0
- `python3 scripts/detect_duplicate_images.py`: exact/near duplicate 0
- `python3 scripts/generate_photo_credits.py --check`: manifest 일치
- `python3 scripts/validate_media.py`: 레거시 호환 계층 0장 (barcelona·girona·nice 전부 manifest로 이관)
- `python3 build/pwa_check.py`: 전체 저장·오프라인 심층 탐색 통과
- `python3 build/hig_check.py`: 19쪽 × 2폭 × 라이트/다크 — 터치타깃·글자·명암비·안전영역·리플로·뷰포트 통과

## 화면 검수

- [Day 6 desktop](screenshots/day-06-desktop.png) — Tossa 야간 hero·Costa Brava 갤러리
- [Day 10 mobile](screenshots/day-10-mobile.png) — Monaco hero + 갤러리 4장, 캡션·크레딧 가독성
- [Girona region desktop](screenshots/girona-region-desktop.png) — Onyar 지역 hero
- [Nice region desktop](screenshots/nice-region-desktop.png) — 성채 언덕 파노라마 지역 hero
- [Photo credits mobile](screenshots/photo-credits-batch1-mobile.png)

## 후속 Batch 전 판단

- PWA 전체 저장이 27.7 → 47.4 MiB로 늘었다. Batch 2(Provence~Lyon, +35~45장)를 같은 방식으로 넣으면
  약 65–70 MiB에 도달한다. **Batch 2 전에 지역별 오프라인 묶음(현 지역만 선캐시) 도입을 결정해야 한다.**
- 원본 저장소 누적 143.8MB. 4000px 정책으로 증가 속도는 절반 이하가 됐지만, Batch 3(Paris) 이후 ~250MB에
  도달하므로 Git LFS 분리 여부는 여전히 열려 있다.
