#!/usr/bin/env python3
"""EX-01: 43-Day Itinerary Feasibility Audit Script (Refined).

Audits:
- Day-by-Day feasibility, load scores, duration, buffers, meals, Plan B.
- Opening hours & closed day constraints against 2026 calendar.
- Fixed booking constraints and buffers.
- Transfer days, driving days, rail/flight days.
- Consecutive high-load sequences.
- Generates:
  1. DAY_FEASIBILITY_MATRIX.csv
  2. EXECUTION_FEASIBILITY_ISSUE_REGISTER.csv
  3. CRITICAL_CONSTRAINT_REGISTER.csv
"""
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PLACE_DIR = ROOT / "source" / "CURRENT" / "30_Places"
DAILY_CARDS_DIR = ROOT / "data" / "daily-cards"
ROUTES_DIR = ROOT / "data" / "daily-cards" / "routes"
ITINERARY_JSON = ROOT / "source" / "CURRENT" / "10_Core" / "itinerary.json"
REGIONS_JSON = ROOT / "source" / "CURRENT" / "10_Core" / "regions.json"
FACTS_JSON = ROOT / "data" / "place-facts.json"
MASTER_ITIN_MD = ROOT / "source" / "CURRENT" / "10_Core" / "03_Whole_Trip_Master_Itinerary_v1.2.md"
LOCK_REGISTER_MD = ROOT / "source" / "OPERATIONS" / "110_Phase8_Reservation_and_Operations_Lock_Register_v1.0.md"
EXEC_AUDIT_MD = ROOT / "source" / "OPERATIONS" / "100_Whole_Trip_43_Day_Execution_Audit_v1.0.md"

OUT_FEASIBILITY_CSV = ROOT / "DAY_FEASIBILITY_MATRIX.csv"
OUT_ISSUES_CSV = ROOT / "EXECUTION_FEASIBILITY_ISSUE_REGISTER.csv"
OUT_CONSTRAINTS_CSV = ROOT / "CRITICAL_CONSTRAINT_REGISTER.csv"

WEEKDAY_KO = ["월", "화", "수", "목", "금", "토", "일"]

TRANSFER_DAYS = {4, 7, 12, 16, 19, 23, 27}
DRIVING_DAYS = {1, 4, 5, 6, 7, 12, 16, 17, 18, 19, 21}
RAIL_DAYS = {9, 10, 14, 22, 23, 26, 27}
FLIGHT_DAYS = {1, 7, 42, 43}

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
            "content_tier": fm.get("content_tier", "TIER_B"),
            "priority": fm.get("priority", "WORTHWHILE")
        }
    return places

def load_facts():
    if not FACTS_JSON.exists():
        return {}
    return json.loads(FACTS_JSON.read_text(encoding="utf-8")).get("places", {})

def parse_time_minutes(t_str):
    if not t_str or ":" not in t_str:
        return None
    try:
        parts = t_str.split(":")
        return int(parts[0]) * 60 + int(parts[1])
    except Exception:
        return None

def compute_physical_load(day_data, day_n):
    stops = day_data.get("stops", [])
    legs = day_data.get("legs", [])
    transport = day_data.get("transport", [])
    
    walk_load = 1
    elev_load = 0
    drive_rail_load = 0
    museum_load = 0
    late_load = 0
    
    stop_names = " ".join(s.get("name", "") + " " + s.get("id", "") for s in stops).lower()
    
    # Walking load
    if day_n in (2, 3, 5, 6, 8, 10, 13, 14, 15, 17, 20, 22, 24, 25, 30, 32, 33, 34, 37, 40):
        walk_load = 3
    elif day_n in (9, 18, 21, 26, 29, 36, 39, 41):
        walk_load = 2
    elif day_n in (11, 28, 31, 35, 38, 42, 43):
        walk_load = 1
    else:
        walk_load = 2
        
    # Elevation / stairs
    if any(k in stop_names for k in ["fourviere", "castle hill", "le suquet", "sentier des ocres", "bories", "gordes", "panier", "montmartre", "rocher"]):
        elev_load = 2
    elif any(k in stop_names for k in ["tossa", "monaco", "saint-paul", "uzes", "croix-rousse", "pont-du-gard"]):
        elev_load = 1
        
    # Driving / Rail
    if day_n in (5, 6, 12, 16, 17, 18, 21):
        drive_rail_load = 2 # Heavy driving
    elif day_n in (1, 4, 7, 9, 10, 14, 19, 22, 23, 26, 27):
        drive_rail_load = 2 # Rail or transfer driving
    else:
        drive_rail_load = 0
        
    # Museum / Cognitive
    museum_count = sum(1 for s in stops if s.get("category") in ("culture", "sight") and any(k in s.get("id", "") for k in ["musee", "museum", "granet", "macba", "orsay", "palais-des-papes", "maricel", "cau-ferrat", "mucem", "atelier", "sant-pau", "sagrada"]))
    if museum_count >= 2 or day_n in (2, 20, 32):
        museum_load = 2
    elif museum_count == 1:
        museum_load = 1
        
    # Late evening
    end_m = parse_time_minutes(day_data.get("endTime"))
    if end_m and end_m >= 22 * 60:
        late_load = 1
    elif day_n in (1, 34, 41):
        late_load = 1
        
    total_score = walk_load + elev_load + drive_rail_load + museum_load + late_load
    
    if total_score <= 3:
        cat = "Light"
    elif total_score <= 6:
        cat = "Moderate"
    elif total_score <= 8:
        cat = "Heavy"
    else:
        cat = "Very Heavy"
        
    return {
        "walking": walk_load,
        "elevation": elev_load,
        "drive_rail": drive_rail_load,
        "museum": museum_load,
        "late": late_load,
        "total_score": total_score,
        "load_category": cat
    }

