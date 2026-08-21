# Phase 8 Reservation and Operations Lock Register v1.0

## 결론

Phase 8의 **Known-Facts Lock**과 Girona 권역·Barcelona 숙소 예약 잠금을 반영했다. 다른 예약은 외부 입력이 없어 차단되어 있다.
현재 문서와 Tracker에 존재하지 않는 예약번호·편명·열차번호·결제금액·체크인 시간·주차·조식 조건을 임의 생성하지 않았다.

## 잠금 완료

- 43일·42박
- 8개 거점 숙박배분
- Nice 5박·Aix 4박
- 9/8 Nice 회복일
- 9/9 NCE 렌터카 인수 전제와 Aix 이동
- 9/21 Avignon TGV 반납·Lyon 이동 구조
- 10/9 Paris CDG 19:10 출국 확정 (OZ502 · 10/10 14:10 인천 도착)
- Sagrada Família 8/30 10:30 계획
- Peralada: 본 일정에서 제외·실제 예약 없음

## Barcelona 숙소 예약 확정

- 상태: 예약 확정 (2026-08-05)
- 일정: 2026-08-29 체크인 14:00–00:00 · 2026-09-01 체크아웃 12:00까지 · 3박
- 표시명: Occidental Barcelona 1929
- 주소: Carrer de la Creu Coberta, 20-22, 08014 Barcelona, Catalonia, Spain (Hostafrancs·Sants-Montjuïc)
- 전화: +34 936 26 88 44
- 여행자: Jason·Julia
- 채널: Trip.com · 확인번호 [CONFIRMED] (2026-08 바우처 대조 정정) · 예약번호 [CONFIRMED]
- 결제: 선결제 KRW 701,054 (VAT 포함) · 현장 결제 €46.2 (도시세 포함, 약 KRW 76,428)
- 무료취소기한: 재확인

## Girona 권역 숙소 예약 확정

- 상태: 예약 확정
- 일정: 2026-09-01 체크인 12:00 · 2026-09-04 체크아웃 11:00 · 3박
- 채널: Airbnb · 예약코드 [CONFIRMED]
- 가격: €330
- 표시명: 바스카라의 B&B
- 예약서 리스팅명·호스트: Torre de Báscara · Luc +34 622 66 14 31 (2026-08 예약서)
- 주소: Plaça de l'Església, 6, 17483 Bàscara
- 여행자: Jason·Julia
- 결제조건·주차·조식·취소조건: 재확인
- 운영 변경: Girona 시내 숙박이 아닌 Bàscara 농촌 거점으로 Day 4–7 출발·귀환 기준 변경

## Day 2·3 운영 재확인

- Day 2: Bàscara → Collioure → Cadaqués → Bàscara. Cadaqués는 직선 귀로가 아닌 해안 쪽 우회이며, Collioure·Cadaqués 주차와 당일 지도는 출발 전 재확인한다.
- Day 3: Bàscara → Tossa de Mar → Sant Feliu de Guíxols → Pals → Peratallada → Bàscara. Tossa Vila Vella 접근·주차, GI-682 해안도로, Peratallada 주차를 재확인한다.
- 비·강풍·멀미·운전 피로 시 Day 3은 Tossa → Sant Feliu → Bàscara로 축소하고, 운전자는 점심에 음주하지 않는다.

## 실제 예약 잠금에 필요한 입력

1. 국제선·Bàscara→Nice 이동수단과 차량 반납 상세
2. 두 렌터카 예약서
3. Avignon→Lyon, Lyon→Paris 열차표
4. 나머지 6개 숙소의 확정명·주소·예약번호·금액·취소기한
5. Bàscara 숙소의 결제조건·주차·조식·취소조건과 Barcelona 숙소의 무료취소기한
6. 핵심 입장권·공연·축구 예약정보
7. 여행자보험·통신

세부 상태는 `TP_Europe_Travel_Master_Tracker_v1.2.xlsx`의 `Phase8 Lock Status` 시트에서 관리한다.
