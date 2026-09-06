"""Regression guard for the final 2026 Paris Museum Pass itinerary."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"build"))
import render

def day(n): return json.loads((ROOT/f"data/daily-cards/day-{n}.json").read_text())

class ParisPmpWindowTests(unittest.TestCase):
    def test_day_assignments_are_unique_and_stale_stops_are_absent(self):
        ids={n:{s['id'] for s in day(n)['stops']} for n in (29,30,31,33,35,39,41)}
        self.assertTrue({'sainte-chapelle','conciergerie'} <= ids[29])
        self.assertTrue({'musee-picasso','notre-dame'} <= ids[30]); self.assertNotIn('petit-palais',ids[30])
        self.assertIn('arc-de-triomphe-optional',ids[31])
        self.assertTrue({'orangerie','musee-guimet'} <= ids[33])
        self.assertEqual('11:00',next(s for s in day(35)['stops'] if s['id']=='musee-du-louvre')['start'])
        self.assertNotIn('musee-picasso',ids[39]); self.assertNotIn('musee-guimet',ids[41])

    def test_confirmed_bookings_and_pmp_window_are_prepared(self):
        bookings={b['id']:b for b in render.PARIS_MUSEUM_BOOKINGS}
        for ident in ('grand-palais|2026-09-25|special','versailles|2026-09-29|10:00',
                      'musee-de-l-orangerie|2026-09-30|permanent','musee-d-orsay|2026-10-01|10:30',
                      'qatar-prix-de-l-arc|2026-10-04|general-entry','paris-museum-pass|2026-09-26|144h'):
            self.assertEqual('booked',bookings[ident]['canonical_status'])
        self.assertEqual('General Entry',bookings['qatar-prix-de-l-arc|2026-10-04|general-entry']['schedule'])
        self.assertIn('10/2 Louvre 11:00',bookings['paris-museum-pass|2026-09-26|144h']['schedule'])

    def test_orsay_special_visit_remains_independent(self):
        ids={b['id'] for b in render.PARIS_MUSEUM_BOOKINGS}
        self.assertIn('musee-d-orsay|2026-10-01|10:30',ids)
        self.assertIn('musee-d-orsay|2026-10-06|special',ids)

if __name__=='__main__': unittest.main()
