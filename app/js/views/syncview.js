import { eventsAll, eventDelete, metaGet, metaSet } from "../db.js";
import { pullSnapshot, exportJournal } from "../sync.js";
import { deviceId } from "../events.js";
import { esc, el, fmtTs } from "../ui.js";

const OP_LABEL = {
  "note": "메모", "set-visited": "방문 체크", "check-action": "액션 처리",
  "set-booking": "예약 상태",
};

export async function syncView(root) {
  const [events, version, lastPull, dev, author] = await Promise.all([
    eventsAll(), metaGet("snapshotVersion"), metaGet("lastPullAt"),
    deviceId(), metaGet("author", "jason"),
  ]);
  const pending = events.filter((e) => e.status === "pending");
  root.innerHTML = "";

  const status = el(`<div class="card">
    <h2>동기화</h2>
    <p class="meta">스냅샷 ${esc((version || "없음").slice(0, 12))} · 마지막 갱신 ${lastPull ? esc(fmtTs(lastPull)) : "—"}</p>
    <p class="meta">기기 ${esc(dev)} · 편집자 <b>${esc(author)}</b></p>
    <div class="row">
      <button id="btn-pull" class="primary" type="button">스냅샷 새로 받기</button>
      <button id="btn-author" type="button">편집자 전환</button>
    </div>
    <p class="meta">GitHub 자동 반영(P2)은 준비 중이다 — 지금은 아래 내보내기로
    편집 내역을 복사해 데스크톱 세션에 전달한다.</p>
  </div>`);
  status.querySelector("#btn-pull").addEventListener("click", async (e) => {
    e.target.disabled = true;
    try {
      const r = await pullSnapshot({ force: true });
      alert(`갱신 완료 — 버전 ${r.version.slice(0, 12)}`);
    } catch (err) {
      alert("갱신 실패 — 온라인 상태를 확인한다: " + err.message);
    }
    document.dispatchEvent(new CustomEvent("spfr:rerender"));
  });
  status.querySelector("#btn-author").addEventListener("click", async () => {
    const next = (await metaGet("author", "jason")) === "jason" ? "julia" : "jason";
    await metaSet("author", next);
    document.dispatchEvent(new CustomEvent("spfr:rerender"));
  });
  root.appendChild(status);

  const journal = el(`<div class="card">
    <h2>편집 내역 <span class="badge warn">대기 ${pending.length}</span></h2>
    <div class="row">
      <button id="btn-export" type="button">대기분 복사 (NDJSON)</button>
    </div>
    <div id="event-list"></div>
  </div>`);
  journal.querySelector("#btn-export").addEventListener("click", async () => {
    const text = await exportJournal();
    if (!text) { alert("대기 중인 편집이 없다."); return; }
    try {
      await navigator.clipboard.writeText(text);
      alert(`${pending.length}건을 클립보드에 복사했다.`);
    } catch {
      prompt("복사가 막혔다 — 직접 선택해 복사한다:", text);
    }
  });
  const list = journal.querySelector("#event-list");
  if (!events.length) {
    list.innerHTML = '<p class="empty">아직 편집이 없다.</p>';
  }
  for (const e of [...events].reverse().slice(0, 100)) {
    const row = el(`<div class="event-row">
      <span class="status-${esc(e.status)}">${esc(e.status)}</span>
      · ${esc(OP_LABEL[e.op] || e.op)} · ${esc(e.entity.kind)}:${esc(e.entity.key)}
      <span class="meta">${esc(e.author)} · ${esc(fmtTs(e.ts))}
        ${e.payload?.text ? "· " + esc(e.payload.text.slice(0, 60)) : ""}
        ${e.payload?.status ? "· → " + esc(e.payload.status) : ""}
        ${e.rejectReason ? "· 사유: " + esc(e.rejectReason) : ""}</span>
    </div>`);
    if (e.status === "pending") {
      const undo = el('<button class="small danger" type="button">되돌리기</button>');
      undo.addEventListener("click", async () => {
        if (!confirm("이 편집을 삭제할까?")) return;
        await eventDelete(e.id);
        document.dispatchEvent(new CustomEvent("spfr:rerender"));
      });
      row.appendChild(undo);
    }
    list.appendChild(row);
  }
  root.appendChild(journal);
}
