"""Execution UX Batch 07의 Day 28–31 (Paris 장기체류 전반) 사실·상태·동선 회귀 검사."""
from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote_plus

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


class ExecutionUxBatch07Tests(unittest.TestCase):
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
        expected = {28: "city", 29: "city", 30: "city", 31: "city"}
        schema = json.loads((DAILY_CARDS / "schema.json").read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
        for number, day_type in expected.items():
            self.assertEqual(day_type, self.day(number).day_type)
            self.assertEqual([], list(validator.iter_errors(load_day(number))))

    def test_day28_city_bus_and_grand_palais(self):
        payload = load_day(28)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Pichard Friday check
        pichard_statuses = {s["type"] for s in stops["morning-routine"]["executionStatuses"]}
        self.assertIn("check", pichard_statuses)
        self.assertNotIn("confirmed", pichard_statuses)

        # Tootbus ticket
        bus_statuses = {s["type"] for s in stops["city-bus-tour"]["executionStatuses"]}
        self.assertIn("ticket", bus_statuses)

        # Grand Palais timed entry book
        palais_statuses = {s["type"] for s in stops["grand-palais-cezanne"]["executionStatuses"]}
        self.assertIn("book", palais_statuses)
        self.assertNotIn("confirmed", palais_statuses)

        # Café du Commerce open check
        dinner_statuses = {s["type"] for s in stops["paris-return"]["executionStatuses"]}
        self.assertIn("check", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(28)
        self.assertIn("Tootbus", rendered)
        self.assertIn("Grand Palais", rendered)
        self.assertIn("Café du Commerce", rendered)

    def test_day29_luxembourg_and_bouillon_racine(self):
        payload = load_day(29)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Saturday Marché Lecourbe check
        market_statuses = {s["type"] for s in stops["morning-routine"]["executionStatuses"]}
        self.assertIn("check", market_statuses)
        self.assertNotIn("confirmed", market_statuses)

        # Musée du Luxembourg Warhol timed entry book
        lux_statuses = {s["type"] for s in stops["luxembourg-warhol"]["executionStatuses"]}
        self.assertIn("book", lux_statuses)
        self.assertNotIn("confirmed", lux_statuses)

        # Notre-Dame compact walk is optional
        self.assertTrue(stops["notre-dame-compact"]["optional"])
        nd_statuses = {s["type"] for s in stops["notre-dame-compact"]["executionStatuses"]}
        self.assertIn("optional", nd_statuses)

        # Bouillon Racine booking required
        dinner_statuses = {s["type"] for s in stops["bouillon-racine-dinner"]["executionStatuses"]}
        self.assertIn("book", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(29)
        self.assertIn("Musée du Luxembourg", rendered)
        self.assertIn("Saint-Germain-des-Prés", rendered)
        self.assertIn("Bouillon Racine", rendered)

    def test_day30_orangerie_and_marche_convention(self):
        payload = load_day(30)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Sunday Marché Convention check
        market_statuses = {s["type"] for s in stops["morning-routine"]["executionStatuses"]}
        self.assertIn("check", market_statuses)
        self.assertNotIn("confirmed", market_statuses)

        # Musée de l'Orangerie timed entry book (Sunday visit mandatory due to Tuesday closure)
        orangerie_statuses = {s["type"] for s in stops["orangerie"]["executionStatuses"]}
        self.assertIn("book", orangerie_statuses)
        self.assertNotIn("confirmed", orangerie_statuses)

        # Opéra Garnier walk is optional
        self.assertTrue(stops["opera-garnier-district"]["optional"])
        opera_statuses = {s["type"] for s in stops["opera-garnier-district"]["executionStatuses"]}
        self.assertIn("optional", opera_statuses)

        # Bouillon Chartier Montparnasse no-reservation check
        dinner_statuses = {s["type"] for s in stops["paris-return"]["executionStatuses"]}
        self.assertIn("check", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(30)
        self.assertIn("Orangerie", rendered)
        self.assertIn("Tuileries", rendered)
        self.assertIn("Palais Royal", rendered)
        self.assertIn("Bouillon Chartier", rendered)

    def test_day31_gustave_moreau_and_fashion_week(self):
        payload = load_day(31)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Pichard Monday closure check
        morning_statuses = {s["type"] for s in stops["morning-routine"]["executionStatuses"]}
        self.assertIn("check", morning_statuses)

        # Musée Gustave Moreau timed ticket (Monday open, Tuesday closed)
        moreau_statuses = {s["type"] for s in stops["gustave-moreau"]["executionStatuses"]}
        self.assertIn("ticket", moreau_statuses)
        self.assertNotIn("confirmed", moreau_statuses)

        # Au Petit Riche Monday lunch booking
        lunch_statuses = {s["type"] for s in stops["opera-lunch"]["executionStatuses"]}
        self.assertIn("book", lunch_statuses)
        self.assertNotIn("confirmed", lunch_statuses)

        # Fashion Week & Marais is optional
        self.assertTrue(stops["fashion-week-marais"]["optional"])
        marais_statuses = {s["type"] for s in stops["fashion-week-marais"]["executionStatuses"]}
        self.assertIn("optional", marais_statuses)

        # Guylas Persian dinner is check (NOT confirmed)
        dinner_statuses = {s["type"] for s in stops["paris-return"]["executionStatuses"]}
        self.assertIn("check", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(31)
        self.assertIn("Gustave Moreau", rendered)
        self.assertIn("Au Petit Riche", rendered)
        self.assertIn("Fashion Week", rendered)
        self.assertIn("Guylas", rendered)

    def test_confirmed_never_coexists_with_booking_action(self):
        for path in sorted(DAILY_CARDS.glob("day-??.json")):
            for stop in json.loads(path.read_text(encoding="utf-8"))["stops"]:
                statuses = stop.get("executionStatuses", [])
                types = {status["type"] for status in statuses}
                labels = {status.get("label", "").upper() for status in statuses}
                if "book" in types or labels & {"BOOK", "ACTION REQUIRED"}:
                    self.assertNotIn("confirmed", types, f"{path.name}: {stop['id']}")

    def test_rendered_links_and_markdown_do_not_leak(self):
        for number in range(28, 32):
            rendered = self.rendered(number)
            self.assertNotIn("**", rendered)
            self.assertNotIn("[CONFIRMED]", rendered)
            self.assertNotIn('href="None"', rendered)
            self.assertNotIn('href=""', rendered)

    def test_day32_onward_semantics_are_unchanged(self):
        payload = [semantic_projection(load_day(number)) for number in range(32, 44)]
        digest = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual("d03226f8e06a193fa920745095336ee30cee92484568f0e5a9ab12382b0bfd96", digest)


if __name__ == "__main__":
    unittest.main()
