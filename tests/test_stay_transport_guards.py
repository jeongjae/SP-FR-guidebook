"""숙박·교통 지역 화면의 조용한 손실과 교차오염 회귀 검사."""
from __future__ import annotations

import html
import sys
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
