"""Execution UX Batch 03의 Day 8–11 사실·상태·교통 회귀 검사."""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote_plus

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))

import model  # noqa: E402
import render  # noqa: E402


class ExecutionUxBatch03Tests(unittest.TestCase):
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
        expected = {8: "city", 9: "transfer", 10: "transfer", 11: "transfer"}
        schema = json.loads(
            (ROOT / "data" / "daily-cards" / "schema.json").read_text(encoding="utf-8")
        )
        validator = jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        )
        for number, day_type in expected.items():
            self.assertEqual(day_type, self.day(number).day_type)
            payload = json.loads(
                (ROOT / "data" / "daily-cards" / f"day-{number:02d}.json")
                .read_text(encoding="utf-8")
            )
            self.assertEqual([], list(validator.iter_errors(payload)))

    def test_day08_nice_facts_and_optional_dinner(self):
        day = self.rendered(8)
        self.assertIn("식품·청과·수산은 06:00~14:30", day)
        self.assertIn("꽃시장은 06:00~17:30", day)
        self.assertIn("08:30~20:00", day)
        self.assertIn("13 rue Bavastro", day)
        self.assertIn("17:30~22:00", day)
        self.assertIn("워크인 전용", day)
        self.assertNotIn("Chez Pipo 쪽으로 잡는다", day)
        self.assertNotIn("무료 입장 (엘리베이터 무료 운영)", day)

        stops = {stop.id: stop for stop in self.day(8).stops}
        self.assertIsNone(stops["castle-hill"].reservation)
        self.assertEqual({"optional"}, {x.type for x in stops["port-lympia"].execution_statuses})
        self.assertEqual({"optional"}, {x.type for x in stops["chez-pipo"].execution_statuses})
        self.assertIn("Chez Pipo", unquote_plus(render.stop_map_url(stops["chez-pipo"])))

    def test_day09_market_booking_and_rain_plan(self):
        day = self.rendered(9)
        self.assertIn("일요일 07:30~13:00", day)
        self.assertIn("일요일 점심 주문 시간 12:15~13:30", day)
        self.assertIn("실제 예약 confirmation 없음", day)
        self.assertIn("Musée Picasso(일요일 10:00~18:00)", day)
        self.assertEqual(
            {"book"},
            {x.type for x in {s.id: s for s in self.day(9).stops}["le-figuier-de-saint-esprit"].execution_statuses},
        )
        self.assertEqual(
            {"optional"},
            {x.type for x in {s.id: s for s in self.day(9).stops}["croisette"].execution_statuses},
        )

    def test_day10_condamine_guard_meals_and_ter(self):
        day = self.rendered(10)
        self.assertIn("11:55 근위병 교대식", day)
        self.assertIn("Café de Paris Monte-Carlo", day)
        self.assertIn("2026 리노베이션으로 이용 불가", day)
        self.assertIn("Restaurant Les Sablettes Beach", day)
        self.assertNotIn("Marché de la Condamine 또는", day)
        self.assertNotIn("Le Petit Port", day)

        stops = {stop.id: stop for stop in self.day(10).stops}
        self.assertEqual(
            {"check", "unavailable"},
            {x.type for x in stops["monaco-port-lunch"].execution_statuses},
        )
        self.assertIn("Café de Paris", unquote_plus(render.stop_map_url(stops["monaco-port-lunch"])))
        self.assertIn("Gare de Menton", unquote_plus(render.stop_map_url(stops["monaco-menton-transfer"])))

    def test_day11_prices_hours_and_real_connections(self):
        day = self.rendered(11)
        self.assertIn("성인 €18", day)
        self.assertIn("11:00~17:30", day)
        self.assertIn("점심 12:00~15:00", day)
        self.assertIn("Jardin Exotique 성인 €10", day)
        self.assertIn("15 → Beaulieu/Baie des Fourmis → 83", day)
        self.assertIn("82 또는 602", day)
        self.assertIn("Nice Vauban", day)
        self.assertIn("Tram L1/연결교통", day)
        self.assertNotIn("82번 버스 25분", day)
        self.assertNotIn("현장 (€7)", day)

        stops = {stop.id: stop for stop in self.day(11).stops}
        self.assertEqual({"ticket"}, {x.type for x in stops["villa-ephrussi"].execution_statuses})
        self.assertEqual({"book", "check"}, {x.type for x in stops["restaurant-beatrice"].execution_statuses})
        self.assertEqual({"ticket"}, {x.type for x in stops["eze-village"].execution_statuses})
        self.assertIn("Èze Village", unquote_plus(render.stop_map_url(stops["villa-eze-transfer"])))
        self.assertIn("12 Rue Verdi", unquote_plus(render.stop_map_url(stops["eze-nice-transfer"])))

    def test_transfer_legs_are_major_and_have_route_actions(self):
        self.assertEqual(3, self.rendered(9).count("tl-leg-major"))
        self.assertEqual(3, self.rendered(10).count("tl-leg-major"))
        self.assertEqual(4, self.rendered(11).count("tl-leg-major"))
        for number in (9, 10, 11):
            day = self.rendered(number)
            self.assertIn("다음 목적지", day)
            self.assertRegex(day, r'class="tl-leg-action"[^>]+google\.com/maps')

    def test_action_links_status_semantics_and_markdown(self):
        for number in (8, 9, 10, 11):
            day = self.rendered(number)
            self.assertRegex(day, r'class="action-actions btn-row">\s*<a[^>]+google\.com/maps')
            self.assertIn('class="tl-actions btn-row"', day)
            self.assertNotIn('<span class="badge badge-caution">예약</span>', day)
            self.assertNotRegex(day, re.compile(r">[^<]*\*\*[^<]*<"))

        self.assertIn("chezpipo.fr", self.rendered(8))
        self.assertIn("montecarlosbm.com", self.rendered(10))
        self.assertIn("menton-riviera-merveilles.fr", self.rendered(10))


if __name__ == "__main__":
    unittest.main()
