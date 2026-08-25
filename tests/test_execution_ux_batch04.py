"""Execution UX Batch 04의 Day 12–15 사실·상태·동선 회귀 검사."""
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
    return json.loads(
        (DAILY_CARDS / f"day-{number:02d}.json").read_text(encoding="utf-8")
    )


def semantic_projection(day: dict) -> dict:
    top_fields = (
        "day", "date", "city", "title", "startTime", "endTime",
        "totalDuration", "totalDistance", "transport", "backup",
    )
    stop_fields = (
        "id", "order", "start", "end", "name", "category", "optional", "place_ref",
    )
    leg_fields = ("from", "to", "mode", "duration", "distance", "line")
    return {
        **{field: day.get(field) for field in top_fields},
        "stops": [
            {field: stop.get(field) for field in stop_fields} for stop in day["stops"]
        ],
        "legs": [
            {field: leg.get(field) for field in leg_fields} for leg in day["legs"]
        ],
    }


class ExecutionUxBatch04Tests(unittest.TestCase):
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
        expected = {12: "driving", 13: "city", 14: "driving", 15: "transfer"}
        schema = json.loads((DAILY_CARDS / "schema.json").read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        )
        for number, day_type in expected.items():
            self.assertEqual(day_type, self.day(number).day_type)
            self.assertEqual([], list(validator.iter_errors(load_day(number))))

    def test_day12_confirmed_values_and_optional_grasse(self):
        stops = {stop.id: stop for stop in self.day(12).stops}
        self.assertEqual(
            {"confirmed", "check", "caution"},
            {status.type for status in stops["nice-station-pickup"].execution_statuses},
        )
        self.assertNotIn(
            "confirmed", {status.type for status in stops["saint-paul"].execution_statuses}
        )
        self.assertTrue(stops["grasse"].optional)
        self.assertEqual(
            {"optional"}, {status.type for status in stops["grasse"].execution_statuses}
        )
        rendered = self.rendered(12)
        self.assertIn("20 boulevard Fragonard", rendered)
        self.assertIn("Parking Indigo CRESP", unquote_plus(render.stop_map_url(stops["grasse"])))
        self.assertIn("12 Rue Verdi", unquote_plus(render.stop_map_url(stops["nice-checkout"])))
        self.assertIn("2 Place Coimbra", unquote_plus(render.stop_map_url(stops["aix-checkin"])))
        self.assertIn("Fondation Maeght 내부관람은 추가하지 않는다", rendered)

    def test_day13_market_atelier_and_granet_facts(self):
        stops = {stop.id: stop for stop in self.day(13).stops}
        rendered = self.rendered(13)
        self.assertIn("Place Richelme의 매일 아침 식품시장", rendered)
        self.assertIn("Places Comtales", rendered)
        self.assertIn("09:00–18:00", rendered)
        self.assertIn("€9.50", rendered)
        self.assertEqual(
            {"book"}, {status.type for status in stops["atelier-des-lauves"].execution_statuses}
        )
        self.assertIn("일반 €14", rendered)
        self.assertIn("Paul McCartney", rendered)
        self.assertEqual(
            {"ticket"}, {status.type for status in stops["musee-granet"].execution_statuses}
        )
        self.assertNotIn("일반 €8", rendered)

    def test_day14_three_calanques_parking_and_unbooked_lunch(self):
        stops = {stop.id: stop for stop in self.day(14).stops}
        rendered = self.rendered(14)
        self.assertIn("3 Calanques", rendered)
        self.assertIn("약 1시간 코스", rendered)
        self.assertIn("연중 운행 Bus 372", rendered)
        self.assertNotIn("Gorguettes 셔틀은 9월 주말", rendered)
        self.assertNotIn("8 Calanques로", stops["calanques"].name)
        self.assertEqual(
            {"book"}, {status.type for status in stops["cassis"].execution_statuses}
        )
        self.assertIsNone(stops["cassis"].reservation)
        self.assertTrue(stops["cassis-port-miou"].optional)
        self.assertIn(
            "Parking relais des Gorguettes",
            unquote_plus(render.stop_map_url(stops["aix-depart"])),
        )

    def test_day15_ter_fish_market_mucem_and_optional_vallon(self):
        stops = {stop.id: stop for stop in self.day(15).stops}
        rendered = self.rendered(15)
        self.assertIn("Quai de la Fraternité", rendered)
        self.assertIn("매일 아침", rendered)
        self.assertNotIn("토요 아침 어시장", rendered)
        self.assertIn("10:00–19:00", rendered)
        self.assertIn("폐관 45분 전", rendered)
        self.assertEqual(
            {"ticket"}, {status.type for status in stops["fort-saint-jean"].execution_statuses}
        )
        self.assertIn("RTM 60번", rendered)
        self.assertTrue(stops["vallon-des-auffes"].optional)
        self.assertEqual(
            {"optional"}, {status.type for status in stops["vallon-des-auffes"].execution_statuses}
        )

    def test_confirmed_never_coexists_with_booking_action(self):
        for path in sorted(DAILY_CARDS.glob("day-??.json")):
            for stop in json.loads(path.read_text(encoding="utf-8"))["stops"]:
                statuses = stop.get("executionStatuses", [])
                types = {status["type"] for status in statuses}
                labels = {status.get("label", "").upper() for status in statuses}
                if "book" in types or labels & {"BOOK", "ACTION REQUIRED"}:
                    self.assertNotIn("confirmed", types, f"{path.name}: {stop['id']}")

    def test_major_route_legs_and_actions(self):
        self.assertEqual(3, self.rendered(12).count("tl-leg-major"))
        self.assertEqual(2, self.rendered(14).count("tl-leg-major"))
        self.assertGreaterEqual(self.rendered(15).count("tl-leg-major"), 2)
        for number in (12, 14, 15):
            self.assertIn("다음 목적지", self.rendered(number))
        day15 = self.rendered(15)
        self.assertIn("Marseille Saint-Charles", day15)
        self.assertIn("Gare%20d%27Aix-en-Provence", day15)

    def test_day16_to_19_itinerary_semantics_are_unchanged(self):
        expected = {
            16: "00e70092006f0aca75c8990c387b3293ae76142ae01414bba848da0577ad61a8",
            17: "5592e3ca8d0caf4935360e25d6e09ffe24f94244f769e142b040eecda3f3198c",
            18: "6da8f397f598e1a7c88da690d0e6fab7d362c13689f4dbd646b7d15f6a872c69",
            19: "04d1eb9d4c59c4badf449e0046d3b3dc581c223d5b1e9e085dac93c0b5116cee",
        }
        for number, digest in expected.items():
            payload = json.dumps(
                semantic_projection(load_day(number)),
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
            self.assertEqual(digest, hashlib.sha256(payload).hexdigest())


if __name__ == "__main__":
    unittest.main()
