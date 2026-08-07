# 상용 가이드북 개편 — 데이터 모델 v1.0

기준 커밋 `c274d42` · 2026-08-06. **새 스키마를 발명하지 않는다.** 현행 정본을
확정하고, 참조 관계와 남은 통합 과제만 정의한다. (원 지시서 §14 의 YAML 트리는
폐기 — 결정 로그 D-02·D-07 참조.)

## 1. 정본 지도 (정보 유형 → 단일 정본)

| 정보 | 정본 | 형식 | 검증 |
|---|---|---|---|
| 여정 (날짜·거점·박) | `source/CURRENT/10_Core/itinerary.json` | JSON | `build/itinerary.py` + `scripts/validate_itinerary.py` (CI) |
| 43일 원고 | `source/CURRENT/10_Core/03_Whole_Trip_Master_Itinerary_v1.2.md` + 지역 챕터 8편 | MD | Day 섹션 가드 (43일·50건) |
| 콘텐츠 장소 (등급·본문·위키) | `source/ASSETS/91_Place_Registry_v1.0.md` — 97행 (spot 94 · node 3) | MD 표 | `check_places` (본문 헤딩 대조·고아 탐지) |
| **지도 장소 (좌표·핀·경로)** | `source/ASSETS/maps/place-registry.json` — 72곳 + `daily-routes.json` + `region-groups.json` | JSON | `scripts/validate_map_data.py` |
| 데일리 카드 (액션맵) | `data/daily-cards/day-NN.json` × 43 + `schema.json` | JSON | 카드 파이프라인 `validate.py` |
| 예약·교통·숙소 | `source/OPERATIONS/TP_…Tracker_v1.2.xlsx` (R001–R028 · T001–T010 · 숙소 8) | XLSX | Phase 8 가드 |
| 공식정보 검증 | `source/OPERATIONS/116_…` (F001–F023) | MD | Phase 10 가드 |
| 이미지 라이선스 | `data/media-catalog.json` (+ 사진 스트림의 manifest 체계) | JSON | `build/media.py` + `scripts/validate_media.py` (CI) |
| 파생 그래프 (읽기 전용) | `site/assets/content-model.json` — regions 8 · days 43 · places 97 · … | 생성물 | `content_model.validate_graph` |

## 2. 장소 이원 체계 (D-07 확정)

콘텐츠 레지스트리(97행, 등급·본문 담당)와 지도 레지스트리(72곳, 좌표·경로 담당)는
**책임이 다른 별개 정본**이다. 같은 장소는 kebab-case 슬러그로 대응한다.

- 대응 규칙: 지도 `id` == 콘텐츠 `슬러그` 를 원칙으로 하되, 지도에만 있는 것
  (주차 노드 등)과 콘텐츠에만 있는 것(본문 전용 섹션)을 허용한다.
- **통합 검토는 스트림 ③ 완료 후** (Place ID 71곳 보강이 끝나야 좌표 신뢰 확정).
- 개편 중 새 장소 추가 절차: ① 91 레지스트리에 행 추가 → ② 지도에 필요하면
  place-registry.json 에 같은 슬러그로 추가 → ③ 빌드로 양쪽 가드 통과 확인.

## 3. 개인정보 규칙 (강화 유지)

- 지도 레지스트리: `private: true` → `address`·`googleMapsUrl`·`googlePlaceId` 공란,
  좌표 소수점 3자리 이하 (validate_map_data 가 오류 처리).
- 예약번호·결제정보는 공개 원고에 넣지 않는다 (OPERATIONS/41 §5.3).
- 원 지시서 §3.4 와 동일 — 추가 조치 불필요, 기존 가드가 이미 강제.

## 4. 원 지시서 §9.1 dossier 필드와 현행의 대응

원 지시서가 요구한 필드 대부분은 이미 존재하되 세 정본에 분산되어 있다:
`priority`→91 레지스트리 등급 · `coordinates`→지도 레지스트리 · `reservationStatus`→트래커 ·
`officialUrl`/`verifiedAt`→dossier 본문 `공식정보` 줄 + F 레지스터. **누락 필드**
(bestTime/avoidTime/skipRule/rainAlternative 의 구조화)는 Phase E(지역·장소 편집)에서
dossier 본문 표준 섹션으로 다룬다 — 새 데이터 파일을 만들지 않는다.

## 5. 검증일 자동 경고 (원 지시서 §13, 채택)

F 레지스터의 `최종확인일` 이 기준일(출발 D-7)보다 오래된 항목을 빌드 경고로
표시하는 검사를 Phase F에서 추가한다. 기존 17개 재검증 게이트 날짜 체계를 재사용.
