import json

# 1. Update place-days.json
with open("data/place-days.json", "r", encoding="utf-8") as f:
    pdays = json.load(f)

pdays["places"]["patisserie-weibel"] = {
    "displayName": "Pâtisserie Weibel",
    "region": "aix",
    "days": [13]
}
pdays["places"]["chez-gilbert-cassis"] = {
    "displayName": "Chez Gilbert (Cassis)",
    "region": "aix",
    "days": [14]
}
pdays["places"]["fou-de-fafa-avignon"] = {
    "displayName": "Fou de Fafa (Avignon)",
    "region": "avignon",
    "days": [19, 20]
}
pdays["places"]["les-cocottes-saint-louis"] = {
    "displayName": "Les Cocottes Saint-Louis",
    "region": "avignon",
    "days": [20, 22]
}
pdays["places"]["le-gibolin-arles"] = {
    "displayName": "Le Gibolin (Arles)",
    "region": "avignon",
    "days": [22]
}

with open("data/place-days.json", "w", encoding="utf-8") as f:
    json.dump(pdays, f, indent=2, ensure_ascii=False)

# 2. Update place-facts.json
with open("data/place-facts.json", "r", encoding="utf-8") as f:
    pfacts = json.load(f)

pfacts["places"]["patisserie-weibel"] = {
    "displayName": "Pâtisserie Weibel",
    "region": "aix",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "화–일 07:30–19:00",
            "confidence": "official",
            "source": "https://www.maisonweibel.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "매주 월요일 정기휴무",
            "confidence": "official",
            "source": "https://www.maisonweibel.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "예약 불필요 (현장 방문 / 테라스석 선착순)",
            "confidence": "official",
            "source": "https://www.maisonweibel.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "40–50분",
            "confidence": "editorial",
            "source": "FCR-03 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["chez-gilbert-cassis"] = {
    "displayName": "Chez Gilbert",
    "region": "aix",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "점심 12:00–14:30 · 저녁 19:00–22:00",
            "confidence": "official",
            "source": "https://www.chezgilbert.net/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "매주 수요일·목요일 정기휴무 (금요일 점심 정상 영업)",
            "confidence": "official",
            "source": "https://www.chezgilbert.net/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "공식 웹사이트 또는 전화 사전 예약 필수 (테라스석)",
            "confidence": "official",
            "source": "https://www.chezgilbert.net/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "75–90분",
            "confidence": "editorial",
            "source": "FCR-03 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["fou-de-fafa-avignon"] = {
    "displayName": "Fou de Fafa",
    "region": "avignon",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "저녁 18:30–21:30",
            "confidence": "official",
            "source": "https://www.foudefafaavignon.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "매주 월요일·화요일 정기휴무 (수~일요일 저녁 정상 영업)",
            "confidence": "official",
            "source": "https://www.foudefafaavignon.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "사전 예약 필수 (공식 사이트 이메일/예약 폼 조기 예약)",
            "confidence": "official",
            "source": "https://www.foudefafaavignon.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "90–105분",
            "confidence": "editorial",
            "source": "FCR-03 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["les-cocottes-saint-louis"] = {
    "displayName": "Les Cocottes Saint-Louis",
    "region": "avignon",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "점심 12:00–14:00 · 저녁 19:00–22:00",
            "confidence": "official",
            "source": "https://www.cloitre-saint-louis.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "연중무휴",
            "confidence": "official",
            "source": "https://www.cloitre-saint-louis.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "온라인 예약 또는 전화 예약 가능 (정원 테라스석 권장)",
            "confidence": "official",
            "source": "https://www.cloitre-saint-louis.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "75–90분",
            "confidence": "editorial",
            "source": "FCR-03 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["le-gibolin-arles"] = {
    "displayName": "Le Gibolin",
    "region": "avignon",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "점심 12:00–14:00 · 저녁 19:30–21:30",
            "confidence": "official",
            "source": "https://www.arlestourisme.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "매주 일요일·월요일 정기휴무 (토요일 점심 정상 영업)",
            "confidence": "official",
            "source": "https://www.arlestourisme.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "전화 예약 또는 12:00 오픈 시각 현장 방문 권장",
            "confidence": "official",
            "source": "https://www.arlestourisme.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "60–75분",
            "confidence": "editorial",
            "source": "FCR-03 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

with open("data/place-facts.json", "w", encoding="utf-8") as f:
    json.dump(pfacts, f, indent=2, ensure_ascii=False)

print("Updated place-days.json and place-facts.json for Provence")
