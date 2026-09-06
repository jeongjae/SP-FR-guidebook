"""MP-04 — 파리 끼니 슬롯이 상호를 잃지 않는가.

파리 16일 중 점심 6끼·저녁 10끼가 '9구 오페라 점심' · '15구 숙소 귀환 &
저녁' 처럼 권역만 적힌 채 비어 있었다. 현장에서 그 줄을 보면 어디로 갈지
그때 정해야 한다 — 정오에 배가 고픈 상태로.

이 테스트는 그 자리가 다시 비는 것을 막는다.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "data" / "daily-cards"
PLACES = ROOT / "source" / "CURRENT" / "30_Places"

# (Day, stop id, place 슬러그)
LUNCH = [
    (31, "opera-lunch", "au-petit-riche"),
    (32, "versailles-lunch", "la-flottille"),
    (33, "champs-elysees-lunch", "chez-savy"),
    (34, "rue-du-bac-lunch", "cafe-varenne"),
    (40, "halles-lunch", "aux-crus-de-bourgogne"),
    (41, "iena-lunch", "les-marches"),
]
DINNER = [
    (27, "paris-return", "le-relais-du-15eme"),
    (29, "bouillon-racine-dinner", "bouillon-racine"),
    (31, "paris-return", "guylas"),
    (33, "paris-return", "stephane-martin"),
    (35, "paris-return", "sawadee-paris"),
    (36, "paris-return", "le-relais-du-15eme"),
    (37, "paris-return", "breizh-cafe-charles-michels"),
    (38, "paris-return", "le-volant-basque"),
    (39, "chez-janou-dinner", "chez-janou"),
    (40, "le-progres-dinner", "le-progres-montmartre"),
]


def day(n: int) -> dict:
    return json.loads((CARDS / f"day-{n:02d}.json").read_text(encoding="utf-8"))


def stop(d: dict, sid: str) -> dict:
    for s in d["stops"]:
        if s["id"] == sid:
            return s
    raise AssertionError(f"day-{d['day']:02d} 에 {sid} 스톱이 없다")


class ParisMealSlotTests(unittest.TestCase):
    def test_every_meal_slot_names_a_place(self):
        """끼니 스톱은 권역이 아니라 상호를 가리킨다."""
        for n, sid, slug in LUNCH + DINNER:
            with self.subTest(day=n, stop=sid):
                s = stop(day(n), sid)
                self.assertEqual(s["place_ref"], slug)
                self.assertEqual(s["category"], "food")

    def test_every_meal_slot_carries_a_menu(self):
        """무엇을 시킬지가 카드에 있어야 현장에서 메뉴판 앞에 서지 않는다."""
        for n, sid, _ in LUNCH + DINNER:
            with self.subTest(day=n, stop=sid):
                menu = stop(day(n), sid).get("menu")
                self.assertTrue(menu and menu.strip(), f"day-{n:02d} {sid} 메뉴 없음")

    def test_named_place_has_a_dossier(self):
        """상호를 적었으면 그 상호의 장문이 있어야 한다."""
        for _, _, slug in LUNCH + DINNER:
            with self.subTest(place=slug):
                path = PLACES / f"{slug}.md"
                self.assertTrue(path.exists(), f"{slug} 정본 없음")
                text = path.read_text(encoding="utf-8")
                for section in ("## 왜 가는가", "## 더 깊이", "## 실용"):
                    self.assertIn(section, text, f"{slug} 에 {section} 없음")

    def test_alternatives_survive_in_backup(self):
        """2·3순위는 페이지를 갖지 않는다 — 그 대신 Plan B 에서 사라지지 않는다."""
        expected = {
            31: "Le Pantruche", 32: "La Petite Venise", 33: "Le Bar des Théâtres",
            34: "La Laiterie", 40: "Le Comptoir de la Gastronomie",
            41: "Hanok", 29: "L'Avant Comptoir", 39: "Au Bourguignon du Marais",
        }
        for n, name in expected.items():
            with self.subTest(day=n):
                self.assertIn(name, day(n).get("backup") or "",
                              f"day-{n:02d} Plan B 에서 대안 {name} 이 사라졌다")

    def test_field_dinner_days_return_home_after_eating(self):
        """현장에서 먹는 세 밤은 식사 뒤에 귀가 스톱이 남아 있어야 한다."""
        for n, sid in ((29, "bouillon-racine-dinner"), (39, "chez-janou-dinner"),
                       (40, "le-progres-dinner")):
            with self.subTest(day=n):
                d = day(n)
                ids = [s["id"] for s in d["stops"]]
                self.assertLess(ids.index(sid), ids.index("paris-return"))
                legs = {(l["from"], l["to"]) for l in d["legs"]}
                self.assertIn((sid, "paris-return"), legs)
                self.assertEqual(len(ids), len(set(ids)), "스톱이 중복됐다")

    def test_montmartre_festival_claim_is_honest(self):
        """10/7 은 개막일이지만 노점·행렬은 10/9~11 이다. 그렇게 적혀 있어야 한다."""
        s = stop(day(40), "vendanges-montmartre")
        self.assertIn("10/9", s["summary"])
        self.assertNotIn("축제 분위기", s["summary"])
        types = {x["type"] for x in s.get("executionStatuses", [])}
        self.assertIn("caution", types)


if __name__ == "__main__":
    unittest.main()
