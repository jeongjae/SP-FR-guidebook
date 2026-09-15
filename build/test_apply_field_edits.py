#!/usr/bin/env python3
"""apply_field_edits 부정·충돌·구조 픽스처 — 폰 편집이 정본을 망치지 못하는가."""
from __future__ import annotations

import copy
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
    @classmethod
    def setUpClass(cls):
        cls.ctx_base = afe.load_context()
        cls.cards_base = {p.stem: json.loads(p.read_text(encoding="utf-8"))
                          for p in afe.DAILY.glob("day-*.json")}

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        field = self.tmp / "field-edits"
        field.mkdir()
        (field / "state.json").write_text(json.dumps(
            {"version": 1, "cursors": {}, "rejected": [], "overwritten": []}),
            encoding="utf-8")
        self._orig = (afe.FIELD_DIR, afe.STATE, afe.PLACE_DIR)
        afe.FIELD_DIR = field
        afe.STATE = field / "state.json"
        # 컨텍스트는 테스트마다 사본 — apply 가 stops 색인을 갱신한다.
        self.ctx = {**self.ctx_base,
                    "stops": {k: set(v) for k, v in self.ctx_base["stops"].items()}}
        self.cards = copy.deepcopy(self.cards_base)
        self.state = {"version": 1, "cursors": {}, "rejected": [], "overwritten": []}
        self.notes = {"version": 1, "notes": [], "visited": {}, "checkedActions": {}}
        self.overrides = {"version": 1, "overrides": {}}

    def tearDown(self):
        afe.FIELD_DIR, afe.STATE, afe.PLACE_DIR = self._orig

    def write_journal(self, dev, events):
        path = afe.FIELD_DIR / f"journal-{dev}.ndjson"
        path.write_text("\n".join(json.dumps(e, ensure_ascii=False)
                                  for e in events) + "\n", encoding="utf-8")

    def run_apply(self):
        events = afe.load_pending(self.state)
        stats = afe.apply_events(events, self.ctx, self.state,
                                 self.notes, self.overrides, self.cards)
        return stats

    # ------------------------------------------------------------ P2 회귀

    def test_happy_path_note_and_visited(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "stop", "key": "day-19/saint-remy"},
               "note", {"text": "시장 주차는 북쪽이 여유"}),
            ev("01B", "devA", 2, {"kind": "stop", "key": "day-19/saint-remy"},
               "set-visited", {"value": True}),
        ])
        stats = self.run_apply()
        self.assertEqual((stats["applied"], stats["rejected"]), (2, 0))
        self.assertEqual(self.notes["notes"][0]["text"], "시장 주차는 북쪽이 여유")
        self.assertTrue(self.notes["visited"]["day-19/saint-remy"]["value"])
        self.assertEqual(self.state["cursors"]["devA"], "01B")

    def test_same_slot_conflict_lww_and_overwritten(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "booking", "key": "R016"},
               "set-booking", {"status": "확정"}, ts="2026-09-16T10:00:01.000Z")])
        self.write_journal("devB", [
            ev("01B", "devB", 1, {"kind": "booking", "key": "R016"},
               "set-booking", {"status": "재확인"}, ts="2026-09-16T10:00:05.000Z")])
        stats = self.run_apply()
        self.assertEqual(stats["applied"], 2)
        self.assertEqual(self.overrides["overrides"]["R016"]["status"], "재확인")
        self.assertEqual(self.state["overwritten"][0]["winner"], "01B")

    def test_unknown_stop_rejected_cursor_advances(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "stop", "key": "day-19/no-such-stop"},
               "note", {"text": "x"})])
        stats = self.run_apply()
        self.assertEqual((stats["applied"], stats["rejected"]), (0, 1))
        self.assertIn("없는 stop", self.state["rejected"][0]["reason"])
        self.assertEqual(self.state["cursors"]["devA"], "01A")

    def test_bad_booking_status_rejected(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "booking", "key": "R016"},
               "set-booking", {"status": "unconfirmed"})])
        stats = self.run_apply()
        self.assertEqual(stats["rejected"], 1)
        self.assertIn("모르는 예약 상태", self.state["rejected"][0]["reason"])

    def test_cursor_skips_processed_and_duplicates(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "day", "key": "day-19"},
               "note", {"text": "a"}),
            ev("01A", "devA", 1, {"kind": "day", "key": "day-19"},
               "note", {"text": "a"}),
        ])
        stats = self.run_apply()
        self.assertEqual(stats["applied"], 1)
        self.assertEqual(afe.load_pending(self.state), [])

    # ------------------------------------------------------------ P3 구조

    def test_set_field_time(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "stop", "key": "day-20/uzes"},
               "set-field", {"field": "start", "value": "09:30"})])
        stats = self.run_apply()
        if stats["rejected"]:
            self.fail(self.state["rejected"])
        stop = next(s for s in self.cards["day-20"]["stops"] if s["id"] == "uzes")
        self.assertEqual(stop["start"], "09:30")

    def test_set_field_bad_time_rejected(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "stop", "key": "day-20/uzes"},
               "set-field", {"field": "start", "value": "9시반"})])
        stats = self.run_apply()
        self.assertEqual(stats["rejected"], 1)
        self.assertIn("HH:MM", self.state["rejected"][0]["reason"])

    def test_add_stop_then_move_and_remove(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "day", "key": "day-21"},
               "add-stop", {"stop": {"id": "gelato-break", "name": "젤라토 휴식",
                                      "category": "cafe", "start": "15:30",
                                      "end": "16:00"},
                            "afterStopId": None}),
            ev("01B", "devA", 2, {"kind": "stop", "key": "day-21/gelato-break"},
               "move-stop", {"afterStopId": None}),
        ])
        stats = self.run_apply()
        self.assertEqual(stats["rejected"], 0, self.state["rejected"])
        card = self.cards["day-21"]
        self.assertEqual(card["stops"][0]["id"], "gelato-break")
        self.assertTrue(card["stops"][0]["fieldEdit"])
        self.assertEqual([s["order"] for s in card["stops"]],
                         list(range(1, len(card["stops"]) + 1)))
        # 이어서 삭제 — 색인 갱신이 반영됐는가
        self.write_journal("devA", [
            ev("01C", "devA", 3, {"kind": "stop", "key": "day-21/gelato-break"},
               "remove-stop", {}),
        ])
        stats = self.run_apply()
        self.assertEqual(stats["rejected"], 0, self.state["rejected"])
        self.assertNotIn("gelato-break",
                         [s["id"] for s in self.cards["day-21"]["stops"]])

    def test_add_stop_over_schema_cap_rejected(self):
        # day-14 는 스톱 9개(스키마 상한) — 하나 더 넣으면 스키마가 막는다.
        full_day = next(k for k, c in self.cards.items() if len(c["stops"]) == 9)
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "day", "key": full_day},
               "add-stop", {"stop": {"id": "one-too-many", "name": "초과",
                                      "category": "sight"},
                            "afterStopId": None})])
        stats = self.run_apply()
        self.assertEqual(stats["rejected"], 1)
        self.assertIn("스키마", self.state["rejected"][0]["reason"])
        self.assertEqual(len(self.cards[full_day]["stops"]), 9)

    def test_remove_stop_drops_legs(self):
        card = self.cards["day-20"]
        target = card["legs"][0]["from"]
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "stop", "key": f"day-20/{target}"},
               "remove-stop", {})])
        stats = self.run_apply()
        self.assertEqual(stats["rejected"], 0, self.state["rejected"])
        card = self.cards["day-20"]  # apply 가 카드 사본을 교체한다
        ids = {s["id"] for s in card["stops"]}
        self.assertNotIn(target, ids)
        for l in card["legs"]:
            self.assertIn(l["from"], ids)
            self.assertIn(l["to"], ids)

    def test_prose_set_section_rewrites_layer(self):
        # PLACE_DIR 를 임시 사본으로 돌려 실제 파일을 지킨다.
        tmp_places = self.tmp / "places"
        tmp_places.mkdir()
        shutil.copy(self._orig[2] / "gordes.md", tmp_places / "gordes.md")
        afe.PLACE_DIR = tmp_places
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "place", "key": "gordes"},
               "prose-set-section",
               {"section": "practical", "md": "- 주차: 테스트 실용 정보"})])
        stats = self.run_apply()
        self.assertEqual(stats["rejected"], 0, self.state["rejected"])
        self.assertEqual(len(stats["proseEvents"]), 1)
        afe.apply_prose(stats["proseEvents"][0])
        text = (tmp_places / "gordes.md").read_text(encoding="utf-8")
        self.assertIn("## 실용\n\n- 주차: 테스트 실용 정보", text)
        self.assertIn("## 왜 가는가", text)   # 다른 층 보존
        self.assertIn("## 더 깊이", text)
        self.assertTrue(text.startswith("---\n"))  # frontmatter 보존
        # 앞머리(현장 실행 카드)는 '왜 가는가' 앞 원위치에 남는다
        self.assertLess(text.index("## 현장 실행"), text.index("## 왜 가는가"))

    def test_prose_unknown_section_rejected(self):
        self.write_journal("devA", [
            ev("01A", "devA", 1, {"kind": "place", "key": "gordes"},
               "prose-set-section", {"section": "history", "md": "x"})])
        stats = self.run_apply()
        self.assertEqual(stats["rejected"], 1)
        self.assertIn("모르는 section", self.state["rejected"][0]["reason"])


if __name__ == "__main__":
    unittest.main()
