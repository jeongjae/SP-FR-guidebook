/* 예약 현황 — 검색 · 상태 필터 · 정렬.
   서드파티 의존성 0. 카드는 서버에서 이미 다 그려져 있고, 이 파일은
   보일 것을 고르고 순서를 바꾸기만 한다. 스크립트가 없으면 도구 막대가
   hidden 인 채로 남고 28장이 전부 보인다 — 화면이 비지는 않는다. */
"use strict";

(function () {
  const tools = document.querySelector(".rz-tools");
  const list = document.querySelector(".rz-list");
  if (!tools || !list) return;

  const cards = Array.from(list.querySelectorAll(".rz-card"));
  const q = tools.querySelector("#rz-q");
  const cat = tools.querySelector("#rz-cat");
  const region = tools.querySelector("#rz-region");
  const sort = tools.querySelector("#rz-sort");
  const chips = Array.from(tools.querySelectorAll(".rz-chip"));
  const countLine = tools.querySelector(".rz-count");
  const empty = document.querySelector(".rz-empty");
  const OPEN = ["미조사", "예약대기", "재확인"];
  const PRIO = { P0: 0, P1: 1, P2: 2 };
  let status = "";

  tools.hidden = false;

  /* ---- 예약목표일 D-표기. 기기 시계로 계산한다 (빌드 시각이 아니라).
     지난 목표일은 "기한 지남"으로 못박는다 — 미확정 항목의 핵심 정보다. */
  function stampGoals() {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    for (const el of document.querySelectorAll(".rz-goal")) {
      const raw = el.dataset.goal;
      if (!raw) continue;
      const goal = new Date(raw + "T00:00:00");
      if (isNaN(goal)) continue;
      const days = Math.round((goal - today) / 86400000);
      const tag = document.createElement("b");
      if (days < 0) {
        el.classList.add("is-late");
        tag.textContent = "기한 지남";
      } else if (days === 0) {
        el.classList.add("is-late");
        tag.textContent = "오늘";
      } else {
        tag.textContent = "D-" + days;
      }
      el.appendChild(tag);
    }
  }

  function matches(card) {
    const term = q.value.trim().toLowerCase();
    if (term && !card.dataset.q.includes(term)) return false;
    if (status === "__open") {
      if (OPEN.indexOf(card.dataset.status) < 0) return false;
    } else if (status && card.dataset.status !== status) return false;
    if (cat.value && card.dataset.cat !== cat.value) return false;
    if (region.value && card.dataset.region !== region.value) return false;
    return true;
  }

  function keyOf(card) {
    if (sort.value === "date") return [card.dataset.date, card.id];
    if (sort.value === "prio") {
      const p = PRIO[card.dataset.prio];
      return [(p === undefined ? 9 : p) + "", card.dataset.date, card.id];
    }
    return [card.dataset.sortStatus, card.dataset.date, card.id];
  }

  function apply() {
    let shown = 0;
    for (const card of cards) {
      const ok = matches(card);
      card.hidden = !ok;
      if (ok) shown++;
    }
    const ordered = cards.slice().sort((a, b) => {
      const x = keyOf(a), y = keyOf(b);
      for (let i = 0; i < x.length; i++) {
        if (x[i] !== y[i]) return x[i] < y[i] ? -1 : 1;
      }
      return 0;
    });
    // DOM 순서만 다시 붙인다. appendChild 는 이동이라 노드를 새로 만들지 않는다.
    for (const card of ordered) list.appendChild(card);

    const filtered = !!(q.value.trim() || status || cat.value || region.value);
    countLine.textContent = filtered
      ? shown + "건 표시 중 · 전체 " + cards.length + "건"
      : "전체 " + cards.length + "건";
    tools.classList.toggle("is-filtered", filtered);
    if (empty) empty.hidden = shown > 0;
  }

  function reset() {
    q.value = "";
    cat.value = "";
    region.value = "";
    status = "";
    for (const c of chips) c.classList.toggle("is-on", c.dataset.status === "");
    apply();
  }

  for (const chip of chips) {
    chip.addEventListener("click", function () {
      status = chip.dataset.status;
      for (const c of chips) c.classList.toggle("is-on", c === chip);
      apply();
    });
  }
  q.addEventListener("input", apply);
  for (const sel of [cat, region, sort]) sel.addEventListener("change", apply);
  for (const btn of document.querySelectorAll(".rz-reset")) {
    btn.addEventListener("click", reset);
  }

  /* 검색 결과에서 #R014 로 들어오면 그 카드가 필터에 걸려 안 보일 수 있다.
     주소로 지목된 카드는 언제나 보여야 한다 — 필터를 풀고 표시한다. */
  function focusHash() {
    const id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    const card = document.getElementById(id);
    if (!card || !list.contains(card)) return;
    reset();
    for (const c of cards) c.classList.remove("is-target");
    card.classList.add("is-target");
    card.scrollIntoView({ block: "center" });
  }

  stampGoals();
  apply();
  focusHash();
  window.addEventListener("hashchange", focusHash);
})();
