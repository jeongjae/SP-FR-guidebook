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
  var mapCards = document.querySelectorAll('.map-card');
  if (mapCards.length) {
    function meta(name) {
      var el = document.querySelector('meta[name="' + name + '"]');
      return el && el.content ? el.content : '';
    }

    var sdkLoading = false;
    var sdkReady = false;
    var cardHandlers = [];

    function ensureSdk(cb) {
      if (window.google && google.maps && google.maps.Map) {
        sdkReady = true;
        cb(true);
        return;
      }
      var key = meta('google-maps-api-key');
      if (!key) { cb(false, '지도 키가 없다.'); return; }
      if (!sdkLoading) {
        sdkLoading = true;
        var s = document.createElement('script');
        s.src = 'https://maps.googleapis.com/maps/api/js?key=' +
          encodeURIComponent(key) + '&language=ko&region=ES';
        s.async = true;
        s.onerror = function () {
          sdkLoading = false;
          cardHandlers.forEach(function (h) { h.fallback('지도를 내려받지 못했다.'); });
        };
        s.onload = function () {
          sdkReady = true;
          sdkLoading = false;
          cardHandlers.forEach(function (h) { if (h.wantMap()) h.tryDraw(); });
        };
        document.head.appendChild(s);
      }
      var deadline = Date.now() + 8000;
      function waitForSdk() {
        if (window.google && google.maps && google.maps.Map) {
          sdkReady = true;
          cb(true);
          return;
        }
        if (Date.now() > deadline) {
          cb(false, '지도를 불러오지 못했다.');
          return;
        }
        setTimeout(waitForSdk, 120);
      }
      waitForSdk();
    }

    Array.prototype.forEach.call(mapCards, function (card) {
      var canvas = card.querySelector('.map-canvas');
      var list = card.querySelector('.map-list');
      var status = card.querySelector('.map-status');
      var mapDataEl = card.querySelector('.map-data-script') || card.querySelector('script[type="application/json"]');
      var toggle = card.querySelector('.map-toggle');
      var mapState = 'idle';   // idle | loading | ready | failed
      var gMap = null;
      var markers = [];

      function say(text) { if (status) status.textContent = text || ''; }

      function show(view) {
        var wantMap = view === 'map';
        if (list) list.hidden = wantMap;
        if (canvas) canvas.hidden = !wantMap;
        if (toggle) {
          Array.prototype.forEach.call(toggle.querySelectorAll('button'), function (b) {
            b.setAttribute('aria-pressed', String((b.dataset.view === 'map') === wantMap));
          });
        }
      }

      function fallback(reason) {
        mapState = 'failed';
        say(reason + ' 목록으로 연다 — 각 항목의 링크로 Google 지도를 열 수 있다.');
        show('list');
      }

      function drawMap() {
        if (!mapDataEl || !canvas) return;
        var data = JSON.parse(mapDataEl.textContent);
        var opts = {
          center: { lat: data.center[0], lng: data.center[1] },
          zoom: data.zoom,
          mapTypeControl: false, streetViewControl: false, fullscreenControl: false
        };
        var mapId = meta('google-maps-map-id');
        if (mapId) opts.mapId = mapId;

        gMap = new google.maps.Map(canvas, opts);
        var bounds = new google.maps.LatLngBounds();
        markers = [];
        data.pins.forEach(function (pin, i) {
          var pos = { lat: pin.lat, lng: pin.lng };
          var marker = new google.maps.Marker({
            map: gMap, position: pos, title: pin.name, label: String(i + 1)
          });
          markers.push(marker);
          bounds.extend(pos);
          marker.addListener('click', function () {
            var row = list && list.querySelector('[data-pin="' + pin.id + '"]');
            if (row) {
              show('list');
              row.scrollIntoView({ block: 'center' });
            }
          });
        });
        if (data.pins.length > 1) gMap.fitBounds(bounds, 40);
        mapState = 'ready';
        say('');
      }

      function tryDraw() {
        try { drawMap(); }
        catch (err) { fallback('지도를 그리지 못했다 (' + err.message + ').'); }
      }

      function loadMap() {
        if (mapState === 'ready') { show('map'); return; }
        if (mapState === 'loading') { show('map'); return; }
        mapState = 'loading';
        say('지도를 불러오는 중');
        show('map');

        ensureSdk(function (ok, err) {
          if (ok) { tryDraw(); }
          else { fallback(err || '지도를 불러오지 못했다.'); }
        });
      }

      cardHandlers.push({
        tryDraw: tryDraw,
        fallback: fallback,
        wantMap: function () { return mapState === 'loading'; }
      });

      if (toggle) {
        toggle.addEventListener('click', function (e) {
          var btn = e.target.closest('button');
          if (!btn) return;
          if (btn.dataset.view === 'map') loadMap(); else show('list');
        });
      }

      // Link list item click to center map if map is active
      if (list) {
        list.addEventListener('click', function (e) {
          var li = e.target.closest('li[data-pin]');
          if (!li || e.target.closest('.map-open') || e.target.closest('a')) return;
          var pinId = li.dataset.pin;
          if (mapState === 'ready' && gMap) {
            show('map');
            if (!mapDataEl) return;
            var data = JSON.parse(mapDataEl.textContent);
            for (var idx = 0; idx < data.pins.length; idx++) {
              if (data.pins[idx].id === pinId) {
                gMap.panTo({ lat: data.pins[idx].lat, lng: data.pins[idx].lng });
                if (markers[idx]) {
                  markers[idx].setAnimation(google.maps.Animation.BOUNCE);
                  setTimeout(function () { if (markers[idx]) markers[idx].setAnimation(null); }, 1400);
                }
                break;
              }
            }
          }
        });
      }

      show('list');   /* 목록이 기본이다 */
    });
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
        var title = mark.querySelector('.tl-title');
        if (what && title) what.innerHTML = title.innerHTML;

        var summary = nextCard.querySelector('.action-summary');
        var markSummary = mark.querySelector('.tl-summary');
        if (markSummary) {
          if (!summary) {
            summary = document.createElement('p');
            summary.className = 'card-dek action-summary';
            nextCard.appendChild(summary);
          }
          summary.textContent = markSummary.textContent;
        } else if (summary) {
          summary.remove();
        }

        /* NOW/NEXT가 바뀌면 행동도 같은 stop의 링크로 교체한다.
           Timeline이 가진 링크를 복제하므로 별도 지도 데이터가 생기지 않는다. */
        var actionRow = nextCard.querySelector('.action-actions');
        var actionTemplate = mark.querySelector('.tl-action-template');
        var markActions = actionTemplate
          ? actionTemplate.content.querySelector('.action-actions') : null;
        if (markActions && markActions.children.length) {
          if (!actionRow) {
            actionRow = document.createElement('div');
            actionRow.className = 'action-actions btn-row';
            nextCard.appendChild(actionRow);
          }
          actionRow.innerHTML = markActions.innerHTML;
        } else if (actionRow) {
          actionRow.remove();
        }
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

      // 1. Set topbar title strictly to currentRegion based on device date
      if (curReg) {
        var tbTitle = document.querySelector('.topbar .tb-title');
        if (tbTitle) {
          if (isPreTrip) {
            tbTitle.textContent = 'NEXT · ' + curReg.name;
          } else if (isPostTrip) {
            tbTitle.textContent = 'Trip Complete · ' + curReg.name;
          } else {
            tbTitle.textContent = curReg.name;
          }
        }
      }

      // 2. Manage selected/active region tab (independent of currentRegion title)
      function selectTab(slug) {
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

      // Initially select currentRegion tab
      if (curReg) {
        selectTab(curReg.slug);
      }

      // When user clicks a region chip, select that tab without changing topbar current-region title
      var tabLinks = document.querySelectorAll('.tabs a[href^="#"]');
      for (var tIdx = 0; tIdx < tabLinks.length; tIdx++) {
        tabLinks[tIdx].addEventListener('click', function () {
          var targetSlug = this.getAttribute('href').replace('#', '');
          selectTab(targetSlug);
        });
      }
    } catch (err) {
      /* fallback gracefully */
    }
  }

  // 오늘 보고 있는 날 탭을 화면 안으로. 43일이 가로로 흐르므로 그냥 두면
  // Paris 후반 날짜는 스트립 밖에서 시작한다 — 현장에서 안 보이는 것과 같다.
  (function centerCurrentTab() {
    try {
      var strip = document.querySelector('nav.tabs');
      if (!strip) return;
      var cur = strip.querySelector('a[aria-current="page"]');
      if (!cur) return;
      if (strip.scrollWidth <= strip.clientWidth) return;
      var want = cur.offsetLeft - (strip.clientWidth - cur.offsetWidth) / 2;
      var max = strip.scrollWidth - strip.clientWidth;
      strip.scrollLeft = Math.max(0, Math.min(want, max));
    } catch (err) {
      /* 스크롤 위치는 부가 기능이다 — 실패해도 링크는 그대로다 */
    }
  })();
})();
