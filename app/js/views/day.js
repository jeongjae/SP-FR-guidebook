import { loadDay, loadTrip } from "../state.js";
import { appendEvent, stopKey } from "../events.js";
import { esc, el, badgeFor, stripGrade, notesHtml, noteButton } from "../ui.js";

const DAY_TYPE = { city: "CITY", driving: "DRIVING", transfer: "TRANSFER", living: "LIVING" };
const MODE = { walk: "도보", car: "운전", train: "기차", bus: "버스", metro: "지하철",
  tram: "트램", taxi: "택시", flight: "비행", funicular: "푸니쿨라" };

export async function renderDayInto(root, n, { heading } = {}) {
  const day = await loadDay(n);
  if (!day) { root.innerHTML = '<p class="empty">이 날의 데이터가 없다.</p>'; return; }
  const trip = await loadTrip();

  const head = el(`<div class="card">
    <div class="title-row"><h2>${esc(heading || `${dayLabel(trip, n)} · Day ${n}`)}</h2>
      <span class="badge">${esc(DAY_TYPE[day.dayType] || day.dayType || "")}</span></div>
    <p class="meta">${esc(day.city)} · 피로도 ${esc(day.fatigue)}/5 · ${esc(day.totalDistance || "")}</p>
    <p><strong>${esc(day.title)}</strong></p>
    <div class="row nav-row">
      ${n > 1 ? `<a class="btn" href="#/day/${n - 1}">← D${n - 1}</a>` : ""}
      ${n < 43 ? `<a class="btn" href="#/day/${n + 1}">D${n + 1} →</a>` : ""}
    </div>
    <div class="day-notes">${notesHtml(day.notes)}</div>
  </div>`);
  head.querySelector(".nav-row").appendChild(
    noteButton({ kind: "day", key: `day-${String(n).padStart(2, "0")}` }, "이날 메모"));
  root.appendChild(head);

  const legByFrom = new Map((day.legs || []).map((l) => [l.from, l]));
  const timeline = el('<div class="card"><h3>시간표</h3></div>');
  for (const stop of day.stops) {
    timeline.appendChild(renderStop(n, stop));
    const leg = legByFrom.get(stop.id);
    if (leg) {
      timeline.appendChild(el(`<div class="leg">↓ ${esc(MODE[leg.mode] || leg.mode)} · ${esc(leg.duration || "")}${leg.distance ? " · " + esc(leg.distance) : ""}</div>`));
    }
  }
  root.appendChild(timeline);

  const extras = el(`<div class="card">
    ${day.food?.length ? `<h3>식사</h3><ul>${day.food.map((f) => `<li>${esc(f)}</li>`).join("")}</ul>` : ""}
    ${day.transport?.length ? `<h3>이동</h3><ul>${day.transport.map((t) => `<li>${esc(t)}</li>`).join("")}</ul>` : ""}
    ${day.backup ? `<h3>Plan B</h3><p class="meta" style="white-space:pre-wrap">${esc(day.backup)}</p>` : ""}
    ${day.needsReview?.length ? `<h3>재확인</h3><ul>${day.needsReview.map((t) => `<li>${esc(t)}</li>`).join("")}</ul>` : ""}
    <p class="meta"><a href="../daily/day-${String(n).padStart(2, "0")}.html">본 사이트에서 이 날 보기 →</a></p>
  </div>`);
  root.appendChild(extras);
}

function dayLabel(trip, n) {
  const e = trip?.days?.find((d) => d.n === n);
  return e ? e.dateLabel : `Day ${n}`;
}

function renderStop(n, stop) {
  const sk = stopKey(n, stop.id);
  const node = el(`<div class="stop${stop.visited ? " visited" : ""}" data-stop="${esc(stop.id)}">
    <span class="time">${esc(stop.start || "")}${stop.end ? "–" + esc(stop.end) : ""}</span>
    ${badgeFor(stop.name)}
    <div class="name">${esc(stripGrade(stop.name))}</div>
    ${stop.summary ? `<div class="summary">${esc(stop.summary)}</div>` : ""}
    ${stop.menu ? `<div class="summary">🍽 ${esc(stop.menu)}</div>` : ""}
    ${stop.reservation ? `<div class="summary">📌 ${esc(stop.reservation)}</div>` : ""}
    <div class="actions"></div>
    <div class="notes">${notesHtml(stop.notes)}</div>
    <div class="row btns"></div>
  </div>`);

  const actions = node.querySelector(".actions");
  for (const st of stop.executionStatuses || []) {
    const label = st.label || st.type || "";
    const detail = st.detail || "";
    const isTask = ["book", "check", "ticket"].includes(st.type);
    const key = `${st.type}:${label}:${detail.slice(0, 40)}`;
    const done = stop.checkedActions?.get(key) === true;
    const row = el(`<div class="summary action-row">
      <span class="badge ${st.type === "confirmed" ? "ok" : "warn"}">${esc(label)}</span>
      ${esc(detail)}</div>`);
    if (isTask) {
      const btn = el(`<button class="small${done ? " on" : ""}" type="button">${done ? "처리됨 ✓" : "처리 완료로 표시"}</button>`);
      btn.addEventListener("click", async () => {
        await appendEvent({ kind: "stop", key: sk }, "check-action",
          { label: key, checked: !done });
        document.dispatchEvent(new CustomEvent("spfr:rerender"));
      });
      row.appendChild(btn);
      if (done) { row.style.opacity = "0.6"; }
    }
    actions.appendChild(row);
  }

  const btns = node.querySelector(".btns");
  const visitBtn = el(`<button class="small${stop.visited ? " on" : ""}" type="button">${stop.visited ? "방문함 ✓" : "방문 체크"}</button>`);
  visitBtn.addEventListener("click", async () => {
    await appendEvent({ kind: "stop", key: sk }, "set-visited", { value: !stop.visited });
    document.dispatchEvent(new CustomEvent("spfr:rerender"));
  });
  btns.appendChild(visitBtn);
  btns.appendChild(noteButton({ kind: "stop", key: sk }));
  if (stop.place_ref) {
    btns.appendChild(el(`<a class="btn small" href="#/place/${esc(stop.place_ref)}">장소 정보</a>`));
  }
  if (stop.lat != null && stop.lng != null) {
    btns.appendChild(el(`<a class="btn small" target="_blank" rel="noopener"
      href="https://www.google.com/maps/search/?api=1&query=${stop.lat}%2C${stop.lng}">지도</a>`));
  }
  return node;
}

export async function dayView(root, params) {
  const n = parseInt(params[0], 10);
  root.innerHTML = "";
  await renderDayInto(root, n);
}
