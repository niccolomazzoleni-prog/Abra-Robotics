// One prompt coding · motore della dashboard (interattiva e ?regia=1).
// Tutto lo stato visibile è funzione del tempo (performance.now): regge anche se il frame rate cala.
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { SCENARI, BANCO } from "./scenari.js";
import { cellaPallet, cellaCnc, materiali } from "./cell.js";
import { costruisci } from "./interprete.js";
const CALL = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ22FrpPdyPVRihi4eXPQlljTcG2toa8XF2d8W-QX-L9cKMaXqozq_YsHym56LEdTs9WsnqlTHeF";

const $ = (s) => document.querySelector(s);
const qs = new URLSearchParams(location.search);
const REGIA = qs.get("regia") === "1";
if (REGIA) document.body.classList.add("regia");
const now = () => performance.now() / 1000;
const clamp01 = (u) => Math.max(0, Math.min(1, u));
const ease = (u) => { u = clamp01(u); return u * u * (3 - 2 * u); };
const num = (v, d = 1) => v.toFixed(d).replace(".", ",");
const usd = (v) => (v === 0 ? "0 $" : v < 0.01 ? num(v, 3) + " $" : num(v, 2) + " $");
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// ---------------------------------------------------------------- 3D
const canvas = $("#c3d"), vp = $("#vp");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance" });
renderer.setPixelRatio(Math.min(devicePixelRatio || 1, REGIA ? 1 : 1.75));
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0e0f10);
scene.fog = new THREE.Fog(0x0e0f10, 9, 22);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.55;
const camera = new THREE.PerspectiveCamera(36, 1, 0.05, 80);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true; controls.dampingFactor = 0.08; controls.maxPolarAngle = 1.5; controls.minDistance = 1.2; controls.maxDistance = 12;
controls.enabled = !REGIA;
let userCam = false;
controls.addEventListener("start", () => { userCam = true; });

const world = new THREE.Group(); world.rotation.x = -Math.PI / 2; scene.add(world); // celle in Z alto
const grid = new THREE.GridHelper(40, 80, 0x2a2e33, 0x1a1d20); grid.position.y = -0.002; scene.add(grid);
const under = new THREE.Mesh(new THREE.PlaneGeometry(60, 60), new THREE.MeshStandardMaterial({ color: 0x111315, roughness: 1 }));
under.rotation.x = -Math.PI / 2; under.position.y = -0.004; under.receiveShadow = true; scene.add(under);
scene.add(new THREE.HemisphereLight(0xdfe6ee, 0x1b1d20, 0.55));
const sun = new THREE.DirectionalLight(0xfff4e2, 1.7);
sun.position.set(3.5, 7, 4); sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -4.5, right: 4.5, top: 4.5, bottom: -4.5, near: 1, far: 20 });
sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.02; scene.add(sun, sun.target);
const fill = new THREE.DirectionalLight(0xc8d8ff, 0.5); fill.position.set(-5, 3, -3); scene.add(fill);

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(256, 256), 0.24, 0.4, 0.97);
composer.addPass(bloom); composer.addPass(new OutputPass());

