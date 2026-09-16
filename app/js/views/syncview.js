import { eventsAll, eventDelete, metaGet, metaSet } from "../db.js";
import { pullSnapshot, exportJournal, fullSync } from "../sync.js";
import { deviceId, appendEvent } from "../events.js";
import { getToken, setToken, REPO } from "../github.js";
import { esc, el, fmtTs } from "../ui.js";
import { APP_VERSION } from "../main.js";

const OP_LABEL = {
  "note": "메모", "set-visited": "방문 체크", "check-action": "액션 처리",
  "set-booking": "예약 상태", "set-field": "스톱 수정", "set-day-meta": "하루 수정",
  "add-stop": "스톱 추가", "remove-stop": "스톱 삭제", "move-stop": "스톱 이동",
  "prose-set-section": "본문 편집",
};

export async function syncView(root) {
  const [events, version, lastPull, dev, author, token] = await Promise.all([
    eventsAll(), metaGet("snapshotVersion"), metaGet("lastPullAt"),
    deviceId(), metaGet("author", "jason"), getToken(),
  ]);
  const pending = events.filter((e) => e.status === "pending");
  const rejected = events.filter((e) => e.status === "rejected");
  root.innerHTML = "";

  const status = el(`<div class="card">
    <h2>동기화</h2>
    <p class="meta">스냅샷 ${esc((version || "없음").slice(0, 12))} · 마지막 갱신 ${lastPull ? esc(fmtTs(lastPull)) : "—"}</p>
    <p class="meta">기기 ${esc(dev)} · 편집자 <b>${esc(author)}</b> · GitHub ${token ? "연결됨 ✓" : "미연결"} · 앱 ${esc(APP_VERSION)}</p>
    ${!token && pending.length ? `<p class="tl-note" style="background:#FDECEA;border:1px solid #D9938B;border-radius:8px;padding:8px 10px;color:#7A1F1F;font-weight:700">GitHub 미연결 — 편집 ${pending.length}건이 이 폰에만 있다. 아래에 토큰을 저장하고 '지금 동기화'를 눌러야 정본·본 사이트에 반영된다.</p>` : ""}
    <div class="row">
      <button id="btn-sync" class="primary" type="button">지금 동기화</button>
      <button id="btn-pull" type="button">스냅샷만 새로 받기</button>
      <button id="btn-author" type="button">편집자 전환</button>
    </div>
    <p id="sync-result" class="meta"></p>
  </div>`);
  const say = (t) => { status.querySelector("#sync-result").textContent = t; };
  status.querySelector("#btn-sync").addEventListener("click", async (e) => {
    e.target.disabled = true;
    say("동기화 중…");
    try {
      const r = await fullSync();
      say(`push ${r.pushed} · 적용확인 ${r.applied} · 거부 ${r.rejected} · 상대편집 ${r.peers}${r.snapshot ? " · 스냅샷 갱신" : ""}`);
    } catch (err) {
      say("실패: " + err.message);
    }
    e.target.disabled = false;
    document.dispatchEvent(new CustomEvent("spfr:rerender"));
  });
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

  const settings = el(`<div class="card">
    <h2>GitHub 연결</h2>
    <p class="meta">fine-grained PAT — 저장소 <b>${esc(REPO)}</b> 만, 권한은
    Contents Read&amp;Write 만, 만료는 여행 후로. 이 폰에만 저장된다.</p>
    <label class="field">토큰
      <input id="pat" type="password" autocomplete="off"
        placeholder="${token ? "저장됨 — 바꾸려면 새로 입력" : "github_pat_…"}">
    </label>
    <div class="row">
      <button id="btn-save-pat" type="button">저장</button>
      ${token ? '<button id="btn-clear-pat" class="danger" type="button">토큰 삭제</button>' : ""}
    </div>
  </div>`);
  settings.querySelector("#btn-save-pat").addEventListener("click", async () => {
    const v = settings.querySelector("#pat").value.trim();
    if (!v) { alert("토큰을 입력한다."); return; }
    await setToken(v);
    alert("저장했다 — '지금 동기화'로 확인한다.");
    document.dispatchEvent(new CustomEvent("spfr:rerender"));
  });
  settings.querySelector("#btn-clear-pat")?.addEventListener("click", async () => {
    if (!confirm("토큰을 삭제할까?")) return;
    await setToken(null);
    document.dispatchEvent(new CustomEvent("spfr:rerender"));
  });
  root.appendChild(settings);

  if (rejected.length) {
    const rej = el(`<div class="card"><h2>거부된 편집 <span class="badge must">${rejected.length}</span></h2>
      <p class="meta">가드가 정본 반영을 거부했다 — 사유를 보고 고쳐서 재제출한다.</p>
      <div id="rej-list"></div></div>`);
    const list = rej.querySelector("#rej-list");
    for (const e of rejected) {
      const row = el(`<div class="event-row">
        <span class="status-rejected">거부</span> · ${esc(OP_LABEL[e.op] || e.op)}
        · ${esc(e.entity.kind)}:${esc(e.entity.key)}
        <span class="meta">사유: ${esc(e.rejectReason || "미기록")}</span></div>`);
      const retry = el('<button class="small" type="button">재제출</button>');
      retry.addEventListener("click", async () => {
        await appendEvent(e.entity, e.op, e.payload);
        await eventDelete(e.id);
        document.dispatchEvent(new CustomEvent("spfr:rerender"));
      });
      const drop = el('<button class="small danger" type="button">버리기</button>');
      drop.addEventListener("click", async () => {
        if (!confirm("이 편집을 완전히 버릴까?")) return;
        await eventDelete(e.id);
        document.dispatchEvent(new CustomEvent("spfr:rerender"));
      });
      row.appendChild(retry); row.appendChild(drop);
      list.appendChild(row);
    }
    root.appendChild(rej);
  }

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
        ${e.payload?.status ? "· → " + esc(e.payload.status) : ""}</span>
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
