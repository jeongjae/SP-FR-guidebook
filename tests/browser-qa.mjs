import { mkdirSync, writeFileSync } from "node:fs";

const port = process.env.CDP_PORT || "9334";
const base = `http://127.0.0.1:${port}`;
const site = process.env.QA_SITE || "http://127.0.0.1:8765";
const output = process.env.QA_OUTPUT || "C:/Users/NB-24021500/AppData/Local/Temp/spfr-map-qa";
const prefix = process.env.QA_PREFIX || "edge";
mkdirSync(output, { recursive: true });

function assert(value, message) {
  if (!value) throw new Error(message);
}

async function target(path) {
  const info = await fetch(`${base}/json/new?${encodeURIComponent(site + "/" + path)}`, { method: "PUT" }).then((r) => r.json());
  const socket = new WebSocket(info.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    socket.addEventListener("open", resolve, { once: true });
    socket.addEventListener("error", reject, { once: true });
  });
  let id = 0;
  const pending = new Map();
  const events = new Map();
  const diagnostics = [];
  socket.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);
    if (message.id && pending.has(message.id)) {
      const { resolve, reject } = pending.get(message.id);
      pending.delete(message.id);
      if (message.error) reject(new Error(message.error.message)); else resolve(message.result);
    }
    if (message.method === "Runtime.exceptionThrown") diagnostics.push("exception: " + message.params.exceptionDetails.text);
    if (message.method === "Log.entryAdded" && message.params.entry.level === "error") diagnostics.push("console: " + message.params.entry.text);
    const listeners = events.get(message.method) || [];
    listeners.splice(0).forEach((resolve) => resolve(message.params));
  });
  function send(method, params = {}) {
    const call = ++id;
    socket.send(JSON.stringify({ id: call, method, params }));
    return new Promise((resolve, reject) => pending.set(call, { resolve, reject }));
  }
  function once(method) {
    return new Promise((resolve) => events.set(method, [...(events.get(method) || []), resolve]));
  }
  async function evaluate(expression) {
    const result = await send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
    if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
    return result.result.value;
  }
  await Promise.all([send("Page.enable"), send("Runtime.enable"), send("Log.enable")]);
  return { info, socket, send, once, evaluate, diagnostics };
}

async function loadPage(path, viewport) {
  const page = await target(path);
  await page.send("Network.enable");
  await page.send("Network.setCacheDisabled", { cacheDisabled: true });
  await page.send("Network.setBypassServiceWorker", { bypass: true });
  await page.send("Emulation.setDeviceMetricsOverride", {
    width: viewport.width, height: viewport.height, deviceScaleFactor: 1,
    mobile: viewport.width < 600
  });
  const loaded = page.once("Page.loadEventFired");
  await page.send("Page.navigate", { url: site + "/" + path });
  await loaded;
  await new Promise((resolve) => setTimeout(resolve, 500));
  return page;
}

async function screenshot(page, name) {
  const result = await page.send("Page.captureScreenshot", { format: "png", fromSurface: true });
  writeFileSync(`${output}/${name}`, Buffer.from(result.data, "base64"));
}

async function auditDaily(path, viewport, name, expectedCards, filter, expectedVisible) {
  const page = await loadPage(path, viewport);
  const initial = await page.evaluate(`({
    cards: document.querySelectorAll('.gm-place-card').length,
    fallback: document.querySelectorAll('.day-card-archive').length,
    route: document.querySelector('.gm-route-all')?.href || ''
  })`);
  assert(initial.cards === expectedCards, `${path}: card count ${initial.cards}`);
  assert(initial.fallback === 1, `${path}: fallback missing`);
  const state = await page.evaluate(`(() => {
    document.querySelector('.gm-filter[data-type="${filter}"]').click();
    const visible = [...document.querySelectorAll('.gm-place-card')].filter((node) => !node.hidden);
    visible[0].querySelector('.gm-card-main').click();
    document.querySelector('.gm-map-disclosure').open = true;
    document.querySelector('.gm-map-disclosure').dispatchEvent(new Event('toggle'));
    document.querySelector('.daily-map-section').scrollIntoView();
    return { visible: visible.length, pressed: visible[0].querySelector('.gm-card-main').getAttribute('aria-pressed') };
  })()`);
  assert(state.visible === expectedVisible, `${path}: visible count ${state.visible}`);
  assert(state.pressed === "true", `${path}: list selection did not activate`);
  await new Promise((resolve) => setTimeout(resolve, 500));
  const status = await page.evaluate(`document.querySelector('.gm-status').dataset.state`);
  assert(status === "error", `${path}: missing-key fallback state ${status}`);
  await screenshot(page, `${prefix}-${name}`);
  assert(page.diagnostics.length === 0, `${path}: ${page.diagnostics.join("; ")}`);
  await fetch(`${base}/json/close/${page.info.id}`);
  return { path, cards: initial.cards, visibleAfterFilter: state.visible, route: initial.route, fallbackState: status };
}