function resize() {
  const w = vp.clientWidth || 640, h = vp.clientHeight || 360;
  renderer.setSize(w, h, false); composer.setSize(w, h); camera.aspect = w / h; camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(vp); resize();

// ---------------------------------------------------------------- costruzione pezzo per pezzo
const SIGNAL = new THREE.Color(0xf2c200);
const edgeCache = new Map();
function prepItems(cell) {
  const out = [];
  for (const it of cell.items) {
    const meshes = it.meshes || []; if (it.obj) it.obj.traverse((o) => { if (o.isMesh) meshes.push(o); });
    const lm = new THREE.LineBasicMaterial({ color: SIGNAL, transparent: true, opacity: 0, depthWrite: false, toneMapped: false });
    const mm = new Map(), rec = [];
    for (const mesh of meshes) {
      const src = mesh.material;
      if (!mm.has(src)) { const c = src.clone(); c.userData.op = src.opacity ?? 1; c.userData.tr = src.transparent; mm.set(src, c); }
      mesh.material = mm.get(src);
      let e = null;
      const g = mesh.geometry, n = g.attributes.position.count;
      if (!mesh.isInstancedMesh && n < 40000 && !qs.get("noedge")) {
        let eg = edgeCache.get(g.uuid); if (!eg) { eg = new THREE.EdgesGeometry(g, 28); edgeCache.set(g.uuid, eg); }
        e = new THREE.LineSegments(eg, lm); e.raycast = () => {}; mesh.add(e);
      }
      rec.push({ mesh, e });
    }
    out.push({ label: it.label, mats: [...mm.values()], lm, rec, phase: -1 });
  }
  return out;
}
function setItem(it, t0, t) { // 0..0.5 filo · 0.5..1 solido
  const u = (t - t0) / 1.25;
  const ph = u < 0 ? 0 : u < 0.45 ? 1 : u < 1 ? 2 : 3;
  if (ph === 3 && it.phase === 3) return;
  if (ph === 0 && it.phase === 0) return;
  if (ph === 0) { it.mats.forEach((m) => (m.visible = false)); it.lm.opacity = 0; it.rec.forEach((r) => r.e && (r.e.visible = false)); }
  else if (ph === 1) {
    it.mats.forEach((m) => (m.visible = false));
    it.rec.forEach((r) => r.e && (r.e.visible = true));
    it.lm.opacity = 0.95 * ease(u / 0.2);
  } else if (ph === 2) {
    const v = ease((u - 0.45) / 0.55);
    it.mats.forEach((m) => { m.visible = true; if (!m.transparent) { m.transparent = true; m.needsUpdate = true; } m.opacity = v * m.userData.op; });
    it.rec.forEach((r) => r.e && (r.e.visible = true)); it.lm.opacity = 0.95 * (1 - v) + 0.08;
  } else {
    it.mats.forEach((m) => { m.visible = true; m.opacity = m.userData.op; if (m.transparent !== m.userData.tr) { m.transparent = m.userData.tr; m.needsUpdate = true; } });
    it.rec.forEach((r) => r.e && (r.e.visible = false));
  }
  it.phase = ph;
}

// ---------------------------------------------------------------- URScript per la cella CNC (dai punti del piano)
const PAR_CNC_RIF = { d: 50, Lp: 120, mat: "acciaio", massa: 1.8498, rate: 40, forza: 55 };
function scriptCnc(cell, par = PAR_CNC_RIF) {
  const dTxt = num(par.d, par.d % 1 ? 1 : 0).replace(",", "."), lTxt = num(par.Lp, par.Lp % 1 ? 1 : 0).replace(",", ".");
  const presa = Math.min(85, Math.max(5, Math.round(par.d - 4)));
  const inv = cell.kin.base.clone().multiply(new THREE.Matrix4().makeRotationZ(Math.PI)).invert(); // frame "base" di URScript
  const P = ([x, y, z]) => { const v = new THREE.Vector3(x, y, z).applyMatrix4(inv); return `p[${v.x.toFixed(4)}, ${v.y.toFixed(4)}, ${v.z.toFixed(4)}, 0.0000, 3.1416, 0.0000]`; };
  const up = ([x, y, z], d = 0.12) => [x, y, z + d];
  const L = [
    "def gemello_asservimento_cnc():",
    "  # generato da gemello: UR10e + Robotiq 2F-85, cella m_ur10e_cnc (CM-18), porta automatica e morsa",
    `  # grezzo tondo D${dTxt}x${lTxt} mm ${par.mat}, ${num(par.massa, 2)} kg; cadenza richiesta ${num(par.rate, par.rate % 1 ? 1 : 0)} pezzi/ora (${Math.round(3600 / par.rate)} s per pezzo)`,
    "  # I/O ipotizzati: DI2 porta aperta, DI3 fine ciclo, DO2 apri porta, DO3 morsa chiusa, DO4 avvio",
    "  set_tcp(p[0, 0, 0.172, 0, 0, 0])",
    "  set_payload(1.00, [0, 0, 0.06])",
    "  def pinza(mm):",
    `    rq_set_force_norm(${par.forza})`,
    "    rq_move_and_wait_mm(mm)",
    "  end",
    "  def porta(aperta):",
    "    set_standard_digital_out(2, aperta)",
    "    while get_standard_digital_in(2) != aperta:",
    "      sync()",
    "    end",
    "  end",
    "  def prendi(sopra, posa):",
    "    movel(sopra, a=0.8, v=0.5)",
    "    movel(posa, a=0.4, v=0.12)",
    `    pinza(${presa})                 # si ferma sul tondo D${dTxt}`,
    `    set_payload(${(1 + par.massa).toFixed(2)}, [0, 0, 0.08])`,
    "    movel(sopra, a=0.4, v=0.15)",
    "  end",
    "  def carica(fuori, sopra, posa):",
    "    porta(True)",
    "    movej(fuori, a=1.0, v=0.8)",
    "    movel(sopra, a=0.6, v=0.3)",
    "    movel(posa, a=0.3, v=0.06)",
    "    set_standard_digital_out(3, True)   # morsa chiude",
    "    sleep(0.3)",
    "    pinza(85)",
    "    set_payload(1.00, [0, 0, 0.06])",
    "    movel(sopra, a=0.6, v=0.2)",
    "    movel(fuori, a=0.8, v=0.4)",
    "  end",
    "  def ciclo():",
    "    porta(False)",
    "    set_standard_digital_out(4, True)",
    "    while not get_standard_digital_in(3):",
    "      sync()",
    "    end",
    "    set_standard_digital_out(4, False)",
    "    porta(True)",
    "  end",
    "  def scarica(sopra, posa, fuori, vaschetta):",
    "    movel(sopra, a=0.6, v=0.3)",
    "    movel(posa, a=0.3, v=0.06)",
    `    pinza(${presa})`,
    "    set_standard_digital_out(3, False)  # morsa apre",
    "    movel(sopra, a=0.4, v=0.15)",
    "    movel(fuori, a=0.8, v=0.4)",
    "    porta(False)",
    "    movej(vaschetta, a=1.0, v=0.8)",
    "    pinza(85)",
    "  end",
    "  movej([1.5708, -1.75, 1.6, -1.42, -1.5708, 0.0], a=1.0, v=0.8)",
    "  pinza(85)",
  ];
  const { src, vise, fuori } = cell.pts;
  src.forEach((s, k) => {
    const bx = 0.25 + ((k % 4) - 1.5) * cell.pts.pitchB;
    L.push(`  # pezzo ${k + 1}: vassoio posto ${k + 1} -> morsa -> vaschetta B`);
    L.push(`  prendi(${P(up(s))}, ${P(s)})`);
    L.push(`  carica(${P(fuori)}, ${P(up(vise))}, ${P(vise)})`);
    L.push("  ciclo()");
    L.push(`  scarica(${P(up(vise))}, ${P(vise)}, ${P(fuori)}, ${P([bx, 0.52, 1.1])})`);
  });
  L.push('  textmsg("lotto: 8 pezzi lavorati in vaschetta B")', "end", "gemello_asservimento_cnc()");
  return L.join("\n");
}


// ---------------------------------------------------------------- caricamento celle
const loader = new GLTFLoader();
const glb = {};
const loadGlb = (n) => new Promise((res, rej) => loader.load(`asset/${n}.glb`, (g) => res((glb[n] = g.scene)), undefined, rej));
const CELLE = {};
const MAT = materiali();
function cella(id) {
  if (CELLE[id]) return CELLE[id];
  const c = id === "pallet" ? cellaPallet(MAT, glb.ur30) : cellaCnc(MAT, glb.ur10e_2f85);
  c.items2 = prepItems(c);
  c.script = SCENARI[id].script || scriptCnc(c);
  c.lmap = c.lineMap(c.script);
  c.root.visible = false; world.add(c.root);
  window.__ik = Object.assign(window.__ik || {}, { [id]: [+c.piano.errMax.toFixed(5), c.piano.bad] }); document.body.dataset.ik = JSON.stringify(window.__ik);
  return (CELLE[id] = c);
}

// cella costruita dalla frase dell'utente: una sola alla volta, la precedente si smaltisce
function cellaDin(id, din) {
  const old = CELLE._din;
  if (old) {
    world.remove(old.root);
    old.root.traverse((o) => { if (o.geometry) { const eg = edgeCache.get(o.geometry.uuid); if (eg) { eg.dispose(); edgeCache.delete(o.geometry.uuid); } o.geometry.dispose(); } });
    old.items2.forEach((it) => { it.mats.forEach((m) => m.dispose()); it.lm.dispose(); });
    delete CELLE._din;
  }
  const c = id === "pallet" ? cellaPallet(MAT, glb.ur30, din.par) : cellaCnc(MAT, glb.ur10e_2f85, din.par);
  c.items2 = prepItems(c);
  c.script = din.scen.script || scriptCnc(c, din.par);
  c.lmap = c.lineMap(c.script);
  c.root.visible = false; world.add(c.root);
  window.__ik = Object.assign(window.__ik || {}, { din: [+c.piano.errMax.toFixed(5), c.piano.bad] }); document.body.dataset.ik = JSON.stringify(window.__ik);
  return (CELLE._din = c);
}

// ---------------------------------------------------------------- UI statica
const LV = [
  ["L0", "Regole + esempi", "parole chiave, misure, casi già visti · sempre per primo"],
  ["L1", "Modello economico", "DeepSeek v4.1 flash · GLM 5.3 flash per le immagini"],
  ["L2", "Claude", "solo se L1 sbaglia o è poco sicuro · tetto 0,30 $"],
];
$("#livelli").innerHTML = LV.map(([id, nm, nt], i) => `<div class="lv" id="lv${i}"><div class="id">${id}</div><div class="nm">${nm}</div>
  <div class="mx"><b class="c">—</b><span class="s">—</span></div><div class="nt">${nt}</div><div class="es2"><span><span class="dot"></span><span class="k">in attesa</span></span><span class="w"></span></div></div>`).join("");
const FL = ["ingresso", "capire", "progetto", "codice", "collaudo", "video"];
{
  let h = "";
  FL.forEach((n, i) => {
    const x = 4 + i * 73;
    if (i) h += `<path id="fp${i}" d="M${x - 10} 32 L${x - 2} 32"/>`;
    h += `<g class="nd" id="fn${i}"><rect x="${x}" y="18" width="63" height="28"/><text x="${x + 31.5}" y="35.5" text-anchor="middle">${n}</text></g>`;
  });
  h += `<text x="4" y="11" style="fill:#5a6066">flusso</text><text x="436" y="11" text-anchor="end" style="fill:#5a6066" id="fl-r">i modelli lavorano solo in «capire»</text>`;
  $("#flusso").innerHTML = h;
}
$("#banco").innerHTML = BANCO.map(([a, b, v, f, c]) => `<div class="bn"><span>${a} · ${b}</span><b>${v}${c ? ` <span>· ${c}</span>` : ""}</b><div class="bar"><i style="width:${f * 100}%"></i></div></div>`).join("");
$("#esempi").innerHTML = Object.values(SCENARI).map((s) => `<button class="es" data-s="${s.id}"><span class="n">${s.n}</span><b>${s.titolo}</b><span>${s.sotto}</span><em>${s.origine}</em></button>`).join("");

// ---------------------------------------------------------------- stato della corsa
let scen = null, cell = null, T0 = 1e9, sched = null, chipsExtra = [];
const els = {
  lv: [0, 1, 2].map((i) => $("#lv" + i)), spec: $("#spec"), code: $("#code"), checks: $("#checks"),
  hudN: $("#hud-n"), hudTot: $("#hud-tot"), hudFase: $("#hud-fase"), hudBar: $("#hud-bar"), clip: $("#clip"),
};
function chips(s) {
  const all = [...(s ? s.allegati : []), ...chipsExtra];
  $("#chips").innerHTML = all.map((a) => `<span class="chip"><b>${a.tipo}</b>${esc(a.nome)} <i>${esc(a.meta || "")}</i></span>`).join("");
}
function scegli(id, testo, din) {
  scen = din ? din.scen : SCENARI[id];
  document.querySelectorAll(".es").forEach((b) => b.classList.toggle("on", !din && b.dataset.s === id));
  $("#prompt").value = testo ?? scen.testo;
  chips(scen);
  for (const k in CELLE) CELLE[k].root.visible = false;
  cell = din ? cellaDin(id, din) : cella(id); cell.root.visible = true;
  document.body.dataset.stima = scen.stima ? "1" : "";
  $("#fl-r").textContent = din ? "capito a sole regole · 0 $" : "i modelli lavorano solo in «capire»";
  $("#vp-cella").textContent = scen.cella;
  $("#code-file").textContent = scen.file;
  $("#code-nota").innerHTML = `<span>${scen.codiceNota}</span><span>${cell.script.split("\n").length} righe · URScript</span>`;
  $("#hud-unita").textContent = scen.unita; els.hudTot.textContent = cell.n;
  $("#hud-ciclo").textContent = scen.cicloTxt;
  if (scen.clip) { $("#clip-l").textContent = scen.clip.label; els.clip.poster = scen.clip.poster; els.clip.src = scen.clip.src; }
  else { els.clip.removeAttribute("poster"); els.clip.removeAttribute("src"); }
  els.clip.parentElement.classList.remove("on");
  $("#ver-f").textContent = scen.fonteVerifica;
  els.checks.innerHTML = scen.verifica.map(([k, a, b]) => `<li class="${k}"><b>${k === "ok" ? "OK" : "VEDI"}</b><span>${a}<em>${b}</em></span></li>`).join("");
  // codice: una riga DOM per riga di programma
  const lines = cell.script.split("\n");
  els.code.innerHTML = lines.map((l, i) => `<div class="ln" style="display:none"><i>${i + 1}</i><span></span></div>`).join("");
  cell.codeLines = lines; cell.codeEls = [...els.code.children]; cell.shown = -1; cell.act = -1; cell.partial = -1;
  cell.lmapRev = cell.lmap;
  // camera iniziale
  const c = cell.centro, cw = new THREE.Vector3(c.x, c.z, -c.y);
  controls.target.copy(cw);
  const qc = qs.get("cam"); // ?cam=x,y,z,tx,ty,tz (coordinate di cella, per inquadrature fisse)
  if (qc) { const v = qc.split(",").map(Number); controls.target.set(v[3], v[5], -v[4]); camera.position.set(v[0], v[2], -v[1]); userCam = true; return; }
  if (!REGIA) { const { r, el, az } = cell.cam; camera.position.set(cw.x + r * Math.cos(el) * Math.cos(az), cw.y + r * Math.sin(el), cw.z - r * Math.cos(el) * Math.sin(az)); userCam = false; }
  sun.target.position.copy(cw); sun.position.set(cw.x + 3.5, 7, cw.z + 4);
}
function programma(s, regia) {
  // tempi relativi della corsa (secondi). In regia un po' più distesi.
  const k = regia ? 1.0 : 0.85, d = { su: 0.9, ok: 2.2, salta: 0.8, no: 0.35 };
  const lv = []; let t = 0.2;
  s.livelli.forEach((l, i) => { const dur = (i === 2 && l.st === "ok" ? 2.8 : d[l.st]) * k; lv.push([t, t + dur]); t += dur + 0.12; });
  const capito = Math.max(...lv.filter((_, i) => s.livelli[i].st !== "no").map((x) => x[1]));
  const spec0 = capito - 1.4 * k, step = 0.3 * k;
  const spec1 = spec0 + s.spec.length * step;
  const build0 = spec1 - 1.2, buildDur = regia ? 9.6 : 8.5;
  const code0 = build0 + 1.6, codeDur = regia ? 11 : 9.5;
  const robot0 = build0 + buildDur + 0.5;
  return { lv, spec0, step, spec1, build0, buildDur, code0, codeDur, robot0, ver0: robot0 + 2.2, tscale: regia ? 1.5 : 1 };
}
function genera(id, testo, din) {
  if (!glb.ur10e_2f85) return;
  scegli(id, testo, din);
  sched = programma(scen, REGIA);
  T0 = now(); lastTxt = {}; cell.items2.forEach((it) => (it.phase = -1));
  els.lv.forEach((e) => { e.className = "lv"; e._s = ""; });
  $("#genera").classList.add("run");
  if (!REGIA) els.clip.pause();
}
// frase libera: la legge l'interprete a regole (interprete.js); il caso di riferimento resta quello registrato
function mostraFuori(f, testo) { // oltre la portata di un cobot (o frase non riconosciuta): nessuna cella, solo ciò che è stato letto
  const s = f.scen || {};
  scen = { id: s.id || "pallet", allegati: [], clip: null };
  cell = null; sched = null; T0 = 1e9; lastTxt = {};
  for (const k in CELLE) CELLE[k].root.visible = false;
  document.querySelectorAll(".es").forEach((b) => b.classList.remove("on"));
  document.body.dataset.stima = "1";
  $("#prompt").value = testo; chips(null);
  const lv = s.livelli || [{ st: "su", costo: 0, sec: 0.02, nota: "non trovo né una pallettizzazione né un asservimento di macchina", esito: "non riconosciuto" }, { st: "no", nota: "non serve", esito: "non serve" }, { st: "no", nota: "non serve", esito: "non serve" }];
  lv.forEach((l, i) => {
    const e = els.lv[i]; e._s = "x"; e.className = "lv " + l.st;
    e.querySelector(".c").textContent = l.st === "no" ? "—" : usd(l.costo); e.querySelector(".s").textContent = l.st === "no" ? "" : num(l.sec, 2) + " s";
    e.querySelector(".k").textContent = l.esito; e.querySelector(".nt").textContent = l.nota; e.querySelector(".w").textContent = "";
  });
  const spec = f.spec || [];
  els.spec.innerHTML = spec.length ? '<div class="sl"><span class="p">{</span></div>' + spec.map(([k, v, fo], i) => `<div class="sl"><span class="kv">  <span class="k">"${k}"</span><span class="p">: </span><span class="v">"${esc(v)}"</span>${i < spec.length - 1 ? '<span class="p">,</span>' : ""}</span><span class="f ${fo}">${fo}</span></div>`).join("") + '<div class="sl"><span class="p">}</span></div>' : "";
  $("#spec-n").textContent = `${spec.length} campi`;
  FL.forEach((_, i) => { const n = $("#fn" + i); n.setAttribute("class", "nd" + (i < 2 ? " done" : "")); if (i) $("#fp" + i).setAttribute("class", i < 2 ? "on" : ""); });
  $("#fl-r").textContent = "capito a sole regole · 0 $";
  $("#tot").textContent = "modelli: 0 $ · 0,0 s"; $("#pf-c").textContent = "0 $"; $("#pf-l").textContent = "L0"; $("#pf-t").textContent = "0,0 s";
  $("#vp-cella").textContent = "nessuna cella · oltre la portata";
  $("#code-file").textContent = "—"; $("#code-nota").innerHTML = "<span>nessun programma generato</span>";
  els.code.innerHTML = `<div style="padding:14px;line-height:1.5;font-size:13px;white-space:normal"><p style="margin:0 0 10px">${esc(f.motivo)}</p><p style="margin:0 0 12px">Questo compito lo impostiamo con te: prenotiamo 20 minuti?</p><a class="btn primary" href="${CALL}" target="_blank" rel="noopener">Prenota una call</a></div>`;
  els.checks.innerHTML = `<li class="warn on"><b>VEDI</b><span>oltre la portata di un cobot<em>${esc(f.motivo)}</em></span></li>`;
  $("#ver-f").textContent = "nessun calcolo eseguito: nessuna cella costruita";
  const tag = $("#ver-tag"); tag.textContent = "da impostare"; tag.className = "tag";
  $("#hud-fase").textContent = "oltre la portata di un cobot: lo impostiamo con te"; els.hudBar.style.width = "0%";
  $("#hud-unita").textContent = "nessuna cella"; els.hudN.textContent = "0"; els.hudTot.textContent = "—"; $("#hud-ciclo").textContent = "—"; $("#hud-tc").textContent = "0,0 s"; $("#hud-x").textContent = "×1";
  $(".cnt").classList.remove("full");
  $("#stato-tag").textContent = "da impostare insieme";
  const g = $("#genera"); g.classList.remove("run"); g.firstChild.textContent = "Genera la cella";
}
function avvia(t, mostraEsito = true) { // mostraEsito=false (vista semplice): se la frase è fuori portata la scena resta com'è
  if (!glb.ur10e_2f85) return { pronto: false };
  let r;
  try { r = costruisci(t); } catch (e) { console.error(e); r = { processo: null, fuori: true, motivo: "Non riesco a leggere questa frase.", testo: t }; }
  if (r.fuori) { if (mostraEsito) mostraFuori(r, t); }
  else genera(r.processo, t, r.rif ? undefined : r);
  window.__gemello.stato = { capito: r.capito || "", stima: !!(r.scen && r.scen.stima && !r.rif) };
  return { pronto: true, processo: r.processo, fuori: !!r.fuori, motivo: r.motivo || "", rif: !!r.rif, capito: r.capito || "" };
}
window.__gemello = { esegui: avvia, stato: { capito: "", stima: false }, cella: () => cell };
document.querySelectorAll(".es").forEach((b) => b.addEventListener("click", () => { chipsExtra = []; window.__gemello.stato = { capito: "", stima: false }; genera(b.dataset.s); }));
$("#genera").addEventListener("click", () => {
  const t = $("#prompt").value.trim();
  if (!t) { window.__gemello.stato = { capito: "", stima: false }; genera(chipsExtra.some((c) => c.tipo === "video") ? "pallet" : scen.id); return; }
  avvia(t);
});
$("#prompt").addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); $("#genera").click(); } });
const fileIn = $("#file"); let attTipo = "foto";
document.querySelectorAll("[data-att]").forEach((b) => b.addEventListener("click", () => {
  attTipo = b.dataset.att;
  if (attTipo === "niente") { chipsExtra = [{ tipo: "niente", nome: "valori tipici", meta: "12 pezzi tipo" }]; $("#prompt").value = ""; chips(null); return; }
  fileIn.accept = { foto: "image/*", video: "video/*", cad: ".stl,.obj,.step,.stp" }[attTipo]; fileIn.click();
}));
fileIn.addEventListener("change", () => {
  for (const f of fileIn.files) chipsExtra.push({ tipo: attTipo, nome: f.name, meta: (f.size / 1e6).toFixed(1).replace(".", ",") + " MB" });
  chips(scen); fileIn.value = "";
});

