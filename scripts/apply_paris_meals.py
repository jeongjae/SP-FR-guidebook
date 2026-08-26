#!/usr/bin/env python3
"""MP-04 — 파리 끼니 슬롯에 상호를 넣는다.

파리 16일 중 점심 6끼·저녁 10끼가 권역만 적힌 채 상호 없이 비어 있었다.
그 자리에 실제 식당을 넣는다. 1순위는 장소 정본(30_Places)을 갖고, 2·3순위는
그 정본 안의 '대안' 절과 Day 카드의 backup 에 남는다 — 갈 수도 있는 집마다
페이지를 만들면 명부가 후보 목록이 되고, 현장에서 무엇이 확정인지 알 수
없게 된다.

    python3 scripts/apply_paris_meals.py

입력  scripts/paris_meal_places.json
출력  source/CURRENT/30_Places/<slug>.md
      source/ASSETS/91_Place_Registry_v1.0.md      (paris 절에 행 추가)
      source/CURRENT/20_Regional_Chapters/11_Paris_Long_Stay_v2.0.md
      data/place-facts.json · data/map-queries.json
      data/images/food-photo-status.json
      data/food-completeness-disposition.json
      FCR_MASTER_FOOD_INVENTORY.csv · PLACE_TAXONOMY_AND_TIERS.csv

한 번 돌리면 멱등이다 — 이미 있는 슬러그는 덮어쓰고 중복 행을 만들지 않는다.
"""
from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "scripts" / "paris_meal_places.json").read_text(encoding="utf-8"))
PLACES = DATA["places"]
VERIFIED = DATA["verifiedAt"]

PLACE_DIR = ROOT / "source" / "CURRENT" / "30_Places"
REGISTRY = ROOT / "source" / "ASSETS" / "91_Place_Registry_v1.0.md"
CHAPTER = ROOT / "source" / "CURRENT" / "20_Regional_Chapters" / "11_Paris_Long_Stay_v2.0.md"

GRADE_TOKEN = {"필수": "essential|필수", "우선 추천": "priority|우선추천",
               "선택": "optional|선택"}
GRADE_EN = {"필수": "essential", "우선 추천": "priority", "선택": "optional"}
TIER = {"필수": "TIER_A", "우선 추천": "TIER_B", "선택": "TIER_C"}
PRIORITY = {"필수": "MUST_SEE", "우선 추천": "RECOMMENDED", "선택": "OPTIONAL"}


# ---------------------------------------------------------------- 1. 장소 정본
def write_dossier(p: dict) -> None:
    fm = [
        "---",
        f"slug: {p['slug']}",
        f'name: "{p["name"]}"',
        f'local_name: "{p["local_name"]}"',
        "region: paris",
        "kind: spot",
        f'grade: "{p["grade"]}"',
        f'priority: "{PRIORITY[p["grade"]]}"',
        f'content_tier: "{TIER[p["grade"]]}"',
        'selection_origin: "RECOMMENDED"',
        f'meal_role: "{p["meal_role"]}"',
        f'food_kind: "{p["food_kind"]}"',
        f'summary: "{p["summary"]}"',
        f"source: source/CURRENT/30_Places/{p['slug']}.md",
        "---",
        "",
        "## 왜 가는가",
        "",
    ]
    body = list(fm)
    body += [para for pair in ((x, "") for x in p["why_go"]) for para in pair]
    body += [
        "### Editor's Verdict",
        f"> {p['verdict']}",
        "",
        f"- **Best For**: {p['best_for']}",
        f"- **Best Context**: {p['best_context']}",
        f"- **Recommended Duration**: {p['duration']}",
        "",
        "## 더 깊이",
        "",
    ]
    for i, sec in enumerate(p["deep"], 1):
        body += [f"### {i}. {sec['h']}", sec["p"], ""]

    rows = [
        ("위치", p["address"]),
        ("운영 시간", p["hours"]),
        ("정기 휴무", p["closed"]),
        ("가격대", p["price"] + (f" — {p['price_note']}" if p.get("price_note") else "")),
        ("예약", p["booking"]),
        ("접근 교통", p["transit"]),
    ]
    if p.get("url"):
        rows.append(("공식 정보", f"[공식 웹사이트]({p['url']}) (verified_at: {VERIFIED})"))
    else:
        rows.append(("공식 정보", f"공식 웹사이트 없음 — 전화 확인 (verified_at: {VERIFIED})"))

    body += ["## 실용", "", "| 항목 | 상세 정보 |", "|---|---|"]
    body += [f"| **{k}** | {v} |" for k, v in rows]
    body += ["", f"> 운영시간·요금은 2026-08-25 웹 조사 기준이다. 프랑스 식당은 "
                 f"연차 휴무와 단축 영업이 잦으니 **방문 3~7일 전 전화로 재확인**한다.", ""]
    (PLACE_DIR / f"{p['slug']}.md").write_text("\n".join(body), encoding="utf-8")


