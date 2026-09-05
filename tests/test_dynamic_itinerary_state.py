"""Regression guards for the travel-time Today and full-schedule state."""
from __future__ import annotations

import json
import re
import sys
import unittest
from datetime import timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))

import model  # noqa: E402


class DynamicItineraryStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trip = model.load_trip()

    def test_every_travel_date_has_one_canonical_day_and_region(self):
        expected_regions = {
            "2026-08-29": "barcelona",
            "2026-09-01": "girona",
            "2026-09-04": "nice",
            "2026-09-06": "nice",
            "2026-09-09": "verdon",
            "2026-09-10": "aix",
            "2026-09-14": "luberon",
            "2026-09-16": "avignon",
            "2026-09-20": "lyon",
            "2026-09-24": "paris",
            "2026-09-30": "paris",
            "2026-10-10": "return",
        }
        dates = [self.trip.start + timedelta(days=offset) for offset in range(43)]
        self.assertEqual(dates, [day.date for day in self.trip.days])

        for today in dates:
            matches = [day for day in self.trip.days if day.date == today]
            self.assertEqual(1, len(matches), today.isoformat())
            # Runtime currentRegion is defined directly from this canonical Day.
            current_day = matches[0]
            current_region = current_day.region
            self.assertEqual(current_day.region, current_region)

        for iso_date, expected_region in expected_regions.items():
            day = next(day for day in self.trip.days if day.date.isoformat() == iso_date)
            self.assertEqual(expected_region, day.region, iso_date)

    def test_partition_invariant_for_all_43_travel_dates(self):
        all_days = set(range(1, 44))
        for current in self.trip.days:
            past_list = [day.n for day in self.trip.days if day.date < current.date]
            today_list = [day.n for day in self.trip.days if day.date == current.date]
            future_list = [day.n for day in self.trip.days if day.date > current.date]
            past, today, future = set(past_list), set(today_list), set(future_list)
            self.assertFalse(past & today)
            self.assertFalse(today & future)
            self.assertFalse(past & future)
            self.assertEqual(all_days, past | today | future)
            self.assertEqual(sorted(past_list), past_list)
            self.assertEqual(sorted(future_list), future_list)

    def test_generated_schedule_keeps_canonical_order_and_runtime_payload(self):
        html = (ROOT / "site" / "schedule.html").read_text(encoding="utf-8")
        payload_match = re.search(
            r'<script type="application/json" id="schedule-data">(.*?)</script>',
            html,
            re.DOTALL,
        )
        self.assertIsNotNone(payload_match)
        payload = json.loads(payload_match.group(1))
        self.assertEqual(list(range(1, 44)), [day["n"] for day in payload["days"]])
        self.assertEqual(
            [day.date.isoformat() for day in self.trip.days],
            [day["date"] for day in payload["days"]],
        )
        self.assertEqual("return", payload["days"][-1]["region"])
        self.assertIn('id="schedule-canonical"', html)
        self.assertIn('id="schedule-live"', html)
        self.assertIn('id="schedule-past"', html)
        self.assertIn('aria-controls="schedule-past-days"', html)

        regions_match = re.search(
            r'<script type="application/json" id="schedule-regions-data">(.*?)</script>',
            html,
            re.DOTALL,
        )
        self.assertIsNotNone(regions_match)
        regions = json.loads(regions_match.group(1))
        self.assertTrue(all(set(region) == {"slug", "name"} for region in regions))

        positions = [html.index(f'data-day-number="{number}"') for number in range(1, 44)]
        self.assertEqual(sorted(positions), positions)

    def test_runtime_current_region_does_not_use_region_ranges(self):
        script = (ROOT / "build" / "assets" / "app.js").read_text(encoding="utf-8")
        self.assertIn("currentRegion: currentDay ? currentDay.region : null", script)
        self.assertIn("now.getFullYear()", script)
        self.assertIn("now.getMonth() + 1", script)
        self.assertIn("now.getDate()", script)
        self.assertNotRegex(script, r"iso\w*\s*>=\s*regions\[")
        self.assertNotRegex(script, r"iso\w*\s*<=\s*regions\[")


if __name__ == "__main__":
    unittest.main()
