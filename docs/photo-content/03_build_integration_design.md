# 사진 빌드 통합 설계

작성일: 2026-08-05

## 데이터 흐름

```text
Master Itinerary + regional chapters
  → scripts/extract_itinerary_places.py
  → data/itinerary-places.{json,csv}

Wikimedia Commons API + reviewed selection
  → photo-candidates / rejected candidates
  → image-manifest
  → originals (SHA-256)
  → process_images.py
  → processed hero/content/thumbnails
  → build/build.py
  → site/assets/images + Day/region/place pages + credits
```

## manifest 계약

`data/images/image-manifest.json`을 Barcelona Pilot의 사진 정본으로 사용한다. 모든 항목은 `imageId`, `placeId`, `title`, `source`, `sourcePage`, `originalFile`, `creator`, `license`, `licenseUrl`, `changes`, `downloadDate`, `usage`, `role`, `status`, 한국어 `alt`·caption, 원본 크기·SHA-256, 파생 variant 목록을 갖는다.

필드 누락, 허용되지 않은 라이선스, private place 참조, 실제 파일 누락, 중복 ID는 빌드 전 실패한다.

## 이미지 처리

- `ImageOps.exif_transpose`로 EXIF 방향 보정
- ICC가 있으면 sRGB로 변환하고 없으면 RGB/sRGB로 정규화
- 초점 좌표 기반 16:9 hero crop
- content는 원본 비율을 유지하며 최대 폭 1280px
- thumbnail은 3:2 480×320 crop
- 원본보다 확대하지 않으며 불가능한 variant는 생성하지 않고 manifest에 남기지 않는다.
- WebP 품질: hero 80, content 78, thumbnail 73
- 원본·파생 SHA-256과 크기·바이트를 manifest에 기록

## HTML 렌더링

- `<picture>`의 WebP `srcset`과 `sizes`를 manifest에서 생성한다.
- 페이지의 첫 hero만 `loading="eager"`와 `fetchpriority="high"`를 쓴다.
- 나머지는 lazy/async이고 모든 `<img>`에 width·height·한국어 alt를 넣는다.
- caption의 사진 정보 링크는 `/about/photo-credits.html#{imageId}`로 연결한다.
- Day 1–4는 한 장 hero와 최대 3개 방문지 thumbnail/content를 사용한다.
- Barcelona 지역 허브는 hero 1장, 핵심 명소 3–5장, 음식·생활 2–3장 상한을 지킨다.

## PWA

- 원본은 `site/`에 복사하지 않는다.
- 사진은 service worker의 core precache에 넣지 않는다.
- 현재 전체 오프라인 저장 기능을 사용할 때만 `offline-files.json`에 포함되고, 일반 방문에서는 runtime cache가 담당한다.
- 지역별 오프라인 분할은 전체 Batch에서 이미지가 35MB를 넘기 시작할 때 도입한다.

## 호환 전략

기존 `media-catalog.json`은 Girona·Nice 16장의 임시 호환 계층으로 유지한다. Barcelona 렌더링·크레딧은 새 manifest를 우선하고 기존 Barcelona 8장은 중복 배포하지 않는다. 후속 Batch에서 지역별로 새 manifest 구조로 순차 이관한다.

