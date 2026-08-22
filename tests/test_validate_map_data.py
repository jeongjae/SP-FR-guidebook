import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_map_data import validate  # noqa: E402


class MapDataValidationTests(unittest.TestCase):
    def setUp(self):
        self.source = ROOT / "source" / "ASSETS" / "maps"
        self.payloads = {
            name: json.loads((self.source / name).read_text(encoding="utf-8"))
            for name in ("place-registry.json", "daily-routes.json", "region-groups.json")
        }

    def write_payloads(self, directory, payloads=None):
        for name, payload in (payloads or self.payloads).items():
            (directory / name).write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    def test_canonical_data_is_valid(self):
        errors, warnings = validate(self.source)
        self.assertEqual(errors, [])
        self.assertGreater(len(warnings), 0)

    def test_duplicate_place_id_is_rejected(self):
        payloads = copy.deepcopy(self.payloads)
        payloads["place-registry.json"]["places"].append(
            copy.deepcopy(payloads["place-registry.json"]["places"][0]))
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            self.write_payloads(directory, payloads)
            errors, _warnings = validate(directory)
        self.assertTrue(any("중복 ID" in error for error in errors))

    def test_private_place_cannot_publish_precise_location_fields(self):
        payloads = copy.deepcopy(self.payloads)
        places = payloads["place-registry.json"]["places"]
        place = next((item for item in places if item.get("private")), None)
        if place is None:
            place = copy.deepcopy(places[0])
            place["id"] = "private-test"
            place["private"] = True
            places.append(place)
        place["lat"] = 42.123456
        place["googleMapsUrl"] = "https://www.google.com/maps/search/?api=1&query=private"
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            self.write_payloads(directory, payloads)
            errors, _warnings = validate(directory)
        self.assertTrue(any("주소·지도 URL·Place ID" in error for error in errors))
        self.assertTrue(any("소수점 3자리" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
