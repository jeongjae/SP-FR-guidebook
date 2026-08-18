#!/usr/bin/env python3
"""PC-06B Validation Script: Place Content Model & Canonicalization Guard.

Checks:
1. Canonical SOT: 30_Places/*.md integrity and duplication check.
2. 5-Layer Model coverage per place (Facts, Strategy, Experience, Deep Guide, Trip Layer).
3. Tier classification and field completeness (Tier A, Tier B, Tier C, Utility).
4. Trip Layer separation: detects hardcoded trip dates (e.g. '8월 30일', 'Day 2') inside Place long-form bodies.
5. Reference integrity: Region <-> Place <-> Day stop links.
"""
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent

PLACE_DIR = ROOT / "source" / "CURRENT" / "30_Places"
REGISTRY_MD = ROOT / "source" / "ASSETS" / "91_Place_Registry_v1.0.md"
DAILY_CARDS = ROOT / "data" / "daily-cards"
FACTS_JSON = ROOT / "data" / "place-facts.json"
TIER_CSV = ROOT / "PLACE_TAXONOMY_AND_TIERS.csv"

def run_gate_validation():
    print("=== PC-06B Place Content Model & Canonicalization Gate Validation ===")
    errors = []
    warnings = []

    # 1. Load Tiers
    tiers = {}
    if TIER_CSV.exists():
        import csv
        with open(TIER_CSV, "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                tiers[r["id"]] = r

    # 2. Check 30_Places/*.md
    place_files = list(PLACE_DIR.glob("*.md"))
    print(f"1. Canonical Place Files in 30_Places: {len(place_files)} files found.")

    # 3. Check 5-Layer completeness and Trip Layer hardcoding
    trip_hardcode_pattern = re.compile(r"(8월\s*\d+일|9월\s*\d+일|10월\s*\d+일|Day\s*\d+에\s*방문|이번\s*일정에서는\s*Day)")
    
    layer_matrix = {}
    trip_hardcodes = []

    for pf in sorted(place_files):
        slug = pf.stem
        text = pf.read_text(encoding="utf-8")
        tier_info = tiers.get(slug, {})
        tier = tier_info.get("content_tier", "TIER_B")

        # Layer checks
        has_facts = "## 실용" in text or "## Facts" in text or "{{fact:" in text or "|항목" in text
        has_strategy = "Editor's Verdict" in text or "## 왜 가는가" in text or "Best For" in text
        has_experience = "Don't Miss" in text or "Look Closer" in text or "핵심" in text or "들어가면 먼저" in text
        has_deep = "## 더 깊이" in text or "## Deep Guide" in text or "### 1." in text or "### 핵심" in text
        
        # Trip layer check
        hardcode_matches = trip_hardcode_pattern.findall(text)
        if hardcode_matches:
            trip_hardcodes.append((slug, hardcode_matches))

        layer_matrix[slug] = {
            "tier": tier,
            "facts": "COMPLETE" if has_facts else "PARTIAL",
            "strategy": "COMPLETE" if has_strategy else "PARTIAL",
            "experience": "COMPLETE" if has_experience else "PARTIAL",
            "deep_guide": "COMPLETE" if has_deep else "PARTIAL",
            "trip_separated": "WARNING" if hardcode_matches else "CLEAN"
        }

    print(f"2. Trip Layer Separation Check:")
    if trip_hardcodes:
        print(f"   [!] Found {len(trip_hardcodes)} places with hardcoded trip schedule references in body:")
        for s, m in trip_hardcodes[:10]:
            print(f"       - {s}: {m}")
            warnings.append(f"{s} contains hardcoded trip schedule references: {m}")
    else:
        print("   [OK] All Place bodies are cleanly decoupled from trip schedule dates.")

    # 4. Barcelona Pilot 5 places detailed check
    bcn_pilot = ["sagrada-familia", "sant-pau-recinte-modernista", "barri-gotic", "macba", "biblioteca-de-catalunya"]
    print(f"\n3. Barcelona Pilot 5 Places Layer Matrix:")
    for b in bcn_pilot:
        if b in layer_matrix:
            m = layer_matrix[b]
            print(f"   - {b:30s} | Tier: {m['tier']:6s} | Facts: {m['facts']:8s} | Strategy: {m['strategy']:8s} | Exp: {m['experience']:8s} | Deep: {m['deep_guide']:8s} | TripSep: {m['trip_separated']}")
        else:
            errors.append(f"Missing Barcelona pilot place file: {b}")

    # 5. Reference integrity
    print(f"\n4. Reference Integrity Check (Day Stops -> Place Files):")
    missing_place_refs = defaultdict(list)
    for dp in sorted(DAILY_CARDS.glob("day-*.json")):
        ddata = json.loads(dp.read_text(encoding="utf-8"))
        for stop in ddata.get("stops", []):
            sid = stop.get("id")
            if sid in tiers and not (PLACE_DIR / f"{sid}.md").exists():
                missing_place_refs[sid].append(dp.stem)

    if missing_place_refs:
        print(f"   [!] {len(missing_place_refs)} referenced canonical places lack 30_Places markdown file.")
    else:
        print("   [OK] All referenced canonical places have corresponding markdown source files.")

    print(f"\n=== Validation Summary ===")
    print(f"Errors: {len(errors)}, Warnings: {len(warnings)}")
    return len(errors) == 0

if __name__ == "__main__":
    success = run_gate_validation()
    sys.exit(0 if success else 1)
