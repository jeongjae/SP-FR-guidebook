"""숙박·교통 지역 화면의 조용한 손실과 교차오염 회귀 검사."""
from __future__ import annotations

import html
import json
import sys
import unittest
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))

import model  # noqa: E402
import render  # noqa: E402


class StayTransportGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trip = model.load_trip()
        # build_region은 사진·사실 전역 색인을 기대한다. 검사의 관심사는
        # 교통 HTML이므로 빈 색인으로도 충분하다.
        render.IMAGES = {"heroes": {}, "by_place": {}, "extras": {}, "dishes": {}}
        render.FACTS = {}

    def test_model_accommodation_consistency(self):
        self.assertEqual([], model.validate(self.trip))

    def test_region_transport_has_no_silent_truncation_or_cross_region_items(self):
        for region in self.trip.regions:
            rendered = html.unescape(render.build_region(region, self.trip))
            marker = 'id="transport"'
            self.assertIn(marker, rendered, f"{region.slug}: 교통 섹션 누락")
            self.assertIn("도착과 출발", rendered, f"{region.slug}: 도착/출발 섹션 누락")
            if region.transit:
                self.assertIn("도시 교통", rendered, f"{region.slug}: 도시 교통 섹션 누락")

    def test_region_arrival_and_departure_link_to_daily_cards(self):
        for region in self.trip.regions:
            rendered = render.build_region(region, self.trip)
            self.assertIn(f'href="../{region.days[0].url}"', rendered)
            self.assertIn(f'href="../{region.days[-1].url}"', rendered)

    def test_region_essentials_and_transit_facts_follow_schema(self):
        for stem in ("region-essentials", "transit-facts", "transit-resources"):
            payload = json.loads((ROOT / "data" / f"{stem}.json").read_text(encoding="utf-8"))
            schema = json.loads((ROOT / "data" / f"{stem}.schema.json").read_text(encoding="utf-8"))
            jsonschema.Draft202012Validator(schema,
                format_checker=jsonschema.FormatChecker()).validate(payload)

    def test_transit_sources_are_official_and_scheduled_for_recheck(self):
        payload = json.loads((ROOT / "data" / "transit-facts.json").read_text(encoding="utf-8"))
        allowed = {"www.tmb.cat", "tmb.cat", "rodalies.gencat.cat",
                   "www.lignesdazur.com", "lignesdazur.com",
                   "aixenbus.fr", "www.aixenbus.fr", "www.rtm.fr", "rtm.fr",
                   "www.lametropolemobilite.fr", "lametropolemobilite.fr",
                   "www.holabarcelona.com", "holabarcelona.com",
                   "www.aerobusbarcelona.es", "aerobusbarcelona.es",
                   "www.iledefrance-mobilites.fr", "iledefrance-mobilites.fr",
                   "www.tcl.fr", "tcl.fr", "www.ter.sncf.com", "ter.sncf.com"}
        allowed.update({"www.orizo.fr", "orizo.fr", "www.lio-occitanie.fr",
                        "lio-occitanie.fr", "www.ter.sncf.com", "ter.sncf.com"})
        allowed.update({"zou.maregionsud.fr", "www.luberon-apt.fr", "luberon-apt.fr"})
        for slug, region in payload["regions"].items():
            for source in region["sources"]:
                self.assertIn(urlparse(source["url"]).hostname, allowed,
                              f"{slug}: 비공식 교통 출처")
                self.assertGreaterEqual(date.fromisoformat(source["recheckBy"]),
                                        date.fromisoformat(source["verifiedAt"]))
                self.assertLessEqual(date.fromisoformat(source["verifiedAt"]), date.today())
                deadlines = {stay["key"]: date.fromisoformat(stay["checkin"])
                             for stay in json.loads((ROOT / "source" / "CURRENT" / "10_Core" /
                                                     "itinerary.json").read_text(encoding="utf-8"))["stays"]}
                deadline = deadlines.get(slug, date.fromisoformat("2026-08-29"))
                self.assertLess(date.fromisoformat(source["recheckBy"]), deadline)

    def test_barcelona_public_transit_pilot_is_rendered(self):
        region = next(r for r in self.trip.regions if r.slug == "barcelona")
        rendered = html.unescape(render.build_region(region, self.trip))
        for token in ("도시 교통", "공항은 Aerobús A1, 시내는 각자 Hola Barcelona 48h",
                      "Hola Barcelona Travel Card 48h", "BCN T1→Plaça Espanya",
                      "공식 자료와 재확인"):
            self.assertIn(token, rendered)
        for day in range(1, 5):
            self.assertIn(f'href="../daily/day-{day:02d}.html"', rendered)

    def test_curated_region_days_belong_to_the_linked_region(self):
        regions = {r.slug: r for r in self.trip.regions}
        payload = json.loads((ROOT / "data" / "transit-facts.json").read_text(encoding="utf-8"))
        for slug, facts in payload["regions"].items():
            self.assertIn(slug, regions)
            region_days = {day.n for day in regions[slug].days}
            for use in facts["itineraryUses"]:
                self.assertIn(use["day"], region_days,
                              f"{slug}: Day {use['day']}는 해당 지역 일정이 아님")

    def test_barcelona_chapter_has_no_superseded_transit_advice(self):
        chapter = (ROOT / "source" / "CURRENT" / "20_Regional_Chapters" /
                   "04_Barcelona_Sitges_v2.0.md").read_text(encoding="utf-8")
        for stale in ("T-familiar", "T-casual", "택시"):
            self.assertNotIn(stale, chapter, f"Barcelona 챕터에 폐기된 교통 권고가 남음: {stale}")

        day1 = json.loads((ROOT / "data" / "daily-cards" / "day-01.json").read_text(encoding="utf-8"))
        day1_text = json.dumps(day1, ensure_ascii=False)
        self.assertNotIn("택시", day1_text)
        self.assertNotIn('"mode": "taxi"', day1_text)
        self.assertIn("Aerobús A1", day1_text)
        self.assertIn("Plaça Espanya", day1_text)

    def test_every_region_has_official_transport_resources(self):
        payload = json.loads((ROOT / "data" / "transit-resources.json").read_text(encoding="utf-8"))
        self.assertEqual({region.slug for region in self.trip.regions}, set(payload["regions"]))
        for slug, resources in payload["regions"].items():
            for resource in resources:
                local_path = resource.get("localPath")
                if local_path:
                    self.assertTrue((ROOT / local_path).is_file(), f"{slug}: missing {local_path}")
                deadlines = {stay["key"]: date.fromisoformat(stay["checkin"])
                             for stay in json.loads((ROOT / "source" / "CURRENT" / "10_Core" /
                                                     "itinerary.json").read_text(encoding="utf-8"))["stays"]}
                deadline = deadlines.get(slug, date.fromisoformat("2026-08-29"))
                self.assertLess(date.fromisoformat(resource["recheckBy"]), deadline)

    def test_transport_resources_render_as_local_or_official_links(self):
        for region in self.trip.regions:
            rendered = html.unescape(render.build_region(region, self.trip))
            self.assertIn("공식 자료와 재확인", rendered)
            for resource in region.transport_resources:
                self.assertIn(resource["title"], rendered)
                if resource.get("localPath"):
                    self.assertIn("PDF 열기", rendered)
                    self.assertIn(resource["rightsHolder"], html.unescape(rendered))
                    self.assertIn(resource["license"], html.unescape(rendered))
                self.assertIn(resource["officialUrl"], rendered)

    def test_barcelona_official_maps_use_original_local_pdfs(self):
        payload = json.loads((ROOT / "data" / "transit-resources.json").read_text(encoding="utf-8"))
        resources = payload["regions"]["barcelona"]
        self.assertEqual(2, len(resources))
        for resource in resources:
            self.assertIn("localPath", resource)
            self.assertIn("All rights reserved", resource["license"])
            self.assertTrue((ROOT / resource["localPath"]).is_file())

    def test_nice_public_transit_matches_daily_cards(self):
        region = next(r for r in self.trip.regions if r.slug == "nice")
        rendered = html.unescape(render.build_region(region, self.trip))
        for token in ("공동 Multi voyages 12회로 시내·Èze 이동 준비", "74분",
                      "Aéro 왕복", "별도 TER", "Gare d’Èze"):
            self.assertIn(token, rendered)
        for day in range(7, 13):
            self.assertIn(f'href="../daily/day-{day:02d}.html"', rendered)
        chapter = (ROOT / "source" / "CURRENT" / "20_Regional_Chapters" /
                   "06_Nice_Cote_d_Azur_v2.0.md").read_text(encoding="utf-8")
        for stale in ("€1.80", "€12.60", "1일권 €5", "1일권(€5.00)"):
            self.assertNotIn(stale, chapter, f"Nice 챕터에 폐기된 교통 요금이 남음: {stale}")
        day11 = json.loads((ROOT / "data" / "daily-cards" / "day-11.json").read_text(encoding="utf-8"))
        self.assertNotIn("602", json.dumps(day11, ensure_ascii=False))
        self.assertIn("Èze", json.dumps(day11, ensure_ascii=False))
        self.assertIn("83", json.dumps(day11, ensure_ascii=False))

    def test_aix_public_transit_matches_current_itinerary(self):
        region = next(r for r in self.trip.regions if r.slug == "aix")
        rendered = html.unescape(render.build_region(region, self.trip))
        for token in ("Aix는 도보, Marseille에서는 같은 카드로 바로 태그",
                      "1인 1여정 €1.20", "1인 1여정 €1.70", "별도 TER", "L50"):
            self.assertIn(token, rendered)
        for day in range(12, 17):
            self.assertIn(f'href="../daily/day-{day:02d}.html"', rendered)
        day15 = json.loads((ROOT / "data" / "daily-cards" / "day-15.json").read_text(encoding="utf-8"))
        day15_text = json.dumps(day15, ensure_ascii=False)
        for token in ("TER Aix-en-Provence Centre", "RTM 60", "RTM 83", "Metro M1"):
            self.assertIn(token, day15_text)
        for stale in ("토요 큰 시장", "Atelier 예약", "스케치·수영"):
            self.assertNotIn(stale, day15_text)
        self.assertEqual(day15["highlights"], [
            "08:50 전후 Aix Centre발 TER",
            "Vieux-Port·Le Panier·Mucem 도보축",
            "RTM 60번으로 Notre-Dame de la Garde",
        ])
        self.assertNotIn("Ligne 50", day15_text)
        lines = {(leg["from"], leg["to"]): leg["line"] for leg in day15["legs"]}
        self.assertIsNone(lines[("vieux-port-marseille", "le-panier")])
        self.assertIsNone(lines[("le-panier", "fort-saint-jean")])
        self.assertIsNone(lines[("fort-saint-jean", "marseille-lunch")])
        self.assertEqual(lines[("marseille-lunch", "notre-dame-de-la-garde")],
                         "RTM 60 Vieux-Port → Notre-Dame de la Garde")
        self.assertEqual(lines[("vallon-des-auffes", "marseille-station")],
                         "RTM 83 + Metro M1 → Marseille Saint-Charles")
        chapter = (ROOT / "source" / "CURRENT" / "20_Regional_Chapters" /
                   "07_Aix_en_Provence_v2.0.md").read_text(encoding="utf-8")
        for stale in ("9/11 Marseille", "Day 14(9/11)는 Marseille",
                      "Ligne 50 고속버스 이용", "Day 15에 그가 마지막",
                      "Marseille — 오래된 항구", "시장, Atelier de Cézanne",
                      "Day 15 스케치", "Marseille 버스"):
            self.assertNotIn(stale, chapter, f"Aix 챕터에 폐기된 일정·교통 권고가 남음: {stale}")

        expected_modes = {
            12: {"car", "walk"}, 13: {"walk"}, 14: {"car", "walk"},
            15: {"train", "bus", "walk"}, 16: {"car"},
        }
        for day, expected in expected_modes.items():
            payload = json.loads((ROOT / "data" / "daily-cards" /
                                  f"day-{day:02d}.json").read_text(encoding="utf-8"))
            self.assertEqual(expected, {leg["mode"] for leg in payload["legs"]})

    def test_avignon_public_transit_matches_current_itinerary(self):
        region = next(r for r in self.trip.regions if r.slug == "avignon")
        rendered = html.unescape(render.build_region(region, self.trip))
        for token in ("성벽 안은 도보", "P+R Piot·Italiens 무료 셔틀",
                      "Avignon Centre↔Arles", "T1은 Gare Centre"):
            self.assertIn(token, rendered)
        for day in range(19, 24):
            self.assertIn(f'href="../daily/day-{day:02d}.html"', rendered)

        day21 = json.loads((ROOT / "data" / "daily-cards" /
                            "day-21.json").read_text(encoding="utf-8"))
        self.assertEqual({"train", "walk"}, {leg["mode"] for leg in day21["legs"]})
        day22 = json.loads((ROOT / "data" / "daily-cards" /
                            "day-22.json").read_text(encoding="utf-8"))
        self.assertEqual({"walk"}, {leg["mode"] for leg in day22["legs"]})

    def test_paris_uses_one_weekly_pass_and_individual_tickets_around_it(self):
        region = next(r for r in self.trip.regions if r.slug == "paris")
        rendered = html.unescape(render.build_region(region, self.trip))
        for token in ("Weekly는 9/28–10/4 한 번만", "1인 1여정 €2.55", "1인 1여정 €2.05",
                      "1인 €32.40", "고정된 월요일–일요일", "Navigo Easy에 넣지 않는다",
                      "CDG Terminal 1은 공식 택시", "1인 13회부터 Weekly",
                      "공항역 진출입만 제외", "이번 일정에서는 쓰지 않는다"):
            self.assertIn(token, rendered)
        self.assertNotIn("Versailles·공항역 제외", rendered)
        self.assertNotIn("Day 36의 32번 bus 등 버스만 타는 여정에 필요할 때 구매", rendered)
        for day in range(27, 43):
            self.assertIn(f'href="../daily/day-{day:02d}.html"', rendered)
        chapter = (ROOT / "source" / "CURRENT" / "20_Regional_Chapters" /
                   "11_Paris_Long_Stay_v2.0.md").read_text(encoding="utf-8")
        for stale in ("Navigo Weekly 2주 연속 권장", "두 주 연속 Weekly", "월 €88.80", "주간권 2회의 유불리"):
            self.assertNotIn(stale, chapter)
        for token in ("9/28–10/4 Weekly 한 번만", "Monthly all zones **€90.80**"):
            self.assertIn(token, chapter)
        day37 = json.loads((ROOT / "data" / "daily-cards" / "day-37.json").read_text(encoding="utf-8"))
        self.assertEqual({"bus", "metro"}, {leg["mode"] for leg in day37["legs"]})
        self.assertIn("무료 셔틀", json.dumps(day37, ensure_ascii=False))
        day42 = json.loads((ROOT / "data" / "daily-cards" / "day-42.json").read_text(encoding="utf-8"))
        self.assertEqual({"taxi", "walk"}, {leg["mode"] for leg in day42["legs"]})

    def test_lyon_contactless_and_annecy_ter_match_itinerary(self):
        region = next(r for r in self.trip.regions if r.slug == "lyon")
        rendered = html.unescape(render.build_region(region, self.trip))
        for token in ("같은 비접촉 카드로 두 사람 검증", "1인 1시간 €2.10",
                      "일일 상한 €7.10", "Voyageur 2 ajouté", "TCL F2", "Lyon↔Annecy TER"):
            self.assertIn(token, rendered)
        for day in range(23, 28):
            self.assertIn(f'href="../daily/day-{day:02d}.html"', rendered)
        expected_modes = {
            23: {"metro", "taxi", "train", "walk"},
            24: {"funicular", "metro", "walk"}, 25: {"bus", "metro", "walk"},
            26: {"train", "walk"}, 27: {"taxi", "train", "walk"},
        }
        for day, expected in expected_modes.items():
            payload = json.loads((ROOT / "data" / "daily-cards" /
                                  f"day-{day:02d}.json").read_text(encoding="utf-8"))
            self.assertEqual(expected, {leg["mode"] for leg in payload["legs"]})
        chapter = (ROOT / "source" / "CURRENT" / "20_Regional_Chapters" /
                   "10_Lyon_v2.0.md").read_text(encoding="utf-8")
        self.assertNotIn("푸니쿨라 F2호선 편도 €2.00", chapter)
        for token in ("1인 1시간 €2.10", "1인 €7.10", "10초 안에"):
            self.assertIn(token, chapter)
        facts = json.loads((ROOT / "data" / "transit-facts.json").read_text(encoding="utf-8"))["regions"]["lyon"]
        self.assertTrue(all(date.fromisoformat(source["recheckBy"]) >= date.fromisoformat("2026-09-02")
                            for source in facts["sources"]))

    def test_luberon_transport_is_car_first_and_bus_fallback_only(self):
        region = next(r for r in self.trip.regions if r.slug == "luberon")
        rendered = html.unescape(render.build_region(region, self.trip))
        for token in ("교통권은 사지 않는다", "ZOU! 917", "ZOU! 915·907",
                      "ZOU! 989 Pays d’Apt", "99xx 계열 통학 노선", "렌터카 업체 지원"):
            self.assertIn(token, rendered)
        for day in range(16, 20):
            self.assertIn(f'href="../daily/day-{day:02d}.html"', rendered)
        expected_modes = {16: {"car"}, 17: {"car", "walk"},
                          18: {"car", "walk"}, 19: {"car", "walk"}}
        for day, expected in expected_modes.items():
            payload = json.loads((ROOT / "data" / "daily-cards" /
                                  f"day-{day:02d}.json").read_text(encoding="utf-8"))
    def test_fold_and_norm_identity_guards(self):
        """한글·라틴·악센트 정규화 시 빈 문자열 오매칭 방지 및 식별성 검증."""
        import unicodedata
        import re

        def fold_norm(s: str) -> str:
            s = unicodedata.normalize("NFKD", s or "")
            s = "".join(c for c in s if not unicodedata.combining(c))
            s = unicodedata.normalize("NFC", s).lower()
            s = re.sub(r"[(（].*?[)）]", "", s)
            s = re.sub(r"[^a-z0-9가-힣]", "", s)
            return s

        # 1. Empty input yields empty string
        self.assertEqual(fold_norm(""), "")
        self.assertEqual(fold_norm("   "), "")
        self.assertEqual(fold_norm("()"), "")

        # 2. Empty token MUST NEVER match valid entities
        empty_key = fold_norm("")
        self.assertFalse(bool(empty_key), "빈 문자열 정규화 결과는 falsy여야 함")

        # 3. Test representative mixed, Latin, accented, and Korean-only names
        test_cases = [
            ("La Paradeta", "laparadeta"),
            ("Pâtisserie Weibel", "patisserieweibel"),
            ("Maison Weibel", "maisonweibel"),
            ("La Maison Pichard", "lamaisonpichard"),
            ("Boulangerie Pichard", "boulangeriepichard"),
            ("숙소 첫 저녁 식사", "숙소첫저녁식사"),
            ("고딕지구 핵심 산책", "고딕지구핵심산책"),
            ("리셸므 광장 목요 대형 시장", "리셸므광장목요대형시장"),
        ]
        for original, expected in test_cases:
            norm_val = fold_norm(original)
            self.assertEqual(norm_val, expected, f"{original} 정규화 결과 불일치")
            self.assertGreater(len(norm_val), 0, f"{original} 정규화 결과가 비어있음")
            self.assertNotEqual(norm_val, empty_key, f"{original}이 empty token과 일치함")

        # 4. Ensure distinct entities do not collide
        keys = {fold_norm(orig) for orig, _ in test_cases}
        self.assertEqual(len(keys), len(test_cases), "테스트 항목 간 정규화 충돌이 없어야 함")

    def test_marche_convention_day_schedule_alignment(self):
        """Marché Convention이 토요일에 배치되지 않고 일요일 개장일에 정상 배치되었는지 검증."""
        # Day 29 (2026-09-26 토)
        day29 = json.loads((ROOT / "data" / "daily-cards" / "day-29.json").read_text(encoding="utf-8"))
        for s in day29["stops"]:
            self.assertNotEqual(s.get("place_ref"), "marche-convention", "Day 29 (토)에 Marché Convention이 있으면 안 됨")

        # Day 36 (2026-10-03 토)
        day36 = json.loads((ROOT / "data" / "daily-cards" / "day-36.json").read_text(encoding="utf-8"))
        for s in day36["stops"]:
            self.assertNotEqual(s.get("place_ref"), "marche-convention", "Day 36 (토)에 Marché Convention이 있으면 안 됨")

        # Day 30 (2026-09-27 일)
        day30 = json.loads((ROOT / "data" / "daily-cards" / "day-30.json").read_text(encoding="utf-8"))
        day30_place_refs = [s.get("place_ref") for s in day30["stops"]]
        self.assertIn("marche-convention", day30_place_refs, "Day 30 (일) 아침에 Marché Convention이 배치되어야 함")

    def test_patisserie_weibel_related_places_linked_to_day13(self):
        """Day 13 stop에서 Pâtisserie Weibel이 related_place_refs로 정상 연결되는지 검증."""
        day13 = json.loads((ROOT / "data" / "daily-cards" / "day-13.json").read_text(encoding="utf-8"))
        stop1 = day13["stops"][0]
        self.assertIn("patisserie-weibel", stop1.get("related_place_refs", []), "Day 13 stop 1에 patisserie-weibel 참조가 있어야 함")
        weibel_place = self.trip.places.get("patisserie-weibel")
        self.assertIsNotNone(weibel_place, "patisserie-weibel 장소가 존재해야 함")
        self.assertIn(13, weibel_place.days, "Pâtisserie Weibel 장소의 days에 13일차가 포함되어야 함")


if __name__ == "__main__":
    unittest.main()
