"""Execution UX Batch 10의 Day 40–43 (Paris 마무리 및 귀국 여정) 사실·상태·동선 회귀 검사."""
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


class ExecutionUxBatch10Tests(unittest.TestCase):
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
        expected = {40: "city", 41: "city", 42: "transfer", 43: "transfer"}
        schema = json.loads((DAILY_CARDS / "schema.json").read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
        for number, day_type in expected.items():
            self.assertEqual(day_type, self.day(number).day_type)
            self.assertEqual([], list(validator.iter_errors(load_day(number))))

    def test_day40_bourse_de_commerce_and_montmartre(self):
        payload = load_day(40)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Bourse de Commerce timed entry book
        bourse_statuses = {s["type"] for s in stops["bourse-de-commerce"]["executionStatuses"]}
        self.assertIn("book", bourse_statuses)
        self.assertNotIn("confirmed", bourse_statuses)

        # Aux Crus de Bourgogne lunch booking
        lunch_statuses = {s["type"] for s in stops["halles-lunch"]["executionStatuses"]}
        self.assertIn("book", lunch_statuses)
        self.assertNotIn("confirmed", lunch_statuses)

        # Montmartre hill stroll is optional
        self.assertTrue(stops["vendanges-montmartre"]["optional"])
        montmartre_statuses = {s["type"] for s in stops["vendanges-montmartre"]["executionStatuses"]}
        self.assertIn("optional", montmartre_statuses)

        # Le Progrès dinner book
        dinner_statuses = {s["type"] for s in stops["le-progres-dinner"]["executionStatuses"]}
        self.assertIn("book", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(40)
        self.assertIn("Bourse de Commerce", rendered)
        self.assertIn("Aux Crus de Bourgogne", rendered)
        self.assertIn("Montmartre", rendered)
        self.assertIn("Le Progrès", rendered)

    def test_day41_musee_guimet_and_trocadero_sunset(self):
        payload = load_day(41)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Musée Guimet timed entry book
        guimet_statuses = {s["type"] for s in stops["musee-guimet"]["executionStatuses"]}
        self.assertIn("book", guimet_statuses)
        self.assertNotIn("confirmed", guimet_statuses)

        # Les Marches lunch booking
        lunch_statuses = {s["type"] for s in stops["iena-lunch"]["executionStatuses"]}
        self.assertIn("book", lunch_statuses)
        self.assertNotIn("confirmed", lunch_statuses)

        # MAM Paris free entry check
        mam_statuses = {s["type"] for s in stops["musee-art-moderne"]["executionStatuses"]}
        self.assertIn("check", mam_statuses)
        self.assertNotIn("confirmed", mam_statuses)

        # Trocadéro sunset is optional
        self.assertTrue(stops["trocadero-sunset"]["optional"])
        trocadero_statuses = {s["type"] for s in stops["trocadero-sunset"]["executionStatuses"]}
        self.assertIn("optional", trocadero_statuses)

        # Le Grand Pan farewell dinner booking
        dinner_statuses = {s["type"] for s in stops["farewell-dinner"]["executionStatuses"]}
        self.assertIn("book", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(41)
        self.assertIn("Guimet", rendered)
        self.assertIn("Les Marches", rendered)
        self.assertIn("Trocadéro", rendered)
        self.assertIn("Le Grand Pan", rendered)

    def test_day42_paris_checkout_and_cdg_oz502(self):
        payload = load_day(42)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Apartment checkout 11:00 confirmed
        checkout_statuses = {s["type"] for s in stops["paris-packing-checkout"]["executionStatuses"]}
        self.assertIn("confirmed", checkout_statuses)

        # Café du Commerce farewell lunch check
        lunch_statuses = {s["type"] for s in stops["farewell-lunch"]["executionStatuses"]}
        self.assertIn("check", lunch_statuses)
        self.assertNotIn("confirmed", lunch_statuses)

        # CDG taxi transfer book
        taxi_statuses = {s["type"] for s in stops["cdg-transfer"]["executionStatuses"]}
        self.assertIn("book", taxi_statuses)
        self.assertNotIn("confirmed", taxi_statuses)

        # OZ502 flight confirmed
        oz_statuses = {s["type"] for s in stops["cdg-departure"]["executionStatuses"]}
        self.assertIn("confirmed", oz_statuses)

        # Plan B contains emergency RER B transit
        self.assertIn("Plan B", payload["backup"])
        self.assertIn("RER B", payload["backup"])

        rendered = self.rendered(42)
        self.assertIn("체크아웃", rendered)
        self.assertIn("Café du Commerce", rendered)
        self.assertIn("CDG", rendered)
        self.assertIn("OZ502", rendered)

    def test_day43_return_flight_and_icn_arrival(self):
        payload = load_day(43)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Inflight confirmed
        inflight_statuses = {s["type"] for s in stops["inflight"]["executionStatuses"]}
        self.assertIn("confirmed", inflight_statuses)

        # ICN arrival check
        icn_statuses = {s["type"] for s in stops["icn"]["executionStatuses"]}
        self.assertIn("check", icn_statuses)
        self.assertNotIn("confirmed", icn_statuses)

        # Home return check
        home_statuses = {s["type"] for s in stops["home"]["executionStatuses"]}
        self.assertIn("check", home_statuses)
        self.assertNotIn("confirmed", home_statuses)

        rendered = self.rendered(43)
        self.assertIn("OZ502", rendered)
        self.assertIn("인천국제공항", rendered)

    def test_confirmed_never_coexists_with_booking_action(self):
        for path in sorted(DAILY_CARDS.glob("day-??.json")):
            for stop in json.loads(path.read_text(encoding="utf-8"))["stops"]:
                statuses = stop.get("executionStatuses", [])
                types = {status["type"] for status in statuses}
                labels = {status.get("label", "").upper() for status in statuses}
                if "book" in types or labels & {"BOOK", "ACTION REQUIRED"}:
                    self.assertNotIn("confirmed", types, f"{path.name}: {stop['id']}")

    def test_rendered_links_and_markdown_do_not_leak(self):
        for number in range(40, 44):
            rendered = self.rendered(number)
            self.assertNotIn("**", rendered)
            self.assertNotIn("[CONFIRMED]", rendered)
            self.assertNotIn('href="None"', rendered)
            self.assertNotIn('href=""', rendered)

    def test_all_43_days_coverage(self):
        cards = list(DAILY_CARDS.glob("day-??.json"))
        self.assertEqual(43, len(cards))
        for number in range(1, 44):
            day = self.day(number)
            self.assertIsNotNone(day.day_type)
            rendered = self.rendered(number)
            self.assertTrue(len(rendered) > 500)


if __name__ == "__main__":
    unittest.main()
