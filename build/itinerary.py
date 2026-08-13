"""Structured stay-plan loader and continuity validation."""

import json
from datetime import date, timedelta
from pathlib import Path


def load_itinerary(root: Path):
    path = root / "source" / "CURRENT" / "10_Core" / "itinerary.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_itinerary(payload)
    return payload


def validate_itinerary(payload):
    problems = []
    trip = payload.get("trip", {})
    stays = payload.get("stays", [])
    try:
        start = date.fromisoformat(trip["start"])
        end = date.fromisoformat(trip["end"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"여행 시작·종료일 형식 오류: {exc}") from exc

    if (end - start).days + 1 != trip.get("days"):
        problems.append("전체 여행 일수 불일치")
    if (end - start).days != trip.get("nights"):
        problems.append("전체 여행 박수 불일치")
    # 마지막 밤은 숙소가 아니라 기내다 — OZ502 는 10/9 저녁 CDG 를 떠나 10/10 인천에
    # 닿는다. 이 한 박을 거점 숙박과 뭉치면 파리 체크아웃 날짜가 하루 밀린다.
    inflight = trip.get("inflightNights", 0)
    if not isinstance(inflight, int) or inflight < 0:
        problems.append("기내박 수 형식 오류")
        inflight = 0
    if not stays:
        problems.append("숙박 거점 누락")

    total_nights = 0
    seen_keys = set()
    for index, stay in enumerate(stays):
        try:
            checkin = date.fromisoformat(stay["checkin"])
            checkout = date.fromisoformat(stay["checkout"])
            nights = stay["nights"]
        except (KeyError, TypeError, ValueError) as exc:
            problems.append(f"숙박 행 형식 오류: {stay!r} ({exc})")
            continue
        if stay.get("key") in seen_keys:
            problems.append(f"숙박 key 중복: {stay.get('key')}")
        seen_keys.add(stay.get("key"))
        actual_nights = (checkout - checkin).days
        if actual_nights != nights:
            problems.append(f"{stay.get('base')}: {nights}박 표기와 날짜 차이 {actual_nights}박 불일치")
        total_nights += nights
        if index and date.fromisoformat(stays[index - 1]["checkout"]) != checkin:
            problems.append(f"{stays[index - 1].get('base')}→{stay.get('base')}: 체크아웃·체크인 불연속")

    if stays:
        if stays[0].get("checkin") != trip.get("start"):
            problems.append("첫 거점 체크인과 여행 시작일 불일치")
        expected_checkout = (end - timedelta(days=inflight)).isoformat()
        if stays[-1].get("checkout") != expected_checkout:
            problems.append("마지막 거점 체크아웃과 여행 종료일 불일치")
    if total_nights + inflight != trip.get("nights"):
        problems.append(f"숙박 합계 {total_nights}박 + 기내 {inflight}박 "
                        f"(기대 {trip.get('nights')}박)")

    if problems:
        raise ValueError("; ".join(problems))
    return payload


def stays_by_key(payload):
    return {stay["key"]: stay for stay in payload["stays"]}
