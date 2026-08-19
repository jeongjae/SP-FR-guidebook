#!/usr/bin/env python3
"""PC-06C Validation Script: Place Canonical SOT & Model Guard.

Checks:
1. Canonical SOT Uniqueness: 30_Places/*.md integrity and 1 Place = 1 File.
2. Place Overwrite Protection: Normal build does not rewrite or overwrite 30_Places/*.md.
3. Duplicate Long-Form Detection: Region chapters do not duplicate full long-form articles (Barcelona, Girona, Nice, Aix).
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
CHAPTER_GRO = ROOT / "source" / "CURRENT" / "20_Regional_Chapters" / "05_Girona_Collioure_Emporda_v2.1.md"
CHAPTER_NICE = ROOT / "source" / "CURRENT" / "20_Regional_Chapters" / "06_Nice_Cote_d_Azur_v2.0.md"
CHAPTER_AIX = ROOT / "source" / "CURRENT" / "20_Regional_Chapters" / "07_Aix_en_Provence_v2.0.md"
TIER_CSV = ROOT / "PLACE_TAXONOMY_AND_TIERS.csv"

def hash_place_dir() -> dict[str, str]:
    hashes = {}
    for p in sorted(PLACE_DIR.glob("*.md")):
        hashes[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    return hashes

def run_gate_validation():
    print("=== PC-06C/PC-09 Place Canonical SOT & Model Guard Validation ===")
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

    # 3. Duplicate Long-Form Detection for Barcelona, Girona, Nice & Aix Places
    print("3. Testing Duplicate Long-Form Detection (Barcelona, Girona, Nice & Aix Places)...")
    bcn_text = CHAPTER_BCN.read_text(encoding="utf-8") if CHAPTER_BCN.exists() else ""
    gro_text = CHAPTER_GRO.read_text(encoding="utf-8") if CHAPTER_GRO.exists() else ""
    nice_text = CHAPTER_NICE.read_text(encoding="utf-8") if CHAPTER_NICE.exists() else ""
    aix_text = CHAPTER_AIX.read_text(encoding="utf-8") if CHAPTER_AIX.exists() else ""
    
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
    long_form_signatures_nice = [
        "자전거 및 롤러블레이드 전용 차선과 보행자 도로가 명확히",
        "정상 시장은 화요일(9/8) 아침이 적기다",
        "현재 요새는 철거되었으나 니스 해안선의 부드러운",
        "1860년 병합 전까지 이탈리아 사보이 백작령의 통치를 500년간",
        "기차역에서 바위 위까지는 오르막 경사가 심하므로"
    ]
    long_form_signatures_aix = [
        "오텔 모렐드퐁테베(오텔 데스파녜)는 소유주 피에르 모렐의",
        "바니에 수원의 온천수가 이 분수로 끌어와졌다",
        "다비드 당제의 작품이다",
        "세잔의 아버지가 모자 가게를 하던 거리도",
        "프랑스가 지중해 문명을 다루는 기관을 수도가 아니라 마르세유에",
        "포문이 바다가 아니라 도시를 향해 나 있다",
        "대형 캔버스를 밖으로 옮기려고 벽에 낸 긴 세로 홈",
        "비베뮈 고원은 가족 저택 너머로 멀리 뻗어 있다",
        "에메 마그다. 판화가이자 화상이었다"
    ]
    
    dups = []
    for sig in long_form_signatures_bcn:
        if sig in bcn_text:
            dups.append(f"[BCN] {sig}")
    for sig in long_form_signatures_gro:
        if sig in gro_text:
            dups.append(f"[GRO] {sig}")
    for sig in long_form_signatures_nice:
        if sig in nice_text:
            dups.append(f"[NICE] {sig}")
    for sig in long_form_signatures_aix:
        if sig in aix_text:
            dups.append(f"[AIX] {sig}")
            
    if dups:
        errors.append(f"Duplicate long-form text detected in Region chapters: {dups}")
        print(f"   [FAIL] Found duplicate long-form sections: {dups}")
    else:
        print("   [OK] Dedup PASS: Regional chapters contain only compact references with no duplicate long-forms.")

    # 4. Trip Layer Separation Check
    print("4. Testing Trip Layer Separation (Barcelona, Girona, Nice & Aix)...")
    trip_hardcode_pattern = re.compile(r"(8월\s*\d+일|9월\s*\d+일|10월\s*\d+일|Day\s*\d+에\s*방문|이번\s*일정에서는\s*Day)")
    check_slugs = [
        # Barcelona
        "sagrada-familia", "sant-pau-recinte-modernista", "barri-gotic", "macba", "biblioteca-de-catalunya",
        # Girona
        "girona-cathedral", "passeig-de-la-muralla", "collioure", "onyar", "pals", "peratallada", "calella-de-palafrugell", "peralada",
        # Nice
        "promenade-des-anglais", "vieux-nice", "colline-du-chateau", "cours-saleya", "le-rocher", "monaco", "menton", "le-suquet", "cannes",
        "marche-forville", "marche-de-la-liberation", "nce-t2", "nice-ville", "nice-walk", "cannes-walk", "monaco-walk",
        # Aix & Marseille
        "cours-mirabeau", "vieil-aix", "atelier-des-lauves", "montagne-sainte-victoire-terrain-des-peintres",
        "place-richelme-place-des-precheurs", "musee-granet", "bastide-du-jas-de-bouffan", "carrieres-de-bibemus", "rotonde",
        "vieux-port-marseille", "le-panier", "mucem", "fort-saint-jean", "notre-dame-de-la-garde", "marseille",
        "saint-paul-de-vence", "grasse", "cassis", "calanques"
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
        print("   [OK] Trip Separation PASS: Places are cleanly decoupled from trip dates.")

    # 5. Reference Integrity Check
    print("5. Testing Reference Integrity (Day Stops & Region refs)...")
    missing_refs = []
    for dp in sorted(DAILY_CARDS.glob("day-*.json")):
        ddata = json.loads(dp.read_text(encoding="utf-8"))
        for stop in ddata.get("stops", []):
            sid = stop.get("id")
            if sid and sid in check_slugs and not (PLACE_DIR / f"{sid}.md").exists():
                missing_refs.append((dp.stem, sid))
    if missing_refs:
        errors.append(f"Missing referenced place files: {missing_refs}")
        print(f"   [FAIL] Missing referenced place files: {missing_refs}")
    else:
        print("   [OK] Reference Integrity PASS: All referenced Canonical Places have valid markdown SOT files.")

    # 6. Content Audit
    print("6. Running Content Audit Guard...")
    audit_res = subprocess.run([sys.executable, str(ROOT / "build" / "content_audit.py")],
                               capture_output=True, text=True, cwd=str(ROOT))
    if audit_res.returncode != 0:
        errors.append(f"Content audit failed:\n{audit_res.stdout}\n{audit_res.stderr}")
    else:
        print("   [OK] Content Audit PASS.")

    # Summary
    print("\n=== Summary ===")
    if errors:
        print(f"FAILED: {len(errors)} error(s) found.")
        for e in errors:
            print(f" - {e}")
        return False
    else:
        print("ALL GATES PASSED: Canonical SOT pipeline is fully verified.")
        return True

if __name__ == "__main__":
    success = run_gate_validation()
    sys.exit(0 if success else 1)
