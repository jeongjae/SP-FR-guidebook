/* 편집 이벤트 — append-only 저널의 원자. 스냅샷은 절대 변형하지 않고
 * 이 이벤트들을 겹쳐(materialize) 화면을 만든다.
 *
 * P1 에서 쓰는 op:
 *   note           entity(stop|day|place|booking)  payload{text}
 *   set-visited    entity stop                     payload{value}
 *   check-action   entity stop                     payload{label, checked}
 *   set-booking    entity booking(R0xx|stay:<key>) payload{status, note?}
 * (구조 편집 op 는 P3 에서 추가)
 */
import { eventPut, metaGet, metaSet } from "./db.js";

const B32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"; // Crockford

export function ulid(now = Date.now()) {
  let ts = "";
  let t = now;
  for (let i = 0; i < 10; i++) { ts = B32[t % 32] + ts; t = Math.floor(t / 32); }
  const rand = crypto.getRandomValues(new Uint8Array(16));
  let rs = "";
  for (let i = 0; i < 16; i++) rs += B32[rand[i] % 32];
  return ts + rs;
}

export async function deviceId() {
  let id = await metaGet("deviceId");
  if (!id) {
    id = "dev-" + ulid().slice(-8).toLowerCase();
    await metaSet("deviceId", id);
  }
  return id;
}

export async function author() {
  return metaGet("author", "jason");
}

export async function appendEvent(entity, op, payload) {
  const seq = ((await metaGet("seq", 0)) | 0) + 1;
  await metaSet("seq", seq);
  const event = {
    id: ulid(),
    deviceId: await deviceId(),
    author: await author(),
    ts: new Date().toISOString(),
    seq,
    entity,
    op,
    payload,
    status: "pending",
  };
  await eventPut(event);
  document.dispatchEvent(new CustomEvent("spfr:event-appended"));
  return event;
}

export const stopKey = (dayN, stopId) => `day-${String(dayN).padStart(2, "0")}/${stopId}`;
