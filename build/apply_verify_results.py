#!/usr/bin/env python3
"""T2-3·T2-4 — 조사 결과를 place-facts.json 에 적재하고 verify_log.csv 를 남긴다.

입력: scratchpad/results/<region>.json  (조사 단위가 반환한 JSON 배열)
  [{"placeId","key","value","source","verified_at","confidence","phone","blocked_reason"}]

원칙
  · 결과는 **원고가 아니라 place-facts.json 에만** 쓴다
  · confidence=official 이면 source·verified_at 필수 (스키마가 강제한다)
  · unreachable 이면 blocked_reason 필수
  · 같은 (placeId, fact_key) 를 두 번 조회했으면 로그에서 중복으로 잡힌다
"""
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FACTS = ROOT / "data/place-facts.json"
LOG = ROOT / "build/verify_log.csv"
RESULTS = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else \
    pathlib.Path("/tmp/claude-1000/-mnt-c-Users-NB-24021500-source-worktrees-SP-FR-content-dev/"
                 "42dae3a8-fe95-444d-bb7f-bd837f298939/scratchpad/results")

TTL = {"price_adult": 180, "price_range": 180, "hours": 90, "closed": 90,
       "booking": 90, "getting_there": 30, "duration": 365, "note": 90}
VALID_KEYS = set(TTL)


def main():
    doc = json.loads(FACTS.read_text(encoding="utf-8"))
    places = doc["places"]

    log_rows, applied, skipped, unknown = [], 0, 0, []
    seen = {}

    for f in sorted(RESULTS.glob("*.json")):
        region = f.stem
        try:
            items = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"  ! {f.name} 파싱 실패: {e}")
            continue
        for it in items:
            pid = (it.get("placeId") or "").strip()
            key = (it.get("key") or it.get("fact_key") or "").strip()
            conf = (it.get("confidence") or "unverified").strip()
            val = (it.get("value") or "").strip()
            src = (it.get("source") or "").strip()
            vat = (it.get("verified_at") or "").strip()
            phone = (it.get("phone") or "").strip()
            reason = (it.get("blocked_reason") or "").strip()

            log_rows.append(dict(region=region, placeId=pid, fact_key=key,
                                 confidence=conf, source=src, verified_at=vat,
                                 phone=phone, blocked_reason=reason))
            k = (pid, key)
            seen[k] = seen.get(k, 0) + 1

            if pid not in places or key not in VALID_KEYS:
                unknown.append(f"{region}: {pid}.{key}")
                continue
            if phone and not places[pid].get("phone"):
                places[pid]["phone"] = phone

            if conf == "official":
                if not val or not src or not vat:
                    skipped += 1
                    continue
                rec = {"value": val, "source": src, "verified_at": vat,
                       "confidence": "official", "ttl_days": TTL.get(key, 90)}
            elif conf == "unreachable":
                rec = {"value": "", "confidence": "unreachable",
                       "blocked_reason": reason or "공식 소스 접근 실패",
                       "ttl_days": TTL.get(key, 90)}
                if src:
                    rec["source"] = src
                if vat:
                    rec["verified_at"] = vat
            else:                       # unverified / secondary
                rec = {"value": val, "confidence": "unverified" if conf != "secondary" else "secondary",
                       "ttl_days": TTL.get(key, 90)}
                if src:
                    rec["source"] = src
                if vat:
                    rec["verified_at"] = vat
                if not val and reason:
                    rec["value"] = ""
                    rec["confidence"] = "unreachable"
                    rec["blocked_reason"] = reason

            cur = places[pid].setdefault("facts", {}).get(key)
            # 기존 official 을 unverified 로 덮지 않는다
            if cur and cur.get("confidence") == "official" and rec["confidence"] != "official":
                skipped += 1
                continue
            places[pid]["facts"][key] = rec
            applied += 1

    doc["places"] = dict(sorted(places.items()))
    FACTS.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with LOG.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["region", "placeId", "fact_key", "confidence",
                                           "source", "verified_at", "phone", "blocked_reason"])
        w.writeheader()
        w.writerows(log_rows)

    dup = {k: v for k, v in seen.items() if v > 1}
    import collections
    conf_c = collections.Counter(r["confidence"] for r in log_rows)
    n_facts = sum(len(p.get("facts", {})) for p in places.values())
    n_closed = sum(1 for p in places.values()
                   if (p.get("facts", {}).get("closed", {}).get("value") or "").strip())
    print(f"조회 로그 {len(log_rows)}행 → build/verify_log.csv")
    print(f"적재 {applied} · 건너뜀 {skipped} · 미등록 대상 {len(unknown)}")
    print(f"조회 confidence: {dict(conf_c)}")
    print(f"place-facts: 장소 {len(places)} · 사실 {n_facts} · closed 보유 {n_closed}곳")
    print(f"중복 조회: {len(dup)}건" + (f" → {list(dup)[:5]}" if dup else ""))
    for u in unknown[:10]:
        print(f"    미등록: {u}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
