import json

# 1. Update place-days.json
with open("data/place-days.json", "r", encoding="utf-8") as f:
    pdays = json.load(f)

pdays["places"]["bodega-joan"] = {
    "displayName": "Bodega Joan",
    "region": "barcelona",
    "days": [2]
}
pdays["places"]["la-paradeta-sagrada-familia"] = {
    "displayName": "La Paradeta Sagrada Família",
    "region": "barcelona",
    "days": [2]
}
pdays["places"]["bar-canete"] = {
    "displayName": "Bar Cañete",
    "region": "barcelona",
    "days": [3]
}
pdays["places"]["mercat-concepcio"] = {
    "displayName": "Mercat de la Concepció",
    "region": "barcelona",
    "days": [3]
}
pdays["places"]["la-zorra"] = {
    "displayName": "La Zorra",
    "region": "barcelona",
    "days": [4]
}
pdays["places"]["casa-marieta"] = {
    "displayName": "Casa Marieta",
    "region": "girona",
    "days": [4]
}
pdays["places"]["mercat-del-lleo"] = {
    "displayName": "Mercat del Lleó",
    "region": "girona",
    "days": [4, 5]
}

with open("data/place-days.json", "w", encoding="utf-8") as f:
    json.dump(pdays, f, indent=2, ensure_ascii=False)

# 2. Update place-facts.json
with open("data/place-facts.json", "r", encoding="utf-8") as f:
    pfacts = json.load(f)

pfacts["places"]["bodega-joan"] = {
    "displayName": "Bodega Joan",
    "region": "barcelona",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "매일 08:00–24:00 (식사: 12:30–16:00 · 19:30–23:30)",
            "confidence": "official",
            "source": "https://bodegajoan.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "연중무휴",
            "confidence": "official",
            "source": "https://bodegajoan.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "공식 웹사이트 온라인 예약 권장 (특히 주말 저녁)",
            "confidence": "official",
            "source": "https://bodegajoan.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "75–90분",
            "confidence": "editorial",
            "source": "FCR-02 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["la-paradeta-sagrada-familia"] = {
    "displayName": "La Paradeta Sagrada Família",
    "region": "barcelona",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "화–토 13:00–16:00 / 20:00–23:30 · 일 13:00–16:00 (일요일 저녁 휴무)",
            "confidence": "official",
            "source": "https://www.laparadeta.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "매주 월요일 정기휴무",
            "confidence": "official",
            "source": "https://www.laparadeta.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "예약 불가 (선착순 현장 대기, 오픈 10분 전 도착 권장)",
            "confidence": "official",
            "source": "https://www.laparadeta.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "60–75분",
            "confidence": "editorial",
            "source": "FCR-02 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["bar-canete"] = {
    "displayName": "Bar Cañete",
    "region": "barcelona",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "매일 13:00–24:00 (브레이크타임 없음)",
            "confidence": "official",
            "source": "https://barcanete.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "연중무휴",
            "confidence": "official",
            "source": "https://barcanete.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "공식 웹사이트 사전 예약 필수 (바 또는 테이블)",
            "confidence": "official",
            "source": "https://barcanete.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "75–90분",
            "confidence": "editorial",
            "source": "FCR-02 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["mercat-concepcio"] = {
    "displayName": "Mercat de la Concepció",
    "region": "barcelona",
    "grade": "priority",
    "facts": {
        "hours": {
            "value": "월–토 08:00–15:00 (화–토 일부 20:00까지, 꽃시장 24시간)",
            "confidence": "official",
            "source": "https://www.laconcepcio.cat/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "일요일 식품시장 휴무 (꽃시장은 연중무휴)",
            "confidence": "official",
            "source": "https://www.laconcepcio.cat/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "예약 불필요 — 공설 생활시장",
            "confidence": "official",
            "source": "https://www.laconcepcio.cat/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "40–50분",
            "confidence": "editorial",
            "source": "FCR-02 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["la-zorra"] = {
    "displayName": "La Zorra",
    "region": "barcelona",
    "grade": "priority",
    "facts": {
        "hours": {
            "value": "매일 점심 13:00–16:30 · 저녁 20:30–23:00",
            "confidence": "official",
            "source": "https://restaurantelazorra.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "연중무휴 (화요일 정상 영업)",
            "confidence": "official",
            "source": "https://restaurantelazorra.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "공식 웹사이트 사전 예약 필수 (13:00 점심 슬롯)",
            "confidence": "official",
            "source": "https://restaurantelazorra.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "75–90분",
            "confidence": "editorial",
            "source": "FCR-02 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["casa-marieta"] = {
    "displayName": "Casa Marieta",
    "region": "girona",
    "grade": "essential",
    "facts": {
        "hours": {
            "value": "매일 점심 13:00–16:00 · 저녁 20:00–23:00",
            "confidence": "official",
            "source": "https://casamarieta.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "연중무휴",
            "confidence": "official",
            "source": "https://casamarieta.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "공식 웹사이트 온라인 예약 가능 (테라스 또는 실내)",
            "confidence": "official",
            "source": "https://casamarieta.com/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "75–90분",
            "confidence": "editorial",
            "source": "FCR-02 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

pfacts["places"]["mercat-del-lleo"] = {
    "displayName": "Mercat del Lleó",
    "region": "girona",
    "grade": "priority",
    "facts": {
        "hours": {
            "value": "월–금 07:00–14:00 · 토 07:00–14:30",
            "confidence": "official",
            "source": "https://www.mercatdelleo.cat/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "closed": {
            "value": "일요일 및 공휴일 휴무",
            "confidence": "official",
            "source": "https://www.mercatdelleo.cat/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "booking": {
            "value": "예약 불필요 — 시립 중앙시장",
            "confidence": "official",
            "source": "https://www.mercatdelleo.cat/",
            "verified_at": "2026-08-21",
            "ttl_days": 90
        },
        "duration": {
            "value": "30–45분",
            "confidence": "editorial",
            "source": "FCR-02 Editorial",
            "verified_at": "2026-08-21",
            "ttl_days": 3650
        }
    }
}

with open("data/place-facts.json", "w", encoding="utf-8") as f:
    json.dump(pfacts, f, indent=2, ensure_ascii=False)

print("Updated place-days.json and place-facts.json for BCN and GIR")
