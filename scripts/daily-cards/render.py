#!/usr/bin/env python3
"""Render selected Daily Action Map JSON files to HTML, PNG and WebP."""

from __future__ import annotations

import argparse
import base64
import json
import math
import re
import shutil
import subprocess
import unicodedata
from pathlib import Path

from PIL import Image
from playwright.sync_api import Error as PlaywrightError, sync_playwright


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "daily-cards"
TEMPLATE = ROOT / "templates" / "daily-card"
OUTPUT = ROOT / "source" / "ASSETS" / "80_Daily_Mobile_Guide_Images" / "v2"
FONT_DIR = ROOT / "build" / "assets" / "vendor" / "nanum"
MAP_WIDTH, MAP_HEIGHT = 746, 1118
WINDOWS_CHROME = Path("/mnt/c/Program Files/Google/Chrome/Application/chrome.exe")


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def world_pixel(lat: float, lng: float, zoom: int) -> tuple[float, float]:
    scale = 256 * 2**zoom
    sin_lat = math.sin(math.radians(lat))
    return ((lng + 180) / 360 * scale,
            (0.5 - math.log((1 + sin_lat) / (1 - sin_lat)) / (4 * math.pi)) * scale)


def tile_payload(day: dict) -> list[dict]:
    zoom = day["map"]["zoom"]
    cx, cy = world_pixel(day["map"]["center"][0], day["map"]["center"][1], zoom)
    left, right = cx - MAP_WIDTH / 2 - 256, cx + MAP_WIDTH / 2 + 256
    top, bottom = cy - MAP_HEIGHT / 2 - 256, cy + MAP_HEIGHT / 2 + 256
    limit = 2**zoom
    tiles = []
    for raw_x in range(math.floor(left/256), math.floor(right/256)+1):
        for y in range(max(0, math.floor(top/256)), min(limit-1, math.floor(bottom/256))+1):
            x = raw_x % limit
            path = DATA / "tiles" / str(zoom) / str(x) / f"{y}.png"
            if not path.exists():
                raise SystemExit(f"missing OSM tile {path}; run cache_tiles.py first")
            tiles.append({"x": raw_x, "y": y, "src": data_uri(path, "image/png")})
    return tiles


def route_payload(day: dict) -> list[list[float]]:
    cache = day.get("map", {}).get("routeCache") if day.get("map") else None
    if not cache:
        return []
    payload = json.loads((DATA / cache).read_text(encoding="utf-8"))
    if payload.get("code") != "Ok":
        raise SystemExit(f"route cache is not successful: {cache}")
    return payload["routes"][0]["geometry"]["coordinates"]


def output_slug(day: dict) -> str:
    text = unicodedata.normalize("NFKD", day["city"]).encode("ascii", "ignore").decode().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return f"day-{day['day']:02d}-{text}"


def build_html(day: dict) -> tuple[Path, str]:
    source_dir = OUTPUT / "source"
    source_dir.mkdir(parents=True, exist_ok=True)
    html = (TEMPLATE / "card.html").read_text(encoding="utf-8")
    style = (TEMPLATE / "card.css").read_text(encoding="utf-8")
    style = style.replace("{{FONT_REGULAR}}", data_uri(FONT_DIR / "nanum-gothic-korean-400-normal.woff2", "font/woff2"))
    style = style.replace("{{FONT_BOLD}}", data_uri(FONT_DIR / "nanum-gothic-korean-700-normal.woff2", "font/woff2"))
    replacements = {
        "{{TITLE}}": f"Day {day['day']:02d} · {day['city']}",
        "{{STYLE}}": style,
        "{{SCRIPT}}": (TEMPLATE / "card.js").read_text(encoding="utf-8"),
        "{{DATA}}": json.dumps(day, ensure_ascii=False),
        "{{TILES}}": json.dumps(tile_payload(day), ensure_ascii=False),
        "{{ROUTE}}": json.dumps(route_payload(day), ensure_ascii=False, separators=(",", ":")),
    }
    for key, value in replacements.items():
        html = html.replace(key, value)
    slug = output_slug(day)
    path = source_dir / f"{slug}.html"
    path.write_text(html, encoding="utf-8")
    return path, slug


def windows_path(path: Path) -> str:
    result = subprocess.check_output(["wslpath", "-w", str(path)], text=True, encoding="utf-8")
    return result.strip()


def render_with_chrome_cli(html_path: Path, png_path: Path) -> dict:
    if not WINDOWS_CHROME.exists():
        raise SystemExit("Playwright Chromium unavailable and Windows Chrome was not found")
    command = [
        str(WINDOWS_CHROME), "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--no-first-run", "--no-default-browser-check", "--disable-background-networking",
        "--allow-file-access-from-files", "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=4000", "--window-size=1440,1920",
        f"--screenshot={windows_path(png_path)}", windows_path(html_path),
    ]
    subprocess.run(command, cwd=ROOT, check=True, timeout=120, capture_output=True, text=True)
    # The CLI cannot return JS values. The same collision algorithm records zero
    # overlap by construction; pixel/DOM checks are performed later when a native
    # Playwright browser is available in CI.
    return {"labelOverlaps": None, "overflow": None, "tileCount": None,
            "markerCount": None, "renderer": "windows-chrome-cli"}


def render(day_number: int, browser=None) -> dict:
    day = json.loads((DATA / f"day-{day_number:02d}.json").read_text(encoding="utf-8"))
    # Prototype gate retired after the 3-card approval (2026-08-05).
    # Mass generation stays impossible: only explicitly listed days render,
    # and days whose schedule data is still a scaffold fail below on null stops.
    if all(s.get("lat") is None for s in day.get("stops", [])):
        raise SystemExit(f"Day {day_number:02d} has no coordinates yet — fill data first")
    html_path, slug = build_html(day)
    full_dir, thumb_dir = OUTPUT / "full", OUTPUT / "thumbs"
    full_dir.mkdir(parents=True, exist_ok=True); thumb_dir.mkdir(parents=True, exist_ok=True)
    png_path = full_dir / f"{slug}.png"
    if browser is not None:
        page = browser.new_page(viewport={"width": 1440, "height": 1920}, device_scale_factor=1)
        page.goto(html_path.as_uri(), wait_until="load")
        page.wait_for_function("document.body.dataset.ready === 'true'")
        page.screenshot(path=str(png_path), full_page=False)
        qa = page.evaluate("window.__CARD_QA__")
        qa["renderer"] = "playwright-chromium"
        page.close()
    else:
        qa = render_with_chrome_cli(html_path, png_path)
    with Image.open(png_path) as image:
        image.save(full_dir / f"{slug}.webp", "WEBP", quality=86, method=6)
        image.resize((480, 640), Image.Resampling.LANCZOS).save(
            thumb_dir / f"{slug}-thumb.webp", "WEBP", quality=82, method=6
        )
    return {"day": day_number, "slug": slug, "html": str(html_path.relative_to(ROOT)), "qa": qa}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("days", nargs="*", type=int, default=[2, 4, 5])
    args = parser.parse_args()
    results, browser, playwright = [], None, None
    try:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
    except PlaywrightError as exc:
        print(f"Playwright unavailable; using Windows Chrome CLI: {exc.__class__.__name__}")
        if browser:
            browser.close()
        if playwright:
            playwright.stop()
        browser = playwright = None
    try:
        for number in args.days:
            results.append(render(number, browser))
    finally:
        if browser:
            browser.close()
        if playwright:
            playwright.stop()
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
