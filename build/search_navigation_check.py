#!/usr/bin/env python3
"""검색 결과의 런타임 URL 생성과 실제 탐색을 Chromium으로 검증한다.

정적 링크 감사는 JavaScript가 만든 href를 볼 수 없다. 서로 다른 page depth에서
place/day/region 검색 결과를 클릭하여 canonical 경로와 HTTP 상태를 함께 확인한다.
사전조건: python3 build/site.py
"""

from __future__ import annotations

import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

from pwa_check import chromium_path


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

# 출발 페이지, 검색어, 결과 종류, canonical 검색 인덱스 경로
CASES = (
    ("index.html", "Sagrada", "place", "places/sagrada-familia.html"),
    ("schedule.html", "Picasso", "place", "places/musee-picasso-paris.html"),
    ("daily/day-10.html", "Monaco", "place", "places/monaco.html"),
    ("guide/paris.html", "Orsay", "place", "places/musee-d-orsay.html"),
    ("places/musee-d-orsay.html", "Louvre", "place", "places/musee-du-louvre.html"),
    ("prepare/index.html", "Versailles", "place", "places/versailles.html"),
    ("guide/paris.html", "9.30", "day", "daily/day-33.html"),
    ("prepare/index.html", "생활 실험", "region", "guide/paris.html"),
)


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def main() -> int:
    problems: list[str] = []
    handler = partial(QuietHandler, directory=str(SITE))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server.daemon_threads = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}/"

    try:
        with sync_playwright() as pw:
            executable = chromium_path()
            browser = pw.chromium.launch(
                **({"executable_path": executable} if executable else {})
            )
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.set_default_timeout(20_000)
            console_errors: list[str] = []
            page.on(
                "console",
                lambda message: console_errors.append(message.text)
                if message.type == "error" else None,
            )
            page.on("pageerror", lambda error: console_errors.append(str(error)))

            for source, query, kind, target in CASES:
                response = page.goto(base + source, wait_until="domcontentloaded")
                if not response or response.status >= 400:
                    problems.append(f"출발 페이지 실패: {source}")
                    continue

                root = page.locator("body").get_attribute("data-site-root")
                expected_root = "." if "/" not in source else ".."
                if root != expected_root:
                    problems.append(
                        f"site root 불일치: {source} {root!r} != {expected_root!r}"
                    )

                page.locator("#search-btn").click()
                page.locator("#search-input").fill(query)
                result = page.locator(
                    f'#search-results a.search-result[href$="{target}"]'
                )
                result.wait_for(state="visible")
                if result.count() != 1:
                    problems.append(
                        f"검색 결과 중복/누락: {source} → {query} → {target} "
                        f"({result.count()}건)"
                    )
                    continue

                raw_href = result.get_attribute("href") or ""
                if "assets/style" in raw_href or "//" in raw_href or "/./" in raw_href:
                    problems.append(f"잘못 정규화된 href: {source} → {raw_href}")

                with page.expect_navigation(wait_until="domcontentloaded") as navigation:
                    result.click()
                landed = navigation.value
                if not landed or landed.status >= 400:
                    problems.append(
                        f"검색 클릭 HTTP 실패: {source} → {target} "
                        f"({landed.status if landed else 'response 없음'})"
                    )
                if not page.url.endswith("/" + target):
                    problems.append(
                        f"검색 목적지 불일치: {source} → {page.url} != {target}"
                    )
                if "404" in page.title():
                    problems.append(f"404 문서 도착: {source} → {target}")

                print(f"PASS {kind:6} {source} → {target}")

            if console_errors:
                problems.extend(f"브라우저 오류: {error}" for error in console_errors)
            browser.close()
    except Exception as error:
        problems.append(f"Playwright 검색 검사 실패: {error}")
    finally:
        server.shutdown()
        server.server_close()

    if problems:
        print(f"검색 탐색 검사 실패: {len(problems)}건")
        for problem in problems:
            print("  " + problem)
        return 1
    print(f"검색 탐색 검사 통과: {len(CASES)}건 · place/day/region · HTTP 404 0건")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
