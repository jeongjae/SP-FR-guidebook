import unittest
import sys
import re
import json
from pathlib import Path
from io import StringIO

sys.path.append(str(Path(__file__).parent))
import content_guard
import fact_guard
import identity_match
import model

# 경로는 여기서 직접 잡는다. 예전에는 build.py 에서 빌려 왔는데, 그 파일이
# 은퇴하면서 이 테스트가 렌더러에 묶일 이유가 없어졌다 — 여기서 보는 것은
# 전부 **원고 쪽 규칙**이다.
ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source"
COMMERCIAL_CARDS = SOURCE / "ASSETS/89_Commercial_City_Experience_Cards_v1.0.md"
PLACE_DOSSIERS = SOURCE / "ASSETS/90_Regional_Context_and_Place_Dossier_Compendium_v1.0.md"
PLACE_REGISTRY = SOURCE / "ASSETS/91_Place_Registry_v1.0.md"
NICE_CHAPTER = SOURCE / "CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md"
SCHEMA_PATH = SOURCE.parent / "build" / "content_schema.json"
TOURIST_MAPS = ROOT / "data" / "tourist-maps.json"

RS_SAMPLE_REGION = """---
slug: "06-nice"
title: "Nice & Côte d’Azur"
content_schema: rs-region-v1
---

# Commercial Guide Module

## 꼭 경험할 세 장면
## 현장 관람과 시간표
## 숙소·생활권·체크인/아웃
## 4. Day 1 — 9월 4일 금요일
## 5. Day 2 — 9월 5일 토요일
## 6. Day 3 — 9월 6일 일요일
## 7. Day 4 — 9월 7일 월요일
## 8. Day 5 — 9월 8일 화요일
## 9. Day 6 — 9월 9일 수요일
## 음식·시장·카페·생활체험
## 이동·주차·비용·귀가
## 이 지역을 이해하는 축
## 당일치기·우천·피로 대안
## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계
"""

# 이 테스트는 추적 대상 원고를 **실제로 망가뜨렸다가 되돌린다**. 가드가
# 진짜로 잡는지 보려면 그 방법밖에 없다. 다만 중간에 죽으면 리포가 더러운
# 채 남고, 콘텐츠 편집이 병행되는 지금은 그 오염이 남의 커밋에 섞여 들어갈
# 수 있다 — 실제로 dummy-slug 가 명부와 스키마에 남아 있었다.
#
# 그래서 복구를 addCleanup 에 건다. setUp 이 반쯤 끝나고 죽어도, 테스트가
# 예외로 끝나도 등록된 것부터 되돌아간다.
MUTATED_FILES = None   # 아래 setUp 이 채운다


# 이 스위트는 추적 대상 원고를 실제로 망가뜨렸다가 되돌린다. 두 프로세스가
# 동시에 돌면 서로의 백업·복원이 엇갈려 **원고가 깨진 채 남는다.** 실제로
# 그렇게 Nice 챕터의 필수 헤딩이 통째로 날아간 적이 있다.
# 파일 잠금으로 한 번에 하나만 돌게 막는다.
_LOCK_PATH = Path(__file__).resolve().parent / ".test_validation.lock"


def _acquire_lock():
    import fcntl
    handle = open(_LOCK_PATH, "w")
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        handle.close()
        raise SystemExit(
            "test_validation 이 이미 다른 프로세스에서 돌고 있다. "
            "이 스위트는 원고를 고쳤다 되돌리므로 동시에 돌리면 원고가 깨진다.")
    return handle


_LOCK_HANDLE = _acquire_lock()


