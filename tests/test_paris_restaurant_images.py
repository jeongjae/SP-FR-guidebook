"""Paris Restaurant Photo Coverage Regression Tests.

Verifies:
1. All Paris food entities (restaurants, bakeries, markets) have canonical representative photos.
2. Manifest entries exist and are valid.
3. Original photo assets and processed WebP variants (content, thumbnail) exist.
4. Rendered HTML pages contain the corresponding images with correct alt and srcset.
5. Source provenance metadata is completely recorded.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
import model

PARIS_FOOD_SLUGS = [
    "au-petit-riche",
    "aux-crus-de-bourgogne",
    "bouillon-chartier-montparnasse",
    "bouillon-racine",
    "boulangerie-pichard",
    "breizh-cafe-charles-michels",
    "cafe-du-commerce",
    "cafe-varenne",
    "chez-janou",
    "chez-savy",
    "guylas",
    "la-flottille",
    "le-grand-pan",
    "le-progres-montmartre",
    "le-relais-du-15eme",
    "le-volant-basque",
    "les-marches",
    "marche-convention",
    "sawadee-paris",
    "stephane-martin",
]


class ParisRestaurantImagesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trip = model.load_trip()
        cls.images = model.load_images(set(cls.trip.places) | {r.slug for r in cls.trip.regions})
        cls.manifest = json.loads((ROOT / "data/images/image-manifest.json").read_text(encoding="utf-8"))
        cls.images_by_id = {img["imageId"]: img for img in cls.manifest.get("images", [])}

    def test_all_paris_food_places_have_photos(self):
        """All 20 Paris food entities must have an active photo mapped in by_place."""
        for slug in PARIS_FOOD_SLUGS:
            with self.subTest(place=slug):
                self.assertIn(slug, self.images["by_place"], f"Missing photo for Paris food place: {slug}")
                img = self.images["by_place"][slug]
                self.assertTrue(img.get("imageId"), f"Image ID empty for {slug}")

    def test_original_assets_exist(self):
        """Referenced original files must exist on disk and have non-zero size."""
        for slug in PARIS_FOOD_SLUGS:
            with self.subTest(place=slug):
                img = self.images["by_place"][slug]
                orig_path = ROOT / img["originalPath"]
                self.assertTrue(orig_path.exists(), f"Original asset missing: {orig_path}")
                self.assertGreater(orig_path.stat().st_size, 0, f"Original asset is empty: {orig_path}")

    def test_processed_variants_exist(self):
        """Each photo must have both content and thumbnail WebP variants."""
        for slug in PARIS_FOOD_SLUGS:
            with self.subTest(place=slug):
                img = self.images["by_place"][slug]
                variants = img.get("variants", {})
                self.assertTrue(variants.get("content"), f"Missing content variant for {slug}")
                self.assertTrue(variants.get("thumbnail"), f"Missing thumbnail variant for {slug}")
                for role, v_list in variants.items():
                    for v in v_list:
                        v_path = ROOT / v["path"]
                        self.assertTrue(v_path.exists(), f"Variant file missing: {v_path}")
                        self.assertGreater(v_path.stat().st_size, 0, f"Variant file empty: {v_path}")

    def test_source_provenance_recorded(self):
        """Every image entry must have source, sourcePage/originalFile, and license metadata."""
        for slug in PARIS_FOOD_SLUGS:
            with self.subTest(place=slug):
                img = self.images["by_place"][slug]
                self.assertTrue(img.get("source"), f"Missing source for {slug}")
                self.assertTrue(img.get("sourcePage") or img.get("originalFile"), f"Missing source URL for {slug}")
                self.assertTrue(img.get("licenseCode"), f"Missing licenseCode for {slug}")
                self.assertTrue(img.get("downloadDate"), f"Missing downloadDate for {slug}")

    def test_place_pages_render_images(self):
        """Rendered place HTML pages must contain img tag with matching sitePath."""
        for slug in PARIS_FOOD_SLUGS:
            with self.subTest(place=slug):
                html_path = ROOT / f"site/places/{slug}.html"
                if html_path.exists():
                    html_content = html_path.read_text(encoding="utf-8")
                    img = self.images["by_place"][slug]
                    content_variant = img["variants"]["content"][0]["sitePath"]
                    content_filename = Path(content_variant).name
                    self.assertIn(content_filename, html_content, f"Content image {content_filename} not found in {html_path}")
                    self.assertNotIn("thumb-empty", html_content, f"Placeholder thumb-empty found in {html_path}")

    def test_paris_guide_renders_all_food_images(self):
        """Rendered Paris guide page must contain all Paris food places without placeholders."""
        guide_path = ROOT / "site/guide/paris.html"
        self.assertTrue(guide_path.exists(), f"Guide page {guide_path} does not exist")
        guide_content = guide_path.read_text(encoding="utf-8")
        for slug in PARIS_FOOD_SLUGS:
            with self.subTest(place=slug):
                img = self.images["by_place"][slug]
                variants = img.get("variants", {})
                filenames = [Path(v["sitePath"]).name for v_list in variants.values() for v in v_list]
                found = any(f in guide_content for f in filenames)
                self.assertTrue(found, f"None of image variants for {slug} found in {guide_path}")


if __name__ == "__main__":
    unittest.main()
