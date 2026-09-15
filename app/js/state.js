/* materialize — 스냅샷 ⊕ 이벤트 저널 → 화면 모델.
 * 스냅샷 객체를 변형하지 않는다. 뷰가 쓰는 파생 필드만 덧붙인 사본을 준다. */
import { snapshotGet, eventsAll } from "./db.js";
import { stopKey } from "./events.js";

function overlayFor(events, kind, key) {
  return events.filter((e) => e.entity.kind === kind && e.entity.key === key
    && e.status !== "rejected");
}

export async function loadTrip() {
  return snapshotGet("trip");
}

export async function loadDay(n) {
  const key = `day-${String(n).padStart(2, "0")}`;
  const day = await snapshotGet(key);
  if (!day) return null;
  const events = await eventsAll();
  const view = structuredClone(day);
  view.notes = overlayFor(events, "day", key)
    .filter((e) => e.op === "note")
    .map((e) => ({ text: e.payload.text, author: e.author, ts: e.ts, id: e.id }));
  for (const stop of view.stops) {
    const sk = stopKey(n, stop.id);
    const evs = overlayFor(events, "stop", sk);
    stop.visited = evs.filter((e) => e.op === "set-visited")
      .reduce((acc, e) => e.payload.value, false);
    const checked = new Map();
    for (const e of evs.filter((x) => x.op === "check-action")) {
      checked.set(e.payload.label, e.payload.checked);
    }
    stop.checkedActions = checked;
    stop.notes = evs.filter((e) => e.op === "note")
      .map((e) => ({ text: e.payload.text, author: e.author, ts: e.ts, id: e.id }));
  }
  return view;
}

export async function loadBookings() {
  const data = await snapshotGet("bookings");
  if (!data) return null;
  const events = await eventsAll();
  const view = structuredClone(data);
  const apply = (entityKey, row) => {
    const evs = overlayFor(events, "booking", entityKey);
    for (const e of evs) {
      if (e.op === "set-booking") {
        row.localStatus = e.payload.status;
        if (e.payload.note) row.localNote = e.payload.note;
      }
    }
    row.notes = evs.filter((e) => e.op === "note")
      .map((e) => ({ text: e.payload.text, author: e.author, ts: e.ts, id: e.id }));
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
  const events = await eventsAll();
  const notes = overlayFor(events, "place", slug)
    .filter((e) => e.op === "note")
    .map((e) => ({ text: e.payload.text, author: e.author, ts: e.ts, id: e.id }));
  return { ...entry, body, notes };
}

export async function loadPlacesIndex() {
  return snapshotGet("places-index");
}
