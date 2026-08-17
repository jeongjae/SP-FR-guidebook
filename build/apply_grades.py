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

# T3-1 이 정한 정본. 이걸 모르면 매트릭스 이름을 보고 폐기된 ID 를 다시 만든다.
from merge_place_ids import MERGE, RENAME  # noqa: E402


def norm(s):
    """괄호 부기는 뗀다. 'Colline du Château' 와 'Colline du Château (성채 언덕)' 은
    같은 장소다 — 이걸 다르게 봐서 `-2` 레코드가 생겼고, 그것이 T3-1 이 치운 중복이다."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    # NFKD 는 한글 음절을 자모로 쪼갠다. 다시 합치지 않으면 아래 필터가 한글을 통째로
    # 날려 **모든 한글 이름이 빈 문자열이 되고 서로 같은 장소로 매칭된다.**
    s = unicodedata.normalize("NFC", s).lower()
    s = re.sub(r"[(（].*?[)）]", "", s)
    s = re.sub(r"[^a-z0-9가-힣]", "", s)
    return s


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
    # 같은 (지역,이름) 이 다른 등급으로 여러 번 나온다 — 최고 등급이 그 장소의 등급이다
    order0 = ["essential", "priority", "optional", "alternative", "excluded", "none"]
    best_grade = {}
    for r in rows:
        g0 = (r.get("grade") or "").strip()
        if g0 not in order0:
            continue
        k = ((r.get("region") or "").strip(), norm(r["name"]))
        if k not in best_grade or order0.index(g0) < order0.index(best_grade[k]):
            best_grade[k] = g0

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
                # 매트릭스가 정본이다 — 올리기만 하면 매트릭스가 내린 등급이 남는다.
                # (peralada 가 excluded 인데 essential 로 살아남은 것이 이 버그였다.)
                # 다만 같은 (지역,이름) 이 여러 등급으로 중복된 행이 있어, 내릴 때는
                # 그 이름의 **최고** 등급을 기준으로 한다.
                order = ["essential", "priority", "optional", "alternative", "excluded", "none"]
                cur = places[pid].get("grade", "none")
                top = best_grade.get((region, norm(r["name"])), g)
                if order.index(top) != order.index(cur):
                    places[pid]["grade"] = top
                    updated += 1
            used.add(pid)
            continue
        # place-facts 에 없는 필수·우선추천은 빈 레코드를 만든다
        if g not in ("essential", "priority"):
            continue
        new_id = slug(r["name"])
        new_id = RENAME.get(new_id, MERGE.get(new_id, new_id))
        if new_id in places:          # 정본이 이미 있다 — 새로 만들지 않는다
            used.add(new_id)
            continue
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
