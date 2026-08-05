/* iPhone 홈 화면 앱 · 전체 오프라인 저장 제어 (점진적 향상) */
(function () {
  "use strict";

  var script = document.currentScript;
  if (!script || !(location.protocol === "https:" || location.hostname === "localhost" ||
      location.hostname === "127.0.0.1")) return;
  if (!("serviceWorker" in navigator)) return;

  var rootUrl = new URL("../", script.src);
  var registration = null;
  var reloading = false;
  var activateRequested = false;
  var panel = document.querySelector("#pwa-panel");

  function $(selector) { return document.querySelector(selector); }
  function formatBytes(value) {
    if (!Number.isFinite(value)) return "—";
    if (value < 1024) return value + " B";
    if (value < 1024 * 1024) return (value / 1024).toFixed(1) + " KiB";
    return (value / (1024 * 1024)).toFixed(1) + " MiB";
  }
  function standalone() {
    return window.matchMedia("(display-mode: standalone)").matches ||
      window.navigator.standalone === true;
  }
  function setText(selector, value) {
    var element = $(selector);
    if (element) element.textContent = value;
  }
  function setBusy(busy) {
    var save = $("#pwa-save"), clear = $("#pwa-clear");
    if (save) save.disabled = busy;
    if (clear) clear.disabled = busy;
    if (panel) panel.classList.toggle("is-busy", busy);
  }
  function worker() {
    return navigator.serviceWorker.controller ||
      (registration && (registration.active || registration.waiting));
  }
  function send(type) {
    var target = worker();
    if (target) target.postMessage({ type: type });
  }
  function showUpdate() {
    var box = $("#pwa-update-box");
    if (box) box.hidden = false;
  }
  async function storageDetail() {
    if (!navigator.storage || !navigator.storage.estimate) return;
    try {
      var estimate = await navigator.storage.estimate();
      var persistent = navigator.storage.persisted ? await navigator.storage.persisted() : false;
      setText("#pwa-storage", "이 출처가 사용 중인 저장 공간 " +
        formatBytes(estimate.usage) + " / 한도 " + formatBytes(estimate.quota) +
        (persistent ? " · 유지 보호됨" : " · iOS가 공간 부족 시 정리할 수 있음"));
    } catch (error) {
      /* 저장소 정보는 보조 정보다. 실패해도 오프라인 기능은 유지한다. */
    }
  }
  async function requestPersistence() {
    if (!navigator.storage || !navigator.storage.persist) return;
    try { await navigator.storage.persist(); } catch (error) { /* best effort */ }
    await storageDetail();
  }

  function renderStatus(data) {
    if (!panel) return;
    var save = $("#pwa-save"), clear = $("#pwa-clear"), progress = $("#pwa-progress");
    panel.dataset.state = data.completed ? "complete" :
      (data.updateRequired ? "update" : "ready");
    if (data.completed) {
      setText("#pwa-status", "오프라인 준비 완료");
      setText("#pwa-detail", (data.saved && data.saved.totalFiles || data.totalFiles || 0) +
        "개 파일 · " + formatBytes(data.saved && data.saved.totalBytes || data.totalBytes));
      setText("#pwa-version", "저장 버전 " + data.version.slice(0, 12) +
        (data.saved && data.saved.savedAt ? " · " + new Date(data.saved.savedAt).toLocaleString("ko-KR") : ""));
      if (save) save.textContent = "최신 버전 다시 확인";
      if (clear) clear.hidden = false;
      if (progress) { progress.value = progress.max = data.saved.totalFiles || 1; }
    } else if (data.updateRequired) {
      setText("#pwa-status", "저장된 이전 버전이 있습니다");
      setText("#pwa-detail", "온라인에서 최신 가이드북으로 업데이트하세요.");
      setText("#pwa-version", "현재 사이트 버전 " + data.version.slice(0, 12));
      if (save) save.textContent = "최신 전체 가이드북 저장";
      if (clear) clear.hidden = false;
    } else {
      setText("#pwa-status", "전체 가이드북을 아직 저장하지 않았습니다");
      setText("#pwa-detail", (data.totalFiles || "—") + "개 파일 · " + formatBytes(data.totalBytes));
      setText("#pwa-version", "사이트 버전 " + data.version.slice(0, 12));
      if (save) save.textContent = "전체 가이드북 저장";
      if (clear) clear.hidden = true;
    }
    setBusy(false);
    storageDetail();
  }

  navigator.serviceWorker.addEventListener("message", function (event) {
    var data = event.data || {};
    var progress = $("#pwa-progress");
    if (data.type === "PWA_STATUS") {
      renderStatus(data);
    } else if (data.type === "PWA_DOWNLOAD_START") {
      if (panel) panel.dataset.state = "downloading";
      setBusy(true);
      setText("#pwa-status", "전체 가이드북 저장 중");
      setText("#pwa-detail", "0 / " + data.totalFiles + "개 파일 · 0 / " + formatBytes(data.totalBytes));
      if (progress) { progress.max = data.totalFiles; progress.value = 0; }
    } else if (data.type === "PWA_DOWNLOAD_PROGRESS") {
      setText("#pwa-detail", data.done + " / " + data.totalFiles + "개 파일 · " +
        formatBytes(data.bytes) + " / " + formatBytes(data.totalBytes));
      if (progress) { progress.max = data.totalFiles; progress.value = data.done; }
    } else if (data.type === "PWA_DOWNLOAD_COMPLETE") {
      setBusy(false);
      requestPersistence().then(function () { send("PWA_GET_STATUS"); });
    } else if (data.type === "PWA_DOWNLOAD_ERROR") {
      if (panel) panel.dataset.state = "error";
      setBusy(false);
      setText("#pwa-status", "저장을 마치지 못했습니다");
      setText("#pwa-detail", data.message + " 연결을 확인한 뒤 다시 누르면 이어서 저장합니다.");
    } else if (data.type === "PWA_CLEARED") {
      setBusy(false);
      setText("#pwa-status", "전체 오프라인 사본을 삭제했습니다");
      setText("#pwa-detail", "핵심 화면 캐시는 앱 실행을 위해 유지됩니다.");
      storageDetail();
    }
  });

  if (panel) {
    panel.hidden = false;
    document.body.classList.toggle("is-standalone", standalone());
    setText("#pwa-install-mode", standalone() ?
      "현재 홈 화면 앱으로 실행 중입니다." :
      "현재 Safari에서 실행 중입니다. 아래 순서로 홈 화면에 추가하세요.");
    var save = $("#pwa-save");
    if (save) save.addEventListener("click", function () {
      if (!navigator.onLine) {
        setText("#pwa-status", "인터넷 연결이 필요합니다");
        setText("#pwa-detail", "Wi-Fi 또는 모바일 데이터를 켠 뒤 다시 시도하세요.");
        return;
      }
      setBusy(true);
      send("PWA_DOWNLOAD_ALL");
    });
    var clear = $("#pwa-clear");
    if (clear) clear.addEventListener("click", function () {
      if (window.confirm("기기에 저장한 전체 가이드북 사본을 삭제할까요?")) {
        setBusy(true);
        send("PWA_CLEAR");
      }
    });
    var update = $("#pwa-activate-update");
    if (update) update.addEventListener("click", function () {
      if (registration && registration.waiting) {
        activateRequested = true;
        registration.waiting.postMessage({ type: "PWA_SKIP_WAITING" });
      } else {
        location.reload();
      }
    });
  }

  navigator.serviceWorker.addEventListener("controllerchange", function () {
    if (activateRequested && !reloading) { reloading = true; location.reload(); }
  });

  navigator.serviceWorker.register(new URL("sw.js", rootUrl), {
    scope: rootUrl.pathname,
    updateViaCache: "none"
  }).then(function (reg) {
    registration = reg;
    if (reg.waiting) showUpdate();
    reg.addEventListener("updatefound", function () {
      var installing = reg.installing;
      if (!installing) return;
      installing.addEventListener("statechange", function () {
        if (installing.state === "installed" && navigator.serviceWorker.controller) showUpdate();
      });
    });
    reg.update().catch(function () { /* 오프라인 업데이트 확인 실패는 정상 */ });
    return navigator.serviceWorker.ready;
  }).then(function () {
    send("PWA_GET_STATUS");
  }).catch(function (error) {
    if (panel) {
      panel.dataset.state = "error";
      setText("#pwa-status", "오프라인 기능을 시작하지 못했습니다");
      setText("#pwa-detail", error.message);
    }
  });
})();
