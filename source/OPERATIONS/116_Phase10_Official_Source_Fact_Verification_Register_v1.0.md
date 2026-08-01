# 116. Phase 10 Official-Source Fact Verification Register v1.0

**검증일:** 2026-08-01  
**원칙:** 공식 운영기관·지자체·국립공원·관광기관의 현재 웹페이지를 우선한다.

## 상태 정의

| 상태 | 의미 |
|---|---|
| VERIFIED | 일정일에 적용 가능한 운영·방문정보 확인 |
| VERIFIED_CURRENT | 현재 확인됐으나 예약일 가격은 예약화면에서 다시 확정 |
| CORRECTED | 기존 문구 또는 숫자를 수정 |
| CONFLICT_RECHECK | 동일 기관 페이지 간 차이가 있어 날짜별 화면 재확인 필요 |
| DATE_GATE | 일정일 전날 또는 당일에만 확정 가능한 정보 |

## 공식자료 검증표

| ID | 지역 | 장소 | 항목 | 상태 | 확인내용 | 공식출처 | 조치 |
|---|---|---|---|---|---|---|---|
| F001 | Barcelona | Sagrada Família | 운영시간 | VERIFIED | 4–9월 월–금 09:00–20:00, 토 09:00–18:00, 일 10:30–20:00. 특별행사로 변경 가능. | [공식](https://sagradafamilia.org/en/schedules-how-to-get) | 8/29 도착 후 8/30 방문 전날 재확인 |
| F002 | Barcelona | Sagrada Família | 티켓 | CORRECTED | 공식 웹사이트 온라인 구매만 가능. 타워 포함 일반권은 현재 €36 표시. 기본권 가격은 실제 예약화면에서 확정. | [공식](https://sagradafamilia.org/en/tickets-individuals) | 기존 ‘기본권 약 €26’ 고정표현 제거 |
| F003 | Barcelona | Sant Pau | 운영·요금 | VERIFIED | 4–10월 매일 09:30–18:30, 마지막 입장 30분 전. 자유관람 45–60분. 일반 €18(14시 이전), €17(14시 이후). | [공식](https://santpaubarcelona.org/en/visita/visita-lliure/) | 8/30 현장 동선에 반영 |
| F004 | Barcelona | MACBA | 무료시간 | VERIFIED | 여름 목·금·토 18:00–20:00 무료, 매월 첫째 일요일 무료. 전시일정과 정규 운영시간은 당일 페이지 확인. | [공식](https://www.macba.cat/en/plan-your-visit/free-entrance-and-discount-admission/) | 8/31 월요일 방문의 정규 개관 여부 48시간 전 확인 |
| F005 | Barcelona | Cau Ferrat·Maricel | 운영·요금 | CONFLICT_RECHECK | 공식 Schedule 페이지는 4–10월 화–일 10:00–19:00, 월 휴관. 다른 공식 여름 안내는 7–9월 20:00까지 표기. 통합권 €12. | [공식](https://museusdesitges.cat/en/schedule) | 9/1 공식 티켓화면에서 최종 확인 |
| F006 | Girona | Girona Walls | 운영시간 | VERIFIED | 9–5월 08:00–21:00. 6–8월 08:00–23:00. | [공식](https://www.girona.cat/turisme/eng/monuments_muralla.php) | 9/1·9/3 일정과 일치 |
| F007 | Girona | Historic City | 역사 | VERIFIED | 로마 Força Vella와 14–15세기 중세 확장 성벽의 두 방어체계가 핵심. | [공식](https://www.girona.cat/turisme/eng/monuments.php) | 지역해설 유지 |
| F008 | Aix/Cassis | Calanques National Park | 접근·요금 | CORRECTED | 공원 입장은 무료. 연중 개방이 원칙이나 화재위험 red day에는 폐쇄. 6/1–9/30 접근금지 가능, 일부 도로 차량통제. | [공식](https://www.calanques-parcnational.fr/en/frequently-asked-questions) | 9/10 밤과 9/11 아침 My Calanques 확인 |
| F009 | Aix/Cassis | Calanques National Park | 안전 | VERIFIED | 육상접근 조건은 매일 변동. 충분한 물·장비가 필요하며 인기 해변에는 상점·급수·화장실·쓰레기통이 없음. | [공식](https://www.calanques-parcnational.fr/en/prepare-your-visit-calanques) | 보트 중심 기본안 유지 |
| F010 | Paris | Notre-Dame | 입장·예약 | CORRECTED | 성당 입장은 100% 무료. 공식사이트 외 유료티켓 판매자는 비공식. 예약은 선택이나 권장, 보통 전날·이틀 전·당일 슬롯 공개. | [공식](https://www.notredamedeparis.fr/en/visit/reservation-free/) | ‘사전 장기예약’ 표현 금지 |
| F011 | Paris | Notre-Dame | 접근 | VERIFIED | Cité역(M4), Saint-Michel역(M4/RER B·C). 전례가 관광보다 우선. | [공식](https://www.notredamedeparis.fr/en/visit/visitor-reception/) | 9/26 방문 전 예배일정 확인 |
| F012 | Paris | Versailles | 운영 | VERIFIED | 궁전은 월요일 휴관, 화–일 09:00 개장. Trianon은 12:00 개장. 4–10월 정원 유료행사일 존재. | [공식](https://en.chateauversailles.fr/plan-your-visit) | 10/3 토요일 시간지정 필수 |
| F013 | Paris | Versailles | 시간지정 | VERIFIED | Passport 시간지정 입장은 09:00–15:00 매시 슬롯, 예약시간 기준 30분 유효. | [공식](https://en.chateauversailles.fr/passport-timed-entry) | 09:00 슬롯 우선 |
| F014 | Paris | Versailles | 후반입장 가격 | VERIFIED_CURRENT | 고시즌 16:00 이후 Passport 우대가격 €28(EEA €25). 일반 Passport 정확한 가격은 날짜별 예약화면 확인. | [공식](https://ticket.chateauversailles.fr/en/ticketing) | 가격을 고정하지 않고 예약화면 캡처 |
| F015 | Paris | Notre-Dame Treasury | 요금 | VERIFIED | 성당 본당은 무료이나 Treasury는 일반 €12, 할인 €6. 현장판매, 온라인예약 없음. | [공식](https://www.notredamedeparis.fr/en/visit/visit-treasury/) | 본당과 Treasury 요금 구분 |
| F016 | Barcelona | Sitges Museums | 요금 | VERIFIED | Cau Ferrat+Maricel 일반 통합권 €12, Stämpfli 포함 결합권 €17. | [공식](https://museusdesitges.cat/en/fees) | 9/1 이동일은 €12 통합권 범위만 검토 |
| F017 | Barcelona | Sant Pau | 관람동선 | VERIFIED | Hypostyle Hall→지하터널→Sant Salvador Pavilion 순으로 병원역사와 Domènech i Montaner를 이해하는 공식 동선. | [공식](https://santpaubarcelona.org/en/visites/) | Sagrada 이후 60분 관람 |
| F018 | Barcelona | MACBA Library | 운영 | VERIFIED | 도서관은 월–목 10:00–19:00, 금–일 휴관. 8월 휴관, 9/1–15는 10:00–18:00 특별시간. | [공식](https://www.macba.cat/en/library/) | 8/31에는 8월 휴관이므로 도서관 일정 제외 |

## 범위와 한계

- 51개 장소의 역사·문화 설명은 Phase 9D에서 공식링크와 함께 정리했다.
- Phase 10에서는 일정에 영향을 크게 주는 시간·요금·휴관·접근·예약 조건을 우선 검증했다.
- 식당, 숙소, 공연, 축구, 실제 열차·항공은 예약정보가 없으므로 Phase 8B가 완료될 때까지 확정하지 않는다.
- Calanques 화재통제, 날씨, 파업, 열차운행은 고정정보가 아니므로 전날·당일 게이트로 관리한다.
