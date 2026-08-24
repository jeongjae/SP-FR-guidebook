"""Execution UX Batch 01의 상태·행동·Day type 회귀 검사."""
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


class ExecutionUxBatch01Tests(unittest.TestCase):
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

    def test_pilot_day_types_are_explicit_and_extensible(self):
        self.assertEqual("city", self.day(3).day_type)
        self.assertEqual("transfer", self.day(4).day_type)
        self.assertEqual("driving", self.day(6).day_type)

    def test_pilot_sources_follow_daily_card_schema(self):
        schema = json.loads(
            (ROOT / "data" / "daily-cards" / "schema.json").read_text(encoding="utf-8")
        )
        validator = jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        )
        for number in (3, 4, 6):
            payload = json.loads(
                (ROOT / "data" / "daily-cards" / f"day-{number:02d}.json")
                .read_text(encoding="utf-8")
            )
            self.assertEqual([], list(validator.iter_errors(payload)))

    def test_misleading_reservation_semantics_are_removed(self):
        expected = {
            3: {
                "biblioteca-de-catalunya": {"check"},
                "bar-canete": {"book", "check"},
                "macba": {"ticket", "check"},
            },
            6: {
                "tossa": {"check"},
                "pals": {"optional"},
                "peratallada": {"caution"},
            },
        }
        for number, stops in expected.items():
            by_id = {stop.id: stop for stop in self.day(number).stops}
            for stop_id, statuses in stops.items():
                stop = by_id[stop_id]
                self.assertIsNone(stop.reservation, f"Day {number} {stop_id}")
                self.assertEqual(statuses, {status.type for status in stop.execution_statuses})

        day3 = self.rendered(3)
        self.assertIn("일반 방문 접근 범위는 현장 확인", day3)
        self.assertNotIn("자유 입장", day3)
        self.assertNotIn('<span class="badge badge-caution">예약</span>', day3)

    def test_factual_content_pass(self):
        day3 = self.rendered(3)
        self.assertIn("월–금 09:00–20:00", day3)
        self.assertIn("13:30 전후 사전 예약 필요", day3)
        self.assertNotIn("13:30 " + "슬롯", day3)
        self.assertIn("하계 월요일 10:00–20:00", day3)
        self.assertIn("온라인 예매 €13.50 권장", day3)
        self.assertIn("현장 일반권 €15", day3)

        day4 = self.rendered(4)
        self.assertIn("C/ Viriat 45", day4)
        self.assertIn("€30 cross-border fee", day4)
        self.assertIn("€600 penalty 가능", day4)
        self.assertNotIn("보험 전체 " + "무효", day4)
        self.assertIn("Museu del Cau Ferrat + Museu de Maricel", day4)
        self.assertIn("restaurantelazorra.com", day4)

    def test_driving_days_target_parking_destinations(self):
        day4 = {stop.id: stop for stop in self.day(4).stops}
        self.assertIn("Aparcament Can Robert", unquote_plus(render.stop_map_url(day4["can-robert"])))

        day6 = {stop.id: stop for stop in self.day(6).stops}
        self.assertIn("Parking Carrer Abeurador, Pals", unquote_plus(render.stop_map_url(day6["pals"])))
        self.assertIn("Aparcament de Baix, Peratallada", unquote_plus(render.stop_map_url(day6["peratallada"])))
        self.assertIn("Avinguda del Pelegrí", unquote_plus(render.stop_map_url(day6["tossa"])))
        self.assertIn("CONTENT_RESEARCH_REQUIRED", self.rendered(6))

    def test_action_card_and_timeline_reuse_map_links(self):
        for number in (3, 4, 6):
            rendered = self.rendered(number)
            self.assertRegex(rendered, r'class="action-actions btn-row">\s*<a[^>]+google\.com/maps')
            self.assertIn('class="tl-actions btn-row"', rendered)
            self.assertNotRegex(rendered, r'class="(?:action|tl)-actions btn-row">\s*</div>')

        day3 = self.rendered(3)
        action = day3.split('class="action-actions btn-row"', 1)[1].split("</div>", 1)[0]
        self.assertLess(action.index("길찾기"), action.index("장소 정보"))
        self.assertLess(action.index("장소 정보"), action.index("티켓·공식"))

    def test_transfer_and_driving_legs_render_as_major_milestones(self):
        self.assertEqual(2, self.rendered(4).count("tl-leg-major"))
        self.assertEqual(5, self.rendered(6).count("tl-leg-major"))
        self.assertIn("Bàscara 출발 → Tossa de Mar", self.rendered(6))
        self.assertIn("다음 목적지", self.rendered(6))

    def test_markdown_markers_do_not_leak_into_ui_text(self):
        rendered = self.rendered(4)
        self.assertNotIn("**프랑스 주행", rendered)
        self.assertNotIn("신고한다**", rendered)
        self.assertNotRegex(rendered, re.compile(r">[^<]*\*\*[^<]*<"))

    def test_plan_b_and_pre_trip_checks_are_separate_sections(self):
        for number in (3, 4, 6):
            rendered = self.rendered(number)
            self.assertIn("PLAN B", rendered)
            self.assertIn("일정 조정 기준", rendered)
            self.assertIn("PRE-TRIP CHECK", rendered)
            self.assertIn("출발 전 확인", rendered)


if __name__ == "__main__":
    unittest.main()