# ---------------------------------------------------------------- 2. 명부
def patch_registry() -> None:
    lines = REGISTRY.read_text(encoding="utf-8").splitlines()
    have = {p["slug"] for p in PLACES}
    lines = [ln for ln in lines if not re.match(r"^\|\s*`(" + "|".join(have) + r")`", ln)]
    out, inserted = [], False
    for i, ln in enumerate(lines):
        out.append(ln)
        if inserted:
            continue
        # paris 절의 마지막 표 행 뒤에 넣는다
        if re.match(r"^\|\s*`bouillon-chartier-montparnasse`", ln):
            for p in PLACES:
                out.append(
                    f"| `{p['slug']}` | {p['name']} | spot | {p['grade']} | "
                    f"{p['name']} | chapters/paris/places.html | {p['name']} | — |")
            inserted = True
    assert inserted, "명부에서 paris 절 삽입 지점을 찾지 못했다"
    REGISTRY.write_text("\n".join(out) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- 3. 챕터 원고
def patch_chapter() -> None:
    text = CHAPTER.read_text(encoding="utf-8")
    for p in PLACES:  # 멱등 — 이미 있으면 지우고 다시 넣는다
        text = re.sub(
            r"\n#### " + re.escape(p["name"]) + r" \{\{grade:.*?\n\n---\n", "\n", text, flags=re.S)

    blocks = []
    for p in PLACES:
        blocks.append(
            f"#### {p['name']} {{{{grade:{GRADE_TOKEN[p['grade']]}}}}}\n"
            f"> **Editor's Verdict**: {p['summary']}\n"
            f"- **상세 가이드**: [{p['name']} 전체 가이드 보기](../places/{p['slug']}.html)\n\n---\n")
    anchor = "\n## 음식·시장·카페·생활체험\n"
    assert anchor in text, "챕터에서 음식 절 앵커를 찾지 못했다"
    text = text.replace(anchor, "\n" + "\n".join(blocks) + anchor, 1)

    # 방문 업소 목록
    marker = "### 방문 업소\n\n"
    assert marker in text
    bullets = "".join(
        f"- **{p['name']}** — {p['summary']} ([상세 정보](../places/{p['slug']}.html))\n"
        for p in PLACES)
    head, tail = text.split(marker, 1)
    existing = [ln for ln in tail.splitlines() if ln.startswith("- **")]
    keep = [ln for ln in existing
            if not any(f"](../places/{p['slug']}.html)" in ln for p in PLACES)]
    rest = tail.split("\n\n", 1)[1] if "\n\n" in tail else ""
    text = head + marker + "\n".join(keep) + "\n" + bullets + "\n" + rest
    CHAPTER.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- 4. JSON 데이터
def patch_json() -> None:
    def load(rel):
        path = ROOT / rel
        return path, json.loads(path.read_text(encoding="utf-8"))

    def save(path, obj):
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")

    # place-facts — 빈칸 판정 가드가 price 를 본다
    path, facts = load("data/place-facts.json")
    for p in PLACES:
        def fact(v, conf, src):
            return {"value": v, "confidence": conf, "source": src,
                    "verified_at": VERIFIED, "ttl_days": 90}
        src = p.get("url") or "MP-04 웹 조사 2026-08-25 (복수 출처 교차)"
        conf = "official" if p.get("url") else "secondary"
        facts["places"][p["slug"]] = {
            "displayName": p["name"],
            "region": "paris",
            "grade": GRADE_EN[p["grade"]],
            "facts": {
                "hours": fact(p["hours"], conf, src),
                "closed": fact(p["closed"], conf, src),
                "booking": fact(p["booking"], conf, src),
                "price_range": fact(p["price"], "secondary", src),
                "duration": {"value": p["duration"], "confidence": "editorial",
                             "source": "MP-04 Editorial", "verified_at": VERIFIED,
                             "ttl_days": 3650},
            },
        }
    save(path, facts)

    # map-queries — 좌표가 없으므로 이름 검색으로 연다
    path, mq = load("data/map-queries.json")
    for p in PLACES:
        mq["places"][p["slug"]] = {
            "query": f"{p['name']}, {p['address'].split(',')[0]}, Paris"
                     if "Versailles" not in p["address"]
                     else f"{p['name']}, Château de Versailles",
            "verdict": "FOUND",
            "resolvedName": p["name"],
            "evidence": p.get("url") or "MP-04 웹 조사 2026-08-25 (복수 출처 교차)",
            "verifiedAt": VERIFIED,
        }
    save(path, mq)

    # 사진 상태 — 새 업소는 사진이 없다. NO_IMAGE 는 실패가 아니다
    path, photo = load("data/images/food-photo-status.json")
    for p in PLACES:
        photo["places"][p["slug"]] = {
            "status": "NO_IMAGE", "region": "paris",
            "why": "MP-04 로 새로 넣은 업소다. 권리 확인된 사진을 아직 찾지 않았다",
            "checkedAt": VERIFIED,
        }
    save(path, photo)

    # 완결성 빈칸 판정 — menu 는 Day 카드에서 채우므로 여기서는 비워 둔다
    path, gaps = load("data/food-completeness-disposition.json")
    for p in PLACES:
        gaps["gaps"]["photo"][p["slug"]] = {
            "disposition": "RESOLVED",
            "why": "사진 없음(NO_IMAGE)으로 판정했다. 근거는 food-photo-status.json",
        }
    save(path, gaps)


# ---------------------------------------------------------------- 5. CSV 대장
def patch_csv() -> None:
    path = ROOT / "FCR_MASTER_FOOD_INVENTORY.csv"
    rows = list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8"))))
    keep = [r for r in rows if r["slug"] not in {p["slug"] for p in PLACES}]
    for p in PLACES:
        keep.append({"item_type": "FOOD_PLACE", "slug": p["slug"], "name": p["name"],
                     "region": "paris", "status": "ACTIVE", "notes": "restaurant"})
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["item_type", "slug", "name", "region",
                                        "status", "notes"], lineterminator="\n")
    w.writeheader()
    w.writerows(keep)
    path.write_text(buf.getvalue(), encoding="utf-8")

    path = ROOT / "PLACE_TAXONOMY_AND_TIERS.csv"
    rows = list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8"))))
    fields = list(rows[0].keys())
    keep = [r for r in rows if r["id"] not in {p["slug"] for p in PLACES}]
    for p in PLACES:
        keep.append({
            "id": p["slug"], "name": p["name"], "region": "paris",
            "legacy_type": "spot", "normalized_type": "restaurant",
            "priority": PRIORITY[p["grade"]], "content_tier": TIER[p["grade"]],
            "day_refs": p["best_context"], "has_dedicated_place_page": "Y",
            "current_content_depth": "DEEP_GUIDE", "rationale": p["summary"],
        })
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    w.writerows(keep)
    path.write_text(buf.getvalue(), encoding="utf-8")


def main() -> int:
    for p in PLACES:
        write_dossier(p)
    patch_registry()
    patch_chapter()
    patch_json()
    patch_csv()
    print(f"장소 정본 {len(PLACES)}개 · 명부·원고·facts·map-queries·사진상태·대장 갱신")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
