#!/usr/bin/env python3
"""iPhone PWA 정적 무결성과 실제 오프라인 탐색을 검사한다.

사용: python3 build/pwa_check.py
사전조건: python3 build/build.py
"""

import hashlib
import json
import struct
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

import os
import shutil


def chromium_path():
    """명시 override 또는 로컬 Chromium. Playwright 관리 브라우저가 최종 폴백이다.

    (hig_check.py 삭제 2026-08-18 로 이쪽으로 옮겨 왔다.)
    """
    override = os.environ.get("TP_GUIDEBOOK_CHROMIUM")
    if override:
        return override
    for candidate in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        found = shutil.which(candidate)
        if found:
            return found
    return None


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
EXCLUDED = {"sw.js", "offline-files.json", ".nojekyll"}
EXPECTED_ICONS = {
    "assets/pwa/apple-touch-icon.png": (180, 180),
    "assets/pwa/icon-192.png": (192, 192),
    "assets/pwa/icon-512.png": (512, 512),
    "assets/pwa/icon-maskable-512.png": (512, 512),
}
OFFLINE_ROUTES = (
    ("index.html", "2026 유럽 여행 가이드북"),
    ("daily/day-43.html", "Day 43"),
    ("chapters/paris/food.html", "먹거리"),
    ("tracker/reservations.html", "예약"),
    ("maps/paris.html", "Paris"),
)


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def png_size(path):
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("PNG IHDR 없음")
    return struct.unpack(">II", data[16:24])


def static_checks(problems):
    required = ("manifest.webmanifest", "offline-files.json", "offline-fallback.html", "sw.js")
    for rel in required:
        if not (SITE / rel).is_file():
            problems.append(f"필수 PWA 파일 없음: {rel}")
    if problems:
        return None

    manifest = json.loads((SITE / "manifest.webmanifest").read_text(encoding="utf-8"))
    for key in ("id", "name", "short_name", "start_url", "scope", "display", "icons"):
        if not manifest.get(key):
            problems.append(f"Manifest 필드 없음: {key}")
    if manifest.get("start_url") != "./index.html":
        problems.append("Manifest start_url은 ./index.html이어야 한다")
    if manifest.get("scope") != "./" or manifest.get("display") != "standalone":
        problems.append("Manifest scope/display가 프로젝트 상대 standalone이 아니다")

    declared = {item.get("src", "").removeprefix("./"): item for item in manifest["icons"]}
    for rel, expected in EXPECTED_ICONS.items():
        path = SITE / rel
        if rel not in declared:
            problems.append(f"Manifest 아이콘 선언 없음: {rel}")
        if not path.is_file():
            problems.append(f"아이콘 파일 없음: {rel}")
            continue
        try:
            actual = png_size(path)
        except ValueError as error:
            problems.append(f"아이콘 형식 오류: {rel} ({error})")
            continue
        if actual != expected:
            problems.append(f"아이콘 크기 오류: {rel} {actual} != {expected}")

    offline = json.loads((SITE / "offline-files.json").read_text(encoding="utf-8"))
    records = {item["path"]: item for item in offline.get("files", [])}
    def precached(rel):
        if rel in EXCLUDED:
            return False
        # 검수용 Action Map PNG 원본은 온라인 전용 (build.py와 같은 규칙).
        return not (rel.startswith("assets/daily-cards/full/") and rel.endswith(".png"))

    actual_files = {
        path.relative_to(SITE).as_posix()
        for path in SITE.rglob("*")
        if path.is_file() and precached(path.relative_to(SITE).as_posix())
    }
    if set(records) != actual_files:
        missing = sorted(actual_files - set(records))
        extra = sorted(set(records) - actual_files)
        if missing:
            problems.append("오프라인 목록 누락: " + ", ".join(missing[:10]))
        if extra:
            problems.append("오프라인 목록에 없는 파일: " + ", ".join(extra[:10]))

    total_bytes = 0
    for rel, item in records.items():
        path = SITE / rel
        content = path.read_bytes()
        total_bytes += len(content)
        if len(content) != item.get("size"):
            problems.append(f"파일 크기 불일치: {rel}")
        if hashlib.sha256(content).hexdigest() != item.get("sha256"):
            problems.append(f"SHA-256 불일치: {rel}")
    if offline.get("totalFiles") != len(records) or offline.get("totalBytes") != total_bytes:
        problems.append("오프라인 목록 합계가 실제 파일 합계와 다르다")

    service_worker = (SITE / "sw.js").read_text(encoding="utf-8")
    if "__PWA_" in service_worker:
        problems.append("Service Worker에 미치환 템플릿 토큰이 남아 있다")
    if offline.get("version") not in service_worker:
        problems.append("Service Worker 버전과 파일 목록 버전이 다르다")
    if "url.origin !== SCOPE.origin" not in service_worker:
        problems.append("Service Worker의 같은 출처 제한이 없다")

    for path in SITE.rglob("*.html"):
        head = path.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in head[:900]:
            continue
        rel = path.relative_to(SITE).as_posix()
        if 'rel="manifest"' not in head:
            problems.append(f"Manifest 링크 없음: {rel}")
        if 'rel="icon"' not in head:
            problems.append(f"브라우저 아이콘 링크 없음: {rel}")
        if "assets/pwa.js" not in head:
            problems.append(f"PWA 등록 스크립트 없음: {rel}")

    return offline


