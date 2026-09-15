#!/usr/bin/env python3
"""현장 편집 저널을 정본에 접는다.

data/field-edits/journal-<deviceId>.ndjson (기기 소유, append-only) 의
이벤트 중 커서(data/field-edits/state.json)를 지난 것을 (ts, deviceId, seq)
전순서로 정렬해 적용한다.

비구조 op (P2):
    note          → data/field-notes.json .notes[]
    set-visited   → data/field-notes.json .visited{stopKey}
    check-action  → data/field-notes.json .checkedActions{stopKey}{label}
    set-booking   → data/booking-overrides.json .overrides{R0xx|stay:<base>}

구조·본문 op (P3):
    set-field     stop 필드 수정         → data/daily-cards/day-NN.json
    set-day-meta  하루 메타 수정          → data/daily-cards/day-NN.json
    add-stop      스톱 추가(fieldEdit 표식)→ data/daily-cards/day-NN.json
    remove-stop   스톱 삭제(관련 leg 제거) → data/daily-cards/day-NN.json
    move-stop     스톱 순서 이동          → data/daily-cards/day-NN.json
    prose-set-section 장소 장문 한 층 교체 → source/CURRENT/30_Places/<slug>.md

규칙:
    - 검증 실패 이벤트는 잃지 않는다 — state.json .rejected 에 사유와 함께
      기록하고 커서는 그 너머로 전진한다 (앱이 사유를 보여 준다).
    - 구조 이벤트는 하나씩 적용하고 그때마다 카드 전체를 정본 스키마
      (data/daily-cards/schema.json)와 구조 검사로 재검증한다. 실패하면
      그 이벤트만 되돌려 거부한다 — 스키마의 상한(스톱 9개 등)도 그대로
      집행된다.
    - 같은 대상 충돌은 정렬 순서의 마지막이 이긴다(LWW). 진 값은
      state.json .overwritten 에 남긴다.
    - 저널 파일 자체는 절대 고쳐 쓰지 않는다.
"""
from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
FIELD_DIR = ROOT / "data" / "field-edits"
STATE = FIELD_DIR / "state.json"
NOTES = ROOT / "data" / "field-notes.json"
OVERRIDES = ROOT / "data" / "booking-overrides.json"
DAILY = ROOT / "data" / "daily-cards"
CARD_SCHEMA = DAILY / "schema.json"
PLACE_DIR = ROOT / "source" / "CURRENT" / "30_Places"

BOOKING_STATUSES = {"확정", "미예약", "재확인", "제외", "예약완료", "미정"}
STOP_CATEGORIES = {"sight", "culture", "food", "cafe", "shopping",
                   "activity", "transport", "hotel"}
STOP_FIELDS = {"start", "end", "name", "summary", "menu", "reservation", "optional"}
DAY_FIELDS = {"title", "startTime", "endTime", "fatigue", "backup"}
PROSE_SECTIONS = {"why_go": "왜 가는가", "deep": "더 깊이", "practical": "실용"}
SIMPLE_OPS = {"note", "set-visited", "check-action", "set-booking"}
STRUCTURAL_OPS = {"set-field", "set-day-meta", "add-stop", "remove-stop", "move-stop"}
PROSE_OPS = {"prose-set-section"}
STOP_KEY_RE = re.compile(r"^day-(\d{2})/([a-z0-9-]+)$")
DAY_KEY_RE = re.compile(r"^day-(\d{2})$")
TIME_RE = re.compile(r"^\d{2}:\d{2}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLACE_FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _dump(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


# ------------------------------------------------------------------ 컨텍스트

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
            "bookings": booking_ids | stay_keys,
            "card_validator": jsonschema.Draft202012Validator(_load(CARD_SCHEMA))}


# ------------------------------------------------------------------ 검증

