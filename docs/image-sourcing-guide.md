# 이미지 소싱 가이드

최종 갱신: 2026-08-03

## 우선순위

1. Wikimedia Commons 파일 페이지
2. Wikipedia 문서가 연결하는 Commons 파일
3. 파일별 재사용 조건이 명시된 관광청·공공기관
4. Unsplash, Pexels, Pixabay의 원본 파일 페이지

이 샘플에서는 API 키가 필요 없고 파일별 구조화 메타데이터를 제공하는 Wikimedia Commons만 사용한다.

## 작업 절차

1. `data/image-requirements.csv`에서 P0 항목을 선택한다.
2. 장소명만으로 자동 확정하지 않고 본문 설명과 실제 피사체를 대조한다.
3. Commons 공식 API 또는 파일 페이지에서 원본 URL, 저자, 라이선스명·URL, 원본 크기와 설명을 확인한다.
4. 허용 라이선스인지 검사하고 후보 점수를 기록한다.
5. 썸네일을 시각 검토해 장소·음식 대표성, 인물·워터마크·광고성, 현재 모습 여부를 확인한다.
6. 공식 다운로드 URL에서만 받고 WebP로 변환한다. EXIF는 보존하지 않는다.
7. `data/media-catalog.json`을 갱신하고 `scripts/validate_media.py`를 실행한다.
8. 저작자 표시 문서를 다시 생성하고 빌드·HIG 검사·렌더링 QA를 수행한다.

## Commons API 사용

검색 결과는 후보 발견에만 사용한다. 최종 메타데이터는 `imageinfo`의 `url`, `descriptionurl`, `size`, `mime`, `extmetadata`를 파일 제목으로 다시 조회한다. 요청에는 식별 가능한 User-Agent를 쓰고, 여러 제목을 한 요청으로 묶으며, 429 응답 시 즉시 중단하고 재시도 간격을 둔다.

최종 채택 전 다음을 모두 확인한다.

- `LicenseShortName`이 허용 목록에 있음
- `LicenseUrl`이 해당 라이선스 공식 페이지임
- `Artist`가 비어 있지 않음(Public Domain의 명백한 무명 저작물은 예외 사유 기록)
- `descriptionurl`이 Commons의 개별 파일 페이지임
- 원본 또는 1200px 이상 썸네일을 확보할 수 있음
- 파일 설명이 대상 장소·음식과 일치함

## 음식·식당

음식은 조리 형태가 분명하고 특정 식당의 플레이팅으로 오인되지 않는 사진을 선택한다. 캡션에는 지역 대표 이미지이며 실제 식당 제공 형태와 다를 수 있음을 밝힌다. 식당 공식 사이트·SNS의 내부나 메뉴 사진은 사용하지 않는다.

## 수정 기록

WebP 변환, 리사이즈, 자동 회전, 색공간 변환, 크롭 여부를 카탈로그의 `modified`와 `modificationNote`에 기록한다. CC BY-SA는 포맷 변환만 했더라도 파생본의 동일조건변경허락 표시를 유지한다.
