import { loadTrip } from "../state.js";
import { esc } from "../ui.js";
import { renderDayInto } from "./day.js";

function localISO(d = new Date()) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

export async function todayView(root) {
  const trip = await loadTrip();
  if (!trip) { root.innerHTML = '<p class="empty">스냅샷이 아직 없다 — 온라인에서 한 번 열어야 한다.</p>'; return; }
  const today = window.__SPFR_TEST_DATE__ || localISO();
  const entry = trip.days.find((d) => d.date === today);
  if (!entry) {
    const first = trip.days[0], last = trip.days[trip.days.length - 1];
    const msg = today < first.date
      ? `여행 시작 전이다 (D1 = ${esc(first.date)})`
      : today > last.date ? "여행이 끝났다" : "오늘 날짜의 Day 를 찾지 못했다";
    root.innerHTML = `<div class="card"><h2>오늘</h2><p class="meta">${msg}</p>
      <p><a href="#/schedule">전체 일정 보기 →</a></p></div>`;
    return;
  }
  root.innerHTML = "";
  await renderDayInto(root, entry.n, { heading: `오늘 · ${esc(entry.dateLabel)}` });
}

export async function scheduleView(root) {
  const trip = await loadTrip();
  if (!trip) { root.innerHTML = '<p class="empty">스냅샷이 아직 없다.</p>'; return; }
  const today = window.__SPFR_TEST_DATE__ || localISO();
  root.innerHTML = `<div class="card"><h2>전체 일정 — ${trip.trip.days}일</h2>
    <div>${trip.days.map((d) => `
      <a class="day-link${d.date === today ? " today-row" : ""}" href="#/day/${d.n}">
        <span class="d">${esc(d.dateLabel)} D${d.n}</span>
        <span>${esc(d.title)}</span>
      </a>`).join("")}</div></div>`;
}
