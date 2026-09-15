#!/usr/bin/env python3
"""apply_field_edits 부정·충돌 픽스처 — 폰 편집이 정본을 망치지 못하는가."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import apply_field_edits as afe


def ev(id_, dev, seq, entity, op, payload, ts=None):
    return {"id": id_, "deviceId": dev, "author": "jason",
            "ts": ts or f"2026-09-16T10:00:{seq:02d}.000Z", "seq": seq,
            "entity": entity, "op": op, "payload": payload, "status": "pushed"}


class ApplyFieldEditsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        field = self.tmp / "field-edits"
        field.mkdir()
        (field / "state.json").write_text(json.dumps(
            {"version": 1, "cursors": {}, "rejected": [], "overwritten": []}),
            encoding="utf-8")
        (self.tmp / "field-notes.json").write_text(json.dumps(
            {"version": 1, "notes": [], "visited": {}, "checkedActions": {}}),
            encoding="utf-8")
        (self.tmp / "booking-overrides.json").write_text(json.dumps(
            {"version": 1, "overrides": {}}), encoding="utf-8")
        self._orig = (afe.FIELD_DIR, afe.STATE, afe.NOTES, afe.OVERRIDES)
        afe.FIELD_DIR = field
        afe.STATE = field / "state.json"
        afe.NOTES = self.tmp / "field-notes.json"
        afe.OVERRIDES = self.tmp / "booking-overrides.json"
        self.ctx = afe.load_context()

    def tearDown(self):
        afe.FIELD_DIR, afe.STATE, afe.NOTES, afe.OVERRIDES = self._orig

    def write_journal(self, dev, events):
        path = afe.FIELD_DIR / f"journal-{dev}.ndjson"
        path.write_text("\n".join(json.dumps(e, ensure_ascii=False)
                                  for e in events) + "\n", encoding="utf-8")

    def run_apply(self):
        state = json.loads(afe.STATE.read_text(encoding="utf-8"))
        notes = json.loads(afe.NOTES.read_text(encoding="utf-8"))
        overrides = json.loads(afe.OVERRIDES.read_text(encoding="utf-8"))
        events = afe.load_pending(state)
        stats = afe.apply_events(events, self.ctx, state, notes, overrides)
        return state, notes, overrides, stats

    def test_happy_path_note_and_visited(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "stop", "key": "day-19/saint-remy"},
               "note", {"text": "시장 주차는 북쪽이 여유"}),
            ev("01B", "devA", 2, {"kind": "stop", "key": "day-19/saint-remy"},
               "set-visited", {"value": True}),
        ])
        state, notes, _, stats = self.run_apply()
        self.assertEqual((stats["applied"], stats["rejected"]), (2, 0))
        self.assertEqual(notes["notes"][0]["text"], "시장 주차는 북쪽이 여유")
        self.assertTrue(notes["visited"]["day-19/saint-remy"]["value"])
        self.assertEqual(state["cursors"]["devA"], "01B")

    def test_same_slot_conflict_lww_and_overwritten(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "booking", "key": "R016"},
               "set-booking", {"status": "확정"},
               ts="2026-09-16T10:00:01.000Z")])
        self.write_journal("devB", [
            ev("01B", "devB", 1, {"kind": "booking", "key": "R016"},
               "set-booking", {"status": "재확인"},
               ts="2026-09-16T10:00:05.000Z")])
        state, _, overrides, stats = self.run_apply()
        self.assertEqual(stats["applied"], 2)
        self.assertEqual(overrides["overrides"]["R016"]["status"], "재확인")
        self.assertEqual(len(state["overwritten"]), 1)
        self.assertEqual(state["overwritten"][0]["winner"], "01B")

    def test_unknown_stop_rejected_cursor_advances(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "stop", "key": "day-19/no-such-stop"},
               "note", {"text": "x"})])
        state, notes, _, stats = self.run_apply()
        self.assertEqual((stats["applied"], stats["rejected"]), (0, 1))
        self.assertIn("없는 stop", state["rejected"][0]["reason"])
        self.assertEqual(state["cursors"]["devA"], "01A")
        self.assertEqual(notes["notes"], [])

    def test_bad_booking_status_rejected(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "booking", "key": "R016"},
               "set-booking", {"status": "unconfirmed"})])
        state, _, overrides, stats = self.run_apply()
        self.assertEqual(stats["rejected"], 1)
        self.assertIn("모르는 예약 상태", state["rejected"][0]["reason"])
        self.assertEqual(overrides["overrides"], {})

    def test_structural_op_rejected_until_p3(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "day", "key": "day-20"},
               "add-stop", {"stop": {"id": "x"}})])
        state, _, _, stats = self.run_apply()
        self.assertEqual(stats["rejected"], 1)
        self.assertIn("미지원 op", state["rejected"][0]["reason"])

    def test_cursor_skips_processed_and_duplicates(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "day", "key": "day-19"},
               "note", {"text": "a"}),
            ev("01A", "devA", 1, {"kind": "day", "key": "day-19"},
               "note", {"text": "a"}),  # 재푸시 중복
        ])
        state, notes, _, stats = self.run_apply()
        self.assertEqual(stats["applied"], 1)
        self.assertEqual(len(notes["notes"]), 1)
        # 두 번째 실행 — 커서 뒤라 아무 것도 없다
        events = afe.load_pending(state)
        self.assertEqual(events, [])


if __name__ == "__main__":
    unittest.main()
