/* 가이드북 내비게이션 — 드로어 · 오늘 버튼 · 검색 · 맨위로 (점진적 향상) */
(function () {
  "use strict";
  var rel = document.body.getAttribute("data-rel") || ".";
  function $(s) { return document.querySelector(s); }

  /* ---------- 검색 시트 ----------
     전체 메뉴는 없다. 상단 오른쪽 버튼은 검색만 연다. */
  var sheet = $("#search-sheet"), overlay = $("#overlay"),
      searchBtn = $("#search-btn");
  function closeSheet() {
    sheet.classList.remove("open");
    overlay.classList.remove("show");
  }
  if (sheet && overlay && searchBtn) {
    function openSheet(e) {
      if (e) e.preventDefault();
      sheet.classList.add("open");
      overlay.classList.add("show");
      var i = $("#search-input");
      if (i) i.focus();
    }
    searchBtn.addEventListener("click", openSheet);
    var searchLinks = document.querySelectorAll(".nav-search");
    for (var si = 0; si < searchLinks.length; si++) {
      searchLinks[si].addEventListener("click", openSheet);
    }
    overlay.addEventListener("click", closeSheet);
    var closeBtn = $("#sheet-close");
    if (closeBtn) closeBtn.addEventListener("click", closeSheet);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeSheet();
    });
  }

  /* ---------- 큰 제목 접힘 (HIG Large Title) ----------
     홈은 본문 맨 위에 큰 제목이 있다. 같은 글자가 상단바에도 동시에 보이면
     한 화면에 제목이 둘이다. 큰 제목이 위로 사라진 뒤에야 상단바 제목을
     띄운다. JS 가 없으면 클래스가 안 붙어 처음부터 보인다 — 그쪽이 안전하다. */
  var bigTitle = $(".hero h1");
  if (bigTitle) {
    document.body.classList.add("has-large-title");
    var syncTitle = function () {
      document.body.classList.toggle(
        "scrolled-past", bigTitle.getBoundingClientRect().bottom < 52);
    };
    window.addEventListener("scroll", syncTitle, { passive: true });
    syncTitle();
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
    var d = parisToday(), u = (G.today || {})[d];
    /* 출발 전에는 '다음 여행일'인 Day 1, 귀국 뒤에는 43일 목록으로 간다. */
    if (!u && G.tripStart && d < G.tripStart) u = (G.today || {})[G.tripStart];
    return rel + "/" + (u || "daily/index.html");
  }
  /* 홈 히어로의 오늘 날짜 — 여행 기간 밖이면 그 사실을 그대로 보인다 */
  var todayEl = $("#today-date");
  if (todayEl) {
    var G = window.GUIDE || {}, d = parisToday();
    todayEl.textContent = d;
    if (!(G.today || {})[d]) {
      todayEl.textContent = (G.tripStart && d < G.tripStart)
        ? "다음 여행일 · " + G.tripStart
        : d + " · 여행 종료";
      todayEl.classList.add("today-out");
    }
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
      for (var j = 0; j < idx.length; j++) {
        var e = idx[j];
        var title = e.t.toLowerCase(), category = e.c.toLowerCase();
        if ((title + " " + category).indexOf(q) === -1) continue;
        var score = title === q ? 0
          : title.indexOf(q) === 0 ? 1
          : category.indexOf("장소") === 0 ? 2
          : title.indexOf(q) !== -1 ? 3 : 4;
        hits.push({entry: e, score: score, order: j});
      }
      hits.sort(function (a, b) { return a.score - b.score || a.order - b.order; });
      hits = hits.slice(0, 30).map(function (hit) { return hit.entry; });
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

  /* ---------- 오프라인 감지 ----------
     외부로 나가는 링크는 연결이 없으면 눌러도 아무 일이 없다. 눌리는데
     반응이 없는 것보다 눌리지 않는 편이 현장에서 낫다. */
  var netLinks = document.querySelectorAll('a[href^="http://"], a[href^="https://"]');
  for (var k = 0; k < netLinks.length; k++) netLinks[k].classList.add("needs-net");

  function syncOnline() {
    var off = !navigator.onLine;
    document.body.classList.toggle("is-offline", off);
    var notes = document.querySelectorAll(".net-note");
    for (var n = 0; n < notes.length; n++) notes[n].hidden = !off;
  }
  window.addEventListener("online", syncOnline);
  window.addEventListener("offline", syncOnline);
  syncOnline();

  /* 로컬 이미지 실패는 레이아웃을 깨뜨리지 않고 명시적 fallback으로 바꾼다. */
  document.querySelectorAll("[data-media-image]").forEach(function (img) {
    img.addEventListener("error", function () {
      var figure = img.closest(".guidebook-image");
      if (figure) figure.classList.add("is-error");
    });
  });

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

  /* ---------- 하단 탭 활성 표시 ----------
     '오늘' 은 href 가 없고(JS 로 그날 카드를 연다) '지역' 은 지역 챕터
     8개를 대표한다. 경로 접미사 비교만으로는 둘 다 판정되지 않는다. */
  function currentTab() {
    var p = window.location.pathname;
    if (/\/daily\//.test(p)) return "today";
    if (/\/chapters\/itinerary\.html$/.test(p)) return "itinerary";
    if (/\/maps\//.test(p)) return "map";
    // 가이드 축 — 지역 목록·지역 챕터·장소. 분할 여부와 무관하게 하위 전부
    if (/\/regions\.html$/.test(p) || /\/chapters\/[^/]+\/[^/]*$/.test(p)
        || /\/places\//.test(p))
      return "guide";
    if (/\/tracker\//.test(p)) return "prepare";
    return "";
  }
  var tab = currentTab();
  if (tab) {
    var cur = document.querySelector('.bottomnav a[data-tab="' + tab + '"]');
    if (cur) {
      cur.classList.add("active");
      cur.setAttribute("aria-current", "page");
    }
  }
})();

// Phase B 파일럿 — 홈 준비 스트립의 D-day. 기기 시계 기준 점진 향상이며
// JS 없이는 정적 출발일 표기가 그대로 남는다.
(function () {
  var el = document.getElementById("plan-dday");
  if (!el || !window.GUIDE || !GUIDE.tripStart) return;
  var start = new Date(GUIDE.tripStart + "T00:00:00");
  var days = Math.ceil((start - new Date()) / 86400000);
  if (days > 0) el.textContent = "D-" + days;
  else if (days === 0) el.textContent = "오늘 출발";
})();

// 모든 페이지 뒤로가기 — 사용자 요청(D-10). 브라우저 이력이 있을 때만 보인다.
(function () {
  var b = document.querySelector(".tb-back");
  if (!b) return;
  if (window.history.length > 1) {
    b.hidden = false;
    b.addEventListener("click", function () { window.history.back(); });
  }
})();
