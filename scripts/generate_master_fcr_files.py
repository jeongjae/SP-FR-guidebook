import csv
import glob
from pathlib import Path

ROOT = Path(".")

# 1. Regional Food Guide Master Matrix
rf_files = sorted(glob.glob("FCR0*_REGIONAL_FOOD_MATRIX.csv") + glob.glob("FCR0*_ANNECY_SAVOY_FOOD_MATRIX.csv") + glob.glob("FCR01_NICE_REGIONAL_FOOD_MATRIX.csv"))
master_rf = []
seen_slugs = set()
all_rf_keys = set()

for rff in rf_files:
    with open(rff, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = row.get("food_slug")
            if slug and slug not in seen_slugs:
                seen_slugs.add(slug)
                master_rf.append(row)
                all_rf_keys.update(row.keys())

fieldnames_rf = ["food_slug", "local_name", "name_ko", "region", "category", "short_intro", "typical_price", "best_context", "recommended_venues", "scheduled_days", "source"]
for k in all_rf_keys:
    if k not in fieldnames_rf:
        fieldnames_rf.append(k)

if master_rf:
    with open("FCR_REGIONAL_FOOD_GUIDE_MATRIX.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames_rf, extrasaction='ignore')
        w.writeheader()
        w.writerows(master_rf)
    print(f"Generated FCR_REGIONAL_FOOD_GUIDE_MATRIX.csv ({len(master_rf)} foods)")

# 2. Restaurant & Café & Market Master Research
res_files = sorted(glob.glob("FCR0*_RESTAURANT_CAFE_*.csv") + glob.glob("FCR01_NICE_VENUE_RESEARCH.csv"))
master_res = []
seen_venues = set()
all_res_keys = set()

for rf in res_files:
    with open(rf, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = row.get("place_slug") or row.get("venue_slug")
            if slug and slug not in seen_venues:
                seen_venues.add(slug)
                if not row.get("place_slug") and row.get("venue_slug"):
                    row["place_slug"] = row["venue_slug"]
                master_res.append(row)
                all_res_keys.update(row.keys())

fieldnames_res = ["place_slug", "name", "region", "selection_origin", "meal_role", "food_kind", "address", "lat", "lng", "opening_hours", "closed_days", "reservation_requirement", "price_range", "signature_dishes", "scheduled_day", "verified_at", "source_url"]
for k in all_res_keys:
    if k not in fieldnames_res:
        fieldnames_res.append(k)

if master_res:
    with open("FCR_RESTAURANT_CAFE_MARKET_RESEARCH.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames_res, extrasaction='ignore')
        w.writeheader()
        w.writerows(master_res)
    print(f"Generated FCR_RESTAURANT_CAFE_MARKET_RESEARCH.csv ({len(master_res)} venues)")

# 3. Master Food Place Registry
with open("PLACE_TAXONOMY_AND_TIERS.csv", "r", encoding="utf-8") as f:
    places_rows = list(csv.DictReader(f))

food_places = [r for r in places_rows if r.get("normalized_type") in ["restaurant", "bakery", "market", "cafe"] or "food" in r.get("rationale", "").lower() or "맛집" in r.get("rationale", "") or "부숑" in r.get("rationale", "") or "식당" in r.get("rationale", "")]
with open("FCR_FOOD_PLACE_REGISTRY.csv", "w", newline="", encoding="utf-8") as f:
    if food_places:
        w = csv.DictWriter(f, fieldnames=list(food_places[0].keys()))
        w.writeheader()
        w.writerows(food_places)
print(f"Generated FCR_FOOD_PLACE_REGISTRY.csv ({len(food_places)} food places)")

# 4. Master Food Inventory
with open("FCR_MASTER_FOOD_INVENTORY.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["item_type", "slug", "name", "region", "status", "notes"])
    for rf in master_rf:
        w.writerow(["REGIONAL_FOOD", rf.get("food_slug"), rf.get("name_ko"), rf.get("region"), "ACTIVE", rf.get("category")])
    for fp in food_places:
        w.writerow(["FOOD_PLACE", fp.get("id"), fp.get("name"), fp.get("region"), "ACTIVE", fp.get("normalized_type")])

print("Generated FCR_MASTER_FOOD_INVENTORY.csv")

# 5. Master Daily Food Link Matrix
with open("FCR_DAILY_FOOD_LINK_MATRIX.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["day", "stop_id", "stop_name", "place_ref", "region", "status"])
    for d in range(1, 44):
        p = Path(f"data/daily-cards/day-{d:02d}.json")
        if p.exists():
            import json
            ddata = json.loads(p.read_text(encoding="utf-8"))
            for s in ddata.get("stops", []):
                if s.get("category") in ["food", "shopping"] or s.get("place_ref") in [fp.get("id") for fp in food_places]:
                    w.writerow([f"Day {d:02d}", s.get("id"), s.get("name"), s.get("place_ref"), ddata.get("region", "general"), "VALID"])

print("Generated FCR_DAILY_FOOD_LINK_MATRIX.csv")

# 6. Master Volatile Recheck Register
with open("FCR06_VOLATILE_RECHECK_MASTER.csv", "r", encoding="utf-8") as f:
    vol_rows = list(csv.DictReader(f))

with open("FCR_VOLATILE_RECHECK_REGISTER.csv", "w", newline="", encoding="utf-8") as f:
    if vol_rows:
        w = csv.DictWriter(f, fieldnames=list(vol_rows[0].keys()))
        w.writeheader()
        w.writerows(vol_rows)

print("Generated FCR_VOLATILE_RECHECK_REGISTER.csv")
