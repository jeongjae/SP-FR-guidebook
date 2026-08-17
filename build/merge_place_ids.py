#!/usr/bin/env python3
"""T3-1 — 중복 placeId 해소.

**왜 심각한가.** 이 인프라 전체가 "같은 사실이 여러 곳에 갈라지는 것"을 막으려고
있는데, 단일 소스 자체가 한 장소에 두 ID를 갖고 있었다. `versailles` 는 값이 있고
`versailles-2` 는 비어 있으면 원고가 어느 토큰을 쓰느냐에 따라 다른 것이 렌더된다 —
**막으려던 사고를 인프라가 재현한다.**

원인은 S2 의 `apply_grades.py` 다. 매트릭스에 있는데 place-facts 에 없는 필수·우선추천을
새 레코드로 만들면서, S0 시드가 다른 이름으로 이미 갖고 있던 장소를 다시 만들었다.
그래서 매트릭스 유래 쪽에만 `days` 가 붙어 있다.

병합 규칙: 값이 다르면 **official 우선 → 최신 verified_at 우선**. 폐기한 값은
`data/superseded.json` 에 남긴다. 조용히 버리지 않는다.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FACTS = ROOT / "data/place-facts.json"
SUPERSEDED = ROOT / "data/superseded.json"
CHAPTERS = ROOT / "source/CURRENT/20_Regional_Chapters"

# ── 판정표 ───────────────────────────────────────────────────────────────
# 같은 장소다 — 뒤를 앞으로 병합한다.
MERGE = {
    "arles-2": "arles",
    "versailles-2": "versailles",
    "les-halles": "les-halles-d-avignon",          # 파리 Les Halles 와 구분해야 한다
    "gordes-2": "gordes",
    "marche-forville-cannes": "marche-forville",
    "colline-du-chateau-2": "colline-du-chateau",
    "lourmarin-2": "lourmarin",
    "atelier-des-lauves-atelier-de-cezanne": "atelier-des-lauves",
    "le-rocher-monaco-ville": "le-rocher",
    "passeig-de-la-muralla-2": "passeig-de-la-muralla",
    "annecy-palais-de-l-ile-chateau": "annecy",
    "montmartre-south-pigalle-sacre-c-ur": "montmartre-south-pigalle",
    "croix-rousse-cour-des-voraces-maison-des-canuts": "croix-rousse",
    "museu-del-cau-ferrat": "cau-ferrat",          # 18쌍 목록 밖에서 추가로 찾은 것
    "saint-paul-de-vence-fondation-maeght": "fondation-maeght",
}

# 별개 장소인데 ID 가 잘못 붙었다 — 개명한다.
RENAME = {
    "gordes-3": "marche-gordes",             # 마을이 아니라 화요시장
    "croix-rousse-2": "marche-croix-rousse",  # 동네가 아니라 시장
    "place": "marche-collioure",             # 'place' 는 ID 가 아니다
    # T4-2 — 도시 접두 없는 일반명사형. region 으로 구분되더라도 ID 자체가
    # 자기설명적이어야 한다. 모호한 ID 는 중복보다 위험하다 — 중복은 값이
    # 갈라지지만, 모호한 ID 는 **엉뚱한 도시의 값이 붙어도 아무도 모른다.**
    "theatre-antique": "arles-theatre-antique",   # 리옹에도 Théâtre antique 가 있다
    "vieux-port": "marseille-vieux-port",         # 칸에도 Vieux-Port 가 있다
    "le-panier": "marseille-le-panier",
    "call": "girona-call",                        # 바르셀로나에도 Call 이 있다
    "la-roquette": "arles-la-roquette",           # 마르세유에도 La Roquette 가 있다
    "gracia": "barcelona-gracia",
    "2-30": "sitges-core-walk-2h30",              # 숫자는 이름이 아니다
}

# 건물과 전시는 별개다. 전시 레코드에서 **시설 사실을 뗀다** — 시설 사실은 건물에만 둔다.
EXHIBITIONS = {
    "grand-palais-cezanne-et-nous": "grand-palais",
    "musee-de-l-orangerie-monet-peindre-le-temps": "musee-de-l-orangerie",
}
FACILITY_KEYS = ("hours", "closed", "getting_there", "address")

CONF_RANK = {"official": 3, "secondary": 2, "unverified": 1, "unreachable": 0}


def better(a, b):
    """두 사실 중 남길 것. official 우선 → 최신 verified_at 우선 → 값 있는 쪽."""
    if not a:
        return b, None
    if not b:
        return a, None
    ra, rb = CONF_RANK.get(a.get("confidence"), 0), CONF_RANK.get(b.get("confidence"), 0)
    if ra != rb:
        return (a, b) if ra > rb else (b, a)
    va, vb = a.get("verified_at", ""), b.get("verified_at", "")
    if va != vb:
        return (a, b) if va > vb else (b, a)
    la, lb = len((a.get("value") or "")), len((b.get("value") or ""))
    return (a, b) if la >= lb else (b, a)


def main():
    doc = json.loads(FACTS.read_text(encoding="utf-8"))
    places = doc["places"]
    log = []

    # ① 개명 — 병합보다 먼저. 병합 대상이 개명된 ID 를 가리킬 수 있다.
    for old, new in RENAME.items():
        if old not in places:
            print(f"  ! 개명 대상 없음: {old}")
            continue
        if new in places:
            print(f"  ! 개명 충돌: {new} 가 이미 있다")
            continue
        places[new] = places.pop(old)
        log.append({"action": "rename", "from": old, "to": new,
                    "displayName": places[new]["displayName"]})

    # ② 병합
    for src, dst in MERGE.items():
        if src not in places:
            print(f"  ! 병합 대상 없음: {src}")
            continue
        if dst not in places:
            # 정본이 없으면 개명으로 처리한다 (값을 잃지 않는다)
            places[dst] = places.pop(src)
            log.append({"action": "rename", "from": src, "to": dst,
                        "displayName": places[dst]["displayName"]})
            continue
        s, t = places.pop(src), places[dst]
        # grade 는 높은 쪽을 남긴다
        order = ["essential", "priority", "optional", "alternative", "excluded", "none"]
        gs, gt = s.get("grade", "none"), t.get("grade", "none")
        if order.index(gs) < order.index(gt):
            t["grade"] = gs
        # displayName 은 더 서술적인 쪽 (긴 쪽)
        if len(s["displayName"]) > len(t["displayName"]):
            t["displayName"] = s["displayName"]
        for k in ("phone", "region"):
            if s.get(k) and not t.get(k):
                t[k] = s[k]
        sf, tf = s.get("facts", {}), t.setdefault("facts", {})
        for key, sv in sf.items():
            keep, drop = better(tf.get(key), sv)
            tf[key] = keep
            if drop and (drop.get("value") or "").strip():
                log.append({"action": "superseded", "placeId": dst, "fact_key": key,
                            "from_id": src, "dropped_value": drop.get("value"),
                            "dropped_confidence": drop.get("confidence"),
                            "dropped_verified_at": drop.get("verified_at"),
                            "kept_value": keep.get("value"),
                            "kept_confidence": keep.get("confidence")})
        log.append({"action": "merge", "from": src, "into": dst})

    # ③ 전시 레코드에서 시설 사실을 뗀다 — 시설 사실은 건물에만 있는다
    for ex, venue in EXHIBITIONS.items():
        if ex not in places:
            continue
        places[ex]["kind"] = "exhibition"
        places[ex]["venue"] = venue
        f = places[ex].get("facts", {})
        for k in FACILITY_KEYS:
            if k in f:
                v = f.pop(k)
                if (v.get("value") or "").strip():
                    log.append({"action": "moved_to_venue", "placeId": ex, "venue": venue,
                                "fact_key": k, "dropped_value": v.get("value")})

    doc["places"] = dict(sorted(places.items()))
    FACTS.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    SUPERSEDED.write_text(json.dumps(
        {"version": "1.0",
         "note": "T3-1 중복 placeId 해소에서 폐기하거나 옮긴 값. 조용히 버리지 않는다.",
         "entries": log}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ④ 원고의 {{fact:}} 토큰이 폐기된 ID 를 가리키지 않게 한다
    alias = dict(MERGE)
    alias.update(RENAME)
    changed = 0
    for f in sorted(CHAPTERS.glob("*.md")):
        t0 = t = f.read_text(encoding="utf-8")
        for old, new in alias.items():
            t = re.sub(r"\{\{fact:" + re.escape(old) + r"\.", "{{fact:" + new + ".", t)
        if t != t0:
            f.write_text(t, encoding="utf-8")
            changed += 1

    import collections
    c = collections.Counter(p.get("grade", "none") for p in places.values())
    print(f"개명 {len(RENAME)} · 병합 {len(MERGE)} · 전시 분리 {len(EXHIBITIONS)}")
    print(f"superseded 로그 {len(log)}건 → data/superseded.json")
    print(f"원고 토큰 갱신: {changed}개 파일")
    print(f"장소 {len(places)}곳 · grade 분포 {dict(c)}")
    print(f"★ essential+priority = {c['essential'] + c['priority']} (목표 101)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