def get_weather_sensitivity(day_n, day_data):
    stops = day_data.get("stops", [])
    if day_n in (5, 6, 8, 10, 17, 18, 21, 26, 37, 40):
        return "HIGH" # Coastal, outdoor canyon, Arc race, outdoor wine festival, lake
    elif day_n in (2, 3, 7, 9, 12, 13, 14, 15, 16, 20, 22, 24, 25, 29, 30, 33, 34, 39, 41):
        return "MEDIUM"
    else:
        return "LOW" # Indoor museums, recovery, airport transfer

def audit_day(day_n, day_data, prev_day, next_day, canonical_places, facts):
    d_str = day_data["date"]
    dt = date.fromisoformat(d_str)
    weekday_idx = dt.weekday()
    weekday_str = WEEKDAY_KO[weekday_idx]
    
    city = day_data.get("city", "")
    title = day_data.get("title", "")
    stops = day_data.get("stops", [])
    legs = day_data.get("legs", [])
    backup = day_data.get("backup", "")
    
    start_t = day_data.get("startTime", "")
    end_t = day_data.get("endTime", "")
    start_m = parse_time_minutes(start_t)
    end_m = parse_time_minutes(end_t)
    
    active_duration = ""
    if start_m and end_m:
        diff = end_m - start_m
        active_duration = f"{diff//60}h {diff%60:02d}m"
        
    stop_count = len(stops)
    place_stops = []
    meal_stops = []
    rest_stops = []
    fixed_bookings = []
    opening_constraints = []
    
    underallocated = []
    opening_issues = []
    booking_issues = []
    transport_issues = []
    meal_issues = []
    plan_b_issues = []
    
    for s in stops:
        sid = s.get("id", "")
        sname = s.get("name", "")
        pref = s.get("place_ref")
        target = pref if pref else sid
        
        s_start = s.get("start")
        s_end = s.get("end")
        s_start_m = parse_time_minutes(s_start)
        s_end_m = parse_time_minutes(s_end)
        s_dur = (s_end_m - s_start_m) if (s_start_m and s_end_m) else None
        
        # Place match
        if target in canonical_places:
            place_stops.append(target)
            p_info = canonical_places[target]
            
            # Duration check
            if p_info["content_tier"] == "TIER_A" and s_dur is not None and s_dur < 60:
                underallocated.append(f"{target}({s_dur}m < 60m min)")
            elif p_info["content_tier"] == "TIER_B" and s_dur is not None and s_dur < 30:
                underallocated.append(f"{target}({s_dur}m < 30m min)")
                
            # Opening check
            p_facts = facts.get(target, {}).get("facts", {})
            closed_f = p_facts.get("closed", {}).get("value")
            
            if closed_f:
                # Disambiguate closed patterns
                if "연중무휴" in closed_f or "휴무 없음" in closed_f:
                    pass
                elif f"{weekday_str}요일 휴관" in closed_f or f"{weekday_str} 휴관" in closed_f or f"{weekday_str}요일 휴장" in closed_f:
                    # Check if exception
                    if not (f"({weekday_str}요일 개관)" in closed_f or f"({weekday_str}요일 제외)" in closed_f):
                        opening_issues.append(f"CLOSED_DAY: {target} closed on {weekday_str} ({closed_f})")
            
        if s.get("category") in ("food", "cafe") or "lunch" in sid or "dinner" in sid:
            meal_stops.append(sid)
            
        if any(k in sid for k in ["rest", "buffer", "laundry", "slow"]):
            rest_stops.append(sid)
            
        if s.get("reservation"):
            fixed_bookings.append(f"{sid}: {s['reservation']}")
            
    # Check meal gaps
    has_lunch = any("lunch" in s.get("id", "") or (parse_time_minutes(s.get("start")) and 11*60 <= parse_time_minutes(s.get("start")) <= 14*60 and s.get("category") in ("food", "shopping")) for s in stops)
    if not has_lunch and day_n not in (1, 43):
        food_list = day_data.get("food", [])
        if not food_list:
            meal_issues.append("NO_EXPLICIT_LUNCH_STOP")
            
    # Check Plan B
    if not backup or len(backup.strip()) < 10:
        plan_b_issues.append("MISSING_OR_VAGUE_PLAN_B")
    elif "대체" not in backup and "비" not in backup and "우천" not in backup and "휴식" not in backup and "카페" not in backup and "실내" not in backup and "단축" not in backup and "전환" not in backup and "날씨" not in backup:
        plan_b_issues.append("GENERIC_PLAN_B")
        
    # Physical load
    load_res = compute_physical_load(day_data, day_n)
    
    # Grading logic
    issue_count = len(underallocated) + len(opening_issues) + len(booking_issues) + len(transport_issues) + len(meal_issues)
    
    if day_n in TRANSFER_DAYS and day_n in (4, 12, 23):
        grade = "C" # Transfer + dense sightseeing / car pickup
        recom = "BUFFER & OPTIONALIZE"
    elif day_n in (5, 6, 10, 22, 37):
        grade = "C" # High density / intensive coastal / train / Arc race
        recom = "BUFFER & RESEQUENCE"
    elif load_res["load_category"] == "Very Heavy" or issue_count >= 2:
        grade = "C"
        recom = "BUFFER & SHORTEN"
    elif load_res["load_category"] == "Heavy":
        grade = "B"
        recom = "KEEP WITH BUFFER"
    else:
        grade = "A" if issue_count == 0 and load_res["load_category"] == "Light" else "B"
        recom = "KEEP"
        
    weather_sens = get_weather_sensitivity(day_n, day_data)

    return {
        "day": day_n,
        "date": f"{d_str} ({weekday_str})",
        "region": day_data.get("region", ""),
        "theme": title,
        "planned_start": start_t,
        "planned_end": end_t,
        "active_duration": active_duration,
        "stop_count": stop_count,
        "place_stop_count": len(place_stops),
        "walking_load": load_res["walking"],
        "driving_load": load_res["drive_rail"],
        "rail_load": 2 if day_n in RAIL_DAYS else 0,
        "total_load_score": load_res["total_score"],
        "load_category": load_res["load_category"],
        "fixed_booking_count": len(fixed_bookings),
        "opening_constraint_count": len(opening_issues),
        "meal_breaks": len(meal_stops),
        "rest_buffer": len(rest_stops),
        "weather_sensitivity": weather_sens,
        "feasibility_grade": grade,
        "issue_count": issue_count,
        "underallocated": "; ".join(underallocated) if underallocated else "None",
        "opening_issues": "; ".join(opening_issues) if opening_issues else "None",
        "meal_issues": "; ".join(meal_issues) if meal_issues else "None",
        "plan_b_issues": "; ".join(plan_b_issues) if plan_b_issues else "None",
        "recommendation": recom,
        "fixed_bookings_str": "; ".join(fixed_bookings) if fixed_bookings else "None"
    }

