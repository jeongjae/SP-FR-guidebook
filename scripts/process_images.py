#!/usr/bin/env python3
"""Create responsive hero, content and thumbnail WebP derivatives."""

from __future__ import annotations

import argparse
import hashlib
import csv
import json
import shutil
from pathlib import Path

from PIL import Image, ImageCms, ImageOps


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data/images/image-manifest.json"
PHOTO_ROOT = ROOT / "source/ASSETS/photos"
PROCESSED = PHOTO_ROOT / "processed"
METADATA = PHOTO_ROOT / "metadata/image-manifest.json"
LOG = PHOTO_ROOT / "metadata/process-log.json"
MANIFEST_CSV = ROOT / "data/images/image-manifest.csv"
HERO_WIDTHS = (800, 1280, 1920)
QUALITY = {"hero": 80, "content": 78, "thumbnail": 73}
BYTE_LIMIT = {"hero": 450_000, "content": 300_000, "thumbnail": 80_000}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def srgb_image(source):
    image = ImageOps.exif_transpose(source)
    icc = image.info.get("icc_profile")
    if icc:
        try:
            input_profile = ImageCms.ImageCmsProfile(__import__("io").BytesIO(icc))
            output_profile = ImageCms.createProfile("sRGB")
            image = ImageCms.profileToProfile(image, input_profile, output_profile,
                                              outputMode="RGB")
        except Exception:
            image = image.convert("RGB")
    else:
        image = image.convert("RGB")
    return image


def crop_box(size, ratio, focus):
    width, height = size
    target_ratio = ratio[0] / ratio[1]
    if width / height > target_ratio:
        crop_h = height
        crop_w = round(height * target_ratio)
    else:
        crop_w = width
        crop_h = round(width / target_ratio)
    center_x = focus["x"] * width
    center_y = focus["y"] * height
    left = min(max(0, round(center_x - crop_w / 2)), width - crop_w)
    top = min(max(0, round(center_y - crop_h / 2)), height - crop_h)
    return left, top, left + crop_w, top + crop_h


def save_under_limit(image, target, role):
    target.parent.mkdir(parents=True, exist_ok=True)
    limit = BYTE_LIMIT[role]
    for quality in range(QUALITY[role], 44, -3):
        image.save(target, "WEBP", quality=quality, method=6, exif=b"")
        if target.stat().st_size <= limit:
            return quality
    return quality


def variant(image, image_id, role, width, height=None, focus=None):
    if height is not None:
        box = crop_box(image.size, (width, height), focus)
        cropped = image.crop(box)
        if cropped.width < width or cropped.height < height:
            return None
        output = cropped.resize((width, height), Image.Resampling.LANCZOS)
    else:
        if image.width > width:
            output = image.resize((width, round(image.height * width / image.width)),
                                  Image.Resampling.LANCZOS)
        else:
            output = image.copy()
            width = output.width
    folder = "thumbnails" if role == "thumbnail" else role
    role_name = "thumb" if role == "thumbnail" else role
    target = PROCESSED / folder / f"{image_id}-{role_name}-{width}.webp"
    quality = save_under_limit(output, target, role)
    if target.stat().st_size > BYTE_LIMIT[role] and role == "hero" and width >= 1920:
        # Extremely detailed frames may not fit the byte budget even at the
        # quality floor; serve up to 1280 instead of shipping an oversize file.
        target.unlink()
        return None
    return {
        "path": str(target.relative_to(ROOT)).replace("\\", "/"),
        "sitePath": f"assets/images/{folder}/{target.name}",
        "width": output.width, "height": output.height,
        "bytes": target.stat().st_size, "sha256": sha256(target), "quality": quality,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default="2026-08-05")
    args = parser.parse_args()
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    log = []
    for item in payload["images"]:
        source_path = ROOT / item["originalPath"]
        if not item.get("originalSha256") or sha256(source_path) != item["originalSha256"]:
            raise SystemExit(f"original hash missing/mismatch: {item['imageId']}")
        with Image.open(source_path) as source:
            image = srgb_image(source)
        variants = {"hero": [], "content": [], "thumbnail": []}
        # Hero variants are only rendered for day/region heroes; majors and
        # supporting images use content/thumbnail, so skipping their hero set
        # keeps the deployed and PWA-precached payload lean.
        if item["role"] == "hero" or item.get("regionHero"):
            for width in HERO_WIDTHS:
                made = variant(image, item["imageId"], "hero", width, round(width * 9 / 16), item["focus"])
                if made:
                    variants["hero"].append(made)
        # Extremely detailed frames can exceed the content byte budget even at
        # the quality floor; step the width down until the file fits.
        for content_width in (1280, 1080, 960):
            made = variant(image, item["imageId"], "content", content_width)
            if made and made["bytes"] <= BYTE_LIMIT["content"]:
                variants["content"].append(made)
                break
            if made:
                (ROOT / made["path"]).unlink()
        made = variant(image, item["imageId"], "thumbnail", 480, 320, item["focus"])
        if made:
            variants["thumbnail"].append(made)
        if not variants["content"] or not variants["thumbnail"]:
            raise SystemExit(f"required derivative missing: {item['imageId']}")
        item["variants"] = variants
        item["status"] = "processed"
        row = {"imageId": item["imageId"], "source": item["originalPath"],
               "originalSize": list(image.size), "variants": variants}
        log.append(row)
        print(f"processed {item['imageId']}: "
              f"{sum(len(value) for value in variants.values())} variants")
    payload["processedAt"] = args.date
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = ["imageId", "placeId", "title", "source", "sourcePage", "originalFile",
              "creator", "license", "licenseUrl", "changes", "downloadDate", "originalWidth",
              "originalHeight", "originalPath", "originalSha256", "usage", "role", "status"]
    with MANIFEST_CSV.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for item in payload["images"]:
            writer.writerow({**{field: item.get(field, "") for field in fields},
                             "usage": ";".join(item["usage"])})
    METADATA.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(MANIFEST, METADATA)
    LOG.write_text(json.dumps({"processedAt": args.date, "images": log},
                              ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"processed {len(payload['images'])} originals")


if __name__ == "__main__":
    main()
