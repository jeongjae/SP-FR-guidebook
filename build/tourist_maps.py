"""관광 조망지도 원본을 저장소에 넣을 WebP 로 줄인다.

원본 PDF·JPG 는 다 합쳐 316MB 다. 저장소에 넣지 않는다 — 대신
scripts/render_tourist_maps.sh 가 각 지도의 '지도 면' 한 쪽만 큰 JPEG 로
뽑아 두면, 이 스크립트가 광고 테두리를 잘라 내고 방향을 바로 세워
source/ASSETS/tourist-maps/<region>/<slug>.webp 로 저장한다.

    python3 build/tourist_maps.py <뽑아 둔 JPEG 폴더>

무엇을 어디서 몇 쪽을 뽑았는지는 scripts/tourist_maps_pages.tsv 에,
누가 발행했고 어떤 권리인지는 data/tourist-maps.json 에 있다. 이 스크립트는
그중 '그림을 어떻게 손보는가' 만 안다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "tourist-maps.json"
OUT_ROOT = ROOT / "source" / "ASSETS" / "tourist-maps"

LONG_EDGE = 2600     # 휴대폰에서 확대해도 지명이 읽히는 선
QUALITY = 72         # WebP. 지도는 평면 색이라 사진보다 잘 줄어든다

# 원본 한 장이 지도 하나가 아닌 경우. 비율로 자른다 — 렌더 해상도가 바뀌어도
# 따라온다. rotate 는 반시계 방향 각도(PIL 규약).
#   crop:   (left, top, right, bottom) — 0~1
#   rotate: 90 / 180 / -90
ADJUST: dict[str, dict] = {
    # 광고 10칸 접지 한복판에 지도가 옆으로 누워 있다
    "lyon": {"crop": (0.345, 0.345, 1.0, 0.672), "rotate": -90},
    # 좌우로 광고와 안내문이 둘린 다면 접지
    "marseille": {"crop": (0.322, 0.163, 0.775, 1.0)},
    "saint-remy-de-provence": {"crop": (0.128, 0.118, 0.830, 0.878)},
}


def entries() -> list[dict]:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    out = []
    for region, maps in data["regions"].items():
        for m in maps:
            out.append({**m, "region": region})
    return out


def shape(im: Image.Image, slug: str) -> Image.Image:
    adj = ADJUST.get(slug) or {}
    if box := adj.get("crop"):
        w, h = im.size
        l, t, r, b = box
        im = im.crop((round(w * l), round(h * t), round(w * r), round(h * b)))
    if angle := adj.get("rotate"):
        im = im.rotate(angle, expand=True)
    w, h = im.size
    if max(w, h) > LONG_EDGE:
        s = LONG_EDGE / max(w, h)
        im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    return im


def main(src_dir: Path) -> int:
    made, missing, total = [], [], 0
    for e in entries():
        src = src_dir / f"{e['slug']}.jpg"
        if not src.exists():
            missing.append(e["slug"])
            continue
        dest = OUT_ROOT / e["region"] / f"{e['slug']}.webp"
        dest.parent.mkdir(parents=True, exist_ok=True)
        im = shape(Image.open(src).convert("RGB"), e["slug"])
        im.save(dest, "WEBP", quality=QUALITY, method=6)
        size = dest.stat().st_size
        total += size
        made.append((e["slug"], im.size, size))
        print(f"  {e['slug']:<26} {im.size[0]:>5}x{im.size[1]:<5} {size // 1024:>5} KB")

    print(f"\n  {len(made)}장 · {total / 1e6:.1f} MB")
    if missing:
        print("\n  뽑아 둔 JPEG 이 없다 (scripts/render_tourist_maps.sh 먼저):")
        for slug in missing:
            print(f"    {slug}")
    return 0 if made and not missing else (0 if made else 1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    raise SystemExit(main(Path(sys.argv[1])))