// ---------------------------------------------------------------- evidenziazione URScript
const RX = /("[^"]*")|\b(def|end|while|not|if|else|elif|return|True|False|and|or)\b|\b([a-z_][a-z0-9_]*)(?=\()|(-?\b\d+(?:\.\d+)?\b)/g;
function hl(line) {
  let code = line, cm = "";
  const h = line.indexOf("#"); if (h >= 0) { code = line.slice(0, h); cm = line.slice(h); }
  let out = "", last = 0;
  code.replace(RX, (m, st, kw, fn, nu, off) => {
    out += esc(code.slice(last, off));
    out += st ? `<span class="st">${esc(st)}</span>` : kw ? `<span class="kw">${kw}</span>` : fn ? `<span class="fn">${fn}</span>` : `<span class="nu">${nu}</span>`;
    last = off + m.length; return m;
  });
  out += esc(code.slice(last));
  return out + (cm ? `<span class="cm">${esc(cm)}</span>` : "");
}

// ---------------------------------------------------------------- aggiornamento per fotogramma
const smp = {}, tcpM = new THREE.Matrix4(), pM = new THREE.Matrix4();
let lastTxt = {};
const setTxt = (el, key, v) => { if (lastTxt[key] !== v) { el.textContent = v; lastTxt[key] = v; } };

