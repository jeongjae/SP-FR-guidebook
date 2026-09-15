/* 앱 스코프(/app/) 서비스워커.
 *
 * 역할을 좁게 잡는다:
 *   - 앱 셸(HTML·CSS·JS·manifest)을 프리캐시해 오프라인 부팅을 보장한다.
 *   - 데이터 스냅샷은 여기서 캐시하지 않는다 — sync.js 가 manifest 버전을
 *     보고 IndexedDB 에 담는다. 캐시 두 겹은 어긋난다.
 *   - ../assets/ (사진·아이콘)은 cache-first + 오리진 전역 caches.match() —
 *     본 사이트 SW 가 이미 받아 둔 85 MiB 저장분을 재활용한다.
 * 버전 문자열은 main.js 의 APP_VERSION 과 함께 올린다.
 */
const APP_CACHE = "spfr-app-shell-v6";
const SHELL = [
  "./",
  "./index.html",
  "./app.css",
  "./manifest.webmanifest",
  "./js/main.js",
  "./js/router.js",
  "./js/idb.js",
  "./js/db.js",
  "./js/events.js",
  "./js/state.js",
  "./js/sync.js",
  "./js/github.js",
  "./js/editforms.js",
  "./js/md.js",
  "./js/ui.js",
  "./js/views/today.js",
  "./js/views/day.js",
  "./js/views/place.js",
  "./js/views/bookings.js",
  "./js/views/search.js",
  "./js/views/syncview.js",
];
const SCOPE = new URL(self.registration.scope);

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(APP_CACHE).then((cache) => cache.addAll(SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names
      .filter((n) => n.startsWith("spfr-app-shell-") && n !== APP_CACHE)
      .map((n) => caches.delete(n)));
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (url.origin !== SCOPE.origin) return;
  const inScope = url.pathname.startsWith(SCOPE.pathname);
  const isData = url.pathname.includes("/app/data/");

  if (inScope && !isData) {
    // 앱 셸 — cache-first, 백그라운드 갱신.
    event.respondWith((async () => {
      const cache = await caches.open(APP_CACHE);
      const hit = await cache.match(event.request, { ignoreSearch: true });
      const refresh = fetch(event.request).then((res) => {
        if (res && res.ok) cache.put(event.request, res.clone());
        return res;
      }).catch(() => null);
      return hit || (await refresh) || cache.match("./index.html");
    })());
    return;
  }

  if (isData) {
    // 스냅샷 — network-first (sync.js 가 버전을 관리하므로 SW 는 통과 위주),
    // 오프라인이면 전역 캐시라도 시도한다.
    event.respondWith(
      fetch(event.request).catch(() => caches.match(event.request))
    );
    return;
  }

  // 앱 밖 같은 오리진 (../assets/ 사진 등) — cache-first, 전역 캐시 조회로
  // 본 사이트 오프라인 저장분을 재활용한다.
  event.respondWith((async () => {
    const global = await caches.match(event.request, { ignoreSearch: true });
    if (global) return global;
    try {
      return await fetch(event.request);
    } catch {
      return Response.error();
    }
  })());
});
