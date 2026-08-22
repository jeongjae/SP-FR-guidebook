#!/usr/bin/env python3
"""Google Maps 의 업소 대표사진을 카탈로그에 넣는다 (FCR-03 사진 정책).

    python3 scripts/add_google_maps_photo.py --audit        # 신원만 확인
    python3 scripts/add_google_maps_photo.py                # 받아서 넣는다
    python3 scripts/add_google_maps_photo.py --only bar-canete

**왜 Google Maps 인가.** 식당·카페는 Commons 에 사진이 거의 없고, 공식
홈페이지는 예외 없이 기본 저작권이라 재배포할 수 없었다. 15곳이 그렇게
빈칸으로 남았다. 사용자가 이 프로젝트에 한해 Maps 사진을 쓰기로 결정했다.

**법적 성격을 숨기지 않는다.** Maps 사진은 업로더에게 저작권이 있고 자유
라이선스가 아니다. 그래서 라이선스 칸에 '자유 이용' 이라고 적지 않는다 —
`google-maps-ugc` 로 적고 출처 URL·업소 신원을 함께 남긴다. 화면의 크레딧도
그대로 나간다.

**신원 확인이 이 스크립트의 본체다.** 이름이 같은 다른 가게 사진을 붙이는
것이 최악의 사고다. 그래서 두 가지를 함께 본다.

    1 Maps 가 찾아 준 장소 이름이 우리가 아는 상호와 겹치는가
      (상호가 바뀐 곳은 `acceptTitle` 에 새 이름을 적어 둔다)
    2 우리가 아는 **번지와 도로명**이 그 장소 페이지에 실제로 있는가

둘 중 하나라도 어긋나면 사진을 받지 않고 `IDENTITY_UNCONFIRMED` 로 남긴다.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
import unicodedata
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "build"))

import model  # noqa: E402
import process_images as pi  # noqa: E402

QUEUE = ROOT / "data" / "images" / "google-maps-photo-queue.json"
MANIFEST = ROOT / "data" / "images" / "image-manifest.json"
MANIFEST_CSV = ROOT / "data" / "images" / "image-manifest.csv"
METADATA = ROOT / "source" / "ASSETS" / "photos" / "metadata" / "image-manifest.json"
ORIGINALS = ROOT / "source" / "ASSETS" / "photos" / "originals"
AUDIT = ROOT / "FCR03_FOOD_PHOTO_AUDIT.json"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124 Safari/537.36")
WANT = "=w1600-h1200-k-no"


# 신원 대조 규칙은 build/identity_match.py 한 곳에 있다. 여기서 다시 만들지
# 않는다 — 예전에 이 함수의 사본이 빈 문자열을 통과시켰다.
from identity_match import fold, names_match  # noqa: E402


def street_tokens(address: str) -> list[str]:
    """번지와 도로명에서 검증에 쓸 조각을 뽑는다."""
    parts = [p.strip() for p in re.split(r"[,]", address) if p.strip()]
    if not parts:
        return []
    head = parts[0]
    number = re.search(r"\d+", head)
    words = [w for w in re.findall(r"[A-Za-zÀ-ÿ']{4,}", head)
             if fold(w) not in ("rue", "carrer", "placa", "plaça", "quai",
                                "avenue", "passeig", "passatge", "boulevard",
                                "cours", "place")]
    out = []
    if number:
        out.append(number.group(0))
    out += words[:2]
    return out


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve(page, entry: dict) -> dict:
    """Maps 에서 장소를 찾고 신원을 대조한다."""
    query = f"{entry['name']} {entry['address']}".replace(" ", "+")
    # hl=en 을 붙인다. 지역 로케일이면 Maps 가 상호 대신 번역된 분류명을
    # 돌려주는 일이 있다 ('푸에스토시요 해산물 요리').
    page.goto(f"https://www.google.com/maps/search/{query}?hl=en&gl=US",
              timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(5200)
    html = page.content()
    title = re.sub(r"\s*-\s*Google.*$", "", page.title()).strip()

    accept = [entry["name"]] + (entry.get("acceptTitle") or [])
    # fold() 는 라틴 문자만 남긴다. Maps 가 상호 대신 번역된 분류명을 돌려주면
    # (예: '푸에스토시요 해산물 요리') 접힌 결과가 빈 문자열이 되고, 빈 문자열은
    # 무엇에나 들어 있으므로 검사를 통과해 버린다. 실제로 그렇게 통과했다.
    folded_title = fold(title)
    name_ok = bool(folded_title) and any(
        fold(a) and (fold(a) in folded_title or folded_title in fold(a))
        for a in accept)
    tokens = street_tokens(entry["address"])
    hits = [t for t in tokens if fold(t) in fold(html)]
    address_ok = bool(tokens) and len(hits) >= max(1, len(tokens) - 1)

    collect = """() => Array.from(document.querySelectorAll('img'))
        .filter(i => i.src && i.src.includes('googleusercontent')
                     && !i.src.includes('default-user'))
        .map(i => ({src: i.src, w: i.naturalWidth, h: i.naturalHeight}))"""

    def usable(rows):
        """DOM 의 크기는 **렌더된 썸네일 크기**다. 원본은 =w1600 으로 다시
        받으므로 절대 크기로 거르면 안 된다 — 그렇게 걸렀다가 Bodega Joan 의
        유일한 후보(408x272)를 버렸다. 비율만 본다. 파노라마는 썸네일
        480x320 크롭이 안 되므로 제외한다."""
        return [s for s in rows
                if s["w"] >= 200 and s["h"] >= 150
                and 0.5 <= s["w"] / max(s["h"], 1) <= 2.2]

    shots = page.evaluate(collect)
    if not usable(shots):
        # 첫 화면에는 파노라마 한 장만 붙어 있는 곳이 있다 (Bodega Joan).
        # 사진 갤러리를 열면 나머지가 로드된다.
        try:
            button = page.query_selector('button[jsaction*="heroHeaderImage"]') \
                or page.query_selector('button img[src*="googleusercontent"]')
            if button:
                button.click()
                page.wait_for_timeout(3500)
                page.mouse.wheel(0, 1200)
                page.wait_for_timeout(2500)
                shots = page.evaluate(collect)
        except Exception:
            pass
    shots = usable(shots)
    shots.sort(key=lambda s: s["w"] * s["h"], reverse=True)
    photo = shots[0]["src"] if shots else None
    if photo:
        photo = re.sub(r"=[^=]*$", "", photo) + WANT

    cid = re.search(r"!1s(0x[0-9a-f]+:0x[0-9a-f]+)", page.url)
    return {"resolvedTitle": title, "mapsUrl": page.url,
            "placeKey": cid.group(1) if cid else None,
            "nameMatch": name_ok, "addressMatch": address_ok,
            "addressTokens": tokens, "addressHits": hits,
            "photoUrl": photo, "photoCount": len(shots)}


def download(url: str, target: Path) -> tuple[int, int]:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=90) as response:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(response.read())
    with Image.open(target) as src:
        image = ImageOps.exif_transpose(src).convert("RGB")
        image.save(target, "JPEG", quality=90)
        return image.size


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
    parser.add_argument("--audit", action="store_true", help="신원 확인까지만")
    parser.add_argument("--only", action="append", default=[])
    args = parser.parse_args()

    from playwright.sync_api import sync_playwright

    queue = json.loads(QUEUE.read_text(encoding="utf-8"))["queue"]
    if args.only:
        queue = [q for q in queue if q["slug"] in args.only]
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    known = {img["imageId"] for img in payload["images"]}

    results, added = [], []
    with sync_playwright() as play:
        browser = play.chromium.launch()
        ctx = browser.new_context(locale="en-US",
                                  viewport={"width": 1280, "height": 900},
                                  user_agent=UA)
        for entry in queue:
            image_id = f"{entry['region']}-{entry['slug']}-gm01"
            page = ctx.new_page()
            try:
                info = resolve(page, entry)
            except Exception as exc:
                info = {"error": f"{type(exc).__name__}: {exc}"}
            page.close()
            record = {"slug": entry["slug"], "region": entry["region"],
                      "name": entry["name"], "address": entry["address"], **info}

            if info.get("error"):
                record["status"] = "LOOKUP_FAILED"
            elif not (info["nameMatch"] and info["addressMatch"]):
                record["status"] = "IDENTITY_UNCONFIRMED"
            elif not info.get("photoUrl"):
                record["status"] = "NO_PHOTO_ON_MAPS"
            else:
                record["status"] = "IDENTITY_CONFIRMED"
            print(f"  {record['status']:22s} {entry['slug']:34s} "
                  f"title={info.get('resolvedTitle','')[:28]:30s} "
                  f"addr={info.get('addressHits')}")
            results.append(record)

            if args.audit or record["status"] != "IDENTITY_CONFIRMED":
                continue
            if image_id in known:
                print(f"      이미 카탈로그에 있다 — 건너뛴다")
                continue

            target = ORIGINALS / f"{image_id}.jpg"
            try:
                width, height = download(info["photoUrl"], target)
            except Exception as exc:
                record["status"] = "DOWNLOAD_FAILED"
                record["error"] = f"{type(exc).__name__}: {exc}"
                continue
            item = {
                "imageId": image_id, "placeId": entry["slug"],
                "region": entry["region"],
                "title": f"{info['resolvedTitle']} — Google Maps",
                "titleKo": entry.get("titleKo") or entry["name"],
                "description": entry["address"],
                "source": "Google Maps",
                "sourcePage": info["mapsUrl"],
                "originalFile": info["photoUrl"],
                "creator": "Google Maps 기여자 (개별 표기 없음)",
                "license": "Google Maps 사용자 제공 사진 — 자유 라이선스 아님",
                "licenseCode": "google-maps-ugc",
                "licenseUrl": "https://www.google.com/help/terms_maps/",
                "businessIdentity": {
                    "name": entry["name"], "resolvedName": info["resolvedTitle"],
                    "address": entry["address"], "placeKey": info["placeKey"],
                    "mapsUrl": info["mapsUrl"],
                    "matchedOn": ["name", "address"]},
                "changes": ("EXIF orientation corrected; resized and converted to "
                            "WebP; metadata removed"),
                "downloadDate": entry.get("verifiedAt", "2026-08-22"),
                "originalWidth": width, "originalHeight": height,
                "originalPath": str(target.relative_to(ROOT)).replace("\\", "/"),
                "originalSha256": sha256(target),
                "originalBytes": target.stat().st_size,
                "focus": {"x": 0.5, "y": 0.5}, "regionHero": False,
                "role": "major",
                "usage": [f"guide/{entry['region']}.html",
                          f"places/{entry['slug']}.html"],
                "selectionScore": 80,
                "altKo": entry.get("altKo") or f"{entry['name']} 외관",
                "captionKo": entry.get("captionKo") or "",
            }
            with Image.open(ROOT / item["originalPath"]) as src:
                image = pi.srgb_image(src)
                variants = {"hero": [], "content": [], "thumbnail": []}
                for cw in (1280, 1080, 960):
                    made = pi.variant(image, image_id, "content", cw)
                    if made and made["bytes"] <= pi.BYTE_LIMIT["content"]:
                        variants["content"].append(made)
                        break
                    if made:
                        (ROOT / made["path"]).unlink()
                made = pi.variant(image, image_id, "thumbnail", 480, 320,
                                  item["focus"])
                if made:
                    variants["thumbnail"].append(made)
            if not variants["content"] or not variants["thumbnail"]:
                record["status"] = "DERIVATIVE_FAILED"
                continue
            item["variants"] = variants
            item["status"] = "processed"
            payload["images"].append(item)
            added.append(image_id)
            record["imageId"] = image_id
            record["status"] = "VALID_GOOGLE_MAPS"
            print(f"      추가 {image_id} ({width}x{height})")
        browser.close()

    if added:
        write_catalog(payload)
    AUDIT.write_text(json.dumps({"auditedAt": "2026-08-22",
                                 "policy": "FCR-03 · Google Maps 우선",
                                 "results": results}, ensure_ascii=False, indent=1),
                     encoding="utf-8")
    print(f"\n확인 {len(results)} · 추가 {len(added)} → {AUDIT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
