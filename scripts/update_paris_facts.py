import json

# 1. Update place-days.json
with open("data/place-days.json", "r", encoding="utf-8") as f:
    pdays = json.load(f)

pdays["places"]["boulangerie-pichard"] = {
    "displayName": "Boulangerie Pichard",
    "region": "paris",
    "days": [28, 29, 31, 35, 38, 42]
}
pdays["places"]["marche-convention"] = {
    "displayName": "Marché Convention",
    "region": "paris",
    "days": [29, 31, 36]
}
pdays["places"]["cafe-du-commerce"] = {
    "displayName": "Café du Commerce",
    "region": "paris",
    "days": [28, 32]
}
pdays["places"]["le-grand-pan"] = {
    "displayName": "Le Grand Pan",
    "region": "paris",
    "days": [34, 41]
}
pdays["places"]["bouillon-chartier-montparnasse"] = {
    "displayName": "Bouillon Chartier Montparnasse",
    "region": "paris",
    "days": [30]
}

with open("data/place-days.json", "w", encoding="utf-8") as f:
    json.dump(pdays, f, indent=2, ensure_ascii=False)

# 2. Update place-facts.json
with open("data/place-facts.json", "r", encoding="utf-8") as f:
    pfacts = json.load(f)

pfacts["places"]["boulangerie-pichard"] = {
    "displayName": "Boulangerie Pichard",
    "region": "paris",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "수–일 07:00–13:30 / 15:30–20:00 (일 07:00–13:30)",
            "confidence": "official",
            "source": "https://www.paris.fr/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "매주 월요일·화요일 정기휴무",
            "confidence": "official",
            "source": "https://www.paris.fr/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "예약 불필요 — 테이크아웃 아티장 베이커리",
            "confidence": "official",
            "source": "https://www.paris.fr/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "10–15분",
            "confidence": "editorial",
            "source": "FCR-05 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["marche-convention"] = {
    "displayName": "Marché Convention",
    "region": "paris",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "화·목 07:00–13:30 · 일 07:00–14:30",
            "confidence": "official",
            "source": "https://www.paris.fr/equipements/marche-convention-5460",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "월·수·금·토 휴무 (인근 토요 대안: Marché Grenelle)",
            "confidence": "official",
            "source": "https://www.paris.fr/equipements/marche-convention-5460",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "예약 불필요 — 공설 노천 생활시장",
            "confidence": "official",
            "source": "https://www.paris.fr/equipements/marche-convention-5460",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "30–45분",
            "confidence": "editorial",
            "source": "FCR-05 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["cafe-du-commerce"] = {
    "displayName": "Café du Commerce",
    "region": "paris",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "매일 11:30–23:30 (브레이크타임 없음)",
            "confidence": "official",
            "source": "https://www.lecafeducommerce.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "연중무휴",
            "confidence": "official",
            "source": "https://www.lecafeducommerce.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "온라인 예약 또는 워크인 상시 입장 가능 (250석)",
            "confidence": "official",
            "source": "https://www.lecafeducommerce.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "75–90분",
            "confidence": "editorial",
            "source": "FCR-05 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["le-grand-pan"] = {
    "displayName": "Le Grand Pan",
    "region": "paris",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "점심 12:00–14:30 · 저녁 19:30–22:30",
            "confidence": "official",
            "source": "https://www.legrandpan.fr/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "매주 토요일·일요일 정기휴무 (월–금 평일 영업)",
            "confidence": "official",
            "source": "https://www.legrandpan.fr/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "사전 예약 필수 (공식 사이트 온라인 예약, 저녁 19:30 또는 20:00)",
            "confidence": "official",
            "source": "https://www.legrandpan.fr/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "90–105분",
            "confidence": "editorial",
            "source": "FCR-05 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["bouillon-chartier-montparnasse"] = {
    "displayName": "Bouillon Chartier Montparnasse",
    "region": "paris",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "매일 11:30–24:00 (브레이크타임 없음)",
            "confidence": "official",
            "source": "https://www.bouillon-chartier.com/montparnasse/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "연중무휴",
            "confidence": "official",
            "source": "https://www.bouillon-chartier.com/montparnasse/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "예약 불가 (선착순 입장, 18:30 이전 방문 시 대기 없음)",
            "confidence": "official",
            "source": "https://www.bouillon-chartier.com/montparnasse/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "60–75분",
            "confidence": "editorial",
            "source": "FCR-05 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

with open("data/place-facts.json", "w", encoding="utf-8") as f:
    json.dump(pfacts, f, indent=2, ensure_ascii=False)

print("Updated place-days.json and place-facts.json for Paris")
