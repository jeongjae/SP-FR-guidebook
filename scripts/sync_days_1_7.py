#!/usr/bin/env python3
"""Sync Days 1 to 7 daily cards with updated execution timings, routes, and place references."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAILY_CARDS = ROOT / "data" / "daily-cards"

def update_day_1():
    p = DAILY_CARDS / "day-01.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "19:10"
    d["endTime"] = "23:00"
    d["totalDuration"] = "3시간 50분"
    d["totalDistance"] = "약 12km · 택시"
    d["transport"] = ["택시 (공항 T1 승강장 → 숙소)", "Aerobús A1 (24시간 대안)"]
    d["stops"] = [
        {
            "id": "bcn-airport",
            "order": 1,
            "start": "19:10",
            "end": "20:40",
            "name": "BCN T1 도착 — OZ511",
            "category": "transport",
            "lat": 41.296944,
            "lng": 2.079047,
            "summary": "19:10 착륙 후 입국심사·수하물 수령. T1 택시 승강장으로 이동",
            "menu": None,
            "reservation": "예약완료 OZ511 (FRRL7R) — ICN T2 11:50 출발",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "barcelona-checkin",
            "order": 2,
            "start": "21:10",
            "end": "22:00",
            "name": "숙소 체크인 — Occidental Barcelona 1929",
            "category": "hotel",
            "lat": 41.375274,
            "lng": 2.147662,
            "summary": "체크인 완료 및 샤워. 여권 사본 및 익일 사그라다 QR 확인",
            "menu": None,
            "reservation": "예약완료 Occidental Barcelona 1929",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "barcelona-sleep",
            "order": 3,
            "start": "22:00",
            "end": "23:00",
            "name": "취침 준비",
            "category": "hotel",
            "lat": 41.375274,
            "lng": 2.147662,
            "summary": "시차 적응 및 취침. 편의점 생수 구매 외 외부 관광 없음",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        }
    ]
    d["legs"] = [
        {
            "from": "bcn-airport",
            "to": "barcelona-checkin",
            "mode": "taxi",
            "duration": "약 30~40분",
            "distance": "약 12km"
        },
        {
            "from": "barcelona-checkin",
            "to": "barcelona-sleep",
            "mode": "walk",
            "duration": "0분",
            "distance": "숙소 내부"
        }
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 01")

def update_day_2():
    p = DAILY_CARDS / "day-02.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "08:30"
    d["endTime"] = "21:30"
    d["totalDuration"] = "13시간"
    d["totalDistance"] = "약 10km · 메트로+도보"
    d["stops"] = [
        {
            "id": "sant-pau",
            "order": 1,
            "start": "09:30",
            "end": "11:30",
            "name": "Recinte Modernista de Sant Pau",
            "category": "culture",
            "lat": 41.4128,
            "lng": 2.1744,
            "summary": "도메네크 이 몬타네르의 카탈루냐 모더니즘 병원 단지. 45도 배치와 채광 설계 관찰",
            "menu": None,
            "reservation": "현장 발권/온라인 자유관람 (€18)",
            "optional": False,
            "place_ref": "sant-pau-recinte-modernista"
        },
        {
            "id": "avinguda-gaudi",
            "order": 2,
            "start": "11:30",
            "end": "12:30",
            "name": "Avinguda de Gaudí",
            "category": "sight",
            "lat": 41.4075,
            "lng": 2.1715,
            "summary": "산파우에서 사그라다 파밀리아로 이어지는 대각선 보행로. 야외 카페 및 일상 관찰",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "la-paradeta-sagrada",
            "order": 3,
            "start": "12:45",
            "end": "14:15",
            "name": "La Paradeta Sagrada Família",
            "category": "food",
            "lat": 41.4022,
            "lng": 2.1764,
            "summary": "직접 고른 해산물을 즉석 조리하는 점심. 13:00 첫 회전 대기 진입",
            "menu": "새우, 맛조개(navajas), 칼라마리 튀김",
            "reservation": "현장 선착순 대기 (13:00 오픈)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "sagrada-familia",
            "order": 4,
            "start": "14:45",
            "end": "17:00",
            "name": "Sagrada Família",
            "category": "culture",
            "lat": 41.4036,
            "lng": 2.1744,
            "summary": "14:45 보안검색 도착, 15:15 확정 입장. 탄생 파사드·수난 파사드·중앙 네이브 빛 관찰",
            "menu": None,
            "reservation": "예약완료 — 15:15 입장 (General · €29.12)",
            "optional": False,
            "place_ref": "sagrada-familia"
        },
        {
            "id": "gracia",
            "order": 5,
            "start": "17:30",
            "end": "18:45",
            "name": "Vila de Gràcia",
            "category": "sight",
            "lat": 41.4028,
            "lng": 2.1572,
            "summary": "Plaça del Sol 주변 광장 산책 및 카페 휴식. 피로 시 생략 가능",
            "menu": None,
            "reservation": None,
            "optional": True,
            "place_ref": None
        },
        {
            "id": "bodega-joan",
            "order": 6,
            "start": "19:15",
            "end": "20:45",
            "name": "Bodega Joan",
            "category": "food",
            "lat": 41.3892,
            "lng": 2.1585,
            "summary": "전통 카탈루냐 그릴 요리와 타파스 저녁 식사",
            "menu": "엠부티도스, 그릴 육류, 하우스 와인",
            "reservation": "저녁 예약 권장",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "barcelona-stay-return",
            "order": 7,
            "start": "21:00",
            "end": "21:30",
            "name": "숙소 귀환 — Occidental Barcelona 1929",
            "category": "hotel",
            "lat": 41.375274,
            "lng": 2.147662,
            "summary": "숙소 복귀 및 익일 고딕지구 도보 준비",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        }
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 02")

def update_day_3():
    p = DAILY_CARDS / "day-03.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "09:00"
    d["endTime"] = "21:00"
    d["totalDuration"] = "12시간"
    d["totalDistance"] = "약 6.5km · 도보+메트로"
    d["stops"] = [
        {
            "id": "mercat-concepcio",
            "order": 1,
            "start": "09:30",
            "end": "10:30",
            "name": "Mercat de la Concepció",
            "category": "shopping",
            "lat": 41.3965,
            "lng": 2.1695,
            "summary": "1888년 철골 구조의 꽃·식품 시장. 아침 로컬 분위기와 신선 과일 관찰",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        },
        {
            "id": "barri-gotic",
            "order": 2,
            "start": "11:00",
            "end": "12:30",
            "name": "고딕지구 핵심 산책",
            "category": "sight",
            "lat": 41.3833,
            "lng": 2.1764,
            "summary": "바르셀로나 대성당, Plaça del Rei, Plaça Sant Jaume, 비숍스 브리지로 이어지는 역사 도보 (90분 통합 블록)",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": "barri-gotic"
        },
        {
            "id": "biblioteca-de-catalunya",
            "order": 3,
            "start": "12:40",
            "end": "13:30",
            "name": "Biblioteca de Catalunya",
            "category": "culture",
            "lat": 41.3811,
            "lng": 2.1702,
            "summary": "옛 산타 크레우 병원 고딕 볼트와 중정 회랑. 카탈루냐 인문 정신의 거점",
            "menu": None,
            "reservation": "자유 입장",
            "optional": False,
            "place_ref": "biblioteca-de-catalunya"
        },
        {
            "id": "bar-canete",
            "order": 4,
            "start": "13:45",
            "end": "15:00",
            "name": "Bar Cañete 점심",
            "category": "food",
            "lat": 41.3789,
            "lng": 2.1741,
            "summary": "라발 지구 최고의 정통 카운터 타파스 바. 13:45 예약 필수",
            "menu": "소꼬리 샌드위치, 풋고추 튀김(Pimientos de Padrón), 신선 해산물",
            "reservation": "사전 예약 필수 (월요일 정상 영업)",
            "optional": False,
            "place_ref": None
        },
        {
            "id": "macba",
            "order": 5,
            "start": "15:15",
            "end": "17:15",
            "name": "MACBA",
            "category": "culture",
            "lat": 41.3832,
            "lng": 2.1669,
            "summary": "리처드 마이어 설계의 백색 공간과 현대미술 기획전. 월요일 정상 개관",
            "menu": None,
            "reservation": "온라인 예매 (€13.50, 월요일 10:00~19:30 개관)",
            "optional": False,
            "place_ref": "macba"
        },
        {
            "id": "llibreria-finestres",
            "order": 6,
            "start": "17:35",
            "end": "18:30",
            "name": "Llibreria Finestres",
            "category": "shopping",
            "lat": 41.3912,
            "lng": 2.1623,
            "summary": "에이샴플라의 인문학 큐레이션 서점. 피로 시 생략 가능",
            "menu": None,
            "reservation": None,
            "optional": True,
            "place_ref": None
        },
        {
            "id": "barcelona-stay-return",
            "order": 7,
            "start": "19:00",
            "end": "21:00",
            "name": "숙소 귀환 — 짐 정리 및 휴식",
            "category": "hotel",
            "lat": 41.375274,
            "lng": 2.147662,
            "summary": "익일 렌터카 인수 및 체크아웃 패킹 준비",
            "menu": None,
            "reservation": None,
            "optional": False,
            "place_ref": None
        }
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 03")

def update_day_4():
    p = DAILY_CARDS / "day-04.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["stops"][3]["place_ref"] = "cau-ferrat"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 04")

def update_day_5():
    p = DAILY_CARDS / "day-05.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["stops"][1]["place_ref"] = "collioure"
    d["stops"][3]["place_ref"] = None # cadaques town is regional exception
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 05")

def update_day_6():
    p = DAILY_CARDS / "day-06.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["stops"][1]["place_ref"] = None # tossa is regional exception
    d["stops"][3]["place_ref"] = "pals"
    d["stops"][4]["place_ref"] = "peratallada"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 06")

def update_day_7():
    p = DAILY_CARDS / "day-07.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["startTime"] = "09:30"
    d["endTime"] = "21:00"
    d["totalDuration"] = "11시간 30분"
    d["totalDistance"] = "차량 약 137km + 항공 NCE 16:55"
    d["stops"][4]["place_ref"] = "promenade-des-anglais"
    d["stops"][4]["start"] = "19:15"
    d["stops"][4]["end"] = "20:30"
    d["stops"][5]["start"] = "20:30"
    d["stops"][5]["end"] = "21:00"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated Day 07")

if __name__ == "__main__":
    update_day_1()
    update_day_2()
    update_day_3()
    update_day_4()
    update_day_5()
    update_day_6()
    update_day_7()
