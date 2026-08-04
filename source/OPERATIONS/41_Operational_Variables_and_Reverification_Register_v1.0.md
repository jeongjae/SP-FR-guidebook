---
title: "Operational Variables & Reverification Register"
version: "1.0"
updated: "2026-08-01"
status: "active"
---

# 41. 변동정보·재확인 등록부 v1.0

## 1. 목적

지역 원고의 서사와 선택기준은 유지하되, 시간이 지나면 바뀌는 정보를 본문에서 분리해 관리한다. 아래 항목은 **확정 사실이 아니라 예약·출발 전 잠금 대상**이다.

## 2. 전 여행 P0

| 범주 | 잠금 대상 | 반영 위치 | 상태 |
|---|---|---|---|
| 항공 | BCN 도착편, BCN→NCE, CDG→ICN 터미널·시각·수하물 | Master Itinerary·예약카드 | 예약값 대기 |
| Spain 렌터카 | 9/1 Sants 인수, 국경조건, Girona/BCN 반납 | Barcelona·Girona | 예약값 대기 |
| France 렌터카 | 9/8 NCE T2 인수, 9/21 Avignon TGV 반납 | Nice~Avignon | 예약값 대기 |
| TGV | Avignon→Lyon, Lyon→Paris | Avignon·Lyon·Paris | 예약값 대기 |
| 숙소 | 8개 거점 주소·객실·총액·취소기한·체크인 | 전 챕터 | 후보단계 |
| 핵심 티켓 | Sagrada, Palais des Papes, Louvre, Orsay, Grand Palais | 해당 챕터 | 판매창 확인 |

## 3. 지역별 P1

| 지역 | 재확인 항목 | 최종 확인시점 |
|---|---|---|
| Barcelona | Sagrada 입장, Sant Pau 전시, MACBA 월요일, 렌터카 영업소 | 예약 시·7일 전 |
| Bàscara·Girona | Bàscara 숙소 주차·체크인/아웃, Collioure·Cadaqués 주차, Tossa·Peratallada 주차, GI-682, Bàscara→Nice 이동 | 14일 전·전날 |
| Nice | Cannes·Monaco TER, 9/8 렌터카, Saint-Paul·Grasse 영업 | 7일 전·당일 |
| Aix | Cassis 보트·바람, Marseille L50, Cézanne 시설, 행사 | 7일 전·전날 |
| Luberon | 농가 재고·도로·주방·세탁, 시장일, 행사 | 예약 시·3일 전 |
| Avignon | Palais 시간지정, Uzès 시장, Pont du Gard, TGV 반납 | 예약 시·전날 |
| Lyon | Annecy 직행 TER, 크루즈, 숙소·야간귀가 | 7일 전·전날 |
| Paris | 특별전·공연·PSG, Versailles·Giverny, Navigo 정책 | 판매창·7일 전 |

## 4. P2 생활정보

- 식당 휴무·여름휴가·예약정책
- 수영장 자유수영 레인·일일권·수영복 규정
- gym 체험권과 여권 요구
- 시장 임시휴장·축제에 따른 이전
- 산불·폭염·미스트랄·강풍·보트 운항
- 지하철·철도 공사·파업·대체교통

## 5. 편집 규칙

1. 잠금 전 숫자에는 `계획범위`, `예정`, `재확인`을 붙인다.
2. 예약 완료 후 지역 챕터·Master Itinerary·Booking Tracker 세 곳을 동시에 갱신한다.
3. 예약번호·결제정보는 공개용 Reader Edition에 넣지 않고 별도 비공개 실행부록에 둔다.
4. 출발 4주·2주·3일 전 세 번 재검증한다.
