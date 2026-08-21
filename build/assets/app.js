/* 런타임 — 서드파티 의존성 0. 완전 오프라인으로 동작해야 한다.
   스크립트가 뜨지 않아도 페이지는 읽힌다. 여기 있는 것은 전부 '있으면 좋은' 것이다. */
(function () {
  "use strict";

  /* 이 파일은 IIFE 하나다. var 는 함수 스코프라 블록이 달라도 같은 변수가
     된다 — 지도 블록과 홈 블록이 각각 var dataEl 을 선언했더니 나중 것이
     먼저 것을 null 로 덮었고, Day 페이지의 지도가 통째로 열리지 않았다.
     블록마다 이름을 달리 짓는다. */

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

     목록은 항상 남는다. 스크립트도 네트워크도 없이 좌표 링크가 손에 있어야
     한다 — 현장에서 그런 상황이 실제로 있다.

     실패는 반드시 화면에 말한다. 처음 만들 때 전역 콜백(callback=)에 기댔다가
     콜백이 돌지 않는 경우 "지도를 불러오는 중" 에서 영영 멈췄다. 사용자는
     기다리면 되는 줄 알고 기다린다. 그건 목록으로 떨어지는 것보다 나쁘다. */
  var toggle = document.querySelector('.map-toggle');
  if (toggle) {
    var canvas = document.getElementById('map-canvas');
    var list = document.getElementById('map-list');
    var status = document.getElementById('map-status');
    var mapDataEl = document.getElementById('map-data');
    var mapState = 'idle';   // idle | loading | ready | failed

    function meta(name) {
      var el = document.querySelector('meta[name="' + name + '"]');
      return el && el.content ? el.content : '';
    }
    function say(text) { if (status) status.textContent = text || ''; }

    function show(view) {
      var wantMap = view === 'map';
      if (list) list.hidden = wantMap;
      if (canvas) canvas.hidden = !wantMap;
      Array.prototype.forEach.call(toggle.querySelectorAll('button'), function (b) {
        b.setAttribute('aria-pressed', String((b.dataset.view === 'map') === wantMap));
      });
    }

    function fallback(reason) {
      mapState = 'failed';
      say(reason + ' 목록으로 연다 — 각 항목의 링크로 Google 지도를 열 수 있다.');
      show('list');
    }

    function drawMap() {
      var data = JSON.parse(mapDataEl.textContent);
      var opts = {
        center: { lat: data.center[0], lng: data.center[1] },
        zoom: data.zoom,
        mapTypeControl: false, streetViewControl: false, fullscreenControl: false
      };
      var mapId = meta('google-maps-map-id');
      if (mapId) opts.mapId = mapId;

      var map = new google.maps.Map(canvas, opts);
      var bounds = new google.maps.LatLngBounds();
      data.pins.forEach(function (pin, i) {
        var pos = { lat: pin.lat, lng: pin.lng };
        var marker = new google.maps.Marker({
          map: map, position: pos, title: pin.name, label: String(i + 1)
        });
        bounds.extend(pos);
        marker.addListener('click', function () {
          var row = list && list.querySelector('[data-pin="' + pin.id + '"]');
          if (row) { show('list'); row.scrollIntoView({ block: 'center' }); }
        });
      });
      if (data.pins.length > 1) map.fitBounds(bounds, 40);
      mapState = 'ready';
      say('');
    }

    function tryDraw() {
      try { drawMap(); }
      catch (err) { fallback('지도를 그리지 못했다 (' + err.message + ').'); }
    }

    /* SDK 가 준비될 때까지 짧게 기다린다. 전역 콜백에 기대지 않는다 —
       콜백이 안 오면 알 방법이 없다. 여기서는 안 오면 목록으로 떨어진다. */
    function waitForSdk(deadline) {
      if (window.google && google.maps && google.maps.Map) { tryDraw(); return; }
      if (Date.now() > deadline) {
        fallback('지도를 불러오지 못했다.');
        return;
      }
      setTimeout(function () { waitForSdk(deadline); }, 120);
    }

    function loadMap() {
      if (mapState === 'ready') { show('map'); return; }
      if (mapState === 'loading') { show('map'); return; }
      var key = meta('google-maps-api-key');
      if (!key) { fallback('지도 키가 없다.'); return; }

      mapState = 'loading';
      say('지도를 불러오는 중');
      show('map');

      if (window.google && google.maps && google.maps.Map) { tryDraw(); return; }

      var s = document.createElement('script');
      s.src = 'https://maps.googleapis.com/maps/api/js?key=' +
        encodeURIComponent(key) + '&language=ko&region=ES';
      s.async = true;
      s.onerror = function () { fallback('지도를 내려받지 못했다.'); };
      s.onload = function () { waitForSdk(Date.now() + 8000); };
      document.head.appendChild(s);
      /* onload 가 오지 않는 경우까지 덮는다 */
      setTimeout(function () {
        if (mapState === 'loading') waitForSdk(Date.now() + 4000);
      }, 6000);
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
  var tripDataEl = document.getElementById('trip-data');
  if (panel && tripDataEl) {
    var trip = JSON.parse(tripDataEl.textContent);
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
        + '<div class="day-card-head" style="margin-bottom:var(--s2)">'
        + '<span class="day-date">' + h(today.date_label || today.date) + '</span>'
        + '<span class="day-num">DAY ' + today.n + '</span></div>'
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

  /* ---- Schedule 페이지 — 현재 날짜 기준 지역 감지 및 상단바/탭 활성화 ---- */
  var schedDataEl = document.getElementById('schedule-regions-data');
  if (schedDataEl) {
    try {
      var regions = JSON.parse(schedDataEl.textContent);
      var regBySlug = {};
      for (var k = 0; k < regions.length; k++) {
        regBySlug[regions[k].slug] = regions[k];
      }

      var now3 = new Date();
      var iso3 = now3.getFullYear() + '-'
        + String(now3.getMonth() + 1).padStart(2, '0') + '-'
        + String(now3.getDate()).padStart(2, '0');

      var curReg = null;
      var isPreTrip = false;
      var isPostTrip = false;

      for (var rIdx = 0; rIdx < regions.length; rIdx++) {
        if (iso3 >= regions[rIdx].start && iso3 <= regions[rIdx].end) {
          curReg = regions[rIdx];
          break;
        }
      }
      if (!curReg && regions.length > 0) {
        if (iso3 < regions[0].start) {
          curReg = regions[0];
          isPreTrip = true;
        } else if (iso3 > regions[regions.length - 1].end) {
          curReg = regions[regions.length - 1];
          isPostTrip = true;
        }
      }

      function updateActiveTab(slug, titlePrefix) {
        var tbTitle = document.querySelector('.topbar .tb-title');
        var reg = regBySlug[slug];
        if (tbTitle && reg) {
          if (titlePrefix) {
            tbTitle.textContent = titlePrefix + ' · ' + reg.name;
          } else {
            tbTitle.textContent = reg.name;
          }
        }
        var allTabs = document.querySelectorAll('.tabs a[href^="#"]');
        for (var i = 0; i < allTabs.length; i++) {
          allTabs[i].removeAttribute('aria-current');
        }
        var targetTab = document.querySelector('.tabs a[href="#' + slug + '"]');
        if (targetTab) {
          targetTab.setAttribute('aria-current', 'page');
          setTimeout(function () {
            targetTab.scrollIntoView({ inline: 'center', block: 'nearest', behavior: 'smooth' });
          }, 100);
        }
      }

      if (curReg) {
        var prefix = isPreTrip ? 'NEXT' : (isPostTrip ? 'Trip Complete' : '');
        updateActiveTab(curReg.slug, prefix);
      }

      var tabLinks = document.querySelectorAll('.tabs a[href^="#"]');
      for (var tIdx = 0; tIdx < tabLinks.length; tIdx++) {
        tabLinks[tIdx].addEventListener('click', function () {
          var targetSlug = this.getAttribute('href').replace('#', '');
          updateActiveTab(targetSlug, '');
        });
      }
    } catch (err) {
      /* fallback gracefully */
    }
  }
})();
