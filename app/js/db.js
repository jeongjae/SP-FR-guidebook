/* DB 스키마와 접근자. 스냅샷은 불변(풀 때 통째 교체), 편집은 events 저널.
 *
 * store snapshot { key, snapshotVersion, data }
 * store events   { id(ULID), deviceId, author, ts, seq, entity{kind,key},
 *                  op, payload, status, rejectReason? }
 * store meta     { k, v }
 */
import { openDb, tx, get, put, getAll, del } from "./idb.js";

let db = null;

export async function ready() {
  if (db) return db;
  db = await openDb("spfr_app", 1, (d) => {
    d.createObjectStore("snapshot", { keyPath: "key" });
    const ev = d.createObjectStore("events", { keyPath: "id" });
    ev.createIndex("by-status", "status");
    ev.createIndex("by-entity", ["entity.kind", "entity.key"]);
    d.createObjectStore("peerEvents", { keyPath: "id" });
    d.createObjectStore("meta", { keyPath: "k" });
  });
  return db;
}

export async function metaGet(k, fallback = null) {
  const d = await ready();
  const row = await tx(d, ["meta"], "readonly", (t) => get(t.objectStore("meta"), k));
  return row ? row.v : fallback;
}

export async function metaSet(k, v) {
  const d = await ready();
  await tx(d, ["meta"], "readwrite", (t) => put(t.objectStore("meta"), { k, v }));
}

export async function snapshotGet(key) {
  const d = await ready();
  const row = await tx(d, ["snapshot"], "readonly",
    (t) => get(t.objectStore("snapshot"), key));
  return row ? row.data : null;
}

export async function snapshotPutMany(entries, snapshotVersion) {
  const d = await ready();
  await tx(d, ["snapshot"], "readwrite", async (t) => {
    const store = t.objectStore("snapshot");
    for (const [key, data] of entries) {
      await put(store, { key, snapshotVersion, data });
    }
  });
}

export async function eventsAll() {
  const d = await ready();
  const rows = await tx(d, ["events"], "readonly",
    (t) => getAll(t.objectStore("events")));
  return rows.sort((a, b) => (a.id < b.id ? -1 : 1));
}

export async function eventsByStatus(status) {
  return (await eventsAll()).filter((e) => e.status === status);
}

export async function eventPut(event) {
  const d = await ready();
  await tx(d, ["events"], "readwrite", (t) => put(t.objectStore("events"), event));
}

export async function eventDelete(id) {
  const d = await ready();
  await tx(d, ["events"], "readwrite", (t) => del(t.objectStore("events"), id));
}
