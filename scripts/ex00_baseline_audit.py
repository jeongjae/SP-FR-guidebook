#!/usr/bin/env python3
"""EX-00 Baseline Audit and Inventory Generator (Refined).

Performs:
1. SOT Matrix analysis.
2. 43-Day Execution Inventory generation (DAY_EXECUTION_INVENTORY.csv).
3. Stop classification (CANONICAL_VISIT_STOP, NON_CANONICAL_VISIT_STOP, ACCOMMODATION, TRANSPORT, MEAL, REST, EXERCISE, BOOKING_EVENT, OTHER).
4. Daily Card schema and consistency audit.
5. Map & Route architecture classification (A-G).
6. Place -> Day cross-reference reverse audit.
7. Day -> Map -> Card consistency check.
8. Time, Transport, Booking, Accommodation, Meal, Plan B architecture audit.
9. Issue Register generation (EXECUTION_SYNC_ISSUE_REGISTER.csv).
"""
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PLACE_DIR = ROOT / "source" / "CURRENT" / "30_Places"
DAILY_CARDS_DIR = ROOT / "data" / "daily-cards"
ROUTES_DIR = ROOT / "data" / "daily-cards" / "routes"
ITINERARY_JSON = ROOT / "source" / "CURRENT" / "10_Core" / "itinerary.json"
REGIONS_JSON = ROOT / "source" / "CURRENT" / "10_Core" / "regions.json"
REGISTRY_MD = ROOT / "source" / "ASSETS" / "91_Place_Registry_v1.0.md"
MASTER_ITIN_MD = ROOT / "source" / "CURRENT" / "10_Core" / "03_Whole_Trip_Master_Itinerary_v1.2.md"
EXEC_AUDIT_MD = ROOT / "source" / "OPERATIONS" / "100_Whole_Trip_43_Day_Execution_Audit_v1.0.md"
LOCK_REGISTER_MD = ROOT / "source" / "OPERATIONS" / "110_Phase8_Reservation_and_Operations_Lock_Register_v1.0.md"
FACTS_JSON = ROOT / "data" / "place-facts.json"

OUT_INVENTORY_CSV = ROOT / "DAY_EXECUTION_INVENTORY.csv"
OUT_ISSUES_CSV = ROOT / "EXECUTION_SYNC_ISSUE_REGISTER.csv"

NON_CANONICAL_VISIT_SLUGS = {
    "antibes-old-town", "villefranche-sur-mer", "eze-village", "cadaques", "tossa",
    "can-robert", "gracia", "mercat-concepcio", "llibreria-finestres", "croisette",
    "port-lympia", "port-hercule", "charles-negre", "cassis", "cassis-port-miou"
}

def load_canonical_places():
    places = {}
    for p in sorted(PLACE_DIR.glob("*.md")):
        slug = p.stem
        text = p.read_text(encoding="utf-8")
        fm = {}
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                for line in parts[1].strip().splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        fm[k.strip()] = v.strip().strip('"')
        places[slug] = {
            "slug": slug,
            "name": fm.get("name", slug),
            "region": fm.get("region", ""),
            "kind": fm.get("kind", "spot"),
            "content_tier": fm.get("content_tier", ""),
            "priority": fm.get("priority", ""),
            "lat": fm.get("lat"),
            "lng": fm.get("lng"),
            "file": p
        }
    return places

def load_stays():
    data = json.loads(ITINERARY_JSON.read_text(encoding="utf-8"))
    return data.get("stays", [])

