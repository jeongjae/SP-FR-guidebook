#!/usr/bin/env python3
"""Day–Place canonical relationship 전수 감사.

UI 링크 반복이 아니라 데이터 관계를 검사한다. ``place_ref``와
``related_place_refs``는 canonical visit만 뜻하며, context/transit/nearby는
``place_relation``으로 명시하고 Place backlink를 만들지 않는다.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import model


ROOT = Path(__file__).resolve().parent.parent
DAILY = ROOT / "data" / "daily-cards"
PLACE_DIR = ROOT / "source" / "CURRENT" / "30_Places"
SITE = ROOT / "site"

# 실제 상호가 정해지지 않은 식사, 복합 도시/산책 구간, 기존 상위 Place의
# 세부 구간이다. 이 목록 밖에서 culture/sight/food/shopping stop이 Place 없이
# 추가되면 Missing Place로 실패한다.
MISSING_PLACE_ALLOWLIST = {
    (2, "avinguda-gaudi"), (2, "gracia"), (3, "llibreria-finestres"),
    (5, "cadaques"), (5, "collioure-lunch"), (6, "tossa"),
    (6, "sant-feliu"), (8, "port-lympia"), (8, "vieux-nice-lunch"),
    (8, "chez-pipo"), (9, "antibes-old-town"),
    (10, "menton-dinner"),
    (11, "villefranche-sur-mer"), (11, "eze-village"),
    (12, "moustiers-evening"), (13, "lapalud-lunch"),
    (14, "marseille-lunch"), (14, "vallon-des-auffes"),
    (15, "aix-lunch"), (16, "cassis-port-miou"),
    (17, "lourmarin-lunch"), (18, "roussillon-lunch"),
    (19, "saint-remy-lunch"), (20, "pont-du-gard-lunch"),
    (19, "avignon-settle"),
    (22, "vieil-avignon"), (22, "palais-lunch"),
    (24, "rosaire-descent"), (24, "saone-presquile"),
    (24, "vieux-lyon-lunch"), (25, "maison-des-canuts"),
    (25, "halles-shopping"), (26, "lakefront"),
    (26, "annecy-cruise"), (27, "part-dieu-lunch"),
    (27, "first-grocery"),
    (28, "city-bus-tour"), (29, "cite-seine-walk"),
    (30, "marais-lunch"), (30, "tuileries-vendome"),
    (30, "palais-royal"), (30, "opera-garnier-district"),
    (33, "avenue-montaigne"), (33, "palais-de-tokyo"),
    (34, "invalides-exterior"), (35, "cour-carree-seine"),
    (36, "ranelagh-passy"), (37, "prix-de-l-arc"),
    (38, "parc-monceau"), (41, "trocadero-sunset"),
}

# 이름에 이동/산책 같은 단어가 있어도 실제 canonical visit인 검토 완료 stop.
CONTEXT_WORD_VISIT_ALLOWLIST = {
    (3, "barri-gotic"), (7, "vy1521"), (7, "promenade"),
    (9, "nice-ville"), (10, "nice-ville"), (11, "nice-ville"),
    (12, "point-sublime"), (13, "plateau-de-valensole"),
    (13, "rotonde"), (15, "cours-mirabeau"), (16, "cassis-port"),
    (17, "lourmarin"), (17, "gordes-village"), (18, "senanque"),
    (20, "maison-carree"), (25, "croix-rousse-market"),
    (27, "paris-return"), (35, "morning-routine"),
    (40, "vendanges-montmartre"),
}

EXPECTED_VISITS = {
    "sainte-chapelle": [29],
    "conciergerie": [29],
    "arc-de-triomphe": [31],
    "grand-palais": [28],
    "versailles": [32],
    "musee-guimet": [33],
    "musee-picasso-paris": [30],
    "musee-d-orsay": [34, 39],
    "musee-du-louvre": [35],
}

# 레지스트리가 의도적으로 제공하는 비일정 탐색 shell. Day visit Place와 달리
# 독립 장문·역링크를 요구하지 않는다.
SOURCELESS_NAVIGATION_SHELLS = {
    "sitges", "barcelona-historic-walk", "barcelona-modernisme-walk",
    "girona-old-town-walk",
}

FALSE_LINK_WORDS = re.compile(r"주변|외관|경유|방면|출발|도착|이동|전망|산책")
REQUIRED_CATEGORIES = {"culture", "sight", "food", "shopping", "market", "cafe"}


def _search_entries() -> list[dict]:
    path = SITE / "assets" / "search-index.js"
    if not path.exists():
        return []
    match = re.fullmatch(
        r"window\.SEARCH_INDEX\s*=\s*(\[.*\]);\s*",
        path.read_text(encoding="utf-8"), re.S,
    )
    return json.loads(match.group(1)) if match else []


def audit() -> dict[str, list[str]]:
    trip = model.load_trip()
    result = {
        "Broken URL": [], "Missing Place": [], "False Place": [],
        "Duplicate Relationship": [], "Stale Reference": [],
        "Search Mismatch": [], "Map Mismatch": [], "Orphan Place": [],
    }

    visits: dict[str, list[int]] = {}
    for day in trip.days:
        pairs: list[str] = []
        for stop in day.stops:
            refs = ([stop.place.slug] if stop.place else []) + [
                place.slug for place in stop.related_places
            ]
            pairs.extend(refs)
            for slug in refs:
                visits.setdefault(slug, []).append(day.n)

            key = (day.n, stop.id)
            relation = stop.place_relation
            if relation != "visit" and refs:
                result["False Place"].append(
                    f"Day {day.n} {stop.id}: {relation} relation has canonical ref"
                )
            if (stop.category in REQUIRED_CATEGORIES and not refs
                    and relation == "visit" and key not in MISSING_PLACE_ALLOWLIST):
                result["Missing Place"].append(
                    f"Day {day.n} {stop.id}: {stop.name}"
                )
            if refs and FALSE_LINK_WORDS.search(stop.name) \
                    and key not in CONTEXT_WORD_VISIT_ALLOWLIST:
                result["False Place"].append(
                    f"Day {day.n} {stop.id}: context-like name → {','.join(refs)}"
                )

        for slug, count in Counter(pairs).items():
            if count > 1:
                result["Duplicate Relationship"].append(
                    f"Day {day.n} → {slug}: {count} canonical visits"
                )

    for slug, expected in EXPECTED_VISITS.items():
        actual = sorted(visits.get(slug, []))
        if actual != expected:
            result["Stale Reference"].append(
                f"{slug}: expected {expected}, got {actual}"
            )

    day29 = (DAILY / "day-29.json").read_text(encoding="utf-8")
    if "Musée du Luxembourg" in day29:
        result["Stale Reference"].append("Day 29: Musée du Luxembourg remains")

    # Registry, Place source, generated URL은 한 엔티티로 함께 존재해야 한다.
    for slug, place in trip.places.items():
        if (slug not in SOURCELESS_NAVIGATION_SHELLS
                and not (PLACE_DIR / f"{slug}.md").is_file()):
            result["Orphan Place"].append(f"{slug}: canonical source missing")
        if place.region not in {region.slug for region in trip.regions}:
            result["Orphan Place"].append(f"{slug}: region {place.region} missing")
        generated = SITE / "places" / f"{slug}.html"
        if SITE.exists() and not generated.is_file():
            result["Broken URL"].append(f"places/{slug}.html missing")

    entries = _search_entries()
    if SITE.exists() and not entries:
        result["Search Mismatch"].append("search-index.js missing or unreadable")
    if entries:
        place_entries = [entry for entry in entries if entry.get("k") == "place"]
        urls = Counter(entry.get("u") for entry in place_entries)
        for slug in trip.places:
            url = f"places/{slug}.html"
            if urls[url] != 1:
                result["Search Mismatch"].append(
                    f"{url}: {urls[url]} search entries"
                )

    # Place 페이지의 지도는 canonical map query를 사용한다. execution map은
    # stop별 핀 ID를 쓰므로 두 ID 공간을 전역 동등 비교하지 않는다.
    for day in trip.days:
        for stop in day.stops:
            for slug in ([stop.place.slug] if stop.place else []) + [
                place.slug for place in stop.related_places
            ]:
                if not trip.places[slug].map_query:
                    result["Map Mismatch"].append(
                        f"Day {day.n} {stop.id}: {slug} has no canonical map query"
                    )

    route_data = json.loads(
        (ROOT / "source/ASSETS/maps/daily-routes.json").read_text(encoding="utf-8")
    )
    route_by_date = {row["date"]: row for row in route_data["days"]}
    required_pins = {
        "2026-09-26": {"sainte-chapelle", "conciergerie"},
        "2026-09-28": {"arc-de-triomphe"},
        "2026-09-29": {"versailles"},
    }
    for date_value, required in required_pins.items():
        pins = [stop["placeId"] for stop in route_by_date[date_value]["stops"]]
        for slug in required:
            if pins.count(slug) != 1:
                result["Map Mismatch"].append(
                    f"{date_value}: {slug} pin count {pins.count(slug)}"
                )
    day33_pins = {
        stop["placeId"] for stop in route_by_date["2026-09-30"]["stops"]
    }
    if "grand-palais" in day33_pins:
        result["Map Mismatch"].append("2026-09-30: Grand Palais context pin remains")

    return result


def main() -> int:
    report = audit()
    total = sum(len(rows) for rows in report.values())
    print("Day–Place relationship audit: 43 days")
    for label, rows in report.items():
        print(f"  {label}: {len(rows)}")
        for row in rows[:20]:
            print(f"    - {row}")
    if total:
        print(f"FAIL: {total} relationship error(s)")
        return 1
    print("PASS: canonical visit/backlink/search/map relationship errors 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