function aggiorna(t) { // t = secondi dall'inizio della corsa
  if (!cell) return;
  const S = sched, s = scen;
  // --- livelli
  let costo = 0, sec = 0;
  s.livelli.forEach((l, i) => {
    const e = els.lv[i], [a, b] = S.lv[i];
    let st = "", c = "—", tt = "—", k = "in attesa";
    if (t >= a && t < b && l.st !== "no") { st = "run"; const u = (t - a) / (b - a); c = "…"; tt = num(l.sec * u, l.sec < 1 ? 2 : 1) + " s"; k = i === 0 ? "regole in corso" : "chiamata in corso"; }
    else if (t >= b || (t >= a && l.st === "no")) {
      st = l.st === "ok" ? "ok" : l.st; c = l.st === "no" || l.st === "salta" ? "—" : usd(l.costo);
      tt = l.st === "no" || l.st === "salta" ? "" : num(l.sec, l.sec < 1 ? 2 : 1) + " s"; k = l.esito;
      costo += l.costo; sec += l.sec;
    }
    const key = st + c + tt;
    if (e._s !== key) {
      e._s = key; e.className = "lv" + (st ? " " + st : "");
      e.querySelector(".c").textContent = c; e.querySelector(".s").textContent = tt; e.querySelector(".k").textContent = k;
      e.querySelector(".nt").textContent = st && st !== "run" ? l.nota : st === "run" ? l.nota : LV[i][2];
      e.querySelector(".w").textContent = st === "run" ? (i === 0 ? "0 $" : "") : st === "su" ? "↓ sale" : "";
    }
  });
  setTxt($("#tot"), "tot", `modelli: ${usd(costo)} · ${num(sec, 1)} s`);
  const lmax = s.livelli.reduce((a, l, i) => (l.st === "ok" || l.st === "su") && t >= S.lv[i][1] ? "L" + i : a, "—");
  setTxt($("#pf-c"), "pfc", t >= S.lv[0][1] ? usd(costo) : "—");
  setTxt($("#pf-l"), "pfl", lmax);
  setTxt($("#pf-t"), "pft", t >= S.spec1 ? num(sec + 0.3, 1) + " s" : "—"); // tempo reale: modelli + progetto e compilazione (~0,3 s)
  // --- spec
  const nf = Math.max(0, Math.min(s.spec.length, Math.floor((t - S.spec0) / S.step) + 1));
  const part = clamp01(((t - S.spec0) % S.step) / (S.step * 0.8));
  const key = nf + ":" + (nf <= s.spec.length && t < S.spec1 ? Math.floor(part * 10) : "x");
  if (lastTxt.spec !== key) {
    lastTxt.spec = key;
    let h = '<div class="sl"><span class="p">{</span></div>';
    s.spec.forEach(([kk, v, f], i) => {
      if (i >= nf) return;
      const cur = i === nf - 1 && t < S.spec1;
      const vv = cur ? v.slice(0, Math.ceil(v.length * part)) : v;
      h += `<div class="sl ${cur ? "new" : ""}"><span class="kv">  <span class="k">"${kk}"</span><span class="p">: </span><span class="v ${cur ? "cur" : ""}">"${esc(vv)}"</span>${i < s.spec.length - 1 ? '<span class="p">,</span>' : ""}</span><span class="f ${f}">${f}</span></div>`;
    });
    if (nf >= s.spec.length) h += '<div class="sl"><span class="p">}</span></div>';
    els.spec.innerHTML = h;
    setTxt($("#spec-n"), "specn", `${nf} / ${s.spec.length} campi`);
  }
  // --- flusso
  const fT = [0, S.lv[0][0], S.spec1 - 0.6, S.code0, S.robot0, S.ver0];
  FL.forEach((_, i) => {
    const on = t >= fT[i], next = i < 5 ? t >= fT[i + 1] : false;
    const cl = "nd" + (on ? (next ? " done" : " on") : "");
    const n = $("#fn" + i); if (n.getAttribute("class") !== cl) n.setAttribute("class", cl);
    if (i) { const p = $("#fp" + i); const c2 = on ? "on" : ""; if (p.getAttribute("class") !== c2) p.setAttribute("class", c2); }
  });
  // --- costruzione
  const its = cell.items2, n = its.length, step = (S.buildDur - 1.25) / Math.max(1, n - 1);
  let fase = "in attesa della richiesta", bp = 0;
  its.forEach((it, i) => setItem(it, S.build0 + i * step, t));
  if (t >= S.build0) {
    const i = Math.min(n - 1, Math.floor((t - S.build0) / step)); bp = clamp01((t - S.build0) / S.buildDur);
    fase = bp < 1 ? `costruzione dalla spec · ${its[i].label}` : "";
  } else if (t >= 0) fase = t < S.spec0 ? "lettura della richiesta" : "compilazione della spec";
  // --- robot e pezzi
  const P = cell.piano, dur = P.t;
  let tc = 0, run = t >= S.robot0;
  if (run) { tc = (t - S.robot0) * S.tscale; tc = REGIA ? Math.min(tc, dur) : tc % dur; }
  P.sample(tc, smp);
  cell.robot.set(smp.q, smp.grip);
  cell.piano.kin.fk(smp.q, tcpM);
  const R = cell.anima(tc);
  cell.pezzi.forEach((p, k) => {
    const M = P.pezzo(k, tc, tcpM, pM);
    if (!M) { p.visible = false; return; }
    p.visible = true; p.matrix.copy(M); if (R) p.matrix.premultiply(R);
    if (P.fin && p.userData.fin) { const f = tc >= P.fin[k]; p.userData.fin.visible = f; p.userData.raw.visible = !f; }
  });
  const posati = run ? P.flag("posato", tc) : 0;
  if (cell.marcatori) cell.marcatori.forEach((r, k) => { r.material.emissiveIntensity = k < posati ? 2.4 : 0.3 + 0.25 * Math.max(0, Math.sin(t * 4 - k * 0.6)); r.visible = t >= S.robot0 - 1.5; });
  setTxt(els.hudN, "n", String(posati));
  const full = posati >= cell.n; if (lastTxt.full !== full) { $(".cnt").classList.toggle("full", full); lastTxt.full = full; }
  const perPezzo = P.marks.posato[cell.n - 1] / cell.n, fx = s.cicloReale / perPezzo;
  setTxt($("#hud-tc"), "tc", run ? num(tc * fx, 1) + " s" : "0,0 s");
  setTxt($("#hud-x"), "x", "×" + Math.round(fx * S.tscale));
  if (run) fase = full ? (s.id === "tavola" ? "piastra piena · la tavola ruota di 90°" : "ciclo completo · riparte") : `ciclo generato in esecuzione · ${s.unita.split(" ")[0]} ${Math.min(cell.n, posati + 1)} di ${cell.n}`;
  setTxt(els.hudFase, "fase", fase);
  const barW = run ? clamp01(posati / cell.n) : bp; if (lastTxt.bar !== barW) { els.hudBar.style.width = barW * 100 + "%"; lastTxt.bar = barW; }
  // --- codice: scrittura in streaming, poi riga attiva
  const L = cell.codeLines, tot = cell.script.length;
  const nch = Math.floor(tot * clamp01((t - S.code0) / S.codeDur));
  if (nch !== cell.partial) {
    let acc = 0, li = 0; while (li < L.length && acc + L[li].length + 1 <= nch) { acc += L[li].length + 1; li++; }
    for (let i = 0; i < L.length; i++) {
      const el = cell.codeEls[i], want = i < li ? "f" : i === li && nch < tot && nch > 0 ? "p" : "";
      if (want === "p") { el.style.display = ""; el.lastChild.innerHTML = hl(L[i].slice(0, nch - acc)); el.classList.add("caret"); el._st = "p"; }
      else if (el._st !== want) {
        el._st = want; el.classList.remove("caret");
        if (want === "f") { el.style.display = ""; el.lastChild.innerHTML = hl(L[i]); } else el.style.display = "none";
      }
    }
    cell.shown = Math.max(0, li - 1); cell.partial = nch;
    if (nch < tot) els.code.scrollTop = Math.max(0, (li + 2) * 17.8 - els.code.clientHeight);
  }
  let act = -1;
  if (run && nch >= tot && smp.line) act = cell.lmap[smp.line] ?? cell.lmap[smp.line.split(":")[0]] ?? -1;
  if (act !== cell.act) {
    if (cell.act >= 0) cell.codeEls[cell.act].classList.remove("act");
    if (act >= 0) { cell.codeEls[act].classList.add("act"); const y = act * 17.8 - els.code.clientHeight * 0.45; els.code.scrollTop = Math.max(0, y); }
    cell.act = act;
  }
  // --- verifica
  const nv = t >= S.ver0 ? Math.min(s.verifica.length, Math.floor((t - S.ver0) / 0.55) + 1) : 0;
  if (lastTxt.nv !== nv) {
    [...els.checks.children].forEach((li, i) => li.classList.toggle("on", i < nv));
    const tag = $("#ver-tag");
    const [tIn, tFine] = s.stima ? ["calcolo in corso", "stimato"] : ["collaudo in corso", "superato"];
    if (nv === 0) { tag.textContent = run ? tIn : "in attesa"; tag.className = "tag" + (run ? " live" : ""); }
    else { tag.textContent = nv < s.verifica.length ? tIn : tFine; tag.className = "tag " + (nv < s.verifica.length ? "live" : "ok"); }
    if (nv > 0 && lastTxt.nv === 0 && s.clip) { els.clip.parentElement.classList.add("on"); if (!REGIA || true) els.clip.play().catch(() => {}); }
    if (nv === 0) els.clip.parentElement.classList.remove("on");
    lastTxt.nv = nv;
  }
  const g = $("#genera"); const busy = t < S.robot0; if (lastTxt.busy !== busy) { g.classList.toggle("run", busy); g.firstChild.textContent = busy ? "Generazione in corso…" : "Genera la cella"; lastTxt.busy = busy; $("#stato-tag").textContent = busy ? "generazione" : "cella pronta"; }
}

