"""Execution UX Batch 06의 Day 24–27 (Lyon & Annecy & Paris Transfer) 사실·상태·동선 회귀 검사."""
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


class ExecutionUxBatch06Tests(unittest.TestCase):
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
        expected = {24: "city", 25: "city", 26: "transfer", 27: "transfer"}
        schema = json.loads((DAILY_CARDS / "schema.json").read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
        for number, day_type in expected.items():
            self.assertEqual(day_type, self.day(number).day_type)
            self.assertEqual([], list(validator.iter_errors(load_day(number))))

    def test_day24_fourviere_vieux_lyon_flow(self):
        payload = load_day(24)
        stops = {stop["id"]: stop for stop in payload["stops"]}
        
        # Funicular check
        funicular_statuses = {s["type"] for s in stops["funicular-ascent"]["executionStatuses"]}
        self.assertIn("check", funicular_statuses)
        
        # Fourvière free admission (not ticket/confirmed)
        fourviere_statuses = {s["type"] for s in stops["fourviere"]["executionStatuses"]}
        self.assertIn("check", fourviere_statuses)
        self.assertNotIn("confirmed", fourviere_statuses)
        self.assertNotIn("ticket", fourviere_statuses)
        
        # Daniel et Denise booking required
        bouchon_statuses = {s["type"] for s in stops["lyon-bouchon-dinner"]["executionStatuses"]}
        self.assertIn("book", bouchon_statuses)
        
        # Optional Saône walk
        self.assertTrue(stops["saone-presquile"]["optional"])
        
        rendered = self.rendered(24)
        for text in ("Fourvière", "Rosaire", "Traboules", "Daniel et Denise"):
            self.assertIn(text, rendered)

    def test_day25_croix_rousse_canuts_and_halles(self):
        payload = load_day(25)
        stops = {stop["id"]: stop for stop in payload["stops"]}
        
        # Tuesday Market check
        market_statuses = {s["type"] for s in stops["croix-rousse-market"]["executionStatuses"]}
        self.assertIn("check", market_statuses)
        
        # Maison des Canuts guided tour ticket
        canuts_statuses = {s["type"] for s in stops["maison-des-canuts"]["executionStatuses"]}
        self.assertIn("ticket", canuts_statuses)
        
        # Halles Paul Bocuse lunch caution
        halles_statuses = {s["type"] for s in stops["halles-gastronomy"]["executionStatuses"]}
        self.assertIn("caution", halles_statuses)
        
        # Tête d'Or optional
        self.assertTrue(stops["tete-dor"]["optional"])
        
        rendered = self.rendered(25)
        for text in ("Marché de la Croix-Rousse", "Maison des Canuts", "Halles Paul Bocuse", "Tête d'Or"):
            self.assertIn(text, rendered)

    def test_day26_annecy_day_trip_live_ter_semantics(self):
        payload = load_day(26)
        stops = {stop["id"]: stop for stop in payload["stops"]}
        
        # Outbound & Return TER are check (not confirmed)
        for stop_id in ("part-dieu-departure", "annecy-return"):
            types = {s["type"] for s in stops[stop_id]["executionStatuses"]}
            self.assertEqual({"check"}, types)
            
        # Palais de l'Île ticket for interior museum visit & check for open hours (no confirmed)
        palais_statuses = {s["type"] for s in stops["vieille-ville"]["executionStatuses"]}
        self.assertIn("ticket", palais_statuses)
        self.assertIn("check", palais_statuses)
        self.assertNotIn("confirmed", palais_statuses)
        
        # Chez Mamie Lise booking recommendation
        lunch_statuses = {s["type"] for s in stops["savoy-lunch"]["executionStatuses"]}
        self.assertIn("book", lunch_statuses)
        
        # Lakefront walk is standard (optional=False), no optional execution status
        self.assertFalse(stops["lakefront"]["optional"])
        lake_statuses = {s["type"] for s in stops["lakefront"]["executionStatuses"]}
        self.assertNotIn("optional", lake_statuses)
        
        # Cruise is separate optional stop (optional=True), weather permitting
        self.assertTrue(stops["annecy-cruise"]["optional"])
        cruise_statuses = {s["type"] for s in stops["annecy-cruise"]["executionStatuses"]}
        self.assertIn("optional", cruise_statuses)
        cruise_labels = {s["label"] for s in stops["annecy-cruise"]["executionStatuses"]}
        self.assertIn("WEATHER PERMITTING", cruise_labels)
        
        # Return buffer: station arrival 17:30 before 17:53 TER departure
        self.assertIn("17:30", stops["annecy-return"]["summary"])
        self.assertIn("17:53", stops["annecy-return"]["summary"])
        
        rendered = self.rendered(26)
        self.assertIn("LIVE TRAIN CHECK", rendered)
        self.assertIn("TICKET", rendered)
        self.assertIn("Chez Mamie Lise", rendered)
        self.assertIn("Thiou", rendered)
        self.assertIn("WEATHER PERMITTING", rendered)

    def test_day27_transfer_to_paris_confirmed_anchors(self):
        payload = load_day(27)
        stops = {stop["id"]: stop for stop in payload["stops"]}
        
        # Lagrange checkout confirmed
        checkout_statuses = {s["type"] for s in stops["lyon-checkout"]["executionStatuses"]}
        self.assertIn("confirmed", checkout_statuses)
        
        # TGV 6618 confirmed
        tgv_statuses = {s["type"] for s in stops["tgv-to-paris"]["executionStatuses"]}
        self.assertIn("confirmed", tgv_statuses)
        self.assertIn("13:04", stops["tgv-to-paris"]["start"])
        self.assertIn("15:00", stops["tgv-to-paris"]["end"])
        
        # Paris 78 Rue de Lourmel checkin confirmed
        checkin_statuses = {s["type"] for s in stops["paris-checkin"]["executionStatuses"]}
        self.assertIn("confirmed", checkin_statuses)
        self.assertIn("caution", checkin_statuses)  # official taxi caution
        
        # Paris return dinner is optional, NOT confirmed
        dinner_statuses = {s["type"] for s in stops["paris-return"]["executionStatuses"]}
        self.assertIn("optional", dinner_statuses)
        self.assertNotIn("confirmed", dinner_statuses)
        
        rendered = self.rendered(27)
        self.assertIn("TGV INOUI 6618", rendered)
        self.assertIn("78 Rue de Lourmel", rendered)
        self.assertIn("Le Relais du 15ème", rendered)

    def test_day27_semantic_projection_is_frozen(self):
        payload = semantic_projection(load_day(27))
        digest = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual("af3aa062b49a895e6147b74d3ada7d7f145a3dee107205344c3b5e324fd42607", digest)

    def test_confirmed_never_coexists_with_booking_action(self):
        for path in sorted(DAILY_CARDS.glob("day-??.json")):
            for stop in json.loads(path.read_text(encoding="utf-8"))["stops"]:
                statuses = stop.get("executionStatuses", [])
                types = {status["type"] for status in statuses}
                labels = {status.get("label", "").upper() for status in statuses}
                if "book" in types or labels & {"BOOK", "ACTION REQUIRED"}:
                    self.assertNotIn("confirmed", types, f"{path.name}: {stop['id']}")

    def test_rendered_links_and_markdown_do_not_leak(self):
        for number in range(24, 28):
            rendered = self.rendered(number)
            self.assertNotIn("**", rendered)
            self.assertNotIn("[CONFIRMED]", rendered)
            self.assertNotIn('href="None"', rendered)
            self.assertNotIn('href=""', rendered)

    def test_day28_onward_semantics_are_unchanged(self):
        payload = [semantic_projection(load_day(number)) for number in range(28, 44)]
        digest = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual("858b7227132036e4082e1746ce853860d46c825e2095d6ed7ccdda3db282d4d4", digest)


if __name__ == "__main__":
    unittest.main()
