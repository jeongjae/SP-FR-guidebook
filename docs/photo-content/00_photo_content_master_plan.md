# 사진 콘텐츠 확충 마스터 플랜

작성일: 2026-08-05  
범위: Barcelona Pilot와 전체 43일 장소 인벤토리

## 현재 구조

- 정본은 `source/CURRENT/10_Core`와 `source/CURRENT/20_Regional_Chapters`다.
- `build/build.py`가 Markdown·XLSX·JSON을 읽어 `site/`를 전부 재생성한다.
- 장소 축은 `source/ASSETS/91_Place_Registry_v1.0.md`, 날짜 축은 Master Itinerary와 지역 챕터가 제공한다.
- 기존 로컬 라이선스 카탈로그는 Barcelona·Girona·Nice 각 8장, 총 24장의 단일 WebP를 관리한다.
- PWA 전체 오프라인 저장은 빌드 결과 전체를 선택 다운로드하며, 초기 precache는 셸 자산만 사용한다.

## 작업 범위

1. 43일 일정의 날짜·거점·방문지·대체지를 정규화한다.
2. public/private, confirmed/optional/reference, hero/major/supporting/text-only, 사진 필요 여부를 기록한다.
3. Barcelona 3박 구간(Day 1–4 전환일 포함)만 13개 원본을 검증한다.
4. 원본에서 hero·content·thumbnail WebP를 생성하고 manifest로 관리한다.
5. Day 1–4, Barcelona 지역 허브·장소·먹거리 페이지와 사진 크레딧에 자동 삽입한다.
6. 빌드·PWA·HIG·이미지·라이선스·중복·성능을 검사한다.

## 예상 수량과 파일 구조

- 43일 인벤토리: 약 130–150개 고유 장소
- Barcelona Pilot 승인 원본: 13장
- 후보: 승인 대상별 최대 3장
- 파생본: 원본별 hero responsive 3종, content 1종, thumbnail 1종을 상한으로 한다.
- 원본: `source/ASSETS/photos/originals/barcelona/`
- 파생본: `source/ASSETS/photos/processed/{hero,content,thumbnails}/`
- 배포본: `site/assets/images/{hero,content,thumbnails}/`
- 데이터 정본: `data/images/image-manifest.json`

## 단계

1. 정본·일정·자산·빌드/PWA 감사
2. 43일 장소 인벤토리 생성과 검증
3. Commons 후보 수집과 파일 설명 페이지 라이선스 검증
4. 승인 원본 다운로드·SHA-256 기록·시각 검토
5. EXIF 보정·sRGB 변환·크롭·WebP 파생 생성
6. manifest 기반 `<picture>`·caption·credit 자동 렌더링
7. 자동 검사와 desktop/mobile 화면 검수
8. 기능별 커밋·푸시·Draft PR

## 위험과 대응

| 위험 | 대응 |
|---|---|
| 일정 정본 혼선 | Current Source of Truth Index와 Master Itinerary를 우선하고 차이를 별도 감사표에 남긴다. |
| 잘못된 장소 사진 | Commons 파일 페이지·설명·해상도·시각 검토를 모두 통과한 파일만 승인한다. |
| 라이선스 누락 | 필수 필드와 허용 라이선스를 빌드 전에 검사한다. |
| private 숙소 노출 | 주소·좌표·외관을 manifest와 배포물에서 금지한다. 기존 노출도 검사 대상으로 둔다. |
| 원본/파생 중복 | 원본 SHA-256과 perceptual hash를 검사한다. |
| 모바일 용량 증가 | 첫 hero만 eager, 나머지 lazy, responsive `srcset`, WebP 용량 상한을 적용한다. |
| PWA 과대 precache | 사진은 core precache에 넣지 않고 방문 또는 전체 오프라인 저장 때만 캐시한다. |

## Pilot 완료 기준

- 43일·43개 날짜 누락 없음
- 장소 ID와 표기 일관성 검사 통과
- Barcelona 승인 원본 12–15장, 라이선스 누락 0
- hero/content/thumbnail 생성과 manifest 파일 대조 통과
- Day 1–4와 Barcelona 지역·장소 페이지 자동 삽입
- alt, width, height, 깨진 링크, private 노출 오류 0
- 대표 페이지 초기 전송량 2MB 이하
- `build.py`, `pwa_check.py`, `hig_check.py`, `image_check.py` 통과 또는 환경 제한을 재현 가능한 근거와 함께 보고

