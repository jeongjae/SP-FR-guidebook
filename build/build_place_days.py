#!/usr/bin/env python3
"""T1-0b — data/place-days.json 생성.

엔트리매트릭스 CSV 의 `days` 열이 정본이다. Day 번호는 **글로벌**(1–43)이며
'Day 2' · '8;9;11' · 'Day 2;Day 3' 같은 표기를 모두 흡수한다.

G1 이 "이 장소를 며칠에 가는가"를 판정할 때 마지막 단계로 쓴다.
"""
import csv
import json
import pathlib
import re
import unicodedata
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
MATRIX = ROOT / "docs/diagnosis-v2/SPFR_전수진단_엔트리매트릭스_v2.0.csv"
FACTS = ROOT / "data/place-facts.json"
OUT = ROOT / "data/place-days.json"

# days 열은 두 형식이 섞여 있다 — "Day 4" · "9" · "9/22(화)" · "10/7;10/8"
DATE_LIT = re.compile(r"(?<!\d)(\d{1,2})/(\d{1,2})(?!\d)")
DAY_NUM = re.compile(r"(?<![\d/])(\d{1,2})(?![\d/])")
TRIP_START = date(2026, 8, 29)


def norm(s):
    s = unicodedata.normalize("NFKC", s or "").lower()
    return re.sub(r"[^a-z0-9가-힣]", "", s)


def parse_days(cell):
    """'Day 4' · '9' · '9/22(화)' · '10/7;10/8' 을 모두 글로벌 Day 번호로."""
    if not cell or not cell.strip():
        return []
    out = set()
    rest = cell
    for m in DATE_LIT.finditer(cell):
        mo, dd = int(m.group(1)), int(m.group(2))
        try:
            d = date(TRIP_START.year, mo, dd)
        except ValueError:
            continue
        n = (d - TRIP_START).days + 1
        if 1 <= n <= 43:
            out.add(n)
        rest = rest.replace(m.group(0), " ")
    for n in DAY_NUM.findall(rest):
        if 1 <= int(n) <= 43:
            out.add(int(n))
    return sorted(out)


# 매트릭스 표기와 place-facts displayName 이 다른 것들 — 직접 지정한다.
ALIAS = {
    "Les Halles d'Avignon": "les-halles",
    "Les Halles d’Avignon": "les-halles",
    "Museu del Cau Ferrat": "cau-ferrat",
    "Marché Forville (Cannes)": "marche-forville",
    "Saint-Paul-de-Vence (Fondation Maeght·마을 묘지)": "fondation-maeght",
    "Halles de Lyon Paul Bocuse": "halles-de-lyon-paul-bocuse",
}


def main():
    facts = json.loads(FACTS.read_text(encoding="utf-8"))["places"]
    by_norm = {norm(p["displayName"]): pid for pid, p in facts.items()}
    # placeId 자체로도 맞춰 본다 (displayName 이 다른 경우)
    for pid in facts:
        by_norm.setdefault(norm(pid.replace("-", "")), pid)

    rows = list(csv.DictReader(MATRIX.open(encoding="utf-8-sig")))
    mapping, unmatched = {}, []
    for r in rows:
        days = parse_days(r.get("days", ""))
        if not days:
            continue
        nm = r["name"]
        pid = ALIAS.get(nm) or by_norm.get(norm(nm))
        if pid and pid not in facts:
            pid = None
        if not pid:
            for k, v in ALIAS.items():
                if norm(k) in norm(nm) or norm(nm) in norm(k):
                    pid = v if v in facts else None
                    if pid:
                        break
        if not pid:
            # "Museu del Cau Ferrat" · "Marché Forville (Cannes)" · "Croix-Rousse (동네…)"
            base = re.sub(r"[（(].*", "", nm)
            base = re.sub(r"^(Museu del|Museu de|Musée du|Musée de la|Musée)\s+", "", base).strip()
            base = re.sub(r"\s+(d'|de |의 )?(Avignon|Cannes|Lyon|Paris|Nice)$", "", base).strip()
            for cand in (base, base.split("·")[0].strip(), base.split("—")[0].strip()):
                pid = by_norm.get(norm(cand))
                if pid:
                    break
        if not pid:
            unmatched.append((r["region"], r["name"], days))
            continue
        mapping.setdefault(pid, {"displayName": facts[pid]["displayName"],
                                 "region": facts[pid]["region"], "days": []})
        mapping[pid]["days"] = sorted(set(mapping[pid]["days"]) | set(days))

    doc = {"version": "1.0",
           "source": "docs/diagnosis-v2/SPFR_전수진단_엔트리매트릭스_v2.0.csv (days 열)",
           "note": "Day 번호는 글로벌 1–43. G1 이 방문일 판정의 마지막 단계로 쓴다.",
           "places": dict(sorted(mapping.items()))}
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"place-days: {len(mapping)}곳 매핑 · CSV 행 {len(rows)}")
    print(f"place-facts 에 없어 건너뛴 엔트리 {len(unmatched)}건")
    for reg, name, days in unmatched[:10]:
        print(f"    · [{reg}] {name[:40]} {days}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
