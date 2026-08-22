#!/usr/bin/env python3
"""대기열의 Commons 사진을 카탈로그에 넣는다.

    python3 scripts/add_commons_photo.py            # data/images/photo-queue.json
    python3 scripts/add_commons_photo.py --dry-run

`process_images.py` 는 카탈로그 전체를 다시 인코딩한다. 사진 몇 장을 넣으려고
162장을 다시 만들면 저장소가 통째로 바뀌고 무엇이 새로 들어왔는지 diff 에서
안 보인다. 그래서 **대기열의 것만** 같은 규칙으로 처리한다 — 크기·품질·
바이트 상한·SHA 기록은 process_images 의 함수를 그대로 쓴다.

무엇을 넣을지는 코드가 아니라 `data/images/photo-queue.json` 이 정한다.
지역이 늘어도 이 파일만 늘고 스크립트는 그대로다.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
import tempfile
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import process_images as pi  # noqa: E402

QUEUE = ROOT / "data/images/photo-queue.json"
MANIFEST = ROOT / "data/images/image-manifest.json"
MANIFEST_CSV = ROOT / "data/images/image-manifest.csv"
METADATA = ROOT / "source/ASSETS/photos/metadata/image-manifest.json"
ORIGINALS = ROOT / "source/ASSETS/photos/originals"
USER_AGENT = "SP-FR-guidebook/1.0 (https://github.com/jeongjae/SP-FR-guidebook)"
MAX_SIDE = 4000

REQUIRED = ("imageId", "placeId", "region", "originalFile", "creator", "license",
            "licenseUrl", "originalWidth", "originalHeight", "altKo",
            "identityEvidence", "verifiedAt")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(entry: dict) -> Path:
    """원본을 받아 치수를 대조한다. 어긋나면 다른 파일을 받은 것이다."""
    target = ORIGINALS / f"{entry['imageId']}.jpg"
    target.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(entry["originalFile"],
                                     headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=180) as response:
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as tmp:
            shutil.copyfileobj(response, tmp)
            tmp_path = Path(tmp.name)
    tmp_path.replace(target)
    with Image.open(target) as source:
        actual = ImageOps.exif_transpose(source).size
    expected = (entry["originalWidth"], entry["originalHeight"])
    if actual != expected:
        raise SystemExit(f"치수 불일치 {entry['imageId']}: API {expected}, 파일 {actual}")
    # 저장소를 가볍게 유지한다. 참 원본은 originalFile 로 다시 받을 수 있다.
    with Image.open(target) as source:
        image = ImageOps.exif_transpose(source)
        if max(image.size) > MAX_SIDE:
            ratio = MAX_SIDE / max(image.size)
            image = image.resize(
                (round(image.width * ratio), round(image.height * ratio)),
                Image.Resampling.LANCZOS)
            image.convert("RGB").save(target, "JPEG", quality=88)
            entry["storedWidth"], entry["storedHeight"] = image.size
    return target


def build_variants(item: dict) -> dict:
    with Image.open(ROOT / item["originalPath"]) as source:
        image = pi.srgb_image(source)
        variants = {"hero": [], "content": [], "thumbnail": []}
        for width in (1280, 1080, 960):
            made = pi.variant(image, item["imageId"], "content", width)
            if made and made["bytes"] <= pi.BYTE_LIMIT["content"]:
                variants["content"].append(made)
                break
            if made:
                (ROOT / made["path"]).unlink()
        made = pi.variant(image, item["imageId"], "thumbnail", 480, 320,
                          item["focus"])
        if made:
            variants["thumbnail"].append(made)
    if not variants["content"] or not variants["thumbnail"]:
        raise SystemExit(f"필수 파생본 없음: {item['imageId']}")
    return variants


def write_catalog(payload: dict) -> None:
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    fields = ["imageId", "placeId", "title", "source", "sourcePage", "originalFile",
              "creator", "license", "licenseUrl", "changes", "downloadDate",
              "originalWidth", "originalHeight", "originalPath", "originalSha256",
              "usage", "role", "status"]
    with MANIFEST_CSV.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for img in payload["images"]:
            writer.writerow({**{f: img.get(f, "") for f in fields},
                             "usage": ";".join(img.get("usage", []))})
    METADATA.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(MANIFEST, METADATA)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    queue = json.loads(QUEUE.read_text(encoding="utf-8"))["queue"]
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    known = {img["imageId"] for img in payload["images"]}

    added = []
    for entry in queue:
        missing = [k for k in REQUIRED if not entry.get(k)]
        if missing:
            raise SystemExit(f"{entry.get('imageId')}: 필수 항목 누락 — {missing}")
        if entry["imageId"] in known:
            print(f"이미 있다 — 건너뛴다: {entry['imageId']}")
            continue
        if args.dry_run:
            print(f"받을 것: {entry['imageId']} ← {entry['commonsTitle']}")
            continue
        path = download(entry)
        item = {
            **{k: entry[k] for k in
               ("imageId", "placeId", "region", "creator", "license",
                "licenseCode", "licenseUrl", "originalFile", "originalWidth",
                "originalHeight", "altKo", "captionKo", "titleKo")
               if k in entry},
            "title": entry["commonsTitle"],
            "description": entry.get("identityEvidence", ""),
            "source": "Wikimedia Commons",
            "sourcePage": "https://commons.wikimedia.org/wiki/File:"
                          + entry["commonsTitle"].replace(" ", "_"),
            "changes": ("EXIF orientation corrected; resized and converted to "
                        "WebP; metadata removed"),
            "downloadDate": entry["verifiedAt"],
            "originalPath": str(path.relative_to(ROOT)).replace("\\", "/"),
            "originalSha256": sha256(path),
            "originalBytes": path.stat().st_size,
            "focus": entry.get("focus") or {"x": 0.5, "y": 0.5},
            "regionHero": False,
            "role": entry.get("role", "major"),
            "usage": entry.get("usage") or [
                f"guide/{entry['region']}.html",
                f"places/{entry['placeId']}.html"],
            "selectionScore": entry.get("selectionScore", 90),
        }
        for key in ("storedWidth", "storedHeight"):
            if key in entry:
                item[key] = entry[key]
        item["variants"] = build_variants(item)
        item["status"] = "processed"
        payload["images"].append(item)
        added.append(item)
        print(f"추가 {item['imageId']} · {item['license']} · {item['creator']}")

    if added and not args.dry_run:
        write_catalog(payload)
        print(f"카탈로그 {len(payload['images'])}장 (신규 {len(added)}장)")
    elif not added:
        print("새로 넣을 것이 없다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
