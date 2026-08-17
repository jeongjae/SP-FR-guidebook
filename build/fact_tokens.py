#!/usr/bin/env python3
"""S0 T0-2 — `{{fact:<placeId>.<key>}}` 치환기.

원고는 사실값을 하드코딩하지 않고 이 토큰으로 참조한다. 값의 단일 소스는
`data/place-facts.json` 이고, 출력 형식은 confidence 와 TTL 로 결정된다.

    official, TTL 이내   → 값 그대로
    official, TTL 초과   → 값 + ⟳출발 전 재확인
    secondary            → 값 + (2차 출처)
    unverified           → 미확인 — 현장 확인 필요
    unreachable          → 공식 확인 불가 — <전화> 문의   (전화가 있으면 자동 삽입)
    값 없음              → 미확인 — 현장 확인 필요

빌드에서 render_inline_tokens 보다 먼저 부른다.
"""
import json
import pathlib
import re
from datetime import date, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
FACTS_PATH = ROOT / "data" / "place-facts.json"

FACT_RE = re.compile(r"\{\{fact:([a-z0-9][a-z0-9-]*)\.([a-z_]+)\}\}")

_cache = None


def load_facts(path=None):
    global _cache
    if _cache is None or path is not None:
        p = path or FACTS_PATH
        _cache = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"places": {}}
    return _cache


def _stale(fact, ttl_defaults, key, today):
    """verified_at + ttl_days 가 지났는가."""
    va = fact.get("verified_at")
    if not va:
        return False
    ttl = fact.get("ttl_days") or ttl_defaults.get(key, 90)
    try:
        d = datetime.strptime(va, "%Y-%m-%d").date()
    except ValueError:
        return False
    return (today - d).days > ttl


def resolve(place_id, key, doc=None, today=None):
    """토큰 하나를 사람이 읽는 문자열로. (텍스트, 상태) 를 돌려준다."""
    doc = doc or load_facts()
    today = today or date.today()
    places = doc.get("places", {})
    ttl_defaults = doc.get("ttl_defaults", {})

    place = places.get(place_id)
    if place is None:
        return (f"[미등록 장소: {place_id}]", "missing_place")

    fact = place.get("facts", {}).get(key)
    phone = place.get("phone", "")
    if fact is None:
        return ("미확인 — 현장 확인 필요", "missing_fact")

    value = (fact.get("value") or "").strip()
    conf = fact.get("confidence", "unverified")

    if conf == "unreachable" or (not value and conf != "official"):
        tail = f" — {phone} 문의" if phone else ""
        return (f"공식 확인 불가{tail}", "unreachable")
    if not value:
        return ("미확인 — 현장 확인 필요", "empty")
    if conf == "unverified":
        return (f"{value} · 미확인 — 현장 확인 필요", "unverified")
    if conf == "secondary":
        return (f"{value} (2차 출처)", "secondary")
    if _stale(fact, ttl_defaults, key, today):
        return (f"{value} ⟳출발 전 재확인", "stale")
    return (value, "fresh")


def render_fact_tokens(text, doc=None, today=None, stats=None):
    """본문의 모든 `{{fact:}}` 토큰을 치환한다."""
    doc = doc or load_facts()

    def sub(m):
        out, status = resolve(m.group(1), m.group(2), doc, today)
        if stats is not None:
            stats[status] = stats.get(status, 0) + 1
        return out

    return FACT_RE.sub(sub, text)


def scan(text):
    """본문에 쓰인 (placeId, key) 목록."""
    return [(m.group(1), m.group(2)) for m in FACT_RE.finditer(text)]


if __name__ == "__main__":
    import sys
    doc = load_facts()
    if len(sys.argv) > 1:
        pid, key = sys.argv[1].split(".", 1)
        print(resolve(pid, key, doc))
    else:
        n = sum(len(p["facts"]) for p in doc["places"].values())
        print(f"place-facts: 장소 {len(doc['places'])} · 사실 {n}")
        for pid, p in list(doc["places"].items())[:3]:
            for k in p["facts"]:
                print(f"  {{{{fact:{pid}.{k}}}}} → {resolve(pid, k, doc)[0][:70]}")
