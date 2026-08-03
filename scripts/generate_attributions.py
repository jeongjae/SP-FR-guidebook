#!/usr/bin/env python3
"""Generate docs/image-attributions.md from the central media catalog."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data" / "media-catalog.json"
OUTPUT = ROOT / "docs" / "image-attributions.md"


def render() -> str:
    assets = json.loads(CATALOG.read_text(encoding="utf-8"))["assets"]
    lines = ["# 이미지 Attribution", "",
             "> 이 문서는 `data/media-catalog.json`에서 생성합니다. 수동 편집하지 않습니다.", ""]
    for region in ("barcelona", "girona", "nice"):
        lines += [f"## {region.title()}", ""]
        for asset in (a for a in assets if a["regionSlug"] == region):
            lines += [f"### {asset['subjectName']}", "",
                      f"- Media ID: `{asset['id']}`",
                      f"- File: `/{asset['localPath']}`",
                      f"- Author: {asset.get('author') or '표시 의무 없음'}",
                      f"- Source: [{asset['sourceName']}]({asset['sourcePageUrl']})",
                      f"- Original: [원본 파일]({asset['originalUrl']})",
                      f"- License: [{asset['licenseName']}]({asset.get('licenseUrl') or asset['sourcePageUrl']})",
                      f"- Modifications: {asset.get('modificationNote') or '없음'}",
                      "- Used in:"]
            lines += [f"  - `/{page}`" for page in asset["usagePages"]]
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            print("Attribution 문서가 카탈로그와 다릅니다.")
            return 1
        print("Attribution 문서: 카탈로그와 일치")
        return 0
    OUTPUT.write_text(expected, encoding="utf-8")
    print(f"Attribution 문서 생성: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
