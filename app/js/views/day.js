import { loadDay, loadTrip } from "../state.js";
import { appendEvent, stopKey } from "../events.js";
import { esc, el, badgeFor, stripGrade, notesHtml, noteButton } from "../ui.js";
import { buildForm, checkTime, CATEGORY_OPTIONS } from "../editforms.js";

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
  const dayKey = `day-${String(n).padStart(2, "0")}`;
  const navRow = head.querySelector(".nav-row");
  navRow.appendChild(noteButton({ kind: "day", key: dayKey }, "이날 메모"));
  const editDayBtn = el('<button class="small" type="button">✎ 하루 수정</button>');
  editDayBtn.addEventListener("click", () => {
    const form = buildForm([
      { name: "title", label: "제목", type: "text" },
      { name: "startTime", label: "시작 (HH:MM)", type: "time" },
      { name: "endTime", label: "끝 (HH:MM)", type: "time" },
      { name: "fatigue", label: "피로도", type: "select",
        options: [["1","1"],["2","2"],["3","3"],["4","4"],["5","5"]] },
      { name: "backup", label: "Plan B", type: "textarea" },
    ], day, async (out) => {
      checkTime(out.startTime, "시작"); checkTime(out.endTime, "끝");
      for (const f of ["title", "startTime", "endTime", "fatigue", "backup"]) {
        const before = day[f] == null ? null : String(day[f]);
        if (out[f] != null && out[f] !== before) {
          await appendEvent({ kind: "day", key: dayKey }, "set-day-meta",
            { field: f, value: out[f] });
        }
      }
    });
    head.after(form);
    editDayBtn.disabled = true;
  });
  navRow.appendChild(editDayBtn);
  const addStopBtn = el('<button class="small" type="button">＋ 스톱 추가</button>');
  addStopBtn.addEventListener("click", () => {
    const anchors = [["", "맨 뒤에"], ...day.stops.map((s) => [s.id, `'${stripGrade(s.name).slice(0, 24)}' 뒤에`])];
    const form = buildForm([
      { name: "name", label: "이름 (필수)", type: "text", placeholder: "예: 젤라토 휴식" },
      { name: "category", label: "분류", type: "select", options: CATEGORY_OPTIONS },
      { name: "start", label: "시작 (HH:MM)", type: "time" },
      { name: "end", label: "끝 (HH:MM)", type: "time" },
      { name: "summary", label: "설명", type: "textarea", rows: 2 },
      { name: "afterStopId", label: "위치", type: "select", options: anchors },
      { name: "optional", label: "선택 일정", type: "checkbox" },
    ], { category: "sight", afterStopId: "" }, async (out) => {
      if (!out.name) throw new Error("이름은 필수다");
      checkTime(out.start, "시작"); checkTime(out.end, "끝");
      const sid = "fe-" + out.name.toLowerCase().replace(/[^a-z0-9]+/g, "-")
        .replace(/^-+|-+$/g, "").slice(0, 24) || "fe-stop";
      const unique = day.stops.some((s) => s.id === sid) ? sid + "-2" : sid;
      await appendEvent({ kind: "day", key: dayKey }, "add-stop", {
        stop: { id: unique, name: out.name, category: out.category,
          start: out.start, end: out.end, summary: out.summary || "",
          optional: !!out.optional },
        afterStopId: out.afterStopId || null,
      });
    });
    head.after(form);
    addStopBtn.disabled = true;
  });
  navRow.appendChild(addStopBtn);
  root.appendChild(head);

  const legByFrom = new Map((day.legs || []).map((l) => [l.from, l]));
  const timeline = el('<div class="card"><h3>시간표</h3></div>');
  for (const stop of day.stops) {
    timeline.appendChild(renderStop(n, stop, day));
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

function renderStop(n, stop, day) {
  const sk = stopKey(n, stop.id);
  const node = el(`<div class="stop${stop.visited ? " visited" : ""}${stop.localEdit ? " local-edit" : ""}" data-stop="${esc(stop.id)}">
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

  // ---- 구조 편집: 수정 · 이동 · 삭제 --------------------------------
  const editBtn = el('<button class="small" type="button">✎ 수정</button>');
  editBtn.addEventListener("click", () => {
    const form = buildForm([
      { name: "name", label: "이름", type: "text" },
      { name: "start", label: "시작 (HH:MM)", type: "time" },
      { name: "end", label: "끝 (HH:MM)", type: "time" },
      { name: "summary", label: "설명", type: "textarea" },
      { name: "menu", label: "식사·메뉴", type: "text" },
      { name: "reservation", label: "예약·주차 메모", type: "text" },
      { name: "optional", label: "선택 일정", type: "checkbox" },
    ], stop, async (out) => {
      checkTime(out.start, "시작"); checkTime(out.end, "끝");
      if (!out.name) throw new Error("이름은 필수다");
      for (const f of ["name", "start", "end", "summary", "menu", "reservation", "optional"]) {
        const before = stop[f] ?? null;
        const after = f === "optional" ? !!out[f] : out[f];
        if (JSON.stringify(after) !== JSON.stringify(before)) {
          await appendEvent({ kind: "stop", key: sk }, "set-field",
            { field: f, value: after });
        }
      }
    });
    node.after(form);
    editBtn.disabled = true;
  });
  btns.appendChild(editBtn);

  const idx = day.stops.findIndex((s) => s.id === stop.id);
  if (idx > 0) {
    const up = el('<button class="small" type="button">↑</button>');
    up.addEventListener("click", async () => {
      await appendEvent({ kind: "stop", key: sk }, "move-stop",
        { afterStopId: idx >= 2 ? day.stops[idx - 2].id : null });
      document.dispatchEvent(new CustomEvent("spfr:rerender"));
    });
    btns.appendChild(up);
  }
  if (idx >= 0 && idx < day.stops.length - 1) {
    const down = el('<button class="small" type="button">↓</button>');
    down.addEventListener("click", async () => {
      await appendEvent({ kind: "stop", key: sk }, "move-stop",
        { afterStopId: day.stops[idx + 1].id });
      document.dispatchEvent(new CustomEvent("spfr:rerender"));
    });
    btns.appendChild(down);
  }
  const rm = el('<button class="small danger" type="button">삭제</button>');
  rm.addEventListener("click", async () => {
    if (!confirm(`'${stripGrade(stop.name)}' 스톱을 삭제할까? (정본 반영 전까지 되돌릴 수 있다)`)) return;
    await appendEvent({ kind: "stop", key: sk }, "remove-stop", {});
    document.dispatchEvent(new CustomEvent("spfr:rerender"));
  });
  btns.appendChild(rm);
  return node;
}

export async function dayView(root, params) {
  const n = parseInt(params[0], 10);
  root.innerHTML = "";
  await renderDayInto(root, n);
}