// ---------------------------------------------------------------- regia (?regia=1): ~45 s
const FRASE = SCENARI.pallet.testo;
const RG = { type0: 1.3, type1: 6.0, chip: 6.4, out0: 7.6, out1: 8.6, run: 8.0, outro0: 40.6, outro1: 41.6, fine: 45.2 };
let R0 = null;
function regia(r) {
  const intro = $("#intro"), outro = $("#outro");
  const n = Math.round(FRASE.length * clamp01((r - RG.type0) / (RG.type1 - RG.type0)));
  const ti = $("#intro-t"); const v = esc(FRASE.slice(0, n)) + '<span class="caret" style="opacity:' + (Math.floor(r * 2.2) % 2 || r > RG.type0 && r < RG.type1 ? 1 : 0) + '"></span>';
  if (ti._v !== v) { ti.innerHTML = v; ti._v = v; }
  $("#intro-chip").style.opacity = ease((r - RG.chip) / 0.5);
  intro.style.opacity = 1 - ease((r - RG.out0) / (RG.out1 - RG.out0));
  intro.style.visibility = r > RG.out1 ? "hidden" : "visible";
  const o = ease((r - RG.outro0) / (RG.outro1 - RG.outro0));
  outro.style.opacity = o; outro.style.visibility = o > 0 ? "visible" : "hidden";
  const h1 = outro.querySelector("h1"); h1.style.transform = `translateY(${(1 - ease((r - RG.outro0 - 0.2) / 1.2)) * 24}px)`; h1.style.opacity = ease((r - RG.outro0 - 0.2) / 1.0);
  outro.querySelector("p").style.opacity = ease((r - RG.outro0 - 1.2) / 1.0);
  // camera cinematografica in funzione del tempo
  const t = r - RG.run, S = sched;
  const fin = ease((t - S.robot0 - 6) / 9), c = controls.target.clone();
  if (cell.fuoco) { const f = cell.fuoco; c.lerp(new THREE.Vector3(f.x, f.z, -f.y), fin * 0.8); }
  const b = ease((t - S.build0) / (S.buildDur + 2)), e = ease((t - S.robot0 - 12) / 10);
  const az = -1.75 + 0.75 * b + 0.3 * ease((t - S.robot0) / 16), el = 0.62 - 0.2 * b + 0.12 * fin, rad = 5.8 - 1.4 * b - 1.9 * fin;
  camera.position.set(c.x + rad * Math.cos(el) * Math.cos(az), c.y + rad * Math.sin(el), c.z - rad * Math.cos(el) * Math.sin(az));
  camera.lookAt(c);
  if (r >= RG.fine && !window.__regiaFine) { window.__regiaFine = true; document.body.dataset.regiaFine = "1"; }
}

