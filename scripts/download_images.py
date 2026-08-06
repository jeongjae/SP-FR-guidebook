#!/usr/bin/env python3
"""Download approved originals and record verified dimensions and SHA-256."""

from __future__ import annotations

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


def main():
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for index, image in enumerate(payload["images"], 1):
        if image["status"] != "approved":
            raise SystemExit(f"not approved: {image['imageId']}")
        target = ROOT / image["originalPath"]
        target.parent.mkdir(parents=True, exist_ok=True)
        needs_download = not target.exists()
        if target.exists():
            try:
                with Image.open(target) as existing:
                    needs_download = ImageOps.exif_transpose(existing).size != (
                        image["originalWidth"], image["originalHeight"])
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
            raise SystemExit(f"dimension mismatch {image['imageId']}: API {expected}, file {actual}")
        image["originalSha256"] = sha256(target)
        image["originalBytes"] = target.stat().st_size
        print(f"download {index:02d}/{len(payload['images'])} {target.name} "
              f"{actual[0]}x{actual[1]} {target.stat().st_size:,} bytes")
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(payload["images"])
    print(f"downloaded {len(payload['images'])} approved originals")


if __name__ == "__main__":
    main()
