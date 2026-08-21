import json
from pathlib import Path

# Day 02
p2 = Path("data/daily-cards/day-02.json")
d2 = json.loads(p2.read_text(encoding="utf-8"))
for s in d2["stops"]:
    if s["id"] == "la-paradeta-sagrada":
        s["place_ref"] = "la-paradeta-sagrada-familia"
        s["name"] = "La Paradeta Sagrada Família 점심"
        s["reservation"] = "현장 대기 (12:50 도착 권장)"
    elif s["id"] == "bodega-joan":
        s["place_ref"] = "bodega-joan"
        s["name"] = "Bodega Joan 저녁"
        s["reservation"] = "사전 예약 권장 (20:30)"
p2.write_text(json.dumps(d2, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# Day 03
p3 = Path("data/daily-cards/day-03.json")
d3 = json.loads(p3.read_text(encoding="utf-8"))
for s in d3["stops"]:
    if s["id"] == "mercat-concepcio":
        s["place_ref"] = "mercat-concepcio"
        s["name"] = "Mercat de la Concepció 아침 장보기"
    elif s["id"] == "bar-canete":
        s["place_ref"] = "bar-canete"
        s["name"] = "Bar Cañete 점심"
        s["reservation"] = "사전 예약 필수 (13:30 슬롯)"
p3.write_text(json.dumps(d3, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# Day 04
p4 = Path("data/daily-cards/day-04.json")
d4 = json.loads(p4.read_text(encoding="utf-8"))
for s in d4["stops"]:
    if s["id"] == "la-zorra":
        s["place_ref"] = "la-zorra"
        s["name"] = "La Zorra 점심 (시체스)"
        s["reservation"] = "사전 예약 필수 (13:00 슬롯)"
p4.write_text(json.dumps(d4, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print("Updated day-02, day-03, day-04 daily cards successfully")
