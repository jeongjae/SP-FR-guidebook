#!/usr/bin/env python3
"""Generate the reviewable Markdown credit ledger from the photo manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data/images/image-manifest.json"
OUTPUT = ROOT / "docs/photo-content/04_barcelona_photo_credits.md"


def render():
    images = json.loads(MANIFEST.read_text(encoding="utf-8"))["images"]
    lines = ["# Barcelona Pilot 사진 크레딧", "",
             "> `data/images/image-manifest.json`에서 자동 생성합니다. 수동 편집하지 않습니다.", ""]
    for image in images:
        lines += [f"## {image['titleKo']}", "", f"<a id=\"{image['imageId']}\"></a>", "",
                  f"- Image ID: `{image['imageId']}`", f"- Place ID: `{image['placeId']}`",
                  f"- Photo: {image['creator']}", f"- Source: [Wikimedia Commons]({image['sourcePage']})",
                  f"- Original: [원본 파일]({image['originalFile']})",
                  f"- License: [{image['license']}]({image['licenseUrl']})",
                  f"- Changes: {image['changes']}", "- Used in:"]
        lines += [f"  - `/{usage}`" for usage in image["usage"]]
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            print("photo credits Markdown is stale")
            return 1
        print("photo credits Markdown: manifest match")
        return 0
    OUTPUT.write_text(expected, encoding="utf-8")
    print(f"generated {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
