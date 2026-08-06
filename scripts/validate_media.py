#!/usr/bin/env python3
"""Validate licensed media metadata, files, deployment, and references."""

import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "data" / "media-catalog.json"
SCHEMA_PATH = ROOT / "data" / "media-catalog.schema.json"
ALLOWED = {"public-domain", "cc0", "cc-by", "cc-by-sa", "unsplash",
           "pexels", "pixabay", "official-permitted"}


def main() -> int:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(catalog)
    errors = []
    ids = set()
    site_exists = (ROOT / "site").exists()
    deployed_html = ""
    if site_exists:
        deployed_html = "\n".join(
            p.read_text(encoding="utf-8") for p in (ROOT / "site").rglob("*.html"))
    legacy_assets = [asset for asset in catalog["assets"]
                     if asset.get("regionSlug") not in {"barcelona", "girona", "nice"}]
    for asset in legacy_assets:
        media_id = asset["id"]
        if media_id in ids:
            errors.append(f"duplicate id: {media_id}")
        ids.add(media_id)
        if asset["license"] not in ALLOWED:
            errors.append(f"disallowed license: {media_id}")
        if not asset["sourcePageUrl"].startswith("https://"):
            errors.append(f"non-HTTPS source page: {media_id}")
        if asset["attributionRequired"] and not asset.get("author"):
            errors.append(f"missing author: {media_id}")
        if not asset["altKo"].strip():
            errors.append(f"missing alt: {media_id}")
        source = ROOT / asset["sourceFile"]
        if not source.is_file():
            errors.append(f"missing source file: {media_id}")
            continue
        if source.suffix.lower() != ".webp" or source.read_bytes()[:4] != b"RIFF":
            errors.append(f"invalid WebP: {media_id}")
        limit = 500_000 if asset["role"] == "hero" else 300_000
        if source.stat().st_size > limit:
            errors.append(f"oversized file: {media_id} ({source.stat().st_size} bytes)")
        if asset["score"]["total"] < 75:
            errors.append(f"score below 75: {media_id}")
        if asset["status"] != "inserted":
            errors.append(f"not inserted: {media_id}")
        if site_exists:
            deployed = ROOT / "site" / asset["localPath"]
            if not deployed.is_file():
                errors.append(f"not deployed: {media_id}")
            if f'data-media-id="{media_id}"' not in deployed_html:
                errors.append(f"unused in generated HTML: {media_id}")

    if site_exists:
        forbidden = ("wikipedia.org/api/rest_v1/page/summary", "data-wiki=",
                     "upload.wikimedia.org/wikipedia/commons/")
        for token in forbidden:
            if token in deployed_html:
                errors.append(f"external image hotlink mechanism remains: {token}")

    if errors:
        print("미디어 검증 실패:")
        for error in errors:
            print(f"  - {error}")
        return 1
    total = sum((ROOT / a["sourceFile"]).stat().st_size for a in legacy_assets)
    print(f"미디어 검증: {len(ids)}개 · {total:,} bytes · 라이선스/참조/용량 이상 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
