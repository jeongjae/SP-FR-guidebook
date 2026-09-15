/* 30_Places 원고가 쓰는 제한된 markdown 부분집합 렌더러.
 * 지원: #~#### 제목 · 굵게 · 기울임 · 링크 · 목록 · 인용 · 표 · {{grade:...}} 뱃지.
 * 그 밖은 문단으로 취급한다. 외부 라이브러리를 쓰지 않는다. */

function esc(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function inline(s) {
  let out = esc(s);
  out = out.replace(/\{\{grade:[a-z]+\|([^}]+)\}\}/g,
    '<span class="badge">$1</span>');
  out = out.replace(/\{\{badge:[a-z]+\|([^}]+)\}\}/g,
    '<span class="badge warn">$1</span>');
  out = out.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  out = out.replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>");
  out = out.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (m, text, href) => {
    if (/^https?:\/\//.test(href)) {
      return `<a href="${href}" target="_blank" rel="noopener">${text}</a>`;
    }
    return text; // 상대 링크(../places/…)는 앱 밖 — 텍스트로 둔다
  });
  return out;
}

export function renderMd(md) {
  if (!md) return "";
  const lines = md.split("\n");
  const html = [];
  let list = null, table = null, quote = null;
  const flush = () => {
    if (list) { html.push(`<ul>${list.join("")}</ul>`); list = null; }
    if (quote) { html.push(`<blockquote>${quote.join("<br>")}</blockquote>`); quote = null; }
    if (table) {
      const rows = table.filter((r) => !/^[\s|:-]+$/.test(r));
      const cells = rows.map((r, i) => {
        const tag = i === 0 ? "th" : "td";
        const cols = r.replace(/^\||\|$/g, "").split("|").map((c) => inline(c.trim()));
        return `<tr>${cols.map((c) => `<${tag}>${c}</${tag}>`).join("")}</tr>`;
      });
      html.push(`<table>${cells.join("")}</table>`);
      table = null;
    }
  };
  for (const raw of lines) {
    const line = raw.replace(/\s+$/, "");
    if (!line.trim()) { flush(); continue; }
    const h = line.match(/^(#{1,4})\s+(.*)$/);
    if (h) { flush(); html.push(`<h${h[1].length + 1}>${inline(h[2])}</h${h[1].length + 1}>`); continue; }
    if (/^\s*[-*]\s+/.test(line)) {
      if (!list) { flush(); list = []; }
      list.push(`<li>${inline(line.replace(/^\s*[-*]\s+/, ""))}</li>`);
      continue;
    }
    if (/^>\s?/.test(line)) {
      if (!quote) { flush(); quote = []; }
      quote.push(inline(line.replace(/^>\s?/, "")));
      continue;
    }
    if (/^\|.*\|$/.test(line)) {
      if (!table) { flush(); table = []; }
      table.push(line);
      continue;
    }
    if (/^-{3,}$/.test(line)) { flush(); continue; }
    flush();
    html.push(`<p>${inline(line)}</p>`);
  }
  flush();
  return html.join("\n");
}
