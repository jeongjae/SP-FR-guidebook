import unittest
import sys
import re
import json
from pathlib import Path
from io import StringIO

# Ensure we can import build
sys.path.append(str(Path(__file__).parent))
import build

SOURCE = build.SOURCE
COMMERCIAL_CARDS = build.COMMERCIAL_CARDS
PLACE_DOSSIERS = build.PLACE_DOSSIERS
PLACE_REGISTRY = build.PLACE_REGISTRY
NICE_CHAPTER = SOURCE / "CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md"
SCHEMA_PATH = SOURCE.parent / "build" / "content_schema.json"

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

class TestValidationGuards(unittest.TestCase):
    def setUp(self):
        # Back up files before editing
        self.nice_backup = NICE_CHAPTER.read_text(encoding="utf-8")
        self.dossier_backup = PLACE_DOSSIERS.read_text(encoding="utf-8")
        self.registry_backup = PLACE_REGISTRY.read_text(encoding="utf-8")
        self.schema_backup = SCHEMA_PATH.read_text(encoding="utf-8")

    def tearDown(self):
        # Restore backups
        NICE_CHAPTER.write_text(self.nice_backup, encoding="utf-8")
        PLACE_DOSSIERS.write_text(self.dossier_backup, encoding="utf-8")
        PLACE_REGISTRY.write_text(self.registry_backup, encoding="utf-8")
        SCHEMA_PATH.write_text(self.schema_backup, encoding="utf-8")

    def run_validation(self):
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            build.check_phase9_commercial_depth_guards()
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

    def test_missing_fatigue_value(self):
        # Remove fatigue line from Nice Day 1
        bad_content = self.nice_backup.replace("**피로도 2/5.**", "")
        NICE_CHAPTER.write_text(bad_content, encoding="utf-8")
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            build.build_chapters()
            build.build_daily()
            success = True
        except SystemExit as e:
            success = (e.code == 0)
        finally:
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
        self.assertFalse(success)
        self.assertIn("피로도 커버리지 가드 실패 — 값 없는 날", output)

    def test_missing_confirmed_fact_token(self):
        # Remove confirmed confirmation number from Barcelona chapter
        barcelona_path = SOURCE / "CURRENT/20_Regional_Chapters/04_Barcelona_Sitges_v2.0.md"
        barcelona_backup = barcelona_path.read_text(encoding="utf-8")
        try:
            bad_content = barcelona_backup.replace("36558SG255002", "REMOVED_CODE")
            barcelona_path.write_text(bad_content, encoding="utf-8")

            old_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                build.check_confirmed_fact_token_guards()
                success = True
            except SystemExit as e:
                success = (e.code == 0)
            finally:
                output = sys.stdout.getvalue()
                sys.stdout = old_stdout

            self.assertFalse(success)
            self.assertIn("확정 사실 토큰 생존 가드 실패:", output)
            self.assertIn("토큰 누락: '36558SG255002'", output)
        finally:
            barcelona_path.write_text(barcelona_backup, encoding="utf-8")

if __name__ == "__main__":
    unittest.main()
