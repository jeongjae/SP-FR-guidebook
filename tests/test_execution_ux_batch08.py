"""Execution UX Batch 08의 Day 32–35 (Paris 장기체류 중반) 사실·상태·동선 회귀 검사."""
from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
DAILY_CARDS = ROOT / "data" / "daily-cards"
sys.path.insert(0, str(ROOT / "build"))

import model  # noqa: E402
import render  # noqa: E402


def load_day(number: int) -> dict:
    return json.loads((DAILY_CARDS / f"day-{number:02d}.json").read_text(encoding="utf-8"))


def semantic_projection(day: dict) -> dict:
    top = ("day", "date", "city", "title", "startTime", "endTime", "totalDuration", "totalDistance", "transport", "backup")
    stops = ("id", "order", "start", "end", "name", "category", "optional", "place_ref")
    legs = ("from", "to", "mode", "duration", "distance", "line")
    return {
        **{key: day.get(key) for key in top},
        "stops": [{key: stop.get(key) for key in stops} for stop in day["stops"]],
        "legs": [{key: leg.get(key) for key in legs} for leg in day["legs"]],
    }


class ExecutionUxBatch08Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trip = model.load_trip()
        render.IMAGES = {"heroes": {}, "by_place": {}, "extras": {}, "dishes": {}}
        render.FACTS = model.load_facts()

    def day(self, number: int):
        day = self.trip.day(number)
        self.assertIsNotNone(day)
        return day

    def rendered(self, number: int) -> str:
        return render.build_day(self.day(number), self.trip)

    def test_day_types_and_schema(self):
        expected = {32: "city", 33: "city", 34: "city", 35: "city"}
        schema = json.loads((DAILY_CARDS / "schema.json").read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
        for number, day_type in expected.items():
            self.assertEqual(day_type, self.day(number).day_type)
            self.assertEqual([], list(validator.iter_errors(load_day(number))))

    def test_day32_orsay_and_rodin(self):
        payload = load_day(32)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Early start check
        morning_statuses = {s["type"] for s in stops["morning-routine"]["executionStatuses"]}
        self.assertIn("check", morning_statuses)

        # Musée d'Orsay timed entry book & Entrée 1 - Quai
        orsay_statuses = {s["type"] for s in stops["musee-d-orsay"]["executionStatuses"]}
        self.assertIn("book", orsay_statuses)
        self.assertNotIn("confirmed", orsay_statuses)
        orsay_detail = stops["musee-d-orsay"]["executionStatuses"][0]["detail"]
        self.assertIn("Entrée 1 - Quai", orsay_detail)
        self.assertNotIn("Entrée A1", orsay_detail)
        self.assertNotIn("Entrée A1", stops["musee-d-orsay"]["executionNote"])

        # Café Varenne lunch check (not confirmed)
        lunch_statuses = {s["type"] for s in stops["rue-du-bac-lunch"]["executionStatuses"]}
        self.assertIn("check", lunch_statuses)
        self.assertNotIn("confirmed", lunch_statuses)

        # Musée Rodin timed ticket
        rodin_statuses = {s["type"] for s in stops["musee-rodin"]["executionStatuses"]}
        self.assertIn("ticket", rodin_statuses)
        self.assertNotIn("confirmed", rodin_statuses)

        # Invalides exterior is optional
        self.assertTrue(stops["invalides-exterior"]["optional"])
        invalides_statuses = {s["type"] for s in stops["invalides-exterior"]["executionStatuses"]}
        self.assertIn("optional", invalides_statuses)

        # Café du Commerce dinner check
        dinner_statuses = {s["type"] for s in stops["paris-return"]["executionStatuses"]}
        self.assertIn("check", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(32)
        self.assertIn("Orsay", rendered)
        self.assertIn("Café Varenne", rendered)
        self.assertIn("Rodin", rendered)
        self.assertIn("Invalides", rendered)

    def test_day33_petit_palais_and_fashion_week(self):
        payload = load_day(33)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Petit Palais free entry check
        pp_statuses = {s["type"] for s in stops["petit-palais"]["executionStatuses"]}
        self.assertIn("check", pp_statuses)
        self.assertNotIn("confirmed", pp_statuses)

        # Chez Savy lunch booking
        lunch_statuses = {s["type"] for s in stops["champs-elysees-lunch"]["executionStatuses"]}
        self.assertIn("book", lunch_statuses)
        self.assertNotIn("confirmed", lunch_statuses)

        # Fashion Week & Palais de Tokyo is optional
        self.assertTrue(stops["fashion-week-montaigne"]["optional"])
        fw_statuses = {s["type"] for s in stops["fashion-week-montaigne"]["executionStatuses"]}
        self.assertIn("optional", fw_statuses)

        # Stéphane Martin dinner booking
        dinner_statuses = {s["type"] for s in stops["paris-return"]["executionStatuses"]}
        self.assertIn("book", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(33)
        self.assertIn("Petit Palais", rendered)
        self.assertIn("Chez Savy", rendered)
        self.assertIn("Palais de Tokyo", rendered)
        self.assertIn("Stéphane Martin", rendered)

    def test_day34_versailles_excursion(self):
        payload = load_day(34)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # RER C transfer check
        transfer_statuses = {s["type"] for s in stops["versailles-transfer"]["executionStatuses"]}
        self.assertIn("check", transfer_statuses)

        # Versailles Palace 10:00 timed entry book
        palace_statuses = {s["type"] for s in stops["versailles-palace"]["executionStatuses"]}
        self.assertIn("book", palace_statuses)
        self.assertNotIn("confirmed", palace_statuses)

        # La Flottille Grand Canal lunch booking
        lunch_statuses = {s["type"] for s in stops["versailles-lunch"]["executionStatuses"]}
        self.assertIn("book", lunch_statuses)
        self.assertNotIn("confirmed", lunch_statuses)

        # Versailles gardens check
        garden_statuses = {s["type"] for s in stops["versailles-gardens"]["executionStatuses"]}
        self.assertIn("check", garden_statuses)

        # Trianon & Hamlet is optional
        self.assertTrue(stops["trianon-hamlet"]["optional"])
        trianon_statuses = {s["type"] for s in stops["trianon-hamlet"]["executionStatuses"]}
        self.assertIn("optional", trianon_statuses)

        # Le Grand Pan dinner booking
        dinner_statuses = {s["type"] for s in stops["paris-return"]["executionStatuses"]}
        self.assertIn("book", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(34)
        self.assertIn("Versailles", rendered)
        self.assertIn("La Flottille", rendered)
        self.assertIn("Trianon", rendered)
        self.assertIn("Le Grand Pan", rendered)

    def test_day35_louvre_and_sawadee(self):
        payload = load_day(35)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Pichard Friday open check
        morning_statuses = {s["type"] for s in stops["morning-routine"]["executionStatuses"]}
        self.assertIn("check", morning_statuses)
        self.assertNotIn("confirmed", morning_statuses)

        # Musée du Louvre 14:00 timed entry book
        louvre_statuses = {s["type"] for s in stops["musee-du-louvre"]["executionStatuses"]}
        self.assertIn("book", louvre_statuses)
        self.assertNotIn("confirmed", louvre_statuses)

        # Cour Carrée & Seine sunset is optional
        self.assertTrue(stops["cour-carree-seine"]["optional"])
        seine_statuses = {s["type"] for s in stops["cour-carree-seine"]["executionStatuses"]}
        self.assertIn("optional", seine_statuses)

        # Sawadee Thai dinner booking
        dinner_statuses = {s["type"] for s in stops["paris-return"]["executionStatuses"]}
        self.assertIn("book", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(35)
        self.assertIn("Louvre", rendered)
        self.assertIn("Cour Carrée", rendered)
        self.assertIn("Sawadee", rendered)

    def test_confirmed_never_coexists_with_booking_action(self):
        for path in sorted(DAILY_CARDS.glob("day-??.json")):
            for stop in json.loads(path.read_text(encoding="utf-8"))["stops"]:
                statuses = stop.get("executionStatuses", [])
                types = {status["type"] for status in statuses}
                labels = {status.get("label", "").upper() for status in statuses}
                if "book" in types or labels & {"BOOK", "ACTION REQUIRED"}:
                    self.assertNotIn("confirmed", types, f"{path.name}: {stop['id']}")

    def test_rendered_links_and_markdown_do_not_leak(self):
        for number in range(32, 36):
            rendered = self.rendered(number)
            self.assertNotIn("**", rendered)
            self.assertNotIn("[CONFIRMED]", rendered)
            self.assertNotIn('href="None"', rendered)
            self.assertNotIn('href=""', rendered)

    def test_day32_to_35_semantics_are_protected(self):
        payload = [semantic_projection(load_day(number)) for number in range(32, 36)]
        digest = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual("c616b6aef5f603b59a5b76f232137cc8a1219a616a422f0249de332aa9f204da", digest)


if __name__ == "__main__":
    unittest.main()
