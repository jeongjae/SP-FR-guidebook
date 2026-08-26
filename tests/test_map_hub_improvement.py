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

    def test_map_index_has_no_regional_maps_or_whole_trip_headings(self):
        """'지역별 지도' 및 '전체 여정 지도' 섹션 제목이 map/index.html 에 존재하지 않는지 확인."""
        map_html = (ROOT / "site" / "map" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("지역별 지도", map_html, "'지역별 지도' 제목/섹션이 index.html 에 존재하지 않아야 함")
        self.assertNotIn("전체 여정 지도", map_html, "'전체 여정 지도' 제목/섹션이 index.html 에 존재하지 않아야 함")

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
        self.assertEqual(len(routes), 39, "Day 14 차량 회수 포함 총 39개 경로 항목이 정의되어야 함")

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

        day14_cassis_aix = routes.get("day-14:cassis-vehicle-return")
        self.assertIsNotNone(day14_cassis_aix)
        self.assertEqual(day14_cassis_aix["origin"], "Parking relais des Gorguettes, Cassis")
        self.assertEqual(day14_cassis_aix["destination"], "2 Place Coimbra, Résidence Les Toits de Méjanes, 13090 Aix-en-Provence")
        self.assertEqual(day14_cassis_aix["travelMode"], "driving")

        day14_port_miou = routes.get("day-14:cassis-port-miou")
        self.assertIsNotNone(day14_port_miou)
        self.assertEqual(day14_port_miou["destination"], "Parking relais des Gorguettes, Cassis")
        self.assertEqual(day14_port_miou["travelMode"], "transit")

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
        """map/index.html이 8개 독립 Region 섹션, 개별 지도, 1~N 번호 매겨진 목록 구조를 갖추었는지 검증."""
        map_html = (ROOT / "site" / "map" / "index.html").read_text(encoding="utf-8")
        
        # 1. '지역별 지도' 및 '전체 여정 지도' 헤딩 부재 확인
        self.assertNotIn("지역별 지도", map_html, "'지역별 지도' 섹션/헤딩이 제거되어야 함")
        self.assertNotIn("전체 여정 지도", map_html, "'전체 여정 지도' 섹션/헤딩이 제거되어야 함")

        # 2. 8 Region headings in exact order
        expected_regions = [
            ("barcelona", "Barcelona", 17),
            ("girona", "Girona · Empordà", 6),
            ("nice", "Nice · Côte d'Azur", 26),
            ("aix", "Aix-en-Provence", 21),
            ("luberon", "Luberon", 11),
            ("avignon", "Avignon · Alpilles", 24),
            ("lyon", "Lyon", 18),
            ("paris", "Paris", 42),
        ]
        last_pos = 0
        total_pins = 0
        for r_slug, r_name, count in expected_regions:
            section_tag = f'id="section-{r_slug}"'
            pos = map_html.find(section_tag, last_pos)
            self.assertNotEqual(pos, -1, f"Region section {r_name} not found or out of order")
            head_tag = f'<h2>{render.esc(r_name)}</h2>'
            self.assertIn(head_tag, map_html[pos:pos+500], f"Region heading {r_name} missing in section")
            total_pins += count
            last_pos = pos

        self.assertEqual(total_pins, 165, "Day 14 차량 회수는 기존 Gorguettes 핀을 재사용하므로 총 핀 수는 165여야 함")

        # 3. 8개의 map-card 및 script data가 존재하는지 확인
        map_cards = re.findall(r'<div class="map-card">', map_html)
        self.assertEqual(len(map_cards), 8, "8개 Region별 map-card가 존재해야 함")

        # 4. 각 Region별 지도 marker와 목록 번호 일치성 (1부터 N까지 순차 번호)
        scripts = re.findall(r'<script type="application/json" class="map-data-script">({.*?})</script>', map_html)
        self.assertEqual(len(scripts), 8, "8개 Region map-data script가 존재해야 함")
        for (r_slug, r_name, expected_count), script_json in zip(expected_regions, scripts):
            data = json.loads(script_json)
            pins = data.get("pins", [])
            self.assertEqual(len(pins), expected_count, f"{r_name} pin 개수 불일치: {len(pins)} != {expected_count}")

        # 5. List item numbers check (1. ~ N.)
        for r_slug, r_name, expected_count in expected_regions:
            for num in range(1, expected_count + 1):
                num_tag = f'<span class="map-num">{num}.</span>'
                self.assertIn(num_tag, map_html, f"{r_name} 목록에 {num}. 번호 태그가 누락됨")

        # 6. Date pattern check: M.D (월|화|수|목|금|토|일) [HH:MM]
        date_pattern = re.compile(r'<span class="meta">(\d{1,2}\.\d{1,2}\s+[월화수목금토일](\s+\d{2}:\d{2})?)</span>')
        matches = date_pattern.findall(map_html)
        self.assertEqual(len(matches), 165, "165개 항목 모두 날짜 메타가 존재해야 함")

        # 7. Verify specific items
        self.assertIn("Lagrange Aparthotel Lyon Lumière → Lyon Part-Dieu", map_html)
        self.assertIn("Gare de Lyon → 78 Rue de Lourmel", map_html)
        self.assertNotIn("data-pin=\"bcn-airport\"", map_html)
        self.assertNotIn("data-pin=\"paris-return\"", map_html)

    def test_all_rendered_google_maps_urls_are_valid(self):
        """사이트 전체의 모든 Google Maps 링크가 올바른 search 또는 dir 형식인지 검증."""
        all_html = list((ROOT / "site").rglob("*.html"))
        gmaps_urls = []
        pattern = re.compile(r'href="(https://www\.google\.com/maps/[^"]+)"')

        # /maps/place/ 퍼머링크는 길찾기가 아니라 **출처 인용**이다. Google Maps
        # 사진을 쓴 자리는 그 사진이 그 업소의 것이라는 근거로 placeKey 가 든
        # 퍼머링크를 남긴다 — search?api=1 로 바꾸면 근거가 사라진다.
        # 우리가 만드는 길찾기 링크는 언제나 /maps/dir/ 또는 /maps/search/ 다.
        citations = []
        for f in all_html:
            content = f.read_text(encoding="utf-8")
            for m in pattern.finditer(content):
                url = m.group(1).replace("&amp;", "&")
                target = (citations if urlparse(url).path.startswith("/maps/place/")
                          else gmaps_urls)
                target.append((f.name, url))

        self.assertGreater(len(gmaps_urls), 200, "전체 사이트에 구글맵 링크가 충분히 존재해야 함")

        # 인용 링크도 아무 주소나 되어서는 안 된다 — placeKey 가 들어 있어야 한다.
        for fname, url in citations:
            self.assertIn("!1s0x", url,
                          f"{fname}: 출처 인용에 placeKey 가 없다 — {url}")

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
