/* GitHub Contents API — 기기 저널 push 와 상태 pull.
 * fine-grained PAT (이 저장소만·Contents R/W)를 meta 에 보관한다.
 * 기기마다 자기 저널 파일 하나만 쓴다 — SHA 경합이 구조적으로 없다. */
import { metaGet, metaSet } from "./db.js";

export const REPO = "jeongjae/SP-FR-guidebook";
const API = `https://api.github.com/repos/${REPO}/contents/`;

export async function getToken() { return metaGet("patToken"); }
export async function setToken(t) { await metaSet("patToken", t || null); }

function b64encodeUtf8(text) {
  const bytes = new TextEncoder().encode(text);
  let bin = "";
  for (let i = 0; i < bytes.length; i += 0x8000) {
    bin += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  }
  return btoa(bin);
}

function b64decodeUtf8(b64) {
  const bin = atob(b64.replace(/\n/g, ""));
  const bytes = Uint8Array.from(bin, (c) => c.charCodeAt(0));
  return new TextDecoder().decode(bytes);
}

async function api(path, options = {}) {
  const token = await getToken();
  const headers = {
    Accept: "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    ...(options.headers || {}),
  };
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(API + path, { ...options, headers });
  if (res.status === 404) return null;
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`GitHub ${res.status}: ${body.slice(0, 140)}`);
  }
  return res.json();
}

export async function readFile(path) {
  const data = await api(path);
  if (!data) return null;
  return { sha: data.sha, text: b64decodeUtf8(data.content) };
}

export async function writeFile(path, text, message, sha) {
  const body = { message, content: b64encodeUtf8(text) };
  if (sha) body.sha = sha;
  return api(path, { method: "PUT", body: JSON.stringify(body) });
}

/* pending 이벤트를 자기 저널에 append. 같은 기기끼리만 경합하므로
 * 409 는 재시도 한 번이면 충분하다. */
export async function pushJournal(deviceId, events) {
  if (!events.length) return { pushed: 0 };
  const path = `data/field-edits/journal-${deviceId}.ndjson`;
  const lines = events.map((e) => JSON.stringify({ ...e, status: undefined }))
    .join("\n") + "\n";
  for (let attempt = 0; attempt < 2; attempt++) {
    const existing = await readFile(path);
    const text = (existing ? existing.text : "") + lines;
    try {
      await writeFile(path, text,
        `[app] ${deviceId} field edits +${events.length}`, existing?.sha);
      return { pushed: events.length };
    } catch (err) {
      if (attempt === 0 && /GitHub 409/.test(err.message)) continue;
      throw err;
    }
  }
  throw new Error("push 재시도 실패");
}

/* CI 소유 상태 — 커서·거부 목록. PAT 이 있으면 API(항상 최신),
 * 없으면 raw(캐시 ~5분) 로 읽는다. */
export async function fetchState() {
  const token = await getToken();
  if (token) {
    const file = await readFile("data/field-edits/state.json");
    return file ? JSON.parse(file.text) : null;
  }
  const res = await fetch(
    `https://raw.githubusercontent.com/${REPO}/main/data/field-edits/state.json`,
    { cache: "no-cache" });
  return res.ok ? res.json() : null;
}

/* 상대 기기 저널 — 커서 이후 이벤트만 미러해 수 초 내 상호 가시성. */
export async function fetchPeerEvents(ownDeviceId, cursors) {
  const dir = await api("data/field-edits");
  if (!dir) return [];
  const peers = dir.filter((f) => f.name.startsWith("journal-")
    && f.name.endsWith(".ndjson")
    && f.name !== `journal-${ownDeviceId}.ndjson`);
  const events = [];
  for (const f of peers) {
    const device = f.name.slice("journal-".length, -".ndjson".length);
    const file = await readFile(`data/field-edits/${f.name}`);
    if (!file) continue;
    const cursor = cursors?.[device] || "";
    for (const line of file.text.split("\n")) {
      if (!line.trim()) continue;
      try {
        const e = JSON.parse(line);
        if ((e.id || "") > cursor) events.push({ ...e, deviceId: device, status: "peer" });
      } catch { /* skip broken line */ }
    }
  }
  return events;
}
