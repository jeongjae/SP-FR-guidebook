# 가이드북 이미지 정책

최종 갱신: 2026-08-05

## 범위와 원칙

이 정책은 웹사이트에 포함되는 장소·도시·음식·교통·체험 사진에 적용한다. 사진을 무료로 열람할 수 있다는 사실은 재사용 허가를 뜻하지 않는다. 모든 외부 사진은 파일 단위로 저작자, 원본 파일 페이지, 라이선스, 검증일을 기록한 뒤 로컬에 저장한다. 외부 이미지 hotlink는 허용하지 않는다.

## 허용 라이선스

- Public Domain, CC0
- CC BY, CC BY-SA
- Unsplash License, Pexels License, Pixabay Content License
- 파일별 이용조건에서 상업적 재사용과 필요한 수정이 명시적으로 허용된 공공기관 이미지

CC BY와 CC BY-SA는 저작자, 출처 페이지, 라이선스명과 라이선스 링크를 표시한다. CC BY-SA 파생 파일에는 리사이즈·크롭·포맷 변환 사실과 동일조건변경허락 의무를 함께 기록한다.

## 제외 라이선스와 출처

- CC BY-NC 계열, CC BY-ND 계열, Editorial Only
- 라이선스·저작자·원본 페이지가 불명확한 파일
- 일반 검색결과, 블로그, 언론사, 여행사, 식당 홈페이지·SNS, Instagram, Facebook, TripAdvisor, Pinterest
- 워터마크가 있거나 별도 허가가 필요한 파일
- 제3자 얼굴, 어린이, 상표, 공연, 미술작품이 주 피사체인 이미지

## 선택과 표현

후보는 라이선스 명확성 30, 대표성 25, 해상도 15, 구도 10, 현재 모습 10, 디자인 적합성 10으로 평가한다. 라이선스가 불명확하면 점수와 관계없이 제외하고, 그 외에는 75점 이상만 채택한다. 음식 사진은 지역 음식의 일반적인 대표 이미지로만 표시하며 특정 식당의 실제 메뉴라고 암시하지 않는다.

인물은 군중 속 부수적 요소만 허용하고 얼굴이 중심인 사진은 피한다. AI 생성 이미지는 실제 장소나 음식의 기록 사진으로 사용하지 않는다.

## 저장과 최적화

- 승인 원본: `source/ASSETS/photos/originals/<region>/`
- 반응형 파생본: `source/ASSETS/photos/processed/{hero,content,thumbnails}/`
- 빌드 결과: `site/assets/images/`
- 매니페스트: `data/images/image-manifest.json`과 `data/images/image-manifest.csv`
- 형식: 원본은 검증용으로 보존하고, 공개 파일은 sRGB WebP로 변환하며 EXIF는 제거한다.
- Hero: 800/1280/1920px, 본문: 최대 1280px, 썸네일: 480×320px
- 원본보다 큰 파생본은 만들지 않으며, 브라우저에는 `srcset`·`sizes`·명시적 크기를 제공한다.
- Hero만 즉시 로드하고 본문·썸네일은 지연 로드한다.
- 목표 용량: 본문 평균 250KB 이하, Hero 평균 350KB 이하, 썸네일 평균 80KB 이하

Barcelona 파일럿은 재현성과 라이선스 증빙을 위해 승인 원본을 저장소에 보관하되 사이트와 PWA에는 포함하지 않는다. 후속 43일 전체 배치에서는 저장소 증가량을 먼저 측정해 Git LFS 또는 별도 원본 보관소를 결정한다. 기존 `data/media-catalog.json` 자산은 단계적으로 새 매니페스트로 이전한다.

## Attribution

각 이미지 바로 아래에 저자, Wikimedia Commons, 라이선스, 원본 링크를 표시한다. 파일럿 전체 목록은 빌드가 `site/about/photo-credits.html`에 생성하고, 저장소용 목록은 `docs/photo-content/04_photo_credits.md`에 둔다. 이미지와 크레디트의 연결이 명확해야 하며, 저자 표시가 필요한데 저자가 없으면 검사를 실패시킨다.

## 미확보 항목

검증 가능한 대표 이미지를 찾지 못하면 임의 대체하지 않는다.

```text
IMAGE_PENDING
Reason: no clearly reusable representative image found
```
