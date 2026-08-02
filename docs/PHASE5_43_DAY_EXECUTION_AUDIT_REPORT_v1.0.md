# Phase 5 — 43일 전체 실행성 감사 완료 보고서 v1.0

**완료일:** 2026-08-03  
**범위:** Day 1–43, Master Itinerary, 8개 지역 정본, Reader판, 데일리 웹페이지

## 결론

43일 일정은 날짜·숙박거점·P0 연결·완충·식사·휴식·삭제순서·대체안 구조가 모두 연결되어 있다. 전수 대조 중 Day 11(9월 8일 화요일)에 Matisse·Chagall 미술관을 배치한 운영일 충돌 1건을 발견해 교정했다. 교정 후 구조적으로 실행 불가능한 날짜는 발견되지 않았다.

단, 항공·열차·숙소·렌터카·시간지정 입장권의 실제 예약값은 아직 확정값이 아니다. 이 항목은 Phase 8 잠금 전까지 `실행 가능하나 미확정` 상태다.

## 발견 및 수정

| 우선순위 | 날짜 | 발견 | 수정 |
|---|---|---|---|
| P1 | Day 11 · 9/8 화 | Matisse와 Chagall이 모두 화요일 휴관인데 선택 문화시설로 배치됨 | 화요일 운영하는 Musée de la Photographie Charles Nègre 선택안으로 교체. 피로하면 생략하도록 유지 |

MAMAC도 2028년까지 공사 휴관이므로 대체안으로 사용하지 않았다.

## 공식 운영 검증

- Musée Matisse de Nice: 화요일 휴관.
- Musée National Marc Chagall: 화요일 휴관. 2026년 여름에는 점심 휴관도 적용.
- Musée de la Photographie Charles Nègre: 화요일 10:00–18:00 운영.
- MACBA: 월요일 운영. Day 3 일정과 일치.
- Sitges Cau Ferrat·Maricel: 4–10월 화–일 운영. Day 4 일정과 일치.
- Collioure 전통시장: 수·일 오전. Day 5 일정과 일치.
- Grand Palais `Cézanne et nous`: 2026-09-23–2027-01-17. Day 34 일정과 일치.

근거 URL은 `source/OPERATIONS/100_Whole_Trip_43_Day_Execution_Audit_v1.0.md`에 함께 기록했다.

## 자동 회귀가드

`build/build.py`의 `check_phase5_execution_guards()`가 다음을 강제한다.

1. 감사표 Day 1–43의 실제 날짜와 요일 일치
2. 감사표 거점과 지역 챕터 날짜범위 일치
3. Day 11에 Matisse·Chagall 동시 선택문구 재등장 금지
4. Day 11 사진미술관 선택안 존재
5. Day 11 화요일 휴관 경고 존재

## 검증 결과

| 검사 | 결과 |
|---|---|
| 정적 빌드 | 통과 · HTML 313개 |
| 43일 감사표 필수필드 | 통과 |
| 날짜·요일·거점 | 43일 통과 |
| P0 연결일 | 6일 유지 |
| Day 11 운영일 교정 | 통과 |
| Phase 1·3·4 회귀검사 | 통과 |
| 내부 링크 | 오류 0건 |
| 장소 레지스트리 | spot 82 · node 3 · 이상 없음 |

## 검증 제한과 다음 잠금

- 클라우드 브라우저는 로컬 주소를 `ERR_BLOCKED_BY_CLIENT`로 차단했다.
- Playwright Chromium 실행 파일이 현재 환경에 없어 320px·390px 시각 검사를 재실행하지 못했다.
- GitHub Pages 배포 후 공개 URL에서 Day 11 모바일 화면과 상세 실행 펼치기를 최종 확인해야 한다.
- Phase 8에서 항공·열차·숙소·렌터카·예약입장 시각과 주소를 실제 값으로 잠가야 Operational Complete가 된다.
