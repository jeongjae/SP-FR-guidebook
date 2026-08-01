/* 가이드북 내비게이션 — 드로어 · 오늘 버튼 · 검색 · 맨위로 (점진적 향상) */
(function () {
  "use strict";
  var rel = document.body.getAttribute("data-rel") || ".";
  function $(s) { return document.querySelector(s); }

  /* ---------- 드로어 ---------- */
  var drawer = $("#drawer"), overlay = $("#overlay"), menuBtn = $("#menu-btn");
  function openDrawer() {
    drawer.classList.add("open");
    overlay.classList.add("show");
    var inp = $("#search-input");
    if (inp && window.matchMedia("(min-width: 768px)").matches) inp.focus();
  }
  function closeDrawer() {
    drawer.classList.remove("open");
    overlay.classList.remove("show");
  }
  if (menuBtn && drawer && overlay) {
    menuBtn.addEventListener("click", openDrawer);
    overlay.addEventListener("click", closeDrawer);
    var closeBtn = $("#drawer-close");
    if (closeBtn) closeBtn.addEventListener("click", closeDrawer);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeDrawer();
    });
  }

  /* ---------- 오늘 버튼 ---------- */
  function parisToday() {
    try {
      return new Intl.DateTimeFormat("sv-SE", { timeZone: "Europe/Paris" })
        .format(new Date());
    } catch (e) {
      var d = new Date();
      return d.getFullYear() + "-" +
        String(d.getMonth() + 1).padStart(2, "0") + "-" +
        String(d.getDate()).padStart(2, "0");
    }
  }
  function todayUrl() {
    var G = window.GUIDE || {};
    var u = (G.today || {})[parisToday()];
    return rel + "/" + (u || "chapters/03.html");
  }
  var todayLinks = document.querySelectorAll(".nav-today");
  for (var i = 0; i < todayLinks.length; i++) {
    todayLinks[i].addEventListener("click", function (e) {
      e.preventDefault();
      window.location.href = todayUrl();
    });
  }

  /* ---------- 검색 ---------- */
  var inp = $("#search-input"), out = $("#search-results");
  if (inp && out) {
    inp.addEventListener("input", function () {
      var q = inp.value.trim().toLowerCase();
      out.innerHTML = "";
      if (!q) return;
      var idx = (window.GUIDE && window.GUIDE.search) || [];
      var hits = [];
      for (var j = 0; j < idx.length && hits.length < 30; j++) {
        var e = idx[j];
        if ((e.t + " " + e.c).toLowerCase().indexOf(q) !== -1) hits.push(e);
      }
      if (!hits.length) {
        out.innerHTML = '<p class="sr-none">검색 결과가 없습니다</p>';
        return;
      }
      hits.forEach(function (h) {
        var a = document.createElement("a");
        a.href = rel + "/" + h.u;
        var t = document.createElement("span");
        t.className = "sr-t";
        t.textContent = h.t;
        var c = document.createElement("span");
        c.className = "sr-c";
        c.textContent = h.c;
        a.appendChild(t);
        a.appendChild(c);
        out.appendChild(a);
      });
    });
  }

  /* ---------- 맨 위로 ---------- */
  var btt = $("#back-top");
  if (btt) {
    window.addEventListener("scroll", function () {
      btt.classList.toggle("show", window.scrollY > 600);
    }, { passive: true });
    btt.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------- 하단 탭 활성 표시 ---------- */
  var path = window.location.pathname;
  document.querySelectorAll(".bottomnav a[href]").forEach(function (a) {
    var href = a.getAttribute("href");
    if (href && href !== "#" &&
        path.slice(-href.replace(/^\.\.?\//, "").length) ===
        href.replace(/^\.\.?\//, "")) {
      a.classList.add("active");
    }
  });
})();