// ---------------------------------------------------------------- avvio
function frame() {
  requestAnimationFrame(frame);
  const tn = now();
  if (REGIA && R0 !== null) { const r = tn - R0; aggiorna(r - RG.run); regia(r); }
  else if (!REGIA) {
    aggiorna(tn - T0);
    if (!userCam && cell) { const t = tn * 0.06; const c = controls.target, { el, az } = cell.cam, r = cell.cam.r * Math.max(1, 1.25 / camera.aspect); const a = az + Math.sin(t) * 0.35; camera.position.set(c.x + r * Math.cos(el) * Math.cos(a), c.y + r * Math.sin(el), c.z - r * Math.cos(el) * Math.sin(a)); }
    controls.update();
  }
  composer.render();
}
if (REGIA) { $("#intro").style.opacity = 1; regiaCaret(); }
function regiaCaret() { $("#intro-t").innerHTML = '<span class="caret"></span>'; }
requestAnimationFrame(frame);
try {
  await Promise.all([loadGlb("ur10e_2f85"), loadGlb("ur30")]);
} catch (e) { $("#hud-fase").textContent = "errore nel caricamento dei modelli 3D"; throw e; }
if (REGIA) {
  scegli("pallet"); sched = programma(scen, true); $("#prompt").value = FRASE;
  cell.items2.forEach((it) => (it.phase = -1));
  const c = controls.target;
  R0 = now();
} else {
  // le altre celle si preparano in sottofondo, poi parte il primo esempio
  const s0 = SCENARI[qs.get("s")] ? qs.get("s") : "pallet";
  genera(s0);
  setTimeout(() => { for (const k of Object.keys(SCENARI)) cella(k); }, 1500);
}
window.__pronto = true;
