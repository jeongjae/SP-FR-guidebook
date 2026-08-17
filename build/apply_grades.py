#!/usr/bin/env python3
"""T2-0(c) — place-facts 의 grade 를 엔트리매트릭스 기준으로 채운다.

매트릭스 CSV 의 `grade` 열이 정본이다. 웹 조사가 아니라 데이터 작업이다.
매트릭스에 있는데 place-facts 에 없는 필수·우선추천 장소는 **레코드를 새로 만든다**
(facts 는 비운 채로) — 그래야 G2·G3 의 분모가 의미를 갖고, 큐가 그것을 MISSING 으로 잡는다.
"""
import csv
import json
import pathlib
import re
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
MATRIX = ROOT / "docs/diagnosis-v2/SPFR_전수진단_엔트리매트릭스_v2.0.csv"
FACTS = ROOT / "data/place-facts.json"

REGIONS = {"barcelona", "girona", "nice", "aix", "luberon", "avignon", "lyon", "paris"}


def norm(s):
    s = unicodedata.normalize("NFKC", s or "").lower()
    return re.sub(r"[^a-z0-9가-힣]", "", s)


def slug(name):
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9가-힣]+", "-", s).strip("-")
    return s[:60] or "place"


def main():
    doc = json.loads(FACTS.read_text(encoding="utf-8"))
    places = doc["places"]
    by_norm = {norm(p["displayName"]): pid for pid, p in places.items()}
    for pid in places:
        by_norm.setdefault(norm(pid.replace("-", "")), pid)

    rows = list(csv.DictReader(MATRIX.open(encoding="utf-8-sig")))
    updated = created = 0
    used = set()

    for r in rows:
        g = (r.get("grade") or "").strip()
        if g not in ("essential", "priority", "optional", "alternative", "excluded"):
            continue
        region = (r.get("region") or "").strip()
        if region not in REGIONS:
            continue
        pid = by_norm.get(norm(r["name"]))
        if pid:
            if places[pid].get("grade") != g:
                # 이미 등급이 있으면 더 높은 쪽을 남긴다 (essential > priority > …)
                order = ["essential", "priority", "optional", "alternative", "excluded", "none"]
                cur = places[pid].get("grade", "none")
                if order.index(g) < order.index(cur):
                    places[pid]["grade"] = g
                    updated += 1
            used.add(pid)
            continue
        # place-facts 에 없는 필수·우선추천은 빈 레코드를 만든다
        if g not in ("essential", "priority"):
            continue
        new_id = slug(r["name"])
        base, i = new_id, 2
        while new_id in places:
            new_id = f"{base}-{i}"; i += 1
        places[new_id] = {"displayName": r["name"].strip(), "region": region,
                          "grade": g, "facts": {}}
        created += 1

    doc["places"] = dict(sorted(places.items()))
    FACTS.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    import collections
    c = collections.Counter(p.get("grade") for p in places.values())
    print(f"grade 갱신 {updated} · 신규 레코드 {created}")
    print(f"분포: {dict(c)}")
    print(f"필수+우선추천: {c['essential'] + c['priority']} / 전체 {len(places)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
