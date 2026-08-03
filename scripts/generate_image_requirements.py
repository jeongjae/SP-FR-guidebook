#!/usr/bin/env python3
"""Generate the normalized image requirement inventory from authoritative sources."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "source" / "ASSETS" / "91_Place_Registry_v1.0.md"
OUTPUT = ROOT / "data" / "image-requirements.csv"

REGION_PAGES = {
    "barcelona": "chapters/barcelona/index.html",
    "girona": "chapters/girona/index.html",
    "nice": "chapters/nice/index.html",
    "aix": "chapters/aix/index.html",
    "luberon": "chapters/luberon/index.html",
    "avignon": "chapters/avignon/index.html",
    "lyon": "chapters/lyon/index.html",
    "paris": "chapters/paris/index.html",
}

REGION_NAMES = {
    "barcelona": "Barcelona · Sitges",
    "girona": "Girona · Costa Brava",
    "nice": "Nice · Côte d’Azur",
    "aix": "Aix-en-Provence",
    "luberon": "Luberon",
    "avignon": "Avignon · Alpilles",
    "lyon": "Lyon · Annecy",
    "paris": "Paris",
}

FOODS = {
    "barcelona": ["Pa amb tomàquet", "Escalivada", "Fideuà", "Crema catalana"],
    "girona": ["Xuixo", "Suquet de peix", "Arròs a la cassola", "Botifarra"],
    "nice": ["Socca", "Pissaladière", "Pan bagnat", "Salade niçoise", "Petits farcis"],
    "aix": ["Calisson", "Tapenade", "Aïoli provençal"],
    "luberon": ["Melon de Cavaillon", "Fromage de chèvre", "Olives de Provence"],
    "avignon": ["Papaline d’Avignon", "Daube provençale", "Fougasse"],
    "lyon": ["Quenelle", "Salade lyonnaise", "Saucisson brioché", "Tarte à la praline"],
    "paris": ["Croissant", "Pain au chocolat", "Jambon-beurre", "Crème brûlée"],
}

SAMPLE_IDS = {
    "region-barcelona", "sagrada-familia", "sant-pau-recinte-modernista",
    "barri-gotic", "sitges", "food-barcelona-pa-amb-tomaquet",
    "food-barcelona-crema-catalana", "market-barcelona-mercat-concepcio",
    "region-girona", "girona-cathedral", "girona-walls", "collioure",
    "peratallada", "calella-de-palafrugell", "food-girona-xuixo",
    "food-girona-suquet-de-peix", "region-nice", "cours-saleya", "vieux-nice",
    "colline-du-chateau", "le-suquet", "monaco", "food-nice-socca",
    "food-nice-pissaladiere",
}

FIELDS = [
    "id", "page", "section", "subjectType", "subjectName", "city", "priority",
    "preferredOrientation", "currentImage", "candidateSource", "status", "notes",
]


def slug(value: str) -> str:
    import unicodedata

    value = "".join(c for c in unicodedata.normalize("NFKD", value.lower())
                    if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def subject_type(name: str, item_type: str) -> str:
    low = name.lower()
    if item_type == "node":
        return "transport"
    if any(x in low for x in ("market", "marché", "mercat", "halles", "시장")):
        return "market"
    if any(x in low for x in ("musée", "museu", "museum", "macba", "biblioteca", "bnf", "louvre")):
        return "museum"
    if any(x in low for x in ("quarter", "vieux nice", "marais", "montmartre", "montorgueil", "croix-rousse", "barri")):
        return "neighborhood"
    if any(x in low for x in ("calanques", "park", "parc", "beach", "해변", "montagne", "river", "강변")):
        return "nature"
    if any(x in low for x in ("pals", "peratallada", "collioure", "gordes", "bonnieux", "goult", "menerbes", "oppède", "saint-rémy", "lourmarin")):
        return "village"
    return "attraction"


def row(*, item_id, page, section, kind, name, region, priority, current=""):
    sample = item_id in SAMPLE_IDS
    return {
        "id": item_id,
        "page": page,
        "section": section,
        "subjectType": kind,
        "subjectName": name,
        "city": REGION_NAMES[region],
        "priority": priority,
        "preferredOrientation": "landscape",
        "currentImage": current,
        "candidateSource": "Wikimedia Commons",
        "status": "sample-selected" if sample else "IMAGE_PENDING",
        "notes": "Phase 1 sample; file-level license verification required" if sample else
                 "Reason: no clearly reusable representative image selected yet",
    }


def main() -> None:
    rows = []
    for region, page in REGION_PAGES.items():
        rows.append(row(item_id=f"region-{region}", page=page, section="지역소개",
                        kind="city" if region not in {"luberon"} else "region",
                        name=REGION_NAMES[region], region=region, priority="P0",
                        current=f"assets/heroes/{region}.jpg"))

    region = None
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^## ([a-z-]+) \(", line)
        if match:
            region = match.group(1)
            continue
        if not region or not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 8:
            continue
        item_slug = cells[0].strip("`")
        name, item_type, grade = cells[1], cells[2], cells[3]
        if item_type not in {"spot", "node"}:
            continue
        priority = "P0" if "필수" in grade else ("P1" if "우선" in grade else "P2")
        current = "Wikipedia runtime hotlink" if cells[7] != "—" else ""
        rows.append(row(item_id=item_slug,
                        page=f"places/{item_slug}.html" if item_type == "spot" else REGION_PAGES[region],
                        section="교통" if item_type == "node" else "장소",
                        kind=subject_type(name, item_type), name=name, region=region,
                        priority=priority, current=current))

    # The Barcelona living-market sample is a requirement independent of the place registry.
    rows.append(row(item_id="market-barcelona-mercat-concepcio",
                    page="chapters/barcelona/food.html", section="시장", kind="market",
                    name="Mercat de la Concepció", region="barcelona", priority="P0"))
    # Girona's wall is described in the chapter but is not a separate registry row.
    rows.append(row(item_id="girona-walls", page="chapters/girona/places.html",
                    section="장소", kind="attraction", name="Passeig de la Muralla",
                    region="girona", priority="P0"))

    for region, foods in FOODS.items():
        for index, food in enumerate(foods):
            item_id = f"food-{region}-{slug(food)}"
            rows.append(row(item_id=item_id, page=f"chapters/{region}/food.html",
                            section="먹거리", kind="food", name=food, region=region,
                            priority="P0" if index < 2 else "P2"))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"image requirements: {len(rows)} rows -> {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
