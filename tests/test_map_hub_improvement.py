"""지도 페이지 및 구글맵 허브 개선 검증 테스트."""
import json
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))

import model  # noqa: E402
import render  # noqa: E402


class MapHubImprovementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trip = model.load_trip()
        cls.map_index_html = (ROOT / "site" / "map" / "index.html").read_text(encoding="utf-8")
        cls.map_queries = json.loads((ROOT / "data" / "map-queries.json").read_text(encoding="utf-8"))

    def test_regional_maps_section_is_at_the_top(self):
        """지역별 지도 섹션이 전체 여정 지도보다 위에 위치하는지 확인."""
        idx_regional = self.map_index_html.find("지역별 지도")
        idx_whole_trip = self.map_index_html.find("전체 여정 지도")
        self.assertNotEqual(idx_regional, -1, "지역별 지도 섹션이 index.html 에 존재해야 함")
        self.assertNotEqual(idx_whole_trip, -1, "전체 여정 지도 섹션이 index.html 에 존재해야 함")
        self.assertLess(idx_regional, idx_whole_trip, "지역별 지도가 전체 여정 지도보다 상단에 위치해야 함")

    def test_non_map_stops_completely_removed_from_map_pages_and_cards(self):
        """비장소 3종이 모든 지도 페이지 및 지도 카드에서 0건인지 확인."""
        forbidden_in_maps = [
            "CDG 공항 출국 수속 & OZ502 탑승",
            "기내박 — OZ502 취침 및 수분 섭취",
            "인천국제공항 제1여객터미널 도착 (ICN)",
            "cdg-departure",
            "inflight",
            "icn",
        ]

        # 1. Check all map pages
        map_dir = ROOT / "site" / "map"
        for map_html_path in map_dir.glob("*.html"):
            content = map_html_path.read_text(encoding="utf-8")
            for forbidden in forbidden_in_maps:
                self.assertNotIn(
                    f'data-pin="{forbidden}"',
                    content,
                    f"{map_html_path.name} map-list 에 {forbidden} 핀이 포함됨"
                )

        # 2. Check all daily pages' map cards
        daily_dir = ROOT / "site" / "daily"
        for day_html_path in daily_dir.glob("*.html"):
            content = day_html_path.read_text(encoding="utf-8")
            if '<div class="map-card">' in content:
                map_card_part = content.split('<div class="map-card">', 1)[1].split('</div></div>', 1)[0]
                for forbidden in ["cdg-departure", "inflight", "icn"]:
                    self.assertNotIn(
                        f'data-pin="{forbidden}"',
                        map_card_part,
                        f"{day_html_path.name} map card 에 {forbidden} 핀이 포함됨"
                    )

    def test_non_map_stops_preserved_in_daily_itineraries(self):
        """비장소 3종이 일정표/타임라인에는 온전히 보존되어 있는지 확인."""
        day42_html = (ROOT / "site" / "daily" / "day-42.html").read_text(encoding="utf-8")
        day43_html = (ROOT / "site" / "daily" / "day-43.html").read_text(encoding="utf-8")

        self.assertIn("CDG 공항 출국 수속", day42_html, "Day 42 일정에 CDG 출국 수속이 보존되어야 함")
        self.assertIn("기내박 — OZ502", day43_html, "Day 43 일정에 기내박이 보존되어야 함")
        self.assertIn("인천국제공항 제1여객터미널", day43_html, "Day 43 일정에 ICN 도착이 보존되어야 함")

    def test_place_queries_are_clean_and_normalized(self):
        """Place 검색어가 한국어 동작 수식어 없이 정규화되어 있는지 확인."""
        stops_dict = {s.id: s for d in self.trip.days for s in d.stops}
        
        # Specific place tests requested in prompt
        # 1. Sant Feliu
        s = stops_dict["sant-feliu"]
        self.assertEqual(s.map_query, "Sant Feliu de Guixols")

        # 2. Vallon des Auffes
        s = stops_dict["vallon-des-auffes"]
        self.assertEqual(s.map_query, "Vallon des Auffes, Marseille")

        # 3. Vieil Avignon
        s = stops_dict["vieil-avignon"]
        self.assertEqual(s.map_query, "Centre Historique d'Avignon, 84000 Avignon")

        # 4. Hertz rental Avignon TGV
        s = stops_dict["avignon-tgv"]
        self.assertEqual(s.map_query, "Hertz, Gare TGV d'Avignon, Place de l'Europe, 84000 Avignon")

        # Check all place entries for bad tokens in query
        bad_tokens = ["점심", "저녁", "산책", "관람", "방문", "(선택)", "(추천)", "(필수)", "➔", "→"]
        for p_slug, p_data in self.map_queries.get("places", {}).items():
            for tok in bad_tokens:
                self.assertNotIn(tok, p_data["query"], f"place {p_slug} query contains bad token: {tok}")

        for s_id, s_data in self.map_queries.get("stops", {}).items():
            for tok in bad_tokens:
                self.assertNotIn(tok, s_data["query"], f"stop {s_id} query contains bad token: {tok}")

    def test_route_urls_are_directions_with_valid_modes(self):
        """Route 항목이 Google Maps Directions 링크로 렌더링되고 이동수단이 일치하는지 확인."""
        routes = self.map_queries.get("routes", {})
        self.assertEqual(len(routes), 29, "총 29개 경로 항목이 정의되어야 함")

        # Spot check key routes
        day9_nice_antibes = routes.get("day-09:nice-ville")
        self.assertIsNotNone(day9_nice_antibes)
        self.assertEqual(day9_nice_antibes["origin"], "Gare de Nice-Ville")
        self.assertEqual(day9_nice_antibes["destination"], "Gare d'Antibes")
        self.assertEqual(day9_nice_antibes["travelMode"], "transit")

        day15_aix_marseille = routes.get("day-15:aix-station")
        self.assertIsNotNone(day15_aix_marseille)
        self.assertEqual(day15_aix_marseille["origin"], "Gare d'Aix-en-Provence")
        self.assertEqual(day15_aix_marseille["destination"], "Marseille Saint-Charles")
        self.assertEqual(day15_aix_marseille["travelMode"], "transit")

        day14_cassis_aix = routes.get("day-14:aix-return")
        self.assertIsNotNone(day14_cassis_aix)
        self.assertEqual(day14_cassis_aix["origin"], "Port de Cassis")
        self.assertEqual(day14_cassis_aix["destination"], "2 Place Coimbra, 13090 Aix-en-Provence")
        self.assertEqual(day14_cassis_aix["travelMode"], "driving")

        # Spot check day 27 direction routes
        day27_lyon = routes.get("day-27:lyon-checkout")
        self.assertIsNotNone(day27_lyon)
        self.assertIn("Lagrange Aparthotel Lyon Lumière", day27_lyon["origin"])
        self.assertEqual(day27_lyon["destination"], "Gare de Lyon-Part-Dieu")
        self.assertEqual(day27_lyon["travelMode"], "transit")

        day27_paris = routes.get("day-27:paris-checkin")
        self.assertIsNotNone(day27_paris)
        self.assertEqual(day27_paris["origin"], "Paris Gare de Lyon")
        self.assertEqual(day27_paris["destination"], "78 Rue de Lourmel, 75015 Paris")
        self.assertEqual(day27_paris["travelMode"], "transit")

        # Verify generated HTML hrefs
        day9_html = (ROOT / "site" / "daily" / "day-09.html").read_text(encoding="utf-8")
        self.assertIn("https://www.google.com/maps/dir/?api=1&amp;origin=Gare%20de%20Nice-Ville&amp;destination=Gare%20d%27Antibes&amp;travelmode=transit", day9_html)

        day15_html = (ROOT / "site" / "daily" / "day-15.html").read_text(encoding="utf-8")
        self.assertIn("https://www.google.com/maps/dir/?api=1&amp;origin=Gare%20d%27Aix-en-Provence&amp;destination=Marseille%20Saint-Charles&amp;travelmode=transit", day15_html)

        day27_html = (ROOT / "site" / "daily" / "day-27.html").read_text(encoding="utf-8")
        self.assertIn("Lagrange%20Aparthotel%20Lyon%20Lumi%C3%A8re", day27_html)
        self.assertIn("78%20Rue%20de%20Lourmel", day27_html)

    def test_map_index_region_groups_and_date_formatting(self):
        """전체 여정 지도 목록이 8개 지역으로 그룹화되고 날짜/요일이 올바른 형식인지 검증."""
        map_html = (ROOT / "site" / "map" / "index.html").read_text(encoding="utf-8")
        
        # 1. 8 Region headings in order
        expected_regions = [
            "Barcelona",
            "Girona · Empordà",
            "Nice · Côte d'Azur",
            "Aix-en-Provence",
            "Luberon",
            "Avignon · Alpilles",
            "Lyon",
            "Paris",
        ]
        last_pos = 0
        for r_name in expected_regions:
            head_tag = f'<h3 class="map-region-head">{render.esc(r_name)}</h3>'
            pos = map_html.find(head_tag, last_pos)
            self.assertNotEqual(pos, -1, f"Region group {r_name} heading not found or out of order")
            last_pos = pos

        # 2. Date pattern check: M.D (월|화|수|목|금|토|일) [HH:MM]
        date_pattern = re.compile(r'<span class="meta">(\d{1,2}\.\d{1,2}\s+[월화수목금토일](\s+\d{2}:\d{2})?)</span>')
        matches = date_pattern.findall(map_html)
        self.assertGreater(len(matches), 100, "지도 목록의 날짜 메타가 충분히 발견되어야 함")

        # 3. Verify specific items
        self.assertIn("Lagrange Aparthotel Lyon Lumière → Lyon Part-Dieu", map_html)
        self.assertIn("Gare de Lyon → 78 Rue de Lourmel", map_html)
        self.assertNotIn("data-pin=\"bcn-airport\"", map_html)
        self.assertNotIn("data-pin=\"paris-return\"", map_html)

    def test_all_rendered_google_maps_urls_are_valid(self):
        """사이트 전체의 모든 Google Maps 링크가 올바른 search 또는 dir 형식인지 검증."""
        all_html = list((ROOT / "site").rglob("*.html"))
        gmaps_urls = []
        pattern = re.compile(r'href="(https://www\.google\.com/maps/[^"]+)"')

        for f in all_html:
            content = f.read_text(encoding="utf-8")
            for m in pattern.finditer(content):
                gmaps_urls.append((f.name, m.group(1).replace("&amp;", "&")))

        self.assertGreater(len(gmaps_urls), 200, "전체 사이트에 구글맵 링크가 충분히 존재해야 함")

        for fname, url in gmaps_urls:
            parsed = urlparse(url)
            self.assertEqual(parsed.hostname, "www.google.com")
            qs = parse_qs(parsed.query)
            self.assertEqual(qs.get("api"), ["1"], f"{fname}: missing api=1 in {url}")

            if parsed.path.startswith("/maps/dir/"):
                # Either full route (origin + destination + travelmode) or place navigation button (destination)
                self.assertIn("destination", qs, f"{fname}: missing destination in dir url {url}")
                if "origin" in qs:
                    self.assertIn("travelmode", qs, f"{fname}: missing travelmode in route dir url {url}")
                    self.assertIn(qs["travelmode"][0], {"driving", "transit", "walking", "bicycling"})
            elif parsed.path.startswith("/maps/search/"):
                self.assertIn("query", qs, f"{fname}: missing query in search url {url}")
                query_val = qs["query"][0]
                self.assertGreater(len(query_val), 1, f"{fname}: empty query in {url}")
                self.assertNotIn("\n", query_val)
            else:
                self.fail(f"Invalid Google Maps URL path in {fname}: {url}")


if __name__ == "__main__":
    unittest.main()
