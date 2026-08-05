#!/usr/bin/env python3
"""Detect exact and near-duplicate approved originals."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data/images/image-manifest.json"


def dhash(path):
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source).convert("L").resize((17, 16), Image.Resampling.LANCZOS)
    value = 0
    for y in range(16):
        for x in range(16):
            value = (value << 1) | int(image.getpixel((x, y)) > image.getpixel((x + 1, y)))
    return value


def main():
    images = json.loads(MANIFEST.read_text(encoding="utf-8"))["images"]
    errors = []
    for i, left in enumerate(images):
        for right in images[i + 1:]:
            if left.get("originalSha256") == right.get("originalSha256"):
                errors.append(f"exact duplicate: {left['imageId']} / {right['imageId']}")
    hashes = [(item["imageId"], dhash(ROOT / item["originalPath"])) for item in images]
    for i, (left_id, left_hash) in enumerate(hashes):
        for right_id, right_hash in hashes[i + 1:]:
            distance = (left_hash ^ right_hash).bit_count()
            if distance <= 10:
                errors.append(f"near duplicate (dHash {distance}): {left_id} / {right_id}")
    if errors:
        print("duplicate validation failed:")
        for error in errors:
            print("  -", error)
        return 1
    print(f"duplicate validation: {len(images)} originals · exact/near duplicates 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
