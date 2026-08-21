#!/usr/bin/env python3
"""Sync Days 24 to 27 daily cards with Lyon, Annecy, and TGV transfer to Paris."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAILY_CARDS = ROOT / "data" / "daily-cards"

def update_day_24():
    p = DAILY_CARDS / "day-24.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "08:30"
    d["endTime"] = "21:30"
    d["totalDuration"] = "13시간"
    d["totalDistance"] = "푸니쿨라 + 도보 약 5.5km"
    d["fatigue"] = "3"
    d["transport"] = [
        "TCL 대중교통 (Metro D + Funicular F2 푸니쿨라)",
        "리옹 구시가지 및 손 강변 도보"
    ]
    d["stops"] = [
        {
            "id": "funicular-ascent",
            "order": 1,
            "start": "08:30",
            "end": "09:00",
            "name": "Metro D ➔ Vieux Lyon ➔ 푸니쿨라 F2 상행",
            "category": "transport",
            "lat": 45.7597,
            "lng": 4.8267,
            "summary": "Monplaisir-Lumière역에서 메트로 D선 탑승 후 Vieux Lyon역 환승, Funicular F2 푸니쿨라로 푸르비에르 언덕 직통 상행 (수직고도 120m 5분 극복)",
            "menu": None,
            "reservation": "TCL 1회권/24시간권 (€2.00 / €6.70)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "fourviere",
            "order": 2,
            "start": "09:00",
            "end": "11:00",
            "name": "Basilique Notre-Dame de Fourvière & 로마극장",
            "category": "culture",
            "lat": 45.7622,
            "lng": 4.8225,
            "summary": "푸르비에르 대성당 내부 화려한 모자이크 관람, 에스플러나드 전망대(리옹 도심·벨쿠르·몽블랑 뷰), 기원전 15년 고대 로마 대극장/오데온 유적 (2시간)",
            "menu": None,
            "reservation": "대성당/로마극장 무료 입장",
            "optional": False,
            "place_ref": "fourviere"
        },
        {
            "id": "rosaire-descent",
            "order": 3,
            "start": "11:00",
            "end": "11:45",
            "name": "Jardin du Rosaire 완만한 정원 하산길",
            "category": "sight",
            "lat": 45.7611,
            "lng": 4.8247,
            "summary": "대성당 뒤편 로제르 정원의 완만한 숲길 산책로를 따라 Vieux Lyon 생장 대성당 방면으로 도보 하산 (무릎 부하 최소화, 45분)",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "vieux-lyon-lunch",
            "order": 4,
            "start": "12:00",
            "end": "13:30",
            "name": "Vieux Lyon 르네상스 비스트로 점심",
            "category": "food",
            "lat": 45.7619,
            "lng": 4.8272,
            "summary": "생장 거리 인근 비스트로 테라스 점심 (생라파엘 파스티세리, 프랄린 브리오슈)",
            "menu": "리옹식 샐러드, 바게트 샌드위치, 프랄린 타르트",
            "reservation": "현장 선택",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "vieux-lyon",
            "order": 5,
            "start": "13:30",
            "end": "15:30",
            "name": "Vieux Lyon & Traboules (비외 리옹 & 트라불)",
            "category": "sight",
            "lat": 45.7628,
            "lng": 4.8278,
            "summary": "16세기 유네스코 르네상스 구시가지. Saint-Jean 대성당, 공개 트라불(Passage de la Tour Rose, 54 Rue Saint-Jean 등 공공 개방 통로) 도보 탐방 (2시간)",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "vieux-lyon"
        },
        {
            "id": "saone-presquile",
            "order": 6,
            "start": "15:45",
            "end": "17:15",
            "name": "Saône 강변 산책 & Passerelle Saint-Georges",
            "category": "sight",
            "lat": 45.7572,
            "lng": 4.8286,
            "summary": "붉은 인도교 생조르주(Passerelle Saint-Georges)를 건너 프레스킬 서안 및 손 강변 파스텔 가옥 조망, 카페 에스프레소",
            "menu": "에스프레소, 로컬 맥주",
            "reservation": None,
            "optional": True,
            "place_ref": None
        },
        {
            "id": "lyon-bouchon-dinner",
            "order": 7,
            "start": "19:00",
            "end": "21:30",
            "name": "정통 부숑 만찬 — Daniel et Denise & 귀환",
            "category": "hotel",
            "lat": 45.746467,
            "lng": 4.868933,
            "summary": "리옹 미식 명가 정통 부숑(Bouchon Lyonnais) 저녁 만찬 후 숙소 복귀 (Lagrange Lumière)",
            "menu": "파테 앙 크루트, 퀘넬 드 브로셰, 타블리에 드 사푀르, 코트 뒤 론",
            "reservation": "저녁 예약 확정/권장 (Daniel & Denise Créqui / Saint-Jean)",
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "funicular-ascent",
            "to": "fourviere",
            "mode": "tram",
            "duration": "푸니쿨라 5분",
            "distance": "0.6km"
        },
        {
            "from": "fourviere",
            "to": "rosaire-descent",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.2km"
        },
        {
            "from": "rosaire-descent",
            "to": "vieux-lyon-lunch",
            "mode": "walk",
            "duration": "15분 (정원 하산)",
            "distance": "0.5km"
        },
        {
            "from": "vieux-lyon-lunch",
            "to": "vieux-lyon",
            "mode": "walk",
            "duration": "3분",
            "distance": "0.1km"
        },
        {
            "from": "vieux-lyon",
            "to": "saone-presquile",
            "mode": "walk",
            "duration": "8분",
            "distance": "0.4km"
        },
        {
            "from": "saone-presquile",
            "to": "lyon-bouchon-dinner",
            "mode": "metro",
            "duration": "메트로 D선 15분",
            "distance": "3.5km"
        }
    ]
    d["backup"] = "우천 또는 피로 시 로마극장 야외 관람을 단축하고 푸르비에르 대성당 내부 및 비외 리옹 실내 트라불/카페 중심 진행"
    d["needsReview"] = [
        "Funicular F2 푸니쿨라 정상 운행 확인",
        "Vieux Lyon 공공 개방 트라불 출입 수칙 준수 (정숙 유지)",
        "저녁 부숑(Daniel & Denise) 예약 확인"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 24")

def update_day_25():
    p = DAILY_CARDS / "day-25.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "08:30"
    d["endTime"] = "20:00"
    d["totalDuration"] = "11시간 30분"
    d["totalDistance"] = "대중교통 + 도보 약 5.5km"
    d["fatigue"] = "3"
    d["transport"] = [
        "TCL 메트로 (Metro D ➔ Metro C선 실크 언덕 상행)",
        "크루아루스 하산길 및 테트도르 공원 도보"
    ]
    d["stops"] = [
        {
            "id": "croix-rousse-market",
            "order": 1,
            "start": "08:30",
            "end": "10:00",
            "name": "Marché de la Croix-Rousse (화요 로컬 시장)",
            "category": "shopping",
            "lat": 45.7744,
            "lng": 4.8319,
            "summary": "메트로 C선을 타고 플라토 정상 하차 후 대로변(Boulevard de la Croix-Rousse) 화요 대형 로컬 시장 탐방 (신선 과일, 치즈, 로컬 빵)",
            "menu": "에스프레소, 페이스트리",
            "reservation": None,
            "optional": False,
            "place_ref": "croix-rousse"
        },
        {
            "id": "croix-rousse-slopes",
            "order": 2,
            "start": "10:00",
            "end": "12:00",
            "name": "Le Mur des Canuts & 실크 직공 트라불",
            "category": "sight",
            "lat": 45.7761,
            "lng": 4.8272,
            "summary": "유럽 최대 트롱프뢰유 벽화(Le Mur des Canuts) ➔ 실크 작업실 거리 ➔ Cour des Voraces(보라스의 뜰 6층 석조 계단 트라불)을 통해 완만하게 하산 (2시간)",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "croix-rousse"
        },
        {
            "id": "halles",
            "order": 3,
            "start": "12:30",
            "end": "14:30",
            "name": "Les Halles de Lyon Paul Bocuse & 점심",
            "category": "food",
            "lat": 45.7622,
            "lng": 4.8519,
            "summary": "메트로 C/B선 경유 폴 보퀴즈 미식 실내시장 도착. Mère Richard 생 마르슬랭 치즈, Sibilia 샤퀴테리 탐방 & 시장 내 해산물/비스트로 점심",
            "menu": "신선 굴, 샤퀴테리 플래터, 생 마르슬랭 치즈, 로컬 화이트 와인",
            "reservation": "현장 선택",
            "optional": False,
            "place_ref": "halles-de-lyon-paul-bocuse"
        },
        {
            "id": "tete-dor",
            "order": 4,
            "start": "15:00",
            "end": "17:30",
            "name": "Parc de la Tête d'Or (황금머리 공원 산책)",
            "category": "sight",
            "lat": 45.7772,
            "lng": 4.8550,
            "summary": "프랑스 최대 도심 공원. 센트럴 호수, 장미원(Roseraie), 열대 온실 식물원 산책 및 잔디밭 휴식 (2시간 30분)",
            "menu": None,
            "reservation": "무료 입장",
            "optional": False,
            "place_ref": "parc-de-la-tete-d-or"
        },
        {
            "id": "lyon-return",
            "order": 5,
            "start": "18:00",
            "end": "20:00",
            "name": "숙소 복귀 & 익일 Annecy 당일치기 준비",
            "category": "hotel",
            "lat": 45.746467,
            "lng": 4.868933,
            "summary": "메트로 B/D선으로 숙소(Lagrange Lumière) 복귀. 가벼운 저녁 식사 및 익일 안시행 기차 시간표 확인",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "croix-rousse-market",
            "to": "croix-rousse-slopes",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.3km"
        },
        {
            "from": "croix-rousse-slopes",
            "to": "halles",
            "mode": "metro",
            "duration": "메트로 C+B선 약 20분",
            "distance": "2.8km"
        },
        {
            "from": "halles",
            "to": "tete-dor",
            "mode": "walk",
            "duration": "18분",
            "distance": "1.4km"
        },
        {
            "from": "tete-dor",
            "to": "lyon-return",
            "mode": "metro",
            "duration": "메트로 B+D선 약 20분",
            "distance": "4.5km"
        }
    ]
    d["backup"] = "피로 시 Tête d'Or 공원 도보를 단축하고 숙소 몽플레지르 생활권 카페 휴식으로 전환"
    d["needsReview"] = [
        "Les Halles Paul Bocuse 화요일 점심 식당 영업 확인",
        "익일 Day 26 Annecy행 TER 왕복 시간표 확인"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 25")

def update_day_26():
    p = DAILY_CARDS / "day-26.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "07:30"
    d["endTime"] = "20:30"
    d["totalDuration"] = "13시간"
    d["totalDistance"] = "TER 기차 왕복 + 안시 도보 약 5km"
    d["fatigue"] = "4"
    d["transport"] = [
        "SNCF TER 기차 왕복 (Lyon Part-Dieu ↔ Annecy, 직통 약 1시간 58분)",
        "안시 구시가지 및 호숫가 도보"
    ]
    d["stops"] = [
        {
            "id": "part-dieu-departure",
            "order": 1,
            "start": "07:30",
            "end": "10:15",
            "name": "Lyon Part-Dieu ➔ Annecy 이동 (TER)",
            "category": "transport",
            "lat": 45.7606,
            "lng": 4.8594,
            "summary": "07:45 Part-Dieu역 도착 ➔ 08:08 TER 직통 탑승 (1시간 58분 소요, 알프스 산자락 경유 10:06 Annecy역 도착). [Backup: 09:08 탑승]",
            "menu": None,
            "reservation": "SNCF Connect (현장/사전 발권)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "vieille-ville",
            "order": 2,
            "start": "10:15",
            "end": "12:30",
            "name": "Annecy Vieille Ville & Palais de l'Île",
            "category": "sight",
            "lat": 45.8992,
            "lng": 6.1286,
            "summary": "안시역 도보 5분 ➔ 튜(Thiou) 운하 중심 ➔ Palais de l'Île (12세기 수상 감옥 요새) ➔ Rue Sainte-Claire 파스텔 아치 골목 산책 (2시간 15분)",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "annecy"
        },
        {
            "id": "savoy-lunch",
            "order": 3,
            "start": "12:30",
            "end": "14:00",
            "name": "사부아(Savoy) 로컬 점심 식사",
            "category": "food",
            "lat": 45.8989,
            "lng": 6.1292,
            "summary": "운하변 테라스 레스토랑에서 즐기는 사부아 정통 점심 (타르티플레트 또는 호수 생선 퐁뒤)",
            "menu": "타르티플레트(Tartiflette), 뻬르슈(호수 농어) 뫼니에르, 사부아 화이트 와인",
            "reservation": "현장 선택 / 대기 적은 곳 우선",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "lakefront",
            "order": 4,
            "start": "14:15",
            "end": "16:45",
            "name": "Lac d'Annecy & Pont des Amours & 유럽 정원",
            "category": "sight",
            "lat": 45.9011,
            "lng": 6.1333,
            "summary": "알프스 설산 배경의 투명한 호숫가. 파키에(Le Pâquier) 잔디밭 ➔ Pont des Amours (사랑의 다리) ➔ Jardins de l'Europe 거목 산책로 (2시간 30분). (선택: 1시간 호수 크루즈)",
            "menu": "로컬 젤라토, 에스프레소",
            "reservation": "크루즈 현장 발권 (선택)",
            "optional": False,
            "place_ref": "annecy"
        },
        {
            "id": "annecy-return",
            "order": 5,
            "start": "17:15",
            "end": "20:30",
            "name": "Annecy ➔ Lyon Part-Dieu 귀환 & 저녁",
            "category": "hotel",
            "lat": 45.746467,
            "lng": 4.868933,
            "summary": "안시역 복귀 ➔ 17:53 TER 직통 탑승 (19:52 Part-Dieu 도착). 숙소 귀환 및 익일 파리 이동 짐 정리. [Backup: 18:53 탑승]",
            "menu": None,
            "reservation": "SNCF Connect",
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "part-dieu-departure",
            "to": "vieille-ville",
            "mode": "train",
            "duration": "TER 1시간 58분 + 도보 5분",
            "distance": "약 140km"
        },
        {
            "from": "vieille-ville",
            "to": "savoy-lunch",
            "mode": "walk",
            "duration": "3분",
            "distance": "0.1km"
        },
        {
            "from": "savoy-lunch",
            "to": "lakefront",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.3km"
        },
        {
            "from": "lakefront",
            "to": "annecy-return",
            "mode": "train",
            "duration": "도보 10분 + TER 1시간 58분",
            "distance": "약 140km"
        }
    ]
    d["backup"] = "악천후/폭우 시 호수 산책 및 크루즈를 축소하고 샤토 디아느시(Château d'Annecy) 박물관 및 구시가지 아케이드 카페 중심 진행"
    d["needsReview"] = [
        "Annecy행 TER 직통 시간표 확인 (08:08 / 17:53)",
        "익일 Day 27 Lyon ➔ Paris TGV 6618 (13:04) 탑승 준비"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 26")

def update_day_27():
    p = DAILY_CARDS / "day-27.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "09:30"
    d["endTime"] = "21:30"
    d["totalDuration"] = "12시간"
    d["totalDistance"] = "TGV 약 465km + 파리 시내 이동"
    d["fatigue"] = "3"
    d["transport"] = [
        "TGV INOUI 6618 (Lyon Part-Dieu 13:04 ➔ Paris Gare de Lyon 15:00, 1등석 확정 [CONFIRMED])",
        "파리 택시 / 메트로 (Gare de Lyon ➔ 78 Rue de Lourmel, 15구)"
    ]
    d["stops"] = [
        {
            "id": "lyon-checkout",
            "order": 1,
            "start": "09:30",
            "end": "11:15",
            "name": "Lyon 숙소 체크아웃 & Part-Dieu역 이동",
            "category": "hotel",
            "lat": 45.746467,
            "lng": 4.868933,
            "summary": "Lagrange Aparthotel Lyon Lumière 체크아웃 후 택시/메트로로 Part-Dieu역 이동 (15분 소요)",
            "menu": None,
            "reservation": "체크아웃 완료 (Lagrange [CONFIRMED])",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "part-dieu-lunch",
            "order": 2,
            "start": "11:30",
            "end": "12:45",
            "name": "Part-Dieu역 점심 & TGV 플랫폼 대기",
            "category": "food",
            "lat": 45.7606,
            "lng": 4.8594,
            "summary": "역사 내 카페/Paul에서 가벼운 샌드위치 점심 식사 후 12:45 전광판 플랫폼 확인 및 대기",
            "menu": "바게트 샌드위치, 에스프레소, 에끌레어",
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "tgv-to-paris",
            "order": 3,
            "start": "13:04",
            "end": "15:00",
            "name": "TGV INOUI 6618 ➔ Paris Gare de Lyon 도착",
            "category": "transport",
            "lat": 48.8449,
            "lng": 2.3734,
            "summary": "TGV INOUI 6618 탑승 (13:04 출발 ➔ 15:00 파리 리옹역 도착, 1등석 편안한 1시간 56분 고속주행)",
            "menu": None,
            "reservation": "예약확정 TGV INOUI 6618 ([CONFIRMED], 1등석)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "paris-checkin",
            "order": 4,
            "start": "15:30",
            "end": "17:30",
            "name": "Paris 15구 숙소 이동 & 체크인 (15박 정착)",
            "category": "hotel",
            "lat": 48.8472,
            "lng": 2.2894,
            "summary": "Gare de Lyon에서 택시 탑승(약 30~45분) ➔ 78 Rue de Lourmel 도착. 정식 체크인, 짐 풀기, 세탁기/주방/Wi-Fi 시설 점검",
            "menu": None,
            "reservation": "예약완료 78 Rue de Lourmel, 75015 Paris (9/24 15:00 체크인 ~ 10/9 11:00 체크아웃)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "first-grocery",
            "order": 5,
            "start": "17:45",
            "end": "19:30",
            "name": "15구 생활권 첫 장보기 & 동네 산책",
            "category": "shopping",
            "lat": 48.8468,
            "lng": 2.2905,
            "summary": "Monoprix Lourmel / Franprix에서 15박 생활용 식재료, 생수, 생필품 구매 및 Rue du Commerce / Champ de Mars 방향 800m 적응 산책",
            "menu": "파리 바게트, 버터, 잼, 와인, 과일",
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "paris-return",
            "order": 6,
            "start": "19:45",
            "end": "21:30",
            "name": "숙소 첫 저녁 식사 & 파리 15박 시작",
            "category": "hotel",
            "lat": 48.8472,
            "lng": 2.2894,
            "summary": "동네 비스트로 저녁 식사 또는 장보기 식재료로 숙소 첫 식사. 파리 15박 장기 체류 시작",
            "menu": "스테이크 프리트 또는 홈메이드 파스타",
            "reservation": "현장 선택",
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "lyon-checkout",
            "to": "part-dieu-lunch",
            "mode": "taxi",
            "duration": "약 15분",
            "distance": "3.5km"
        },
        {
            "from": "part-dieu-lunch",
            "to": "tgv-to-paris",
            "mode": "train",
            "duration": "TGV 1시간 56분",
            "distance": "약 465km"
        },
        {
            "from": "tgv-to-paris",
            "to": "paris-checkin",
            "mode": "taxi",
            "duration": "약 35분",
            "distance": "7.5km"
        },
        {
            "from": "paris-checkin",
            "to": "first-grocery",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.3km"
        },
        {
            "from": "first-grocery",
            "to": "paris-return",
            "mode": "walk",
            "duration": "5분",
            "distance": "0.3km"
        }
    ]
    d["backup"] = "TGV 지연 또는 피로 시 첫날 관광 산책을 일절 생략하고 숙소 체크인 및 최소 장보기 후 조기 휴식"
    d["needsReview"] = [
        "TGV INOUI 6618 (13:04 출발) 탑승 확인",
        "Paris 78 Rue de Lourmel 숙소 도어락/열쇠 수령 지침 확인"
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 27")

if __name__ == "__main__":
    update_day_24()
    update_day_25()
    update_day_26()
    update_day_27()