def validate_event(e: dict, ctx: dict) -> str | None:
    """None = 통과, 아니면 거부 사유. 구조 op 는 여기서 형태만 보고
    실제 카드 반영 가능 여부는 적용 시점에 스키마로 다시 본다."""
    for field in ("id", "deviceId", "author", "ts", "entity", "op", "payload"):
        if field not in e:
            return f"필드 누락: {field}"
    op, entity = e["op"], e["entity"]
    kind, key = entity.get("kind"), entity.get("key")
    payload = e["payload"] or {}

    if op not in SIMPLE_OPS | STRUCTURAL_OPS | PROSE_OPS:
        return f"모르는 op: {op}"

    if kind == "stop":
        m = STOP_KEY_RE.match(key or "")
        if not m:
            return f"stop key 형식 오류: {key}"
        day_key = f"day-{m.group(1)}"
        if day_key not in ctx["stops"]:
            return f"없는 날: {day_key}"
        if op != "add-stop" and m.group(2) not in ctx["stops"][day_key]:
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
    elif op == "set-field":
        if kind != "stop":
            return "set-field 는 stop entity 에만"
        f = payload.get("field")
        if f not in STOP_FIELDS:
            return f"수정 불가 필드: {f} (허용: {sorted(STOP_FIELDS)})"
        return _validate_stop_field(f, payload.get("value"))
    elif op == "set-day-meta":
        if kind != "day":
            return "set-day-meta 는 day entity 에만"
        f = payload.get("field")
        if f not in DAY_FIELDS:
            return f"수정 불가 필드: {f} (허용: {sorted(DAY_FIELDS)})"
        v = payload.get("value")
        if f in ("startTime", "endTime") and not (isinstance(v, str) and TIME_RE.match(v)):
            return f"{f} 는 HH:MM"
        if f == "fatigue" and str(v) not in {"1", "2", "3", "4", "5"}:
            return "fatigue 는 1~5"
        if f in ("title", "backup") and not str(v or "").strip():
            return f"{f} 는 빈 값 불가"
    elif op == "add-stop":
        if kind != "day":
            return "add-stop 은 day entity 에만"
        stop = payload.get("stop") or {}
        sid = stop.get("id", "")
        if not SLUG_RE.match(sid):
            return f"stop id 형식 오류: {sid}"
        if sid in ctx["stops"].get(key, set()):
            return f"이미 있는 stop id: {sid}"
        if not str(stop.get("name", "")).strip():
            return "스톱 이름이 비었다"
        if stop.get("category") not in STOP_CATEGORIES:
            return f"모르는 category: {stop.get('category')} (어휘: {sorted(STOP_CATEGORIES)})"
        for tf in ("start", "end"):
            tv = stop.get(tf)
            if tv is not None and not (isinstance(tv, str) and TIME_RE.match(tv)):
                return f"{tf} 는 HH:MM 또는 없음"
        after = payload.get("afterStopId")
        if after is not None and after not in ctx["stops"].get(key, set()):
            return f"afterStopId 가 없다: {after}"
    elif op == "remove-stop":
        if kind != "stop":
            return "remove-stop 은 stop entity 에만"
    elif op == "move-stop":
        if kind != "stop":
            return "move-stop 은 stop entity 에만"
        after = (payload or {}).get("afterStopId")
        m = STOP_KEY_RE.match(key)
        if after is not None:
            if after not in ctx["stops"].get(f"day-{m.group(1)}", set()):
                return f"afterStopId 가 없다: {after}"
            if after == m.group(2):
                return "자기 자신 뒤로는 이동 불가"
    elif op == "prose-set-section":
        if kind != "place":
            return "prose-set-section 은 place entity 에만"
        if payload.get("section") not in PROSE_SECTIONS:
            return f"모르는 section: {payload.get('section')} (허용: {sorted(PROSE_SECTIONS)})"
        if not str(payload.get("md", "")).strip():
            return "빈 본문"
        if not (PLACE_DIR / f"{key}.md").is_file():
            return f"장문 파일 없음: 30_Places/{key}.md"
    return None


def _validate_stop_field(field: str, value) -> str | None:
    if field in ("start", "end"):
        if value is not None and not (isinstance(value, str) and TIME_RE.match(value)):
            return f"{field} 는 HH:MM 또는 없음"
    elif field == "name":
        if not str(value or "").strip():
            return "이름은 빈 값 불가"
    elif field == "optional":
        if not isinstance(value, bool):
            return "optional 은 bool"
    elif field in ("summary", "menu", "reservation"):
        if value is not None and not isinstance(value, str):
            return f"{field} 는 문자열 또는 없음"
    return None


# ------------------------------------------------------------------ 카드 변형

def _renumber(card: dict) -> None:
    for i, s in enumerate(card["stops"], 1):
        s["order"] = i


def _card_problems(card: dict, ctx: dict) -> str | None:
    errors = sorted(ctx["card_validator"].iter_errors(card),
                    key=lambda x: x.json_path)
    if errors:
        e = errors[0]
        return f"카드 스키마 위반 — {e.json_path}: {e.message[:100]}"
    ids = [s["id"] for s in card["stops"]]
    if len(ids) != len(set(ids)):
        return "stop id 중복"
    idset = set(ids)
    for l in card.get("legs", []):
        if l["from"] not in idset or l["to"] not in idset:
            return f"leg 가 stop 을 벗어난다: {l['from']}→{l['to']}"
    for s in card["stops"]:
        if s.get("place_ref") and s["place_ref"] not in ctx["places"]:
            return f"없는 place_ref: {s['place_ref']}"
    return None


