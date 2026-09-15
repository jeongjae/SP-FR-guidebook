/* IndexedDB 프라미스 래퍼 — 서드파티 의존성 0 원칙의 자작 최소본. */

export function openDb(name, version, upgrade) {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(name, version);
    req.onupgradeneeded = (e) => upgrade(req.result, e.oldVersion);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

function reqp(req) {
  return new Promise((resolve, reject) => {
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export function tx(db, stores, mode, run) {
  return new Promise((resolve, reject) => {
    const t = db.transaction(stores, mode);
    let out;
    t.oncomplete = () => resolve(out);
    t.onerror = () => reject(t.error);
    t.onabort = () => reject(t.error || new Error("tx aborted"));
    Promise.resolve(run(t)).then((v) => { out = v; }).catch((err) => {
      try { t.abort(); } catch { /* already done */ }
      reject(err);
    });
  });
}

export const get = (store, key) => reqp(store.get(key));
export const put = (store, value) => reqp(store.put(value));
export const del = (store, key) => reqp(store.delete(key));
export const getAll = (store, query) => reqp(store.getAll(query));
export const indexAll = (store, index, query) =>
  reqp(store.index(index).getAll(query));
