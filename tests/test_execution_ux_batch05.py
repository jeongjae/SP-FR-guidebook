"""Execution UX Batch 05의 Day 20–23 사실·상태·동선 회귀 검사."""
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


class ExecutionUxBatch05Tests(unittest.TestCase):
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
        expected = {20: "driving", 21: "transfer", 22: "city", 23: "transfer"}
        schema = json.loads((DAILY_CARDS / "schema.json").read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
        for number, day_type in expected.items():
            self.assertEqual(day_type, self.day(number).day_type)
            self.assertEqual([], list(validator.iter_errors(load_day(number))))

    def test_day20_hard_stop_return_anchor_and_vehicle_flow(self):
        payload = load_day(20)
        stops = {stop["id"]: stop for stop in payload["stops"]}
        self.assertEqual("15:45", stops["maison-carree"]["end"])
        self.assertIn("15:45 HARD STOP", json.dumps(stops["maison-carree"], ensure_ascii=False))
        self.assertEqual("18:30", stops["avignon-tgv"]["end"])
        self.assertEqual({"confirmed", "caution"}, {s["type"] for s in stops["avignon-tgv"]["executionStatuses"]})
        rendered = self.rendered(20)
        for text in ("Uzès", "Pont du Gard", "Nîmes", "주유", "Hertz"):
            self.assertIn(text, rendered)
        routes = json.loads((ROOT / "data" / "map-queries.json").read_text(encoding="utf-8"))["routes"]
        self.assertIn("Parking Cordeliers", routes["day-20:avignon-depart"]["destination"])
        self.assertIn("Parking Rive Gauche", routes["day-20:uzes"]["destination"])
        self.assertIn("Parking Arènes", routes["day-20:pont-du-gard-lunch"]["destination"])
        self.assertIn("Hertz", routes["day-20:avignon-tgv"]["destination"])

    def test_pont_du_gard_third_level_is_not_free_visit(self):
        stop = {s.id: s for s in self.day(20).stops}["pont-du-gard"]
        text = f"{stop.summary} {stop.execution_note}"
        self.assertIn("1층", text)
        self.assertIn("자유관람이 아니다", text)
        self.assertIn("가이드", text)
        self.assertNotIn("3층 자유", text)

    def test_day21_live_ter_is_check_not_confirmed(self):
        stops = {s.id: s for s in self.day(21).stops}
        for stop_id in ("avignon-centre", "avignon-return"):
            types = {status.type for status in stops[stop_id].execution_statuses}
            self.assertEqual({"check"}, types)
        rendered = self.rendered(21)
        self.assertIn("LIVE TRAIN CHECK", rendered)
        self.assertNotIn("08:45 TER 탑승", rendered)

    def test_day22_ticket_semantics_and_optional_deletion(self):
        stops = {s.id: s for s in self.day(22).stops}
        self.assertEqual(set(), {s.type for s in stops["les-halles"].execution_statuses})
        self.assertEqual(set(), {s.type for s in stops["rocher-doms"].execution_statuses})
        self.assertEqual({"ticket"}, {s.type for s in stops["palais"].execution_statuses})
        self.assertEqual({"ticket"}, {s.type for s in stops["pont"].execution_statuses})
        self.assertEqual({"optional"}, {s.type for s in stops["vieil-avignon"].execution_statuses})

    def test_day23_transfer_milestones_and_confirmed_train(self):
        stops = {s.id: s for s in self.day(23).stops}
        self.assertEqual(["avignon-checkout", "part-dieu", "lyon-checkin"], [s.id for s in self.day(23).stops[:3]])
        self.assertIn("confirmed", {s.type for s in stops["part-dieu"].execution_statuses})
        self.assertTrue(stops["ainay-walk"].optional)
        route = json.loads((ROOT / "data" / "map-queries.json").read_text(encoding="utf-8"))["routes"]["day-23:lyon-checkin"]
        self.assertIn("81-85 Cours Albert Thomas", route["destination"])
        self.assertIn("Place Béraudier", route["origin"])

    def test_confirmed_never_coexists_with_booking_action(self):
        for path in sorted(DAILY_CARDS.glob("day-??.json")):
            for stop in json.loads(path.read_text(encoding="utf-8"))["stops"]:
                statuses = stop.get("executionStatuses", [])
                types = {status["type"] for status in statuses}
                labels = {status.get("label", "").upper() for status in statuses}
                if "book" in types or labels & {"BOOK", "ACTION REQUIRED"}:
                    self.assertNotIn("confirmed", types, f"{path.name}: {stop['id']}")

    def test_rendered_links_and_markdown_do_not_leak(self):
        for number in range(20, 24):
            rendered = self.rendered(number)
            self.assertNotIn("**", rendered)
            self.assertNotIn("[CONFIRMED]", rendered)
            self.assertNotIn('href="None"', rendered)
            self.assertNotIn('href=""', rendered)
        day20 = self.rendered(20)
        self.assertIn("Hertz", unquote_plus(day20))

    def test_day24_onward_semantics_are_unchanged(self):
        payload = [semantic_projection(load_day(number)) for number in range(24, 44)]
        digest = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual("1eb888b4ff3ef3b4b7dd3495ccaa757fd0ddd5ecd21f26e576a859c8dd9c8a77", digest)


if __name__ == "__main__":
    unittest.main()
