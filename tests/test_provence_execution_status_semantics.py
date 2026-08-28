"""Provence Daily Card execution-status 의미의 회귀 검사."""
from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DAILY_CARDS = ROOT / "data" / "daily-cards"


def load_day(number: int) -> dict:
    return json.loads(
        (DAILY_CARDS / f"day-{number:02d}.json").read_text(encoding="utf-8")
    )


def statuses(stop: dict) -> list[dict]:
    return stop.get("executionStatuses", [])


class ProvenceExecutionStatusSemanticsTests(unittest.TestCase):
    def test_action_required_or_book_is_never_also_confirmed(self):
        for path in sorted(DAILY_CARDS.glob("day-??.json")):
            day = json.loads(path.read_text(encoding="utf-8"))
            for stop in day["stops"]:
                stop_statuses = statuses(stop)
                types = {status["type"] for status in stop_statuses}
                labels = {status.get("label", "").upper() for status in stop_statuses}
                action_required = "book" in types or bool(
                    labels & {"BOOK", "ACTION REQUIRED"}
                )
                if action_required:
                    self.assertNotIn(
                        "confirmed",
                        types,
                        f"{path.name} {stop['id']} mixes CONFIRMED with BOOK/ACTION REQUIRED",
                    )

    def test_unavailable_is_never_also_confirmed(self):
        for path in sorted(DAILY_CARDS.glob("day-??.json")):
            day = json.loads(path.read_text(encoding="utf-8"))
            for stop in day["stops"]:
                stop_statuses = statuses(stop)
                types = {status["type"] for status in stop_statuses}
                unavailable = "unavailable" in types or any(
                    "UNAVAILABLE" in " ".join(
                        (status.get("label", ""), status.get("detail", ""))
                    ).upper()
                    for status in stop_statuses
                )
                if unavailable:
                    self.assertNotIn(
                        "confirmed",
                        types,
                        f"{path.name} {stop['id']} represents UNAVAILABLE as CONFIRMED",
                    )

    def test_provence_facts_and_optional_bonus_use_neutral_semantics(self):
        # RS01(2026-08-28): 16→17(Lourmarin·Lacoste), 17→18(오크르·화요시장), 18 소멸, 19 통합 도착일
        by_day = {
            number: {stop["id"]: stop for stop in load_day(number)["stops"]}
            for number in range(17, 20)
        }

        self.assertEqual(
            {"book", "optional"},
            {status["type"] for status in statuses(by_day[17]["lourmarin-lunch"])},
        )
        self.assertIn("12:00–14:00", by_day[17]["lourmarin-lunch"]["executionNote"])
        self.assertEqual(
            {"check"},
            {status["type"] for status in statuses(by_day[18]["roussillon"])},
        )

        self.assertNotIn("menerbes", by_day[18], "RS01: Ménerbes는 Day 18 기본 일정에서 제외")
        self.assertNotIn("goult", by_day[18], "RS01: Goult는 Day 18 기본 일정에서 제외")
        lisle = by_day[18]["l-isle-sur-la-sorgue"]
        self.assertTrue(lisle["optional"], "RS01: L'Isle은 Day 18 오후 선택 왕복")
        self.assertNotIn("executionStatuses", lisle)
        self.assertNotIn("executionStatuses", by_day[19]["saint-remy"])
        self.assertEqual(
            {"check"},
            {status["type"] for status in statuses(by_day[19]["les-baux-de-provence"])},
        )
        self.assertNotIn("orange", by_day[19], "RS01: Orange는 일정에서 제외")
        self.assertIn("avignon-checkin", by_day[19], "RS01: Day 19은 Avignon 체크인 통합 도착일")


if __name__ == "__main__":
    unittest.main()
