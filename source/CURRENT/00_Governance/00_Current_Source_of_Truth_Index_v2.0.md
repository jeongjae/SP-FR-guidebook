# Current Source of Truth Index v2.0 — 콘텐츠 중복 통합

## 기준
- 일정: 2026-08-29 출발, 2026-10-10 파리 출국
- 규모: 43일 일정·42박
- 원칙: **정보 유형마다 정본은 한 파일이다.** 사본은 `source/ARCHIVE/` 에만 있다.
- 실측 근거: `docs/content-architecture-audit.md` (빌드가 읽는 파일 전수 확인)

## Authoritative core
- `CURRENT/10_Core/01_How_to_Use_This_Guidebook_v1.0.md`
- `CURRENT/10_Core/02_Whole_Trip_Experience_Highlights_v1.0.md`
- `CURRENT/10_Core/03_Whole_Trip_Master_Itinerary_v1.2.md`

## Authoritative regional chapters — v2 증보판이 정본이다
- `04_Barcelona_Sitges_v2.0.md`
- `05_Girona_Collioure_Emporda_v2.1.md`
- `06_Nice_Cote_d_Azur_v2.0.md`
- `07_Aix_en_Provence_v2.0.md`
- `08_Luberon_Farmhouse_v2.0.md`
- `09_Avignon_Alpilles_Pont_du_Gard_v2.0.md`
- `10_Lyon_v2.0.md`
- `11_Paris_Long_Stay_v2.0.md`

v1.x 구판과 Reader Edition, 42_Guidebook_Master 통합본은 2026-08-03 감사에서
**빌드 미사용 사본**으로 확인되어 `source/ARCHIVE/` 로 옮겼다. 웹사이트가
독자판의 역할을 대신하며, 별도 Reader 사본은 유지하지 않는다.

## 장소 정본
- `ASSETS/91_Place_Registry_v1.0.md` — 장소 그래프. 빌드가 지도 핀·본문
  헤딩과 대조하며, 편집은 이 MD를 직접 고친다.

## Authoritative operations
- `OPERATIONS/TP_Europe_Travel_Master_Tracker_v1.2.xlsx` (트래커·콘텐츠 모델)
- `OPERATIONS/100_Whole_Trip_43_Day_Execution_Audit_v1.0.md`
- `OPERATIONS/41_Operational_Variables_and_Reverification_Register_v1.0.md`
- `OPERATIONS/116_Phase10_Official_Source_Fact_Verification_Register_v1.0.md`
- `OPERATIONS/117_Departure_and_Daily_Reverification_Calendar_v1.0.md`
- `OPERATIONS/118_Phase10_Final_Fact_Verification_Report_v1.0.md`
- `OPERATIONS/90_Guidebook_100pct_Roadmap_and_Scorecard_v1.9.md`

## Authoritative assets
- `ASSETS/75_Execution_Maps/*` (실행지도 HTML·GeoJSON·KML)
- `ASSETS/80_Daily_Mobile_Guide_Images/*` (데일리 카드)
- `ASSETS/85_Editorial_Visuals/*.png` + 권리 대장 86·87
- `ASSETS/88_Representative_Public_Photos/*.jpg` + `88_..._Credits_v1.0.md`
- `ASSETS/89_Commercial_City_Experience_Cards_v1.0.md` (phase9 가드 대상)
- `ASSETS/90_Regional_Context_and_Place_Dossier_Compendium_v1.0.md` (phase9 가드 대상)

## Editorial standards
- `CURRENT/00_Governance/88_Editorial_Style_Guide_v1.0.md`
- `CURRENT/00_Governance/89_Commercial_Guidebook_Editorial_and_Layout_Standard_v1.0.md`
- `CURRENT/00_Governance/90_Regional_and_Place_Dossier_Editorial_Standard_v1.0.md`

## 이 색인의 유지 규칙
- 챕터를 개정하면 새 버전 파일을 만들지 말고 **정본 파일을 제자리에서 고친다.**
  버전 파일을 늘리는 방식이 3~4중 사본 3만 줄을 만들었다 (감사 보고서 참조).
- 구판이 필요하면 git 이력을 쓴다. 파일 사본을 CURRENT에 두지 않는다.