def apply_structural(e: dict, card: dict, ctx: dict) -> str | None:
    """카드(사본)에 구조 이벤트 하나를 적용한다. 반환 None = 성공."""
    op = e["op"]
    payload = e["payload"] or {}
    stops = card["stops"]

    def find(sid):
        return next((s for s in stops if s["id"] == sid), None)

    if op == "set-field":
        sid = STOP_KEY_RE.match(e["entity"]["key"]).group(2)
        stop = find(sid)
        if stop is None:
            return f"없는 stop: {sid}"
        stop[payload["field"]] = payload["value"]
    elif op == "set-day-meta":
        card[payload["field"]] = (str(payload["value"])
                                  if payload["field"] == "fatigue"
                                  else payload["value"])
    elif op == "add-stop":
        src = payload["stop"]
        new_stop = {
            "id": src["id"], "order": 0,
            "start": src.get("start"), "end": src.get("end"),
            "name": str(src["name"]).strip(),
            "category": src["category"],
            "lat": src.get("lat"), "lng": src.get("lng"),
            "summary": str(src.get("summary") or ""),
            "menu": src.get("menu"), "reservation": src.get("reservation"),
            "optional": bool(src.get("optional")),
            "place_ref": None,
            "fieldEdit": True,
        }
        after = payload.get("afterStopId")
        if after is None:
            stops.append(new_stop)
        else:
            idx = next(i for i, s in enumerate(stops) if s["id"] == after)
            stops.insert(idx + 1, new_stop)
    elif op == "remove-stop":
        sid = STOP_KEY_RE.match(e["entity"]["key"]).group(2)
        if find(sid) is None:
            return f"없는 stop: {sid}"
        card["stops"] = stops = [s for s in stops if s["id"] != sid]
        card["legs"] = [l for l in card.get("legs", [])
                        if l["from"] != sid and l["to"] != sid]
    elif op == "move-stop":
        sid = STOP_KEY_RE.match(e["entity"]["key"]).group(2)
        stop = find(sid)
        if stop is None:
            return f"없는 stop: {sid}"
        stops.remove(stop)
        after = payload.get("afterStopId")
        if after is None:
            stops.insert(0, stop)
        else:
            target = next((i for i, s in enumerate(stops) if s["id"] == after), None)
            if target is None:
                return f"afterStopId 가 없다: {after}"
            stops.insert(target + 1, stop)
    _renumber(card)
    return _card_problems(card, ctx)


# ------------------------------------------------------------------ 장문 변형

def apply_prose(e: dict) -> str | None:
    """30_Places/<slug>.md 의 한 층을 교체한다. model.load_place_bodies 와
    같은 규칙으로 가르고, 정본 층 순서(왜/더 깊이/실용)로 다시 쓴다."""
    slug = e["entity"]["key"]
    path = PLACE_DIR / f"{slug}.md"
    text = path.read_text(encoding="utf-8")
    fm = PLACE_FM.match(text)
    front = fm.group(0) if fm else ""
    body = text[fm.end():] if fm else text

    # 첫 층 제목 앞의 앞머리(현장 실행 카드 등)는 제자리에 보존한다 —
    # model.load_place_bodies 는 이를 '더 깊이'로 읽지만 파일 배치는
    # 원래 순서가 정본이다.
    layers = {"preamble": [], "why_go": [], "deep": [], "practical": []}
    current = "preamble"
    for line in body.strip().splitlines():
        head = re.match(r"^##\s+(왜 가는가|더 깊이|실용)\s*$", line)
        if head:
            current = {"왜 가는가": "why_go", "더 깊이": "deep",
                       "실용": "practical"}[head.group(1)]
            continue
        layers[current].append(line)

    section = e["payload"]["section"]
    layers[section] = str(e["payload"]["md"]).strip().splitlines()

    parts = [front.rstrip("\n")] if front else []
    preamble = "\n".join(layers["preamble"]).strip()
    if preamble:
        parts.append(preamble)
    for key_name, title in (("why_go", "왜 가는가"), ("deep", "더 깊이"),
                            ("practical", "실용")):
        content = "\n".join(layers[key_name]).strip()
        if content:
            parts.append(f"## {title}\n\n{content}")
    path.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    return None


