#!/usr/bin/env python3
"""현장 편집 저널을 정본에 접는다.

data/field-edits/journal-<deviceId>.ndjson (기기 소유, append-only) 의
이벤트 중 커서(data/field-edits/state.json)를 지난 것을 (ts, deviceId, seq)
전순서로 정렬해 적용한다.

P2 에서 받는 op (비구조 — 가드 표면을 건드리지 않는다):
    note          → data/field-notes.json .notes[]
    set-visited   → data/field-notes.json .visited{stopKey}
    check-action  → data/field-notes.json .checkedActions{stopKey}{label}
    set-booking   → data/booking-overrides.json .overrides{R0xx|stay:<base>}

규칙:
    - 검증 실패 이벤트는 잃지 않는다 — state.json .rejected 에 사유와 함께
      기록하고 커서는 그 너머로 전진한다 (앱이 사유를 보여 준다).
    - 같은 대상 충돌은 정렬 순서의 마지막이 이긴다(LWW). 진 값은
      state.json .overwritten 에 남긴다.
    - 저널 파일 자체는 절대 고쳐 쓰지 않는다.

구조 편집 op(add-stop 등)는 P3 에서 추가한다 — 지금 만나면 거부한다.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELD_DIR = ROOT / "data" / "field-edits"
STATE = FIELD_DIR / "state.json"
NOTES = ROOT / "data" / "field-notes.json"
OVERRIDES = ROOT / "data" / "booking-overrides.json"
DAILY = ROOT / "data" / "daily-cards"

BOOKING_STATUSES = {"확정", "미예약", "재확인", "제외", "예약완료", "미정"}
P2_OPS = {"note", "set-visited", "check-action", "set-booking"}
STOP_KEY_RE = re.compile(r"^day-(\d{2})/([a-z0-9-]+)$")
DAY_KEY_RE = re.compile(r"^day-(\d{2})$")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _dump(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def load_context() -> dict:
    """검증에 쓰는 정본 색인 — 스톱·장소·예약 항목의 실재 여부."""
    stops: dict[str, set[str]] = {}
    for card_path in DAILY.glob("day-*.json"):
        card = _load(card_path)
        key = f"day-{card['day']:02d}"
        stops[key] = {s["id"] for s in card.get("stops", [])}

    place_slugs: set[str] = set()
    registry = ROOT / "source/ASSETS/91_Place_Registry_v1.0.md"
    for m in re.finditer(r"^\|\s*`([a-z0-9-]+)`\s*\|", registry.read_text(encoding="utf-8"), re.M):
        place_slugs.add(m.group(1))

    sys.path.insert(0, str(ROOT / "build"))
    import content_model
    tracker = ROOT / "source/OPERATIONS/TP_Europe_Travel_Master_Tracker_v1.2.xlsx"
    booking_ids = {str(r["ID"]) for r in content_model._rows(tracker, "Reservations")}
    stay_keys = {f'stay:{r["거점"]}' for r in content_model._rows(tracker, "Accommodation")}
    return {"stops": stops, "places": place_slugs,
            "bookings": booking_ids | stay_keys}


def validate_event(e: dict, ctx: dict) -> str | None:
    """None = 통과, 아니면 거부 사유."""
    for field in ("id", "deviceId", "author", "ts", "entity", "op", "payload"):
        if field not in e:
            return f"필드 누락: {field}"
    op, entity = e["op"], e["entity"]
    kind, key = entity.get("kind"), entity.get("key")
    if op not in P2_OPS:
        return f"미지원 op (P3 예정): {op}"

    if kind == "stop":
        m = STOP_KEY_RE.match(key or "")
        if not m:
            return f"stop key 형식 오류: {key}"
        day_key = f"day-{m.group(1)}"
        if day_key not in ctx["stops"]:
            return f"없는 날: {day_key}"
        if m.group(2) not in ctx["stops"][day_key]:
            return f"없는 stop: {key}"
    elif kind == "day":
        if not DAY_KEY_RE.match(key or "") or key not in ctx["stops"]:
            return f"없는 날: {key}"
    elif kind == "place":
        if key not in ctx["places"]:
            return f"명부에 없는 장소: {key}"
    elif kind == "booking":
        if key not in ctx["bookings"]:
            return f"트래커에 없는 예약 항목: {key}"
    else:
        return f"모르는 entity kind: {kind}"

    payload = e["payload"] or {}
    if op == "note":
        if not str(payload.get("text", "")).strip():
            return "빈 메모"
    elif op == "set-visited":
        if kind != "stop" or not isinstance(payload.get("value"), bool):
            return "set-visited 는 stop + bool value"
    elif op == "check-action":
        if kind != "stop" or not payload.get("label") \
                or not isinstance(payload.get("checked"), bool):
            return "check-action 은 stop + label + bool checked"
    elif op == "set-booking":
        if kind != "booking":
            return "set-booking 은 booking entity 에만"
        if payload.get("status") not in BOOKING_STATUSES:
            return f"모르는 예약 상태: {payload.get('status')} (어휘: {sorted(BOOKING_STATUSES)})"
    return None


def load_pending(state: dict) -> list[dict]:
    cursors = state.get("cursors", {})
    seen: set[str] = set()
    events: list[dict] = []
    for journal in sorted(FIELD_DIR.glob("journal-*.ndjson")):
        device = journal.stem.removeprefix("journal-")
        cursor = cursors.get(device, "")
        for line_no, line in enumerate(
                journal.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                print(f"  경고: {journal.name}:{line_no} JSON 아님 — 건너뜀")
                continue
            if e.get("deviceId") != device:
                e["deviceId"] = device  # 저널 파일명이 정본
            if e.get("id", "") <= cursor or e.get("id") in seen:
                continue  # 이미 처리됐거나 재푸시 중복
            seen.add(e["id"])
            events.append(e)
    events.sort(key=lambda e: (e.get("ts", ""), e.get("deviceId", ""),
                               e.get("seq", 0)))
    return events


def apply_events(events: list[dict], ctx: dict, state: dict,
                 notes: dict, overrides: dict) -> dict:
    applied = rejected = 0
    winners: dict[tuple, dict] = {}   # LWW 추적 (op별 대상 → 마지막 이벤트)
    for e in events:
        reason = validate_event(e, ctx)
        if reason:
            state["rejected"].append({
                "id": e.get("id"), "deviceId": e.get("deviceId"),
                "reason": reason, "event": e})
            rejected += 1
            continue
        op, key = e["op"], e["entity"]["key"]
        meta = {"id": e["id"], "author": e["author"], "ts": e["ts"]}
        if op == "note":
            notes["notes"].append({
                **meta, "entity": e["entity"],
                "text": str(e["payload"]["text"]).strip()})
        elif op == "set-visited":
            slot = ("visited", key)
            if slot in winners:
                state["overwritten"].append(
                    {"loser": winners[slot]["id"], "winner": e["id"], "slot": "visited:" + key})
            winners[slot] = e
            notes["visited"][key] = {**meta, "value": e["payload"]["value"]}
        elif op == "check-action":
            label = e["payload"]["label"]
            slot = ("check", key, label)
            if slot in winners:
                state["overwritten"].append(
                    {"loser": winners[slot]["id"], "winner": e["id"], "slot": f"check:{key}:{label[:40]}"})
            winners[slot] = e
            notes["checkedActions"].setdefault(key, {})[label] = {
                **meta, "checked": e["payload"]["checked"]}
        elif op == "set-booking":
            slot = ("booking", key)
            if slot in winners:
                state["overwritten"].append(
                    {"loser": winners[slot]["id"], "winner": e["id"], "slot": "booking:" + key})
            winners[slot] = e
            entry = {**meta, "status": e["payload"]["status"]}
            if e["payload"].get("note"):
                entry["note"] = str(e["payload"]["note"])
            overrides["overrides"][key] = entry
        applied += 1
        cursor = state["cursors"].get(e["deviceId"], "")
        if e["id"] > cursor:
            state["cursors"][e["deviceId"]] = e["id"]
    # 거부 이벤트도 처리 완료다 — 커서를 전진시켜 재처리 루프를 막는다.
    for r in state["rejected"]:
        dev, eid = r.get("deviceId"), r.get("id")
        if dev and eid and eid > state["cursors"].get(dev, ""):
            state["cursors"][dev] = eid
    return {"applied": applied, "rejected": rejected}


def main() -> int:
    check_only = "--check" in sys.argv
    state = _load(STATE)
    notes = _load(NOTES)
    overrides = _load(OVERRIDES)
    events = load_pending(state)
    if not events:
        print("적용할 현장 편집 없음 — 커서 최신")
        return 0
    ctx = load_context()
    stats = apply_events(events, ctx, state, notes, overrides)
    print(f"현장 편집 {len(events)}건 처리 — 적용 {stats['applied']} · "
          f"거부 {stats['rejected']} · 기기 {len(state['cursors'])}")
    for r in state["rejected"][-stats["rejected"]:] if stats["rejected"] else []:
        print(f"  거부 {r['id']}: {r['reason']}")
    if check_only:
        print("(--check — 쓰지 않음)")
        return 0
    _dump(NOTES, notes)
    _dump(OVERRIDES, overrides)
    _dump(STATE, state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
