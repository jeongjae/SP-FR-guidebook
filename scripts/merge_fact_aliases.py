#!/usr/bin/env python3
"""place-facts 의 별칭 레코드를 canonical 슬러그로 합친다.

    python3 scripts/merge_fact_aliases.py --dry-run
    python3 scripts/merge_fact_aliases.py

같은 장소가 두 슬러그로 들어 있으면 운영시간이 서로 다른 채로 남는다.
실제로 그랬다 — `les-halles-d-avignon` 과 `les-halles` 의 영업시간이 달랐고,
화면은 그중 하나만 읽었다. 현장에서 어느 쪽이 맞는지 알 방법이 없다.

판정의 정본은 `data/place-facts-disposition.json` 이다. 이 스크립트는 거기서
`ALIAS_OF_EXISTING_PLACE` 인 것만 옮긴다.

충돌은 최신값을 임의로 고르지 않는다.

    1 신뢰도  official > secondary > editorial > unverified > unreachable
    2 같으면 verified_at 이 늦은 쪽
    3 그래도 같으면 canonical 쪽을 남긴다
    4 값이 다른 official 끼리 부딪히면 **보고서에 남긴다**

원고의 `{{fact:별칭.항목}}` 토큰도 함께 옮긴다. 안 옮기면 화면이 조용히
'(확인 필요)' 로 바뀐다.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

import model  # noqa: E402

FACTS = ROOT / "data" / "place-facts.json"
DISPOSITION = ROOT / "data" / "place-facts-disposition.json"
CHAPTERS = sorted((ROOT / "source" / "CURRENT" / "20_Regional_Chapters").glob("*.md"))
PLACES = sorted((ROOT / "source" / "CURRENT" / "30_Places").glob("*.md"))

RANK = {"official": 4, "secondary": 3, "editorial": 2,
        "unverified": 1, "unreachable": 0}


# 이 항목들이 official 끼리 다른 값으로 부딪히면 **같은 시설이 아니다.**
# Museu de Maricel(화–일 10–19시)과 Palau de Maricel(가이드투어 전용)이
# 그랬다. 한쪽을 버리면 현장에서 닫힌 문 앞에 서게 된다.
ENTITY_KEYS = ("hours", "closed", "booking", "price_adult", "address")


def better(a: dict, b: dict) -> tuple[dict, bool]:
    """(남길 것, 값이 실제로 충돌했는가)."""
    ra, rb = RANK.get(a.get("confidence"), 0), RANK.get(b.get("confidence"), 0)
    clash = (a.get("value") or "") != (b.get("value") or "")
    if ra != rb:
        return (a if ra > rb else b), clash
    da, db = a.get("verified_at") or "", b.get("verified_at") or ""
    if da != db:
        return (a if da > db else b), clash
    return a, clash


def hard_conflict(key: str, a: dict, b: dict) -> bool:
    """같은 시설이라는 전제를 무너뜨리는 충돌인가."""
    if key not in ENTITY_KEYS:
        return False
    va, vb = (a.get("value") or "").strip(), (b.get("value") or "").strip()
    if not va or not vb or va == vb:
        return False
    return a.get("confidence") == "official" and b.get("confidence") == "official"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    trip = model.load_trip()
    payload = json.loads(FACTS.read_text(encoding="utf-8"))
    places = payload["places"]
    rules = json.loads(DISPOSITION.read_text(encoding="utf-8"))["slugs"]

    merged, skipped, conflicts, blocked = [], [], [], []
    for alias, rule in sorted(rules.items()):
        if rule["disposition"] != "ALIAS_OF_EXISTING_PLACE":
            continue
        canon = rule.get("canonical")
        if alias not in places:
            continue
        if not canon or canon not in trip.places:
            skipped.append((alias, canon, "canonical 이 명부에 없다 — 상위 판정이 먼저다"))
            continue
        src = places[alias]
        dst = places.setdefault(canon, {
            "displayName": trip.places[canon].name,
            "region": trip.places[canon].region,
            "grade": trip.places[canon].grade or "none",
            "facts": {}})
        # 먼저 훑어본다. 하드 충돌이 하나라도 있으면 합치지 않는다.
        hard = [k for k, f in (src.get("facts") or {}).items()
                if k in (dst.get("facts") or {})
                and hard_conflict(k, dst["facts"][k], f)]
        # 사람이 이미 판정한 충돌은 통과시킨다. 판정 근거는 disposition 파일에
        # 적혀 있고, 버린 값은 아래 conflicts 기록에 남는다.
        if hard and rule.get("conflictResolution") == "prefer-canonical":
            for key in rule.get("preserveAsNote") or []:
                f = (src.get("facts") or {}).get(key)
                if f and "note" not in dst["facts"]:
                    dst["facts"]["note"] = dict(f)
            hard = []
        if hard:
            blocked.append((alias, canon, hard))
            continue
        places.pop(alias)
        moved_keys = []
        for key, fact in (src.get("facts") or {}).items():
            have = dst["facts"].get(key)
            if have is None:
                dst["facts"][key] = fact
                moved_keys.append(key)
                continue
            keep, clash = better(have, fact)
            if clash:
                conflicts.append({
                    "canonical": canon, "alias": alias, "key": key,
                    "kept": {"value": keep.get("value"),
                             "confidence": keep.get("confidence"),
                             "verified_at": keep.get("verified_at"),
                             "source": keep.get("source")},
                    "dropped": {"value": (fact if keep is have else have).get("value"),
                                "confidence": (fact if keep is have else have).get("confidence"),
                                "verified_at": (fact if keep is have else have).get("verified_at"),
                                "source": (fact if keep is have else have).get("source")},
                })
            dst["facts"][key] = keep
        merged.append((alias, canon, moved_keys))

    # 원고·장소 원고의 토큰도 옮긴다
    renames = {a: c for a, c, _ in merged}
    touched = []
    for path in CHAPTERS + PLACES:
        text = path.read_text(encoding="utf-8")
        new = text
        for alias, canon in renames.items():
            new = new.replace(f"{{{{fact:{alias}.", f"{{{{fact:{canon}.")
        if new != text and not args.dry_run:
            path.write_text(new, encoding="utf-8")
        if new != text:
            touched.append(path.name)

    for alias, canon, keys in merged:
        print(f"  {alias:52s} → {canon:34s} 옮긴 항목 {keys or '없음(중복)'}")
    for alias, canon, why in skipped:
        print(f"  · {alias:52s} 보류 — {why}")
    for alias, canon, keys in blocked:
        print(f"  ! {alias:52s} 병합 중단 — {canon} 와 {keys} 가 official 끼리 다르다. "
              f"같은 시설이 아닐 수 있다")
    if conflicts:
        print(f"\n값 충돌 {len(conflicts)}건:")
        for c in conflicts:
            print(f"  {c['canonical']}.{c['key']}")
            print(f"     남김: {c['kept']['value'][:60]!r} ({c['kept']['confidence']}·{c['kept']['verified_at']})")
            print(f"     버림: {c['dropped']['value'][:60]!r} ({c['dropped']['confidence']}·{c['dropped']['verified_at']})")

    if not args.dry_run:
        FACTS.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
        (ROOT / "FCR03_FACT_MERGE_CONFLICTS.json").write_text(
            json.dumps({"mergedAt": "2026-08-22", "merged": len(merged),
                        "skipped": skipped, "blocked": blocked,
                        "conflicts": conflicts},
                       ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n병합 {len(merged)} · 보류 {len(skipped)} · 중단 {len(blocked)} "
          f"· 값 충돌 {len(conflicts)} "
          f"· 토큰 고친 원고 {len(set(touched))}개" + (" (dry-run)" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
