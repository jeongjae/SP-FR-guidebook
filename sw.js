/* 2026 유럽 여행 가이드북 Service Worker — build.py가 버전을 삽입한다. */
"use strict";

const VERSION = "d6dcaeb8f4e2a288b78ff5187f28fef72c83e8d39868ccdb875721a1614dd322";
const CACHE_PREFIX = "sp-fr-guidebook-";
const CORE_CACHE = CACHE_PREFIX + "core-" + VERSION;
const FULL_CACHE = CACHE_PREFIX + "full-" + VERSION;
const RUNTIME_CACHE = CACHE_PREFIX + "runtime-" + VERSION;
const CORE_PATHS = ["index.html", "offline-fallback.html", "maps/offline.html", "chapters/itinerary.html", "daily/index.html", "regions.html", "tracker/index.html", "assets/style.css", "assets/data.js", "assets/nav.js", "assets/pwa.js", "assets/vendor/nanum/nanum-gothic-latin-400-normal.woff2", "assets/vendor/nanum/nanum-gothic-korean-400-normal.woff2", "assets/vendor/nanum/nanum-gothic-latin-700-normal.woff2", "assets/vendor/nanum/nanum-gothic-korean-700-normal.woff2", "manifest.webmanifest", "assets/pwa/apple-touch-icon.png", "assets/pwa/icon-192.png", "assets/pwa/icon-512.png", "assets/pwa/icon-maskable-512.png"];
const SCOPE = new URL("./", self.registration.scope);
const COMPLETE_URL = new URL("__pwa_complete__", SCOPE).href;
let downloadTask = null;

function scoped(path) {
  return new URL(path, SCOPE).href;
}

function isCacheable(response) {
  return response && response.ok && (response.type === "basic" || response.type === "default");
}

async function putIfCacheable(cache, request, response) {
  if (isCacheable(response)) await cache.put(request, response.clone());
  return response;
}

async function notify(message, source) {
  if (source && source.postMessage) source.postMessage(message);
  const clients = await self.clients.matchAll({ type: "window", includeUncontrolled: true });
  for (const client of clients) {
    if (!source || client.id !== source.id) client.postMessage(message);
  }
}

async function readManifest() {
  const response = await fetch(scoped("offline-files.json"), { cache: "no-store" });
  if (!response.ok) throw new Error("오프라인 파일 목록을 불러오지 못했습니다.");
  const manifest = await response.json();
  if (manifest.version !== VERSION) {
    throw new Error("새 사이트 버전이 감지되었습니다. 페이지를 새로고침한 뒤 다시 시도하세요.");
  }
  return manifest;
}

async function completedCaches() {
  const names = (await caches.keys()).filter(name => name.startsWith(CACHE_PREFIX + "full-"));
  const completed = [];
  for (const name of names) {
    const cache = await caches.open(name);
    const marker = await cache.match(COMPLETE_URL);
    if (marker) {
      try {
        completed.push({ name, detail: await marker.json() });
      } catch (error) {
        completed.push({ name, detail: {} });
      }
    }
  }
  return completed;
}

async function status(source) {
  let manifest = null;
  try {
    manifest = await readManifest();
  } catch (error) {
    /* 오프라인에서는 현재 캐시 표식만으로 상태를 보고한다. */
  }
  const current = await caches.open(FULL_CACHE);
  const marker = await current.match(COMPLETE_URL);
  let detail = null;
  if (marker) {
    try { detail = await marker.json(); } catch (error) { detail = {}; }
  }
  const previous = await completedCaches();
  await notify({
    type: "PWA_STATUS",
    version: VERSION,
    completed: Boolean(marker),
    availableOffline: Boolean(marker) || previous.length > 0,
    saved: detail,
    totalFiles: manifest && manifest.totalFiles,
    totalBytes: manifest && manifest.totalBytes,
    updateRequired: !marker && previous.length > 0
  }, source);
}

async function removeOldFullCaches() {
  const names = await caches.keys();
  await Promise.all(names.map(name => {
    if (name.startsWith(CACHE_PREFIX + "full-") && name !== FULL_CACHE) {
      return caches.delete(name);
    }
    return Promise.resolve(false);
  }));
}

