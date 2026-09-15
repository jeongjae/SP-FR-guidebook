import { loadBookings } from "../state.js";
import { appendEvent } from "../events.js";
import { esc, el, notesHtml, noteButton } from "../ui.js";

/* 상태 어휘는 트래커와 같다 — 확정 / 미예약 / 제외 (+ 예약완료·재확인·미정 계열).
 * 로컬 변경은 set-booking 이벤트로 겹친다 (P2 에서 정본 반영). */
const NEXT = { "미예약": "확정", "재확인": "확정", "미정": "확정" };

function statusBadge(status) {
  const cls = /확정|예약완료/.test(status) ? "ok" : /제외/.test(status) ? "opt" : "warn";
  return `<span class="badge ${cls}">${esc(status)}</span>`;
}

function fmtDate(v) {
  if (!v) return "";
  return String(v).slice(0, 10);
}

export async function bookingsView(root) {
  const data = await loadBookings();
  if (!data) { root.innerHTML = '<p class="empty">스냅샷이 아직 없다.</p>'; return; }
  root.innerHTML = "";

  const stays = el('<div class="card"><h2>숙소</h2></div>');
  for (const a of data.accommodations) {
    const effective = a.effectiveStatus || a.localStatus || a.status;
    const row = el(`<div class="stop">
      <div class="title-row"><div class="name">${esc(a.base)} · ${esc(String(a.nights))}박</div>${statusBadge(effective)}</div>
      <div class="summary">${esc(fmtDate(a.checkIn))} → ${esc(fmtDate(a.checkOut))}${a.address ? " · " + esc(a.address) : ""}</div>
      ${a.localStatus ? `<div class="summary">✎ 로컬 변경: ${esc(a.localStatus)}${a.localNote ? " — " + esc(a.localNote) : ""}</div>`
        : a.syncedStatus ? `<div class="summary">☁ 반영됨: ${esc(a.syncedStatus)}${a.syncedNote ? " — " + esc(a.syncedNote) : ""}</div>` : ""}
      <div class="notes">${notesHtml(a.notes)}</div>
      <div class="row btns"></div>
    </div>`);
    row.querySelector(".btns").appendChild(noteButton({ kind: "booking", key: `stay:${a.base}` }));
    stays.appendChild(row);
  }
  root.appendChild(stays);

  const res = el('<div class="card"><h2>예약</h2></div>');
  const rows = [...data.reservations].sort((x, y) => String(x.date || "9999").localeCompare(String(y.date || "9999")));
  for (const r of rows) {
    if ((r.effectiveStatus || r.status) === "제외") continue;
    const effective = r.effectiveStatus || r.localStatus || r.status;
    const row = el(`<div class="stop">
      <div class="title-row"><div class="name">${esc(r.name)}</div>${statusBadge(effective)}</div>
      <div class="summary">${esc(fmtDate(r.date))}${r.time ? " · " + esc(String(r.time)) : ""}${r.category ? " · " + esc(r.category) : ""}</div>
      ${r.localStatus ? `<div class="summary">✎ 로컬 변경: ${esc(r.localStatus)}${r.localNote ? " — " + esc(r.localNote) : ""}</div>`
        : r.syncedStatus ? `<div class="summary">☁ 반영됨: ${esc(r.syncedStatus)}${r.syncedNote ? " — " + esc(r.syncedNote) : ""}</div>` : ""}
      <div class="notes">${notesHtml(r.notes)}</div>
      <div class="row btns"></div>
    </div>`);
    const btns = row.querySelector(".btns");
    const next = NEXT[effective];
    if (next) {
      const btn = el(`<button class="small" type="button">${esc(next)}으로 표시</button>`);
      btn.addEventListener("click", async () => {
        const note = prompt("예약번호·시각 등 메모 (선택)") || "";
        await appendEvent({ kind: "booking", key: r.id }, "set-booking",
          { status: next, note: note.trim() || undefined });
        document.dispatchEvent(new CustomEvent("spfr:rerender"));
      });
      btns.appendChild(btn);
    } else if (r.localStatus) {
      const btn = el('<button class="small" type="button">로컬 변경 취소</button>');
      btn.addEventListener("click", async () => {
        await appendEvent({ kind: "booking", key: r.id }, "set-booking",
          { status: r.status });
        document.dispatchEvent(new CustomEvent("spfr:rerender"));
      });
      btns.appendChild(btn);
    }
    btns.appendChild(noteButton({ kind: "booking", key: r.id }));
    res.appendChild(row);
  }
  root.appendChild(res);
}
