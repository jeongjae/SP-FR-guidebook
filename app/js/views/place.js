import { loadPlace } from "../state.js";
import { renderMd } from "../md.js";
import { esc, el, notesHtml, noteButton } from "../ui.js";

export async function placeView(root, params) {
  const slug = params[0];
  const place = await loadPlace(slug);
  if (!place) { root.innerHTML = '<p class="empty">장소를 찾지 못했다.</p>'; return; }
  root.innerHTML = "";
  const head = el(`<div class="card">
    <div class="title-row"><h2>${esc(place.name)}</h2>
      <span class="badge">${esc(place.gradeLabel || "")}</span></div>
    <p class="meta">${esc(place.region)}${place.days?.length ? " · 방문일 Day " + place.days.join("·") : ""}</p>
    ${place.summary ? `<p>${esc(place.summary)}</p>` : ""}
    <div class="row btns"></div>
    <div class="notes">${notesHtml(place.notes)}</div>
  </div>`);
  const btns = head.querySelector(".btns");
  btns.appendChild(noteButton({ kind: "place", key: slug }));
  if (place.mapQuery || place.pin) {
    const q = encodeURIComponent(place.mapQuery || place.pin);
    btns.appendChild(el(`<a class="btn small" target="_blank" rel="noopener"
      href="https://www.google.com/maps/search/?api=1&query=${q}">지도</a>`));
  }
  btns.appendChild(el(`<a class="btn small" href="../places/${esc(slug)}.html">본 사이트 페이지</a>`));
  root.appendChild(head);

  if (place.body) {
    const { whyGoMd, bodyMd, practicalMd } = place.body;
    if (whyGoMd) root.appendChild(el(`<div class="card prose"><h3>왜 가는가</h3>${renderMd(whyGoMd)}</div>`));
    if (bodyMd) root.appendChild(el(`<div class="card prose"><h3>더 깊이</h3>${renderMd(bodyMd)}</div>`));
    if (practicalMd) root.appendChild(el(`<div class="card prose"><h3>실용</h3>${renderMd(practicalMd)}</div>`));
  }
}