class TestValidationGuards(unittest.TestCase):
    def _assert_clean(self):
        """정리가 끝난 뒤 잔재가 없는지 본다. cleanup 은 LIFO 라 가장 먼저
        등록한 이것이 가장 늦게 돈다."""
        for path in (PLACE_REGISTRY, SCHEMA_PATH):
            if "dummy-slug" in path.read_text(encoding="utf-8"):
                raise AssertionError(
                    f"테스트 잔재가 {path.name} 에 남았다 — git checkout 으로 되돌려라")

    def setUp(self):
        self.addCleanup(self._assert_clean)
        for path in (NICE_CHAPTER, PLACE_DOSSIERS, PLACE_REGISTRY, SCHEMA_PATH):
            original = path.read_text(encoding="utf-8")
            self.addCleanup(path.write_text, original, encoding="utf-8")
        self.nice_backup = NICE_CHAPTER.read_text(encoding="utf-8")
        self.dossier_backup = PLACE_DOSSIERS.read_text(encoding="utf-8")
        self.registry_backup = PLACE_REGISTRY.read_text(encoding="utf-8")
        self.schema_backup = SCHEMA_PATH.read_text(encoding="utf-8")



    def run_validation(self):
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            content_guard.check_phase9_commercial_depth_guards()
            success = True
            output = sys.stdout.getvalue()
        except SystemExit as e:
            success = (e.code == 0)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
        return success, output

    def test_normal_pass(self):
        # Normal files should successfully pass
        success, output = self.run_validation()
        self.assertTrue(success, f"Normal pass failed: {output}")
        self.assertIn("Phase 9 상용편집·장소심화 가드: 스키마 및 레지스트리-Dossier 검증 이상 없음", output)

    def test_missing_required_h2(self):
        # Remove a required H2 from sample rs-region-v1 content
        bad_content = RS_SAMPLE_REGION.replace("## 꼭 경험할 세 장면", "## 다른 장면")
        NICE_CHAPTER.write_text(bad_content, encoding="utf-8")
        success, output = self.run_validation()
        self.assertFalse(success)
        self.assertIn("06_Nice_Cote_d_Azur_v2.0.md: 필수 헤딩 누락 — 꼭 경험할 세 장면", output)

    def test_out_of_order_h2(self):
        # Swap order of two required H2s in sample rs-region-v1 content
        bad_content = RS_SAMPLE_REGION.replace(
            "## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계", "TEMP_VERDICT"
        ).replace(
            "## 꼭 경험할 세 장면", "## Editor’s Verdict — 이 지역에 시간을 쓸 가치와 한계"
        ).replace(
            "TEMP_VERDICT", "## 꼭 경험할 세 장면"
        )
        NICE_CHAPTER.write_text(bad_content, encoding="utf-8")
        success, output = self.run_validation()
        self.assertFalse(success)
        self.assertIn("06_Nice_Cote_d_Azur_v2.0.md: 헤딩 순서 오류", output)

    def test_duplicate_h2(self):
        # Add a duplicate H2 in sample rs-region-v1 content
        bad_content = RS_SAMPLE_REGION.replace(
            "## 꼭 경험할 세 장면", "## 꼭 경험할 세 장면\n\n## 꼭 경험할 세 장면"
        )
        NICE_CHAPTER.write_text(bad_content, encoding="utf-8")
        success, output = self.run_validation()
        self.assertFalse(success)
        self.assertIn("06_Nice_Cote_d_Azur_v2.0.md: 중복 헤딩 발견 — 꼭 경험할 세 장면", output)

    def test_unknown_content_schema(self):
        # Set schema to unknown-schema in sample content
        bad_content = RS_SAMPLE_REGION.replace("content_schema: rs-region-v1", "content_schema: unknown-schema")
        NICE_CHAPTER.write_text(bad_content, encoding="utf-8")
        success, output = self.run_validation()
        self.assertFalse(success)
        self.assertIn("06_Nice_Cote_d_Azur_v2.0.md: 알 수 없는 content_schema 값 — unknown-schema", output)

    def test_registry_item_missing_dossier(self):
        # Add new spot in registry and mapping, but don't add to dossier compendium
        schema_data = json.loads(self.schema_backup)
        schema_data["dossier_mapping"]["dummy-slug"] = {"heading": "Nonexistent Dossier", "region": "nice"}
        SCHEMA_PATH.write_text(json.dumps(schema_data, indent=2, ensure_ascii=False), encoding="utf-8")

        # Add to place registry
        reg_lines = self.registry_backup.splitlines()
        for idx, line in enumerate(reg_lines):
            if "cours-saleya" in line:
                reg_lines.insert(idx + 1, "| `dummy-slug` | Dummy Place | spot | 필수 | — | chapters/nice/places.html | Dummy Place | Dummy |")
                break
        PLACE_REGISTRY.write_text("\n".join(reg_lines), encoding="utf-8")

        success, output = self.run_validation()
        self.assertFalse(success)
        self.assertIn("레지스트리에 대응되는 dossier 누락 발견 (ID: dummy-slug, 헤딩: Nonexistent Dossier)", output)

    def test_orphan_dossier(self):
        # Add a dossier in the compendium that is not mapped in schema
        bad_content = self.dossier_backup.replace(
            "# Nice", "# Nice\n\n## Dummy Orphan Dossier\n- 방문: 도보\n- 관람: 외관\n- 체류: 10분\n- 요금·예약: 무료\n- 주의: 없음\n- 공식정보: https://example.com"
        )
        PLACE_DOSSIERS.write_text(bad_content, encoding="utf-8")
        success, output = self.run_validation()
        self.assertFalse(success)
        self.assertIn("레지스트리 매핑이 없는 orphan dossier 발견: Dummy Orphan Dossier", output)

    def test_duplicate_place_walk_id(self):
        # Add duplicate dossier heading
        bad_content = self.dossier_backup.replace(
            "## Cours Saleya", "## Cours Saleya\n...\n\n## Cours Saleya"
        )
        PLACE_DOSSIERS.write_text(bad_content, encoding="utf-8")
        success, output = self.run_validation()
        self.assertFalse(success)
        self.assertIn("Dossier 중복 헤딩 발견: Cours Saleya", output)

    def test_walk_missing_required_fields(self):
        # Remove - 공식정보 from Nice Old Town–Castle Hill Walk dossier
        bad_content = self.dossier_backup.replace(
            "- 공식정보: https://www.explorenicecotedazur.com/", ""
        )
        PLACE_DOSSIERS.write_text(bad_content, encoding="utf-8")
        success, output = self.run_validation()
        self.assertFalse(success)
        self.assertIn("Dossier Nice Old Town–Castle Hill Walk (nice-walk): 필수 필드 누락 — 공식정보", output)

    def test_missing_official_source(self):
        # Remove - 공식정보 from Cours Saleya dossier
        bad_content = self.dossier_backup.replace(
            "- 공식정보: https://www.explorenicecotedazur.com/", "- 공식정보: "
        )
        PLACE_DOSSIERS.write_text(bad_content, encoding="utf-8")
        success, output = self.run_validation()
        self.assertTrue(not success)
        self.assertIn("Dossier Cours Saleya (cours-saleya): 필수 필드 누락 — 공식정보", output)

    def test_broken_day_reference_is_caught(self):
        """하루의 구간이 그날 없는 장소를 가리키면 잡아야 한다.

        예전에는 챕터 원고의 피로도 표기 누락을 봤다. 이제 하루의 정본은
        data/daily-cards/*.json 이고, 거기서 가장 위험한 파손은 동선이
        존재하지 않는 지점을 가리키는 것이다 — 현장에서 길이 끊긴다.
        """
        trip = model.load_trip()
        self.assertEqual(model.validate(trip), [], "정상 데이터가 검증에 걸린다")

        day = trip.day(2)
        original = list(day.legs)
        try:
            day.legs.append(model.Leg(frm="does-not-exist", to=day.stops[0].id,
                                      mode="walk"))
            problems = model.validate(trip)
            self.assertTrue(
                any("does-not-exist" in p for p in problems),
                "없는 지점을 가리키는 구간을 검증이 놓쳤다")
        finally:
            day.legs[:] = original

    def test_every_day_has_fatigue(self):
        """43일 전부 피로도가 있어야 한다. 없으면 하루 강도를 못 읽는다."""
        trip = model.load_trip()
        missing = [d.n for d in trip.days if not d.fatigue]
        self.assertEqual(missing, [], f"피로도 없는 날: {missing}")

    def test_stale_tourist_map_recheck_is_caught(self):
        """관광지도 재확인 날짜가 그 지역 체크인을 넘기면 잡아야 한다.

        관광청 지도는 링크다. 링크는 조용히 죽는다 — 현장에서 눌렀을 때
        404 가 뜨는 지도는 없느니만 못하다. 그래서 체크인 전에 사람이 한 번
        열어 보도록 날짜로 강제한다.
        """
        backup = TOURIST_MAPS.read_text(encoding="utf-8")
        try:
            data = json.loads(backup)
            data["regions"]["barcelona"][0]["recheckBy"] = "2026-09-30"
            TOURIST_MAPS.write_text(json.dumps(data, ensure_ascii=False),
                                    encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                model.load_trip()
            self.assertIn("tourist map recheckBy", str(caught.exception))
        finally:
            TOURIST_MAPS.write_text(backup, encoding="utf-8")

    def test_unknown_tourist_map_kind_is_caught(self):
        """렌더러가 모르는 지도 종류가 들어오면 멈춘다.

        어휘 가드와 같은 이유다. 모르는 값은 화면에 영어 코드로 샌다.
        """
        backup = TOURIST_MAPS.read_text(encoding="utf-8")
        try:
            data = json.loads(backup)
            data["regions"]["barcelona"][0]["kind"] = "subway-map"
            TOURIST_MAPS.write_text(json.dumps(data, ensure_ascii=False),
                                    encoding="utf-8")
            with self.assertRaises(Exception) as caught:
                model.load_trip()
            self.assertIn("subway-map", str(caught.exception))
        finally:
            TOURIST_MAPS.write_text(backup, encoding="utf-8")

    def test_tourist_map_region_must_exist(self):
        """없는 지역에 매달린 관광지도는 어느 화면에도 뜨지 않는다.

        오타 하나로 지도가 통째로 사라지고, 사라진 줄도 모른다.
        """
        backup = TOURIST_MAPS.read_text(encoding="utf-8")
        try:
            data = json.loads(backup)
            data["regions"]["barthelona"] = data["regions"].pop("barcelona")
            TOURIST_MAPS.write_text(json.dumps(data, ensure_ascii=False),
                                    encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                model.load_trip()
            self.assertIn("not a trip region", str(caught.exception))
        finally:
            TOURIST_MAPS.write_text(backup, encoding="utf-8")

    def test_missing_confirmed_fact_token(self):
        # Remove confirmed hotel phone token from Barcelona chapter
        barcelona_path = SOURCE / "CURRENT/20_Regional_Chapters/04_Barcelona_Sitges_v2.0.md"
        barcelona_backup = barcelona_path.read_text(encoding="utf-8")
        try:
            bad_content = barcelona_backup.replace("+34 936 26 88 44", "+34 000 00 00 00")
            barcelona_path.write_text(bad_content, encoding="utf-8")

            old_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                fact_guard.check_confirmed_fact_token_guards()
                success = True
            except SystemExit as e:
                success = (e.code == 0)
            finally:
                output = sys.stdout.getvalue()
                sys.stdout = old_stdout

            self.assertFalse(success)
            self.assertIn("확정 사실 토큰 생존 가드 실패:", output)
            self.assertIn("토큰 누락: '+34 936 26 88 44'", output)
        finally:
            barcelona_path.write_text(barcelona_backup, encoding="utf-8")

    def test_missing_manifest_fact_token(self):
        # Remove chapter-resident token (€809.54) from Nice chapter
        nice_path = SOURCE / "CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md"
        nice_backup = nice_path.read_text(encoding="utf-8")
        try:
            bad_content = nice_backup.replace("€809.54", "€000.00")
            nice_path.write_text(bad_content, encoding="utf-8")

            old_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                fact_guard.check_confirmed_fact_token_guards()
                success = True
            except SystemExit as e:
                success = (e.code == 0)
            finally:
                output = sys.stdout.getvalue()
                sys.stdout = old_stdout

            self.assertFalse(success)
            self.assertIn("확정 사실 토큰 생존 가드 실패:", output)
            self.assertIn("토큰 누락: '€809.54'", output)
        finally:
            nice_path.write_text(nice_backup, encoding="utf-8")


class TestIdentityMatch(unittest.TestCase):
    """업소 신원 대조 — 빈 정규화가 통과하면 남의 가게 사진이 붙는다.

    실제로 났던 일이다. Google Maps 가 'La Paradeta' 자리에서 번역된
    분류명('푸에스토시요 해산물 요리')을 돌려줬고, 그것을 접으니 빈
    문자열이 됐다. 빈 문자열은 어떤 문자열에도 들어 있어 부분일치가
    무조건 참이 됐다.
    """

    def test_empty_fold_never_matches(self):
        # 한글만 있는 표시 이름 — 접으면 빈 문자열이 된다
        self.assertEqual(identity_match.fold("푸에스토시요 해산물 요리"), "")
        self.assertFalse(
            identity_match.names_match(["La Paradeta"], "푸에스토시요 해산물 요리"))

    def test_empty_candidate_is_ignored(self):
        self.assertFalse(identity_match.names_match(["한글만"], "La Paradeta"))
        self.assertFalse(identity_match.names_match([""], "La Paradeta"))
        self.assertFalse(identity_match.names_match([], "La Paradeta"))

    def test_accent_and_case_are_folded(self):
        self.assertTrue(
            identity_match.names_match(["Café Comptoir Abel"],
                                       "Cafe Comptoir Abel"))
        self.assertTrue(
            identity_match.names_match(["Bar Cañete"], "Bar Canete"))

    def test_known_renames_match_through_accept_list(self):
        # 상호가 바뀐 곳은 확인된 새 이름을 후보에 넣어야만 통과한다
        self.assertFalse(
            identity_match.names_match(["Boulangerie Pichard"],
                                       "La Maison Pichard"))
        self.assertTrue(
            identity_match.names_match(["Boulangerie Pichard", "La Maison Pichard"],
                                       "La Maison Pichard"))
        self.assertTrue(
            identity_match.names_match(["Pâtisserie Weibel", "Maison Weibel"],
                                       "Maison Weibel"))

    def test_different_business_does_not_match(self):
        self.assertFalse(
            identity_match.names_match(["La Paradeta Sagrada Família"],
                                       "Puertecillo Sagrada Familia"))
        self.assertFalse(
            identity_match.names_match(["Le Grand Pan"], "Le Grand Palais"))

    def test_short_noise_does_not_match(self):
        self.assertFalse(identity_match.names_match(["Ab"], "Absolutely Anything"))


if __name__ == "__main__":
    unittest.main()
