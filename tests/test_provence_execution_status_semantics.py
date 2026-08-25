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
        by_day = {
            number: {stop["id"]: stop for stop in load_day(number)["stops"]}
            for number in range(16, 20)
        }

        self.assertEqual(
            {"book", "optional"},
            {status["type"] for status in statuses(by_day[16]["lourmarin-lunch"])},
        )
        self.assertIn("12:00–14:00", by_day[16]["lourmarin-lunch"]["executionNote"])
        self.assertEqual(
            {"check"},
            {status["type"] for status in statuses(by_day[17]["roussillon"])},
        )

        menerbes = by_day[17]["menerbes"]
        self.assertTrue(menerbes["optional"])
        self.assertEqual(
            {"optional"}, {status["type"] for status in statuses(menerbes)}
        )
        self.assertIn("월요일 휴무", menerbes["executionNote"])

        self.assertNotIn("executionStatuses", by_day[18]["l-isle-sur-la-sorgue"])
        self.assertNotIn("executionStatuses", by_day[19]["saint-remy"])
        self.assertEqual(
            {"check"},
            {status["type"] for status in statuses(by_day[19]["les-baux-de-provence"])},
        )
        self.assertEqual(
            ["OPTIONAL BONUS"],
            [status["label"] for status in statuses(by_day[19]["orange"])],
        )


if __name__ == "__main__":
    unittest.main()
