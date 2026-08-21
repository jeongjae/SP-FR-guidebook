import json
from pathlib import Path

def update_json(day_num, modifier):
    p = Path(f"data/daily-cards/day-{day_num:02d}.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    modifier(data)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated day-{day_num:02d}.json")

# Day 13
def mod13(d):
    for s in d["stops"]:
        if s["id"] == "place-richelme-place-des-precheurs":
            s["name"] = "Place Richelme 목요 시장 & Pâtisserie Weibel"
            s["summary"] = "리셸므 광장 목요 대형 시장 탐방 및 1954년 전통 메종 베벨(Maison Weibel) 테라스에서 칼리송과 아침 커피"
            s["menu"] = "Calisson d'Aix, 크루아상, 카페 오 레"
        elif s["id"] == "aix-lunch":
            s["place_ref"] = "vieil-aix"
            s["name"] = "Vieil Aix 구시가지 점심 식사"
            s["menu"] = "라타투유, 도브 프로방살, 로제 와인"
update_json(13, mod13)

# Day 14
def mod14(d):
    for s in d["stops"]:
        if s["id"] == "cassis":
            s["place_ref"] = "chez-gilbert-cassis"
            s["name"] = "Chez Gilbert 점심 (Cassis 항구)"
            s["summary"] = "카시스 구항구 앞 공인 부야베스 헌장 인증 레스토랑. 지중해 암초 생선 수프/부야베스와 카시스 AOC 화이트 와인"
            s["menu"] = "Bouillabaisse de roche, 생선 수프(Soupe de poissons), 카시스 화이트 와인"
            s["reservation"] = "테라스석 사전 예약 권장 (12:30)"
update_json(14, mod14)

# Day 15
def mod15(d):
    for s in d["stops"]:
        if s["id"] == "marseille-lunch":
            s["place_ref"] = "vieux-port-marseille"
            s["name"] = "Vieux-Port 마르세유 항구 점심"
            s["menu"] = "파니스(Panisse), 정어리 구이, 생선 수프"
update_json(15, mod15)

# Day 18
def mod18(d):
    for s in d["stops"]:
        if s["id"] == "picnic":
            s["place_ref"] = "gordes"
            s["name"] = "Gordes 시장 재료 피크닉 점심"
            s["menu"] = "고르드 시장 바게트, 바농 염소치즈, 무화과, 하몽"
update_json(18, mod18)

# Day 19
def mod19(d):
    for s in d["stops"]:
        if s["id"] == "avignon-parking-lunch":
            s["place_ref"] = "les-halles"
            s["name"] = "Les Halles d'Avignon 주변 점심"
            s["menu"] = "프로방스 샐러드, 델리 조리식품"
        elif s["id"] == "avignon-return":
            s["place_ref"] = "fou-de-fafa-avignon"
            s["name"] = "Fou de Fafa 아비뇽 첫 저녁"
            s["category"] = "food"
            s["menu"] = "프로방스 양갈비 구이, 계절 3코스 디너"
            s["reservation"] = "사전 예약 필수 (19:30)"
update_json(19, mod19)

# Day 20
def mod20(d):
    for s in d["stops"]:
        if s["id"] == "palais-lunch":
            s["place_ref"] = "palais-des-papes"
            s["name"] = "교황청 광장 비스트로 점심"
            s["menu"] = "프로방스 타파스, 제철 샐러드"
        elif s["id"] == "avignon-return":
            s["place_ref"] = "les-cocottes-saint-louis"
            s["name"] = "Les Cocottes Saint-Louis 저녁 식사"
            s["category"] = "food"
            s["menu"] = "도브 프로방살 냄비 요리, 양정강이 콩피"
            s["reservation"] = "회랑 정원 테라스 예약 권장 (20:00)"
update_json(20, mod20)

# Day 21
def mod21(d):
    for s in d["stops"]:
        if s["id"] == "uzes-lunch":
            s["place_ref"] = "uzes"
            s["name"] = "Uzès Place aux Herbes 광장 테라스 점심"
            s["menu"] = "에르브 광장 브라세리 런치, 로컬 치즈"
update_json(21, mod21)

# Day 22
def mod22(d):
    for s in d["stops"]:
        if s["id"] == "forum-lunch":
            s["place_ref"] = "le-gibolin-arles"
            s["name"] = "Le Gibolin 점심 (아를 로케트 지구)"
            s["menu"] = "카마르그 황소 스튜(Gardianne de taureau), 카마르그 적미 밥"
            s["reservation"] = "12:00 오픈 시각 현장 방문 또는 사전 예약"
update_json(22, mod22)

print("Updated all Provence daily cards successfully")
