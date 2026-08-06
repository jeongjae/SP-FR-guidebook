(function (global) {
  "use strict";

  var MODE_LABELS = {
    walking: "도보",
    driving: "자동차",
    transit: "대중교통",
    bicycling: "자전거"
  };

  // 좌표를 넘긴다. 표시 이름(한글 혼용)은 Google 이 해석하지 못해
  // 출발지가 "내 위치"로 대체되거나 엉뚱한 곳이 찍힌다.
  function mapsQuery(place) {
    if (!place || place.private) return "";
    return place.lat + "," + place.lng;
  }

  function buildPlaceUrl(place) {
    if (!place || place.private) return null;
    if (place.googleMapsUrl) return place.googleMapsUrl;
    var params = new URLSearchParams({ api: "1", query: mapsQuery(place) });
    if (place.googlePlaceId) params.set("query_place_id", place.googlePlaceId);
    return "https://www.google.com/maps/search/?" + params.toString();
  }

  function buildDirectionsUrl(origin, destination, mode) {
    if (!destination || destination.private) return null;
    var params = new URLSearchParams({
      api: "1",
      destination: mapsQuery(destination),
      travelmode: mode || "walking"
    });
    if (destination.googlePlaceId) params.set("destination_place_id", destination.googlePlaceId);
    if (origin && !origin.private) {
      params.set("origin", mapsQuery(origin));
      if (origin.googlePlaceId) params.set("origin_place_id", origin.googlePlaceId);
    }
    return "https://www.google.com/maps/dir/?" + params.toString();
  }

  function selectRoutePlaces(day, placeById, includeOptional) {
    if (!day || !Array.isArray(day.stops)) return [];
    var seen = new Set();
    return day.stops.slice().sort(function (a, b) { return a.order - b.order; })
      .map(function (stop) { return placeById[stop.placeId]; })
      .filter(function (place) {
        if (!place || place.private || seen.has(place.id)) return false;
        if (!includeOptional && place.optional) return false;
        if (day.defaultMode === "driving" && place.type !== "parking") return false;
        seen.add(place.id);
        return true;
      });
  }

  function buildMultiStopRouteUrl(day, placeById, includeOptional) {
    var places = selectRoutePlaces(day, placeById, includeOptional);
    if (!places.length) return null;
    if (places.length === 1) return buildDirectionsUrl(null, places[0], day.defaultMode);
    var params = new URLSearchParams({
      api: "1",
      origin: mapsQuery(places[0]),
      destination: mapsQuery(places[places.length - 1]),
      travelmode: day.defaultMode || "walking"
    });
    var middle = places.slice(1, -1);
    if (middle.length) params.set("waypoints", middle.map(mapsQuery).join("|"));
    return "https://www.google.com/maps/dir/?" + params.toString();
  }

  function parseData(root) {
    var script = root.querySelector('script[type="application/json"]');
    if (!script) throw new Error("Map component data is missing");
    return JSON.parse(script.textContent);
  }

  function setStatus(root, message, state) {
    var status = root.querySelector(".gm-status");
    if (!status) return;
    status.textContent = message;
    status.dataset.state = state || "ready";
    root.classList.toggle("gm-map-error", state === "error");
    if (state === "error") root.classList.remove("gm-map-open");
  }

  function markerGlyph(place, order) {
    var node = document.createElement("span");
    node.className = "gm-marker gm-marker-" + place.type;
    node.textContent = String(order || "•");
    node.setAttribute("aria-label", place.name);
    return node;
  }

  function infoContent(place) {
    var box = document.createElement("div");
    box.className = "gm-info-window";
    var title = document.createElement("strong");
    title.textContent = place.name;
    box.appendChild(title);
    var meta = document.createElement("span");
    meta.textContent = place.city + " · " + place.type;
    box.appendChild(meta);
    var url = buildPlaceUrl(place);
    if (url) {
      var link = document.createElement("a");
      link.href = url;
      link.target = "_blank";
      link.rel = "noopener";
      link.textContent = "Google Maps에서 열기";
      box.appendChild(link);
    }
    return box;
  }

  function enhance(root) {
    var data;
    try { data = parseData(root); }
    catch (error) {
      setStatus(root, "지도 데이터를 읽지 못했습니다. 아래 장소 목록은 계속 사용할 수 있습니다.", "error");
      return;
    }

    var places = data.places || [];
    var placeById = {};
    places.forEach(function (place) { placeById[place.id] = place; });
    var day = data.day || null;
    var map = null;
    var infoWindow = null;
    var markers = [];
    var loaded = false;

    var routeLink = root.querySelector(".gm-route-all");
    if (routeLink && day) {
      var routeUrl = buildMultiStopRouteUrl(day, placeById, false);
      if (routeUrl) routeLink.href = routeUrl;
      else routeLink.hidden = true;
    }

    function selectPlace(id) {
      root.querySelectorAll(".gm-card-main").forEach(function (button) {
        var active = button.dataset.placeId === id;
        button.setAttribute("aria-pressed", String(active));
        button.closest(".gm-place-card").classList.toggle("is-active", active);
      });
      var item = markers.find(function (entry) { return entry.place.id === id; });
      if (item && map) {
        map.panTo({ lat: item.place.lat, lng: item.place.lng });
        map.setZoom(Math.max(map.getZoom() || 13, 14));
        infoWindow.setContent(infoContent(item.place));
        infoWindow.open({ map: map, anchor: item.marker });
      }
    }

    root.querySelectorAll(".gm-card-main").forEach(function (button) {
      button.addEventListener("click", function () { selectPlace(button.dataset.placeId); });
    });

    root.querySelectorAll(".gm-filter").forEach(function (button) {
      button.addEventListener("click", function () {
        var type = button.dataset.type;
        root.querySelectorAll(".gm-filter").forEach(function (item) {
          item.setAttribute("aria-pressed", String(item === button));
        });
        root.querySelectorAll(".gm-place-card").forEach(function (card) {
          card.hidden = type !== "all" && card.dataset.type !== type;
        });
        markers.forEach(function (entry) {
          entry.marker.map = type === "all" || entry.place.type === type ? map : null;
        });
      });
    });

    function loadMap() {
      if (loaded) return;
      loaded = true;
      setStatus(root, "지도를 불러오는 중입니다…", "loading");
      var loader = global.SPFRGoogleMapsLoader;
      if (!loader) {
        setStatus(root, "지도 로더를 사용할 수 없습니다. 아래 장소 목록과 링크를 이용하세요.", "error");
        return;
      }
      loader.load().then(function (maps) {
        var canvas = root.querySelector(".gm-canvas");
        map = new maps.Map(canvas, {
          center: { lat: data.center[0], lng: data.center[1] },
          zoom: data.zoom,
          mapId: loader.mapId(),
          streetViewControl: false,
          fullscreenControl: true,
          mapTypeControl: false
        });
        infoWindow = new maps.InfoWindow();
        var orderById = {};
        if (day) day.stops.forEach(function (stop) {
          if (!(stop.placeId in orderById)) orderById[stop.placeId] = stop.order;
        });
        places.forEach(function (place, index) {
          var marker = new maps.marker.AdvancedMarkerElement({
            map: map,
            position: { lat: place.lat, lng: place.lng },
            title: place.name,
            content: markerGlyph(place, orderById[place.id] === undefined ? index + 1 : orderById[place.id])
          });
          marker.addListener("click", function () { selectPlace(place.id); });
          markers.push({ place: place, marker: marker });
        });
        setStatus(root, "지도와 장소 목록이 연결되었습니다.", "ready");
      }).catch(function () {
        setStatus(root, "지도를 불러오지 못했습니다. 아래 장소 목록과 Google Maps 링크는 계속 사용할 수 있습니다.", "error");
      });
    }

    var disclosure = root.querySelector(".gm-map-disclosure");
    if (disclosure) {
      disclosure.addEventListener("toggle", function () {
        root.classList.toggle("gm-map-open", disclosure.open);
        if (disclosure.open) loadMap();
      });
      if (disclosure.open) loadMap();
    }
  }

  var api = {
    MODE_LABELS: MODE_LABELS,
    buildPlaceUrl: buildPlaceUrl,
    buildDirectionsUrl: buildDirectionsUrl,
    selectRoutePlaces: selectRoutePlaces,
    buildMultiStopRouteUrl: buildMultiStopRouteUrl,
    enhance: enhance
  };
  global.SPFRGoogleMaps = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;

  if (typeof document !== "undefined") {
    document.addEventListener("DOMContentLoaded", function () {
      document.querySelectorAll(".gm-component").forEach(enhance);
    });
  }
}(typeof window !== "undefined" ? window : globalThis));
