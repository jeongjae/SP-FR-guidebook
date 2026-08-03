# Phase 8 Reservation and Operations Lock Register v1.0

## 결론

Phase 8의 **Known-Facts Lock**과 Girona 권역 숙소 예약 잠금을 반영했다. 다른 예약은 외부 입력이 없어 차단되어 있다.
현재 문서와 Tracker에 존재하지 않는 예약번호·편명·열차번호·결제금액·체크인 시간·주차·조식 조건을 임의 생성하지 않았다.

## 잠금 완료

- 43일·42박
- 8개 거점 숙박배분
- Nice 5박·Aix 4박
- 9/8 Nice 회복일
- 9/9 NCE 렌터카 인수 전제와 Aix 이동
- 9/21 Avignon TGV 반납·Lyon 이동 구조
- 10/10 Paris 19:10 출국 계획
- Sagrada Família 8/30 10:30 계획
- Peralada 9/2 17:30 계획

## Girona 권역 숙소 예약 확정

- 상태: 예약 확정
- 일정: 2026-09-01 체크인 · 2026-09-04 체크아웃 · 3박
- 채널: Airbnb
- 표시명: 바스카라의 B&B
- 주소: 비공개 숙소 · 정확 주소는 개인 보관본에서 확인
- 여행자: Jason·Julia
- 확정번호·가격·결제조건·체크인 시간·주차·조식·취소조건: 재확인
- 운영 변경: Girona 시내 숙박이 아닌 Bàscara 농촌 거점으로 Day 4–7 출발·귀환 기준 변경

## 실제 예약 잠금에 필요한 입력

1. 국제선·Bàscara→Nice 이동수단과 차량 반납 상세
2. 두 렌터카 예약서
3. Avignon→Lyon, Lyon→Paris 열차표
4. 나머지 7개 숙소의 확정명·주소·예약번호·금액·취소기한
5. Bàscara 숙소의 확정번호·금액·결제·체크인·주차·조식·취소조건
6. 핵심 입장권·공연·축구 예약정보
7. 여행자보험·통신

세부 상태는 `TP_Europe_Travel_Master_Tracker_v1.2.xlsx`의 `Phase8 Lock Status` 시트에서 관리한다.
