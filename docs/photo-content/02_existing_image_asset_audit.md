# 기존 이미지 자산 감사

감사일: 2026-08-05

## 현황

| 자산 | 수량·상태 | 판단 |
|---|---|---|
| `88_Representative_Public_Photos` | 지역 hero 8장과 contact sheet | Commons 크레딧은 있으나 JPG 단일본이며 별도 상수와 문서가 정본 역할을 중복한다. |
| `licensed-guidebook-images` | Barcelona·Girona·Nice 각 8장, 총 24 WebP | 파일별 출처·작가·라이선스·alt가 `media-catalog.json`에 있다. 단일 해상도라 responsive/thumbnail 요구를 충족하지 않는다. |
| Daily Mobile Guide Images | Day 1–43 카드와 일부 중복/Phase4 카드 | 내부 제작 실행 카드다. 장소 사진 원본으로 재사용하지 않는다. |
| Editorial Visuals | 6개 PNG | 내부 제작 도식이다. 사진 manifest와 분리한다. |
| `site/assets/media` | 빌드 때 24장을 복사 | `site/`는 산출물이므로 직접 수정하지 않는다. |

## Barcelona 기존 승인본 8장

- Sagrada Família
- Sant Pau Recinte Modernista
- Barri Gòtic
- Biblioteca de Catalunya
- Sitges 해안
- Mercat de la Concepció
- pa amb tomàquet
- crema catalana

모두 Commons 원본 페이지와 CC BY/CC BY-SA 메타데이터가 있으므로 Pilot 후보로 재검증한다. 기존 WebP의 평균은 약 136KB이고 각 파일은 현재 300KB 이하이나, 원본 SHA-256·responsive 파생·thumbnail·초점 좌표가 없다.

## 중복·공백

- Sagrada Família는 기존 지역 hero JPG와 Barcelona WebP 카탈로그에 중복 존재한다.
- Barcelona 일정의 Eixample/Passeig de Gràcia, Avinguda de Gaudí, MACBA, Cau Ferrat, Palau de Maricel은 기존 로컬 승인본이 없다.
- 기존 카탈로그의 Barcelona 사진은 날짜별 Day 1–4 페이지에 직접 삽입되지 않는다.
- 기존 credit 페이지는 `credits.html`이고 지시서의 `about/photo-credits.html` anchor 계약이 없다.

## PWA·성능 기준선

- 변경 전 빌드: 314 HTML, PWA 444 files, 14.1 MiB
- 변경 전 `site/` 실제 크기: 14,880,426 bytes
- Barcelona 배포 WebP 8장: 1,089,776 bytes
- 사진은 core precache 목록이 아니라 전체 오프라인 저장 manifest에 포함된다.

## 권장 조치

Barcelona 8장을 새 manifest와 원본/파생 구조로 이관하고 5장을 추가한다. 기존 다른 지역 16장은 현 카탈로그에서 유지하되, Barcelona는 새 manifest를 우선하여 이중 렌더링과 이중 크레딧을 막는다.

