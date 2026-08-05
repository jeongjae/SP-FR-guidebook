# Barcelona 사진 Pilot QA 보고서

작성일: 2026-08-05  
범위: Day 1–4, Barcelona 지역 허브·관련 주제 페이지, 사진 크레딧

## 결과 요약

- 43일 인벤토리: 43일, 159개 날짜-장소 행, 142개 고유 장소, 공개 사진 필요 장소 132개
- Pilot 승인: 원본 13장, 반응형 파생본 60개
- 라이선스: CC BY 3장, CC BY-SA 9장, Public Domain 1장
- 라이선스 필드 누락·private place 참조·중복 이미지: 모두 0
- 한국어 alt, caption, 크레딧 앵커, width/height, lazy/eager 정책: 모두 통과
- 비공개 Bàscara 숙소: 주소·좌표·지도 링크를 공개 HTML·지도·콘텐츠 모델에서 제외

## 용량과 성능

| 항목 | 결과 |
|---|---:|
| 승인 원본 합계 | 62,536,399 bytes |
| 배포 파생본 합계 | 6,450,702 bytes |
| Hero 평균 | 129,309 bytes |
| Content 평균 | 136,584 bytes |
| Thumbnail 평균 | 21,430 bytes |
| 빌드 사이트 | 20,266,671 bytes |
| 작업 전 사이트 | 14,880,426 bytes |
| 순증가 | 5,386,245 bytes |
| PWA 전체 저장 | 497개 파일 · 19.3 MiB |

대표 일자 초기 전송 추정치는 공통 CSS/JS, HTML, eager hero만 합산했다.

| 페이지 | 추정 초기 전송량 |
|---|---:|
| Day 1 | 578,841 bytes |
| Day 2 | 478,010 bytes |
| Day 3 | 501,782 bytes |
| Day 4 | 510,012 bytes |

네 페이지 모두 2MB 기준 이하이며, 원본은 사이트와 PWA에 포함하지 않는다.

## 자동 검사

- `python3 build/build.py`: 315 HTML, 전체 Phase 1–10·링크·날짜·장소 가드 통과
- `python3 build/image_check.py`: 원본/파생/배포/HTML/개인정보/초기 전송량 통과
- `python3 scripts/validate_image_licenses.py`: 13장, 누락 0, private 0
- `python3 scripts/detect_duplicate_images.py`: exact/near duplicate 0
- `python3 scripts/generate_photo_credits.py --check`: manifest 일치
- `python3 scripts/validate_media.py`: 호환 계층 16장 통과
- `python3 build/pwa_check.py`: 전체 저장과 오프라인 심층 탐색 통과
- `python3 build/hig_check.py`: 19쪽 × 2폭 × 라이트/다크에서 터치타깃·글자·명암비·안전영역·리플로·뷰포트 통과

## 화면 검수

- [Day 1 desktop](screenshots/day-01-desktop.png)
- [Day 3 mobile](screenshots/day-03-mobile.png)
- [Barcelona region desktop](screenshots/barcelona-region-desktop.png)
- [Photo credits mobile](screenshots/photo-credits-mobile.png)

Hero의 대표성, 모바일 크롭, caption/credit 가독성, 하단 내비게이션과의 간섭을 확인했다. Day 3 모바일에서 hero 아래 보조 사진이 지연 로드되고, 데스크톱 지역 허브에서는 Sagrada Família가 지역 대표 이미지로 한 번만 사용된다.

## 후속 Batch 전 판단

전체 132개 공개 사진 필요 장소를 같은 방식으로 확장하면 원본 저장소 크기가 빠르게 증가한다. 다음 지역 Batch를 시작하기 전에 원본을 Git LFS 또는 별도 보관소로 분리하고, PWA의 지역별 오프라인 묶음을 도입할지 결정한다. 이번 Pilot은 Barcelona 13장까지만 승인·배포하며 나머지 43일 사진 수집은 수행하지 않는다.
