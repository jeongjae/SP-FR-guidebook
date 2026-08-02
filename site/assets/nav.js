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
    searchBtn.addEventListener("click", function () {
      sheet.classList.add("open");
      overlay.classList.add("show");
      var i = $("#search-input");
      if (i) i.focus();
    });
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
    var u = (G.today || {})[parisToday()];
    return rel + "/" + (u || "chapters/03.html");
  }
  /* 홈 히어로의 오늘 날짜 — 여행 기간 밖이면 그 사실을 그대로 보인다 */
  var todayEl = $("#today-date");
  if (todayEl) {
    var G = window.GUIDE || {}, d = parisToday();
    todayEl.textContent = d;
    if (!(G.today || {})[d]) {
      todayEl.textContent = d + " · 여행 기간 밖";
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
  window.addEventListener("online", function () { syncOnline(); loadPlacePhotos(); });
  window.addEventListener("offline", syncOnline);
  syncOnline();

  /* ---------- 주요 방문지 사진 (Wikipedia, 점진적 향상) ----------
     지역 대표사진은 로컬 자산이라 오프라인에서도 보인다. 여기서 불러오는
     것은 방문지별 사진이고, 이건 추가 향상이다. 없으면 카드가 글로만 남는다.
     지역 사진을 방문지 사진 자리에 대신 넣지 않는다 — Sagrada Família 사진이
     Sitges 카드에 붙는 식의 거짓 표시가 된다. */
  var wikiDone = {};
  function loadPlacePhotos() {
    if (!navigator.onLine || typeof fetch !== "function") return;
    var cards = document.querySelectorAll(".pl-card[data-wiki]");
    cards.forEach(function (card) {
      var title = card.getAttribute("data-wiki");
      if (!title || wikiDone[title]) return;
      wikiDone[title] = true;
      var lang = card.getAttribute("data-wlang") || "en";
      var url = "https://" + lang + ".wikipedia.org/api/rest_v1/page/summary/" +
        encodeURIComponent(title.replace(/ /g, "_"));
      fetch(url).then(function (r) { return r.ok ? r.json() : null; })
        .then(function (data) {
          if (!data || !data.thumbnail || !data.thumbnail.source) return;
          var box = card.querySelector(".pl-photo");
          var img = box.querySelector("img");
          img.src = data.thumbnail.source;
          img.onload = function () { box.hidden = false; };
          var credit = box.querySelector(".pl-credit");
          if (credit && data.content_urls && data.content_urls.desktop) {
            credit.href = data.content_urls.desktop.page;
          }
        }).catch(function () {
          wikiDone[title] = false;   // 연결이 돌아오면 다시 시도한다
        });
    });
  }
  loadPlacePhotos();

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
    // 지역 챕터는 지명 디렉터리를 쓴다 — 분할 여부와 무관하게 하위 페이지 전부
    if (/\/regions\.html$/.test(p) || /\/chapters\/[^/]+\/[^/]*$/.test(p))
      return "regions";
    if (/\/topics\//.test(p)) return "topics";
    if (/\/maps\//.test(p)) return "maps";
    if (/\/tracker\//.test(p)) return "tracker";
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
