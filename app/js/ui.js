/* 작은 DOM 도우미와 공용 위젯. */
import { appendEvent } from "./events.js";

export function esc(s) {
  return String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

export function el(html) {
  const t = document.createElement("template");
  t.innerHTML = html.trim();
  return t.content.firstElementChild;
}

export function fmtTs(iso) {
  const d = new Date(iso);
  return `${d.getMonth() + 1}.${d.getDate()} ${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}

export function badgeFor(name) {
  if (/^MUST/.test(name)) return '<span class="badge must">MUST</span>';
  if (/^RECOMMENDED/.test(name)) return '<span class="badge ok">추천</span>';
  if (/^OPTIONAL/.test(name)) return '<span class="badge opt">선택</span>';
  return "";
}

export function stripGrade(name) {
  return name.replace(/^(MUST|RECOMMENDED|OPTIONAL)\s*·\s*/, "");
}

export function notesHtml(notes) {
  return (notes || []).map((n) =>
    `<div class="note-item">${esc(n.text)}<span class="meta">${esc(n.author)} · ${fmtTs(n.ts)}</span></div>`
  ).join("");
}

/* 메모 추가 버튼 + 프롬프트. entity = {kind, key}. */
export function noteButton(entity, label = "메모") {
  const btn = el(`<button class="small" type="button">✎ ${label}</button>`);
  btn.addEventListener("click", async () => {
    const text = prompt("메모를 입력하세요");
    if (!text || !text.trim()) return;
    await appendEvent(entity, "note", { text: text.trim() });
    document.dispatchEvent(new CustomEvent("spfr:rerender"));
  });
  return btn;
}
