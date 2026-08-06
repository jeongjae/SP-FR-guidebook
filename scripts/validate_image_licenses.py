#!/usr/bin/env python3
"""Fail on incomplete, disallowed or internally inconsistent photo licenses."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data/images/image-manifest.json"
ITINERARY = ROOT / "data/itinerary-places.json"
MEDIA_CATALOG = ROOT / "data/media-catalog.json"
REQUIRED = {"imageId", "placeId", "title", "source", "sourcePage", "originalFile",
            "creator", "license", "licenseUrl", "changes", "downloadDate", "usage",
            "role", "status", "altKo", "captionKo", "originalWidth", "originalHeight",
            "originalPath", "originalSha256", "variants"}
ALLOWED = {"public-domain", "cc0", "cc-by", "cc-by-sa"}


def main():
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    itinerary = json.loads(ITINERARY.read_text(encoding="utf-8"))
    place_visibility = {}
    for day in itinerary["days"]:
        for place in day["places"]:
            place_visibility[place["id"]] = place["visibility"]
    # Verified media-catalog subjects (registry spots and regional foods that
    # already carried reviewed images) are valid photo subjects too.
    catalog = json.loads(MEDIA_CATALOG.read_text(encoding="utf-8"))
    catalog_subjects = set()
    for asset in catalog.get("assets", []):
        if asset.get("placeSlug"):
            catalog_subjects.add(asset["placeSlug"])
        else:
            catalog_subjects.add(asset["id"].removeprefix(asset["regionSlug"] + "-"))
    errors, ids = [], set()
    for image in payload.get("images", []):
        missing = sorted(field for field in REQUIRED if not image.get(field))
        if missing:
            errors.append(f"{image.get('imageId', '<missing>')}: missing {', '.join(missing)}")
        image_id = image.get("imageId")
        if image_id in ids:
            errors.append(f"duplicate imageId: {image_id}")
        ids.add(image_id)
        if image.get("licenseCode") not in ALLOWED:
            errors.append(f"disallowed license: {image_id} {image.get('license')}")
        if not image.get("sourcePage", "").startswith("https://commons.wikimedia.org/wiki/File:"):
            errors.append(f"not a Commons file-description page: {image_id}")
        if not image.get("originalFile", "").startswith("https://upload.wikimedia.org/"):
            errors.append(f"not an original Commons upload URL: {image_id}")
        if place_visibility.get(image.get("placeId")) == "private":
            errors.append(f"private place image: {image_id}")
        if (image.get("placeId") not in place_visibility
                and image.get("placeId") not in catalog_subjects):
            errors.append(f"placeId absent from itinerary inventory: {image_id}")
    if errors:
        print("license validation failed:")
        for error in errors:
            print("  -", error)
        return 1
    print(f"license validation: {len(ids)} approved images · missing 0 · private 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
