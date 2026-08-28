"""Execution UX Batch 09의 Day 36–39 (Paris 장기체류 후반) 사실·상태·동선 회귀 검사."""
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


class ExecutionUxBatch09Tests(unittest.TestCase):
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
        expected = {36: "city", 37: "city", 38: "city", 39: "city"}
        schema = json.loads((DAILY_CARDS / "schema.json").read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
        for number, day_type in expected.items():
            self.assertEqual(day_type, self.day(number).day_type)
            self.assertEqual([], list(validator.iter_errors(load_day(number))))

    def test_day36_marmottan_monet_and_passy(self):
        payload = load_day(36)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Saturday Lecourbe market check
        morning_statuses = {s["type"] for s in stops["morning-routine"]["executionStatuses"]}
        self.assertIn("check", morning_statuses)
        self.assertNotIn("confirmed", morning_statuses)

        # Musée Marmottan Monet timed entry book
        marmottan_statuses = {s["type"] for s in stops["marmottan-monet"]["executionStatuses"]}
        self.assertIn("book", marmottan_statuses)
        self.assertNotIn("confirmed", marmottan_statuses)

        # Ranelagh & Passy stroll is optional
        self.assertTrue(stops["ranelagh-passy"]["optional"])
        passy_statuses = {s["type"] for s in stops["ranelagh-passy"]["executionStatuses"]}
        self.assertIn("optional", passy_statuses)

        # Le Relais du 15ème dinner check
        dinner_statuses = {s["type"] for s in stops["paris-return"]["executionStatuses"]}
        self.assertIn("check", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(36)
        self.assertIn("Marmottan", rendered)
        self.assertIn("Ranelagh", rendered)
        self.assertIn("Le Relais du 15ème", rendered)

    def test_day37_prix_de_l_arc_de_triomphe(self):
        payload = load_day(37)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Shuttle transfer check
        transfer_statuses = {s["type"] for s in stops["longchamp-transfer"]["executionStatuses"]}
        self.assertIn("check", transfer_statuses)

        # Prix de l'Arc confirmed booking from France Galop SOT
        arc_statuses = {s["type"] for s in stops["prix-de-l-arc"]["executionStatuses"]}
        self.assertIn("confirmed", arc_statuses)
        self.assertNotIn("book", arc_statuses)
        self.assertIn("check", arc_statuses)  # RACE TIME check

        # Breizh Café dinner check
        dinner_statuses = {s["type"] for s in stops["paris-return"]["executionStatuses"]}
        self.assertIn("check", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(37)
        self.assertIn("Arc de Triomphe", rendered)
        self.assertIn("ParisLongchamp", rendered)
        self.assertIn("Breizh Café", rendered)

    def test_day38_jacquemart_andre_and_monceau(self):
        payload = load_day(38)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Morning recovery check
        morning_statuses = {s["type"] for s in stops["morning-routine"]["executionStatuses"]}
        self.assertIn("check", morning_statuses)

        # Musée Jacquemart-André timed entry book
        ja_statuses = {s["type"] for s in stops["jacquemart-andre"]["executionStatuses"]}
        self.assertIn("book", ja_statuses)
        self.assertNotIn("confirmed", ja_statuses)

        # Parc Monceau stroll is optional
        self.assertTrue(stops["parc-monceau"]["optional"])
        monceau_statuses = {s["type"] for s in stops["parc-monceau"]["executionStatuses"]}
        self.assertIn("optional", monceau_statuses)

        # Le Volant Basque dinner booking
        dinner_statuses = {s["type"] for s in stops["paris-return"]["executionStatuses"]}
        self.assertIn("book", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(38)
        self.assertIn("Jacquemart-André", rendered)
        self.assertIn("Monceau", rendered)
        self.assertIn("Le Volant Basque", rendered)

    def test_day39_convention_market_orsay_cassatt_marais(self):
        payload = load_day(39)
        stops = {stop["id"]: stop for stop in payload["stops"]}

        # Tuesday Convention market check
        morning_statuses = {s["type"] for s in stops["morning-routine"]["executionStatuses"]}
        self.assertIn("check", morning_statuses)
        self.assertNotIn("confirmed", morning_statuses)

        # Orsay Mary Cassatt opening timed entry & Entrée 1 - Quai
        orsay_statuses = {s["type"] for s in stops["musee-d-orsay-cassatt"]["executionStatuses"]}
        self.assertIn("book", orsay_statuses)
        self.assertNotIn("confirmed", orsay_statuses)
        orsay_detail = stops["musee-d-orsay-cassatt"]["executionStatuses"][0]["detail"]
        self.assertIn("Entrée 1 - Quai", orsay_detail)

        # Musée Picasso Paris is optional with timed ticket requirement
        self.assertTrue(stops["musee-picasso"]["optional"])
        picasso_statuses = {s["type"] for s in stops["musee-picasso"]["executionStatuses"]}
        self.assertIn("optional", picasso_statuses)
        self.assertIn("book", picasso_statuses)
        self.assertNotIn("confirmed", picasso_statuses)

        # Musée Carnavalet is optional
        self.assertTrue(stops["musee-carnavalet"]["optional"])
        carnavalet_statuses = {s["type"] for s in stops["musee-carnavalet"]["executionStatuses"]}
        self.assertIn("optional", carnavalet_statuses)

        # Chez Janou dinner booking
        dinner_statuses = {s["type"] for s in stops["chez-janou-dinner"]["executionStatuses"]}
        self.assertIn("book", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)

        rendered = self.rendered(39)
        self.assertIn("Mary Cassatt", rendered)
        self.assertIn("Picasso", rendered)
        self.assertIn("Carnavalet", rendered)
        self.assertIn("Chez Janou", rendered)

    def test_confirmed_never_coexists_with_booking_action(self):
        for path in sorted(DAILY_CARDS.glob("day-??.json")):
            for stop in json.loads(path.read_text(encoding="utf-8"))["stops"]:
                statuses = stop.get("executionStatuses", [])
                types = {status["type"] for status in statuses}
                labels = {status.get("label", "").upper() for status in statuses}
                if "book" in types or labels & {"BOOK", "ACTION REQUIRED"}:
                    self.assertNotIn("confirmed", types, f"{path.name}: {stop['id']}")

    def test_rendered_links_and_markdown_do_not_leak(self):
        for number in range(36, 40):
            rendered = self.rendered(number)
            self.assertNotIn("**", rendered)
            self.assertNotIn("[CONFIRMED]", rendered)
            self.assertNotIn('href="None"', rendered)
            self.assertNotIn('href=""', rendered)

    def test_day36_to_39_semantics_are_protected(self):
        payload = [semantic_projection(load_day(number)) for number in range(36, 40)]
        digest = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual("713a263b6db13e4fea85266a760906d85d033b721ea3f53dfed87498a01e5871", digest)


if __name__ == "__main__":
    unittest.main()
