/* 스냅샷 pull. (GitHub push 는 P2 — 지금은 수동 내보내기가 sync 화면에 있다.)
 *
 * app/data/manifest.json 의 version 을 IndexedDB 에 저장된 버전과 비교해
 * 다르면 파일들을 받아 snapshot store 를 통째로 교체한다. */
import { snapshotPutMany, metaGet, metaSet, eventsByStatus } from "./db.js";

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
    // 백그라운드 갱신 — 실패해도 로컬 스냅샷으로 계속 간다.
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
