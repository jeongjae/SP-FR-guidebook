#!/usr/bin/env python3
"""콘텐츠 스키마 가드 — 원고가 편집 표준을 지키는가.

챕터 h2 구성과 순서, 장소 명부 ↔ dossier 대조, walk 필수 필드, 공식 출처.
build/content_schema.json 이 규칙의 정본이고 여기서는 집행만 한다.

부정 픽스처(build/test_validation.py)가 이 가드를 겨눈다 — 일부러 망가뜨린
원고를 넣었을 때 잡아내는지 본다. 못 잡는 가드는 없는 것과 같다.

2026-08-18 개편에서 build.py 를 은퇴시키며 들어냈다. 배포 산출물을 보는
부분만 새 IA(지역 · 장소 · 데일리 페이지)로 옮겼고 규칙은 그대로다.

    python3 build/content_guard.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source"
SITE = Path(os.environ.get("SPFR_SITE_DIR") or (ROOT / "site"))
CORE = "CURRENT/10_Core"
REGIONAL = "CURRENT/20_Regional_Chapters"
COMMERCIAL_CARDS = SOURCE / "ASSETS" / "89_Commercial_City_Experience_Cards_v1.0.md"
PLACE_DOSSIERS = SOURCE / "ASSETS" / "90_Regional_Context_and_Place_Dossier_Compendium_v1.0.md"
COMMERCIAL_STANDARD = SOURCE / "CURRENT" / "00_Governance" / "89_Commercial_Guidebook_Editorial_and_Layout_Standard_v1.0.md"
DOSSIER_STANDARD = SOURCE / "CURRENT" / "00_Governance" / "90_Regional_and_Place_Dossier_Editorial_Standard_v1.0.md"

CHAPTER_FILES = {
    "barcelona": "04_Barcelona_Sitges_v2.0.md",
    "girona": "05_Girona_Collioure_Emporda_v2.1.md",
    "nice": "06_Nice_Cote_d_Azur_v2.0.md",
    "verdon": "06B_Verdon_Moustiers_v1.0.md",
    "aix": "07_Aix_en_Provence_v2.0.md",
    "luberon": "08_Luberon_Farmhouse_v2.0.md",
    "avignon": "09_Avignon_Alpilles_Pont_du_Gard_v2.0.md",
    "lyon": "10_Lyon_v2.0.md",
    "paris": "11_Paris_Long_Stay_v2.0.md",
}
CHAPTERS = [{"kind": "region", "slug": s, "name": s, "path": f"{REGIONAL}/{f}"}
            for s, f in CHAPTER_FILES.items()]

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model import load_registry as _registry_rows  # noqa: E402


def load_place_registry():
    """model 의 명부 로더를 이 가드가 쓰던 형태로 맞춘다."""
    return [{"slug": r["slug"], "name": r["name"], "chapter": r["region"],
             "type": r["kind"], "grade": r["grade"], "grade_raw": r["grade_label"],
             "pin": r["pin"], "wiki": r["wiki"]} for r in _registry_rows()]


EMBEDDED_FM_RE = re.compile(
    r"^---[ \t]*\n((?:[A-Za-z_][A-Za-z0-9_-]*:[^\n]*\n)+)---[ \t]*\n", re.M)


def _read_fm(chunk, meta):
    for line in chunk.strip().splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip('"')


def parse_frontmatter(text):
    """단순 YAML frontmatter를 dict로 파싱하고 본문을 돌려준다.

    파일 머리의 블록과, 본문 중간에 남은 블록 하나를 모두 걷어낸다.
    """
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            _read_fm(text[3:end], meta)
            text = text[end + 4:]
    m = EMBEDDED_FM_RE.search(text)
    if m:
        _read_fm(m.group(1), meta)
        text = text[:m.start()] + text[m.end():]
    return meta, text.lstrip("\n")


def check_phase9_commercial_depth_guards():
    """상용 편집모듈과 장소 dossier가 원고·배포본에서 빠지지 않게 잠근다.
    하드코딩 매직 넘버와 지역별 분기를 제거하고 content_schema.json 데이터 기반으로 유연하게 검증한다.
    """
    import json
    problems = []
    
    schema_path = SOURCE.parent / "build" / "content_schema.json"
    if not schema_path.exists():
        problems.append("콘텐츠 검증 스키마 파일(build/content_schema.json) 누락")
        print("Phase 9 상용편집·장소심화 가드 실패:")
        print("  build/content_schema.json 파일이 없습니다.")
        sys.exit(1)
        
    try:
        schema_data = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as e:
        problems.append(f"콘텐츠 검증 스키마 파일 파싱 실패: {e}")
        print("Phase 9 상용편집·장소심화 가드 실패:")
        print(f"  build/content_schema.json 파싱 중 예외 발생: {e}")
        sys.exit(1)
        
    schemas = schema_data["schemas"]
    dossier_mapping = schema_data["dossier_mapping"]
    
    required_files = (COMMERCIAL_CARDS, PLACE_DOSSIERS, COMMERCIAL_STANDARD, DOSSIER_STANDARD)
    for path in required_files:
        if not path.exists() or path.stat().st_size < 500:
            problems.append(f"Phase 9 기준파일 누락·손상: {path.relative_to(SOURCE)}")

    cards_text = COMMERCIAL_CARDS.read_text(encoding="utf-8")
    dossier_text = PLACE_DOSSIERS.read_text(encoding="utf-8")
    
    if len(re.findall(r"^## .+$", cards_text, re.M)) != 9:  # RS01: verdon 추가로 8→9
        problems.append("Commercial City Experience Card는 정확히 9개 지역이어야 함")
        
    registry = load_place_registry()
    registry_spots = {r["slug"]: r for r in registry if r["type"] in ("spot", "walk")}
    
    actual_headings = [m.group(1).strip() for m in re.finditer(r"^## (.+)$", dossier_text, re.M)]
    actual_headings_set = set(actual_headings)
    
    duplicates = [h for h in actual_headings_set if actual_headings.count(h) > 1]
    for h in duplicates:
        problems.append(f"Dossier 중복 헤딩 발견: {h}")
        
    expected_headings_set = set()
    for slug, mapping in dossier_mapping.items():
        heading = mapping["heading"]
        if slug not in registry_spots:
            problems.append(f"dossier_mapping에 정의된 슬러그 '{slug}'가 레지스트리에 존재하지 않음")
            continue
        expected_headings_set.add(heading)
        if heading not in actual_headings_set:
            problems.append(f"레지스트리에 대응되는 dossier 누락 발견 (ID: {slug}, 헤딩: {heading})")
            
    for heading in actual_headings_set:
        if heading not in expected_headings_set:
            problems.append(f"레지스트리 매핑이 없는 orphan dossier 발견: {heading}")
            
    dossiers_content = {}
    for m in re.finditer(r"^## (.+)$", dossier_text, re.M):
        name = m.group(1).strip()
        seg = dossier_text[m.end():]
        nxt = seg.find("\n## ")
        if nxt == -1:
            nxt = seg.find("\n# ")
        seg = seg[:nxt] if nxt != -1 else seg
        dossiers_content[name] = seg

    heading_to_slugs = {}
    for slug, mapping in dossier_mapping.items():
        heading_to_slugs.setdefault(mapping["heading"], []).append(slug)
        
    for name, content in dossiers_content.items():
        slugs = heading_to_slugs.get(name, [])
        if not slugs:
            continue
        slug = slugs[0]
        r = registry_spots.get(slug)
        if not r:
            continue
            
        fields = {}
        for line in content.splitlines():
            if line.strip().startswith("- "):
                key, value = line.split(":", 1) if ":" in line else (line, "")
                fields[key.strip("- ").strip()] = value.strip()
                
        if r["type"] == "walk":
            if "공식정보" not in fields or not fields["공식정보"].startswith("http"):
                problems.append(f"Dossier {name} ({slug}): 필수 필드 누락 — 공식정보")
        else:
            required_spot_fields = ["방문", "관람", "체류", "주의", "공식정보"]
            for field in required_spot_fields:
                if field not in fields or not fields[field]:
                    problems.append(f"Dossier {name} ({slug}): 필수 필드 누락 — {field}")
            has_fee = any(x in fields for x in ["요금·예약", "요금", "예약"])
            if not has_fee:
                problems.append(f"Dossier {name} ({slug}): 필수 필드 누락 — 요금·예약")
                
    chapter_expected_unique_headings = {}
    for slug, mapping in dossier_mapping.items():
        r = registry_spots.get(slug)
        if r:
            region = mapping["region"]
            chapter_expected_unique_headings.setdefault(region, set())
            chapter_expected_unique_headings[region].add(mapping["heading"])
    chapter_expected_unique_headings = {k: len(v) for k, v in chapter_expected_unique_headings.items()}

    region_name_map = {
        "barcelona": "Barcelona", "girona": "Girona", "nice": "Nice", "verdon": "Verdon", "aix": "Aix",
        "luberon": "Luberon", "avignon": "Avignon", "lyon": "Lyon", "paris": "Paris"
    }

    for chapter in (c for c in CHAPTERS if c["kind"] == "region"):
        slug = chapter["name"]
        region_heading = region_name_map[slug]
        source_path = SOURCE / chapter["path"]
        source_text = source_path.read_text(encoding="utf-8")
        
        meta, body_md = parse_frontmatter(source_text)
        schema_name = meta.get("content_schema")
        
        if schema_name is None:
            schema_name = "legacy-region-v1"
            
        if schema_name not in schemas:
            problems.append(f"{source_path.name}: 알 수 없는 content_schema 값 — {schema_name}")
            continue
            
        schema = schemas[schema_name]
        
        for module in schema["required_modules"]:
            if not re.search(rf"^#\s+{re.escape(module)}\s*$", source_text, re.M):
                problems.append(f"{source_path.name}: 필수 모듈 누락 — {module}")
                
        h2_headings_in_file = [m.group(1).strip() for m in re.finditer(r"^## (.+)$", source_text, re.M)]
        h2_headings_set = set(h2_headings_in_file)
        
        for h2 in schema["required_h2"]:
            if h2 == "Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계" and "Editor’s Verdict" in h2_headings_set and schema_name == "legacy-region-v1":
                continue
            if h2 not in h2_headings_set:
                problems.append(f"{source_path.name}: 필수 헤딩 누락 — {h2}")
                
        if schema["strict_order"]:
            positions = [source_text.find(f"## {h2}") for h2 in schema["required_h2"]]
            valid_positions = [pos for pos in positions if pos != -1]
            if valid_positions != sorted(valid_positions):
                problems.append(f"{source_path.name}: 헤딩 순서 오류 (H2 순서가 올바르지 않음)")
                
        if not schema["allow_duplicates"]:
            dups = [h for h in h2_headings_set if h2_headings_in_file.count(h) > 1]
            for h in dups:
                problems.append(f"{source_path.name}: 중복 헤딩 발견 — {h}")
                
        if schema_name == "legacy-region-v1":
            if not re.search(r"^## (?:지역을 이해하는 다섯 개의 층|이 (?:도시를|지역을) 이해하는 축)",
                             source_text, re.M):
                problems.append(f"{source_path.name}: 역사·경제·사회·문화 지역맥락 축 누락")
                
        region_match = re.search(
            rf"^# {re.escape(region_heading)}\s*$([\s\S]*?)(?=^# [^#]|\Z)",
            dossier_text, re.M)
        actual_places = len(re.findall(r"^## .+$", region_match.group(1), re.M)) if region_match else 0
        expected_places = chapter_expected_unique_headings.get(slug, 0)
        if actual_places != expected_places:
            problems.append(f"{region_heading}: dossier {actual_places}개 (기대 {expected_places}개)")

        # 배포 산출물. 새 IA 에서 한 지역의 콘텐츠는 지역 페이지와 장소·
        # 데일리 페이지에 나뉘어 있다 — 챕터 10개 카테고리 페이지가 아니다.
        deployed_paths = [SITE / "guide" / f"{slug}.html"]
        deployed_paths += sorted((SITE / "places").glob("*.html"))
        deployed_paths += sorted((SITE / "daily").glob("*.html"))
        deployed_chunks = []
        for p in deployed_paths:
            try:
                deployed_chunks.append(p.read_text(encoding="utf-8"))
            except OSError:
                pass
        deployed = "\n".join(deployed_chunks)
            
        for token in schema["required_deployed_tokens"]:
            if token not in deployed:
                problems.append(f"{slug} 배포 챕터: Restructured 콘텐츠 누락 — {token}")
                
        for token in schema["required_deployed_context_tokens"]:
            if not any(t in deployed for t in schema["required_deployed_context_tokens"]):
                problems.append(f"{slug} 배포 챕터: 역사·경제·사회·문화 지역맥락 축 누락")
                break

    if problems:
        print("Phase 9 상용편집·장소심화 가드 실패:")
        for problem in problems[:40]:
            print("  " + problem)
        sys.exit(1)
    print("Phase 9 상용편집·장소심화 가드: 스키마 및 레지스트리-Dossier 검증 이상 없음")


if __name__ == "__main__":
    check_phase9_commercial_depth_guards()
    print("콘텐츠 스키마 가드 통과")
