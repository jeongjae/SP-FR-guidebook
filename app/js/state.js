/* materialize — 스냅샷 ⊕ (적용 전) 이벤트 → 화면 모델.
 *
 * 이중 표시 방지의 축은 기기별 커서다: 스냅샷 field-state 의
 * cursors[deviceId] 이하 이벤트는 이미 정본에 반영돼 있으므로 겹치지
 * 않고, 그보다 새 이벤트(내 것 + 상대 기기 미러)만 겹친다. */
import { snapshotGet, eventsAll, peerEventsAll } from "./db.js";
import { stopKey } from "./events.js";

async function overlayEvents() {
  const fieldState = (await snapshotGet("field-state")) || { cursors: {} };
  const cursors = fieldState.cursors || {};
  const all = [...(await eventsAll()), ...(await peerEventsAll())];
  return {
    fieldState,
    events: all.filter((e) => e.status !== "rejected"
      && (e.id || "") > (cursors[e.deviceId] || "")),
  };
}

function forEntity(events, kind, key) {
  return events.filter((e) => e.entity.kind === kind && e.entity.key === key);
}

function noteRows(fieldState, events, kind, key) {
  const base = (fieldState.notes || [])
    .filter((n) => n.entity?.kind === kind && n.entity?.key === key)
    .map((n) => ({ text: n.text, author: n.author, ts: n.ts, id: n.id, synced: true }));
  const local = forEntity(events, kind, key)
    .filter((e) => e.op === "note")
    .map((e) => ({ text: e.payload.text, author: e.author, ts: e.ts, id: e.id }));
  return [...base, ...local];
}

export async function loadTrip() {
  return snapshotGet("trip");
}

/* 서버(apply_field_edits.py)와 같은 의미의 구조 오버레이 —
 * 아직 정본에 접히지 않은 add/remove/move/set-field 를 화면 모델에 미리
 * 반영한다. 실패는 조용히 건너뛴다(정본 검증이 최종 판정). */
function applyStructuralOverlay(view, key, events) {
  const structural = events
    .filter((e) => ["set-field", "set-day-meta", "add-stop", "remove-stop", "move-stop"].includes(e.op))
    .filter((e) => (e.entity.kind === "day" && e.entity.key === key)
      || (e.entity.kind === "stop" && e.entity.key.startsWith(key + "/")))
    .sort((a, b) => (a.id < b.id ? -1 : 1));
  for (const e of structural) {
    const stops = view.stops;
    const sid = e.entity.kind === "stop" ? e.entity.key.split("/")[1] : null;
    const find = (id) => stops.find((s) => s.id === id);
    try {
      if (e.op === "set-field") {
        const s = find(sid); if (s) { s[e.payload.field] = e.payload.value; s.localEdit = true; }
      } else if (e.op === "set-day-meta") {
        view[e.payload.field] = e.payload.value; view.localEdit = true;
      } else if (e.op === "add-stop") {
        if (find(e.payload.stop.id)) continue;
        const ns = { summary: "", menu: null, reservation: null, optional: false,
          lat: null, lng: null, place_ref: null, ...e.payload.stop,
          fieldEdit: true, localEdit: true };
        const after = e.payload.afterStopId;
        if (after == null) stops.push(ns);
        else {
          const i = stops.findIndex((s) => s.id === after);
          stops.splice(i < 0 ? stops.length : i + 1, 0, ns);
        }
      } else if (e.op === "remove-stop") {
        const i = stops.findIndex((s) => s.id === sid);
        if (i >= 0) stops.splice(i, 1);
        view.legs = (view.legs || []).filter((l) => l.from !== sid && l.to !== sid);
      } else if (e.op === "move-stop") {
        const i = stops.findIndex((s) => s.id === sid);
        if (i < 0) continue;
        const [s] = stops.splice(i, 1);
        const after = e.payload.afterStopId;
        if (after == null) stops.unshift(s);
        else {
          const j = stops.findIndex((x) => x.id === after);
          stops.splice(j < 0 ? stops.length : j + 1, 0, s);
        }
      }
    } catch (err) { console.warn("structural overlay skip", e.id, err); }
  }
  view.stops.forEach((s, i) => { s.order = i + 1; });
}

export async function loadDay(n) {
  const key = `day-${String(n).padStart(2, "0")}`;
  const day = await snapshotGet(key);
  if (!day) return null;
  const { fieldState, events } = await overlayEvents();
  const view = structuredClone(day);
  applyStructuralOverlay(view, key, events);
  view.notes = noteRows(fieldState, events, "day", key);
  for (const stop of view.stops) {
    const sk = stopKey(n, stop.id);
    const evs = forEntity(events, "stop", sk).sort((a, b) => (a.id < b.id ? -1 : 1));
    stop.visited = fieldState.visited?.[sk]?.value || false;
    for (const e of evs.filter((x) => x.op === "set-visited")) {
      stop.visited = e.payload.value;
    }
    const checked = new Map(Object.entries(fieldState.checkedActions?.[sk] || {})
      .map(([label, v]) => [label, v.checked]));
    for (const e of evs.filter((x) => x.op === "check-action")) {
      checked.set(e.payload.label, e.payload.checked);
    }
    stop.checkedActions = checked;
    stop.notes = noteRows(fieldState, events, "stop", sk);
  }
  return view;
}

export async function loadBookings() {
  const data = await snapshotGet("bookings");
  if (!data) return null;
  const { fieldState, events } = await overlayEvents();
  const view = structuredClone(data);
  const overrides = view.overrides || {};
  const apply = (entityKey, row) => {
    const o = overrides[entityKey];
    if (o) { row.syncedStatus = o.status; if (o.note) row.syncedNote = o.note; }
    const evs = forEntity(events, "booking", entityKey)
      .filter((e) => e.op === "set-booking")
      .sort((a, b) => (a.id < b.id ? -1 : 1));
    for (const e of evs) {
      row.localStatus = e.payload.status;
      if (e.payload.note) row.localNote = e.payload.note;
    }
    row.effectiveStatus = row.localStatus || row.syncedStatus || row.status;
    row.notes = noteRows(fieldState, events, "booking", entityKey);
  };
  for (const r of view.reservations) apply(r.id, r);
  for (const a of view.accommodations) apply(`stay:${a.base}`, a);
  return view;
}

export async function loadPlace(slug) {
  const index = await snapshotGet("places-index");
  const entry = (index?.places || []).find((p) => p.slug === slug);
  if (!entry) return null;
  const regionDoc = await snapshotGet(`places-${entry.region}`);
  const body = regionDoc?.places?.[slug]
    ? structuredClone(regionDoc.places[slug]) : null;
  const { fieldState, events } = await overlayEvents();
  if (body) {
    const proseKey = { why_go: "whyGoMd", deep: "bodyMd", practical: "practicalMd" };
    const prose = forEntity(events, "place", slug)
      .filter((e) => e.op === "prose-set-section")
      .sort((a, b) => (a.id < b.id ? -1 : 1));
    for (const e of prose) {
      const k = proseKey[e.payload.section];
      if (k) { body[k] = e.payload.md; body.localEdit = true; }
    }
  }
  return { ...entry, body, notes: noteRows(fieldState, events, "place", slug) };
}

export async function loadPlacesIndex() {
  return snapshotGet("places-index");
}

export async function loadFieldState() {
  return (await snapshotGet("field-state")) || { cursors: {}, rejected: [] };
}
