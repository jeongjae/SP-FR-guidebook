"""Regression guard for the 9/29 Versailles ↔ 10/1 Orsay/Rodin swap."""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "data" / "daily-cards"


def day(number: int) -> dict:
    return json.loads((CARDS / f"day-{number:02d}.json").read_text(encoding="utf-8"))


class ParisSeptember29October1SwapTests(unittest.TestCase):
    def test_day32_is_versailles_only(self):
        payload = day(32)
        ids = {stop["id"] for stop in payload["stops"]}
        self.assertEqual("2026-09-29", payload["date"])
        self.assertTrue({"versailles-palace", "versailles-gardens", "trianon-hamlet"} <= ids)
        self.assertTrue(ids.isdisjoint({"musee-d-orsay", "musee-rodin", "invalides-exterior"}))

    def test_day34_is_confirmed_orsay_and_rodin_only(self):
        payload = day(34)
        stops = {stop["id"]: stop for stop in payload["stops"]}
        self.assertEqual("2026-10-01", payload["date"])
        self.assertEqual("10:30", stops["musee-d-orsay"]["start"])
        self.assertIn("confirmed", {s["type"] for s in stops["musee-d-orsay"]["executionStatuses"]})
        self.assertIn("musee-rodin", stops)
        self.assertIn("invalides-exterior", stops)
        self.assertNotIn("versailles-palace", stops)

    def test_adjacent_and_special_visit_days_are_preserved(self):
        day33 = {stop["id"]: stop for stop in day(33)["stops"]}
        day35 = {stop["id"]: stop for stop in day(35)["stops"]}
        day39 = {stop["id"]: stop for stop in day(39)["stops"]}
        self.assertEqual("10:00", day33["orangerie"]["start"])
        self.assertIn("confirmed", {s["type"] for s in day33["orangerie"]["executionStatuses"]})
        self.assertIn("musee-du-louvre", day35)
        self.assertIn("musee-d-orsay-cassatt", day39)
        self.assertIn("Mary Cassatt", day39["musee-d-orsay-cassatt"]["name"])

    def test_route_registry_matches_each_day(self):
        routes = json.loads((ROOT / "data" / "map-queries.json").read_text(encoding="utf-8"))["routes"]
        day32 = {key.partition(":")[2] for key in routes if key.startswith("day-32:")}
        day34 = {key.partition(":")[2] for key in routes if key.startswith("day-34:")}
        self.assertIn("versailles-palace", day32)
        self.assertNotIn("musee-d-orsay", day32)
        self.assertIn("musee-d-orsay", day34)
        self.assertIn("musee-rodin", day34)
        self.assertNotIn("versailles-palace", day34)


if __name__ == "__main__":
    unittest.main()
