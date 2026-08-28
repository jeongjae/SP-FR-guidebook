import json
import unittest
from pathlib import Path
import jsonschema

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "build"))

import model
import render

ROOT = Path(__file__).resolve().parent.parent
PHRASES_JSON = ROOT / "data" / "travel-french-phrases.json"
PHRASES_SCHEMA = ROOT / "data" / "travel-french-phrases.schema.json"
GUIDE_JSON = ROOT / "data" / "travel-french-guide.json"


class TravelFrenchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trip = model.load_trip()
        render.IMAGES = render.load_image_index(cls.trip)

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

    def test_pwa_core_paths_contains_french(self):
        self.assertIn("prepare/french.html", render.PWA_CORE_PATHS)

    def test_prepare_pages_generation(self):
        prepare_pages = render.build_prepare(self.trip, {"todo": [], "confirmed": [], "dropped": []})
        self.assertIn("french.html", prepare_pages)
        french_html = prepare_pages["french.html"]
        self.assertIn("여행 프랑스어", french_html)
        self.assertIn("french-search", french_html)
        self.assertIn("french-filter-chips", french_html)
        self.assertIn("french-phrase-grid", french_html)
        self.assertIn("10분 발음", french_html)
        self.assertIn("표지판", french_html)

        # Check all 120 phrases are present in prepare/french.html
        for pid in self.trip.french_phrases:
            self.assertIn(f'data-phrase-id="{pid}"', french_html)

        # Check link in prepare/index.html
        index_html = prepare_pages["index.html"]
        self.assertIn('href="french.html"', index_html)

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

    def test_day_french_map_all_ids_valid(self):
        for day_num, pids in render.DAY_FRENCH_MAP.items():
            self.assertTrue(2 <= len(pids) <= 4, f"Day {day_num} must have 2~4 phrases, got {len(pids)}")
            for pid in pids:
                self.assertIn(pid, self.trip.french_phrases, f"Day {day_num} references non-existent phrase ID {pid}")

    def test_place_category_french_map_all_ids_valid(self):
        for cat, pids in render.PLACE_CATEGORY_FRENCH_MAP.items():
            self.assertTrue(2 <= len(pids) <= 4, f"Category {cat} must have 2~4 phrases, got {len(pids)}")
            for pid in pids:
                self.assertIn(pid, self.trip.french_phrases, f"Category {cat} references non-existent phrase ID {pid}")


if __name__ == "__main__":
    unittest.main()
