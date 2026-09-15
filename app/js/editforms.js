/* 인라인 편집 폼 빌더 — 모달 없이 카드 안에서 펼친다. */
import { el, esc } from "./ui.js";

/* spec: [{name,label,type:"text"|"time"|"textarea"|"select"|"checkbox",options?,placeholder?}] */
export function buildForm(spec, initial, onSave, onCancel) {
  const form = el('<form class="card edit-form"></form>');
  for (const f of spec) {
    const v = initial[f.name];
    let inner;
    if (f.type === "textarea") {
      inner = `<textarea name="${f.name}" rows="${f.rows || 4}" placeholder="${esc(f.placeholder || "")}">${esc(v ?? "")}</textarea>`;
    } else if (f.type === "select") {
      inner = `<select name="${f.name}">${f.options.map(([val, label]) =>
        `<option value="${esc(val)}"${val === v ? " selected" : ""}>${esc(label)}</option>`).join("")}</select>`;
    } else if (f.type === "checkbox") {
      inner = `<input type="checkbox" name="${f.name}"${v ? " checked" : ""}>`;
    } else if (f.type === "time") {
      // 네이티브 시간 선택기 — 모바일 숫자 키패드로는 ':' 를 입력할 수
      // 없다. type="time" 의 값은 항상 "HH:MM" 이라 검증 형식과 같다.
      inner = `<input type="time" name="${f.name}" value="${esc(v ?? "")}" step="300">`;
    } else {
      inner = `<input type="text" name="${f.name}" value="${esc(v ?? "")}" placeholder="${esc(f.placeholder || "")}">`;
    }
    form.appendChild(el(`<label class="field">${esc(f.label)}${inner}</label>`));
  }
  const row = el(`<div class="row">
    <button type="submit" class="primary">저장</button>
    <button type="button" class="btn-cancel">취소</button></div>`);
  form.appendChild(row);
  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const out = {};
    for (const f of spec) {
      const input = form.elements[f.name];
      out[f.name] = f.type === "checkbox" ? input.checked : input.value.trim();
      if (out[f.name] === "" && f.type !== "checkbox") out[f.name] = null;
    }
    try {
      await onSave(out);
    } catch (err) {
      alert("저장 실패: " + err.message);
      return;
    }
    document.dispatchEvent(new CustomEvent("spfr:rerender"));
  });
  row.querySelector(".btn-cancel").addEventListener("click", () =>
    onCancel ? onCancel() : document.dispatchEvent(new CustomEvent("spfr:rerender")));
  return form;
}

export const TIME_RE = /^\d{2}:\d{2}$/;

export function checkTime(v, label) {
  if (v != null && !TIME_RE.test(v)) {
    throw new Error(`${label}은 HH:MM 형식 (예: 09:30)`);
  }
}

export const CATEGORY_OPTIONS = [
  ["sight", "볼거리"], ["culture", "문화·전시"], ["food", "식사"],
  ["cafe", "카페"], ["shopping", "쇼핑·시장"], ["activity", "활동"],
  ["transport", "이동"], ["hotel", "숙소"],
];
