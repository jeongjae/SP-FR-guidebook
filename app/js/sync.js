/* 동기화 — 스냅샷 pull + GitHub 저널 push/reconcile.
 *
 * push:      pending 이벤트를 자기 저널(NDJSON)에 append → status pushed
 * reconcile: CI 의 state.json 을 읽어 커서 이하 → applied,
 *            거부 목록 → rejected(사유 포함)
 * pull:      app/data/manifest.json 버전이 다르면 스냅샷 교체
 * peers:     상대 기기 저널을 미러해 수 초 내 상호 가시성 (PAT 필요) */
import {
  snapshotPutMany, metaGet, metaSet, eventsByStatus, eventPut,
  peerEventsReplace,
} from "./db.js";
import { deviceId } from "./events.js";
import { getToken, pushJournal, fetchState, fetchPeerEvents } from "./github.js";

// import.meta.url = …/app/js/sync.js → ../data/ = …/app/data/
const DATA_BASE = new URL("../data/", import.meta.url);

async function fetchJson(rel) {
  const res = await fetch(new URL(rel, DATA_BASE), { cache: "no-cache" });
  if (!res.ok) throw new Error(`${rel}: HTTP ${res.status}`);
  return res.json();
}

export async function currentVersion() {
  return metaGet("snapshotVersion");
}

export async function pullSnapshot({ force = false } = {}) {
  const manifest = await fetchJson("manifest.json");
  const have = await metaGet("snapshotVersion");
  if (!force && have === manifest.version) {
    return { updated: false, version: manifest.version };
  }
  const entries = [];
  for (const f of manifest.files) {
    const data = await fetchJson(f.path);
    let key = f.path.replace(/\.json$/, "");
    if (key.startsWith("days/")) key = key.slice(5);          // day-NN
    else if (key.startsWith("places/")) key = "places-" + key.slice(7);
    entries.push([key, data]);
  }
  await snapshotPutMany(entries, manifest.version);
  await metaSet("snapshotVersion", manifest.version);
  await metaSet("lastPullAt", new Date().toISOString());
  document.dispatchEvent(new CustomEvent("spfr:snapshot-updated"));
  return { updated: true, version: manifest.version, files: manifest.files.length };
}

export async function ensureSnapshot() {
  const have = await metaGet("snapshotVersion");
  if (have) {
    pullSnapshot().catch(() => {});
    return true;
  }
  try {
    await pullSnapshot({ force: true });
    return true;
  } catch (err) {
    console.warn("snapshot pull failed", err);
    return false;
  }
}

export async function pendingCount() {
  return (await eventsByStatus("pending")).length;
}

export async function exportJournal() {
  const pending = await eventsByStatus("pending");
  return pending.map((e) => JSON.stringify(e)).join("\n");
}

async function reconcileWithState() {
  const state = await fetchState();
  if (!state) return { applied: 0, rejected: 0 };
  const cursors = state.cursors || {};
  const rejectedById = new Map(
    (state.rejected || []).map((r) => [r.id, r.reason || "사유 미기록"]));
  let applied = 0, rejected = 0;
  for (const e of await eventsByStatus("pushed")) {
    if (rejectedById.has(e.id)) {
      await eventPut({ ...e, status: "rejected", rejectReason: rejectedById.get(e.id) });
      rejected += 1;
    } else if ((cursors[e.deviceId] || "") >= e.id) {
      await eventPut({ ...e, status: "applied" });
      applied += 1;
    }
  }
  return { applied, rejected, cursors };
}

/* 전체 동기화 한 사이클. PAT 없으면 push·peers 는 건너뛰고 pull 만 한다. */
export async function fullSync() {
  const out = { pushed: 0, applied: 0, rejected: 0, peers: 0, snapshot: false };
  const token = await getToken();
  const dev = await deviceId();

  if (token) {
    const pending = await eventsByStatus("pending");
    if (pending.length) {
      await pushJournal(dev, pending);
      for (const e of pending) await eventPut({ ...e, status: "pushed" });
      out.pushed = pending.length;
    }
  }

  try {
    const r = await reconcileWithState();
    out.applied = r.applied;
    out.rejected = r.rejected;
    if (token) {
      const peers = await fetchPeerEvents(dev, r.cursors || {});
      await peerEventsReplace(peers);
      out.peers = peers.length;
    }
  } catch (err) {
    console.warn("reconcile 실패", err);
  }

  const pulled = await pullSnapshot().catch(() => ({ updated: false }));
  out.snapshot = pulled.updated;
  document.dispatchEvent(new CustomEvent("spfr:rerender"));
  return out;
}
