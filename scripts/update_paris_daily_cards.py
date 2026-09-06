import json
from pathlib import Path

def update_json(day_num, modifier):
    p = Path(f"data/daily-cards/day-{day_num:02d}.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    modifier(data)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated day-{day_num:02d}.json")

# Day 28
def mod28(d):
    for s in d["stops"]:
        if s["id"] == "morning-routine":
            s["place_ref"] = "boulangerie-pichard"
            s["name"] = "Boulangerie Pichard 아침 빵 조달 & 루틴"
            s["menu"] = "바게트 트라디시옹, 크루아상, 에스프레소"
        elif s["id"] == "paris-return":
            s["place_ref"] = "cafe-du-commerce"
            s["name"] = "Café du Commerce 15구 브라세리 첫 저녁"
            s["category"] = "food"
            s["summary"] = "1921년 15구 상업거리 역사적 3층 아르데코 가든 브라세리에서 즐기는 편안한 클래식 프랑스 만찬"
            s["menu"] = "오리 다리 콩피, 샤롤레 소고기 스테이크 프릿, 프로피테롤"
update_json(28, mod28)

# Day 29
def mod29(d):
    for s in d["stops"]:
        if s["id"] == "morning-routine":
            s["place_ref"] = "marche-convention"
            s["name"] = "Marché Convention 일요 노천시장 장보기"
            s["summary"] = "15구 콩방시옹 일요 시장에서 갓 구운 로티세리 치킨, 콩테 치즈, 무화과 조달"
            s["menu"] = "로티세리 치킨 & 감자 구이, 콩테 치즈, 제철 과일"
update_json(29, mod29)

# Day 30
def mod30(d):
    for s in d["stops"]:
        if s["id"] == "paris-return":
            s["place_ref"] = "bouillon-chartier-montparnasse"
            s["name"] = "Bouillon Chartier Montparnasse 저녁"
            s["category"] = "food"
            s["summary"] = "1903년 역사기념물 등록 아르누보 식당에서 종이 식탁보에 연필로 주문하며 즐기는 전설적인 가성비 부이용 만찬"
            s["menu"] = "에스카르고, 뵈프 부르기뇽, 초콜릿 무스"
update_json(30, mod30)

# Day 31
def mod31(d):
    for s in d["stops"]:
        if s["id"] == "morning-routine":
            s["place_ref"] = "boulangerie-pichard"
            s["name"] = "Boulangerie Pichard 아침 빵 조달 & 숙소 생활"
            s["menu"] = "크루아상, 팽 오 쇼콜라, 과일, 커피"
update_json(31, mod31)

# Day 32 — Versailles day
def mod32(d):
    for s in d["stops"]:
        if s["id"] == "paris-return":
            s["place_ref"] = "le-grand-pan"
            s["name"] = "Le Grand Pan 15구 비스트로 저녁"
            s["category"] = "food"
            s["summary"] = "베르사유 투어 후 15구 숯불 비스트로 저녁"
            s["menu"] = "샤롤레 소 티본 스테이크 숯불구이, 송아지 흉선 요리"
update_json(32, mod32)

# Day 34 — Orsay / Rodin day
def mod34(d):
    for s in d["stops"]:
        if s["id"] == "paris-return":
            s["place_ref"] = "cafe-du-commerce"
            s["name"] = "Café du Commerce 동네 저녁"
            s["category"] = "food"
            s["summary"] = "메트로 8호선으로 15구에 복귀해 동네 브라세리 저녁"
            s["menu"] = "에스카르고, 소고기 타르타르, 하우스 와인"
            s["reservation"] = None
update_json(34, mod34)

# Day 35
def mod35(d):
    for s in d["stops"]:
        if s["id"] == "morning-routine":
            s["place_ref"] = "boulangerie-pichard"
            s["name"] = "Boulangerie Pichard 잠봉 뵈르 샌드위치 & 아침"
            s["menu"] = "바게트 트라디시옹, 잠봉 뵈르 샌드위치"
update_json(35, mod35)

# Day 36
def mod36(d):
    for s in d["stops"]:
        if s["id"] == "morning-routine":
            s["place_ref"] = "marche-convention"
            s["name"] = "Marché Convention 토요 장보기 & 아침 루틴"
            s["menu"] = "제철 무화과, 사과, 바농 치즈, 바게트"
update_json(36, mod36)

# Day 38
def mod38(d):
    for s in d["stops"]:
        if s["id"] == "morning-routine":
            s["place_ref"] = "boulangerie-pichard"
            s["name"] = "Boulangerie Pichard 브런치 빵 조달 & 세탁"
            s["menu"] = "애플 턴오버, 브리오슈, 과일 샐러드"
update_json(38, mod38)

# Day 41
def mod41(d):
    for s in d["stops"]:
        if s["id"] == "farewell-dinner":
            s["place_ref"] = "le-grand-pan"
            s["name"] = "Le Grand Pan 파리 15박 고별 만찬"
            s["category"] = "food"
            s["summary"] = "15구 최고 권위의 비스트로에서 2인용 참나무 숯불 코트 드 뵈프와 제철 버섯 요리로 즐기는 대망의 고별 디너"
            s["menu"] = "Côte de boeuf 2인 숯불구이, 제철 그물버섯, 바스크 디저트"
            s["reservation"] = "사전 예약 필수 (20:00)"
update_json(41, mod41)

# Day 42
def mod42(d):
    for s in d["stops"]:
        if s["id"] == "farewell-lunch":
            s["place_ref"] = "cafe-du-commerce"
            s["name"] = "Café du Commerce 15구 마지막 점심"
            s["category"] = "food"
            s["menu"] = "가벼운 브라세리 런치, 샐러드, 커피"
update_json(42, mod42)

print("Updated Paris daily cards successfully")
