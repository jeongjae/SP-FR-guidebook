#!/usr/bin/env python3
"""Sync Days 16 to 18 daily cards with updated Luberon driving execution data."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAILY_CARDS = ROOT / "data" / "daily-cards"

def update_day_16():
    p = DAILY_CARDS / "day-16.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "08:00"
    d["endTime"] = "20:30"
    d["totalDuration"] = "12시간 30분"
    d["totalDistance"] = "약 67km · 차량 이동"
    d["fatigue"] = "3"
    d["transport"] = [
        "렌터카 (Aix ➔ Lourmarin ➔ Coustellet ➔ Goult ➔ Domaine des Peyre)",
        "차량 내 수하물 완전 은폐 (가림막 장착, 짐 노출 금지)"
    ]
    d["stops"] = [
        {
            "id": "aix-checkout",
            "order": 1,
            "start": "08:00",
            "end": "08:45",
            "name": "Aix 숙소 체크아웃 & 차량 적재",
            "category": "hotel",
            "lat": 43.5283,
            "lng": 5.4497,
            "summary": "숙소 체크아웃 및 렌터카 수하물 적재. 트렁크 짐 노출 방지 가림막 장착",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "lourmarin",
            "order": 2,
            "start": "09:30",
            "end": "11:30",
            "name": "Lourmarin 마을 & 르네상스 샤토 외관",
            "category": "sight",
            "lat": 43.7636,
            "lng": 5.3628,
            "summary": "남부 뤼베롱 관문 마을. Parking du Rayol 주차 후 카뮈의 흔적, 플라타너스 카페 거리, 르네상스 고성 외관 산책 (2시간)",
            "menu": "에스프레소, 크루아상",
            "reservation": "주차: Parking du Rayol (Primary) / Parking du Château (Backup)",
            "optional": False,
            "place_ref": "lourmarin"
        },
        {
            "id": "coustellet",
            "order": 3,
            "start": "12:00",
            "end": "13:30",
            "name": "Marché Paysan de Coustellet & 장보기",
            "category": "shopping",
            "lat": 43.8686,
            "lng": 5.1436,
            "summary": "일요 파머스 마켓(08:00~13:00 운영, 12시 마감 전 신선 식재료 확보). 3박 농가 체류용 식재료(치즈, 멜론, 무화과, 바게트, 생수, 와인) 구매",
            "menu": "시장 바게트 샌드위치, 프로방스 멜론, 염소 치즈",
            "reservation": "주차: Parking de la Gare / Marché (무료 주차)",
            "optional": False,
            "place_ref": "coustellet"
        },
        {
            "id": "goult",
            "order": 4,
            "start": "13:45",
            "end": "15:00",
            "name": "Goult 체크인 전 완충 & 카페",
            "category": "sight",
            "lat": 43.8631,
            "lng": 5.2417,
            "summary": "쿠스텔레에서 차로 10분. Café de la Poste 테라스 커피 및 예루살렘 풍차(Moulin de Jérusalem) 가벼운 산책. 피로 시 생략 후 조기 체크인 가능",
            "menu": "테라스 에스프레소, 타르트",
            "reservation": "주차: Place de la Libération",
            "optional": True,
            "place_ref": "goult"
        },
        {
            "id": "farm-checkin",
            "order": 5,
            "start": "15:30",
            "end": "20:30",
            "name": "Domaine des Peyre 농가 체크인 & 테라스 첫 저녁",
            "category": "hotel",
            "lat": 43.87088,
            "lng": 5.12202,
            "summary": "농가 숙소 체크인 (15:30~16:30 권장). 좁은 진입 농로 서행, 짐 정리, 수영장/정원 휴식, Coustellet 시장 식재료로 테라스 첫 저녁 식사",
            "menu": "프로방스 샐러드, 바게트, 로컬 치즈 & 뤼베롱 와인",
            "reservation": "숙소 확정/후보 (Domaine des Peyre, Robion 인근)",
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "aix-checkout",
            "to": "lourmarin",
            "mode": "car",
            "duration": "약 40분",
            "distance": "36.8km",
            "roadType": "국도 D543 ➔ 지방도 D943 (뤼베롱 산지 진입)"
        },
        {
            "from": "lourmarin",
            "to": "coustellet",
            "mode": "car",
            "duration": "약 30분",
            "distance": "28.0km",
            "roadType": "지방도 D943 ➔ 간선국도 D900 (쿠스텔레 평지)"
        },
        {
            "from": "coustellet",
            "to": "goult",
            "mode": "car",
            "duration": "약 12분",
            "distance": "8.5km",
            "roadType": "간선국도 D900 ➔ D218 언덕 진입로"
        },
        {
            "from": "goult",
            "to": "farm-checkin",
            "mode": "car",
            "duration": "약 13분",
            "distance": "11.0km",
            "roadType": "지방도 D900 ➔ 좁은 농로(Chemin des Peyres)"
        }
    ]
    d["backup"] = "1. Aix 출발 지연 시 Lourmarin 체류를 60분으로 압축하고 Coustellet 시장(13:00 마감) 정시 도착 우선\n2. 피로 누적 시 Goult 완충 스톱을 생략하고 15:30 농가 숙소로 직행\n3. 악천후 시 Lourmarin 실내 갤러리/카페 중심 관람 후 숙소 이동"
    d["needsReview"] = [
        "Lourmarin 주차 시 트렁크 짐 노출 방지 수칙 준수",
        "Coustellet 일요 시장 13:00 마감 전 식재료 구매 완료",
        "농가 숙소 진입 농로 및 체크인 시각 호스트 연락 확인"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 16")

def update_day_17():
    p = DAILY_CARDS / "day-17.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "08:30"
    d["endTime"] = "20:30"
    d["totalDuration"] = "12시간"
    d["totalDistance"] = "약 56km · 차량 이동"
    d["fatigue"] = "3"
    d["transport"] = [
        "렌터카 (Domaine des Peyre ↔ Roussillon ↔ Goult ↔ 숙소)",
        "황토길 오커 트레일 도보 (30분/50분 코스)"
    ]
    d["stops"] = [
        {
            "id": "farm-depart",
            "order": 1,
            "start": "08:30",
            "end": "09:00",
            "name": "농가 숙소 아침 & 출발",
            "category": "hotel",
            "lat": 43.87088,
            "lng": 5.12202,
            "summary": "숙소 테라스 아침식사 후 08:30 출발. 루시용 주차장(Parking Saint-Michel)으로 이동 (20분 소요)",
            "menu": "크루아상, 잼, 커피",
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "sentier-ocres",
            "order": 2,
            "start": "09:00",
            "end": "10:30",
            "name": "Sentier des Ocres (오커 트레일)",
            "category": "sight",
            "lat": 43.9019,
            "lng": 5.2939,
            "summary": "붉은 황토 절벽과 소나무 숲 트레일(30분/50분 루프). 오전 햇살에 가장 화려한 색채. [주의] 붉은 흙먼지로 인한 밝은색 옷/흰 신발 착용 절대 금지",
            "menu": None,
            "reservation": "입장료 현장 €3.50 / 주차: Parking Saint-Michel (Primary)",
            "optional": False,
            "place_ref": "roussillon-sentier-des-ocres"
        },
        {
            "id": "roussillon",
            "order": 3,
            "start": "10:30",
            "end": "13:15",
            "name": "Roussillon 구시가지 & 점심",
            "category": "sight",
            "lat": 43.9022,
            "lng": 5.2928,
            "summary": "오커 파스텔 건물 골목, 벨베데레 전망대 조망 후 마을 비스트로에서 여유로운 프로방스 점심 식사",
            "menu": "라타투이, 오리 콩피, 니스식 샐러드, 로제 와인",
            "reservation": "식당: Restaurant David 또는 Le Bistrot de Roussillon",
            "optional": False,
            "place_ref": "roussillon-sentier-des-ocres"
        },
        {
            "id": "farm-rest",
            "order": 4,
            "start": "13:45",
            "end": "15:45",
            "name": "농가 숙소 한낮 휴식 (Siesta)",
            "category": "hotel",
            "lat": 43.87088,
            "lng": 5.12202,
            "summary": "한낮 13:30~15:30 폭염 피하기. 농가 숙소로 복귀하여 수영장/에어컨 휴식 및 독서",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "goult",
            "order": 5,
            "start": "16:00",
            "end": "18:00",
            "name": "Goult 조용한 생활마을 & 풍차 언덕",
            "category": "sight",
            "lat": 43.8631,
            "lng": 5.2417,
            "summary": "관광 인파가 적은 정통 석조 생활마을. 조용한 돌담길, 에밀 졸라 광장, Moulin de Jérusalem 풍차 언덕에서 북쪽 뤼베롱 계곡 조망 (2시간)",
            "menu": "Café de la Poste 테라스 음료",
            "reservation": "주차: Place de la Libération / Rue de la République",
            "optional": False,
            "place_ref": "goult"
        },
        {
            "id": "farm-return",
            "order": 6,
            "start": "18:30",
            "end": "20:30",
            "name": "농가 숙소 복귀 & 저녁",
            "category": "hotel",
            "lat": 43.87088,
            "lng": 5.12202,
            "summary": "숙소 귀환, 여유로운 저녁 식사 및 휴식. 익일 화요 고르드 시장(08:15 출발) 준비",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "farm-depart",
            "to": "sentier-ocres",
            "mode": "car",
            "duration": "약 20분",
            "distance": "16.7km",
            "roadType": "국도 D900 ➔ 지방도 D104 ➔ D227 (루시용 오르막)"
        },
        {
            "from": "sentier-ocres",
            "to": "roussillon",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.3km",
            "roadType": "루시용 마을 보행로"
        },
        {
            "from": "roussillon",
            "to": "farm-rest",
            "mode": "car",
            "duration": "약 20분",
            "distance": "17.2km",
            "roadType": "지방도 D227 ➔ 간선국도 D900 ➔ 농로"
        },
        {
            "from": "farm-rest",
            "to": "goult",
            "mode": "car",
            "duration": "약 13분",
            "distance": "10.8km",
            "roadType": "농로 ➔ 간선국도 D900 ➔ 지방도 D218"
        },
        {
            "from": "goult",
            "to": "farm-return",
            "mode": "car",
            "duration": "약 13분",
            "distance": "10.9km",
            "roadType": "지방도 D218 ➔ 간선국도 D900 ➔ 농로"
        }
    ]
    d["backup"] = "1. 우천/트레일 폐쇄 시 오커길 도보를 생략하고 루시용 구시가지 실내 갤러리 및 Goult 긴 점심/카페로 전환\n2. 피로 시 오후 Goult 방문을 생략하고 숙소 전일 휴식\n3. 원할 경우 Goult 대신 Bonnieux(남향 계곡 뷰)로 대체 가능"
    d["needsReview"] = [
        "Sentier des Ocres 오커 흙먼지 대비 복장(어두운색 의류/편한 신발)",
        "루시용 주차장(Parking Saint-Michel) 오전 09:00 이전 선점",
        "루시용/구트 점심 식당 월요일 영업 여부 확인"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 17")

def update_day_18():
    p = DAILY_CARDS / "day-18.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "08:15"
    d["endTime"] = "19:30"
    d["totalDuration"] = "11시간 15분"
    d["totalDistance"] = "약 42km · 차량 이동"
    d["fatigue"] = "3"
    d["transport"] = [
        "렌터카 (Domaine des Peyre ↔ Gordes ↔ Village des Bories ↔ Sénanque ➔ Ménerbes ➔ 숙소)",
        "외곽 주차 후 도보 접근 (Parking Bel-Air / Parking Charles de Gaulle)"
    ]
    d["stops"] = [
        {
            "id": "farm-depart",
            "order": 1,
            "start": "08:15",
            "end": "08:45",
            "name": "농가 숙소 조기 출발 ➔ Gordes 이동",
            "category": "hotel",
            "lat": 43.87088,
            "lng": 5.12202,
            "summary": "화요 대형 시장 인파/주차 혼잡 회피를 위해 08:15 조기 출발. D15 도로를 통해 고르드 접근 (15분 소요)",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "gordes",
            "order": 2,
            "start": "08:45",
            "end": "11:30",
            "name": "Gordes 화요 대형 시장 & 벨베데레 전망",
            "category": "sight",
            "lat": 43.9114,
            "lng": 5.2003,
            "summary": "뤼베롱 최대 규모의 전통시장(08:30~13:00). 성곽 광장과 골목을 채우는 직물·비누·치즈·라벤더 꿀 탐방 및 Belvédère de Gordes 벼랑 뷰포인트 사진 촬영 (2시간 45분)",
            "menu": "프로방스 꿀 사탕, 로컬 건과일, 페이스트리",
            "reservation": "주차: Parking Bel-Air (Primary, 외곽) / Parking Charles de Gaulle (Backup)",
            "optional": False,
            "place_ref": "gordes"
        },
        {
            "id": "village-des-bories",
            "order": 3,
            "start": "11:45",
            "end": "12:45",
            "name": "Village des Bories (돌의 문화)",
            "category": "culture",
            "lat": 43.9056,
            "lng": 5.1819,
            "summary": "고르드 남서쪽 4.4km. 회반죽 없이 쌓아올린 건식 석조 가옥(Bories) 야외 박물관 관람 (60분)",
            "menu": None,
            "reservation": "입장료 현장 €6 / 주차장 완비 (진입로 협소 주의)",
            "optional": False,
            "place_ref": "village-des-bories"
        },
        {
            "id": "picnic",
            "order": 4,
            "start": "12:45",
            "end": "13:45",
            "name": "피크닉 점심 식사",
            "category": "food",
            "lat": 43.9050,
            "lng": 5.1825,
            "summary": "고르드 시장에서 구입한 신선 바게트, 샤퀴테리, 치즈, 과일로 그늘 아래 피크닉 또는 카페 간단식",
            "menu": "바게트 샌드위치, 로컬 치즈, 멜론, 탄산수",
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "senanque",
            "order": 5,
            "start": "14:00",
            "end": "15:15",
            "name": "Abbaye de Sénanque (세낭크 수도원 외관)",
            "category": "sight",
            "lat": 43.9283,
            "lng": 5.1889,
            "summary": "고르드 북쪽 좁은 협곡 도로(D177 일방통행 주의). 12세기 시토회 수도원의 절제된 석조 건축과 협곡 정경 감상 (9월 중순 라벤더 수확 후 차분한 수도원)",
            "menu": None,
            "reservation": "외관/주차 무료 (내부 가이드 투어 시 사전 예약)",
            "optional": True,
            "place_ref": "abbaye-de-senanque"
        },
        {
            "id": "menerbes",
            "order": 6,
            "start": "15:45",
            "end": "17:00",
            "name": "Ménerbes (한적한 언덕마을 산책)",
            "category": "sight",
            "lat": 43.8333,
            "lng": 5.2083,
            "summary": "피터 메일(A Year in Provence)의 무대. 언덕 꼭대기 성채와 포도밭 전경 산책. 피로 시 생략 가능",
            "menu": "테라스 에스프레소",
            "reservation": "주차: Parking de la Mairie / Parking du Lavoir",
            "optional": True,
            "place_ref": "menerbes"
        },
        {
            "id": "farm-return",
            "order": 7,
            "start": "17:30",
            "end": "19:30",
            "name": "농가 복귀 & 익일 Avignon 이동 준비",
            "category": "hotel",
            "lat": 43.87088,
            "lng": 5.12202,
            "summary": "17:30 숙소 복귀. Day 19 Avignon 이동(D900/N100, 45km)을 위한 차량 주유, 짐 패킹, 체크아웃 준비 및 조기 휴식",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "farm-depart",
            "to": "gordes",
            "mode": "car",
            "duration": "약 15분",
            "distance": "9.8km",
            "roadType": "농로 ➔ 국도 D900 ➔ 지방도 D15 (고르드 오르막)"
        },
        {
            "from": "gordes",
            "to": "village-des-bories",
            "mode": "car",
            "duration": "약 8분",
            "distance": "4.4km",
            "roadType": "지방도 D15 ➔ 좁은 포장길 (마주오는 차 교행 주의)"
        },
        {
            "from": "village-des-bories",
            "to": "picnic",
            "mode": "walk",
            "duration": "0분",
            "distance": "현장",
            "roadType": "보행로"
        },
        {
            "from": "picnic",
            "to": "senanque",
            "mode": "car",
            "duration": "약 12분",
            "distance": "7.5km",
            "roadType": "지방도 D177 (협곡 편도 일방통행 구간 주의)"
        },
        {
            "from": "senanque",
            "to": "menerbes",
            "mode": "car",
            "duration": "약 20분",
            "distance": "15.0km",
            "roadType": "지방도 D177 ➔ D2 ➔ 국도 D900 ➔ D3 (메네르브)"
        },
        {
            "from": "menerbes",
            "to": "farm-return",
            "mode": "car",
            "duration": "약 12분",
            "distance": "10.2km",
            "roadType": "지방도 D3 ➔ 간선국도 D900 ➔ 농로"
        }
    ]
    d["backup"] = "1. Gordes 주차 극심 시 Bel-Air 외곽 주차장 대기 또는 셔틀 이용\n2. 피로/시간 지연 시 Sénanque와 Ménerbes를 생략하고 Bories 관람 후 14:30 조기 복귀\n3. 악천후 시 Gordes 실내 카페 및 Bories 야외 관람 축소"
    d["needsReview"] = [
        "Gordes 화요 시장 외곽 주차장(Parking Bel-Air) 08:45 이전 진입",
        "Sénanque 수도원 진입 시 D177 일방통행 협곡 도로 서행",
        "익일 Day 19 Avignon 이동(09:00 출발)을 위한 차량 주유 및 짐 정리"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 18")

if __name__ == "__main__":
    update_day_16()
    update_day_17()
    update_day_18()
