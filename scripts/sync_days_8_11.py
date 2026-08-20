#!/usr/bin/env python3
"""Sync Days 8 to 11 daily cards with updated execution timings, routes, and place references."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAILY_CARDS = ROOT / "data" / "daily-cards"

def update_day_8():
    p = DAILY_CARDS / "day-08.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "08:30"
    d["endTime"] = "21:00"
    d["totalDuration"] = "12시간 30분"
    d["totalDistance"] = "약 5.5km · 도보"
    d["fatigue"] = "3"
    d["transport"] = ["니스 시내 도보"]
    d["stops"] = [
        {
            "id": "cours-saleya",
            "order": 1,
            "start": "08:30",
            "end": "10:00",
            "name": "Cours Saleya 시장",
            "category": "shopping",
            "lat": 43.6958,
            "lng": 7.2753,
            "summary": "토요 꽃·청과·식품 시장. 신선한 과일과 즉석 소카(Socca) 맛보기",
            "menu": "소카(Socca), 신선 무화과, 에스프레소",
            "reservation": None,
            "optional": False,
            "place_ref": "cours-saleya"
        },
        {
            "id": "vieux-nice",
            "order": 2,
            "start": "10:15",
            "end": "12:15",
            "name": "Vieux Nice 구시가지",
            "category": "sight",
            "lat": 43.6975,
            "lng": 7.2783,
            "summary": "사보이 공국 시대의 바로크 골목, 생레파라트 대성당, Fenocchio 젤라토",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "vieux-nice"
        },
        {
            "id": "vieux-nice-lunch",
            "order": 3,
            "start": "12:30",
            "end": "14:00",
            "name": "구시가지 점심 — 니스와즈 요리",
            "category": "food",
            "lat": 43.6971,
            "lng": 7.2778,
            "summary": "Chez Acchiardo 또는 Lou Balico 인근의 정통 니스와즈 가정식 점심",
            "menu": "살라드 니스와즈, 다우브(소고기 스튜), 팍시(Farcis)",
            "reservation": "현장 방문 또는 점심 예약 권장",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "castle-hill",
            "order": 4,
            "start": "14:30",
            "end": "16:30",
            "name": "Colline du Château",
            "category": "sight",
            "lat": 43.6953,
            "lng": 7.2797,
            "summary": "엘리베이터(Ascenseur) 탑승 상행, Baie des Anges와 니스 전경 조망, 인공 폭포 산책",
            "menu": None,
            "reservation": "무료 입장 (엘리베이터 무료 운영)",
            "optional": False,
            "place_ref": "colline-du-chateau"
        },
        {
            "id": "promenade",
            "order": 5,
            "start": "16:45",
            "end": "18:00",
            "name": "Promenade des Anglais",
            "category": "sight",
            "lat": 43.6944,
            "lng": 7.2652,
            "summary": "Quai des États-Unis에서 프롬나드로 이어지는 지중해 해안 산책",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "promenade-des-anglais"
        },
        {
            "id": "port-lympia",
            "order": 6,
            "start": "18:30",
            "end": "20:00",
            "name": "Port Lympia 산책 & 저녁",
            "category": "sight",
            "lat": 43.6978,
            "lng": 7.2861,
            "summary": "항구의 전통 목선(Pointu)과 요트 풍경, 가벼운 저녁 식사. 피로 시 생략 가능",
            "menu": None,
            "reservation": None,
            "optional": True,
            "place_ref": None
        },
        {
            "id": "nice-stay-return",
            "order": 7,
            "start": "20:30",
            "end": "21:00",
            "name": "숙소 귀환 — Palais ALZIRA",
            "category": "hotel",
            "lat": 43.7002,
            "lng": 7.2628,
            "summary": "12 Rue Verdi 숙소 복귀 및 휴식",
            "menu": None,
            "reservation": "예약완료 Airbnb HMJ3HX8QAY — 12 Rue Verdi",
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "cours-saleya",
            "to": "vieux-nice",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.2km"
        },
        {
            "from": "vieux-nice",
            "to": "vieux-nice-lunch",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.1km"
        },
        {
            "from": "vieux-nice-lunch",
            "to": "castle-hill",
            "mode": "walk",
            "duration": "10분 + 엘리베이터",
            "distance": "0.4km"
        },
        {
            "from": "castle-hill",
            "to": "promenade",
            "mode": "walk",
            "duration": "15분",
            "distance": "0.8km"
        },
        {
            "from": "promenade",
            "to": "port-lympia",
            "mode": "walk",
            "duration": "20분",
            "distance": "1.2km"
        },
        {
            "from": "port-lympia",
            "to": "nice-stay-return",
            "mode": "walk",
            "duration": "25분",
            "distance": "1.8km"
        }
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 08")

def update_day_9():
    p = DAILY_CARDS / "day-09.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "08:15"
    d["endTime"] = "18:30"
    d["totalDuration"] = "10시간 15분"
    d["totalDistance"] = "TER 왕복 + 칸 시내 도보 약 5.5km"
    d["fatigue"] = "3"
    d["transport"] = ["TER 왕복 (Nice-Ville ↔ Cannes)", "칸 시내 도보"]
    d["stops"] = [
        {
            "id": "nice-ville",
            "order": 1,
            "start": "08:15",
            "end": "08:50",
            "name": "Nice-Ville역 출발",
            "category": "transport",
            "lat": 43.7047,
            "lng": 7.2619,
            "summary": "숙소에서 도보 10분 이동 후 TER 탑승 (약 30분 소요, 09:20 칸 도착)",
            "menu": None,
            "reservation": "현장 발권/SNCF Connect (20~30분 배차)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "marche-forville",
            "order": 2,
            "start": "09:30",
            "end": "11:00",
            "name": "Marché Forville",
            "category": "shopping",
            "lat": 43.5522,
            "lng": 7.0125,
            "summary": "칸의 역사적 지붕 시장. 일요 활성화 시간대 로컬 치즈·과일·프로방스 빵 탐방",
            "menu": "소카, 포카치아, 프로방스 생치즈",
            "reservation": None,
            "optional": False,
            "place_ref": "marche-forville"
        },
        {
            "id": "le-suquet",
            "order": 3,
            "start": "11:15",
            "end": "12:45",
            "name": "Le Suquet & 구시가지 언덕",
            "category": "sight",
            "lat": 43.5511,
            "lng": 7.0108,
            "summary": "칸의 옛 어촌 기원 언덕. 자갈 계단길을 올라 성채 광장에서 칸 만 전경 조망",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "le-suquet"
        },
        {
            "id": "vieux-port-cannes",
            "order": 4,
            "start": "13:00",
            "end": "14:30",
            "name": "Vieux-Port 점심",
            "category": "food",
            "lat": 43.5508,
            "lng": 7.0161,
            "summary": "구항구 테라스 레스토랑에서 신선한 지중해 해산물 점심 식사",
            "menu": "오늘의 생선 그릴, 부야베스 스타일 해산물 스프",
            "reservation": "현장 선택",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "croisette",
            "order": 5,
            "start": "14:45",
            "end": "16:30",
            "name": "Boulevard de la Croisette",
            "category": "sight",
            "lat": 43.5502,
            "lng": 7.0255,
            "summary": "팔레 데 페스티발 외관 및 야자수 해안 산책로. 벤치 휴식. 피로 시 단축 가능",
            "menu": None,
            "reservation": None,
            "optional": True,
            "place_ref": None
        },
        {
            "id": "cannes-station",
            "order": 6,
            "start": "17:00",
            "end": "17:45",
            "name": "Gare de Cannes ➔ Nice TER 탑승",
            "category": "transport",
            "lat": 43.5539,
            "lng": 7.0205,
            "summary": "칸 역으로 복귀하여 니스행 TER 탑승 (30분 소요)",
            "menu": None,
            "reservation": "SNCF Connect (유연한 복귀 시간대)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "nice-return",
            "order": 7,
            "start": "18:00",
            "end": "18:30",
            "name": "Nice-Ville 도착 ➔ 숙소 귀환",
            "category": "hotel",
            "lat": 43.7002,
            "lng": 7.2628,
            "summary": "니스역 도착 후 숙소 12 Rue Verdi로 복귀 및 휴식",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "nice-ville",
            "to": "marche-forville",
            "mode": "train",
            "duration": "TER 약 30분 + 도보 8분",
            "distance": "약 32km"
        },
        {
            "from": "marche-forville",
            "to": "le-suquet",
            "mode": "walk",
            "duration": "10분 (계단/경사)",
            "distance": "0.3km"
        },
        {
            "from": "le-suquet",
            "to": "vieux-port-cannes",
            "mode": "walk",
            "duration": "10분",
            "distance": "0.4km"
        },
        {
            "from": "vieux-port-cannes",
            "to": "croisette",
            "mode": "walk",
            "duration": "15분",
            "distance": "0.8km"
        },
        {
            "from": "croisette",
            "to": "cannes-station",
            "mode": "walk",
            "duration": "15분",
            "distance": "0.9km"
        },
        {
            "from": "cannes-station",
            "to": "nice-return",
            "mode": "train",
            "duration": "TER 약 30분 + 도보 10분",
            "distance": "약 32km"
        }
    ]
    d["backup"] = "우천 또는 혼잡 시 Croisette 산책을 생략하고 Forville 시장 및 Le Suquet 위주로 관람 후 조기 귀환"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 09")

def update_day_10():
    p = DAILY_CARDS / "day-10.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "08:15"
    d["endTime"] = "21:30"
    d["totalDuration"] = "13시간 15분"
    d["totalDistance"] = "TER 3개 구간 + 도보 약 5.5km"
    d["fatigue"] = "4"
    d["transport"] = ["전 구간 TER (Nice-Ville ➔ Monaco ➔ Menton ➔ Nice-Ville)", "모나코/망통 시내 도보 및 엘리베이터"]
    d["stops"] = [
        {
            "id": "nice-ville",
            "order": 1,
            "start": "08:15",
            "end": "09:00",
            "name": "Nice-Ville역 출발 ➔ Monaco 이동",
            "category": "transport",
            "lat": 43.7047,
            "lng": 7.2619,
            "summary": "08:30~08:40 TER 탑승, 해안 철도 경유 09:05 모나코 몽테카를로역 도착",
            "menu": None,
            "reservation": "SNCF Connect (15~20분 간격 운행)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "le-rocher",
            "order": 2,
            "start": "09:15",
            "end": "11:30",
            "name": "Le Rocher / Monaco-Ville",
            "category": "sight",
            "lat": 43.7311,
            "lng": 7.4239,
            "summary": "모나코역 터널/공공 엘리베이터 경유 르 로셰 언덕 진입. 대공궁 광장, 대성당, 바다 전망대",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "le-rocher"
        },
        {
            "id": "port-hercule",
            "order": 3,
            "start": "11:45",
            "end": "13:15",
            "name": "Port Hercule & 점심",
            "category": "food",
            "lat": 43.7353,
            "lng": 7.4206,
            "summary": "에르퀼 항구 산책 및 라 콘다민 시장/항구 인근에서 캐주얼 점심 식사",
            "menu": "바르바주앙(Barbajuan), 신선 파스타, 포카치아",
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "monaco-station",
            "order": 4,
            "start": "13:30",
            "end": "14:15",
            "name": "Monaco역 ➔ Menton 이동 (TER)",
            "category": "transport",
            "lat": 43.7386,
            "lng": 7.4194,
            "summary": "모나코역 복귀 및 13:50 전후 망통행 TER 탑승 (11분 소요, 14:15 망통역 도착)",
            "menu": None,
            "reservation": "SNCF Connect (20분 간격 운행)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "menton",
            "order": 5,
            "start": "14:30",
            "end": "17:00",
            "name": "Menton 구시가지 & 사블레트 해변",
            "category": "sight",
            "lat": 43.7749,
            "lng": 7.5069,
            "summary": "바질리크 생미셸, 중세 파스텔톤 계단 골목, Plage des Sablettes 레몬 도시 풍경",
            "menu": "레몬 타르트, 소르베",
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "menton-dinner",
            "order": 6,
            "start": "17:30",
            "end": "19:00",
            "name": "Menton 저녁 — Le Petit Port",
            "category": "food",
            "lat": 43.7762,
            "lng": 7.5118,
            "summary": "구항구 인근 테라스에서 지중해식 이른 저녁 식사 또는 아페리티보",
            "menu": "구운 생선 요리, 해산물 리조또",
            "reservation": "사전 확인 권장",
            "optional": True,
            "place_ref": None
        },
        {
            "id": "nice-return",
            "order": 7,
            "start": "19:30",
            "end": "21:00",
            "name": "Menton ➔ Nice 귀환",
            "category": "hotel",
            "lat": 43.7002,
            "lng": 7.2628,
            "summary": "망통역에서 니스행 TER 탑승 (약 35분 소요), 니스역 도착 후 숙소 귀환",
            "menu": None,
            "reservation": "SNCF Connect",
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "nice-ville",
            "to": "le-rocher",
            "mode": "train",
            "duration": "TER 22분 + 엘리베이터/도보 15분",
            "distance": "약 16km"
        },
        {
            "from": "le-rocher",
            "to": "port-hercule",
            "mode": "walk",
            "duration": "15분 (하산)",
            "distance": "0.8km"
        },
        {
            "from": "port-hercule",
            "to": "monaco-station",
            "mode": "walk",
            "duration": "15분",
            "distance": "0.7km"
        },
        {
            "from": "monaco-station",
            "to": "menton",
            "mode": "train",
            "duration": "TER 11분 + 도보 10분",
            "distance": "약 9km"
        },
        {
            "from": "menton",
            "to": "menton-dinner",
            "mode": "walk",
            "duration": "10분",
            "distance": "0.5km"
        },
        {
            "from": "menton-dinner",
            "to": "nice-return",
            "mode": "train",
            "duration": "TER 35분 + 도보 10분",
            "distance": "약 25km"
        }
    ]
    d["backup"] = "1. 모나코 지연 시 몽테카를로를 생략하고 13:30 망통 이동 유지\n2. 피로 누적 시 망통 저녁을 생략하고 17:00 TER로 니스 조기 복귀\n3. 악천후 시 망통을 생략하고 모나코 해양박물관 중심 실내 전환 후 니스 복귀"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 10")

def update_day_11():
    p = DAILY_CARDS / "day-11.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "09:00"
    d["endTime"] = "19:30"
    d["totalDuration"] = "10시간 30분"
    d["totalDistance"] = "약 4km · 도보/트램"
    d["fatigue"] = "2"
    d["transport"] = ["도보", "트램 1호선 (선택)"]
    d["stops"] = [
        {
            "id": "liberation-market",
            "order": 1,
            "start": "09:30",
            "end": "11:30",
            "name": "Marché de la Libération",
            "category": "shopping",
            "lat": 43.7102,
            "lng": 7.2625,
            "summary": "화요일 대형 로컬 시장. 니스 시민들의 일상 식재료·치즈·과일 탐방 및 Gare du Sud 카페",
            "menu": "프로방스 과일, 에스프레소",
            "reservation": None,
            "optional": False,
            "place_ref": "marche-de-la-liberation"
        },
        {
            "id": "liberation-lunch",
            "order": 2,
            "start": "12:00",
            "end": "13:30",
            "name": "리베라시옹 점심",
            "category": "food",
            "lat": 43.7095,
            "lng": 7.2631,
            "summary": "리베라시옹 시장 인근 비스트로 점심 또는 숙소 간단식",
            "menu": "파니니, 니스식 샐러드",
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "charles-negre",
            "order": 3,
            "start": "14:30",
            "end": "16:00",
            "name": "사진미술관 Charles Nègre",
            "category": "culture",
            "lat": 43.6975,
            "lng": 7.2736,
            "summary": "구시가지 입구의 사진 특화 미술관 기획전 관람. 피로 시 생략 가능",
            "menu": None,
            "reservation": "현장 발권 (€5)",
            "optional": True,
            "place_ref": None
        },
        {
            "id": "promenade",
            "order": 4,
            "start": "16:30",
            "end": "18:00",
            "name": "Promenade des Anglais 산책",
            "category": "sight",
            "lat": 43.6944,
            "lng": 7.2652,
            "summary": "숙소 세탁 후 프롬나드 해변 벤치 휴식 및 카페",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "promenade-des-anglais"
        },
        {
            "id": "nice-stay-return",
            "order": 5,
            "start": "18:30",
            "end": "19:30",
            "name": "숙소 — 익일 렌터카 준비 & 휴식",
            "category": "hotel",
            "lat": 43.7002,
            "lng": 7.2628,
            "summary": "12 Rue Verdi 복귀, 9/9 09:00 렌터카 인수 서류/동선 확인, 조기 취침",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "liberation-market",
            "to": "liberation-lunch",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.2km"
        },
        {
            "from": "liberation-lunch",
            "to": "charles-negre",
            "mode": "walk",
            "duration": "15분",
            "distance": "1.4km"
        },
        {
            "from": "charles-negre",
            "to": "promenade",
            "mode": "walk",
            "duration": "10분",
            "distance": "0.6km"
        },
        {
            "from": "promenade",
            "to": "nice-stay-return",
            "mode": "walk",
            "duration": "10분",
            "distance": "0.7km"
        }
    ]
    d["backup"] = "피로 시 사진미술관을 생략하고 숙소 세탁·휴식 및 프롬나드 카페 중심 생활일 유지"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 11")

if __name__ == "__main__":
    update_day_8()
    update_day_9()
    update_day_10()
    update_day_11()
