#!/usr/bin/env python3
"""MP-03 — 사진 없는 장소의 레이아웃 안전성 검사.

카드에서 사진이 빠지면 자리가 사라지는 것이 아니라 **빈 열이 남는다**.
`.place-card` 는 `84px 1fr` 그리드라 첫 열이 비면 제목과 설명이 사진 칸으로
밀려 들어간다 — 니스의 식당 세 곳에서 실제로 그렇게 깨졌다.

그래서 이 검사는 "사진이 있는가" 가 아니라 **"사진이 없을 때 자리가 지켜지는가"**
를 본다. 사진을 다 채우는 것은 목표가 아니다. 못 채운 곳에서 포맷이 무너지지
않는 것이 목표다.

사용:
    SPFR_SITE_DIR=<빌드경로> python3 scripts/mp03_place_photo_layout_audit.py
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARD = re.compile(r'<article class="card (place-card|place-card-lg)">(.*?)</article>', re.S)
LINK = re.compile(r'class="card-link" href="\.\./places/([^"]+)\.html"')
LABEL = re.compile(r'aria-label="([^"]+)"')


def main() -> int:
    site = Path(os.environ.get("SPFR_SITE_DIR") or (ROOT / "site")).resolve()
    if not site.exists():
        print(f"빌드 산출물이 없다: {site}")
        return 1

    manifest = json.loads(
        (ROOT / "data" / "images" / "image-manifest.json").read_text(encoding="utf-8"))
    have = {i["placeId"] for i in manifest.get("images", []) if i.get("placeId")}

    rows, naked, missing_asset = [], [], []
    for page in sorted(site.glob("guide/*.html")):
        if page.name == "index.html":
            continue
        html = page.read_text(encoding="utf-8", errors="replace")
        for kind, body in CARD.findall(html):
            m = LINK.search(body)
            slug = m.group(1) if m else ""
            has_img = "<img" in body
            has_ph = "thumb-empty" in body
            label = LABEL.search(body).group(1) if LABEL.search(body) else ""
            if not has_img and not has_ph:
                naked.append((page.name, slug))
            rows.append({
                "region": page.stem, "card_type": kind, "place_id": slug,
                "has_photo": "YES" if has_img else "NO",
                "has_placeholder": "YES" if has_ph else "NO",
                "placeholder_label": label,
                "status": "HAS_PHOTO" if has_img else
                          ("FALLBACK_OK" if has_ph else "LAYOUT_RISK"),
            })

    # 참조된 이미지 파일이 실제로 배포됐는가
    for img in manifest.get("images", []):
        for role, variants in (img.get("variants") or {}).items():
            for v in variants:
                # 배포 경로는 sitePath 다. path 는 저장소 안의 원본 위치라
                # 빌드 산출물에는 없다 — 그걸 찾으면 전부 '깨짐' 으로 잡힌다.
                sp = v.get("sitePath") if isinstance(v, dict) else None
                if not sp:
                    continue
                if not (site / str(sp).lstrip("/")).exists():
                    missing_asset.append((img.get("placeId"), sp))

    out = ROOT / "MP03_PLACE_PHOTO_LAYOUT_AUDIT.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    photo = sum(1 for r in rows if r["status"] == "HAS_PHOTO")
    fb = sum(1 for r in rows if r["status"] == "FALLBACK_OK")
    print(f"가이드 장소 카드 {len(rows)} · 사진 {photo} · fallback {fb}")
    print(f"  정본 사진 보유 장소 {len(have)}")
    print(f"  자리 없이 비어 있는 카드(레이아웃 위험): {len(naked)}")
    print(f"  깨진 이미지 참조: {len(missing_asset)}")
    print(f"  → {out.name}")
    for n in naked[:10]:
        print("   !", n)
    for m in missing_asset[:5]:
        print("   !", m)
    return 1 if (naked or missing_asset) else 0


if __name__ == "__main__":
    raise SystemExit(main())
