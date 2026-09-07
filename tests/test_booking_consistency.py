import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class BookingConsistencyTests(unittest.TestCase):
    def test_prepare_and_paris_museum_share_single_booking_sot(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "build" / "booking_consistency_audit.py")],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
