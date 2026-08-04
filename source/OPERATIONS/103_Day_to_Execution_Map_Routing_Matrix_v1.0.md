# 103. Day-to-Execution-Map Routing Matrix v1.0

| Day | 사용할 지도 | 핵심 범위 |
|---|---|---|
| 1–3 | Barcelona | Barcelona 시내 |
| 4 | Barcelona + Girona | Sants·Sitges·Girona 전환 |
| 5–6 | Bàscara | Day 5 Collioure·Cadaqués · Day 6 Tossa de Mar·Sant Feliu·Pals·Peratallada |
| 7 | Girona + Nice | BCN 반납·NCE 도착 |
| 8–11 | Nice | Nice·Cannes·Monaco |
| 12 | Nice + Aix | NCE·Saint-Paul·Grasse·Aix |
| 13–15 | Aix | Aix·Cassis |
| 16 | Aix + Luberon | Lourmarin·Coustellet·농가 |
| 17–19 | Luberon | Roussillon·Gordes·Ménerbes |
| 20 | Luberon + Avignon | L’Isle·Avignon |
| 21–23 | Avignon | Avignon·Uzès·Alpilles |
| 24 | Avignon + Lyon | Avignon TGV·Lyon |
| 25–27 | Lyon | Lyon·Annecy |
| 28 | Lyon + Paris | Lyon Part-Dieu·Paris |
| 29–43 | Paris | Paris 생활권·근교 |

## 전환일 원칙

두 지도를 함께 쓰는 Day 4, 7, 12, 16, 20, 24, 28은 출발지 지도에서 교통·반납·인수 지점을 확인하고, 도착지 지도에서 체크인 후보권역을 확인한다. 실제 문전 경로와 교통상황은 당일 Google Maps로 계산한다.
