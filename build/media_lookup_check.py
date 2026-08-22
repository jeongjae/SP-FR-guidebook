#!/usr/bin/env python3
"""사진이 저장소에 있으면서 화면에 안 나오는 일을 막는다.

    python3 build/media_lookup_check.py

사진 카탈로그의 `placeId` 는 장소 명부의 슬러그가 아니다. 사진 프로그램이
명부보다 먼저 '주제 키'(socca · monaco-ville · versailles-gardens)로 사진을
모았고, 명부는 그 뒤에 다른 이름 공간으로 자랐다. 두 이름이 의미가 달라
문자열 정규화로는 이어지지 않는다 — 사람이 사진 설명을 읽고 판정해야 한다.
판정의 정본은 `data/images/place-aliases.json` 하나다.

이 검사가 세우는 것:

  1 별칭표에 없는 placeId (unmapped)              → 0 이어야 한다
  2 잇혀 있는데 배포본 어디에도 안 나오는 사진      → 0 이어야 한다

'명부에 없는 장소'(unregistered)는 실패가 아니라 **선언된 잔여분**이다.
장소로 승격해야 화면에 올라간다 — 세어서 보여 준다.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = Path(os.environ.get("SPFR_SITE_DIR") or (ROOT / "site"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import model  # noqa: E402


def rendered_image_ids() -> set[str]:
    """배포본이 실제로 거는 사진. 파일 이름에 imageId 가 들어 있다."""
    ids: set[str] = set()
    manifest = json.loads(model.IMAGE_MANIFEST.read_text(encoding="utf-8"))
    images = manifest if isinstance(manifest, list) else manifest.get("images", [])
    by_id = {img["imageId"]: img for img in images if img.get("imageId")}
    pages = "\n".join(p.read_text(encoding="utf-8")
                      for p in SITE.rglob("*.html"))
    for image_id in by_id:
        if image_id in pages:
            ids.add(image_id)
    return ids


def check(trip) -> tuple[list[str], dict]:
    known = set(trip.places) | {r.slug for r in trip.regions}
    idx = model.load_images(known)
    manifest = json.loads(model.IMAGE_MANIFEST.read_text(encoding="utf-8"))
    images = manifest if isinstance(manifest, list) else manifest.get("images", [])

    linked: set[str] = set()
    for img in idx["by_place"].values():
        linked.add(img["imageId"])
    for rows in idx["extras"].values():
        linked.update(img["imageId"] for img in rows)
    for rows in idx["dishes"].values():
        linked.update(img["imageId"] for img in rows)
    for img in idx["heroes"].values():
        linked.add(img["imageId"])

    unregistered = {x.get("imageId") for x in idx["unregistered"]}
    rendered = rendered_image_ids()

    problems = []
    for row in idx["unmapped"]:
        problems.append(
            f"별칭표에 없는 placeId — {row['placeId']} ({row['imageId']}). "
            f"data/images/place-aliases.json 에 판정을 적는다")

    silent = sorted(linked - rendered)
    for image_id in silent:
        problems.append(f"잇혔는데 화면에 안 나오는 사진 — {image_id}")

    stats = {
        "catalog": len(images),
        "linked": len(linked),
        "rendered": len(linked & rendered),
        "unmapped": len(idx["unmapped"]),
        "silent": len(silent),
        "unregistered": len(unregistered),
        "dishes": sum(len(v) for v in idx["dishes"].values()),
        "extras": sum(len(v) for v in idx["extras"].values()),
    }
    return problems, stats


def main() -> int:
    trip = model.load_trip()
    problems, stats = check(trip)
    print("사진 연결 검사")
    for key, label in (("catalog", "카탈로그"), ("linked", "장소·지역에 연결"),
                       ("rendered", "배포본에 실제로 나오는 것"),
                       ("extras", "  그중 장소 갤러리"), ("dishes", "  그중 요리 사진"),
                       ("unmapped", "별칭표에 없는 placeId (목표 0)"),
                       ("silent", "잇혔는데 안 나오는 사진 (목표 0)"),
                       ("unregistered", "명부 미등재 장소 — 선언된 잔여분")):
        print(f"  {label:34s} {stats[key]}")
    if problems:
        print(f"\n실패 {len(problems)}건:")
        for p in problems[:30]:
            print("  " + p)
        return 1
    print("\n사진 연결 검사 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
