# Batch 3 (Paris) 사진 QA 보고서

작성일: 2026-08-07  
범위: Day 28–43, Paris 챕터 place dossier·카드, 사진 크레딧. **사진 콘텐츠 최종 배치.**

## 결과 요약

- 신규 승인: 원본 24장 → **누적 102장** (지시서 최종 목표 100–130장 달성), 파생본 325개
- 라이선스 (누적 102장): CC BY-SA 70 · CC BY 25 · Public Domain 6 · CC0 1
- 라이선스 필드 누락·private 참조·중복 이미지: 모두 0
- 챕터 11 place 카드 9곳을 CARD_PLACE_SLUGS에 연결

## 파리 고유 제약의 처리 (기술하지 않은 것 포함)

프랑스에는 파노라마의 자유가 없어, 저작권이 살아 있는 현대 건축·설치물이 주 피사체인 사진은
촬영자의 CC 라이선스로도 건축가의 권리가 해소되지 않는다.

| 대상 | 처리 |
|---|---|
| 필하모니 드 파리 (장 누벨, 2015) | **text-only** — 외관·내부 모두 건축이 주 피사체 |
| 루이비통 재단 (프랭크 게리, 2014) | **text-only** — 동일 사유 |
| 루브르 | 피라미드(I. M. 페이, 1989)가 없는 **쿠르 카레** 구도 채택 |
| 팔레 루아얄 | 뷔렌 기둥(1986)이 프레임에 없는 정원 회랑 구도 채택 |
| 부르스 드 코메르스 | 1889년 로톤다 외관만 — 안도 다다오 내부(2021) 배제 |
| 파리 전경 | 에펠탑 야간 조명(저작권 보호) 회피 — 주간 촬영본만 |
| 오랑주리·튈르리 | 일정 신분 reference(설명 언급) — 지시서 원칙대로 제외 |

노트르담: 2019–2024 공사기(비계·크레인) 사진을 전부 배제. 복원 후 주간 사진은 모두 크레인이
걸려 있어, 화재로 손상되지 않았고 복원 후와 외관이 동일한 **서쪽 파사드의 2013년 촬영본**을
채택했다.

## 용량과 성능

| 항목 | 결과 |
|---|---:|
| 배포 파생본 합계 (누적 102장) | 43,618,918 bytes (목표 35–50MB 내) |
| Hero 평균 | 189,519 bytes (기준 400KB) |
| Content 평균 | 175,712 bytes (기준 250KB) |
| Thumbnail 평균 | 27,101 bytes (기준 60KB) |
| Batch 3 원본 (4000px 축소) | 93.5MB → 원본 누적 388.2MB |
| 빌드 사이트 | 157,326,501 bytes |
| PWA 전체 저장 | 865개 파일 · 149.9 MiB |

Day 28–43 초기 전송 추정치: 최대 757KB (Day 41), 전부 기준 2MB 이하.

고디테일 프레임 예외 처리: 지베르니 content는 품질 하한에서도 300KB를 넘겨 1080px로
단계 축소해 한도 안에 들어왔다 (`process_images.py`의 content 폭 단계 축소).

## 사이트 용량 구성 주의

PWA 전체 저장 149.9 MiB 중 **사진은 43.6MB**다. Daily Action Map PNG(카드 56MB +
데일리 46MB ≈ 102MB)가 대부분을 차지하며 이는 사진 파이프라인 밖의 별도 워크스트림이다.
전체 저장 UX를 유지하려면 **Action Map PNG의 WebP 전환·해상도 조정을 별도 과제로 권고**한다.

## 자동 검사

- `python3 build/build.py`: 328 HTML, 전체 가드 통과
- `python3 build/image_check.py`: 102 originals · 325 derivatives · errors 0
- `python3 scripts/validate_image_licenses.py`: 102장, 누락 0 · private 0
- `python3 scripts/detect_duplicate_images.py`: exact/near duplicate 0
- `python3 scripts/generate_photo_credits.py --check`: manifest 일치
- `python3 build/pwa_check.py`: 865개 파일 · 149.9 MiB 전체 저장·오프라인 심층 탐색 통과
- `python3 build/hig_check.py`: 19쪽 × 2폭 × 라이트/다크 전부 통과

## 화면 검수

- [Day 29 mobile](screenshots/day-29-mobile.png) — 노트르담 hero + 라탱·팡테옹 갤러리
- [Day 36 desktop](screenshots/day-36-desktop.png) — 베르사유 hero + 정원·트리아농
- [Day 41 mobile](screenshots/day-41-mobile.png) — 지베르니 hero
- [Paris places desktop](screenshots/paris-places-desktop.png) — 카드 썸네일

## 전체 작업 종결 상태

- 43일 중 사진이 배치된 일자: Day 1–37, 39–41 (Day 38 휴식일·Day 42–43 출국·text-only 정책 장소 제외)
- 최종 제외 목록(사유 포함)은 각 batch plan JSON의 `excluded`에 기록
- 후속 과제(사진 범위 밖): Daily Action Map PNG 경량화, 원본 388MB의 Git LFS 분리 여부
