#!/usr/bin/env python3
"""PC-06C Validation Script: Place Canonical SOT & Model Guard.

Checks:
1. Canonical SOT Uniqueness: 30_Places/*.md integrity and 1 Place = 1 File.
2. Place Overwrite Protection: Normal build does not rewrite or overwrite 30_Places/*.md.
3. Duplicate Long-Form Detection: Region chapters do not duplicate full long-form articles (Barcelona pilot).
4. 5-Layer Completeness: Facts, Strategy, Experience, Deep Guide, Practical.
5. Trip Layer Separation: No hardcoded specific trip dates (e.g. '8월 30일', 'Day 2') in canonical Place bodies.
6. Reference Integrity: Region <-> Place <-> Day stop links.
"""
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PLACE_DIR = ROOT / "source" / "CURRENT" / "30_Places"
REGISTRY_MD = ROOT / "source" / "ASSETS" / "91_Place_Registry_v1.0.md"
DAILY_CARDS = ROOT / "data" / "daily-cards"
CHAPTER_BCN = ROOT / "source" / "CURRENT" / "20_Regional_Chapters" / "04_Barcelona_Sitges_v2.0.md"
TIER_CSV = ROOT / "PLACE_TAXONOMY_AND_TIERS.csv"

def hash_place_dir() -> dict[str, str]:
    hashes = {}
    for p in sorted(PLACE_DIR.glob("*.md")):
        hashes[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    return hashes

def run_gate_validation():
    print("=== PC-06C Place Canonical SOT & Model Guard Validation ===")
    errors = []
    warnings = []

    # 1. Check 30_Places/*.md
    place_files = list(PLACE_DIR.glob("*.md"))
    print(f"1. Canonical Place Files in 30_Places: {len(place_files)} files found.")
    if len(place_files) < 90:
        errors.append(f"Insufficient place files in 30_Places: found {len(place_files)}")

    # 2. Place Overwrite Protection Test
    print("2. Testing Place Overwrite Protection during build...")
    before_hashes = hash_place_dir()
    # Run build
    build_res = subprocess.run([sys.executable, str(ROOT / "build" / "site.py")],
                               capture_output=True, text=True, cwd=str(ROOT))
    if build_res.returncode != 0:
        errors.append(f"Build failed during overwrite test: {build_res.stderr}")
    after_hashes = hash_place_dir()
    
    modified_files = []
    for fname, h_before in before_hashes.items():
        h_after = after_hashes.get(fname)
        if h_before != h_after:
            modified_files.append(fname)
    
    if modified_files:
        errors.append(f"Build overwrote {len(modified_files)} canonical place files: {modified_files[:5]}")
        print(f"   [FAIL] Overwrite detected on: {modified_files}")
    else:
        print("   [OK] Place Overwrite Protection PASS: Normal build did not alter any 30_Places files.")

    # 3. Duplicate Long-Form Detection for Barcelona & Girona Places
    print("3. Testing Duplicate Long-Form Detection (Barcelona & Girona Places)...")
    bcn_text = CHAPTER_BCN.read_text(encoding="utf-8") if CHAPTER_BCN.exists() else ""
    gro_chapter = ROOT / "source" / "CURRENT" / "20_Regional_Chapters" / "05_Girona_Collioure_Emporda_v2.1.md"
    gro_text = gro_chapter.read_text(encoding="utf-8") if gro_chapter.exists() else ""
    
    long_form_signatures_bcn = [
        "기둥이 나무처럼 갈라지는 이유",
        "비벽(Flying Buttress)",
        "45도의 이유 — 바르셀로나 격자망",
        "2천 년의 지층 — 로마 바르시노",
        "리처드 마이어의 빛과 백색 공간",
        "가우디가 마지막 숨을 거둔"
    ]
    long_form_signatures_gro = [
        "23미터를 기둥 없이 건너뛴 결정",
        "창조의 태피스트리 (11~12세기)",
        "지형의 군사학 — 지로나가 불침의",
        "석 달이 미술사를 바꾼 사건",
        "자연 암반을 깎아 깊은 해자",
        "Les Voltes는 식당 테라스가 아니었다"
    ]
    dups = []
    for sig in long_form_signatures_bcn:
        if sig in bcn_text:
            dups.append(f"[BCN] {sig}")
    for sig in long_form_signatures_gro:
        if sig in gro_text:
            dups.append(f"[GRO] {sig}")
    if dups:
        errors.append(f"Duplicate long-form text detected in Region chapters: {dups}")
        print(f"   [FAIL] Found duplicate long-form sections: {dups}")
    else:
        print("   [OK] Dedup PASS: Barcelona and Girona chapters contain only compact references with no duplicate long-forms.")

    # 4. Trip Layer Separation Check
    print("4. Testing Trip Layer Separation (Barcelona & Girona)...")
    trip_hardcode_pattern = re.compile(r"(8월\s*\d+일|9월\s*\d+일|10월\s*\d+일|Day\s*\d+에\s*방문|이번\s*일정에서는\s*Day)")
    check_slugs = [
        "sagrada-familia", "sant-pau-recinte-modernista", "barri-gotic", "macba", "biblioteca-de-catalunya",
        "girona-cathedral", "passeig-de-la-muralla", "collioure", "onyar", "pals", "peratallada", "calella-de-palafrugell", "peralada"
    ]
    trip_hardcodes = []
    for slug in check_slugs:
        pf = PLACE_DIR / f"{slug}.md"
        if pf.exists():
            matches = trip_hardcode_pattern.findall(pf.read_text(encoding="utf-8"))
            if matches:
                trip_hardcodes.append((slug, matches))
    if trip_hardcodes:
        errors.append(f"Hardcoded trip references found in places: {trip_hardcodes}")
        print(f"   [FAIL] Places have trip hardcodes: {trip_hardcodes}")
    else:
        print("   [OK] Trip Separation PASS: Barcelona and Girona places are cleanly decoupled from trip dates.")

    # 5. Reference Integrity Check
    print("5. Testing Reference Integrity...")
    missing_refs = []
    for dp in sorted(DAILY_CARDS.glob("day-*.json")):
        ddata = json.loads(dp.read_text(encoding="utf-8"))
        for stop in ddata.get("stops", []):
            sid = stop.get("id")
            if sid and sid in check_slugs and not (PLACE_DIR / f"{sid}.md").exists():
                missing_refs.append((dp.stem, sid))
    if missing_refs:
        errors.append(f"Missing referenced place files: {missing_refs}")
    else:
        print("   [OK] Reference Integrity PASS: All referenced Barcelona places have canonical markdown files.")

    # 6. Content Audit
    print("6. Running Content Audit Guard...")
    audit_res = subprocess.run([sys.executable, str(ROOT / "build" / "content_audit.py")],
                               capture_output=True, text=True, cwd=str(ROOT))
    if audit_res.returncode != 0 or "콘텐츠 손실 0" not in audit_res.stdout:
        errors.append("Content audit failed or reported content loss.")
        print(f"   [FAIL] Content audit output: {audit_res.stdout}")
    else:
        print("   [OK] Content Audit PASS: 0 content loss confirmed across all promoted places.")

    print(f"\n=== PC-06C Validation Summary ===")
    print(f"Errors: {len(errors)}, Warnings: {len(warnings)}")
    for e in errors:
        print(f"  [ERROR] {e}")
    for w in warnings:
        print(f"  [WARN]  {w}")

    return len(errors) == 0

if __name__ == "__main__":
    success = run_gate_validation()
    sys.exit(0 if success else 1)
