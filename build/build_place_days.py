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
# 시각(19:30)의 숫자를 Day 번호로 읽으면 안 된다 — 콜론 양옆을 배제한다.
DAY_NUM = re.compile(r"(?<![\d/:])(\d{1,2})(?![\d/:])")
TRIP_START = date(2026, 8, 29)


def norm(s):
    s = unicodedata.normalize("NFKC", s or "").lower()
    return re.sub(r"[^a-z0-9가-힣]", "", s)


def parse_days(cell):
    """'Day 4' · '9' · '9/22(화)' · '10/7;10/8' 을 모두 글로벌 Day 번호로."""
    if not cell or not cell.strip():
        return []
    out = set()
    rest = re.sub(r"\d{1,2}:\d{2}", " ", cell)     # 시각 제거가 먼저다
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
# T3-1 이 정한 정본 ID 를 쓴다. 병합 전 ID 를 남겨 두면 매핑이 조용히 빈다.
ALIAS = {
    "Les Halles d'Avignon": "les-halles-d-avignon",
    "Les Halles d’Avignon": "les-halles-d-avignon",
    "Les Halles": "les-halles-d-avignon",
    "Museu del Cau Ferrat": "cau-ferrat",
    "Marché Forville (Cannes)": "marche-forville",
    "Saint-Paul-de-Vence (Fondation Maeght·마을 묘지)": "fondation-maeght",
    "Halles de Lyon Paul Bocuse": "halles-de-lyon-paul-bocuse",
    "콜리우르 시장 (수요일)": "marche-collioure",
    "Croix-Rousse 시장": "marche-croix-rousse",
    "Gordes 화요시장": "marche-gordes",
}


# 지역 챕터가 덮는 Day 범위. 이 밖의 값은 파싱 사고다 —
# "Day1 시간표" 같은 문서 이름의 숫자가 Day 번호로 잡히면 리옹 식당이 Day 1 에 선다.
REGION_DAYS = {"barcelona": (1, 4), "girona": (4, 7), "nice": (7, 12), "aix": (12, 16),
               "luberon": (16, 19), "avignon": (19, 23), "lyon": (23, 27), "paris": (27, 43)}


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
        rng = REGION_DAYS.get(facts[pid].get("region"))
        if rng:
            kept = [n for n in days if rng[0] <= n <= rng[1]]
            if kept:                       # 전부 범위 밖이면 원값을 남겨 사람이 본다
                days = kept
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
