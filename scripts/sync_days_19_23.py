#!/usr/bin/env python3
"""Sync Days 19 to 23 daily cards with Avignon, Uzes, Pont du Gard, Arles, and TGV to Lyon."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAILY_CARDS = ROOT / "data" / "daily-cards"

def update_day_19():
    p = DAILY_CARDS / "day-19.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "09:30"
    d["endTime"] = "20:30"
    d["totalDuration"] = "11시간"
    d["totalDistance"] = "약 35km · 차량 이동"
    d["fatigue"] = "3"
    d["transport"] = [
        "렌터카 (Domaine des Peyre ➔ Avignon 성벽 주차장)",
        "아비뇽 시내 도보"
    ]
    d["stops"] = [
        {
            "id": "farm-checkout",
            "order": 1,
            "start": "09:30",
            "end": "10:30",
            "name": "농가 숙소 체크아웃 & 출발",
            "category": "hotel",
            "lat": 43.87088,
            "lng": 5.12202,
            "summary": "Domaine des Peyre 체크아웃 후 차량 짐 적재. D900/N100 도로를 통해 아비뇽으로 이동 (35km, 약 40분)",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "avignon-parking-lunch",
            "order": 2,
            "start": "11:30",
            "end": "14:00",
            "name": "Avignon 주차 & 구시가지 점심",
            "category": "food",
            "lat": 43.9493,
            "lng": 4.8061,
            "summary": "Parking des Halles 또는 Parking Palais des Papes 관리 지하주차장 입차 후 레 알 인근 비스트로 점심",
            "menu": "프로방스 타르트, 샐러드, 에스프레소",
            "reservation": "주차: Parking des Halles (Primary) / Parking Palais des Papes (Backup)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "avignon-checkin",
            "order": 3,
            "start": "14:30",
            "end": "16:00",
            "name": "Avignon 숙소 체크인",
            "category": "hotel",
            "lat": 43.94993,
            "lng": 4.81302,
            "summary": "숙소 체크인 (15:00부터 가능). 짐 하역 및 객실 정리",
            "menu": None,
            "reservation": "숙소 예약/후보 (La Terrasse du Clocher 인근)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "teinturiers-walls",
            "order": 4,
            "start": "16:30",
            "end": "18:30",
            "name": "Rue des Teinturiers & 성벽 오리엔테이션",
            "category": "sight",
            "lat": 43.9458,
            "lng": 4.8133,
            "summary": "물레방아가 돌아가는 염색공의 거리(Rue des Teinturiers), 시계탑 광장(Place de l'Horloge), 14세기 아비뇽 석조 성벽 둘레길 산책",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "palais-des-papes"
        },
        {
            "id": "avignon-return",
            "order": 5,
            "start": "19:00",
            "end": "20:30",
            "name": "아비뇽 첫 저녁 & 휴식",
            "category": "hotel",
            "lat": 43.94993,
            "lng": 4.81302,
            "summary": "구시가지 테라스 저녁 식사 후 숙소 귀환",
            "menu": "프로방스식 양고기 구이, 로컬 론 와인(AOC Côtes du Rhône)",
            "reservation": "현장 선택",
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "farm-checkout",
            "to": "avignon-parking-lunch",
            "mode": "car",
            "duration": "약 40분",
            "distance": "35.0km"
        },
        {
            "from": "avignon-parking-lunch",
            "to": "avignon-checkin",
            "mode": "walk",
            "duration": "8분",
            "distance": "0.5km"
        },
        {
            "from": "avignon-checkin",
            "to": "teinturiers-walls",
            "mode": "walk",
            "duration": "8분",
            "distance": "0.6km"
        },
        {
            "from": "teinturiers-walls",
            "to": "avignon-return",
            "mode": "walk",
            "duration": "10분",
            "distance": "0.7km"
        }
    ]
    d["backup"] = "피로 시 성벽 외곽 산책을 생략하고 숙소권 카페 휴식 위주 오리엔테이션 진행"
    d["needsReview"] = [
        "Avignon 성벽 내 차량 진입 제한 및 Parking des Halles 입차 확인",
        "숙소 체크인 시각(15:00) 확인"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 19")

def update_day_20():
    p = DAILY_CARDS / "day-20.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "08:30"
    d["endTime"] = "21:00"
    d["totalDuration"] = "12시간 30분"
    d["totalDistance"] = "약 4.5km · 도보"
    d["fatigue"] = "3"
    d["transport"] = ["아비뇽 구시가지 도보 (성벽 내 압축권)"]
    d["stops"] = [
        {
            "id": "les-halles",
            "order": 1,
            "start": "08:30",
            "end": "09:30",
            "name": "Les Halles d'Avignon 아침 시장",
            "category": "shopping",
            "lat": 43.9483,
            "lng": 4.8108,
            "summary": "수직 정원 파사드가 유명한 중앙 실내시장. 신선한 과일, 치즈, 에스프레소",
            "menu": "치즈 크루아상, 에스프레소, 무화과",
            "reservation": None,
            "optional": False,
            "place_ref": "les-halles"
        },
        {
            "id": "palais",
            "order": 2,
            "start": "09:45",
            "end": "12:15",
            "name": "Palais des Papes (교황청 궁전)",
            "category": "culture",
            "lat": 43.9508,
            "lng": 4.8075,
            "summary": "14세기 아비뇽 유수기 거대한 고딕 교황궁. 히스토패드(Histopad) 3D 증강현실 관람, 대예배당, 생마르샬 예배당 프레스코화 (2시간 30분 집중 관람)",
            "menu": None,
            "reservation": "사전 시간지정 예약 필수 (€12 / 결합권 €14.50)",
            "optional": False,
            "place_ref": "palais-des-papes"
        },
        {
            "id": "palais-lunch",
            "order": 3,
            "start": "12:15",
            "end": "13:45",
            "name": "교황청 광장 비스트로 점심",
            "category": "food",
            "lat": 43.9501,
            "lng": 4.8068,
            "summary": "교황청 광장 인근 테라스 레스토랑에서 프로방스식 점심 식사",
            "menu": "생선 수프, 오리 콩피, 론 화이트 와인",
            "reservation": "현장 선택",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "rocher-doms",
            "order": 4,
            "start": "14:00",
            "end": "15:00",
            "name": "Rocher des Doms (돔 바위 정원)",
            "category": "sight",
            "lat": 43.9525,
            "lng": 4.8078,
            "summary": "교황청 북쪽 바위 언덕 위의 고즈넉한 정원. 론 강, 생베네제 다리, 빌뇌브레자비뇽 성채 파노라마 조망 (60분)",
            "menu": None,
            "reservation": "무료 입장",
            "optional": False,
            "place_ref": "rocher-des-doms"
        },
        {
            "id": "pont",
            "order": 5,
            "start": "15:15",
            "end": "16:45",
            "name": "Pont Saint-Bénézet (아비뇽 다리)",
            "category": "sight",
            "lat": 43.9539,
            "lng": 4.8047,
            "summary": "노래 '아비뇽 다리 위에서'로 유명한 12세기 미완의 다리. 생니콜라 예배당 및 론 강변 조망 (90분)",
            "menu": None,
            "reservation": "교황청 결합권 이용",
            "optional": False,
            "place_ref": "pont-saint-benezet"
        },
        {
            "id": "vieil-avignon",
            "order": 6,
            "start": "17:00",
            "end": "18:30",
            "name": "Vieil Avignon 구시가지 산책",
            "category": "sight",
            "lat": 43.9489,
            "lng": 4.8083,
            "summary": "생피에르 성당의 화려한 고딕 목조 문, Rue des Marchands 부티크 거리 산책",
            "menu": None,
            "reservation": None,
            "optional": True,
            "place_ref": None
        },
        {
            "id": "avignon-return",
            "order": 7,
            "start": "19:30",
            "end": "21:00",
            "name": "아비뇽 저녁 식사 & 숙소 귀환",
            "category": "hotel",
            "lat": 43.94993,
            "lng": 4.81302,
            "summary": "구시가지 레스토랑(SEVIN 또는 La Fourchette) 저녁 식사 후 숙소 귀환",
            "menu": None,
            "reservation": "저녁 예약 권장",
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "les-halles",
            "to": "palais",
            "mode": "walk",
            "duration": "10분",
            "distance": "0.5km"
        },
        {
            "from": "palais",
            "to": "palais-lunch",
            "mode": "walk",
            "duration": "3분",
            "distance": "0.1km"
        },
        {
            "from": "palais-lunch",
            "to": "rocher-doms",
            "mode": "walk",
            "duration": "8분 (오르막)",
            "distance": "0.3km"
        },
        {
            "from": "rocher-doms",
            "to": "pont",
            "mode": "walk",
            "duration": "8분 (내리막)",
            "distance": "0.3km"
        },
        {
            "from": "pont",
            "to": "vieil-avignon",
            "mode": "walk",
            "duration": "10분",
            "distance": "0.6km"
        },
        {
            "from": "vieil-avignon",
            "to": "avignon-return",
            "mode": "walk",
            "duration": "8분",
            "distance": "0.5km"
        }
    ]
    d["backup"] = "우천 또는 폭염 시 야외 다리/성벽 도보를 축소하고 교황청 내부 관람 및 실내 미술관(Petit Palais) 중심 진행"
    d["needsReview"] = [
        "Palais des Papes 사전 시간지정(09:45) 예약 필수",
        "Palais + Pont Saint-Bénézet 결합 티켓 구매"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 20")

def update_day_21():
    p = DAILY_CARDS / "day-21.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "08:30"
    d["endTime"] = "20:00"
    d["totalDuration"] = "11시간 30분"
    d["totalDistance"] = "약 84km · 차량 이동"
    d["fatigue"] = "3"
    d["transport"] = [
        "렌터카 (Avignon ↔ Uzès ↔ Pont du Gard ↔ Avignon)",
        "외곽 전용 주차장 (Parking Cordeliers / Pont du Gard Rive Gauche)"
    ]
    d["stops"] = [
        {
            "id": "avignon-depart",
            "order": 1,
            "start": "08:30",
            "end": "09:15",
            "name": "Avignon 숙소 출발 ➔ Uzès 이동",
            "category": "hotel",
            "lat": 43.94993,
            "lng": 4.81302,
            "summary": "주차장에서 출차 후 D981 도로를 통해 위제스로 이동 (40.7km, 약 45분)",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "uzes",
            "order": 2,
            "start": "09:30",
            "end": "12:15",
            "name": "Uzès 구시가지 & 에르브 광장",
            "category": "sight",
            "lat": 44.0122,
            "lng": 4.4197,
            "summary": "프랑스 최초의 공작령 도시. Place aux Herbes 아치 회랑 광장, 공작성(Duché d'Uzès) 외관, 페네스트렐 탑(Tour Fenestrelle) 조망 (2시간 45분)",
            "menu": "프로방스 빵, 에스프레소",
            "reservation": "주차: Parking Cordeliers (Primary) / Parking Gide (Backup)",
            "optional": False,
            "place_ref": "uzes"
        },
        {
            "id": "uzes-lunch",
            "order": 3,
            "start": "12:15",
            "end": "13:30",
            "name": "위제스 광장 테라스 점심",
            "category": "food",
            "lat": 44.0125,
            "lng": 4.4201,
            "summary": "Place aux Herbes 광장 플라타너스 그늘 아래 테라스 레스토랑 점심",
            "menu": "타르틴, 샐러드 니스와즈, 로컬 가르 와인",
            "reservation": "현장 선택",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "pont-du-gard",
            "order": 4,
            "start": "14:15",
            "end": "17:00",
            "name": "Pont du Gard (퐁 뒤 가르 수로교)",
            "category": "sight",
            "lat": 43.9475,
            "lng": 4.5350,
            "summary": "기원전 1세기 고대 로마 3층 수로교(높이 49m). 좌안(Rive Gauche) 대형 주차장 이용 ➔ 박물관 관람 ➔ 수로교 도보 횡단 ➔ 가르동 강변 자갈밭 전경 조망 (2시간 45분). [주의] 그늘 부족, 모자/생수 필수",
            "menu": None,
            "reservation": "주차/입장권 (€9.50/차량 포함) / Left Bank (Rive Gauche) 주차장",
            "optional": False,
            "place_ref": "pont-du-gard"
        },
        {
            "id": "avignon-return",
            "order": 5,
            "start": "18:00",
            "end": "20:00",
            "name": "Avignon 복귀 & 저녁",
            "category": "hotel",
            "lat": 43.94993,
            "lng": 4.81302,
            "summary": "D907 도로를 통해 아비뇽으로 복귀 (30km, 40분). 차량 안전 주차 후 저녁 식사",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "avignon-depart",
            "to": "uzes",
            "mode": "car",
            "duration": "약 45분",
            "distance": "40.7km"
        },
        {
            "from": "uzes",
            "to": "uzes-lunch",
            "mode": "walk",
            "duration": "2분",
            "distance": "0.1km"
        },
        {
            "from": "uzes-lunch",
            "to": "pont-du-gard",
            "mode": "car",
            "duration": "약 20분",
            "distance": "14.0km"
        },
        {
            "from": "pont-du-gard",
            "to": "avignon-return",
            "mode": "car",
            "duration": "약 40분",
            "distance": "29.5km"
        }
    ]
    d["backup"] = "폭염 또는 악천후 시 Pont du Gard 야외 체류를 60분으로 단축하고 실내 박물관 중심 관람 후 아비뇽 조기 복귀"
    d["needsReview"] = [
        "Pont du Gard 좌안(Rive Gauche) 주차장 네비게이션 설정",
        "위제스 Parking Cordeliers 주차 잔여면 확인"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 21")

def update_day_22():
    p = DAILY_CARDS / "day-22.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "08:30"
    d["endTime"] = "20:30"
    d["totalDuration"] = "12시간"
    d["totalDistance"] = "TER 철도 왕복 + 아를 시내 도보 약 4.5km"
    d["fatigue"] = "3"
    d["transport"] = [
        "SNCF TER 기차 왕복 (Avignon Centre ↔ Arles, 단 17분 소요)",
        "아를 시내 도보 (원형경기장 ➔ 고대극장 ➔ 포룸 광장 ➔ 생트로핌 ➔ 라 로케트)"
    ]
    d["stops"] = [
        {
            "id": "avignon-centre",
            "order": 1,
            "start": "08:30",
            "end": "09:15",
            "name": "Avignon Centre역 ➔ Arles 이동 (TER)",
            "category": "transport",
            "lat": 43.9422,
            "lng": 4.8058,
            "summary": "숙소에서 아비뇽 중앙역 도보 이동 후 08:45 TER 탑승. 09:02 아를 역 도착 (17분 소요). [차량은 아비뇽에 거치]",
            "menu": None,
            "reservation": "SNCF Connect (30분 간격 배차)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "arenes",
            "order": 2,
            "start": "09:20",
            "end": "10:45",
            "name": "Arènes d'Arles (아를 원형경기장)",
            "category": "sight",
            "lat": 43.6778,
            "lng": 4.6311,
            "summary": "기원후 90년 로마 원형경기장. 2층 아케이드와 중세 방어탑 전망대에서 론 강과 아를 구시가지 파노라마 조망. [JEP 2026 유럽문화유산의 날 주말 개방]",
            "menu": None,
            "reservation": "현장 발권 / JEP 무료/특별 입장",
            "optional": False,
            "place_ref": "arenes-d-arles"
        },
        {
            "id": "theatre",
            "order": 3,
            "start": "10:45",
            "end": "11:45",
            "name": "Théâtre Antique & 공화국 광장",
            "category": "sight",
            "lat": 43.6767,
            "lng": 4.6297,
            "summary": "기원전 1세기 아우구스투스 황제 시기 고대극장 회랑 기둥 및 오벨리스크가 서 있는 Place de la République",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "theatre-antique-arles"
        },
        {
            "id": "forum-lunch",
            "order": 4,
            "start": "11:45",
            "end": "13:15",
            "name": "Place du Forum & 반 고흐 카페 점심",
            "category": "food",
            "lat": 43.6764,
            "lng": 4.6267,
            "summary": "반 고흐의 '밤의 카페 테라스' 배경지인 포룸 광장 테라스 레스토랑에서 카마르그식 점심 식사",
            "menu": "가르디안 드 토로(황소고기 스튜), 카마르그 붉은 쌀, 로컬 와인",
            "reservation": "현장 선택",
            "optional": False,
            "place_ref": "place-du-forum-arles"
        },
        {
            "id": "saint-trophime",
            "order": 5,
            "start": "13:30",
            "end": "14:45",
            "name": "Cloître Saint-Trophime (생트로핌 회랑)",
            "category": "culture",
            "lat": 43.6764,
            "lng": 4.6283,
            "summary": "12-14세기 로마네스크와 고딕 조각의 정수가 보존된 생트로핌 대성당 회랑",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "cloitre-saint-trophime"
        },
        {
            "id": "la-roquette",
            "order": 6,
            "start": "15:00",
            "end": "16:30",
            "name": "La Roquette 구시가지 & 론 강변",
            "category": "sight",
            "lat": 43.6750,
            "lng": 4.6231,
            "summary": "옛 어부들의 거주지 라 로케트의 조용한 석조 골목 및 론 강변(반 고흐 '론 강의 별이 빛나는 밤' 배경지) 산책",
            "menu": None,
            "reservation": None,
            "optional": True,
            "place_ref": "la-roquette"
        },
        {
            "id": "avignon-return",
            "order": 7,
            "start": "17:00",
            "end": "20:30",
            "name": "Arles ➔ Avignon 귀환 & 마지막 저녁",
            "category": "hotel",
            "lat": 43.94993,
            "lng": 4.81302,
            "summary": "Arles역에서 17:15 TER 탑승 ➔ 17:32 Avignon Centre 도착. 아비뇽 마지막 저녁 식사 및 익일 차량 반납/TGV 짐 정리",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "avignon-centre",
            "to": "arenes",
            "mode": "train",
            "duration": "TER 17분 + 도보 8분",
            "distance": "약 36km"
        },
        {
            "from": "arenes",
            "to": "theatre",
            "mode": "walk",
            "duration": "3분",
            "distance": "0.2km"
        },
        {
            "from": "theatre",
            "to": "forum-lunch",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.3km"
        },
        {
            "from": "forum-lunch",
            "to": "saint-trophime",
            "mode": "walk",
            "duration": "3분",
            "distance": "0.2km"
        },
        {
            "from": "saint-trophime",
            "to": "la-roquette",
            "mode": "walk",
            "duration": "10분",
            "distance": "0.6km"
        },
        {
            "from": "la-roquette",
            "to": "avignon-return",
            "mode": "train",
            "duration": "도보 12분 + TER 17분",
            "distance": "약 36km"
        }
    ]
    d["backup"] = "JEP 2026 문화유산의 날 인파로 대기줄 과다 시: 원형경기장 1곳만 내부 입장하고 고대극장/생트로핌은 외관 관람 후 론 강변 산책 중심 조기 귀환"
    d["needsReview"] = [
        "JEP 2026 주말 Arènes 특별 운영 및 사전 예약 필요 여부 확인",
        "익일 Day 23 아침 09:00 Avignon TGV 렌터카 반납 준비"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 22")

def update_day_23():
    p = DAILY_CARDS / "day-23.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "07:30"
    d["endTime"] = "21:00"
    d["totalDuration"] = "13시간 30분"
    d["totalDistance"] = "차량 반납 + TGV 약 230km"
    d["fatigue"] = "3"
    d["transport"] = [
        "렌터카 반납 (Avignon TGV역 Hertz 09:00 반납 완료, 확정 [CONFIRMED])",
        "TGV INOUI 12176 (Avignon TGV 10:22 ➔ Lyon Part-Dieu 11:28, 1등석 확정)",
        "Lyon 택시/지하철"
    ]
    d["stops"] = [
        {
            "id": "avignon-checkout",
            "order": 1,
            "start": "07:30",
            "end": "08:15",
            "name": "Avignon 숙소 체크아웃 & 차량 적재",
            "category": "hotel",
            "lat": 43.94993,
            "lng": 4.81302,
            "summary": "아비뇽 숙소 체크아웃 후 차량 짐 적재. Avignon TGV역으로 출발 (주유소 경유 20분 소요)",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "avignon-tgv",
            "order": 2,
            "start": "08:45",
            "end": "09:30",
            "name": "Avignon TGV역 Hertz 렌터카 반납",
            "category": "transport",
            "lat": 43.9219,
            "lng": 4.7861,
            "summary": "08:45 TGV역 진입 ➔ 주유 완료 확인 ➔ Hertz 전용 반납 베이 주차 ➔ 차량 사방 외관/계기판 사진 촬영 ➔ 카운터/키드롭 박스 키 반납 (08:55 반납 완료). 10:22 열차까지 67분 완충 확보",
            "menu": None,
            "reservation": "예약확정 Hertz [CONFIRMED] — 9/20 09:00 반납",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "part-dieu",
            "order": 3,
            "start": "10:22",
            "end": "11:28",
            "name": "TGV 12176 ➔ Lyon Part-Dieu 도착",
            "category": "transport",
            "lat": 45.7606,
            "lng": 4.8594,
            "summary": "TGV INOUI 12176 탑승 (10:22 출발 ➔ 11:28 파르디외역 도착, 1등석 편안한 휴식)",
            "menu": None,
            "reservation": "예약완료 TGV INOUI 12176 · 1등석 (10:22~11:28)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "lyon-checkin",
            "order": 4,
            "start": "12:00",
            "end": "15:30",
            "name": "Lyon 숙소 이동 & 짐 보관 & 점심",
            "category": "hotel",
            "lat": 45.746467,
            "lng": 4.868933,
            "summary": "택시로 숙소 이동 (15분). 짐 보관(Luggage Drop) 후 몽플레지르/파르디외 인근 점심 식사 ➔ 15:00 정식 체크인 및 짐 정리",
            "menu": "리옹식 샐러드, 퀘넬(Quenelle)",
            "reservation": "예약확정 Lagrange Aparthotel Lyon Lumière ([CONFIRMED]) — 체크인 15:00",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "ainay-walk",
            "order": 5,
            "start": "16:00",
            "end": "18:30",
            "name": "Presqu'île (벨쿠르 광장 & 셀레스탱 극장)",
            "category": "sight",
            "lat": 45.7578,
            "lng": 4.8322,
            "summary": "메트로 D선 탑승 ➔ 프레스킬 반도 중심 벨쿠르 광장(Place Bellecour), 루이 14세 기마상, 셀레스탱 극장(Théâtre des Célestins) 외관 산책",
            "menu": "에스프레소, 프랄린 브리오슈",
            "reservation": None,
            "optional": False,
            "place_ref": "bellecour"
        },
        {
            "id": "lyon-return",
            "order": 6,
            "start": "19:00",
            "end": "21:00",
            "name": "리옹 부숑 저녁 식사 & 숙소 귀환",
            "category": "hotel",
            "lat": 45.746467,
            "lng": 4.868933,
            "summary": "전통 부숑(Bouchon Lyonnais) 저녁 식사 후 숙소 귀환",
            "menu": "살치숑, 타블리에 드 사푀르, 코트 뒤 론 와인",
            "reservation": "저녁 예약 권장 (Café Comptoir Abel 등)",
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "avignon-checkout",
            "to": "avignon-tgv",
            "mode": "car",
            "duration": "약 20분 (주유 포함)",
            "distance": "6.0km"
        },
        {
            "from": "avignon-tgv",
            "to": "part-dieu",
            "mode": "train",
            "duration": "1시간 6분",
            "distance": "약 230km"
        },
        {
            "from": "part-dieu",
            "to": "lyon-checkin",
            "mode": "taxi",
            "duration": "약 15분",
            "distance": "3.5km"
        },
        {
            "from": "lyon-checkin",
            "to": "ainay-walk",
            "mode": "subway",
            "duration": "메트로 D선 10분",
            "distance": "2.8km"
        },
        {
            "from": "ainay-walk",
            "to": "lyon-return",
            "mode": "walk",
            "duration": "10분",
            "distance": "0.8km"
        }
    ]
    d["backup"] = "1. 차량 반납 지연 시: 08:30까지 숙소 출발 엄수하여 09:15 이전 반납 완료(TGV 출발 1시간 전 안전선 확보)\n2. Lyon 도착 후 피로 시: 프레스킬 산책을 축소하고 숙소 휴식 후 인근 비스트로 저녁"
    d["needsReview"] = [
        "Avignon TGV Hertz 반납 시 차량 사진 증빙(외관/계기판) 촬영",
        "Lagrange Aparthotel Lyon Lumière 도착 시 짐 보관 확인"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 23")

if __name__ == "__main__":
    update_day_19()
    update_day_20()
    update_day_21()
    update_day_22()
    update_day_23()
