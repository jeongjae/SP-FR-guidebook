import { loadPlace } from "../state.js";
import { renderMd } from "../md.js";
import { esc, el, notesHtml, noteButton } from "../ui.js";
import { buildForm } from "../editforms.js";
import { appendEvent } from "../events.js";

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
    const sections = [
      ["why_go", "왜 가는가", place.body.whyGoMd],
      ["deep", "더 깊이", place.body.bodyMd],
      ["practical", "실용", place.body.practicalMd],
    ];
    for (const [section, title, md] of sections) {
      if (!md && section !== "practical") continue;
      const card = el(`<div class="card prose">
        <div class="title-row"><h3>${esc(title)}</h3></div>
        <div class="prose-body">${renderMd(md || "")}</div></div>`);
      const editBtn = el('<button class="small" type="button">✎ 편집</button>');
      editBtn.addEventListener("click", () => {
        const form = buildForm(
          [{ name: "md", label: `${title} — markdown`, type: "textarea", rows: 14 }],
          { md: md || "" },
          async (out) => {
            if (!out.md || !out.md.trim()) throw new Error("빈 본문은 저장할 수 없다");
            await appendEvent({ kind: "place", key: slug },
              "prose-set-section", { section, md: out.md });
          });
        card.after(form);
        editBtn.disabled = true;
      });
      card.querySelector(".title-row").appendChild(editBtn);
      root.appendChild(card);
    }
  }
}
