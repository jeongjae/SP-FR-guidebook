#!/usr/bin/env python3
"""Capture and verify the generated date-page integration preview."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "site" / "daily" / "day-02.html"
OUTPUT = ROOT / "docs" / "previews" / "day-02-daily-card-integration-mobile.png"


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
        page.goto(PAGE.as_uri(), wait_until="load")
        card = page.locator("details.day-card-archive").filter(has_text="Daily Action Map")
        card.scroll_into_view_if_needed()
        card.screenshot(path=str(OUTPUT))
        image = card.locator("img")
        full_link = card.locator("figure > a").first
        png_link = card.locator("figcaption a")
        result = {
            "page": str(PAGE.relative_to(ROOT)),
            "screenshot": str(OUTPUT.relative_to(ROOT)),
            "thumbnail": image.get_attribute("src"),
            "thumbnailSize": image.evaluate("el => [el.naturalWidth, el.naturalHeight]"),
            "loading": image.get_attribute("loading"),
            "alt": image.get_attribute("alt"),
            "fullWebp": full_link.get_attribute("href"),
            "fullPng": png_link.get_attribute("href"),
        }
        for key in ("thumbnail", "fullWebp", "fullPng"):
            path = (PAGE.parent / result[key]).resolve()
            if not path.exists():
                raise SystemExit(f"broken integration link: {key} → {path}")
        if result["thumbnailSize"] != [480, 640] or result["loading"] != "lazy" or not result["alt"]:
            raise SystemExit(f"invalid thumbnail integration: {result}")
        browser.close()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

