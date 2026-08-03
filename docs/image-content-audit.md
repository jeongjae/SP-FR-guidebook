# 이미지 콘텐츠 감사 보고서

감사일: 2026-08-03
대상 브랜치: `feat/licensed-guidebook-images`

## 요약

이 저장소는 React/Next.js가 아니라 Python 빌더가 Markdown·XLSX 정본을 순수 정적 HTML로 변환하는 사이트다. `site/`는 생성물이므로 직접 편집하지 않고 `source/`, `build/`, `data/`를 변경한 뒤 전체 빌드한다. 첫 샘플은 Barcelona, Girona, Nice 각 8장, 총 24장으로 제한한다.

## 현재 구조

| 항목 | 감사 결과 |
|---|---|
| 프레임워크 | Python 정적 사이트 생성기 (`build/build.py`) |
| 콘텐츠 정본 | `source/CURRENT/10_Core`, `source/CURRENT/20_Regional_Chapters`의 Markdown, 운영 XLSX |
| 빌드 결과 | `site/` 아래 313개 HTML |
| 배포 | `main` push 시 GitHub Actions가 빌드해 `gh-pages`에 배포 |
| 이미지 컴포넌트 | 템플릿 함수 `hero_figure`; React/Next Image 없음 |
| 기존 이미지 | 지역 Hero 8장, 데일리 카드 43장 외 파생 카드·도식, Leaflet 자산 |
| 기존 최적화 | Hero JPG를 그대로 복사. 일반 이미지 최적화 파이프라인 없음 |
| 기존 권리 기록 | Hero 8장은 `source/ASSETS/88_Representative_Public_Photo_Credits_v1.0.md`에 저자·CC 라이선스·원문 기록 |
| 기존 장소 사진 | 브라우저가 Wikipedia summary API의 썸네일을 런타임 hotlink. 파일별 라이선스·저자 표시 없음 |
| 오프라인 | 본문과 로컬 자산은 동작하지만 기존 장소 사진은 네트워크 의존 |

## 콘텐츠 인벤토리

장소 레지스트리의 실제 표 행은 82개 `spot`과 3개 교통 `node`다. 문서 하단에는 `spot 83`으로 쓰여 있어 1건 차이가 있으며, 별도 데이터 정합성 이슈로 남긴다. 지역별 실제 행은 다음과 같다.

| 지역 | 장소 spot | 교통 node | 1차 예상 이미지 |
|---|---:|---:|---:|
| Barcelona | 8 | 1 | 8 (샘플) |
| Girona / Costa Brava | 7 | 0 | 8 (샘플) |
| Nice / Côte d’Azur | 10 | 2 | 8 (샘플) |
| Aix-en-Provence | 13 | 0 | 6–8 |
| Luberon | 11 | 0 | 6–8 |
| Avignon / Alpilles | 11 | 0 | 6–8 |
| Lyon | 7 | 0 | 6–8 |
| Paris | 15 | 0 | 8–12 |

정본 지역 챕터에는 사진용 `VIS-PHOTO` 토큰 44건이 있다. `source/CURRENT` 전체에는 Reader Edition 등 중복 정본 후보까지 포함해 166건이 검색되므로, 전체 확장 때 토큰 수를 그대로 이미지 수로 사용하면 중복이 생긴다. 요구사항 CSV는 장소 레지스트리와 지역별 대표 음식 목록을 기준으로 한 번만 정규화한다.

## 1차 샘플 범위

지역당 도시 Hero 1, 장소·시장 5, 음식 2를 기본으로 총 24장을 채택한다. 기존 Hero 3장은 파일 페이지 메타데이터를 재검증한 뒤 WebP 카탈로그에 편입한다.

- Barcelona: Sagrada Família Hero, Sant Pau, Barri Gòtic, Sitges, 생활시장, pa amb tomàquet, crema catalana 등 8장
- Girona: Onyar Hero, 대성당, 성벽, Collioure, Peratallada, Calella de Palafrugell, xuixo, suquet de peix 등 8장
- Nice: Promenade Hero, Cours Saleya, Vieux Nice, Castle Hill, Cannes/Le Suquet, Monaco, socca, pissaladière 등 8장

## 기술적 제약

- `site/` 전체가 빌드 때 재생성되므로 모든 이미지 복사와 HTML 삽입을 빌더에 구현해야 한다.
- npm 프로젝트가 없어 `npm run build/lint/typecheck`는 해당하지 않는다. 기존 필수 검증은 `python build/build.py`와 `python build/hig_check.py`다.
- 로컬 머신에 시스템 Python이 없어 `uv`의 작업공간 격리 런타임으로 같은 Python 3.12 환경을 재현한다.
- GitHub Pages는 정적 파일만 제공하므로 서버 측 이미지 변환이나 동적 라이선스 조회를 사용할 수 없다.
- 기존 장소 사진 로더는 외부 hotlink이며 오프라인·Attribution 기준을 충족하지 못한다.

## 저작권 위험

1. Wikipedia 대표 썸네일은 사진별 저자·라이선스를 화면에 표시하지 않아 CC BY/CC BY-SA 의무 누락 위험이 있다.
2. Wikipedia 페이지 제목만으로 이미지를 선택하면 동음이의어나 문서 대표 이미지 변경으로 잘못된 장소가 노출될 수 있다.
3. 음식 사진을 추천 식당 문맥에 바로 배치하면 실제 메뉴로 오인될 수 있다.
4. 기존 JPG Hero는 크롭·리사이즈 기록이 있으나 중앙 카탈로그와 자동 참조 검증이 없다.
5. 시장·거리 사진은 얼굴과 상표가 중심이 되지 않는지 별도 시각 검토가 필요하다.

## 권장 구현

`data/media-catalog.json`을 단일 정본으로 두고 JSON Schema와 Python 검증기를 연결한다. `build/build.py`는 `mediaId` 또는 장소 slug로 카탈로그를 조회해 로컬 WebP, 한국어 alt, 캡션, 저자·라이선스·원본 링크를 한 figure로 렌더링한다. 장소 페이지·지역 챕터 카드·음식 섹션이 같은 렌더러를 공유하게 하며, 기존 Wikipedia 런타임 이미지 로더는 제거한다.

미확보 항목은 `data/image-requirements.csv`에 `IMAGE_PENDING`과 이유를 남기고 화면에 가짜 대체 이미지를 넣지 않는다.
