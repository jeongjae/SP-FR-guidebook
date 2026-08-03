# Phase 2 Content Model v1.0

## 목적

날짜·지역·장소·숙소·예약·교통을 화면 제목이나 자연어 문자열이 아니라 안정적인 ID로 연결한다. Phase 2 전환 중에는 기존 Markdown과 Excel이 입력 원본이며, 빌드는 이를 하나의 검증 가능한 콘텐츠 그래프로 정규화한다.

## ID 규칙

| 유형 | 형식 | 예시 |
|---|---|---|
| 날짜 | `day:NNN` | `day:001` |
| 지역 | `region:slug` | `region:nice` |
| 장소 | `place:slug` | `place:colline-du-chateau` |
| 숙소 구간 | `stay:slug` | `stay:nice` |
| 예약 | `reservation:rNNN` | `reservation:r003` |
| 교통 | `transport:tNNN` | `transport:t004` |

## 관계

- 날짜는 하나의 주 거점(`regionId`)을 가진다.
- 장소는 하나 이상의 관련 지역(`regionIds`)과 0개 이상의 실행일(`dayIds`)을 가진다. 경계 지역의 동일 장소는 한 레코드로 합치며 구 슬러그는 `legacySlugs`로 보존한다.
- 숙소는 소유 지역과 체크인·체크아웃 구간을 가진다.
- 예약은 관련 지역과, 날짜가 정해진 경우 관련 실행일을 가진다.
- 교통은 반드시 하나의 실행일을 가진다.
- 장소의 별칭은 `aliases`에 보존해 한국어·현지어 검색 확장의 기반으로 사용한다.

## 생성물과 검증

빌드 시 `site/assets/content-model.json`을 생성한다. ID 중복, 깨진 참조, 43일 연속성을 검사하며 오류가 있으면 빌드를 중단한다. 이 파일은 향후 데일리·지역·준비 대시보드가 공유하는 읽기 전용 데이터 API다.

## 단계적 전환 원칙

1. Phase 2에서는 기존 화면 URL과 디자인을 유지한다.
2. 새로운 화면은 콘텐츠 그래프를 먼저 읽는다.
3. 기존 화면은 Phase 3~6에서 순차적으로 그래프 참조로 전환한다.
4. 모든 화면 전환이 끝나면 Markdown/Excel 추출기를 입력 어댑터로 축소하거나 제거한다.
