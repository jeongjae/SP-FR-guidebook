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

    def test_day32_versailles_excursion(self):
        payload = load_day(32)
        stops = {stop["id"]: stop for stop in payload["stops"]}
        self.assertIn("check", {s["type"] for s in stops["versailles-transfer"]["executionStatuses"]})
        self.assertIn("book", {s["type"] for s in stops["versailles-palace"]["executionStatuses"]})
        self.assertIn("book", {s["type"] for s in stops["versailles-lunch"]["executionStatuses"]})
        self.assertTrue(stops["trianon-hamlet"]["optional"])
        self.assertIn("book", {s["type"] for s in stops["paris-return"]["executionStatuses"]})
        rendered = self.rendered(32)
        self.assertIn("Versailles", rendered)
        self.assertIn("La Flottille", rendered)
        self.assertIn("Trianon", rendered)
        self.assertIn("Le Grand Pan", rendered)
        self.assertNotIn("Musée d&#x27;Orsay", rendered)

    def test_day33_orangerie_and_fashion_week(self):
        payload = load_day(33)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # User confirmed the September 30, 10:00 ticket.
        orangerie_statuses = {s["type"] for s in stops["orangerie"]["executionStatuses"]}
        self.assertIn("confirmed", orangerie_statuses)
        self.assertNotIn("book", orangerie_statuses)
        self.assertEqual("10:00", stops["orangerie"]["start"])
        self.assertEqual("11:30", stops["orangerie"]["end"])
        self.assertNotIn("petit-palais", stops)

        # Chez Savy lunch booking
        lunch_statuses = {s["type"] for s in stops["champs-elysees-lunch"]["executionStatuses"]}
        self.assertIn("book", lunch_statuses)
        self.assertNotIn("confirmed", lunch_statuses)

        # Grand Palais public Fashion Week route and Palais de Tokyo are optional.
        self.assertFalse(stops["avenue-montaigne"]["optional"])
        self.assertTrue(stops["grand-palais-fashion-week"]["optional"])
        fw_statuses = {s["type"] for s in stops["grand-palais-fashion-week"]["executionStatuses"]}
        self.assertIn("optional", fw_statuses)
        self.assertTrue(stops["palais-de-tokyo"]["optional"])
        self.assertEqual("14:40", stops["musee-guimet"]["start"])

        # Stéphane Martin dinner booking
        dinner_statuses = {s["type"] for s in stops["paris-return"]["executionStatuses"]}
        self.assertIn("book", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(33)
        self.assertIn("Orangerie", rendered)
        self.assertNotIn("Petit Palais", rendered)
        self.assertIn("Chez Savy", rendered)
        self.assertIn("Palais de Tokyo", rendered)
        self.assertIn("Stéphane Martin", rendered)

    def test_day34_orsay_and_rodin(self):
        payload = load_day(34)
        stops = {stop["id"]: stop for stop in payload["stops"]}
        self.assertEqual("10:30", stops["musee-d-orsay"]["start"])
        self.assertIn("confirmed", {s["type"] for s in stops["musee-d-orsay"]["executionStatuses"]})
        self.assertNotIn("book", {s["type"] for s in stops["musee-d-orsay"]["executionStatuses"]})
        self.assertEqual("14:15", stops["musee-rodin"]["start"])
        self.assertIn("ticket", {s["type"] for s in stops["musee-rodin"]["executionStatuses"]})
        self.assertTrue(stops["invalides-exterior"]["optional"])
        rendered = self.rendered(34)
        self.assertIn("Orsay", rendered)
        self.assertIn("Café Varenne", rendered)
        self.assertIn("Rodin", rendered)
        self.assertIn("Invalides", rendered)
        self.assertNotIn("Versailles", rendered)

    def test_day35_louvre_and_sawadee(self):
        payload = load_day(35)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Pichard Friday open check
        morning_statuses = {s["type"] for s in stops["morning-routine"]["executionStatuses"]}
        self.assertIn("check", morning_statuses)
        self.assertNotIn("confirmed", morning_statuses)

        # Musée du Louvre 11:00 timed entry book and PMP last use
        louvre_statuses = {s["type"] for s in stops["musee-du-louvre"]["executionStatuses"]}
        self.assertIn("book", louvre_statuses)
        self.assertNotIn("confirmed", louvre_statuses)
        self.assertEqual("11:00", stops["musee-du-louvre"]["start"])

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
        self.assertEqual("c87cff05b9a786b7419aa1edaeaf8612ff4f40c3c513250738f5bcdaba33e754", digest)


if __name__ == "__main__":
    unittest.main()