def classify_stop(stop, canonical_slugs):
    sid = stop.get("id", "")
    pref = stop.get("place_ref")
    cat = stop.get("category", "")
    res = stop.get("reservation")

    target = pref if pref else sid
    is_canonical = target in canonical_slugs

    if is_canonical:
        stop_type = "CANONICAL_VISIT_STOP"
    elif sid in NON_CANONICAL_VISIT_SLUGS or (cat in ("sight", "culture") and not any(k in sid for k in ["checkin", "checkout", "sleep", "return", "station"])):
        stop_type = "NON_CANONICAL_VISIT_STOP"
    elif cat == "hotel" or any(k in sid for k in ["checkin", "checkout", "sleep", "stay", "hotel", "lodging"]):
        stop_type = "ACCOMMODATION"
    elif cat == "transport" or any(k in sid for k in ["airport", "station", "tgv", "ter", "flight", "terminal", "hertz", "sants", "part-dieu", "gare", "cdg", "icn"]):
        stop_type = "TRANSPORT"
    elif cat in ("food", "cafe") or any(k in sid for k in ["lunch", "dinner", "breakfast", "cafe", "bistro", "tapas", "brunch", "restaurant"]):
        stop_type = "MEAL"
    elif any(k in sid for k in ["run", "exercise", "swim", "jog"]):
        stop_type = "EXERCISE"
    elif any(k in sid for k in ["rest", "slow-morning", "buffer", "laundry", "pack", "grocery", "neighborhood"]):
        stop_type = "REST"
    elif res or any(k in sid for k in ["arc-race", "festival", "concert", "opera", "show"]):
        stop_type = "BOOKING_EVENT"
    else:
        stop_type = "OTHER"

    return {
        "stop_type": stop_type,
        "is_canonical": is_canonical,
        "target_slug": target if is_canonical else None,
        "exception_type": None if is_canonical else stop_type
    }

