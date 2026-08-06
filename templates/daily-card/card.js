(function () {
  "use strict";
  const data = window.CARD_DATA;
  const tiles = window.CARD_TILES;
  const route = window.CARD_ROUTE;
  const weekdays = ["일", "월", "화", "수", "목", "금", "토"];
  const date = new Date(data.date + "T12:00:00");
  const $ = (id) => document.getElementById(id);
  const esc = (value) => String(value ?? "").replace(/[&<>\"]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

  $("day-number").textContent = String(data.day).padStart(2, "0");
  $("date-line").textContent = `${date.getFullYear()}. ${String(date.getMonth()+1).padStart(2,"0")}. ${String(date.getDate()).padStart(2,"0")} ${weekdays[date.getDay()]}요일`;
  $("city-line").textContent = data.city;
  $("title-line").textContent = data.title;
  $("duration-line").textContent = data.startTime && data.endTime
    ? `${data.startTime}–${data.endTime}`
    : (data.startTime ? `${data.startTime}–` : "시각 미정");
  $("fatigue-line").textContent = `피로도 ${data.fatigue}/5`;
  $("distance-line").textContent = data.totalDistance;
  $("total-duration-line").textContent = data.totalDuration ? `총 ${data.totalDuration}` : "";

  const list = (id, items) => { $(id).innerHTML = items.map((x) => `<li>${esc(x)}</li>`).join(""); };
  list("transport-list", data.transport.slice(0, 3));
  list("food-list", data.food.slice(0, 3));
  list("highlight-list", data.highlights.slice(0, 3));
  $("backup-line").textContent = `대체 · ${data.backup}`;

  const timeline = $("timeline");
  timeline.dataset.count = data.stops.length;
  timeline.innerHTML = data.stops.map((stop) => {
    const time = (!stop.end || stop.start === stop.end) ? (stop.start || '')
      : (!stop.start ? stop.end : `${stop.start}–${stop.end}`);
    const detail = stop.menu || stop.reservation;
    return `<article class="timeline-item cat-${esc(stop.category)}">
      <div class="timeline-top"><time class="timeline-time">${esc(time)}</time><h3 class="timeline-name">${esc(stop.name)}</h3></div>
      <p class="timeline-summary">${esc(stop.summary)}</p>
      ${detail ? `<p class="timeline-detail">${esc(detail)}</p>` : ""}
    </article>`;
  }).join("");

  const modes = new Set(data.legs.map((leg) => leg.mode));
  const labels = [];
  if (modes.has("walk")) labels.push('<span class="walk"><i></i>도보</span>');
  if (["metro","train","bus","tram"].some((m) => modes.has(m))) labels.push('<span class="transit"><i></i>대중교통</span>');
  if (["car","taxi"].some((m) => modes.has(m))) labels.push('<span class="car"><i></i>차량</span>');
  if (modes.has("unconfirmed")) labels.push('<span class="unconfirmed"><i></i>이동 미확정</span>');
  $("legend").innerHTML = labels.join("");

  const map = $("map");
  const width = map.clientWidth;
  const height = map.clientHeight;
  const zoom = data.map.zoom;
  const scale = 256 * Math.pow(2, zoom);
  const project = (lat, lng) => {
    const sin = Math.sin(lat * Math.PI / 180);
    return {
      x: (lng + 180) / 360 * scale,
      y: (0.5 - Math.log((1 + sin) / (1 - sin)) / (4 * Math.PI)) * scale
    };
  };
  const center = project(data.map.center[0], data.map.center[1]);
  const screen = (lat, lng) => {
    const p = project(lat, lng);
    return {x: p.x - center.x + width / 2, y: p.y - center.y + height / 2};
  };

  $("tiles").innerHTML = tiles.map((tile) => {
    const x = tile.x * 256 - center.x + width / 2;
    const y = tile.y * 256 - center.y + height / 2;
    return `<img class="map-tile" alt="" src="${tile.src}" style="left:${x}px;top:${y}px">`;
  }).join("");

  const svg = $("route-layer");
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  const pathFor = (coords) => coords.map((coord, index) => {
    const p = screen(coord[1], coord[0]);
    return `${index ? "L" : "M"}${p.x.toFixed(1)},${p.y.toFixed(1)}`;
  }).join(" ");
  if (route && route.length) {
    const path = pathFor(route);
    svg.insertAdjacentHTML("beforeend", `<path class="route-halo" d="${path}"></path><path class="route-path car" d="${path}"></path>`);
  } else {
    const byId = Object.fromEntries(data.stops.map((stop) => [stop.id, stop]));
    for (const leg of data.legs) {
      const from = byId[leg.from], to = byId[leg.to];
      if (!from || !to) continue;
      const path = pathFor([[from.lng, from.lat], [to.lng, to.lat]]);
      svg.insertAdjacentHTML("beforeend", `<path class="route-halo" d="${path}"></path><path class="route-path ${esc(leg.mode)}" d="${path}"></path>`);
    }
  }

  const markerRoot = $("markers");
  const visibleStops = [];
  for (const stop of data.stops) {
    const existing = visibleStops.find((item) => Math.abs(item.lat-stop.lat) < 0.00001 && Math.abs(item.lng-stop.lng) < 0.00001);
    if (existing) {
      existing.orders.push(stop.order);
      existing.name = existing.name.replace(/ 복귀$/, " 출발·복귀");
    } else {
      visibleStops.push({...stop, orders:[stop.order]});
    }
  }

  const placed = [];
  const markerRects = [];
  const overlap = (a, b, pad=7) => !(a.right + pad < b.left || a.left > b.right + pad || a.bottom + pad < b.top || a.top > b.bottom + pad);
  const candidates = [
    [26,-62], [26,18], [-246,-62], [-246,18], [26,-112], [-246,-112], [46,-22], [-266,-22]
  ];
  for (const stop of visibleStops) {
    const point = screen(stop.lat, stop.lng);
    const marker = document.createElement("div");
    marker.className = `map-marker cat-${stop.category}`;
    marker.style.left = `${point.x}px`; marker.style.top = `${point.y}px`;
    marker.textContent = stop.orders.join("/");
    markerRoot.appendChild(marker);
    markerRects.push({left:point.x-23,right:point.x+23,top:point.y-23,bottom:point.y+23});

    const label = document.createElement("div");
    label.className = "map-label";
    label.innerHTML = `<strong>${esc(stop.name)}</strong><span>${esc(stop.start || "")}</span>`;
    label.style.visibility = "hidden";
    markerRoot.appendChild(label);
    const lw = label.offsetWidth, lh = label.offsetHeight;
    let chosen = null;
    for (const [dx, dy] of candidates) {
      const rect = {left:point.x+dx, top:point.y+dy, right:point.x+dx+lw, bottom:point.y+dy+lh};
      const inside = rect.left >= 8 && rect.top >= 8 && rect.right <= width-8 && rect.bottom <= height-30;
      if (inside && !placed.some((item) => overlap(rect,item)) && !markerRects.some((item) => overlap(rect,item,2))) { chosen = rect; break; }
    }
    if (!chosen) {
      outer: for (let radius=70; radius<360; radius+=30) {
        for (let angle=0; angle<360; angle+=30) {
          const rad = angle * Math.PI / 180;
          const left = point.x + Math.cos(rad)*radius - lw/2;
          const top = point.y + Math.sin(rad)*radius - lh/2;
          const rect = {left,top,right:left+lw,bottom:top+lh};
          const inside = rect.left >= 8 && rect.top >= 8 && rect.right <= width-8 && rect.bottom <= height-30;
          if (inside && !placed.some((item) => overlap(rect,item)) && !markerRects.some((item) => overlap(rect,item,2))) { chosen=rect; break outer; }
        }
      }
    }
    chosen = chosen || {left:Math.max(8,Math.min(width-lw-8,point.x+25)),top:Math.max(8,Math.min(height-lh-30,point.y+20))};
    label.style.left = `${chosen.left}px`; label.style.top = `${chosen.top}px`; label.style.visibility = "visible";
    placed.push(chosen);
    const anchorX = Math.max(chosen.left, Math.min(point.x, chosen.right));
    const anchorY = Math.max(chosen.top, Math.min(point.y, chosen.bottom));
    svg.insertAdjacentHTML("beforeend", `<line class="label-connector" x1="${point.x}" y1="${point.y}" x2="${anchorX}" y2="${anchorY}"></line>`);
  }

  const labelOverlaps = placed.reduce((count, rect, i) => count + placed.slice(i+1).filter((other) => overlap(rect, other, 0)).length, 0);
  const overflow = [...document.querySelectorAll(".timeline-item,.summary-cell,.map-label")].filter((el) => el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1).length;
  window.__CARD_QA__ = {labelOverlaps, overflow, tileCount: tiles.length, markerCount: visibleStops.length};
  document.body.dataset.qaLabelOverlaps = String(labelOverlaps);
  document.body.dataset.qaOverflow = String(overflow);
  document.body.dataset.qaTileCount = String(tiles.length);
  document.body.dataset.qaMarkerCount = String(visibleStops.length);
  document.body.dataset.ready = "true";
})();
