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
        render.IMAGES = {"heroes": {}, "by_place": {}}
        render.FACTS = {}

    def test_model_accommodation_consistency(self):
        self.assertEqual([], model.validate(self.trip))

    def test_region_transport_has_no_silent_truncation_or_cross_region_items(self):
        for region in self.trip.regions:
            rendered = html.unescape(render.build_region(region, self.trip))
            marker = '<div id="transport">'
            self.assertIn(marker, rendered, f"{region.slug}: 교통 섹션 누락")
            transport_html = rendered.split(marker, 1)[1]
            ends = [p for p in (transport_html.find('<details class="acc"'),
                                transport_html.find('<div class="alert-card'))
                    if p >= 0]
            if ends:
                transport_html = transport_html[:min(ends)]
            own = []
            foreign = []
            for day in region.days:
                target = own if day.region == region.slug else foreign
                for item in day.transport:
                    if item not in target:
                        target.append(item)

            for item in own:
                item_html = f"<li>{item}</li>"
                self.assertIn(item_html, transport_html,
                              f"{region.slug}: 지역 교통 요약이 조용히 누락됨")
            for item in foreign:
                if item not in own:
                    item_html = f"<li>{item}</li>"
                    self.assertNotIn(item_html, transport_html,
                                     f"{region.slug}: 다른 거점 교통이 혼입됨")

    def test_region_arrival_and_departure_link_to_daily_cards(self):
        for region in self.trip.regions:
            rendered = render.build_region(region, self.trip)
            self.assertIn(f'href="../{region.days[0].url}"', rendered)
            self.assertIn(f'href="../{region.days[-1].url}"', rendered)

    def test_region_essentials_and_transit_facts_follow_schema(self):
        for stem in ("region-essentials", "transit-facts"):
            payload = json.loads((ROOT / "data" / f"{stem}.json").read_text(encoding="utf-8"))
            schema = json.loads((ROOT / "data" / f"{stem}.schema.json").read_text(encoding="utf-8"))
            jsonschema.Draft202012Validator(schema,
                format_checker=jsonschema.FormatChecker()).validate(payload)

    def test_transit_sources_are_official_and_scheduled_for_recheck(self):
        payload = json.loads((ROOT / "data" / "transit-facts.json").read_text(encoding="utf-8"))
        allowed = {"www.tmb.cat", "tmb.cat", "rodalies.gencat.cat"}
        for slug, region in payload["regions"].items():
            for source in region["sources"]:
                self.assertIn(urlparse(source["url"]).hostname, allowed,
                              f"{slug}: 비공식 교통 출처")
                self.assertGreaterEqual(date.fromisoformat(source["recheckBy"]),
                                        date.fromisoformat(source["verifiedAt"]))

    def test_barcelona_public_transit_pilot_is_rendered(self):
        region = next(r for r in self.trip.regions if r.slug == "barcelona")
        rendered = html.unescape(render.build_region(region, self.trip))
        for token in ("도시 공공교통", "현재 일정은 단일 승차가 기본",
                      "T-familiar 1 zone", "공항 L9 불가",
                      "공식 출처와 재확인일"):
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


if __name__ == "__main__":
    unittest.main()
