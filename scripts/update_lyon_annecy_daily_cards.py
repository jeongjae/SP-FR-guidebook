import json
from pathlib import Path

def update_json(day_num, modifier):
    p = Path(f"data/daily-cards/day-{day_num:02d}.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    modifier(data)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated day-{day_num:02d}.json")

# Day 23
def mod23(d):
    for s in d["stops"]:
        if s["id"] == "lyon-return":
            s["place_ref"] = "cafe-comptoir-abel"
            s["name"] = "Café Comptoir Abel 부숑 첫 저녁"
            s["category"] = "food"
            s["summary"] = "1726년 리옹에서 가장 오래된 유서 깊은 부숑에서 즐기는 전통 끄넬(Quenelle de brochet)과 크림 치킨 만찬"
            s["menu"] = "강꼬치고기 끄넬(낭튀아 가재 소스), 뿔레 아 라 크렘, 보졸레 와인"
            s["reservation"] = "사전 예약 필수 (19:30)"
update_json(23, mod23)

# Day 24
def mod24(d):
    for s in d["stops"]:
        if s["id"] == "vieux-lyon-lunch":
            s["place_ref"] = "vieux-lyon"
            s["name"] = "Vieux Lyon 구시가지 점심"
            s["menu"] = "살라드 리요네즈, 가벼운 비스트로 런치"
        elif s["id"] == "lyon-bouchon-dinner":
            s["place_ref"] = "daniel-et-denise"
            s["name"] = "Daniel et Denise 정통 부숑 만찬"
            s["category"] = "food"
            s["summary"] = "MOF 조제프 비올라 셰프의 공인 부숑. 세계 챔피언 파테 앙 크루트와 타블리에 드 사푀르"
            s["menu"] = "파테 앙 크루트, 타블리에 드 사푀르, 프랄린 타르트"
            s["reservation"] = "사전 예약 필수 (19:45)"
update_json(24, mod24)

# Day 25
def mod25(d):
    for s in d["stops"]:
        if s["id"] == "halles-gastronomy":
            s["place_ref"] = "halles-de-lyon-paul-bocuse"
            s["name"] = "Halles Paul Bocuse 미식 점심"
            s["summary"] = "폴 보퀴즈 시장 내 해산물 바에서 신선한 생굴과 샤르도네, 샤퀴테리 테이스팅"
            s["menu"] = "생굴 플래터, 로제트 드 리옹, 생마르슬랭 치즈"
update_json(25, mod25)

# Day 26
def mod26(d):
    for s in d["stops"]:
        if s["id"] == "savoy-lunch":
            s["place_ref"] = "chez-mamie-lise"
            s["name"] = "Chez Mamie Lise 점심 (안시)"
            s["category"] = "food"
            s["summary"] = "안시 구시가지 운하 골목 알프스 샬레 산장 식당에서 즐기는 전통 사부아 치즈 요리와 호수 생선"
            s["menu"] = "사부아 치즈 퐁뒤 또는 타르티플레트, 안시 호수 생선구이"
            s["reservation"] = "사전 예약 권장 (12:30)"
update_json(26, mod26)

print("Updated all Lyon/Annecy daily cards successfully")
