#!/usr/bin/env python3
"""Collect Commons candidates and create an approved Barcelona manifest.

Only file-description metadata returned by the Wikimedia Commons API is used.
The search plan pins the reviewed file title; search results supply two
alternatives for the audit trail and never silently replace the reviewed file.
"""

from __future__ import annotations

import csv
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data/images"
PLAN = DATA / "barcelona-search-plan.json"
API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "SP-FR-guidebook-photo-pilot/1.0 (https://github.com/jeongjae/SP-FR-guidebook)"


def api(params):
    query = urllib.parse.urlencode({"format": "json", "formatversion": 2, **params})
    request = urllib.request.Request(f"{API}?{query}", headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


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


def original_path(item, info):
    suffix = Path(urllib.parse.unquote(urllib.parse.urlparse(info["originalFile"]).path)).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".tif", ".tiff"}:
        suffix = ".jpg"
    return f"source/ASSETS/photos/originals/barcelona/{item['imageId']}{suffix}"


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    candidates, rejected, approved = [], [], []
    for subject in plan["subjects"]:
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
        if selected_info["licenseCode"] not in {"public-domain", "cc0", "cc-by", "cc-by-sa"}:
            raise SystemExit(f"selected file has disallowed/unknown license: {selected_title}")
        if not selected_info["creator"] and selected_info["licenseCode"] not in {"public-domain", "cc0"}:
            raise SystemExit(f"selected file creator missing: {selected_title}")

        for rank, title in enumerate(titles, 1):
            if title not in infos:
                continue
            info = infos[title]
            is_selected = title == selected_title
            parts = score(info, is_selected)
            reason = ("장소 대표성·구도·해상도·라이선스를 검토해 Pilot 승인"
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
            "originalPath": original_path(subject, selected_info), "originalSha256": "",
            "usage": subject["usage"], "role": subject["role"],
            "regionHero": subject.get("regionHero", False), "status": "approved",
            "altKo": subject["altKo"], "captionKo": subject["captionKo"],
            "focus": subject["focus"], "variants": {"hero": [], "content": [], "thumbnail": []},
            "selectionScore": next(row["score"] for row in candidates
                                   if row["placeId"] == subject["placeId"] and row["selected"]),
        })

    payload = {"schemaVersion": "1.0", "generatedAt": plan["downloadDate"],
               "source": "Wikimedia Commons file-description pages", "candidates": candidates}
    (DATA / "photo-candidates.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = ["placeId", "candidateRank", "photoTitle", "description", "creator", "sourcePage",
              "originalFile", "license", "licenseUrl", "originalWidth", "originalHeight", "capturedAt",
              "representativeness", "composition", "guidebookFit", "mobileRecognition", "resolution",
              "licenseClarity", "score", "selected", "reason"]
    write_csv(DATA / "photo-candidates.csv", candidates, fields)
    write_csv(DATA / "rejected-photo-candidates.csv", rejected, fields + ["rejectionReason"])
    manifest = {"schemaVersion": "1.0", "generatedAt": plan["downloadDate"],
                "region": "barcelona", "images": approved}
    (DATA / "image-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Commons candidates: {len(candidates)} · approved {len(approved)} · rejected {len(rejected)}")


if __name__ == "__main__":
    main()
