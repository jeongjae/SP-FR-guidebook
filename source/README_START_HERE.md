# TP Europe Travel Guidebook — source/

2026-08-29 ~ 2026-10-10 · 43일 42박(숙박 41박 + 기내 1박). 이 디렉터리가 웹사이트의 원고다.
빌드는 `python3 build/build.py` — 명시된 정본 파일만 읽는다.

## 시작 순서
1. `CURRENT/00_Governance/00_Current_Source_of_Truth_Index_v2.0.md` — 정본 목록
2. `CURRENT/10_Core/03_Whole_Trip_Master_Itinerary_v1.2.md` — 43일 뼈대
   - 숙박 날짜·박수의 구조화된 정본은 같은 폴더의 `itinerary.json`
3. `CURRENT/20_Regional_Chapters/` — 지역 정본 8개 (v2.0/v2.1)
4. `OPERATIONS/116_Phase10_Official_Source_Fact_Verification_Register_v1.0.md`
5. `OPERATIONS/117_Departure_and_Daily_Reverification_Calendar_v1.0.md`
6. `OPERATIONS/90_Guidebook_100pct_Roadmap_and_Scorecard_v1.9.md`

## 규칙
- 챕터 개정은 정본 파일을 제자리에서 고친다. 새 버전 파일을 만들지 않는다.
- 사본·구판은 `ARCHIVE/` 에 있다. 여행 판단에 쓰지 않는다.
- 장소는 `ASSETS/91_Place_Registry_v1.0.md` 가 정본이다.

다음 단계: Phase 11 Word·모바일 PDF·인쇄 PDF 제작.
실제 예약서가 제공되면 Phase 8B를 병행해 최종본에 반영한다.