async function downloadAll(source) {
  const manifest = await readManifest();
  const cache = await caches.open(FULL_CACHE);
  let done = 0;
  let bytes = 0;
  const total = manifest.files.length;
  await notify({ type: "PWA_DOWNLOAD_START", version: VERSION,
    totalFiles: total, totalBytes: manifest.totalBytes }, source);

  for (const item of manifest.files) {
    const url = scoped(item.path);
    const cached = await cache.match(url);
    if (!cached) {
      const response = await fetch(url, { cache: "no-store" });
      if (!isCacheable(response)) throw new Error(item.path + " 저장에 실패했습니다.");
      await cache.put(url, response);
    }
    done += 1;
    bytes += item.size;
    if (done === total || done % 4 === 0) {
      await notify({ type: "PWA_DOWNLOAD_PROGRESS", version: VERSION,
        done, totalFiles: total, bytes, totalBytes: manifest.totalBytes }, source);
    }
  }

  const detail = {
    version: VERSION,
    savedAt: new Date().toISOString(),
    totalFiles: total,
    totalBytes: manifest.totalBytes
  };
  await cache.put(COMPLETE_URL, new Response(JSON.stringify(detail), {
    headers: { "Content-Type": "application/json" }
  }));
  await removeOldFullCaches();
  await notify({ type: "PWA_DOWNLOAD_COMPLETE", ...detail }, source);
}

async function clearOffline(source) {
  const names = await caches.keys();
  await Promise.all(names.map(name => {
    if (name.startsWith(CACHE_PREFIX + "full-") || name.startsWith(CACHE_PREFIX + "runtime-")) {
      return caches.delete(name);
    }
    return Promise.resolve(false);
  }));
  await notify({ type: "PWA_CLEARED", version: VERSION }, source);
  await status(source);
}

self.addEventListener("install", event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CORE_CACHE);
    for (const path of CORE_PATHS) {
      const response = await fetch(scoped(path), { cache: "reload" });
      if (!isCacheable(response)) throw new Error("핵심 파일 저장 실패: " + path);
      await cache.put(scoped(path), response);
    }
  })());
});

self.addEventListener("activate", event => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names.map(name => {
      const oldCore = name.startsWith(CACHE_PREFIX + "core-") && name !== CORE_CACHE;
      const oldRuntime = name.startsWith(CACHE_PREFIX + "runtime-") && name !== RUNTIME_CACHE;
      return oldCore || oldRuntime ? caches.delete(name) : Promise.resolve(false);
    }));
    await self.clients.claim();
  })());
});

async function networkFirst(request, event) {
  const runtime = await caches.open(RUNTIME_CACHE);
  const network = fetch(request).then(response => putIfCacheable(runtime, request, response));
  let timeoutId;
  try {
    return await Promise.race([
      network,
      new Promise((resolve, reject) => {
        timeoutId = setTimeout(() => reject(new Error("network timeout")), 3000);
      })
    ]);
  } catch (error) {
    if (event) event.waitUntil(network.catch(() => undefined));
    const cached = await preferredMatch(request);
    if (cached) return cached;
    if (new URL(request.url).pathname === SCOPE.pathname) {
      const home = await caches.match(scoped("index.html"));
      if (home) return home;
    }
    const fallback = await caches.match(scoped("offline-fallback.html"));
    if (fallback) return fallback;
    throw error;
  } finally {
    if (timeoutId) clearTimeout(timeoutId);
  }
}

async function preferredMatch(request) {
  for (const name of [CORE_CACHE, FULL_CACHE, RUNTIME_CACHE]) {
    const cache = await caches.open(name);
    const response = await cache.match(request, { ignoreSearch: true });
    if (response) return response;
  }
  return caches.match(request, { ignoreSearch: true });
}

async function fetchIntoRuntime(request) {
  const response = await fetch(request);
  const runtime = await caches.open(RUNTIME_CACHE);
  return putIfCacheable(runtime, request, response);
}

async function cacheFirst(request, event) {
  const cached = await preferredMatch(request);
  if (cached) {
    event.waitUntil(fetchIntoRuntime(request).catch(() => undefined));
    return cached;
  }
  return fetchIntoRuntime(request);
}

self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin !== SCOPE.origin || !url.pathname.startsWith(SCOPE.pathname)) return;

  const relative = url.pathname.slice(SCOPE.pathname.length);
  if (request.mode === "navigate" || relative.endsWith(".html") || relative === "") {
    event.respondWith(networkFirst(request, event));
  } else if (relative === "manifest.webmanifest" || relative === "offline-files.json") {
    event.respondWith(networkFirst(request, event));
  } else {
    event.respondWith(cacheFirst(request, event));
  }
});

self.addEventListener("message", event => {
  const data = event.data || {};
  if (data.type === "PWA_GET_STATUS") {
    event.waitUntil(status(event.source));
  } else if (data.type === "PWA_DOWNLOAD_ALL") {
    if (!downloadTask) {
      downloadTask = downloadAll(event.source)
        .catch(error => notify({ type: "PWA_DOWNLOAD_ERROR", message: error.message }, event.source))
        .finally(() => { downloadTask = null; });
    }
    event.waitUntil(downloadTask);
  } else if (data.type === "PWA_CLEAR") {
    event.waitUntil(clearOffline(event.source));
  } else if (data.type === "PWA_SKIP_WAITING") {
    self.skipWaiting();
  }
});
