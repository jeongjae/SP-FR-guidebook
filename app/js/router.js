import { todayView, scheduleView } from "./views/today.js";
import { dayView } from "./views/day.js";
import { placeView } from "./views/place.js";
import { bookingsView } from "./views/bookings.js";
import { searchView } from "./views/search.js";
import { syncView } from "./views/syncview.js";

const ROUTES = [
  [/^#\/today$/, todayView, "today"],
  [/^#\/schedule$/, scheduleView, "schedule"],
  [/^#\/day\/(\d+)$/, dayView, "schedule"],
  [/^#\/place\/([a-z0-9-]+)$/, placeView, "search"],
  [/^#\/bookings$/, bookingsView, "bookings"],
  [/^#\/search$/, searchView, "search"],
  [/^#\/sync$/, syncView, "sync"],
];

export async function render() {
  const hash = location.hash || "#/today";
  const root = document.getElementById("view");
  for (const [re, view, tab] of ROUTES) {
    const m = hash.match(re);
    if (m) {
      document.querySelectorAll(".tabbar a").forEach((a) =>
        a.classList.toggle("active", a.dataset.tab === tab));
      root.innerHTML = "";
      try {
        await view(root, m.slice(1));
      } catch (err) {
        root.innerHTML = `<div class="card"><h2>오류</h2><p class="meta">${err.message}</p></div>`;
        console.error(err);
      }
      window.scrollTo(0, 0);
      return;
    }
  }
  location.hash = "#/today";
}

export function startRouter() {
  addEventListener("hashchange", render);
  document.addEventListener("spfr:rerender", render);
  document.addEventListener("spfr:snapshot-updated", render);
  return render();
}