# ------------------------------------------------------------------ 저널 처리

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
                 notes: dict, overrides: dict,
                 cards: dict[str, dict]) -> dict:
    """cards: day-key → 카드 dict (변형 대상, 호출자가 로드/저장).
    장문(prose) 이벤트는 파일을 바로 쓰지 않고 반환값에 모은다 —
    --check 모드가 정본을 건드리지 않게 하기 위해서다."""
    applied = rejected = 0
    prose_events: list[dict] = []
    winners: dict[tuple, dict] = {}   # LWW 추적 (op별 대상 → 마지막 이벤트)

    def reject(e, reason):
        nonlocal rejected
        state["rejected"].append({
            "id": e.get("id"), "deviceId": e.get("deviceId"),
            "reason": reason, "event": e})
        rejected += 1

    def day_key_of(e):
        kind, key = e["entity"]["kind"], e["entity"]["key"]
        if kind == "day":
            return key
        m = STOP_KEY_RE.match(key or "")
        return f"day-{m.group(1)}" if m else None

    for e in events:
        reason = validate_event(e, ctx)
        if reason:
            reject(e, reason)
        else:
            op, key = e["op"], e["entity"]["key"]
            meta = {"id": e["id"], "author": e["author"], "ts": e["ts"]}
            if op == "note":
                notes["notes"].append({
                    **meta, "entity": e["entity"],
                    "text": str(e["payload"]["text"]).strip()})
                applied += 1
            elif op == "set-visited":
                slot = ("visited", key)
                if slot in winners:
                    state["overwritten"].append(
                        {"loser": winners[slot]["id"], "winner": e["id"],
                         "slot": "visited:" + key})
                winners[slot] = e
                notes["visited"][key] = {**meta, "value": e["payload"]["value"]}
                applied += 1
            elif op == "check-action":
                label = e["payload"]["label"]
                slot = ("check", key, label)
                if slot in winners:
                    state["overwritten"].append(
                        {"loser": winners[slot]["id"], "winner": e["id"],
                         "slot": f"check:{key}:{label[:40]}"})
                winners[slot] = e
                notes["checkedActions"].setdefault(key, {})[label] = {
                    **meta, "checked": e["payload"]["checked"]}
                applied += 1
            elif op == "set-booking":
                slot = ("booking", key)
                if slot in winners:
                    state["overwritten"].append(
                        {"loser": winners[slot]["id"], "winner": e["id"],
                         "slot": "booking:" + key})
                winners[slot] = e
                entry = {**meta, "status": e["payload"]["status"]}
                if e["payload"].get("note"):
                    entry["note"] = str(e["payload"]["note"])
                overrides["overrides"][key] = entry
                applied += 1
            elif op in STRUCTURAL_OPS:
                dk = day_key_of(e)
                card = cards[dk]
                trial = copy.deepcopy(card)
                fail = apply_structural(e, trial, ctx)
                if fail:
                    reject(e, fail)
                else:
                    cards[dk] = trial
                    # 다음 이벤트 검증이 추가/삭제를 보도록 색인 갱신
                    ctx["stops"][dk] = {s["id"] for s in trial["stops"]}
                    applied += 1
            elif op in PROSE_OPS:
                prose_events.append(e)
                applied += 1

        cursor = state["cursors"].get(e["deviceId"], "")
        if e["id"] > cursor:
            state["cursors"][e["deviceId"]] = e["id"]
    return {"applied": applied, "rejected": rejected,
            "proseEvents": prose_events}


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
    cards = {p.stem: _load(p) for p in DAILY.glob("day-*.json")}
    before = {k: json.dumps(v, ensure_ascii=False, sort_keys=True)
              for k, v in cards.items()}
    n_rejected_before = len(state["rejected"])
    stats = apply_events(events, ctx, state, notes, overrides, cards)
    print(f"현장 편집 {len(events)}건 처리 — 적용 {stats['applied']} · "
          f"거부 {stats['rejected']} · 기기 {len(state['cursors'])}")
    for r in state["rejected"][n_rejected_before:]:
        print(f"  거부 {r['id']}: {r['reason']}")
    if check_only:
        print("(--check — 쓰지 않음)")
        return 0
    _dump(NOTES, notes)
    _dump(OVERRIDES, overrides)
    _dump(STATE, state)
    for e in stats["proseEvents"]:
        apply_prose(e)
    if stats["proseEvents"]:
        print(f"장소 장문 {len(stats['proseEvents'])}건 갱신")
    changed_cards = 0
    for k, card in cards.items():
        if json.dumps(card, ensure_ascii=False, sort_keys=True) != before[k]:
            _dump(DAILY / f"{k}.json", card)
            changed_cards += 1
    if changed_cards:
        print(f"일일카드 {changed_cards}개 갱신")
    return 0


if __name__ == "__main__":
    sys.exit(main())
