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

  /* ---- 공통 날짜 상태 — 기기의 local calendar date가 유일한 런타임 기준 ---- */
  function htmlEscape(value) {
    return String(value == null ? '' : value).replace(/[&<>"]/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c];
    });
  }

  function localDateOnly() {
    var override = window.__SPFR_TEST_DATE__;
    if (typeof override === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(override)) {
      return override;
    }
    var now = new Date();
    return now.getFullYear() + '-'
      + String(now.getMonth() + 1).padStart(2, '0') + '-'
      + String(now.getDate()).padStart(2, '0');
  }

  function dateState(trip) {
    var todayLocal = localDateOnly();
    var tripMode = todayLocal < trip.start ? 'pre-trip'
      : (todayLocal > trip.end ? 'post-trip' : 'in-trip');
    var currentDay = tripMode === 'in-trip'
      ? trip.days.filter(function (day) { return day.date === todayLocal; })[0] || null
      : null;
    return {
      todayLocal: todayLocal,
      tripMode: tripMode,
      currentDay: currentDay,
      currentRegion: currentDay ? currentDay.region : null,
      pastDays: trip.days.filter(function (day) { return day.date < todayLocal; }),
      futureDays: trip.days.filter(function (day) { return day.date > todayLocal; })
    };
  }

  function localMidnight(isoDate) {
    var parts = isoDate.split('-').map(Number);
    return new Date(parts[0], parts[1] - 1, parts[2]);
  }

  /* ---- 홈 — Today와 향후 4일 ---- */
  var panel = document.getElementById('today-panel');
  var tripDataEl = document.getElementById('trip-data');
  if (panel && tripDataEl) {
    try {
      var homeTrip = JSON.parse(tripDataEl.textContent);
      var homeState = dateState(homeTrip);
      if (homeState.tripMode === 'in-trip' && homeState.currentDay) {
        var today = homeState.currentDay;
        var nextActivity = (today.next || [])[0];
        var bookingItems = (today.bookings || []).map(function (item) {
          return '<li><strong>' + htmlEscape(item.t) + '</strong> ' + htmlEscape(item.n) + '</li>';
        }).join('');
        var alertItems = (today.alerts || []).map(function (item) {
          return '<li>' + htmlEscape(item) + '</li>';
        }).join('');
        var upNext = homeState.futureDays.slice(0, 4).map(function (day) {
          return '<a class="today-preview-row" href="' + htmlEscape(day.url) + '">'
            + '<span><strong>' + htmlEscape(day.date_label || day.date) + '</strong> '
            + htmlEscape(day.city) + '</span><span aria-hidden="true">→</span></a>';
        }).join('');
        panel.innerHTML =
          '<div class="action-card today-current" data-current-region="' + htmlEscape(today.region)
          + '" aria-current="date">'
          + '<div class="day-card-head"><span class="label">TODAY · '
          + htmlEscape(today.date_label || today.date) + '</span>'
          + '<span class="day-num">DAY ' + today.n + '</span></div>'
          + '<div class="action-when today-city">' + htmlEscape(today.city) + '</div>'
          + '<p class="card-dek">' + htmlEscape(today.title) + '</p>'
          + (nextActivity ? '<div class="today-next"><span class="label">NEXT</span>'
            + '<div class="action-what">' + htmlEscape(nextActivity.t) + ' '
            + htmlEscape(nextActivity.n) + '</div></div>' : '')
          + '<div class="btn-row today-actions"><a class="btn btn-primary" href="'
          + htmlEscape(today.url) + '">오늘 일정</a>'
          + '<a class="btn btn-secondary" href="map/index.html">오늘 지도</a>'
          + '<a class="btn btn-secondary" href="schedule.html">전체 일정</a></div></div>'
          + (bookingItems || alertItems ? '<section class="today-ops" aria-labelledby="today-ops-title">'
            + '<h2 id="today-ops-title">예약 · 확인</h2><div class="prose"><ul>'
            + bookingItems + alertItems + '</ul></div></section>' : '')
          + (upNext ? '<section class="today-preview" aria-labelledby="up-next-title">'
            + '<div class="schedule-live-heading"><span class="label">UP NEXT</span>'
            + '<h2 id="up-next-title">다가오는 일정</h2></div>' + upNext + '</section>' : '');
      } else if (homeState.tripMode === 'pre-trip') {
        var firstDay = homeTrip.days[0];
        var left = Math.round((localMidnight(homeTrip.start) - localMidnight(homeState.todayLocal)) / 86400000);
        panel.innerHTML = '<div class="action-card"><span class="label">TRIP STARTS IN ' + left + ' DAYS</span>'
          + '<div class="action-when">D-' + left + '</div>'
          + '<div class="action-what">Day 1 · ' + htmlEscape(firstDay.city) + '</div>'
          + '<p class="card-dek">' + htmlEscape(firstDay.title) + '</p>'
          + '<div class="btn-row today-actions"><a class="btn btn-primary" href="'
          + htmlEscape(firstDay.url) + '">첫 일정</a>'
          + '<a class="btn btn-secondary" href="prepare/index.html">준비 확인</a>'
          + '<a class="btn btn-secondary" href="schedule.html">전체 일정</a></div></div>';
      } else if (homeState.tripMode === 'in-trip') {
        panel.innerHTML = '<div class="action-card"><span class="label">TODAY</span>'
          + '<div class="action-what">오늘 날짜의 일정이 없습니다.</div>'
          + '<div class="btn-row today-actions"><a class="btn btn-secondary" href="schedule.html">전체 일정</a></div></div>';
      } else {
        panel.innerHTML = '<div class="action-card"><span class="label">TRIP COMPLETED</span>'
          + '<div class="action-what">43일의 여정을 모두 마쳤습니다.</div>'
          + '<div class="btn-row today-actions"><a class="btn btn-secondary" href="schedule.html">전체 일정 보기</a></div></div>';
      }
    } catch (err) {
      panel.innerHTML = '<p class="meta">오늘 일정을 불러오지 못했습니다. <a href="schedule.html">전체 일정</a></p>';
    }
  }

  /* ---- 전체 일정 — in-trip에서 NOW → Future → collapsed Past ---- */
  var schedDataEl = document.getElementById('schedule-regions-data');
  var scheduleDataEl = document.getElementById('schedule-data');
  if (schedDataEl && scheduleDataEl) {
    try {
      var regions = JSON.parse(schedDataEl.textContent);
      var scheduleTrip = JSON.parse(scheduleDataEl.textContent);
      var scheduleState = dateState(scheduleTrip);
      var regionNames = { return: 'Return' };
      regions.forEach(function (region) { regionNames[region.slug] = region.name; });
      var topbarTitle = document.querySelector('.topbar .tb-title');
      if (topbarTitle) {
        if (scheduleState.tripMode === 'pre-trip') topbarTitle.textContent = 'NEXT · ' + regions[0].name;
        else if (scheduleState.tripMode === 'post-trip') topbarTitle.textContent = 'Trip Complete';
        else if (scheduleState.currentRegion) topbarTitle.textContent = regionNames[scheduleState.currentRegion] || scheduleState.currentRegion;
      }

      function reducedMotion() {
        return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      }
      function selectTab(slug) {
        var tabs = document.querySelectorAll('.tabs a[href^="#"]');
        for (var i = 0; i < tabs.length; i++) tabs[i].removeAttribute('aria-current');
        var target = document.querySelector('.tabs a[href="#' + slug + '"]');
        if (target) {
          target.setAttribute('aria-current', 'page');
          setTimeout(function () {
            target.scrollIntoView({ inline: 'center', block: 'nearest', behavior: reducedMotion() ? 'auto' : 'smooth' });
          }, 100);
        }
      }

      if (scheduleState.currentRegion) selectTab(scheduleState.currentRegion);
      else if (scheduleState.tripMode === 'pre-trip') selectTab(regions[0].slug);

      var canonical = document.getElementById('schedule-canonical');
      var live = document.getElementById('schedule-live');
      var pastDetails = document.getElementById('schedule-past');
      if (scheduleState.tripMode === 'in-trip' && scheduleState.currentDay && canonical && live) {
        var cards = {};
        canonical.querySelectorAll('.day-card[data-date]').forEach(function (card) {
          cards[card.dataset.date] = card;
        });
        var nowRoot = document.getElementById('schedule-now');
        var futureRoot = document.getElementById('schedule-future');
        var pastRoot = document.getElementById('schedule-past-days');
        var currentCard = cards[scheduleState.currentDay.date];
        if (currentCard) {
          currentCard.setAttribute('aria-current', 'date');
          nowRoot.appendChild(currentCard);
        }
        scheduleState.futureDays.forEach(function (day) {
          if (cards[day.date]) futureRoot.appendChild(cards[day.date]);
        });
        scheduleState.pastDays.forEach(function (day) {
          if (cards[day.date]) pastRoot.appendChild(cards[day.date]);
        });
        document.getElementById('schedule-future-section').hidden = scheduleState.futureDays.length === 0;
        var pastSummary = document.getElementById('schedule-past-summary');
        pastSummary.textContent = '지난 일정 ' + scheduleState.pastDays.length + '일 보기';
        pastSummary.setAttribute('aria-expanded', 'false');
        pastDetails.addEventListener('toggle', function () {
          pastSummary.setAttribute('aria-expanded', pastDetails.open ? 'true' : 'false');
        });
        canonical.hidden = true;
        live.hidden = false;
      }

      var tabLinks = document.querySelectorAll('.tabs a[href^="#"]');
      for (var tIdx = 0; tIdx < tabLinks.length; tIdx++) {
        tabLinks[tIdx].addEventListener('click', function (event) {
          var slug = this.getAttribute('href').slice(1);
          selectTab(slug);
          if (scheduleState.tripMode === 'in-trip' && live && !live.hidden) {
            var visibleDay = live.querySelector('.day-card[data-day-region="' + slug + '"]');
            if (visibleDay) {
              event.preventDefault();
              if (pastDetails.contains(visibleDay)) pastDetails.open = true;
              visibleDay.scrollIntoView({ block: 'start', behavior: reducedMotion() ? 'auto' : 'smooth' });
              history.replaceState(null, '', '#' + slug);
            }
          }
        });
      }
    } catch (err) {
      /* 정적 canonical 일정이 그대로 fallback이다. */
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

  /* ---- 여행 프랑스어 (Travel French) — TTS, 복사, 즐겨찾기, 실시간 검색 ---- */
  var FAV_KEY = 'spfr_travel_french_favs';
  function getFrenchFavs() {
    try {
      var raw = localStorage.getItem(FAV_KEY);
      if (!raw) return [];
      var parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) { return []; }
  }
  function saveFrenchFavs(favs) {
    try {
      localStorage.setItem(FAV_KEY, JSON.stringify(favs));
    } catch (e) {}
  }

  var cachedVoices = [];
  function updateVoices() {
    try {
      if ('speechSynthesis' in window) {
        cachedVoices = window.speechSynthesis.getVoices() || [];
      }
    } catch (e) {}
  }
  if ('speechSynthesis' in window) {
    updateVoices();
    if (window.speechSynthesis.onvoiceschanged !== undefined) {
      window.speechSynthesis.onvoiceschanged = updateVoices;
    }
  }

  function getFrenchVoice() {
    if (!('speechSynthesis' in window)) return null;
    try {
      var voices = cachedVoices.length ? cachedVoices : (window.speechSynthesis.getVoices() || []);
      for (var i = 0; i < voices.length; i++) {
        if (voices[i].lang === 'fr-FR' || voices[i].lang === 'fr_FR') return voices[i];
      }
      for (var j = 0; j < voices.length; j++) {
        if (voices[j].lang && voices[j].lang.toLowerCase().indexOf('fr') === 0) return voices[j];
      }
    } catch (e) {}
    return null;
  }

  function speakFrench(text, btn) {
    if (!('speechSynthesis' in window)) {
      if (btn) {
        btn.disabled = true;
        btn.title = '이 기기에서는 음성 재생을 지원하지 않습니다.';
      }
      return false;
    }
    try {
      if (window.speechSynthesis.speaking || window.speechSynthesis.pending) {
        window.speechSynthesis.cancel();
      }
      var u = new SpeechSynthesisUtterance(text);
      u.lang = 'fr-FR';
      u.rate = 0.88;
      var voice = getFrenchVoice();
      if (voice) u.voice = voice;

      // Keep reference to prevent WebKit premature garbage collection
      window.__currentUtterance = u;

      if (btn) {
        var origSpan = btn.querySelector('span');
        var origText = origSpan ? origSpan.textContent : '듣기';
        btn.classList.add('playing');
        btn.classList.remove('failed');
        if (origSpan) origSpan.textContent = '재생 중';

        function resetBtn() {
          btn.classList.remove('playing');
          if (origSpan) origSpan.textContent = origText;
        }
        function failBtn() {
          btn.classList.remove('playing');
          btn.classList.add('failed');
          if (origSpan) origSpan.textContent = '재생 실패';
          setTimeout(function () {
            btn.classList.remove('failed');
            if (origSpan) origSpan.textContent = origText;
          }, 1400);
        }

        u.onend = resetBtn;
        u.onerror = failBtn;
      }
      window.speechSynthesis.speak(u);
      return true;
    } catch (err) {
      if (btn) {
        btn.classList.remove('playing');
        btn.classList.add('failed');
        var fSpan = btn.querySelector('span');
        if (fSpan) fSpan.textContent = '재생 실패';
        setTimeout(function () {
          btn.classList.remove('failed');
          if (fSpan) fSpan.textContent = '듣기';
        }, 1400);
      }
      return false;
    }
  }

  // 1. Initial setup of favorite buttons on load
  function initFrenchFavs() {
    var favs = getFrenchFavs();
    var favBtns = document.querySelectorAll('.btn-phrase-fav');
    for (var i = 0; i < favBtns.length; i++) {
      var id = favBtns[i].getAttribute('data-fav-id');
      var isFav = favs.indexOf(id) >= 0;
      favBtns[i].setAttribute('aria-pressed', isFav ? 'true' : 'false');
      var span = favBtns[i].querySelector('span');
      if (span) span.textContent = isFav ? '저장됨' : '저장';
    }
  }
  initFrenchFavs();

  // 2. Global Event Delegation for phrase buttons (audio, copy, fav)
  document.addEventListener('click', function (e) {
    // Audio / Speech Synthesis
    var audioBtn = e.target.closest('.btn-phrase-audio');
    if (audioBtn) {
      var text = audioBtn.getAttribute('data-audio');
      if (text) {
        speakFrench(text, audioBtn);
      }
      return;
    }

    // Copy to clipboard
    var copyBtn = e.target.closest('.btn-phrase-copy');
    if (copyBtn) {
      var copyText = copyBtn.getAttribute('data-copy');
      if (copyText) {
        var origSpan = copyBtn.querySelector('span');
        var origText = origSpan ? origSpan.textContent : '복사';
        function setCopied() {
          copyBtn.classList.remove('failed');
          copyBtn.classList.add('copied');
          if (origSpan) origSpan.textContent = '복사됨';
          setTimeout(function () {
            copyBtn.classList.remove('copied');
            if (origSpan) origSpan.textContent = origText;
          }, 1400);
        }
        function setCopyFailed() {
          copyBtn.classList.add('failed');
          if (origSpan) origSpan.textContent = '복사 실패';
          setTimeout(function () {
            copyBtn.classList.remove('failed');
            if (origSpan) origSpan.textContent = origText;
          }, 1400);
        }

        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(copyText).then(setCopied, function () {
            fallbackCopy(copyText, setCopied, setCopyFailed);
          });
        } else {
          fallbackCopy(copyText, setCopied, setCopyFailed);
        }
      }
      return;
    }

    // Favorite toggle
    var favBtn = e.target.closest('.btn-phrase-fav');
    if (favBtn) {
      var fid = favBtn.getAttribute('data-fav-id');
      if (fid) {
        var favs = getFrenchFavs();
        var idx = favs.indexOf(fid);
        var isNowFav = false;
        if (idx >= 0) {
          favs.splice(idx, 1);
        } else {
          favs.push(fid);
          isNowFav = true;
        }
        saveFrenchFavs(favs);
        favBtn.setAttribute('aria-pressed', isNowFav ? 'true' : 'false');
        var fSpan = favBtn.querySelector('span');
        if (fSpan) fSpan.textContent = isNowFav ? '저장됨' : '저장';

        // Update all buttons with same id across the page
        var allSame = document.querySelectorAll('.btn-phrase-fav[data-fav-id="' + fid + '"]');
        for (var sIdx = 0; sIdx < allSame.length; sIdx++) {
          allSame[sIdx].setAttribute('aria-pressed', isNowFav ? 'true' : 'false');
          var sameSpan = allSame[sIdx].querySelector('span');
          if (sameSpan) sameSpan.textContent = isNowFav ? '저장됨' : '저장';
        }

        if (typeof window.applyFrenchFilter === 'function') {
          window.applyFrenchFilter();
        }
      }
      return;
    }
  });

  function fallbackCopy(text, cb, errCb) {
    try {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      var successful = document.execCommand('copy');
      document.body.removeChild(ta);
      if (successful) {
        if (cb) cb();
      } else {
        if (errCb) errCb();
      }
    } catch (e) {
      if (errCb) errCb();
    }
  }

  // 3. Travel French Page (prepare/french.html) Search & Category Filters
  var frenchSearchInput = document.getElementById('french-search');
  var frenchChips = document.getElementById('french-filter-chips');
  var frenchGrid = document.getElementById('french-phrase-grid');
  var frenchNoResults = document.getElementById('french-no-results');
  var frenchResetBtn = document.getElementById('french-reset-btn');
  var frenchListTitle = document.getElementById('french-list-title');

  if (frenchGrid && frenchChips) {
    var curCategory = 'essential';

    function applyFrenchFilter() {
      var query = (frenchSearchInput ? frenchSearchInput.value : '').trim().toLowerCase();
      var favs = getFrenchFavs();
      var cards = frenchGrid.querySelectorAll('.phrase-card');
      var visibleCount = 0;

      for (var c = 0; c < cards.length; c++) {
        var card = cards[c];
        var pid = card.getAttribute('data-phrase-id') || '';
        var cat = card.getAttribute('data-category') || '';
        var pri = card.getAttribute('data-priority') || '';
        var sData = card.getAttribute('data-search') || '';

        var matchCat = false;
        if (query) {
          if (curCategory === 'fav') {
            matchCat = favs.indexOf(pid) >= 0;
          } else {
            matchCat = true;
          }
        } else {
          if (curCategory === 'all') {
            matchCat = true;
          } else if (curCategory === 'fav') {
            matchCat = favs.indexOf(pid) >= 0;
          } else if (curCategory === 'essential') {
            matchCat = (cat === 'essential');
          } else {
            matchCat = (cat === curCategory);
          }
        }

        var matchQuery = true;
        if (query) {
          matchQuery = sData.indexOf(query) >= 0;
        }

        if (matchCat && matchQuery) {
          card.hidden = false;
          card.style.display = "";
          visibleCount++;
        } else {
          card.hidden = true;
          card.style.display = "none";
        }
      }

      if (frenchNoResults) {
        frenchNoResults.style.display = (visibleCount === 0) ? 'flex' : 'none';
      }
      if (frenchListTitle) {
        if (curCategory === 'fav') {
          frenchListTitle.textContent = '즐겨찾기한 회화 (' + visibleCount + '건)';
        } else if (query) {
          frenchListTitle.textContent = '검색 결과 (' + visibleCount + '건)';
        } else if (curCategory === 'essential') {
          frenchListTitle.textContent = '기본 회화 20선 (' + visibleCount + '문구)';
        } else if (curCategory === 'all') {
          frenchListTitle.textContent = '전체 회화 (' + visibleCount + '문구)';
        } else {
          frenchListTitle.textContent = '상황별 회화 (' + visibleCount + '문구)';
        }
      }
    }
    window.applyFrenchFilter = applyFrenchFilter;

    if (frenchSearchInput) {
      frenchSearchInput.addEventListener('input', applyFrenchFilter);
    }

    frenchChips.addEventListener('click', function (e) {
      var chip = e.target.closest('.chip');
      if (!chip) return;
      var cat = chip.getAttribute('data-category');
      if (!cat) return;
      curCategory = cat;

      var allChips = frenchChips.querySelectorAll('.chip');
      for (var k = 0; k < allChips.length; k++) {
        allChips[k].setAttribute('aria-pressed', 'false');
      }
      chip.setAttribute('aria-pressed', 'true');
      applyFrenchFilter();
    });

    if (frenchResetBtn) {
      frenchResetBtn.addEventListener('click', function () {
        if (frenchSearchInput) frenchSearchInput.value = '';
        curCategory = 'all';
        var allChips = frenchChips.querySelectorAll('.chip');
        for (var k = 0; k < allChips.length; k++) {
          allChips[k].setAttribute('aria-pressed', allChips[k].getAttribute('data-category') === 'all' ? 'true' : 'false');
        }
        applyFrenchFilter();
      });
    }

    // Apply initial filter on load
    applyFrenchFilter();
  }

  // 4. Paris Museum Booking Interactive State (prepare/paris-museums.html)
  var PARIS_MUSEUM_STORAGE_KEY = 'spfr_paris_museum_booking_state';

  function getParisMuseumState() {
    try {
      var raw = localStorage.getItem(PARIS_MUSEUM_STORAGE_KEY);
      if (!raw) return {};
      var parsed = JSON.parse(raw);
      return (typeof parsed === 'object' && parsed !== null && !Array.isArray(parsed)) ? parsed : {};
    } catch (e) {
      return {};
    }
  }

  function saveParisMuseumState(state) {
    try {
      localStorage.setItem(PARIS_MUSEUM_STORAGE_KEY, JSON.stringify(state));
      return true;
    } catch (e) {
      return false;
    }
  }

  function renderParisMuseumUI() {
    var cards = document.querySelectorAll('.paris-museum-card');
    if (!cards.length) return;

    var state = getParisMuseumState();
    var counts = {
      'book-now': 0,
      'check-sale': 0,
      'book-later': 0,
      'recheck': 0,
      'booked': 0,
      'no-reservation': 0,
      'total': cards.length
    };

    cards.forEach(function (card) {
      var id = card.getAttribute('data-museum-id');
      var canonical = card.getAttribute('data-canonical-status');
      var local = state[id];

      var effective = canonical;
      if (local === 'booked') {
        effective = 'booked';
      } else if (local === 'recheck') {
        effective = 'recheck';
      }

      card.setAttribute('data-effective-status', effective);
      card.classList.remove('is-booked', 'is-recheck');
      if (effective === 'booked') card.classList.add('is-booked');
      if (effective === 'recheck') card.classList.add('is-recheck');

      if (counts[effective] !== undefined) {
        counts[effective]++;
      }

      // Badge update
      var badgeContainer = card.querySelector('.status-badge-container');
      if (badgeContainer) {
        if (effective === 'booked') {
          badgeContainer.innerHTML = '<span class="badge badge-ok">✓ 예약 완료</span>';
        } else if (effective === 'recheck') {
          badgeContainer.innerHTML = '<span class="badge badge-caution">재확인 필요</span>';
        } else if (canonical === 'book-now') {
          badgeContainer.innerHTML = '<span class="badge badge-must">1차 · 지금</span>';
        } else if (canonical === 'check-sale') {
          badgeContainer.innerHTML = '<span class="badge badge-caution">2차 · 9월 초</span>';
        } else if (canonical === 'book-later') {
          badgeContainer.innerHTML = '<span class="badge badge-neutral">3차 · 직전</span>';
        } else if (canonical === 'no-reservation') {
          badgeContainer.innerHTML = '<span class="badge badge-ok">예약 불필요</span>';
        }
      }

      // Book Toggle Button
      var bookBtn = card.querySelector('.btn-museum-book-toggle');
      if (bookBtn) {
        if (effective === 'booked') {
          bookBtn.textContent = '완료 취소';
          bookBtn.classList.remove('btn-primary');
          bookBtn.classList.add('btn-secondary');
          bookBtn.setAttribute('data-action', 'unbook');
        } else {
          bookBtn.textContent = '✓ 예약 완료';
          bookBtn.classList.remove('btn-secondary');
          bookBtn.classList.add('btn-primary');
          bookBtn.setAttribute('data-action', 'book');
        }
      }

      // Recheck Toggle Button
      var recheckBtn = card.querySelector('.btn-museum-recheck-toggle');
      if (recheckBtn) {
        if (effective === 'recheck') {
          recheckBtn.textContent = '재확인 해제';
          recheckBtn.setAttribute('data-action', 'unrecheck');
        } else {
          recheckBtn.textContent = '재확인';
          recheckBtn.setAttribute('data-action', 'recheck');
        }
        recheckBtn.style.display = (effective === 'booked') ? 'none' : '';
      }
    });

    // Update summary counts
    var countBookNow = document.getElementById('count-book-now');
    if (countBookNow) countBookNow.textContent = counts['book-now'];
    var countCheckSale = document.getElementById('count-check-sale');
    if (countCheckSale) countCheckSale.textContent = counts['check-sale'];
    var countBookLater = document.getElementById('count-book-later');
    if (countBookLater) countBookLater.textContent = counts['book-later'];
    var countRecheck = document.getElementById('count-recheck');
    if (countRecheck) countRecheck.textContent = counts['recheck'];
    var countBooked = document.getElementById('count-booked');
    if (countBooked) countBooked.textContent = counts['booked'];
    var countNoReservation = document.getElementById('count-no-reservation');
    if (countNoReservation) countNoReservation.textContent = counts['no-reservation'];

    applyParisMuseumFilter();
  }

  function applyParisMuseumFilter() {
    var activeChip = document.querySelector('.paris-filter-chip[aria-pressed="true"]');
    var filter = activeChip ? activeChip.getAttribute('data-filter') : 'all';
    var cards = document.querySelectorAll('.paris-museum-card');

    cards.forEach(function (card) {
      var eff = card.getAttribute('data-effective-status');
      if (filter === 'all' || eff === filter) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
  }

  window.__renderParisMuseumUI = renderParisMuseumUI;

  // Initialize on script execution if DOM ready, or DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderParisMuseumUI);
  } else {
    renderParisMuseumUI();
  }

  // Global Click Handlers for Paris Museums
  document.addEventListener('click', function (e) {
    var bookBtn = e.target.closest('.btn-museum-book-toggle');
    if (bookBtn) {
      var card = bookBtn.closest('.paris-museum-card');
      var id = card ? card.getAttribute('data-museum-id') : null;
      if (!id) return;

      var action = bookBtn.getAttribute('data-action');
      var state = getParisMuseumState();
      if (action === 'book') {
        state[id] = 'booked';
      } else {
        delete state[id];
      }
      if (saveParisMuseumState(state)) {
        renderParisMuseumUI();
      } else {
        alert('상태를 저장하지 못했습니다 (브라우저 저장소 제한 또는 비활성화).');
      }
      return;
    }

    var recheckBtn = e.target.closest('.btn-museum-recheck-toggle');
    if (recheckBtn) {
      var card = recheckBtn.closest('.paris-museum-card');
      var id = card ? card.getAttribute('data-museum-id') : null;
      if (!id) return;

      var action = recheckBtn.getAttribute('data-action');
      var state = getParisMuseumState();
      if (action === 'recheck') {
        state[id] = 'recheck';
      } else {
        delete state[id];
      }
      if (saveParisMuseumState(state)) {
        renderParisMuseumUI();
      } else {
        alert('상태를 저장하지 못했습니다 (브라우저 저장소 제한 또는 비활성화).');
      }
      return;
    }

    var chip = e.target.closest('.paris-filter-chip');
    if (chip) {
      var allChips = document.querySelectorAll('.paris-filter-chip');
      allChips.forEach(function (c) {
        c.setAttribute('aria-pressed', 'false');
      });
      chip.setAttribute('aria-pressed', 'true');
      applyParisMuseumFilter();
      return;
    }

    var resetBtn = e.target.closest('#btn-reset-museum-state');
    if (resetBtn) {
      if (confirm('내 예약 체크 상태를 모두 초기화하시겠습니까? (정본 계획 상태로 복귀)')) {
        try {
          localStorage.removeItem(PARIS_MUSEUM_STORAGE_KEY);
        } catch (err) {}
        renderParisMuseumUI();
      }
      return;
    }
  });
})();
