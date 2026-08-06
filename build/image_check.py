#!/usr/bin/env python3
"""Validate the responsive photo pipeline, generated HTML and performance."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data/images/image-manifest.json"
SITE = ROOT / "site"
PROCESSED = ROOT / "source/ASSETS/photos/processed"
ORIGINALS = ROOT / "source/ASSETS/photos/originals"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-(?:hero|content|thumb)-\d+\.webp$")
LIMITS = {"hero": 450_000, "content": 300_000, "thumbnail": 80_000}
AVERAGE_LIMITS = {"hero": 400_000, "content": 250_000, "thumbnail": 60_000}


def main():
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    images = payload.get("images", [])
    errors, ids, declared_processed, declared_originals = [], set(), set(), set()
    html_text = ""
    if SITE.exists():
        html_text = "\n".join(path.read_text(encoding="utf-8") for path in SITE.rglob("*.html"))

    role_sizes = {key: [] for key in LIMITS}
    for item in images:
        image_id = item["imageId"]
        if image_id in ids:
            errors.append(f"duplicate imageId: {image_id}")
        ids.add(image_id)
        original = ROOT / item["originalPath"]
        declared_originals.add(original.resolve())
        if not original.is_file():
            errors.append(f"missing original: {image_id}")
            continue
        with Image.open(original) as source:
            source_size = source.size
        for role, variants in item["variants"].items():
            if role in {"content", "thumbnail"} and not variants:
                errors.append(f"required {role} missing: {image_id}")
            for variant in variants:
                path = ROOT / variant["path"]
                declared_processed.add(path.resolve())
                if not path.is_file():
                    errors.append(f"missing derivative: {variant['path']}")
                    continue
                if not NAME_RE.fullmatch(path.name):
                    errors.append(f"invalid derivative filename: {path.name}")
                if path.suffix != ".webp" or path.read_bytes()[:4] != b"RIFF":
                    errors.append(f"invalid WebP: {path.name}")
                with Image.open(path) as rendered:
                    actual = rendered.size
                if actual != (variant["width"], variant["height"]):
                    errors.append(f"dimension metadata mismatch: {path.name}")
                if actual[0] > source_size[0] or actual[1] > source_size[1]:
                    errors.append(f"upscaled derivative: {path.name}")
                size = path.stat().st_size
                role_sizes[role].append(size)
                if size > LIMITS[role]:
                    errors.append(f"oversized {role}: {path.name} {size}")
                if SITE.exists():
                    deployed = SITE / variant["sitePath"]
                    if not deployed.is_file():
                        errors.append(f"not deployed: {variant['sitePath']}")
        if SITE.exists():
            if f'data-photo-id="{image_id}"' not in html_text:
                errors.append(f"manifest image unused in HTML: {image_id}")
            if item["altKo"] not in html_text:
                errors.append(f"alt text unused in HTML: {image_id}")
            credit = SITE / "about/photo-credits.html"
            if not credit.is_file() or f'id="{image_id}"' not in credit.read_text(encoding="utf-8"):
                errors.append(f"credit anchor missing: {image_id}")

    actual_processed = {path.resolve() for path in PROCESSED.rglob("*") if path.is_file()}
    actual_originals = {path.resolve() for path in ORIGINALS.rglob("*") if path.is_file()}
    for path in sorted(actual_processed - declared_processed):
        errors.append(f"derivative without manifest: {path.relative_to(ROOT)}")
    for path in sorted(actual_originals - declared_originals):
        errors.append(f"original without manifest: {path.relative_to(ROOT)}")

    for role, values in role_sizes.items():
        if values and sum(values) / len(values) > AVERAGE_LIMITS[role]:
            errors.append(f"{role} average exceeds limit: {sum(values) // len(values)}")

    if SITE.exists():
        for token in ("비공개 숙소 근사 권역", "B%C3%A0scara"):
            if token in html_text:
                errors.append("private accommodation exact address exposed in generated HTML")
        hero_days = sorted({
            int(match.group(1))
            for item in images if item.get("role") == "hero"
            for usage in item.get("usage", [])
            if (match := re.fullmatch(r"daily/day-(\d+)\.html", usage))})
        for day in hero_days:
            page = SITE / f"daily/day-{day:02d}.html"
            text = page.read_text(encoding="utf-8")
            if 'class="guide-photo guide-photo--hero"' not in text:
                errors.append(f"Day {day}: hero photo missing")
            if not re.search(r'<img[^>]+width="\d+"[^>]+height="\d+"[^>]+loading="eager"', text):
                errors.append(f"Day {day}: eager hero dimensions/loading missing")
            # Initial transfer estimate: HTML + shared CSS/JS + eager image only.
            shared = [SITE / "assets/style.css", SITE / "assets/data.js",
                      SITE / "assets/nav.js", SITE / "assets/pwa.js"]
            initial = page.stat().st_size + sum(path.stat().st_size for path in shared)
            eager = re.search(r'<img src="\.\./([^"]+)"[^>]+loading="eager"', text)
            if eager and (SITE / eager.group(1)).is_file():
                initial += (SITE / eager.group(1)).stat().st_size
            if initial > 2_000_000:
                errors.append(f"Day {day}: estimated initial transfer {initial} > 2MB")

    if errors:
        print("image validation failed:")
        for error in errors[:80]:
            print("  -", error)
        return 1
    total = sum(role_sizes[role][i] for role in role_sizes for i in range(len(role_sizes[role])))
    averages = " · ".join(f"{role} avg {sum(values)//len(values):,}B"
                           for role, values in role_sizes.items() if values)
    print(f"image validation: {len(ids)} originals · {len(declared_processed)} derivatives · "
          f"{total:,} bytes · {averages} · errors 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
