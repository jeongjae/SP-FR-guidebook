"""MP-05 — 관광 조망지도가 자리를 지키는가.

여행 중 낯선 도시에 내려서 가장 먼저 필요한 것은 '무엇이 유명하고 어디쯤
있나' 다. 구글 지도는 목적지를 하나 찍어야 답을 준다. 현지 관광안내소가
종이로 주는 조망지도는 그 반대 방향의 물건이고, 이 테스트는 그것이

  · 파일로 실제 존재하는지
  · 지역 페이지에 실려 오프라인에서 열리는지
  · 권리자와 출처를 잃지 않았는지

를 지킨다. 저작권 표시가 빠진 채 남의 지도를 넣고 다니는 일이 없어야 한다.
"""
from __future__ import annotations

import html as htmllib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "tourist-maps.json"
SITE = ROOT / "site"
ASSETS = ROOT / "source" / "ASSETS"

DATA = json.loads(CATALOG.read_text(encoding="utf-8"))
MAPS = [(region, m) for region, ms in DATA["regions"].items() for m in ms]

# 이 지역들은 지도를 반드시 갖는다 — 실수로 통째로 빠지는 것을 막는다.
REQUIRED = {"barcelona", "girona", "nice", "aix", "luberon", "avignon", "lyon", "paris"}

# 이 고장들은 이번 여행에서 하루 이상 머물거나 주요 방문지다. 이름이 사라지면
# 어느 도시가 지도 없이 남았는지 알 수 없게 된다.
MUST_COVER = {
    "Barcelona", "Sitges", "Cadaqués", "Tossa de Mar", "Collioure",
    "Nice", "Antibes", "Cannes", "Èze", "Villefranche-sur-Mer", "Monaco",
    "Saint-Jean-Cap-Ferrat", "Aix-en-Provence", "Marseille", "Cassis",
    "Gordes", "L'Isle-sur-la-Sorgue", "Roussillon", "Avignon",
    "Saint-Rémy-de-Provence", "Les Baux-de-Provence", "Arles", "Nîmes",
    "Pont du Gard", "Lyon", "Annecy", "Versailles", "Giverny",
}


class TouristMapTests(unittest.TestCase):
    def test_every_map_file_exists_in_the_repo(self):
        """카탈로그에 있는데 파일이 없으면 화면에 빈 자리만 남는다."""
        for region, m in MAPS:
            with self.subTest(map=m["slug"]):
                path = ASSETS / m["localPath"].removeprefix("assets/")
                self.assertTrue(path.is_file(), f"{path} 없음")
                self.assertGreater(path.stat().st_size, 40_000,
                                   f"{m['slug']} 파일이 지나치게 작다")

    def test_local_path_matches_its_region(self):
        """지역을 옮기면서 파일 경로만 그대로 두는 실수를 막는다."""
        for region, m in MAPS:
            with self.subTest(map=m["slug"]):
                self.assertEqual(m["localPath"],
                                 f"assets/tourist-maps/{region}/{m['slug']}.webp")

    def test_every_map_names_its_rights_holder_and_source(self):
        """남의 지도를 싣는다. 누구 것인지와 어디서 왔는지가 항상 붙어 있어야 한다."""
        for region, m in MAPS:
            with self.subTest(map=m["slug"]):
                self.assertTrue(m["rightsHolder"].strip())
                self.assertTrue(m["license"].strip())
                self.assertTrue(m["redistributionBasis"].strip())
                self.assertRegex(m["sourceUrl"], r"^https://")

    def test_required_regions_have_at_least_one_map(self):
        self.assertEqual(REQUIRED, set(DATA["regions"]))
        for region, ms in DATA["regions"].items():
            with self.subTest(region=region):
                self.assertTrue(ms, f"{region} 에 지도가 없다")

    def test_every_visited_place_is_covered(self):
        covered = {m["place"] for _, m in MAPS}
        missing = MUST_COVER - covered
        self.assertFalse(missing, f"지도 없이 남은 고장: {sorted(missing)}")

    def test_region_pages_show_the_maps_and_their_credit(self):
        """빌드한 페이지에 실제로 실려 있는가 — 그리고 저작권 줄과 함께인가."""
        for region, ms in DATA["regions"].items():
            page = SITE / "guide" / f"{region}.html"
            if not page.exists():          # 빌드 전이면 이 검사는 건너뛴다
                self.skipTest("site/ 가 아직 빌드되지 않았다")
            # esc() 가 아포스트로피를 &#x27; 로 바꾼다 — 되돌려 놓고 비교한다
            html = htmllib.unescape(page.read_text(encoding="utf-8"))
            with self.subTest(region=region):
                self.assertIn('id="maps"', html)
                self.assertEqual(len(re.findall(r'class="map-sheet"', html)), len(ms))
                for m in ms:
                    self.assertIn(m["localPath"], html)
                    self.assertIn(m["rightsHolder"], html)

    def test_maps_are_bundled_for_offline_use(self):
        """현지에서 데이터가 없을 때 열려야 한다 — 오프라인 목록에 들어 있어야 한다."""
        manifest = SITE / "offline-files.json"
        if not manifest.exists():
            self.skipTest("site/ 가 아직 빌드되지 않았다")
        precached = {f["path"] for f in json.loads(
            manifest.read_text(encoding="utf-8"))["files"]}
        for region, m in MAPS:
            with self.subTest(map=m["slug"]):
                self.assertIn(m["localPath"], precached)

    def test_usage_note_says_what_the_sheet_is_for(self):
        """'파리 지도' 라고만 적힌 줄은 현장에서 아무 도움이 안 된다."""
        for region, m in MAPS:
            with self.subTest(map=m["slug"]):
                self.assertGreaterEqual(len(m["usage"]), 40)
                self.assertNotIn("**", m["usage"])   # 이 자리는 마크다운이 아니다


if __name__ == "__main__":
    unittest.main()
