from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

import place_relationship_audit


class PlaceRelationshipAuditTests(unittest.TestCase):
    def test_all_relationship_categories_are_clean(self):
        report = place_relationship_audit.audit()
        self.assertEqual(
            {}, {name: rows for name, rows in report.items() if rows},
            "Day–Place relationship audit must have no errors",
        )


if __name__ == "__main__":
    unittest.main()
