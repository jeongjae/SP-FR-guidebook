import json

# 1. Update place-days.json
with open("data/place-days.json", "r", encoding="utf-8") as f:
    pdays = json.load(f)

pdays["places"]["cafe-comptoir-abel"] = {
    "displayName": "Café Comptoir Abel",
    "region": "lyon",
    "days": [23]
}
pdays["places"]["daniel-et-denise"] = {
    "displayName": "Daniel et Denise",
    "region": "lyon",
    "days": [24]
}
pdays["places"]["chez-mamie-lise"] = {
    "displayName": "Chez Mamie Lise (Annecy)",
    "region": "lyon",
    "days": [26]
}

with open("data/place-days.json", "w", encoding="utf-8") as f:
    json.dump(pdays, f, indent=2, ensure_ascii=False)

# 2. Update place-facts.json
with open("data/place-facts.json", "r", encoding="utf-8") as f:
    pfacts = json.load(f)

pfacts["places"]["cafe-comptoir-abel"] = {
    "displayName": "Café Comptoir Abel",
    "region": "lyon",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "점심 12:00–14:00 · 저녁 19:30–22:00",
            "confidence": "official",
            "source": "https://www.cafecomptoirabel.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "연중무휴 (일요일 저녁 정상 영업)",
            "confidence": "official",
            "source": "https://www.cafecomptoirabel.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "공식 웹사이트 온라인 사전 예약 필수 (19:30 슬롯)",
            "confidence": "official",
            "source": "https://www.cafecomptoirabel.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "75–90분",
            "confidence": "editorial",
            "source": "FCR-04 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["daniel-et-denise"] = {
    "displayName": "Daniel et Denise",
    "region": "lyon",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "점심 12:00–14:00 · 저녁 19:30–22:00",
            "confidence": "official",
            "source": "https://danieletdenise.fr/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "매주 토요일·일요일 정기휴무 (월요일 저녁 정상 영업)",
            "confidence": "official",
            "source": "https://danieletdenise.fr/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "공식 웹사이트 온라인 사전 예약 필수 (월요일 19:45 슬롯)",
            "confidence": "official",
            "source": "https://danieletdenise.fr/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "75–90분",
            "confidence": "editorial",
            "source": "FCR-04 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["chez-mamie-lise"] = {
    "displayName": "Chez Mamie Lise",
    "region": "lyon",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "점심 12:00–14:00 · 저녁 19:00–22:00",
            "confidence": "official",
            "source": "https://www.chez-mamie-lise.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "연중무휴 (수요일 점심 정상 영업)",
            "confidence": "official",
            "source": "https://www.chez-mamie-lise.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "온라인 예약 또는 전화 사전 예약 권장 (점심 12:30 슬롯)",
            "confidence": "official",
            "source": "https://www.chez-mamie-lise.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "60–75분",
            "confidence": "editorial",
            "source": "FCR-04 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

with open("data/place-facts.json", "w", encoding="utf-8") as f:
    json.dump(pfacts, f, indent=2, ensure_ascii=False)

print("Updated place-days.json and place-facts.json for Lyon and Annecy")
