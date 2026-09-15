/* 부팅: DB 열기 → 스냅샷 확보(온라인이면 갱신) → 라우터 시작 → SW 등록. */
import { ready } from "./db.js";
import { ensureSnapshot, pendingCount } from "./sync.js";
import { startRouter } from "./router.js";

export const APP_VERSION = "p1.0";

async function updateSyncDot() {
  const dot = document.getElementById("sync-dot");
  if (!dot) return;
  const n = await pendingCount();
  dot.className = "sync-dot " + (n > 0 ? "pending" : "clean");
  dot.title = n > 0 ? `대기 중 편집 ${n}건` : "편집 대기 없음";
}

(async () => {
  await ready();
  const ok = await ensureSnapshot();
  if (!ok) {
    document.getElementById("view").innerHTML =
      '<div class="card"><h2>스냅샷 없음</h2><p class="meta">처음 한 번은 온라인에서 열어야 한다. 연결 후 새로고침.</p></div>';
  }
  await startRouter();
  await updateSyncDot();
  document.addEventListener("spfr:event-appended", updateSyncDot);
  document.addEventListener("spfr:rerender", updateSyncDot);

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("./sw.js", { scope: "./" }).catch((err) =>
      console.warn("SW 등록 실패", err));
  }
})();
