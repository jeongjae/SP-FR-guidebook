#!/usr/bin/env python3
"""Sync Days 12 to 15 daily cards with Aix Cezanne redistribution and Marseille mandatory day trip."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAILY_CARDS = ROOT / "data" / "daily-cards"

def update_day_12():
    p = DAILY_CARDS / "day-12.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "08:00"
    d["endTime"] = "20:30"
    d["totalDuration"] = "12시간 30분"
    d["totalDistance"] = "약 204km · 차량 이동"
    d["fatigue"] = "4"
    d["transport"] = [
        "렌터카 — Nice역 09:00 인수 (확정 [CONFIRMED])",
        "A8 고속도로 및 프로방스 국도"
    ]
    d["stops"] = [
        {
            "id": "nice-checkout",
            "order": 1,
            "start": "08:00",
            "end": "08:45",
            "name": "Nice 숙소 체크아웃 — Palais ALZIRA",
            "category": "hotel",
            "lat": 43.7002,
            "lng": 7.2628,
            "summary": "12 Rue Verdi 체크아웃 후 Nice-Ville 기차역 Hertz 영업소로 도보 이동 (10분)",
            "menu": None,
            "reservation": "체크아웃 완료 (Airbnb [CONFIRMED])",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "nice-station-pickup",
            "order": 2,
            "start": "09:00",
            "end": "09:40",
            "name": "Nice-Ville역 Hertz 렌터카 인수",
            "category": "transport",
            "lat": 43.7047,
            "lng": 7.2619,
            "summary": "09:00 렌터카 인수(서류·차량촬영·내비설정). 수하물 트렁크 적재",
            "menu": None,
            "reservation": "예약확정 Hertz [CONFIRMED] — 9/9 09:00 인수",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "saint-paul",
            "order": 3,
            "start": "10:15",
            "end": "12:30",
            "name": "Saint-Paul-de-Vence",
            "category": "sight",
            "lat": 43.6969,
            "lng": 7.1222,
            "summary": "중세 성벽마을, 샤갈의 묘지, 예술가들의 골목 및 퐁다시옹 매그(Fondation Maeght) 외관 (2시간 15분)",
            "menu": "에스프레소, 크루아상",
            "reservation": "주차: Parking Indigo Saint-Paul-de-Vence (Primary)",
            "optional": False,
            "place_ref": "saint-paul-de-vence"
        },
        {
            "id": "grasse",
            "order": 4,
            "start": "13:15",
            "end": "14:30",
            "name": "Grasse 점심 & Fragonard 역사공장",
            "category": "food",
            "lat": 43.6586,
            "lng": 6.9242,
            "summary": "향수의 수도 그라스 테라스 점심 및 프라고나르 향수 역사공장 관람. 지연 시 우선 축소 가능",
            "menu": "프로방스 샐러드, 파니니",
            "reservation": "주차: Parking Notre Dame des Fleurs",
            "optional": True,
            "place_ref": "grasse"
        },
        {
            "id": "aix-checkin",
            "order": 5,
            "start": "16:45",
            "end": "18:00",
            "name": "Aix 숙소 체크인",
            "category": "hotel",
            "lat": 43.5283,
            "lng": 5.4497,
            "summary": "Aix 숙소 체크인(2 Place Coimbra, 15:00부터 가능). 짐 정리 및 차량 안전 주차",
            "menu": None,
            "reservation": "예약완료 Airbnb [CONFIRMED] — 체크인 9/9 15:00 · 체크아웃 9/13 14:00",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "rotonde",
            "order": 6,
            "start": "18:30",
            "end": "19:30",
            "name": "Place de la Rotonde & Cours Mirabeau 첫 산책",
            "category": "sight",
            "lat": 43.5263,
            "lng": 5.4454,
            "summary": "로통드 분수 및 쿠르 미라보 가로수길 첫 저녁 산책. 구시가지 지형 파악",
            "menu": None,
            "reservation": None,
            "optional": True,
            "place_ref": "rotonde"
        },
        {
            "id": "aix-stay-return",
            "order": 7,
            "start": "19:30",
            "end": "20:30",
            "name": "숙소권 저녁 식사 & 휴식",
            "category": "hotel",
            "lat": 43.5283,
            "lng": 5.4497,
            "summary": "숙소 인근 비스트로 저녁 식사 후 휴식",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "nice-checkout",
            "to": "nice-station-pickup",
            "mode": "walk",
            "duration": "약 10분",
            "distance": "1.0km"
        },
        {
            "from": "nice-station-pickup",
            "to": "saint-paul",
            "mode": "car",
            "duration": "약 30분",
            "distance": "18.7km"
        },
        {
            "from": "saint-paul",
            "to": "grasse",
            "mode": "car",
            "duration": "약 35분",
            "distance": "22.1km"
        },
        {
            "from": "grasse",
            "to": "aix-checkin",
            "mode": "car",
            "duration": "약 1시간 50분",
            "distance": "162.9km"
        },
        {
            "from": "aix-checkin",
            "to": "rotonde",
            "mode": "walk",
            "duration": "7분",
            "distance": "0.5km"
        },
        {
            "from": "rotonde",
            "to": "aix-stay-return",
            "mode": "walk",
            "duration": "7분",
            "distance": "0.5km"
        }
    ]
    d["backup"] = "렌터카 인수 지연 시 Grasse를 생략하고 Saint-Paul-de-Vence 관람 후 A8 고속도로를 통해 Aix로 직행"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 12")

def update_day_13():
    p = DAILY_CARDS / "day-13.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["title"] = "Aix 목요시장, Vieil Aix, 세잔 아틀리에와 Musée Granet"
    d["startTime"] = "08:30"
    d["endTime"] = "20:30"
    d["totalDuration"] = "12시간"
    d["totalDistance"] = "약 5km · 도보"
    d["fatigue"] = "3"
    d["transport"] = ["Aix 시내 도보 (구시가지 및 북부 아틀리에 도보권)"]
    d["stops"] = [
        {
            "id": "place-richelme-place-des-precheurs",
            "order": 1,
            "start": "08:30",
            "end": "10:00",
            "name": "Place Richelme & 목요 대형 시장",
            "category": "shopping",
            "lat": 43.5297,
            "lng": 5.4478,
            "summary": "리셸름 광장 식품시장, 프레셔 광장 꽃시장, 쿠르 미라보 공예시장 탐방 (08:00~13:00 운영 중 아침 활성화 시간대)",
            "menu": "프로방스 칼리송(Calisson), 제철 무화과, 에스프레소",
            "reservation": None,
            "optional": False,
            "place_ref": "place-richelme-place-des-precheurs"
        },
        {
            "id": "vieil-aix",
            "order": 2,
            "start": "10:00",
            "end": "11:45",
            "name": "Vieil Aix 구시가지 & 세잔의 흔적",
            "category": "sight",
            "lat": 43.5311,
            "lng": 5.4472,
            "summary": "17-18세기 귀족 저택(Hôtel Particulier), 생소뵈르 대성당, 네 마리 돌고래 분수, 세잔 탄생지/모교 흔적 도보 (105분)",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "vieil-aix"
        },
        {
            "id": "aix-lunch",
            "order": 3,
            "start": "12:00",
            "end": "13:15",
            "name": "구시가지 점심 식사",
            "category": "food",
            "lat": 43.5289,
            "lng": 5.4468,
            "summary": "구시가지 테라스 비스트로에서 프로방스식 점심 (La Brocherie 또는 Coucou 인근)",
            "menu": "도브 프로방살(소고기 스튜), 팍시, 로제 와인",
            "reservation": "현장 방문 또는 점심 예약 권장",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "atelier-des-lauves",
            "order": 4,
            "start": "13:30",
            "end": "15:00",
            "name": "Atelier des Lauves (세잔의 아틀리에)",
            "category": "culture",
            "lat": 43.5392,
            "lng": 5.4461,
            "summary": "폴 세잔이 생애 마지막 4년간(1902-1906) 대형 목욕자들과 생트빅투아르산을 그리던 작업실. 정물화 소품, 대형 이젤, 올리브 정원 [Cézanne Core]",
            "menu": None,
            "reservation": "사전 예약 필수 (Aix Tourism / €9.50)",
            "optional": False,
            "place_ref": "atelier-des-lauves"
        },
        {
            "id": "musee-granet",
            "order": 5,
            "start": "15:30",
            "end": "17:15",
            "name": "Musée Granet (그라네 미술관)",
            "category": "culture",
            "lat": 43.5258,
            "lng": 5.4522,
            "summary": "세잔의 초기작 및 유화/수채화 컬렉션, 프랑수아 마리우스 그라네, 인상파 회화 컬렉션 (105분 compact visit)",
            "menu": None,
            "reservation": "현장 발권 / 뮤지엄 패스 (€8)",
            "optional": False,
            "place_ref": "musee-granet"
        },
        {
            "id": "cours-mirabeau",
            "order": 6,
            "start": "17:30",
            "end": "19:30",
            "name": "Cours Mirabeau & 마자랭 지구 산책",
            "category": "sight",
            "lat": 43.5269,
            "lng": 5.4486,
            "summary": "플라타너스 가로수길 카페(Les Deux Garçons 터) 테라스 휴식 및 Quartier Mazarin 분수 산책 후 저녁 식사",
            "menu": "테라스 와인/맥주, 프로방스 타파스",
            "reservation": None,
            "optional": False,
            "place_ref": "cours-mirabeau"
        },
        {
            "id": "aix-stay-return",
            "order": 7,
            "start": "19:30",
            "end": "20:30",
            "name": "숙소 귀환 & 휴식",
            "category": "hotel",
            "lat": 43.5283,
            "lng": 5.4497,
            "summary": "숙소 2 Place Coimbra 귀환 및 휴식",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "place-richelme-place-des-precheurs",
            "to": "vieil-aix",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.3km"
        },
        {
            "from": "vieil-aix",
            "to": "aix-lunch",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.3km"
        },
        {
            "from": "aix-lunch",
            "to": "atelier-des-lauves",
            "mode": "walk",
            "duration": "20분 (오르막)",
            "distance": "1.3km"
        },
        {
            "from": "atelier-des-lauves",
            "to": "musee-granet",
            "mode": "walk",
            "duration": "25분 (내리막)",
            "distance": "1.6km"
        },
        {
            "from": "musee-granet",
            "to": "cours-mirabeau",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.3km"
        },
        {
            "from": "cours-mirabeau",
            "to": "aix-stay-return",
            "mode": "walk",
            "duration": "10분",
            "distance": "0.6km"
        }
    ]
    d["backup"] = "1. Atelier des Lauves 예약 시간에 맞춰 오전/오후 순서 미세 조정\n2. 피로 누적 시 Musée Granet을 60분으로 압축하고 Cours Mirabeau 카페 휴식 확대\n3. 우천 시 야외 도보를 줄이고 Granet 미술관 및 구시가지 실내 카페 중심 진행"
    d["needsReview"] = [
        "Atelier des Lauves 사전 예약 확정 (방문 시간대 지정)",
        "Musée Granet 2026 특별전 확인",
        "Aix 목요시장 08:00~13:00 운영 확인"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 13")

def update_day_14():
    p = DAILY_CARDS / "day-14.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["title"] = "Cassis & Calanques — 석회암 절벽과 지중해"
    d["startTime"] = "08:30"
    d["endTime"] = "20:30"
    d["totalDuration"] = "12시간"
    d["totalDistance"] = "약 100km · 차량 왕복 + 보트"
    d["fatigue"] = "3"
    d["transport"] = [
        "차량 왕복 (Aix ↔ Cassis, A52/A50 고속도로 48km)",
        "Cassis Presqu'île 또는 Gorguettes 주차",
        "칼랑크 유람선 (Cassis 항구 출발)"
    ]
    d["stops"] = [
        {
            "id": "aix-depart",
            "order": 1,
            "start": "08:30",
            "end": "09:00",
            "name": "Aix 숙소 출발 — 렌터카",
            "category": "hotel",
            "lat": 43.5283,
            "lng": 5.4497,
            "summary": "Aix 숙소 출발하여 A52 고속도로 경유 카시스로 이동 (48km, 35분)",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "cassis-parking",
            "order": 2,
            "start": "09:35",
            "end": "10:00",
            "name": "Cassis 도착 & 주차",
            "category": "transport",
            "lat": 43.2147,
            "lng": 5.5342,
            "summary": "Parking de la Presqu'île (Primary, 포르미우 방면) 또는 Parking des Gorguettes (Backup) 주차",
            "menu": None,
            "reservation": "주차 요금 현장 결제",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "calanques",
            "order": 3,
            "start": "10:15",
            "end": "12:15",
            "name": "Calanques 국립공원 유람선 투어",
            "category": "sight",
            "lat": 43.2131,
            "lng": 5.5386,
            "summary": "카시스 항구에서 유람선 탑승. Port-Miou, Port-Pin, En-Vau의 백색 석회암 피오르드 해상 관람 (2시간)",
            "menu": None,
            "reservation": "현장 발권 / 사전 예매 권장",
            "optional": False,
            "place_ref": "calanques"
        },
        {
            "id": "cassis",
            "order": 4,
            "start": "12:30",
            "end": "14:00",
            "name": "Cassis 항구 해산물 점심",
            "category": "food",
            "lat": 43.2144,
            "lng": 5.5375,
            "summary": "파스텔 가옥이 늘어선 카시스 구항구 테라스 레스토랑에서 신선한 지중해 해산물 점심",
            "menu": "문어 샐러드, 도미 구이, 카시스 화이트 와인(AOC Cassis)",
            "reservation": "현장 선택",
            "optional": False,
            "place_ref": "cassis"
        },
        {
            "id": "cassis-port-miou",
            "order": 5,
            "start": "14:15",
            "end": "15:45",
            "name": "Port-Miou 해안 트레일 초입 산책",
            "category": "sight",
            "lat": 43.2119,
            "lng": 5.5203,
            "summary": "요트가 정박한 포르미우 칼랑크 해안 소나무 산책로 도보 (선택)",
            "menu": None,
            "reservation": None,
            "optional": True,
            "place_ref": None
        },
        {
            "id": "aix-return",
            "order": 6,
            "start": "16:00",
            "end": "17:00",
            "name": "Cassis ➔ Aix 귀환 (차량)",
            "category": "transport",
            "lat": 43.5283,
            "lng": 5.4497,
            "summary": "A52 고속도로를 통해 Aix로 복귀 (35분 소요)",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "aix-stay-return",
            "order": 7,
            "start": "17:30",
            "end": "20:30",
            "name": "숙소 귀환 & 저녁",
            "category": "hotel",
            "lat": 43.5283,
            "lng": 5.4497,
            "summary": "숙소 휴식 및 익일 Day 15 마르세유 당일치기(기차 이동) 준비",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "aix-depart",
            "to": "cassis-parking",
            "mode": "car",
            "duration": "35분",
            "distance": "48.0km"
        },
        {
            "from": "cassis-parking",
            "to": "calanques",
            "mode": "walk",
            "duration": "15분",
            "distance": "1.0km"
        },
        {
            "from": "calanques",
            "to": "cassis",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.3km"
        },
        {
            "from": "cassis",
            "to": "cassis-port-miou",
            "mode": "walk",
            "duration": "15분",
            "distance": "1.2km"
        },
        {
            "from": "cassis-port-miou",
            "to": "aix-return",
            "mode": "car",
            "duration": "35분",
            "distance": "48.0km"
        },
        {
            "from": "aix-return",
            "to": "aix-stay-return",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.3km"
        }
    ]
    d["backup"] = "강풍/기상 악화로 보트 결항 시 마르세유로 이동하지 않고(익일 방문), 카시스 구시가지 골목 산책 및 Cap Canaille / Route des Crêtes 절벽 파노라마 드라이브로 대체"
    d["needsReview"] = [
        "전날 저녁 부슈뒤론 산불위험 예보 확인 (도보 트레일 진입 허용 여부)",
        "카시스 유람선 운항 여부 및 주차장 잔여면 확인"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 14")

def update_day_15():
    p = DAILY_CARDS / "day-15.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["city"] = "Marseille"
    d["title"] = "마르세유 전일 당일치기 — 구항구·르 파니에·Mucem·노트르담 대성당"
    d["startTime"] = "08:30"
    d["endTime"] = "20:30"
    d["totalDuration"] = "12시간"
    d["totalDistance"] = "TER 왕복 + 마르세유 시내 대중교통/도보 약 6km"
    d["fatigue"] = "4"
    d["transport"] = [
        "TER 기차 왕복 (Aix-en-Provence ↔ Marseille Saint-Charles, 36~45분)",
        "RTM 버스 60번 (Vieux-Port ↔ Notre-Dame de la Garde 직통)",
        "마르세유 시내 도보 (Vieux-Port ➔ Le Panier ➔ Fort Saint-Jean ➔ Mucem)"
    ]
    d["map"] = {"zoom": 13, "center": [43.2965, 5.3698], "routeCache": None}
    d["stops"] = [
        {
            "id": "aix-station",
            "order": 1,
            "start": "08:30",
            "end": "09:30",
            "name": "Aix-en-Provence역 출발 ➔ Marseille 이동 (TER)",
            "category": "transport",
            "lat": 43.5233,
            "lng": 5.4467,
            "summary": "숙소에서 도보 10분 이동 후 08:50 전후 TER 탑승. 생샤를 역 09:30 도착 (36분 소요, 생샤를 역 대계단 파노라마 조망)",
            "menu": None,
            "reservation": "SNCF Connect (30분 간격 배차 / 유연한 탑승)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "vieux-port-marseille",
            "order": 2,
            "start": "09:45",
            "end": "10:30",
            "name": "Vieux-Port (마르세유 구항구)",
            "category": "sight",
            "lat": 43.2951,
            "lng": 5.3744,
            "summary": "라 카네비에르(La Canebière)를 지나 노먼 포스터의 거울 그늘막(L'Ombrière), 토요 아침 활기찬 전통 어시장(Marché aux Poissons) 및 항만 풍경",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "vieux-port-marseille"
        },
        {
            "id": "le-panier",
            "order": 3,
            "start": "10:30",
            "end": "11:45",
            "name": "Le Panier (르 파니에 역사 골목)",
            "category": "sight",
            "lat": 43.2981,
            "lng": 5.3678,
            "summary": "마르세유에서 가장 오래된 역사 지구. 생로랑 성당, 비에유 샤리테(Vieille Charité) 외관, 골목 그래피티와 파스텔톤 가옥 (75분 도보)",
            "menu": "나베트(Navette, 오렌지꽃 향 전통 비스킷)",
            "reservation": None,
            "optional": False,
            "place_ref": "le-panier"
        },
        {
            "id": "fort-saint-jean",
            "order": 4,
            "start": "12:00",
            "end": "13:45",
            "name": "Fort Saint-Jean & Mucem (유럽지중해문명박물관)",
            "category": "culture",
            "lat": 43.2969,
            "lng": 5.3611,
            "summary": "생장 요새 성벽 정원 ➔ 공중 보행교(Footbridge) ➔ 뤼디 리치오티 설계의 Mucem 격자 건축 및 상설전/지중해 전망 (105분). 토요일 정상 개관(10:00~19:00)",
            "menu": None,
            "reservation": "Mucem 입장권 현장 (€11) / 요새 정원 무료",
            "optional": False,
            "place_ref": "mucem"
        },
        {
            "id": "marseille-lunch",
            "order": 5,
            "start": "13:45",
            "end": "15:00",
            "name": "Vieux-Port / Mucem 해산물 점심",
            "category": "food",
            "lat": 43.2958,
            "lng": 5.3672,
            "summary": "구항구 테라스 비스트로에서 신선한 구운 생선(Loup/Daurade) 또는 프로방스식 해산물 점심",
            "menu": "오늘의 생선 구이, 수프 드 푸아송(생선 수프), 지중해 샐러드",
            "reservation": "현장 선택",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "notre-dame-de-la-garde",
            "order": 6,
            "start": "15:15",
            "end": "17:00",
            "name": "Notre-Dame de la Garde (노트르담 드 라 가르드)",
            "category": "sight",
            "lat": 43.2842,
            "lng": 5.3714,
            "summary": "Vieux-Port에서 RTM 버스 60번 탑승(직통 15분). 해발 149m 정상 대성당, 황금 성모상, 선원들의 봉헌화(Ex-voto) 및 마르세유 360도 전경 조망 (90분)",
            "menu": None,
            "reservation": "무료 입장 (RTM 버스 1회권 €1.70)",
            "optional": False,
            "place_ref": "notre-dame-de-la-garde"
        },
        {
            "id": "vallon-des-auffes",
            "order": 7,
            "start": "17:15",
            "end": "18:15",
            "name": "Vallon des Auffes & 코르니슈 (선택)",
            "category": "sight",
            "lat": 43.2856,
            "lng": 5.3528,
            "summary": "다리 아래 전통 목선이 정박한 그림 같은 어촌 포구 산책. 피로 시 생략하고 구항구 카페 휴식",
            "menu": None,
            "reservation": None,
            "optional": True,
            "place_ref": None
        },
        {
            "id": "marseille-station",
            "order": 8,
            "start": "18:45",
            "end": "19:30",
            "name": "Marseille Saint-Charles역 복귀 ➔ Aix TER 탑승",
            "category": "transport",
            "lat": 43.3028,
            "lng": 5.3806,
            "summary": "생샤를역 복귀 후 Aix행 TER 열차 탑승 (36분 소요)",
            "menu": None,
            "reservation": "SNCF Connect",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "aix-stay-return",
            "order": 9,
            "start": "19:45",
            "end": "20:30",
            "name": "Aix 숙소 귀환 & 익일 Luberon 이동 준비",
            "category": "hotel",
            "lat": 43.5283,
            "lng": 5.4497,
            "summary": "20:15 숙소 귀환. 익일 Day 16 뤼베롱 농가 숙소 이동(08:00 체크아웃)을 위한 짐 정리, 주유 및 조기 취침",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "aix-station",
            "to": "vieux-port-marseille",
            "mode": "train",
            "duration": "TER 36분 + 도보 12분",
            "distance": "약 32km"
        },
        {
            "from": "vieux-port-marseille",
            "to": "le-panier",
            "mode": "walk",
            "duration": "8분",
            "distance": "0.5km"
        },
        {
            "from": "le-panier",
            "to": "fort-saint-jean",
            "mode": "walk",
            "duration": "8분",
            "distance": "0.5km"
        },
        {
            "from": "fort-saint-jean",
            "to": "marseille-lunch",
            "mode": "walk",
            "duration": "10분",
            "distance": "0.6km"
        },
        {
            "from": "marseille-lunch",
            "to": "notre-dame-de-la-garde",
            "mode": "bus",
            "duration": "RTM 버스 60번 약 15분",
            "distance": "약 2.5km"
        },
        {
            "from": "notre-dame-de-la-garde",
            "to": "vallon-des-auffes",
            "mode": "bus",
            "duration": "버스/도보 약 20분",
            "distance": "약 2.0km"
        },
        {
            "from": "vallon-des-auffes",
            "to": "marseille-station",
            "mode": "bus",
            "duration": "버스 83번 + 지하철 M1 약 25분",
            "distance": "약 3.8km"
        },
        {
            "from": "marseille-station",
            "to": "aix-stay-return",
            "mode": "train",
            "duration": "TER 36분 + 도보 10분",
            "distance": "약 32km"
        }
    ]
    d["backup"] = "1. 우천 시: Vieux-Port/Le Panier 도보를 단축하고 Mucem 상설/특별전 관람을 2.5시간으로 확대\n2. 폭염 시: 야외 보행을 줄이고 점심 후 RTM 버스 60번으로 노트르담 대성당 이동\n3. TER 지연/파행 시: Aix ↔ Marseille L50 직행 버스 코치(Gare Routière) 백업 활용\n4. 피로 시: Vallon des Auffes를 생략하고 Vieux-Port 카페 휴식 후 18:00 조기 귀환"
    d["needsReview"] = [
        "Aix ↔ Marseille Saint-Charles TER 토요일 시간표 확인 (30분 간격)",
        "Mucem 토요일 운영(10:00~19:00) 및 RTM 버스 60번 노선 확인",
        "익일 Day 16 뤼베롱 이동 준비 (08:00 체크아웃)"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 15 (Marseille Mandatory Full-Day Trip)")

if __name__ == "__main__":
    update_day_12()
    update_day_13()
    update_day_14()
    update_day_15()
