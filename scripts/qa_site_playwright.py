#!/usr/bin/env python3
"""Smoke-test the generated guidebook in Chromium and save QA screenshots."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright


PAGES = {
    "home": ("/index.html", ("43일 42박", "Luberon Farmhouse", "(3박)", "(16박)")),
    "itinerary": ("/chapters/itinerary.html", ("43일 Master Itinerary", "9/24", "Paris")),
    "aix": ("/chapters/aix/index.html", ("Marseille", "Cassis", "선택 대안")),
    "marseille": ("/daily/day-14.html", ("Marseille 대중교통 당일치기", "Vieux-Port", "Mucem")),
    "luberon": ("/chapters/luberon/index.html", ("3박", "9/13", "9/16")),
    "avignon": ("/chapters/avignon/index.html", ("Arles", "Les Baux", "선택 대안")),
    "arles": ("/daily/day-22.html", ("Arles 철도 당일치기", "Arènes d’Arles", "La Roquette")),
    "lyon": ("/chapters/lyon/index.html", ("9/20", "9/24", "Annecy")),
    "paris": ("/chapters/paris/index.html", ("16박", "9/24", "생활")),
    "aix-map": ("/maps/aix.html", ("Marseille", "Mucem", "Fort Saint-Jean")),
    "avignon-map": ("/maps/avignon.html", ("Arles", "Arènes d’Arles", "La Roquette")),
    "reservations": ("/tracker/reservations.html", ("예약 변경 필요", "Luberon", "Paris")),
}

MOBILE_SHOTS = {"home", "marseille", "arles", "aix-map", "avignon-map", "reservations"}


def safe_name(value: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8765")
    parser.add_argument("--output", default="/tmp/spfr-guidebook-qa")
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    errors: list[str] = []
    report: dict[str, object] = {"baseUrl": args.base_url, "pages": {}}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for mode, viewport in (("desktop", {"width": 1440, "height": 1000}),
                               ("mobile", {"width": 390, "height": 844})):
            context = browser.new_context(viewport=viewport, color_scheme="light")
            for name, (path, required) in PAGES.items():
                if mode == "mobile" and name not in MOBILE_SHOTS:
                    continue
                page_errors: list[str] = []
                page = context.new_page()
                page.on("console", lambda msg, bucket=page_errors:
                        bucket.append(f"console.{msg.type}: {msg.text}")
                        if msg.type == "error" else None)
                page.on("pageerror", lambda exc, bucket=page_errors:
                        bucket.append(f"pageerror: {exc}"))
                response = page.goto(args.base_url + path, wait_until="networkidle")
                if not response or response.status >= 400:
                    errors.append(f"{mode}/{name}: HTTP {response.status if response else '없음'}")
                body = page.content()
                for term in required:
                    if term not in body:
                        errors.append(f"{mode}/{name}: 필수 텍스트 누락 — {term}")
                overflow = page.evaluate(
                    "document.documentElement.scrollWidth - document.documentElement.clientWidth"
                )
                if overflow > 0:
                    errors.append(f"{mode}/{name}: 가로 넘침 {overflow}px")
                if page_errors:
                    errors.extend(f"{mode}/{name}: {item}" for item in page_errors)
                shot = output / f"{safe_name(name)}-{mode}.png"
                page.screenshot(path=str(shot), full_page=True)
                report["pages"][f"{name}-{mode}"] = {
                    "url": path,
                    "title": page.title(),
                    "screenshot": str(shot),
                    "horizontalOverflow": overflow,
                    "consoleErrors": page_errors,
                }
                page.close()
            context.close()

        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        search_errors: list[str] = []
        page.on("console", lambda msg: search_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: search_errors.append(str(exc)))
        page.goto(args.base_url + "/index.html", wait_until="networkidle")
        page.click("#search-btn")
        search_report = {}
        for term, target in (("Marseille", "places/marseille.html"), ("Arles", "places/arles.html")):
            page.fill("#search-input", term)
            page.wait_for_timeout(150)
            links = page.locator("#search-results a")
            hrefs = [links.nth(i).get_attribute("href") for i in range(links.count())]
            if not any(href and target in href for href in hrefs):
                errors.append(f"search/{term}: 유효한 장소 결과 누락")
            search_report[term] = hrefs[:10]
        page.screenshot(path=str(output / "search-mobile.png"), full_page=True)
        if search_errors:
            errors.extend(f"search: {item}" for item in search_errors)
        report["search"] = search_report
        context.close()
        browser.close()

    report["errors"] = errors
    (output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if errors:
        print(f"브라우저 QA 실패: {len(errors)}건")
        for error in errors:
            print("  " + error)
        return 1
    print(f"브라우저 QA 통과: 데스크톱 {len(PAGES)}쪽 · 모바일 {len(MOBILE_SHOTS)}쪽 · 검색 2건")
    print(f"스크린샷·리포트: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
