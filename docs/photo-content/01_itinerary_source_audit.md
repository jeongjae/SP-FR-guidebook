# 일정 정본 감사

감사일: 2026-08-05

## 채택한 정본 순서

1. `source/CURRENT/00_Governance/00_Current_Source_of_Truth_Index_v2.0.md`
2. `source/CURRENT/10_Core/03_Whole_Trip_Master_Itinerary_v1.2.md`
3. 해당 날짜의 `source/CURRENT/20_Regional_Chapters/*.md`
4. `source/OPERATIONS/100_Whole_Trip_43_Day_Execution_Audit_v1.0.md`
5. 지도·장소 레지스트리는 장소명과 공개 범위를 대조하는 보조 자료로만 사용

지시서에 예시된 `source/40_Master_Guidebook/`는 현재 저장소에 없다. 2026-08-03 중복 통합 후 `source/CURRENT/`가 정본이며 `source/ARCHIVE/`는 빌드에서 제외된다.

## 불일치와 조치

| 날짜 | 서로 다른 내용 | 관련 파일 | 권장 정본·근거 | 조치 |
|---|---|---|---|---|
| 2026-09-01 (Day 4) | Master/지역 챕터는 `Sitges → Girona 또는 Bàscara`, 실행 감사는 `Sitges → Bàscara` 직행을 기본으로 적는다. | Master Itinerary, Barcelona·Girona 챕터, Execution Audit | Bàscara 체크인 시간이 우선이고 Girona는 조건부다. 가장 구체적인 Girona 운영안이 이를 명시한다. | Sitges·Bàscara는 `confirmed`, Girona는 `optional`로 분류했다. |
| 2026-09-01 (Day 4) | Barcelona 챕터는 Sitges를 선택으로 소개하지만 Master와 시간표에는 실제 경유로 배치한다. | Barcelona 챕터, Master Itinerary | 날짜별 실행표가 편집 추천표보다 구체적이다. | Sitges는 `confirmed`; Cau Ferrat·Palau de Maricel 내부 방문은 `optional`. |
| 2026-09-21 (Day 24) | Avignon 챕터 피로도 4, Lyon 챕터 피로도 3. | 두 지역 챕터, 기존 빌드 경고 | 도착 지역 Lyon 값 3을 현재 빌드가 사용하지만 이동일 감사는 4다. | 사진 분류에는 영향 없음. 일정 데이터에는 Master의 `4`를 유지하고 별도 일정 수정 대상으로 남긴다. |
| 전체 | 장소 레지스트리는 81개 spot이지만 최신 Master에는 Cadaqués, Tossa de Mar, Sant Feliu 등 레지스트리 밖 실제 방문지가 있다. | Place Registry, Master Itinerary | 방문 여부는 Master가 우선이다. | 사진 인벤토리는 Master의 장소를 포함한다. 레지스트리 보강은 사진 Pilot 밖 후속 과제다. |
| 전체 | `daily-maps.json`은 이름과 달리 43일이 아니라 5일 샘플만 포함한다. | Daily Execution Maps JSON | 전체 날짜 정본으로 사용할 수 없다. | 좌표를 인벤토리에 복사하지 않고 Master+지역 챕터로 43일을 생성한다. |
| Barcelona Pilot | 작업지시서 예시의 La Boqueria·Passeig de Gràcia는 최신 핵심 일정과 다르다. 최신 일정은 Mercat de la Concepció·Eixample 생활권을 쓴다. | 작업지시서, Master, Barcelona 챕터 | 최신 일정 우선 원칙 | La Boqueria는 제외하고 Mercat de la Concepció를 채택한다. Passeig de Gràcia 사진은 Eixample 생활권 대표로만 사용한다. |

## 개인정보 감사

Girona 정본에 private Airbnb의 정확한 도로명 주소와 지도 링크가 기존부터 세 차례 들어 있다. 사진 인벤토리에는 `Bàscara private stay`라는 일반명만 남기고 주소·좌표·사진 필요 여부를 제거했다. 공개 빌드의 private 주소 잔존은 Pilot 완료 전에 제거·검사해야 한다.

## 결론

- 43일(2026-08-29~2026-10-10) 날짜 자체의 누락이나 중복은 없다.
- 사진 작업의 기준은 Master의 핵심 일정과 선택·축소 레버다.
- 조건부 장소는 확정 장소처럼 촬영·hero 우선순위를 부여하지 않는다.

