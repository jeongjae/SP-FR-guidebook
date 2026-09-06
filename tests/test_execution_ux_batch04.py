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
        expected = {12: "driving", 13: "driving", 14: "transfer", 15: "city", 16: "driving"}  # RS01 재배치
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
        self.assertIn("Fondation Maeght 내부관람은 추가하지 않는다", rendered)

    def test_day13_market_atelier_and_granet_facts(self):
        # RS01: 시장·아틀리에 시내일은 Day 15(9/12 토)로 이동
        stops = {stop.id: stop for stop in self.day(15).stops}
        rendered = self.rendered(15)
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
        day13_stops = {stop.id: stop for stop in self.day(13).stops}
        self.assertIn("2 Place Coimbra", unquote_plus(render.stop_map_url(day13_stops["aix-checkin"])))

    def test_day14_three_calanques_parking_and_unbooked_lunch(self):
        # RS01: Cassis일은 Day 16(9/13 일)으로 이동
        stops = {stop.id: stop for stop in self.day(16).stops}
        rendered = self.rendered(16)
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
        self.assertIn("차량 회수", stops["cassis-vehicle-return"].name)
        self.assertIn("Bus 372", stops["cassis-vehicle-return"].summary)
        self.assertIn(
            "Parking relais des Gorguettes",
            unquote_plus(render.stop_map_url(stops["aix-depart"])),
        )

    def test_day14_vehicle_retrieval_precedes_return_drive(self):
        payload = load_day(16)  # RS01: Cassis일 이동
        stop_order = {stop["id"]: stop["order"] for stop in payload["stops"]}
        self.assertLess(
            stop_order["cassis-port-miou"], stop_order["cassis-vehicle-return"]
        )
        self.assertLess(stop_order["cassis-vehicle-return"], stop_order["aix-return"])

        return_leg = next(
            leg for leg in payload["legs"] if leg["to"] == "aix-return"
        )
        self.assertEqual("car", return_leg["mode"])
        self.assertEqual("cassis-vehicle-return", return_leg["from"])

        routes = json.loads(
            (ROOT / "data" / "map-queries.json").read_text(encoding="utf-8")
        )["routes"]
        car_return = routes["day-16:cassis-vehicle-return"]
        self.assertEqual("Parking relais des Gorguettes, Cassis", car_return["origin"])
        self.assertEqual("driving", car_return["travelMode"])
        for key, route in routes.items():
            if not key.startswith("day-16:") or route["travelMode"] != "driving":
                continue
            self.assertFalse(
                route["origin"].startswith("Port-Miou")
                and "Aix" in route["destination"],
                f"invalid vehicle continuity route: {key}",
            )

    def test_day14_rendered_vehicle_retrieval_flow(self):
        rendered = self.rendered(16)  # RS01: Cassis일 이동
        port_miou = rendered.index("OPTIONAL · Port-Miou")
        retrieval = rendered.index("Gorguettes P+R 복귀 · 차량 회수")
        return_drive = rendered.index("Parking des Gorguettes ➔ Aix 귀환")
        self.assertLess(port_miou, retrieval)
        self.assertLess(retrieval, return_drive)
        self.assertIn("Cassis centre 접근 → Bus 372", rendered)
        self.assertIn("차량 회수 없이 Aix로 출발하지 않는다", rendered)

    def test_day15_ter_fish_market_mucem_and_optional_vallon(self):
        # RS01: Marseille일은 Day 14(9/11 금)로 이동
        stops = {stop.id: stop for stop in self.day(14).stops}
        rendered = self.rendered(14)
        self.assertIn("Quai de la Fraternité", rendered)
        self.assertIn("매일 아침", rendered)
        self.assertNotIn("토요 아침 어시장", rendered)
        self.assertIn("11:00–19:00", rendered)  # Mucem 9/3–11/4 시즌 (2026-08-28 공식 확인)
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
        self.assertGreaterEqual(self.rendered(12).count("tl-leg-major"), 3)
        self.assertEqual(2, self.rendered(16).count("tl-leg-major"))
        self.assertGreaterEqual(self.rendered(14).count("tl-leg-major"), 2)
        for number in (12, 14, 16):
            self.assertIn("다음 목적지", self.rendered(number))
        day14 = self.rendered(14)
        self.assertIn("Marseille Saint-Charles", day14)
        self.assertIn("Gare%20d%27Aix-en-Provence", day14)

    def test_day16_to_19_itinerary_semantics_are_unchanged(self):
        # RS01(2026-08-28) 재기준선 — Cassis(16)·Lacoste 이동일(17)·화요시장(18)·통합 도착일(19)
        expected = {
            16: "049be12552f982701209b7e7c275ba141098cd078e61b079bf00e037990335ed",
            17: "057c8cbeeb82bb2dd548b26e2f92493123aa69c6600cb42c4899568dcadc1b00",
            18: "56e05bb501dca4b2d5dd05c7c9dd7f7a38b7a1d81a5979bdde15e222505c772f",
            19: "db799c436b511b83ffe007aa2fdb7afde3f567f5772e7881c701c864158478a6",
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
