#!/usr/bin/env python3
"""Validate the structured itinerary and its tracker/daily-page projections."""

import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

from itinerary import load_itinerary  # noqa: E402


def main():
    payload = load_itinerary(ROOT)
    trip = payload["trip"]
    stays = payload["stays"]
    errors = []

    expected_by_date = {}
    for stay in stays:
        cursor = date.fromisoformat(stay["checkin"])
        checkout = date.fromisoformat(stay["checkout"])
        while cursor < checkout:
            if cursor.isoformat() in expected_by_date:
                errors.append(f"숙박 날짜 중복: {cursor}")
            expected_by_date[cursor.isoformat()] = stay["base"]
            cursor += timedelta(days=1)

    # 마지막 밤은 숙소가 아니라 기내다 (OZ502, 10/9 CDG → 10/10 인천).
    # 그 박을 거점 숙박으로 세면 파리 체크아웃이 하루 밀린다.
    lodging_nights = trip["nights"] - trip.get("inflightNights", 0)
    expected_dates = {
        (date.fromisoformat(trip["start"]) + timedelta(days=i)).isoformat()
        for i in range(lodging_nights)
    }
    missing = sorted(expected_dates - set(expected_by_date))
    extra = sorted(set(expected_by_date) - expected_dates)
    if missing:
        errors.append("숙박 날짜 누락: " + ", ".join(missing))
    if extra:
        errors.append("숙박 날짜 범위 초과: " + ", ".join(extra))

    tracker = ROOT / "source" / "OPERATIONS" / "TP_Europe_Travel_Master_Tracker_v1.2.xlsx"
    wb = load_workbook(tracker, data_only=True, read_only=True)
    ws = wb["Accommodation"]
    headers = [cell.value for cell in ws[3]]
    rows = [dict(zip(headers, row)) for row in ws.iter_rows(min_row=4, values_only=True)
            if row[0] is not None]
    tracker_by_base = {row["거점"]: row for row in rows}
    for stay in stays:
        row = tracker_by_base.get(stay["base"])
        if not row:
            errors.append(f"트래커 숙소 누락: {stay['base']}")
            continue
        actual = (row["체크인"].date().isoformat(), row["체크아웃"].date().isoformat(), row["박수"])
        expected = (stay["checkin"], stay["checkout"], stay["nights"])
        if actual != expected:
            errors.append(f"트래커 숙박 불일치 {stay['base']}: {actual} != {expected}")

    data_js = ROOT / "site" / "assets" / "data.js"
    if not data_js.exists():
        errors.append("생성 검색 데이터 누락: site/assets/data.js")
    else:
        match = re.fullmatch(
            r"window\.GUIDE\s*=\s*(\{.*\});\s*",
            data_js.read_text(encoding="utf-8"),
            flags=re.DOTALL,
        )
        if not match:
            errors.append("site/assets/data.js JSON 해석 실패")
        else:
            guide = json.loads(match.group(1))
            entries = guide.get("search", [])
            searchable = " ".join(
                f"{entry.get('t', '')} {entry.get('c', '')} {entry.get('u', '')}"
                for entry in entries
            ).casefold()
            for term in (
                "marseille", "vieux-port", "le panier", "mucem", "fort-saint-jean",
                "arles", "arènes d’arles", "théâtre antique", "saint-trophime",
                "fondation vincent van gogh", "la roquette",
            ):
                if term.casefold() not in searchable:
                    errors.append(f"검색 인덱스 누락: {term}")
            for entry in entries:
                url = entry.get("u", "")
                if not url or url.startswith(("http://", "https://", "mailto:")):
                    continue
                target = ROOT / "site" / url.split("#", 1)[0].split("?", 1)[0]
                if not target.exists():
                    errors.append(f"검색 링크 대상 없음: {url}")

            today = guide.get("today", {})
            all_dates = {
                (date.fromisoformat(trip["start"]) + timedelta(days=i)).isoformat()
                for i in range(trip["days"])
            }
            if set(today) != all_dates:
                errors.append(f"오늘 일정 날짜 매핑 {len(today)}개 (기대 {trip['days']}개)")
            if len(set(today.values())) != trip["days"]:
                errors.append("오늘 일정 링크 중복 또는 누락")

    daily_dir = ROOT / "site" / "daily"
    if daily_dir.exists():
        pages = sorted(daily_dir.glob("day-*.html"))
        if len(pages) != trip["days"]:
            errors.append(f"데일리 페이지 {len(pages)}개 (기대 {trip['days']}개)")

    required_page_terms = {
        "daily/day-14.html": ("Marseille", "Vieux-Port", "Mucem", "Fort Saint-Jean"),
        "daily/day-22.html": ("Arles", "Arènes d’Arles", "Saint-Trophime", "La Roquette"),
        "chapters/luberon/index.html": ("3박", "9/13", "9/16"),
        "chapters/paris/index.html": ("15박", "9/24", "10/9"),
    }
    for relative, terms in required_page_terms.items():
        path = ROOT / "site" / relative
        if not path.exists():
            errors.append(f"필수 생성 페이지 누락: {relative}")
            continue
        rendered = path.read_text(encoding="utf-8")
        for term in terms:
            if term not in rendered:
                errors.append(f"필수 생성 콘텐츠 누락: {relative} → {term}")

    forbidden_day_place_links = {
        "daily/day-14.html": ("places/arles.html", "places/cassis.html"),
        "daily/day-22.html": ("places/les-baux-de-provence.html", "places/saint-remy-de-provence.html"),
    }
    for relative, links in forbidden_day_place_links.items():
        rendered = (ROOT / "site" / relative).read_text(encoding="utf-8")
        place_section = rendered.split('class="ic ic-pin"', 1)[-1].split(
            'class="ic ic-note"', 1
        )[0]
        for link in links:
            if link in place_section:
                errors.append(f"선택안이 기본 데일리 장소로 노출됨: {relative} → {link}")

    home = ROOT / "site" / "index.html"
    if home.exists():
        rendered = home.read_text(encoding="utf-8")
        for stay in stays:
            marker = f'data-region="{stay["key"]}"'
            if marker not in rendered:
                errors.append(f"홈 거점 누락: {stay['base']}")
                continue
            card = rendered.split(marker, 1)[1].split("</li>", 1)[0]
            for term in (f'({stay["nights"]}박)',):
                if term not in card:
                    errors.append(f"홈 숙박 요약 불일치: {stay['base']} → {term}")

    if errors:
        print("일정 검증 실패:")
        for error in errors:
            print("  " + error)
        raise SystemExit(1)

    print(f"일정 검증 통과: {trip['days']}일 · {trip['nights']}박 · 날짜 누락 0 · 중복 0 · 거점 연결 {len(stays)-1}건 일치")


if __name__ == "__main__":
    main()
