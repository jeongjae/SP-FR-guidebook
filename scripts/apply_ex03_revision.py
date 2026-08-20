#!/usr/bin/env python3
"""Apply EX-03 Revision: Antibes mandatory in Day 9, Villefranche + Eze + Monaco + Menton in Day 10."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAILY_CARDS = ROOT / "data" / "daily-cards"

def apply_day_9():
    p = DAILY_CARDS / "day-09.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["city"] = "Antibes & Cannes"
    d["title"] = "앙티브 요새마을과 칸 당일치기"
    d["startTime"] = "08:00"
    d["endTime"] = "18:00"
    d["totalDuration"] = "10시간"
    d["totalDistance"] = "TER 왕복 + 시내 도보 약 6.5km"
    d["fatigue"] = "3"
    d["transport"] = ["TER 왕복 (Nice-Ville ↔ Antibes ↔ Cannes)", "앙티브 및 칸 시내 도보"]
    d["map"] = {"zoom": 11, "center": [43.58, 7.08], "routeCache": None}
    d["stops"] = [
        {
            "id": "nice-ville",
            "order": 1,
            "start": "08:00",
            "end": "08:35",
            "name": "Nice-Ville역 출발 ➔ Antibes 이동",
            "category": "transport",
            "lat": 43.7047,
            "lng": 7.2619,
            "summary": "08:15 숙소(12 Rue Verdi) 출발 ➔ 08:24~08:42 TER 탑승 앙티브 이동 (18분 소요)",
            "menu": None,
            "reservation": "SNCF Connect / 현장 발권 (15~20분 간격)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "antibes-old-town",
            "order": 2,
            "start": "08:45",
            "end": "11:15",
            "name": "Vieil Antibes & Marché Provençal",
            "category": "sight",
            "lat": 43.5811,
            "lng": 7.1264,
            "summary": "앙티브 구시가지 성벽길(Promenade Amiral de Grasse), 프로방스 전통시장(Marché Provençal 활성화 시간대), 포르 보방(Port Vauban) 조망 (2.5시간 compact visit)",
            "menu": "프로방스 빵, 올리브, 소카",
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "marche-forville",
            "order": 3,
            "start": "11:55",
            "end": "12:45",
            "name": "Marché Forville",
            "category": "shopping",
            "lat": 43.5522,
            "lng": 7.0125,
            "summary": "11:30 TER 탑승 ➔ 11:42 칸 역 도착 ➔ 포르빌 시장 탐방 및 로컬 치즈·과일 관찰",
            "menu": "소카, 포카치아, 프로방스 생치즈",
            "reservation": None,
            "optional": False,
            "place_ref": "marche-forville"
        },
        {
            "id": "vieux-port-cannes",
            "order": 4,
            "start": "12:45",
            "end": "14:00",
            "name": "Vieux-Port 점심",
            "category": "food",
            "lat": 43.5508,
            "lng": 7.0161,
            "summary": "구항구 테라스 레스토랑에서 신선한 지중해 해산물 점심 식사",
            "menu": "오늘의 생선 그릴, 해산물 파스타",
            "reservation": "현장 선택",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "le-suquet",
            "order": 5,
            "start": "14:00",
            "end": "15:15",
            "name": "Le Suquet & 구시가지 언덕",
            "category": "sight",
            "lat": 43.5511,
            "lng": 7.0108,
            "summary": "칸의 옛 어촌 언덕. 자갈 계단길을 올라 성채 광장에서 칸 만과 구항구 파노라마 조망",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "le-suquet"
        },
        {
            "id": "croisette",
            "order": 6,
            "start": "15:30",
            "end": "16:45",
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
            "order": 7,
            "start": "16:45",
            "end": "17:30",
            "name": "Gare de Cannes ➔ Nice TER 탑승",
            "category": "transport",
            "lat": 43.5539,
            "lng": 7.0205,
            "summary": "칸 역으로 복귀하여 니스행 TER 탑승 (약 30분 소요, 17:30 니스역 도착)",
            "menu": None,
            "reservation": "SNCF Connect",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "nice-return",
            "order": 8,
            "start": "17:30",
            "end": "18:00",
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
            "to": "antibes-old-town",
            "mode": "train",
            "duration": "TER 18분 + 도보 8분",
            "distance": "약 20km"
        },
        {
            "from": "antibes-old-town",
            "to": "marche-forville",
            "mode": "train",
            "duration": "도보 10분 + TER 12분 + 도보 8분",
            "distance": "약 12km"
        },
        {
            "from": "marche-forville",
            "to": "vieux-port-cannes",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.3km"
        },
        {
            "from": "vieux-port-cannes",
            "to": "le-suquet",
            "mode": "walk",
            "duration": "10분 (계단/경사)",
            "distance": "0.4km"
        },
        {
            "from": "le-suquet",
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
    d["backup"] = "우천 시 Croisette 해변 산책을 생략하고 앙티브 피카소 미술관 외관 및 칸 포르빌·르 쉬케 위주로 관람 후 조기 귀환"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Applied Day 09 Revision (Antibes + Cannes)")

def apply_day_10():
    p = DAILY_CARDS / "day-10.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["city"] = "Villefranche · Èze · Monaco · Menton"
    d["title"] = "빌프랑슈·에즈·모나코·망통 4개 도시 연계 당일치기"
    d["startTime"] = "08:00"
    d["endTime"] = "21:00"
    d["totalDuration"] = "13시간"
    d["totalDistance"] = "TER 및 버스 4개 구간 + 도보 약 6km"
    d["fatigue"] = "4"
    d["transport"] = [
        "TER (Nice ➔ Villefranche, Monaco ➔ Menton, Menton ➔ Nice)",
        "Zou! / Lignes d'Azur 버스 (Villefranche ➔ Èze Village, Èze Village ➔ Monaco)",
        "각 도시 내 도보 및 공공 엘리베이터"
    ]
    d["map"] = {"zoom": 11, "center": [43.74, 7.42], "routeCache": None}
    d["stops"] = [
        {
            "id": "nice-ville",
            "order": 1,
            "start": "08:00",
            "end": "08:30",
            "name": "Nice-Ville역 출발 ➔ Villefranche 이동",
            "category": "transport",
            "lat": 43.7047,
            "lng": 7.2619,
            "summary": "08:15 숙소 출발 ➔ 08:25 TER 탑승 (7분 소요, 08:32 빌프랑슈역 도착)",
            "menu": None,
            "reservation": "SNCF Connect / 현장 발권",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "villefranche-sur-mer",
            "order": 2,
            "start": "08:40",
            "end": "10:00",
            "name": "Villefranche-sur-Mer 구시가지 & 항만",
            "category": "sight",
            "lat": 43.7042,
            "lng": 7.3111,
            "summary": "해안역 하차 후 콰이 쿠르베(Quai Courbet), 13세기 지하 어두운 골목(Rue Obscure), 생피에르 예배당 외관 및 성채 조망 (75분 compact visit)",
            "menu": "에스프레소, 크루아상",
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "eze-village",
            "order": 3,
            "start": "10:30",
            "end": "12:15",
            "name": "Èze Village 중세 절벽마을",
            "category": "sight",
            "lat": 43.7278,
            "lng": 7.3619,
            "summary": "버스로 모옌 코르니슈 이동(해발 429m). 자갈 골목, 이국적 정원(Jardin Exotique) 절벽 뷰, 지중해 파노라마 조망 (90분 compact visit)",
            "menu": None,
            "reservation": "이국적 정원 현장 (€7)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "monaco-port-lunch",
            "order": 4,
            "start": "12:45",
            "end": "13:45",
            "name": "Monaco Port Hercule & 점심",
            "category": "food",
            "lat": 43.7353,
            "lng": 7.4206,
            "summary": "에즈에서 버스 602 탑승(20분) ➔ 모나코 플레이스 다르메 도착. 라 콘다민 시장/항구 인근 캐주얼 점심",
            "menu": "바르바주앙(Barbajuan), 파스타, 포카치아",
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "le-rocher",
            "order": 5,
            "start": "14:00",
            "end": "15:30",
            "name": "Le Rocher / Monaco-Ville",
            "category": "sight",
            "lat": 43.7311,
            "lng": 7.4239,
            "summary": "공공 엘리베이터 상행 ➔ 르 로셰 언덕 진입. 대공궁 광장, 모나코 대성당, 지중해 클리프 전망대",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "le-rocher"
        },
        {
            "id": "menton",
            "order": 6,
            "start": "16:00",
            "end": "18:30",
            "name": "Menton 구시가지 & 사블레트 해변",
            "category": "sight",
            "lat": 43.7749,
            "lng": 7.5069,
            "summary": "15:45 모나코역 ➔ 15:56 망통역 도착(TER 11분). 바질리크 생미셸, 파스텔톤 지그재그 계단(Les Rampes), Plage des Sablettes 황금빛 전경",
            "menu": "멘통 레몬 타르트, 소르베",
            "reservation": None,
            "optional": False,
            "place_ref": "menton"
        },
        {
            "id": "menton-dinner",
            "order": 7,
            "start": "18:30",
            "end": "20:00",
            "name": "Menton 저녁 — Le Petit Port",
            "category": "food",
            "lat": 43.7762,
            "lng": 7.5118,
            "summary": "구항구 테라스에서 일몰과 함께 즐기는 신선한 해산물 저녁 식사",
            "menu": "구운 생선 요리, 해산물 리조또",
            "reservation": "사전 확인 권장",
            "optional": True,
            "place_ref": None
        },
        {
            "id": "nice-return",
            "order": 8,
            "start": "20:15",
            "end": "21:00",
            "name": "Menton ➔ Nice-Ville 복귀 ➔ 숙소",
            "category": "hotel",
            "lat": 43.7002,
            "lng": 7.2628,
            "summary": "망통역 20:15~20:25 TER 탑승 (35분 소요) ➔ 니스역 도착 후 숙소(12 Rue Verdi) 귀환 및 휴식",
            "menu": None,
            "reservation": "SNCF Connect",
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "nice-ville",
            "to": "villefranche-sur-mer",
            "mode": "train",
            "duration": "TER 7분 + 도보 3분",
            "distance": "약 6km"
        },
        {
            "from": "villefranche-sur-mer",
            "to": "eze-village",
            "mode": "bus",
            "duration": "버스/환승 약 20~25분",
            "distance": "약 6km"
        },
        {
            "from": "eze-village",
            "to": "monaco-port-lunch",
            "mode": "bus",
            "duration": "버스 602 약 20분",
            "distance": "약 8km"
        },
        {
            "from": "monaco-port-lunch",
            "to": "le-rocher",
            "mode": "walk",
            "duration": "공공 엘리베이터 + 도보 10분",
            "distance": "0.6km"
        },
        {
            "from": "le-rocher",
            "to": "menton",
            "mode": "train",
            "duration": "도보 12분 + TER 11분 + 도보 10분",
            "distance": "약 10km"
        },
        {
            "from": "menton",
            "to": "menton-dinner",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.3km"
        },
        {
            "from": "menton-dinner",
            "to": "nice-return",
            "mode": "train",
            "duration": "도보 12분 + TER 35분 + 도보 10분",
            "distance": "약 25km"
        }
    ]
    d["backup"] = "1. [정상 운영] 4개 도시 모두 방문 (빌프랑슈 75분, 에즈 90분, 모나코 90분, 망통 150분)\n2. [지연 압축] 특정 도시 지연 시 도시 내 부속 관람(에즈 이국적정원 생략, 모나코 몽테카를로 제외, 망통 저녁 생략 후 18:30 니스 조기 복귀)\n3. [비상 Plan B] 철도 파행/악천후 시 에즈/망통을 생략하고 모나코 해양박물관 중심 실내 전환 후 니스 복귀"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Applied Day 10 Revision (Villefranche + Eze + Monaco + Menton)")

if __name__ == "__main__":
    apply_day_9()
    apply_day_10()
