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

export async function loadDay(n) {
  const key = `day-${String(n).padStart(2, "0")}`;
  const day = await snapshotGet(key);
  if (!day) return null;
  const { fieldState, events } = await overlayEvents();
  const view = structuredClone(day);
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
  const body = regionDoc?.places?.[slug] || null;
  const { fieldState, events } = await overlayEvents();
  return { ...entry, body, notes: noteRows(fieldState, events, "place", slug) };
}

export async function loadPlacesIndex() {
  return snapshotGet("places-index");
}

export async function loadFieldState() {
  return (await snapshotGet("field-state")) || { cursors: {}, rejected: [] };
}
