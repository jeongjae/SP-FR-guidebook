import { loadPlacesIndex, loadTrip } from "../state.js";
import { esc, el } from "../ui.js";

export async function searchView(root) {
  const [index, trip] = await Promise.all([loadPlacesIndex(), loadTrip()]);
  if (!index || !trip) { root.innerHTML = '<p class="empty">스냅샷이 아직 없다.</p>'; return; }
  root.innerHTML = "";
  const card = el(`<div class="card">
    <h2>검색</h2>
    <div class="searchbox"><input type="text" id="q" placeholder="장소·하루·도시 검색" autocomplete="off"></div>
    <div id="results"></div>
  </div>`);
  root.appendChild(card);
  const input = card.querySelector("#q");
  const results = card.querySelector("#results");

  const pool = [
    ...index.places.map((p) => ({
      t: p.name, x: `${p.region} ${p.pin || ""} ${p.slug}`,
      href: `#/place/${p.slug}`, k: p.gradeLabel || "장소",
    })),
    ...trip.days.map((d) => ({
      t: `${d.dateLabel} · Day ${d.n} ${d.title}`, x: d.city,
      href: `#/day/${d.n}`, k: "하루",
    })),
  ];

  const render = () => {
    const q = input.value.trim().toLowerCase();
    if (!q) { results.innerHTML = '<p class="meta">이름·도시·슬러그의 일부를 입력한다.</p>'; return; }
    const hits = pool.filter((e) =>
      (e.t + " " + e.x).toLowerCase().includes(q)).slice(0, 30);
    results.innerHTML = hits.length
      ? hits.map((e) => `<a class="day-link" href="${e.href}">
          <span class="badge">${esc(e.k)}</span><span>${esc(e.t)}</span></a>`).join("")
      : '<p class="empty">결과 없음</p>';
  };
  input.addEventListener("input", render);
  render();
  input.focus();
}