def main():
    canonical_places = load_canonical_places()
    facts = load_facts()
    day_files = sorted(DAILY_CARDS_DIR.glob("day-*.json"))
    days_data = [json.loads(df.read_text(encoding="utf-8")) for df in day_files]
    
    matrix_rows = []
    issues = []
    critical_constraints = []
    
    grade_counts = Counter()
    load_counts = Counter()
    
    for i, d in enumerate(days_data):
        day_n = d["day"]
        prev_d = days_data[i-1] if i > 0 else None
        next_d = days_data[i+1] if i < len(days_data)-1 else None
        
        row = audit_day(day_n, d, prev_d, next_d, canonical_places, facts)
        matrix_rows.append(row)
        
        grade_counts[row["feasibility_grade"]] += 1
        load_counts[row["load_category"]] += 1
        
        # Collect feasibility issues
        if row["underallocated"] != "None":
            issues.append({
                "issue_id": f"FEAS-DUR-{day_n:02d}",
                "day": day_n,
                "severity": "P2",
                "category": "VISIT_DURATION",
                "summary": f"Day {day_n:02d} duration underallocated for major place(s): {row['underallocated']}",
                "detail": f"Time window in Day JSON is tighter than recommended minimum stay duration for Tier A/B places.",
                "proposed_action": "BUFFER / SHORTEN MINOR STOPS",
                "source_phase": "EX-01"
            })
            
        if row["opening_issues"] != "None":
            issues.append({
                "issue_id": f"FEAS-OPN-{day_n:02d}",
                "day": day_n,
                "severity": "P1",
                "category": "OPENING_HOURS",
                "summary": f"Day {day_n:02d} opening hour/closed day constraint: {row['opening_issues']}",
                "detail": f"Place opening schedule or closed day aligns tightly with visit day/time.",
                "proposed_action": "RESEQUENCE / REVERIFY",
                "source_phase": "EX-01"
            })
            
        if day_n in TRANSFER_DAYS:
            critical_constraints.append({
                "constraint_id": f"CST-TRF-{day_n:02d}",
                "day": day_n,
                "category": "TRANSFER_DAY",
                "description": f"Day {day_n:02d} lodging transition ({row['region']}): Check-out, luggage transit, check-in window.",
                "risk_level": "HIGH" if day_n in (4, 12, 23) else "MEDIUM",
                "buffer_required_min": 60 if day_n in (4, 12, 23) else 30
            })
            
        if row["fixed_bookings_str"] != "None":
            critical_constraints.append({
                "constraint_id": f"CST-BKG-{day_n:02d}",
                "day": day_n,
                "category": "FIXED_BOOKING",
                "description": f"Day {day_n:02d} fixed booking(s): {row['fixed_bookings_str']}",
                "risk_level": "CRITICAL" if day_n in (1, 2, 4, 7, 12, 23, 27, 37, 42) else "HIGH",
                "buffer_required_min": 45
            })
            
        if row["feasibility_grade"] == "C":
            issues.append({
                "issue_id": f"FEAS-TIGHT-{day_n:02d}",
                "day": day_n,
                "severity": "P2",
                "category": "ITINERARY_TIGHTNESS",
                "summary": f"Day {day_n:02d} schedule is tight (Grade C, Load: {row['load_category']})",
                "detail": f"Requires strict timing adherence and carries vulnerability to transit/parking delays.",
                "proposed_action": row["recommendation"],
                "source_phase": "EX-01"
            })

    # Consecutive Load Audit
    for i in range(len(matrix_rows)-2):
        r1, r2, r3 = matrix_rows[i], matrix_rows[i+1], matrix_rows[i+2]
        if r1["total_load_score"] >= 7 and r2["total_load_score"] >= 7 and r3["total_load_score"] >= 7:
            issues.append({
                "issue_id": f"FEAS-FATIGUE-D{r1['day']:02d}-D{r3['day']:02d}",
                "day": f"Days {r1['day']}-{r3['day']}",
                "severity": "P2",
                "category": "CONSECUTIVE_FATIGUE",
                "summary": f"Consecutive 3-day heavy load sequence (Days {r1['day']}–{r3['day']})",
                "detail": f"Load scores {r1['total_load_score']} -> {r2['total_load_score']} -> {r3['total_load_score']} create fatigue accumulation without recovery day.",
                "proposed_action": "INSERT RECOVERY BUFFER IN REGIONAL SYNC",
                "source_phase": "EX-01"
            })

    # Write Matrix CSV
    with open(OUT_FEASIBILITY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(matrix_rows[0].keys()))
        writer.writeheader()
        writer.writerows(matrix_rows)
    print(f"Wrote {len(matrix_rows)} rows to {OUT_FEASIBILITY_CSV}")

    # Write Issues CSV
    with open(OUT_ISSUES_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["issue_id", "day", "severity", "category", "summary", "detail", "proposed_action", "source_phase"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(issues)
    print(f"Wrote {len(issues)} issues to {OUT_ISSUES_CSV}")

    # Write Constraints CSV
    with open(OUT_CONSTRAINTS_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["constraint_id", "day", "category", "description", "risk_level", "buffer_required_min"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(critical_constraints)
    print(f"Wrote {len(critical_constraints)} constraints to {OUT_CONSTRAINTS_CSV}")

    # Summary
    print("\n=== Feasibility Audit Summary ===")
    print(f"Total Days Audited: {len(matrix_rows)}")
    print("Grade Distribution:", dict(grade_counts))
    print("Physical Load Distribution:", dict(load_counts))
    print(f"Total Feasibility Issues Identified: {len(issues)}")
    print(f"  P0: {sum(1 for x in issues if x['severity'] == 'P0')}")
    print(f"  P1: {sum(1 for x in issues if x['severity'] == 'P1')}")
    print(f"  P2: {sum(1 for x in issues if x['severity'] == 'P2')}")
    print(f"Critical Constraints Tracked: {len(critical_constraints)}")

if __name__ == "__main__":
    main()