const results = [];
results.push(await auditDaily("daily/day-02.html", { width: 390, height: 844 }, "day-02-mobile.png", 3, "attraction", 2));
results.push(await auditDaily("daily/day-06.html", { width: 1440, height: 1000 }, "day-06-desktop.png", 9, "parking", 4));

const region = await loadPage("maps/barcelona.html", { width: 1440, height: 1000 });
const regionCards = await region.evaluate(`document.querySelectorAll('.gm-place-card').length`);
assert(regionCards === 8, `Barcelona region card count ${regionCards}`);
const initialRegionState = await region.evaluate(`({
  status: document.querySelector('.gm-status').dataset.state,
  listWidth: document.querySelector('.gm-place-list').getBoundingClientRect().width
})`);
assert(initialRegionState.status === "idle", `Barcelona region loaded before disclosure`);
assert(initialRegionState.listWidth > 650, `Barcelona closed list width ${initialRegionState.listWidth}`);
await region.evaluate(`(() => {
  const details = document.querySelector('.gm-map-disclosure');
  details.open = true;
  details.dispatchEvent(new Event('toggle'));
  document.querySelector('.gm-component').scrollIntoView();
})()`);
await new Promise((resolve) => setTimeout(resolve, 500));
const regionFallback = await region.evaluate(`document.querySelector('.gm-status').dataset.state`);
assert(regionFallback === "error", `Barcelona missing-key fallback ${regionFallback}`);
await screenshot(region, `${prefix}-barcelona-region-desktop.png`);
assert(region.diagnostics.length === 0, region.diagnostics.join("; "));
await fetch(`${base}/json/close/${region.info.id}`);
results.push({ path: "maps/barcelona.html", cards: regionCards, fallbackState: regionFallback });

const reference = await loadPage("daily/day-01.html", { width: 390, height: 844 });
await reference.evaluate(`document.querySelector('.daily-map-section').scrollIntoView()`);
await screenshot(reference, `${prefix}-legacy-reference-day-01.png`);
await fetch(`${base}/json/close/${reference.info.id}`);

async function responsiveAudit(path, viewport, name) {
  const page = await loadPage(path, viewport);
  const metrics = await page.evaluate(`(() => {
    document.querySelector('.gm-component').scrollIntoView();
    const targets = [...document.querySelectorAll('.gm-filter, .gm-action, .gm-card-actions a, .gm-map-disclosure > summary')];
    return {
      overflow: document.documentElement.scrollWidth - window.innerWidth,
      minTarget: Math.min(...targets.map((node) => node.getBoundingClientRect().height))
    };
  })()`);
  assert(metrics.overflow <= 1, `${path} ${viewport.width}px horizontal overflow ${metrics.overflow}`);
  assert(metrics.minTarget >= 43.5, `${path} ${viewport.width}px target ${metrics.minTarget}`);
  await screenshot(page, `${prefix}-${name}`);
  await fetch(`${base}/json/close/${page.info.id}`);
  return { path, viewport: viewport.width, ...metrics };
}

results.push(await responsiveAudit("daily/day-06.html", { width: 375, height: 812 }, "day-06-375.png"));
results.push(await responsiveAudit("maps/girona.html", { width: 768, height: 900 }, "girona-region-768.png"));

console.log(JSON.stringify({ results, output }, null, 2));