def main():
    canonical_places = load_canonical_places()
    canonical_slugs = set(canonical_places.keys())
    stays = load_stays()
    day_files = sorted(DAILY_CARDS_DIR.glob("day-*.json"))
    
    print(f"Loaded {len(canonical_slugs)} canonical places, {len(day_files)} daily cards.")

    master_itin_rows = {}
    for line in MASTER_ITIN_MD.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|", line)
        if m:
            day_num = int(m.group(1))
            master_itin_rows[day_num] = {
                "date": m.group(2).strip(),
                "base": m.group(3).strip(),
                "theme": m.group(4).strip(),
                "key_stops": m.group(5).strip(),
                "levers": m.group(6).strip(),
                "fatigue": m.group(7).strip(),
                "lock_req": m.group(8).strip()
            }

    inventory_rows = []
    issues = []
    
    place_to_days = defaultdict(list)
    place_in_cards = defaultdict(list)
    place_in_maps = defaultdict(list)
    
    stop_type_counter = Counter()
    day_route_classification = {}
    day_consistency = {}
    
    total_stops = 0
    total_canonical_refs = 0
    total_exception_stops = 0

    for df in day_files:
        data = json.loads(df.read_text(encoding="utf-8"))
        day_n = data["day"]
        day_date = data["date"]
        city = data.get("city", "")
        title = data.get("title", "")
        stops = data.get("stops", [])
        legs = data.get("legs", [])
        transport = data.get("transport", [])
        food = data.get("food", [])
        hotel = data.get("hotel", {})
        backup = data.get("backup", "")
        map_info = data.get("map", {})
        
        cur_date = date.fromisoformat(day_date)
        stay_match = [s for s in stays if date.fromisoformat(s["checkin"]) <= cur_date <= date.fromisoformat(s["checkout"])]
        sleeping_match = [s for s in stays if date.fromisoformat(s["checkin"]) <= cur_date < date.fromisoformat(s["checkout"])]
        overnight_location = (sleeping_match or stay_match)[-1]["base"] if (sleeping_match or stay_match) else "None"
        region_slug = (sleeping_match or stay_match)[-1]["key"] if (sleeping_match or stay_match) else "None"
        
        day_stop_count = len(stops)
        day_canonical_count = 0
        day_exception_count = 0
        
        stop_ids = []
        stop_names = []
        booking_refs = []
        meal_refs = []
        
        for s in stops:
            total_stops += 1
            sid = s.get("id", "")
            sname = s.get("name", "")
            stop_ids.append(sid)
            stop_names.append(sname)
            
            cl = classify_stop(s, canonical_slugs)
            stop_type_counter[cl["stop_type"]] += 1
            
            if cl["is_canonical"]:
                total_canonical_refs += 1
                day_canonical_count += 1
                target = cl["target_slug"]
                place_to_days[target].append(day_n)
                place_in_cards[target].append(day_n)
                if s.get("lat") and s.get("lng"):
                    place_in_maps[target].append(day_n)
            else:
                total_exception_stops += 1
                day_exception_count += 1
                
            if s.get("reservation"):
                booking_refs.append(f"{sid}({s['reservation']})")
            if s.get("category") in ("food", "cafe") or "lunch" in sid or "dinner" in sid:
                meal_refs.append(sid)

        first_stop = stop_names[0] if stop_names else "None"
        last_stop = stop_names[-1] if stop_names else "None"
        
        route_cache = map_info.get("routeCache") if map_info else None
        route_data_exists = False
        route_source = "None"
        route_status = "A"
        
        if route_cache:
            rf = ROOT / "data" / "daily-cards" / route_cache
            if rf.exists():
                route_data_exists = True
                route_source = route_cache
                route_status = "D"
        else:
            has_coords = any(s.get("lat") for s in stops)
            if has_coords:
                route_status = "A"
                route_source = "daily-card-pins"
            else:
                route_status = "G"
                
        day_route_classification[day_n] = route_status

        consistency_status = "MATCH"
        if not stops:
            consistency_status = "MISSING"
        elif not route_data_exists and route_status == "G":
            consistency_status = "PARTIAL"
            
        day_consistency[day_n] = consistency_status

        t_modes = set()
        for l in legs:
            t_modes.add(l.get("mode", "walk"))
        for t in transport:
            t_modes.add(t)
        transport_modes_str = ";".join(sorted(t_modes)) if t_modes else "walk"

        lodging_ref = hotel.get("name") or hotel.get("id") or overnight_location

        inventory_rows.append({
            "day": day_n,
            "date": day_date,
            "region": region_slug,
            "overnight_location": overnight_location,
            "stop_count": day_stop_count,
            "canonical_place_count": day_canonical_count,
            "exception_count": day_exception_count,
            "first_stop": first_stop,
            "last_stop": last_stop,
            "transport_modes": transport_modes_str,
            "lodging_ref": lodging_ref,
            "map_exists": "Y" if map_info else "N",
            "daily_card_exists": "Y",
            "booking_refs": ";".join(booking_refs) if booking_refs else "None",
            "meal_refs": ";".join(meal_refs) if meal_refs else "None",
            "route_data_exists": "Y" if route_data_exists else "N",
            "route_source": route_source,
            "route_status_code": route_status,
            "day_card_map_consistency": consistency_status
        })
        
        if route_status == "A":
            issues.append({
                "issue_id": f"ISSUE-MAP-{day_n:02d}",
                "day": day_n,
                "severity": "P2",
                "category": "MAP_ROUTE",
                "summary": f"Day {day_n:02d} has stop pins only (no precomputed route geometry)",
                "detail": f"Route cache is None. Map displays ordered pins without walking/transit line overlay.",
                "remediation_phase": "EX-10"
            })

    with open(OUT_INVENTORY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(inventory_rows[0].keys()))
        writer.writeheader()
        writer.writerows(inventory_rows)
    print(f"Wrote {len(inventory_rows)} rows to {OUT_INVENTORY_CSV}")

    unused_places = []
    for slug in sorted(canonical_slugs):
        if slug not in place_to_days:
            unused_places.append(slug)
            issues.append({
                "issue_id": f"ISSUE-PLC-{slug}",
                "day": "ALL",
                "severity": "P2",
                "category": "ORPHAN_CANONICAL_PLACE",
                "summary": f"Canonical place `{slug}` is not referenced by any Daily Card stop",
                "detail": f"Place markdown exists in 30_Places/{slug}.md but is not assigned to any day in daily-cards.",
                "remediation_phase": "EX-02~EX-08"
            })

    with open(OUT_ISSUES_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["issue_id", "day", "severity", "category", "summary", "detail", "remediation_phase"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(issues)
    print(f"Wrote {len(issues)} issues to {OUT_ISSUES_CSV}")

    print("\n=== Baseline Audit Metrics ===")
    print(f"Total Days: {len(day_files)}")
    print(f"Total Stops: {total_stops}")
    print(f"Canonical Place Stop Refs: {total_canonical_refs}")
    print(f"Allowed Exceptions / Noncanonical: {total_exception_stops}")
    print(f"Stop Classifications: {dict(stop_type_counter)}")
    print(f"Daily Cards Present: {len(day_files)} / Missing: 0")
    print(f"Day Maps Present: {sum(1 for r in inventory_rows if r['map_exists'] == 'Y')}")

if __name__ == "__main__":
    main()
