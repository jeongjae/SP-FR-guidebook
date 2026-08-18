#!/usr/bin/env python3
"""Collect Commons candidates and create an approved photo manifest.

Only file-description metadata returned by the Wikimedia Commons API is used.
The search plan pins the reviewed file title; search results supply two
alternatives for the audit trail and never silently replace the reviewed file.
With --merge, existing candidates and manifest entries from earlier batches
are preserved and entries for the plan's places are replaced in place.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data/images"
DEFAULT_PLAN = DATA / "barcelona-search-plan.json"
API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "SP-FR-guidebook-photo-pilot/1.0 (https://github.com/jeongjae/SP-FR-guidebook)"


def api(params):
    query = urllib.parse.urlencode({"format": "json", "formatversion": 2, **params})
    request = urllib.request.Request(f"{API}?{query}", headers={"User-Agent": USER_AGENT})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = json.load(response)
            time.sleep(1)
            return payload
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == 4:
                raise
            time.sleep(10 * (attempt + 1))


def clean(value):
    text = html.unescape(re.sub(r"<[^>]+>", " ", str(value or "")))
    return re.sub(r"\s+", " ", text).strip()


def normalized_license(short_name):
    name = clean(short_name).upper().replace("CREATIVE COMMONS", "CC")
    if "PUBLIC DOMAIN" in name or name in {"PD", "PDM"}:
        return "Public Domain", "public-domain"
    if "CC0" in name:
        return "CC0 1.0", "cc0"
    if "CC BY-SA" in name:
        match = re.search(r"CC BY-SA(?: |-|_)?([0-9.]+)", name)
        version = match.group(1) if match else ""
        return f"CC BY-SA {version}".strip(), "cc-by-sa"
    if "CC BY" in name:
        match = re.search(r"CC BY(?: |-|_)?([0-9.]+)", name)
        version = match.group(1) if match else ""
        return f"CC BY {version}".strip(), "cc-by"
    return clean(short_name) or "Unknown", "unknown"


def image_info(titles):
    payload = api({
        "action": "query", "prop": "imageinfo", "titles": "|".join(titles),
        "iiprop": "url|size|extmetadata", "iiurlwidth": 1920,
    })
    out = {}
    for page in payload.get("query", {}).get("pages", []):
        if page.get("missing") or not page.get("imageinfo"):
            continue
        info = page["imageinfo"][0]
        meta = {key: clean(value.get("value")) for key, value in info.get("extmetadata", {}).items()}
        lic_name, lic_code = normalized_license(meta.get("LicenseShortName", ""))
        license_url = meta.get("LicenseUrl", "")
        if not license_url and lic_code == "public-domain":
            license_url = "https://creativecommons.org/publicdomain/mark/1.0/"
        elif not license_url and lic_code == "cc0":
            license_url = "https://creativecommons.org/publicdomain/zero/1.0/"
        out[page["title"]] = {
            "title": page["title"],
            "description": meta.get("ImageDescription") or page["title"].removeprefix("File:"),
            "creator": meta.get("Artist") or meta.get("Credit") or "",
            "sourcePage": info.get("descriptionurl", ""),
            "originalFile": info.get("url", ""),
            "downloadFile": info.get("thumburl") or info.get("url", ""),
            "license": lic_name,
            "licenseCode": lic_code,
            "licenseUrl": license_url,
            "originalWidth": info.get("width", 0),
            "originalHeight": info.get("height", 0),
            "capturedAt": meta.get("DateTimeOriginal") or meta.get("DateTime") or "",
        }
    return out


def search_titles(query, limit=8):
    payload = api({
        "action": "query", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": query, "gsrlimit": limit, "gsrsort": "relevance",
    })
    return [page["title"] for page in payload.get("query", {}).get("pages", [])
            if page.get("title", "").lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff"))]


# 재사용·재배포가 금지되지 않은 것. 여기 없는 값도 경고만 하고 통과시킨다.
ALLOWED_LICENSES = {"public-domain", "cc0", "cc-by", "cc-by-sa"}


def score(info, selected):
    width, height = info["originalWidth"], info["originalHeight"]
    return {
        "representativeness": 30 if selected else 22,
        "composition": 19 if selected else 14,
        "guidebookFit": 15 if selected else 11,
        "mobileRecognition": 14 if selected else 10,
        "resolution": 10 if max(width, height) >= 2400 else (8 if max(width, height) >= 1600 else 5),
        "licenseClarity": 10 if info["licenseCode"] != "unknown" else 0,
    }


def total(parts):
    return sum(parts.values())


def original_path(item, info, region):
    suffix = Path(urllib.parse.unquote(urllib.parse.urlparse(info["originalFile"]).path)).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".tif", ".tiff"}:
        suffix = ".jpg"
    return f"source/ASSETS/photos/originals/{region}/{item['imageId']}{suffix}"


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--merge", action="store_true",
                        help="preserve entries from earlier batches, replacing this plan's places")
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    candidates, rejected, approved = [], [], []
    for subject in plan["subjects"]:
        region = subject.get("region") or plan["region"]
        selected_title = subject["selectedTitle"]
        titles = [selected_title]
        for title in search_titles(subject["query"]):
            if title not in titles:
                titles.append(title)
            if len(titles) == 3:
                break
        infos = image_info(titles)
        if selected_title not in infos:
            raise SystemExit(f"selected Commons file not found: {selected_title}")
        selected_info = infos[selected_title]
        # Jason 지시(2026-08-18) — 라이선스·저작자 강제를 **차단이 아니라 경고**로 내린다.
        # 재사용이 금지되지 않은 공개 사진을 폭넓게 쓰기 위해서다.
        #
        # 다만 두 가지는 사실로 남겨 둔다.
        #  · 이 사이트는 gh-pages 로 공개 배포된다. '개인 사용만' 라이선스는 검사를
        #    없앤다고 쓸 수 있게 되는 것이 아니라 빌드가 알려주지 않게 되는 것이다.
        #  · 저작자 표시는 CC BY·CC BY-SA 의 이용 조건이다. 그래서 저작자가 비어 있으면
        #    거부하는 대신 '저작자 미상'으로 채워 크레딧 페이지에 그대로 드러낸다.
        if selected_info["licenseCode"] not in ALLOWED_LICENSES:
            print(f"  ! 라이선스 확인 필요: {selected_title} ({selected_info['license']})")
        if not selected_info["creator"]:
            print(f"  ! 저작자 미상: {selected_title}")
            selected_info["creator"] = "저작자 미상 (Wikimedia Commons)"

        for rank, title in enumerate(titles, 1):
            if title not in infos:
                continue
            info = infos[title]
            is_selected = title == selected_title
            parts = score(info, is_selected)
            reason = ("장소 대표성·구도·해상도·라이선스를 검토해 승인"
                      if is_selected else "승인본보다 대표성 또는 모바일 구도가 낮아 대안 후보로 보류")
            row = {
                "placeId": subject["placeId"], "candidateRank": rank,
                "photoTitle": title.removeprefix("File:"), "description": info["description"],
                "creator": info["creator"], "sourcePage": info["sourcePage"],
                "originalFile": info["originalFile"], "license": info["license"],
                "licenseUrl": info["licenseUrl"], "originalWidth": info["originalWidth"],
                "originalHeight": info["originalHeight"], "capturedAt": info["capturedAt"],
                **parts, "score": total(parts), "selected": is_selected, "reason": reason,
            }
            candidates.append(row)
            if not is_selected:
                rejected.append({**row, "rejectionReason": reason})

        change = "EXIF orientation corrected; cropped, resized and converted to WebP; metadata removed"
        approved.append({
            "imageId": subject["imageId"], "placeId": subject["placeId"],
            "title": selected_title.removeprefix("File:"), "titleKo": subject["titleKo"],
            "description": selected_info["description"], "source": "Wikimedia Commons",
            "sourcePage": selected_info["sourcePage"], "originalFile": selected_info["originalFile"],
            "creator": selected_info["creator"], "license": selected_info["license"],
            "licenseCode": selected_info["licenseCode"], "licenseUrl": selected_info["licenseUrl"],
            "changes": change, "downloadDate": plan["downloadDate"],
            "originalWidth": selected_info["originalWidth"],
            "originalHeight": selected_info["originalHeight"],
            "originalPath": original_path(subject, selected_info, region), "originalSha256": "",
            "usage": subject["usage"], "role": subject["role"], "region": region,
            "regionHero": subject.get("regionHero", False), "status": "approved",
            "altKo": subject["altKo"], "captionKo": subject["captionKo"],
            "focus": subject["focus"], "variants": {"hero": [], "content": [], "thumbnail": []},
            "selectionScore": next(row["score"] for row in candidates
                                   if row["placeId"] == subject["placeId"] and row["selected"]),
        })

    plan_places = {subject["placeId"] for subject in plan["subjects"]}
    plan_image_ids = {subject["imageId"] for subject in plan["subjects"]}
    if args.merge:
        previous = json.loads((DATA / "photo-candidates.json").read_text(encoding="utf-8"))
        kept = [row for row in previous.get("candidates", [])
                if row["placeId"] not in plan_places]
        candidates = kept + candidates
        rejected = [row for row in candidates if not row["selected"]]
        previous_manifest = json.loads((DATA / "image-manifest.json").read_text(encoding="utf-8"))
        previous_by_id = {image["imageId"]: image
                          for image in previous_manifest.get("images", [])}
        # Same selected original as before → keep downloaded/processed pipeline
        # state so a plan re-run stays idempotent.
        for image in approved:
            prev = previous_by_id.get(image["imageId"])
            if prev and prev.get("originalFile") == image["originalFile"]:
                for key in ("originalSha256", "originalBytes", "storedWidth",
                            "storedHeight", "variants", "status", "changes"):
                    if prev.get(key):
                        image[key] = prev[key]
        kept_images = []
        for image in previous_manifest.get("images", []):
            if image["imageId"] in plan_image_ids or image["placeId"] in plan_places:
                continue
            image.setdefault("region", Path(image["originalPath"]).parent.name)
            kept_images.append(image)
        approved = kept_images + approved

    payload = {"schemaVersion": "1.0", "generatedAt": plan["downloadDate"],
               "source": "Wikimedia Commons file-description pages", "candidates": candidates}
    (DATA / "photo-candidates.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = ["placeId", "candidateRank", "photoTitle", "description", "creator", "sourcePage",
              "originalFile", "license", "licenseUrl", "originalWidth", "originalHeight", "capturedAt",
              "representativeness", "composition", "guidebookFit", "mobileRecognition", "resolution",
              "licenseClarity", "score", "selected", "reason"]
    write_csv(DATA / "photo-candidates.csv", candidates, fields)
    write_csv(DATA / "rejected-photo-candidates.csv",
              [{**row, "rejectionReason": row.get("rejectionReason", row["reason"])}
               for row in rejected], fields + ["rejectionReason"])
    regions = sorted({image.get("region", "") for image in approved})
    manifest = {"schemaVersion": "1.0", "generatedAt": plan["downloadDate"],
                "regions": regions, "images": approved}
    (DATA / "image-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Commons candidates: {len(candidates)} · approved {len(approved)} · rejected {len(rejected)}")


if __name__ == "__main__":
    main()
