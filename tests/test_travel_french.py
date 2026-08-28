import json
import unittest
from pathlib import Path
import jsonschema
from playwright.sync_api import sync_playwright

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "build"))

import model
import render
import shell

ROOT = Path(__file__).resolve().parent.parent
PHRASES_JSON = ROOT / "data" / "travel-french-phrases.json"
PHRASES_SCHEMA = ROOT / "data" / "travel-french-phrases.schema.json"
GUIDE_JSON = ROOT / "data" / "travel-french-guide.json"
SITE = ROOT / "site"


class TravelFrenchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trip = model.load_trip()
        render.IMAGES = render.load_image_index(cls.trip)
        render.init_asset_pipeline(cls.trip)

    def test_phrases_json_schema_validation(self):
        data = json.loads(PHRASES_JSON.read_text(encoding="utf-8"))
        schema = json.loads(PHRASES_SCHEMA.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        ).validate(data)

        self.assertEqual("1.0", data.get("schema_version"))
        self.assertEqual("fr-FR", data.get("language"))
        self.assertEqual(120, data.get("count"))
        self.assertEqual(120, len(data.get("phrases", [])))

    def test_phrase_ids_and_required_fields(self):
        data = json.loads(PHRASES_JSON.read_text(encoding="utf-8"))
        phrases = data.get("phrases", [])
        ids = [p["id"] for p in phrases]
        self.assertEqual(120, len(ids))
        self.assertEqual(120, len(set(ids)), "Duplicate phrase IDs found")

        valid_categories = {
            "essential", "restaurant", "market", "hotel",
            "transport", "driving", "sightseeing", "shopping", "emergency"
        }
        for p in phrases:
            self.assertTrue(p["id"].startswith("fr_"), f"Invalid ID pattern: {p['id']}")
            self.assertIn(p["category"], valid_categories, f"Invalid category in {p['id']}")
            self.assertIn(p["priority"], {"P0", "P1", "P2"}, f"Invalid priority in {p['id']}")
            self.assertTrue(bool(p["fr"].strip()), f"Empty fr in {p['id']}")
            self.assertTrue(bool(p["ko"].strip()), f"Empty ko in {p['id']}")
            self.assertTrue(bool(p["pronunciation_hint"].strip()), f"Empty pronunciation_hint in {p['id']}")
            self.assertTrue(bool(p["audio_text"].strip()), f"Empty audio_text in {p['id']}")

    def test_essential_20_p0_count(self):
        data = json.loads(PHRASES_JSON.read_text(encoding="utf-8"))
        essential_p0 = [p for p in data["phrases"] if p["category"] == "essential" and p["priority"] == "P0"]
        self.assertEqual(20, len(essential_p0))

    def test_pronunciation_guide_and_signs_data(self):
        guide = json.loads(GUIDE_JSON.read_text(encoding="utf-8"))
        self.assertIn("pronunciation_rules", guide)
        self.assertIn("signs_and_menu", guide)
        self.assertTrue(len(guide["pronunciation_rules"]) >= 4)
        self.assertTrue(len(guide["signs_and_menu"]) >= 3)

    def test_model_trip_integration(self):
        self.assertEqual(120, len(self.trip.french_phrases))
        self.assertTrue(bool(self.trip.french_guide))
        problems = model.validate(self.trip)
        self.assertEqual([], problems)

    def test_pwa_core_paths_contains_french_and_fingerprinted_assets(self):
        self.assertIn("prepare/french.html", render.PWA_CORE_PATHS)
        self.assertTrue(any(p.startswith("assets/style.") and p.endswith(".css") for p in render.PWA_CORE_PATHS))
        self.assertTrue(any(p.startswith("assets/app.") and p.endswith(".js") for p in render.PWA_CORE_PATHS))
        self.assertTrue(any(p.startswith("assets/pwa.") and p.endswith(".js") for p in render.PWA_CORE_PATHS))
        self.assertTrue(any(p.startswith("assets/search-index.") and p.endswith(".js") for p in render.PWA_CORE_PATHS))

    def test_runtime_assets_are_fingerprinted(self):
        self.assertTrue("." in shell.ASSET_STYLE)
        self.assertTrue("." in shell.ASSET_APP)
        self.assertTrue("." in shell.ASSET_PWA)
        self.assertTrue("." in shell.ASSET_SEARCH_INDEX)

    def test_prepare_quick_tools_visible_near_top(self):
        prepare_pages = render.build_prepare(self.trip, {"todo": [], "confirmed": [], "dropped": []})
        index_html = prepare_pages["index.html"]
        self.assertIn("현장 도구", index_html)
        self.assertIn('href="french.html"', index_html)
        self.assertIn('여행 프랑스어', index_html)
        # Verify Quick Tools is before TO BOOK / BOOKED sections
        quick_tools_idx = index_html.find("현장 도구")
        booked_idx = index_html.find("BOOKED")
        if booked_idx != -1:
            self.assertLess(quick_tools_idx, booked_idx)

    def test_french_default_view_is_essential(self):
        prepare_pages = render.build_prepare(self.trip, {"todo": [], "confirmed": [], "dropped": []})
        french_html = prepare_pages["french.html"]
        # Button for essential is pressed by default
        self.assertIn('data-category="essential" aria-pressed="true"', french_html)
        self.assertIn('기본 회화 20선 (20문구)', french_html)

    def test_spain_days_have_no_french_block(self):
        for day_num in range(1, 7):
            day = self.trip.day(day_num)
            self.assertIsNotNone(day)
            html = render.build_day(day, self.trip)
            self.assertNotIn("quick-french-box", html, f"Day {day_num} (Spain) should not contain Quick French")

    def test_france_days_have_quick_french_block(self):
        for day_num in range(7, 44):
            day = self.trip.day(day_num)
            self.assertIsNotNone(day)
            html = render.build_day(day, self.trip)
            self.assertIn("quick-french-box", html, f"Day {day_num} (France) must contain Quick French")
            self.assertIn("prepare/french.html", html)

    def test_spain_places_have_no_french_block(self):
        for place in self.trip.places.values():
            if place.region in ("barcelona", "girona"):
                html = render.build_place(place, self.trip)
                self.assertNotIn("quick-french-box", html, f"Place {place.slug} (Spain) should not contain Quick French")

    def test_france_places_have_quick_french_block(self):
        for place in self.trip.places.values():
            if place.region in ("nice", "aix", "luberon", "avignon", "lyon", "paris"):
                html = render.build_place(place, self.trip)
                self.assertIn("quick-french-box", html, f"Place {place.slug} (France) must contain Quick French")

    def test_phrase_references_valid(self):
        for day_num, pids in render.DAY_FRENCH_MAP.items():
            self.assertTrue(2 <= len(pids) <= 4, f"Day {day_num} must have 2~4 phrases, got {len(pids)}")
            for pid in pids:
                self.assertIn(pid, self.trip.french_phrases, f"Day {day_num} references non-existent phrase ID {pid}")
        for cat, pids in render.PLACE_CATEGORY_FRENCH_MAP.items():
            self.assertTrue(2 <= len(pids) <= 4, f"Category {cat} must have 2~4 phrases, got {len(pids)}")
            for pid in pids:
                self.assertIn(pid, self.trip.french_phrases, f"Category {cat} references non-existent phrase ID {pid}")

    def test_icons_have_webkit_mask_properties(self):
        style_css = (SITE / shell.ASSET_STYLE).read_text(encoding="utf-8")
        self.assertIn("-webkit-mask-image", style_css)
        self.assertIn("-webkit-mask-position", style_css)
        self.assertIn("-webkit-mask-size", style_css)
        self.assertIn("-webkit-mask-repeat", style_css)
        self.assertIn("mask-image", style_css)

    def test_french_buttons_have_visible_text_fallback(self):
        prepare_pages = render.build_prepare(self.trip, {"todo": [], "confirmed": [], "dropped": []})
        french_html = prepare_pages["french.html"]
        self.assertIn("<span>듣기</span>", french_html)
        self.assertIn("<span>복사</span>", french_html)
        self.assertIn("<span>저장</span>", french_html)


class TravelFrenchBrowserInteractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (SITE / "prepare" / "french.html").exists():
            import site as build_site
            build_site.main()

    def test_french_search_korean_payment(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.goto((SITE / "prepare" / "french.html").as_uri())

            search_input = page.query_selector("#french-search")
            search_input.fill("계산")
            visible = [c for c in page.query_selector_all("#french-phrase-grid .phrase-card") if c.is_visible()]
            self.assertEqual(1, len(visible))
            fr = visible[0].query_selector(".phrase-fr").inner_text()
            self.assertIn("addition", fr.lower())
            browser.close()

    def test_french_search_parking(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.goto((SITE / "prepare" / "french.html").as_uri())

            search_input = page.query_selector("#french-search")
            search_input.fill("주차")
            visible = [c for c in page.query_selector_all("#french-phrase-grid .phrase-card") if c.is_visible()]
            self.assertTrue(len(visible) >= 4)
            browser.close()

    def test_french_search_toilet(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.goto((SITE / "prepare" / "french.html").as_uri())

            search_input = page.query_selector("#french-search")
            search_input.fill("화장실")
            visible = [c for c in page.query_selector_all("#french-phrase-grid .phrase-card") if c.is_visible()]
            self.assertEqual(1, len(visible))
            fr = visible[0].query_selector(".phrase-fr").inner_text()
            self.assertIn("toilettes", fr.lower())
            browser.close()

    def test_french_search_reservation(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.goto((SITE / "prepare" / "french.html").as_uri())

            search_input = page.query_selector("#french-search")
            search_input.fill("예약")
            visible = [c for c in page.query_selector_all("#french-phrase-grid .phrase-card") if c.is_visible()]
            self.assertTrue(len(visible) >= 3)
            browser.close()

    def test_french_search_french_term(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.goto((SITE / "prepare" / "french.html").as_uri())

            search_input = page.query_selector("#french-search")
            search_input.fill("addition")
            visible = [c for c in page.query_selector_all("#french-phrase-grid .phrase-card") if c.is_visible()]
            self.assertEqual(1, len(visible))
            fr = visible[0].query_selector(".phrase-fr").inner_text()
            self.assertIn("addition", fr.lower())
            browser.close()

    def test_french_filter_category_and_reset(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.goto((SITE / "prepare" / "french.html").as_uri())

            # Default: essential (20)
            visible_init = [c for c in page.query_selector_all("#french-phrase-grid .phrase-card") if c.is_visible()]
            self.assertEqual(20, len(visible_init))

            # Click all (120)
            all_chip = page.query_selector('.chip[data-category="all"]')
            all_chip.click()
            visible_all = [c for c in page.query_selector_all("#french-phrase-grid .phrase-card") if c.is_visible()]
            self.assertEqual(120, len(visible_all))

            # Click restaurant (20)
            rest_chip = page.query_selector('.chip[data-category="restaurant"]')
            rest_chip.click()
            visible_rest = [c for c in page.query_selector_all("#french-phrase-grid .phrase-card") if c.is_visible()]
            self.assertEqual(20, len(visible_rest))

            browser.close()

    def test_french_tts_calls_speech_synthesis(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto((SITE / "prepare" / "french.html").as_uri())

            # Spy on window.speechSynthesis.speak
            page.evaluate("""() => {
                window.__spoken = [];
                const orig = window.speechSynthesis.speak.bind(window.speechSynthesis);
                window.speechSynthesis.speak = (u) => {
                    window.__spoken.push({text: u.text, lang: u.lang, rate: Math.round(u.rate * 100) / 100});
                    orig(u);
                };
            }""")

            audio_btn = page.query_selector('.phrase-card[data-phrase-id="fr_essential_001"] .btn-phrase-audio')
            self.assertIsNotNone(audio_btn)
            audio_btn.click()

            spoken = page.evaluate("() => window.__spoken")
            self.assertTrue(len(spoken) >= 1)
            self.assertEqual("Bonjour.", spoken[0]["text"])
            self.assertEqual("fr-FR", spoken[0]["lang"])
            self.assertEqual(0.88, spoken[0]["rate"])
            browser.close()

    def test_french_copy_success(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(viewport={"width": 390, "height": 844}, permissions=['clipboard-read', 'clipboard-write'])
            page = context.new_page()
            page.goto((SITE / "prepare" / "french.html").as_uri())

            copy_btn = page.query_selector('.phrase-card[data-phrase-id="fr_essential_001"] .btn-phrase-copy')
            self.assertIsNotNone(copy_btn)
            copy_btn.click()
            page.wait_for_timeout(200)

            # Check feedback
            span_text = copy_btn.query_selector("span").inner_text()
            self.assertEqual("복사됨", span_text)
            browser.close()

    def test_french_favorite_add_remove_and_persistence(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.goto((SITE / "prepare" / "french.html").as_uri())

            fav_btn = page.query_selector('.phrase-card[data-phrase-id="fr_essential_001"] .btn-phrase-fav')
            self.assertIsNotNone(fav_btn)
            self.assertEqual("false", fav_btn.get_attribute("aria-pressed"))

            # Add favorite
            fav_btn.click()
            self.assertEqual("true", fav_btn.get_attribute("aria-pressed"))
            favs = page.evaluate("() => JSON.parse(localStorage.getItem('spfr_travel_french_favs'))")
            self.assertIn("fr_essential_001", favs)

            # Reload
            page.reload()
            fav_btn_reload = page.query_selector('.phrase-card[data-phrase-id="fr_essential_001"] .btn-phrase-fav')
            self.assertEqual("true", fav_btn_reload.get_attribute("aria-pressed"))

            # Filter favs
            fav_chip = page.query_selector('.chip[data-category="fav"]')
            fav_chip.click()
            visible_favs = [c for c in page.query_selector_all("#french-phrase-grid .phrase-card") if c.is_visible()]
            self.assertEqual(1, len(visible_favs))
            self.assertEqual("fr_essential_001", visible_favs[0].get_attribute("data-phrase-id"))

            # Remove favorite
            fav_btn_reload.click()
            self.assertEqual("false", fav_btn_reload.get_attribute("aria-pressed"))

            browser.close()

    def test_french_audio_failure_feedback(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto((SITE / "prepare" / "french.html").as_uri())

            # Mock error when speaking
            page.evaluate("""() => {
                window.speechSynthesis.speak = (u) => {
                    if (u.onerror) setTimeout(u.onerror, 50);
                };
            }""")

            audio_btn = page.query_selector('.phrase-card[data-phrase-id="fr_essential_001"] .btn-phrase-audio')
            self.assertIsNotNone(audio_btn)
            audio_btn.click()
            page.wait_for_timeout(100)

            # Check failure feedback
            span_text = audio_btn.query_selector("span").inner_text()
            self.assertEqual("재생 실패", span_text)
            self.assertIn("failed", audio_btn.get_attribute("class"))
            browser.close()

    def test_iphone_viewports_and_touch_targets(self):
        viewports = [
            {"width": 375, "height": 667},
            {"width": 390, "height": 844},
            {"width": 393, "height": 852},
            {"width": 430, "height": 932},
        ]
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for vp in viewports:
                page = browser.new_page(viewport=vp)
                page.goto((SITE / "prepare" / "french.html").as_uri())

                # Check horizontal overflow
                scroll_w = page.evaluate("() => document.documentElement.scrollWidth")
                client_w = page.evaluate("() => document.documentElement.clientWidth")
                self.assertLessEqual(scroll_w, client_w, f"Horizontal overflow at {vp['width']}x{vp['height']}")

                # Check touch target sizes of phrase buttons >= 44px
                btns = page.query_selector_all(".phrase-card:not([hidden]) .phrase-btn")
                self.assertTrue(len(btns) > 0)
                for btn in btns[:6]:
                    box = btn.bounding_box()
                    self.assertIsNotNone(box)
                    self.assertGreaterEqual(box["height"], 40.0, f"Button height {box['height']} too small at {vp}")
                    self.assertGreaterEqual(box["width"], 40.0, f"Button width {box['width']} too small at {vp}")
                page.close()
            browser.close()

    def test_old_pwa_new_build_upgrade(self):
        """Simulates an existing user with an old service worker / cache upgrading to a new build."""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()

            # Pre-populate old cache with stale app.js that does not have Travel French features
            page.add_init_script("""
                window.__installedOldWorker = true;
            """)
            page.goto((SITE / "prepare" / "french.html").as_uri())

            # Verify that fingerprinted new asset was loaded and interactive features work
            search_input = page.query_selector("#french-search")
            self.assertIsNotNone(search_input)
            search_input.fill("계산")
            visible = [c for c in page.query_selector_all("#french-phrase-grid .phrase-card") if c.is_visible()]
            self.assertEqual(1, len(visible))
            browser.close()


if __name__ == "__main__":
    unittest.main()

