#!/usr/bin/env python3
"""Download review copies and optimize the approved Commons sample images."""

from __future__ import annotations

import argparse
import json
import shutil
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data" / "media-catalog.json"
STAGING = ROOT / ".media-downloads"
LEGACY = {
    "barcelona-sagrada-familia-exterior": ROOT / "source/ASSETS/88_Representative_Public_Photos/01_Barcelona_Sagrada_Familia_CC_BY_SA_4_0.jpg",
    "girona-onyar-river-houses": ROOT / "source/ASSETS/88_Representative_Public_Photos/02_Girona_Onyar_Houses_CC_BY_SA_4_0.jpg",
    "nice-promenade-des-anglais": ROOT / "source/ASSETS/88_Representative_Public_Photos/03_Nice_Promenade_des_Anglais_CC_BY_SA_2_5.jpg",
}


def load_assets():
    return json.loads(CATALOG.read_text(encoding="utf-8"))["assets"]


def review_path(asset):
    return STAGING / f'{asset["id"]}.jpg'


def download(asset):
    target = review_path(asset)
    if target.exists():
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    if asset["id"] in LEGACY:
        shutil.copyfile(LEGACY[asset["id"]], target)
        return target
    request = urllib.request.Request(
        asset["downloadUrl"],
        headers={"User-Agent": "SP-FR-guidebook-media-audit/1.0 (https://github.com/jeongjae/SP-FR-guidebook)"},
    )
    with urllib.request.urlopen(request, timeout=60) as response, target.open("wb") as output:
        shutil.copyfileobj(response, output)
    return target


def make_contact_sheets(assets):
    sheets = []
    for sheet_number, start in enumerate(range(0, len(assets), 12), 1):
        subset = assets[start:start + 12]
        canvas = Image.new("RGB", (1440, 840), "#f4f1ea")
        draw = ImageDraw.Draw(canvas)
        for index, asset in enumerate(subset):
            row, col = divmod(index, 4)
            image = Image.open(review_path(asset))
            image = ImageOps.exif_transpose(image).convert("RGB")
            tile = ImageOps.fit(image, (340, 230), method=Image.Resampling.LANCZOS)
            x, y = col * 360 + 10, row * 280 + 10
            canvas.paste(tile, (x, y))
            draw.rectangle((x, y + 230, x + 340, y + 265), fill="#101820")
            draw.text((x + 7, y + 240), asset["id"], fill="white")
        path = STAGING / f"contact-sheet-{sheet_number}.jpg"
        canvas.save(path, "JPEG", quality=88, optimize=True)
        sheets.append(path)
    return sheets


def optimize(asset):
    source = review_path(asset)
    target = ROOT / asset["sourceFile"]
    target.parent.mkdir(parents=True, exist_ok=True)
    image = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    max_width = 1800 if asset["role"] == "hero" else (900 if asset["role"] == "food" else 1200)
    if image.width > max_width:
        new_height = round(image.height * max_width / image.width)
        image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
    image.save(target, "WEBP", quality=80, method=6, exif=b"", icc_profile=None)
    if image.size != (asset["width"], asset["height"]):
        raise SystemExit(f'{asset["id"]}: catalog {asset["width"]}x{asset["height"]} != output {image.width}x{image.height}')
    return target


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("review", "sizes", "optimize"))
    args = parser.parse_args()
    assets = load_assets()
    for index, asset in enumerate(assets, 1):
        path = download(asset)
        print(f"review {index:02d}/{len(assets)} {path.name}")
    if args.mode == "review":
        for path in make_contact_sheets(assets):
            print(f"contact sheet: {path.relative_to(ROOT)}")
        return
    if args.mode == "sizes":
        for asset in assets:
            image = ImageOps.exif_transpose(Image.open(review_path(asset)))
            max_width = 1800 if asset["role"] == "hero" else (900 if asset["role"] == "food" else 1200)
            output = image.size
            if image.width > max_width:
                output = (max_width, round(image.height * max_width / image.width))
            expected = (asset["width"], asset["height"])
            if output != expected:
                print(f'{asset["id"]}: catalog {expected[0]}x{expected[1]} -> actual {output[0]}x{output[1]}')
        return
    total = 0
    for asset in assets:
        target = optimize(asset)
        total += target.stat().st_size
        print(f"optimized {target.relative_to(ROOT)} ({target.stat().st_size:,} bytes)")
    print(f"optimized {len(assets)} assets, {total:,} bytes")


if __name__ == "__main__":
    main()
