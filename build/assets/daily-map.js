(function () {
  "use strict";

  const TYPES = {
    accommodation: { label: "숙소", icon: "stay", color: "#6f42a8" },
    attraction: { label: "관광지", icon: "pin", color: "#000091" },
    restaurant: { label: "식당", icon: "food", color: "#a33b14" },
    cafe: { label: "카페", icon: "food", color: "#7a4b18" },
    market: { label: "시장", icon: "table", color: "#276c2e" },
    parking: { label: "주차장", icon: "region", color: "#5b4b16" },
    station: { label: "역", icon: "train", color: "#805000" },
    airport: { label: "공항", icon: "region", color: "#9a2532" }
  };

  const escapeHtml = (value) => String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  function directionsUrl(destination, origin) {
    const params = new URLSearchParams({
      api: "1",
      destination: `${destination.lat},${destination.lng}`,
      travelmode: "walking"
    });
    if (origin) params.set("origin", `${origin.lat},${origin.lng}`);
    return `https://www.google.com/maps/dir/?${params.toString()}`;
  }

  function routeUrl(places) {
    if (places.length < 2) return places[0]?.googleMapsUrl || "https://www.google.com/maps";
    const params = new URLSearchParams({
      api: "1",
      origin: `${places[0].lat},${places[0].lng}`,
      destination: `${places.at(-1).lat},${places.at(-1).lng}`,
      travelmode: "walking"
    });
    if (places.length > 2) {
      params.set("waypoints", places.slice(1, -1).map((place) => `${place.lat},${place.lng}`).join("|"));
    }
    return `https://www.google.com/maps/dir/?${params.toString()}`;
  }

  function markerHtml(place) {
    if (place.type === "attraction") {
      return `<span class="dem-marker-number"><b>${escapeHtml(place.order)}</b></span>`;
    }
    const type = TYPES[place.type] || TYPES.attraction;
    return `<span class="dem-marker-icon" style="--marker-color:${type.color}"><b class="ic ic-only ic-${type.icon}" aria-hidden="true"></b></span>`;
  }

  function placeLabel(place) {
    const type = TYPES[place.type] || TYPES.attraction;
    return place.type === "attraction" ? `${place.order}. ${place.name}` : `${type.label} · ${place.name}`;
  }

  function privacyNote(place) {
    if (place.private) return "비공개 숙소 · 근사 위치";
    if (place.approximate) return "후보 위치 · 예약 후 교체";
    if (place.optional) return "선택 장소";
    return "";
  }

  function actionLinks(place, stay, next) {
    const links = [];
    if (!place.private && place.googleMapsUrl) {
      links.push(`<a target="_blank" rel="noopener" href="${escapeHtml(place.googleMapsUrl)}">Google Maps에서 보기</a>`);
    }
    links.push(`<a target="_blank" rel="noopener" href="${escapeHtml(directionsUrl(place))}">여기까지 길찾기</a>`);
    if (stay && stay.id !== place.id && !stay.private) {
      links.push(`<a target="_blank" rel="noopener" href="${escapeHtml(directionsUrl(place, stay))}">숙소에서 길찾기</a>`);
    }
    if (next) {
      links.push(`<a target="_blank" rel="noopener" href="${escapeHtml(directionsUrl(next, place))}">다음 장소까지 길찾기</a>`);
    }
    return links.join("");
  }

  function popupHtml(place, stay, next) {
    const note = privacyNote(place);
    return `<article class="dem-popup">
      <b>${escapeHtml(placeLabel(place))}</b>
      <time>${escapeHtml(place.plannedTime)}</time>
      <p>${escapeHtml(place.description)}</p>
      ${note ? `<small>${escapeHtml(note)}</small>` : ""}
      <div class="dem-popup-actions">${actionLinks(place, stay, next)}</div>
    </article>`;
  }

  function render(root, day) {
    if (!window.L) {
      root.innerHTML = '<p class="offline-note"><b>지도를 불러오지 못했습니다.</b> 아래 정적 지도와 장소 목록을 사용하세요.</p>';
      return;
    }

    root.innerHTML = `
      <div class="dem-map" role="region" aria-label="${escapeHtml(day.date)} 실행지도"></div>
      <p class="dem-map-note">선은 방문 순서를 잇는 개요이며 실제 보행 경로가 아닙니다. 배경 지도는 온라인에서 표시됩니다.</p>
      <div class="dem-legend" aria-label="지도 범례"></div>
      <ol class="dem-place-list" aria-label="장소 목록"></ol>
      <div class="dem-google-actions" aria-label="Google Maps 바로가기"></div>`;

    const map = window.L.map(root.querySelector(".dem-map"), { scrollWheelZoom: false });
    window.L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    const ordered = [...day.places].sort((a, b) => a.order - b.order);
    const stay = ordered.find((place) => place.type === "accommodation");
    const byId = Object.fromEntries(ordered.map((place) => [place.id, place]));
    const markers = new Map();
    const markerLayer = window.L.featureGroup().addTo(map);
    const list = root.querySelector(".dem-place-list");

    function selectPlace(id, moveMap) {
      root.querySelectorAll(".dem-place-item").forEach((item) => {
        const selected = item.dataset.placeId === id;
        item.classList.toggle("is-active", selected);
        item.querySelector("button").setAttribute("aria-pressed", String(selected));
      });
      const marker = markers.get(id);
      if (marker && moveMap) {
        map.setView(marker.getLatLng(), Math.max(map.getZoom(), 16), { animate: true });
        marker.openPopup();
      }
      root.querySelector(`[data-place-id="${CSS.escape(id)}"]`)?.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }

    ordered.forEach((place, index) => {
      const next = ordered[index + 1];
      const type = TYPES[place.type] || TYPES.attraction;
      const marker = window.L.marker([place.lat, place.lng], {
        icon: window.L.divIcon({
          className: "daily-map-marker",
          html: markerHtml(place),
          iconSize: [38, 44],
          iconAnchor: [19, 42],
          popupAnchor: [0, -40]
        }),
        title: placeLabel(place)
      }).addTo(markerLayer);
      marker.bindPopup(popupHtml(place, stay, next), { maxWidth: 310 });
      marker.on("click", () => selectPlace(place.id, false));
      markers.set(place.id, marker);

      const item = document.createElement("li");
      item.className = "dem-place-item";
      item.dataset.placeId = place.id;
      item.innerHTML = `<button type="button" aria-pressed="false">
          <span class="dem-list-marker" style="--marker-color:${type.color}">${markerHtml(place)}</span>
          <span class="dem-list-copy"><b>${escapeHtml(place.name)}</b><time>${escapeHtml(place.plannedTime)}</time><span>${escapeHtml(place.description)}</span>${privacyNote(place) ? `<small>${escapeHtml(privacyNote(place))}</small>` : ""}</span>
        </button>
        <div class="dem-list-actions">${actionLinks(place, stay, next)}</div>`;
      item.querySelector("button").addEventListener("click", () => selectPlace(place.id, true));
      list.appendChild(item);
    });

    day.routes.forEach((route) => {
      const from = byId[route.from];
      const to = byId[route.to];
      if (!from || !to) return;
      window.L.polyline([[from.lat, from.lng], [to.lat, to.lng]], {
        color: "#59636e",
        weight: 3,
        opacity: 0.75,
        dashArray: "7 8",
        interactive: false
      }).addTo(map);
    });

    if (ordered.length > 1) map.fitBounds(markerLayer.getBounds().pad(0.18), { maxZoom: 16 });
    else map.setView(day.center, day.zoom);

    const usedTypes = [...new Set(ordered.map((place) => place.type))];
    root.querySelector(".dem-legend").innerHTML = usedTypes.map((typeName) => {
      const type = TYPES[typeName] || TYPES.attraction;
      return `<span><i style="--marker-color:${type.color}"></i>${escapeHtml(type.label)}</span>`;
    }).join("");

    const routePlaces = ordered.filter((place) => !place.optional || place.type === "accommodation");
    root.querySelector(".dem-google-actions").innerHTML = `
      <a class="dem-primary-action" target="_blank" rel="noopener" href="${escapeHtml(routeUrl(routePlaces))}">Google Maps로 일정 열기</a>`;
  }

  document.querySelectorAll("[data-daily-map-date]").forEach((root) => {
    const day = window.DAILY_MAP_DATA?.days?.find((item) => item.date === root.dataset.dailyMapDate);
    if (!day) {
      root.innerHTML = '<p class="offline-note">이 날짜의 인터랙티브 지도 데이터가 없습니다.</p>';
      return;
    }
    render(root, day);
  });
})();