def browser_checks(offline, problems):
    handler = partial(QuietHandler, directory=str(SITE))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server.daemon_threads = True
    server.block_on_close = False
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}/"
    console_errors = []
    try:
        with sync_playwright() as pw:
            executable = chromium_path()
            browser = pw.chromium.launch(**({"executable_path": executable} if executable else {}))
            context = browser.new_context(viewport={"width": 390, "height": 844})
            page = context.new_page()
            page.set_default_timeout(20_000)

            def record_console_error(message):
                if message.type != "error":
                    return
                location = message.location.get("url", "")
                suffix = f" ({location})" if location else ""
                console_errors.append(message.text + suffix)

            page.on("console", record_console_error)

            print("PWA 브라우저 검사: 등록", flush=True)
            page.goto(base + "maps/offline.html", wait_until="domcontentloaded")
            if page.title() != "오프라인 준비 — 2026 유럽 여행 가이드북":
                problems.append("오프라인 준비 페이지 제목이 예상과 다르다")
            page.wait_for_function("() => 'serviceWorker' in navigator")
            page.evaluate("async () => { await navigator.serviceWorker.ready; return true; }")
            if not page.evaluate("() => Boolean(navigator.serviceWorker.controller)"):
                page.reload(wait_until="domcontentloaded")
            page.wait_for_function("() => Boolean(navigator.serviceWorker.controller)")
            page.locator("#pwa-panel").wait_for(state="visible")
            print("PWA 브라우저 검사: 전체 저장", flush=True)
            page.locator("#pwa-save").click()
            page.wait_for_function(
                "() => document.querySelector('#pwa-status').textContent.includes('오프라인 준비 완료')",
                timeout=120_000)
            progress_value = page.locator("#pwa-progress").evaluate("element => element.value")
            if progress_value != offline["totalFiles"]:
                problems.append("전체 저장 뒤 progress 값이 전체 파일 수와 다르다")

            print("PWA 브라우저 검사: 오프라인 심층 탐색", flush=True)
            # 브라우저 네트워크 에뮬레이션만 믿지 않고 원본 서버 자체를 내린다.
            # 이후 성공은 Service Worker 캐시에서 왔다는 뜻이다.
            server.shutdown()
            context.set_offline(True)
            for rel, expected in OFFLINE_ROUTES:
                response = page.goto(base + rel, wait_until="domcontentloaded", timeout=20_000)
                if not response or response.status >= 400:
                    problems.append(f"오프라인 탐색 실패: {rel}")
                    continue
                if expected not in (page.title() + " " + page.locator("body").inner_text()[:2000]):
                    problems.append(f"오프라인 페이지 내용 불일치: {rel}")

            response = page.goto(base + "not-in-offline-package.html", wait_until="domcontentloaded")
            if not response or "아직 저장되지 않았습니다" not in page.locator("body").inner_text():
                problems.append("저장되지 않은 경로가 오프라인 fallback을 표시하지 않는다")
            context.set_offline(False)
            context.close()
            browser.close()
    except Exception as error:
        problems.append(f"Playwright PWA 검사 실패: {error}")
    finally:
        server.shutdown()
        server.server_close()

    relevant = [message for message in console_errors
                if "ERR_INTERNET_DISCONNECTED" not in message and "tile.openstreetmap.org" not in message]
    if relevant:
        problems.append("브라우저 콘솔 오류: " + " | ".join(relevant[:5]))


def main():
    if not SITE.is_dir():
        print("site/가 없다. 먼저 python3 build/build.py를 실행하라.")
        return 1
    problems = []
    offline = static_checks(problems)
    if offline and not problems and "--static" not in sys.argv:
        browser_checks(offline, problems)
    if problems:
        print(f"PWA 검사 실패 — {len(problems)}건")
        for problem in problems[:40]:
            print("  " + problem)
        return 1
    scope = "정적 무결성" if "--static" in sys.argv else "전체 저장/오프라인 심층 탐색"
    print(f"PWA 검사: {offline['totalFiles']}개 파일 · "
          f"{offline['totalBytes'] / 1048576:.1f} MiB · {scope} 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
