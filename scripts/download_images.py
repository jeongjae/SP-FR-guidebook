#!/usr/bin/env python3
"""Download approved originals and record verified dimensions and SHA-256.

From Batch 1 onward, freshly downloaded originals are stored downscaled to a
maximum long side (default 4000px) to keep the repository small. The Commons
dimensions stay in originalWidth/originalHeight; the stored file's dimensions
are recorded in storedWidth/storedHeight. The true original remains
retrievable via originalFile. Files that already exist (Pilot) are untouched.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import tempfile
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data/images/image-manifest.json"
MANIFEST_CSV = ROOT / "data/images/image-manifest.csv"
USER_AGENT = "SP-FR-guidebook-photo-pilot/1.0 (https://github.com/jeongjae/SP-FR-guidebook)"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(images):
    fields = ["imageId", "placeId", "title", "source", "sourcePage", "originalFile",
              "creator", "license", "licenseUrl", "changes", "downloadDate", "originalWidth",
              "originalHeight", "originalPath", "originalSha256", "usage", "role", "status"]
    with MANIFEST_CSV.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for image in images:
            writer.writerow({**{field: image.get(field, "") for field in fields},
                             "usage": ";".join(image["usage"])})


def stored_size(image):
    if image.get("storedWidth") and image.get("storedHeight"):
        return image["storedWidth"], image["storedHeight"]
    return image["originalWidth"], image["originalHeight"]


def downscale(target, image, max_side):
    """Store the original at a bounded long side; record the stored dimensions."""
    with Image.open(target) as source:
        upright = ImageOps.exif_transpose(source)
        if max(upright.size) <= max_side:
            return upright.size, False
        scale = max_side / max(upright.size)
        new_size = (round(upright.width * scale), round(upright.height * scale))
        resized = upright.convert("RGB").resize(new_size, Image.Resampling.LANCZOS)
        icc = upright.info.get("icc_profile")
    save_kwargs = {"quality": 95, "optimize": True}
    if icc:
        save_kwargs["icc_profile"] = icc
    if target.suffix.lower() in {".png", ".tif", ".tiff"}:
        resized.save(target, "PNG", optimize=True,
                     **({"icc_profile": icc} if icc else {}))
    else:
        resized.save(target, "JPEG", **save_kwargs)
    return new_size, True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-side", type=int, default=4000,
                        help="downscale freshly downloaded originals to this long side (0 disables)")
    args = parser.parse_args()
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for index, image in enumerate(payload["images"], 1):
        if image["status"] not in {"approved", "processed"}:
            raise SystemExit(f"not approved: {image['imageId']}")
        target = ROOT / image["originalPath"]
        target.parent.mkdir(parents=True, exist_ok=True)
        needs_download = not target.exists()
        if target.exists():
            try:
                with Image.open(target) as existing:
                    needs_download = ImageOps.exif_transpose(existing).size != stored_size(image)
            except Exception:
                needs_download = True
        if needs_download:
            request = urllib.request.Request(image["originalFile"], headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=120) as response:
                with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as tmp:
                    shutil.copyfileobj(response, tmp)
                    tmp_path = Path(tmp.name)
            tmp_path.replace(target)
            try:
                with Image.open(target) as source:
                    actual = ImageOps.exif_transpose(source).size
            except Exception as exc:
                raise SystemExit(f"invalid image {image['imageId']}: {exc}") from exc
            expected = (image["originalWidth"], image["originalHeight"])
            if actual != expected:
                raise SystemExit(
                    f"dimension mismatch {image['imageId']}: API {expected}, file {actual}")
            if args.max_side:
                (stored_w, stored_h), reduced = downscale(target, image, args.max_side)
                if reduced:
                    image["storedWidth"], image["storedHeight"] = stored_w, stored_h
                    note = f"original stored downscaled to max {args.max_side}px"
                    if note not in image["changes"]:
                        image["changes"] = f"{image['changes']}; {note}"
        try:
            with Image.open(target) as source:
                actual = ImageOps.exif_transpose(source).size
        except Exception as exc:
            raise SystemExit(f"invalid image {image['imageId']}: {exc}") from exc
        expected = stored_size(image)
        if actual != expected:
            raise SystemExit(f"dimension mismatch {image['imageId']}: stored {expected}, file {actual}")
        image["originalSha256"] = sha256(target)
        image["originalBytes"] = target.stat().st_size
        print(f"download {index:02d}/{len(payload['images'])} {target.name} "
              f"{actual[0]}x{actual[1]} {target.stat().st_size:,} bytes")
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(payload["images"])
    print(f"downloaded {len(payload['images'])} approved originals")


if __name__ == "__main__":
    main()
