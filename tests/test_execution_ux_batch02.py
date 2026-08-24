"""Execution UX Batch 02의 상태·행동·Day type·사실관계 회귀 검사."""
from __future__ import annotations

import re
import json
import sys
import unittest
from urllib.parse import unquote_plus
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))

import model  # noqa: E402
import render  # noqa: E402


class ExecutionUxBatch02Tests(unittest.TestCase):
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

    def test_batch02_day_types_are_explicit_and_extensible(self):
        self.assertEqual("transfer", self.day(1).day_type)
        self.assertEqual("city", self.day(2).day_type)
        self.assertEqual("driving", self.day(5).day_type)
        self.assertEqual("transfer", self.day(7).day_type)

    def test_batch02_sources_follow_daily_card_schema(self):
        schema = json.loads(
            (ROOT / "data" / "daily-cards" / "schema.json").read_text(encoding="utf-8")
        )
        validator = jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        )
        for number in (1, 2, 5, 7):
            payload = json.loads(
                (ROOT / "data" / "daily-cards" / f"day-{number:02d}.json")
                .read_text(encoding="utf-8")
            )
            self.assertEqual([], list(validator.iter_errors(payload)))

    def test_misleading_reservation_semantics_are_removed(self):
        expected = {
            1: {
                "bcn-airport": {"confirmed", "ticket", "check"},
                "barcelona-checkin": {"confirmed"},
            },
            2: {
                "sant-pau": {"ticket"},
                "puertecillo-sagrada": {"book"},
                "sagrada-familia": {"confirmed", "caution"},
                "gracia": {"optional"},
                "bodega-joan": {"book"},
            },
            5: {
                "bascara-stay": {"caution"},
                "collioure": {"caution", "check"},
                "cadaques": {"caution"},
            },
            7: {
                "bascara-checkout": {"confirmed"},
                "bcn-airport-return": {"confirmed", "check"},
                "vy1521": {"confirmed", "caution"},
                "nice-checkin": {"confirmed", "ticket"},
                "promenade": {"optional"},
            },
        }
        for number, stops in expected.items():
            by_id = {stop.id: stop for stop in self.day(number).stops}
            for stop_id, statuses in stops.items():
                stop = by_id[stop_id]
                self.assertIsNone(stop.reservation, f"Day {number} {stop_id}")
                self.assertEqual(statuses, {status.type for status in stop.execution_statuses})

        for number in (1, 2, 5, 7):
            rendered_html = self.rendered(number)
            self.assertNotIn('<span class="badge badge-caution">예약</span>', rendered_html)

    def test_factual_content_pass_day01(self):
        day1 = self.rendered(1)
        self.assertIn("Aerobús A1", day1)
        self.assertIn("€7.75", day1)
        self.assertIn("Floor 0", day1)
        self.assertIn("24시간 reception", day1)
        self.assertNotIn("00:00", day1)

    def test_factual_content_pass_day02(self):
        day2 = self.rendered(2)
        self.assertIn("13:00", day2)
        self.assertIn("14:45 보안검색 도착", day2)
        self.assertIn("15:15 확정 입장", day2)
        self.assertIn("€18", day2)
        self.assertIn("19:15 저녁 목표", day2)
        self.assertNotIn("20:30 예약", day2)
        self.assertNotIn("사그라다 예약이 끝내 안 되면", day2)

    def test_factual_content_pass_day05(self):
        day5 = self.rendered(5)
        self.assertIn("수요 전통시장", day5)
        self.assertIn("Parking du Château d'eau", day5)
        self.assertIn("Parking Saba Cadaqués", day5)
        self.assertIn("17:30 Cadaqués 출발", day5)
        self.assertNotIn("Le Jardin 선택 시", day5)

    def test_factual_content_pass_day07(self):
        day7 = self.rendered(7)
        self.assertIn("12:30 Hertz 반납 운영 목표", day7)
        self.assertIn("14:00", day7)
        self.assertIn("14:50", day7)
        self.assertIn("14:45 수하물 위탁 완료 목표", day7)
        self.assertIn("Aéro €10 왕복권", day7)
        self.assertIn("Palais ALZIRA", day7)
        self.assertNotIn("Hertz 변경 불가 시 기내반입 위주", day7)

    def test_driving_and_transfer_map_destinations(self):
        day5 = {stop.id: stop for stop in self.day(5).stops}
        self.assertIn("Parking du Château d'eau, Collioure", unquote_plus(render.stop_map_url(day5["collioure"])))
        self.assertIn("Parking Saba Cadaqués", unquote_plus(render.stop_map_url(day5["cadaques"])))

        day7 = {stop.id: stop for stop in self.day(7).stops}
        self.assertIn("Hertz", unquote_plus(render.stop_map_url(day7["bcn-airport-return"])))
        self.assertIn("12 Rue Verdi", unquote_plus(render.stop_map_url(day7["nice-checkin"])))

    def test_action_card_and_timeline_reuse_map_links(self):
        for number in (1, 2, 5, 7):
            rendered = self.rendered(number)
            self.assertRegex(rendered, r'class="action-actions btn-row">\s*<a[^>]+google\.com/maps')
            self.assertIn('class="tl-actions btn-row"', rendered)
            self.assertNotRegex(rendered, r'class="(?:action|tl)-actions btn-row">\s*</div>')

    def test_markdown_markers_do_not_leak(self):
        for number in (1, 2, 5, 7):
            rendered = self.rendered(number)
            self.assertNotRegex(rendered, re.compile(r">[^<]*\*\*[^<]*<"))


if __name__ == "__main__":
    unittest.main()
