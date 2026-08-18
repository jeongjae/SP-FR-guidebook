/* 런타임 — 서드파티 의존성 0. 완전 오프라인으로 동작해야 한다.
   스크립트가 뜨지 않아도 페이지는 읽힌다. 여기 있는 것은 전부 '있으면 좋은' 것이다. */
(function () {
  "use strict";

  var rel = document.querySelector('link[rel=stylesheet]').getAttribute('href')
              .replace(/assets\/style\.css$/, '').replace(/\/$/, '') || '.';

  /* ---- 뒤로가기 — 이력이 있을 때만 보인다 ---- */
  var back = document.querySelector('.tb-back');
  if (back && history.length > 1) {
    back.hidden = false;
    back.addEventListener('click', function () { history.back(); });
  }

  /* ---- 검색 시트 ---- */
  var sheet = document.getElementById('search-sheet');
  var input = document.getElementById('search-input');
  var results = document.getElementById('search-results');
  var openBtn = document.getElementById('search-btn');
  var closeBtn = document.getElementById('search-close');
  var lastFocus = null;

  function openSearch(e) {
    if (e) e.preventDefault();
    lastFocus = document.activeElement;
    sheet.hidden = false;
    openBtn.setAttribute('aria-expanded', 'true');
    input.focus();
  }
  function closeSearch() {
    sheet.hidden = true;
    openBtn.setAttribute('aria-expanded', 'false');
    if (lastFocus) lastFocus.focus();
  }
  if (openBtn) openBtn.addEventListener('click', openSearch);
  if (closeBtn) closeBtn.addEventListener('click', closeSearch);
  var quick = document.getElementById('quick-search');
  if (quick) quick.addEventListener('click', openSearch);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && sheet && !sheet.hidden) closeSearch();
  });

  var KIND = { place: '장소', day: '일정', region: '지역' };
  if (input) input.addEventListener('input', function () {
    var q = input.value.trim().toLowerCase();
    if (!q || !window.SEARCH_INDEX) { results.innerHTML = ''; return; }
    var hits = window.SEARCH_INDEX.filter(function (r) {
      return (r.t + ' ' + (r.x || '')).toLowerCase().indexOf(q) >= 0;
    }).slice(0, 30);
    results.innerHTML = hits.length
      ? hits.map(function (r) {
          return '<a class="search-result" href="' + rel + '/' + r.u + '">'
            + '<span class="sr-title">' + r.t + '</span>'
            + '<span class="sr-path">' + (KIND[r.k] || r.k)
            + (r.x ? ' · ' + r.x : '') + '</span></a>';
        }).join('')
      : '<p class="meta">찾는 것이 없다.</p>';
  });

  /* ---- 지도 / 목록 전환 ----
     지도는 눌렀을 때만 불러온다. 43일 내내 열리는 화면마다 지도 SDK 를
     받으면 데이터가 약한 곳에서 첫 화면이 늦는다.
     목록은 항상 남는다 — 스크립트나 네트워크가 없어도 좌표 링크는 손에
     있어야 한다. */
  var toggle = document.querySelector('.map-toggle');
  if (toggle) {
    var canvas = document.getElementById('map-canvas');
    var list = document.getElementById('map-list');
    var status = document.getElementById('map-status');
    var dataEl = document.getElementById('map-data');
    var mapReady = false, mapLoading = false;

    function meta(name) {
      var el = document.querySelector('meta[name="' + name + '"]');
      return el ? el.content : '';
    }
    var apiKey = meta('google-maps-api-key');

    function show(view) {
      var wantMap = view === 'map';
      list.hidden = wantMap;
      canvas.hidden = !wantMap;
      Array.prototype.forEach.call(toggle.querySelectorAll('button'), function (b) {
        b.setAttribute('aria-pressed', String((b.dataset.view === 'map') === wantMap));
      });
    }

    function drawMap() {
      if (mapReady || !dataEl) return;
      var data = JSON.parse(dataEl.textContent);
      var map = new google.maps.Map(canvas, {
        center: { lat: data.center[0], lng: data.center[1] },
        zoom: data.zoom,
        mapId: meta('google-maps-map-id') || undefined,
        mapTypeControl: false, streetViewControl: false, fullscreenControl: false
      });
      var bounds = new google.maps.LatLngBounds();
      data.pins.forEach(function (pin, i) {
        var marker = new google.maps.Marker({
          map: map, position: { lat: pin.lat, lng: pin.lng },
          title: pin.name, label: String(i + 1)
        });
        bounds.extend(marker.getPosition());
        marker.addListener('click', function () {
          var row = list.querySelector('[data-pin="' + pin.id + '"]');
          if (row) { show('list'); row.scrollIntoView({ block: 'center' }); }
        });
      });
      if (data.pins.length > 1) map.fitBounds(bounds, 40);
      mapReady = true;
      if (status) status.textContent = '';
    }

    function loadMap() {
      if (mapReady) { show('map'); return; }
      if (!apiKey) {
        if (status) status.textContent =
          '지도 키가 없어 목록으로 연다. 각 항목의 링크로 Google 지도를 열 수 있다.';
        show('list');
        return;
      }
      if (mapLoading) return;
      mapLoading = true;
      if (status) status.textContent = '지도를 불러오는 중';
      show('map');
      var s = document.createElement('script');
      s.src = 'https://maps.googleapis.com/maps/api/js?key=' +
        encodeURIComponent(apiKey) + '&loading=async&callback=__mapReady';
      s.async = true;
      window.__mapReady = function () { drawMap(); };
      s.onerror = function () {
        mapLoading = false;
        if (status) status.textContent = '지도를 불러오지 못했다. 목록을 쓴다.';
        show('list');
      };
      document.head.appendChild(s);
    }

    toggle.addEventListener('click', function (e) {
      var btn = e.target.closest('button');
      if (!btn) return;
      if (btn.dataset.view === 'map') loadMap(); else show('list');
    });
    show('list');   /* 목록이 기본이다 */
  }

  /* ---- Day 타임라인 — 지금 항목 강조 ----
     오늘이 아닌 날에는 아무것도 하지 않는다. 어제 날짜에 '지금' 이 뜨면
     현장에서 잘못 읽는다. */
  var nextCard = document.getElementById('next-action');
  if (nextCard) {
    var dayISO = nextCard.dataset.day;
    var now = new Date();
    var todayISO = now.getFullYear() + '-'
      + String(now.getMonth() + 1).padStart(2, '0') + '-'
      + String(now.getDate()).padStart(2, '0');
    if (dayISO === todayISO) {
      var mins = now.getHours() * 60 + now.getMinutes();
      var items = document.querySelectorAll('.tl-item[data-start]');
      var current = null, upcoming = null;
      Array.prototype.forEach.call(items, function (li) {
        var s = li.dataset.start, e = li.dataset.end;
        if (!s) return;
        var sm = parseInt(s.slice(0, 2), 10) * 60 + parseInt(s.slice(3, 5), 10);
        var em = e ? parseInt(e.slice(0, 2), 10) * 60 + parseInt(e.slice(3, 5), 10) : sm;
        if (mins >= sm && mins <= em) current = li;
        if (!upcoming && sm > mins) upcoming = li;
      });
      var mark = current || upcoming;
      if (mark) {
        mark.classList.add('tl-item-now');
        var label = nextCard.querySelector('.label');
        if (label) label.textContent = current ? 'NOW' : 'NEXT';
        var when = nextCard.querySelector('.action-when');
        var what = nextCard.querySelector('.action-what');
        if (when) when.textContent = mark.dataset.start;
        if (what) what.innerHTML = mark.querySelector('.tl-name').innerHTML;
      }
    }
  }

  /* ---- 홈 — 여행 전/중 모드 ----
     빌드 시각에 모드를 굳히지 않는다. 출발 전에 만든 페이지가 여행 중에도
     맞아야 하기 때문이다. */
  var panel = document.getElementById('today-panel');
  var dataEl = document.getElementById('trip-data');
  if (panel && dataEl) {
    var trip = JSON.parse(dataEl.textContent);
    var now2 = new Date();
    var iso = now2.getFullYear() + '-'
      + String(now2.getMonth() + 1).padStart(2, '0') + '-'
      + String(now2.getDate()).padStart(2, '0');
    var today = trip.days.filter(function (d) { return d.date === iso; })[0];

    function h(s) { return s.replace(/[&<>"]/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); }

    if (today) {
      var nx = today.next[0];
      panel.innerHTML =
        '<section class="action-card">'
        + '<span class="label">TODAY · DAY ' + today.n + '</span>'
        + '<div class="action-when" style="font-size:var(--t-h2)">' + h(today.city) + '</div>'
        + '<p class="card-dek">' + h(today.title) + '</p>'
        + (nx ? '<div style="margin-top:1rem"><span class="label">NEXT</span>'
                + '<div class="action-what">' + h(nx.t) + ' ' + h(nx.n) + '</div></div>' : '')
        + '<div class="btn-row" style="margin-top:1rem">'
        + '<a class="btn btn-primary" href="' + today.url + '">오늘 일정</a>'
        + '<a class="btn btn-secondary" href="map/index.html">지도</a>'
        + '</div></section>';
    } else if (iso < trip.start) {
      var d1 = new Date(trip.start + 'T00:00:00');
      var left = Math.ceil((d1 - now2) / 86400000);
      panel.innerHTML =
        '<section class="action-card">'
        + '<span class="label">TRIP STARTS IN</span>'
        + '<div class="action-when">D-' + left + '</div>'
        + '<div class="action-what">' + trip.start + ' 출발</div>'
        + '<div class="btn-row" style="margin-top:1rem">'
        + '<a class="btn btn-primary" href="prepare/index.html">준비 확인</a>'
        + '<a class="btn btn-secondary" href="schedule.html">전체 일정</a>'
        + '</div></section>';
    } else {
      panel.innerHTML =
        '<section class="action-card"><span class="label">여행 종료</span>'
        + '<div class="action-what">43일이 끝났다.</div>'
        + '<div class="btn-row" style="margin-top:1rem">'
        + '<a class="btn btn-secondary" href="schedule.html">전체 일정 다시 보기</a>'
        + '</div></section>';
    }
  }
})();
