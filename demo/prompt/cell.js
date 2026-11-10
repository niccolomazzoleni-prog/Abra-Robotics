// Le tre celle: geometria (Z in alto, metri), ordine di costruzione e piano del ciclo robot.
import * as THREE from "three";
import { Cinematica, Robot, posa } from "./robot.js";

const PI = Math.PI;
const M = (o) => new THREE.MeshStandardMaterial(o);
export const materiali = () => ({
  floor: M({ color: 0x2e3134, roughness: 0.92, metalness: 0.0 }),
  steel: M({ color: 0x8e959c, roughness: 0.38, metalness: 0.8 }),
  inox: M({ color: 0xc4c9ce, roughness: 0.28, metalness: 0.85 }),
  dark: M({ color: 0x24282c, roughness: 0.6, metalness: 0.3 }),
  paint: M({ color: 0x9aa0a6, roughness: 0.55, metalness: 0.2 }),
  paint2: M({ color: 0x5b6168, roughness: 0.5, metalness: 0.25 }),
  frame: M({ color: 0x2f557a, roughness: 0.5, metalness: 0.3 }),
  signal: M({ color: 0xf2c200, roughness: 0.45, metalness: 0.1 }),
  black: M({ color: 0x111315, roughness: 0.7, metalness: 0.1 }),
  plate: M({ color: 0xc19a6b, roughness: 0.62, metalness: 0.05 }),
  part: M({ color: 0xa8aeb4, roughness: 0.3, metalness: 0.9 }),
  raw: M({ color: 0x5d6368, roughness: 0.75, metalness: 0.6 }),
  fin: M({ color: 0xdfe4e8, roughness: 0.14, metalness: 1.0 }),
  card: M({ color: 0xb4875a, roughness: 0.88, metalness: 0.0 }),
  wood: M({ color: 0x9c7a52, roughness: 0.9, metalness: 0.0 }),
  rubber: M({ color: 0x1a1c1e, roughness: 0.9, metalness: 0.0 }),
  glass: M({ color: 0x1b2a33, roughness: 0.1, metalness: 0.2, transparent: true, opacity: 0.45 }),
  screen: M({ color: 0x0d1114, roughness: 0.3, emissive: 0x2a2200, emissiveIntensity: 1 }),
});

function box(mat, lx, ly, lz, x, y, z0) { // z0 = quota della faccia inferiore
  const m = new THREE.Mesh(new THREE.BoxGeometry(lx, ly, lz), mat); m.position.set(x, y, z0 + lz / 2);
  m.castShadow = m.receiveShadow = true; return m;
}
function cyl(mat, r, h, x, y, z0, seg = 40, r2 = r) {
  const g = new THREE.CylinderGeometry(r2, r, h, seg); g.rotateX(PI / 2);
  const m = new THREE.Mesh(g, mat); m.position.set(x, y, z0 + h / 2); m.castShadow = m.receiveShadow = true; return m;
}
const grp = (...c) => { const g = new THREE.Group(); c.forEach((o) => g.add(o)); return g; };

// rete della recinzione: texture a maglia generata in un canvas
let _rete;
function reteTex() {
  if (_rete) return _rete;
  const c = document.createElement("canvas"); c.width = c.height = 64; const x = c.getContext("2d");
  x.strokeStyle = "rgba(150,156,162,1)"; x.lineWidth = 3; x.strokeRect(0, 0, 64, 64);
  _rete = new THREE.CanvasTexture(c); _rete.wrapS = _rete.wrapT = THREE.RepeatWrapping; _rete.anisotropy = 4; return _rete;
}
function grigliaTex() {
  const c = document.createElement("canvas"); c.width = c.height = 128; const x = c.getContext("2d");
  x.fillStyle = "#3a3e42"; x.fillRect(0, 0, 128, 128); x.strokeStyle = "#1c1f22"; x.lineWidth = 5;
  for (let i = 0; i <= 128; i += 16) { x.beginPath(); x.moveTo(i, 0); x.lineTo(i, 128); x.stroke(); }
  x.lineWidth = 2; for (let i = 0; i <= 128; i += 32) { x.beginPath(); x.moveTo(0, i); x.lineTo(128, i); x.stroke(); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t;
}
function pavimento(m, lx, ly, cx = 0, cy = 0) {
  const g = new THREE.Group();
  const f = new THREE.Mesh(new THREE.PlaneGeometry(lx, ly), m.floor); f.position.set(cx, cy, 0); f.receiveShadow = true; g.add(f);
  return g;
}
function striscia(m, pts) { // linee gialle a pavimento
  const g = new THREE.Group();
  for (let i = 0; i < pts.length - 1; i++) {
    const [a, b] = [pts[i], pts[i + 1]]; const L = Math.hypot(b[0] - a[0], b[1] - a[1]);
    const s = new THREE.Mesh(new THREE.PlaneGeometry(L + 0.06, 0.06), m.signal);
    s.position.set((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0.002); s.rotation.z = Math.atan2(b[1] - a[1], b[0] - a[0]); s.receiveShadow = true; g.add(s);
  }
  return g;
}
function recinzione(m, pts, h = 1.9) {
  const g = new THREE.Group();
  const rete = new THREE.MeshStandardMaterial({ color: 0x9aa0a6, map: reteTex(), alphaMap: reteTex(), transparent: true, alphaTest: 0.3, side: THREE.DoubleSide, roughness: 0.6, metalness: 0.5 });
  for (let i = 0; i < pts.length - 1; i++) {
    const [a, b] = [pts[i], pts[i + 1]]; const L = Math.hypot(b[0] - a[0], b[1] - a[1]); const n = Math.max(1, Math.round(L / 1.2));
    for (let k = 0; k < n; k++) {
      const u0 = k / n, u1 = (k + 1) / n;
      const x0 = a[0] + (b[0] - a[0]) * u0, y0 = a[1] + (b[1] - a[1]) * u0, x1 = a[0] + (b[0] - a[0]) * u1, y1 = a[1] + (b[1] - a[1]) * u1;
      const l = L / n, ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
      const t = rete.clone(); t.map = rete.map.clone(); t.map.repeat.set(l / 0.05, (h - 0.25) / 0.05); t.map.needsUpdate = true; t.alphaMap = t.map;
      const p = new THREE.Mesh(new THREE.PlaneGeometry(l - 0.05, h - 0.25), t);
      p.rotation.set(PI / 2, 0, 0); const w = new THREE.Group(); w.add(p); w.rotation.z = ang; w.position.set((x0 + x1) / 2, (y0 + y1) / 2, 0.15 + (h - 0.25) / 2); g.add(w);
      const fr = box(m.paint2, l - 0.04, 0.025, 0.025, 0, 0, 0); fr.position.set(0, 0, 0); const fw = new THREE.Group(); fw.add(fr);
      fw.rotation.z = ang; fw.position.set((x0 + x1) / 2, (y0 + y1) / 2, h - 0.08); g.add(fw);
      g.add(box(m.dark, 0.05, 0.05, h, x0, y0, 0));
      g.add(box(m.signal, 0.06, 0.06, 0.02, x0, y0, h));
    }
  }
  const e = pts[pts.length - 1]; g.add(box(m.dark, 0.05, 0.05, h, e[0], e[1], 0)); g.add(box(m.signal, 0.06, 0.06, 0.02, e[0], e[1], h));
  return g;
}
function piedistallo(m, x, y, z, lato = 0.32) {
  return grp(box(m.paint2, lato, lato, z - 0.03, x, y, 0), box(m.dark, lato + 0.12, lato + 0.12, 0.03, x, y, 0), box(m.steel, lato + 0.04, lato + 0.04, 0.03, x, y, z - 0.03));
}
function quadroComandi(m, x, y, yaw = 0) {
  const g = grp(box(m.paint2, 0.06, 0.06, 1.1, 0, 0, 0), box(m.paint, 0.36, 0.08, 0.28, 0, 0, 1.1), box(m.screen, 0.3, 0.01, 0.2, 0, -0.041, 1.14), box(m.signal, 0.05, 0.03, 0.05, 0.12, -0.05, 1.32));
  g.position.set(x, y, 0); g.rotation.z = yaw; return g;
}

// ---------- piano del ciclo: segmenti in spazio giunti + stati dei pezzi in funzione del tempo ----------
const ease = (u) => (u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u));
export class Piano {
  constructor(kin, q0) { this.kin = kin; this.q = q0.slice(); this.grip = 0; this.t = 0; this.segs = []; this.keys = {}; this.marks = {}; this.errMax = 0; this.line = -1; }
  to(T, dur, line = this.line) {
    let { q, err } = this.kin.ik(T, this.q, 300);
    if (err > 1e-3) { // riprova da semi diversi, tiene la soluzione più vicina
      for (const d of [[0, 0.4, -0.4, 0, 0, 0], [0, -0.4, 0.4, 0, 0, 0], [0, 0, 0, 0.8, 0, 0], [0, 0, 0, -0.8, 0, 0], [0, 0, 0, 0, 0, 1.5]]) {
        const r = this.kin.ik(T, this.q.map((v, i) => v + d[i]), 300); if (r.err < err - 1e-4) ({ q, err } = r);
      }
    }
    this.errMax = Math.max(this.errMax, err);
    if (err > 1e-3) (this.bad = this.bad || []).push([this.line, +err.toFixed(4), [T.elements[12], T.elements[13], T.elements[14]].map((v) => +v.toFixed(3))]);
    for (let j = 0; j < 6; j++) { while (q[j] - this.q[j] > PI) q[j] -= 2 * PI; while (q[j] - this.q[j] < -PI) q[j] += 2 * PI; }
    this.segs.push({ t0: this.t, t1: this.t + dur, q0: this.q, q1: q, g0: this.grip, g1: this.grip, line }); this.q = q; this.t += dur; return this;
  }
  joints(q, dur, line = this.line) { this.segs.push({ t0: this.t, t1: this.t + dur, q0: this.q, q1: q.slice(), g0: this.grip, g1: this.grip, line }); this.q = q.slice(); this.t += dur; return this; }
  gr(g, dur, line = this.line) { this.segs.push({ t0: this.t, t1: this.t + dur, q0: this.q, q1: this.q, g0: this.grip, g1: g, line }); this.grip = g; this.t += dur; return this; }
  wait(dur, line = this.line) { return this.gr(this.grip, dur, line); }
  mark(n) { (this.marks[n] = this.marks[n] || []).push(this.t); return this; }
  tcp() { return this.kin.fk(this.q, new THREE.Matrix4()); }
  // pezzi
  key(k, o) { (this.keys[k] = this.keys[k] || []).push({ t: this.t, ...o }); return this; }
  ultimo(k) { const ks = this.keys[k]; const l = ks[ks.length - 1]; return l.M1 || l.M; }
  attach(k) { const off = this.tcp().invert().multiply(this.ultimo(k)); return this.key(k, { kind: "att", off }); }
  detach(k, M) { const ks = this.keys[k]; const off = [...ks].reverse().find((x) => x.kind === "att").off; return this.key(k, { kind: "static", M: M || this.tcp().multiply(off) }); }
  sample(t, out) {
    const s = this.segs; let lo = 0, hi = s.length - 1;
    if (t <= 0) { out.q = s[0].q0; out.grip = s[0].g0; out.line = s[0].line; return out; }
    while (lo < hi) { const mid = (lo + hi) >> 1; if (s[mid].t1 < t) lo = mid + 1; else hi = mid; }
    const g = s[lo], u = ease((t - g.t0) / (g.t1 - g.t0 || 1));
    out.q = g.q0.map((a, i) => a + (g.q1[i] - a) * u); out.grip = g.g0 + (g.g1 - g.g0) * u; out.line = g.line; return out;
  }
  pezzo(k, t, tcpM, out) { // matrice del pezzo k al tempo t (null = nascosto)
    const ks = this.keys[k]; let c = null;
    for (const x of ks) { if (x.t <= t) c = x; else break; }
    if (!c || c.kind === "hide") return null;
    if (c.kind === "static") return out.copy(c.M);
    if (c.kind === "att") return out.multiplyMatrices(tcpM, c.off);
    if (c.kind === "lerp") {
      const u = Math.min(1, (t - c.t) / c.d); const e = c.fall ? u * u : ease(u);
      const p0 = new THREE.Vector3().setFromMatrixPosition(c.M0), p1 = new THREE.Vector3().setFromMatrixPosition(c.M1);
      return out.copy(c.M1).setPosition(p0.lerp(p1, e));
    }
    return null;
  }
  flag(name, t) { const m = this.marks[name] || []; let n = 0; for (const x of m) if (x <= t) n++; return n; }
}
const Tm = (x, y, z, rz = 0) => new THREE.Matrix4().makeRotationZ(rz).setPosition(x, y, z);

// ---------- pezzi ----------
function raccordo(m) { // origine: sotto la testa esagonale
  const head = new THREE.Mesh(new THREE.CylinderGeometry(0.0098, 0.0098, 0.008, 6).rotateX(PI / 2).translate(0, 0, 0.004), m.part);
  const sh = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.03, 16).rotateX(PI / 2).translate(0, 0, -0.015), m.part);
  head.castShadow = sh.castShadow = true; return grp(head, sh);
}


// associa le etichette del piano alle righe del programma (k-esima occorrenza)
function mapLinee(script, kind) {
  const lines = script.split("\n"), map = {}, cnt = {};
  lines.forEach((l, i) => { const k = kind(l, i); if (!k) return; const n = cnt[k] = (cnt[k] ?? -1) + 1; map[k + ":" + n] = i; if (!(k in map)) map[k] = i; });
  return map;
}

// ================= SCENA 2: pallettizzazione =================
export function cellaPallet(m, gltf) {
  const items = []; const add = (label, obj) => { items.push({ label, obj }); return obj; };
  const root = new THREE.Group();
  root.add(add("pavimento", grp(pavimento(m, 9, 8, -0.3, 0.2), striscia(m, [[-1.6, 2.0], [1.4, 2.0], [1.4, -1.0]]))));
  root.add(add("recinzione", recinzione(m, [[-1.4, -0.6], [-1.4, 2.25], [1.65, 2.25]])));
  // rulliera lungo Y a x = -0.715 (punto di presa del programma reale)
  const cx = -0.715, ctop = 0.652, y0 = -2.6, y1 = 0.35, w = 0.7;
  const conv = new THREE.Group();
  conv.add(box(m.paint2, 0.05, y1 - y0, 0.1, cx - w / 2, (y0 + y1) / 2, ctop - 0.12), box(m.paint2, 0.05, y1 - y0, 0.1, cx + w / 2, (y0 + y1) / 2, ctop - 0.12));
  for (let i = 0; i < 5; i++) for (const s of [-1, 1]) conv.add(box(m.dark, 0.05, 0.05, ctop - 0.12, cx + s * w / 2, y0 + 0.15 + (i * (y1 - y0 - 0.3)) / 4, 0));
  for (let i = 0; i < 34; i++) { const g = new THREE.CylinderGeometry(0.025, 0.025, w - 0.06, 14); g.rotateZ(PI / 2); const r = new THREE.Mesh(g, m.steel); r.position.set(cx, y0 + 0.05 + i * ((y1 - y0 - 0.1) / 33), ctop - 0.025); r.castShadow = true; conv.add(r); }
  conv.add(box(m.signal, w, 0.04, 0.12, cx, y1 - 0.02, ctop - 0.02));
  conv.add(box(m.black, 0.06, 0.06, 0.06, cx - w / 2 - 0.05, -0.25, ctop + 0.05));
  root.add(add("rulliera motorizzata", conv));
  // pallet EUR 1200x800x144
  const pal = new THREE.Group(), px = 0, py = 0.959;
  for (const yy of [-0.35, 0, 0.35]) pal.add(box(m.wood, 1.2, 0.1, 0.022, px, py + yy, 0));
  for (const xx of [-0.55, 0, 0.55]) for (const yy of [-0.35, 0, 0.35]) pal.add(box(m.wood, 0.1, 0.1, 0.078, px + xx, py + yy, 0.022));
  for (const xx of [-0.55, 0, 0.55]) pal.add(box(m.wood, 0.1, 0.8, 0.022, px + xx, py, 0.1));
  for (let i = 0; i < 5; i++) pal.add(box(m.wood, 1.2, 0.1, 0.022, px, py - 0.35 + i * 0.175, 0.122));
  root.add(add("pallet EUR 1200×800", pal));
  root.add(add("quadro comandi", quadroComandi(m, 1.1, -0.6, PI / 2)));
  root.add(add("piedistallo", piedistallo(m, 0, 0, 0.4, 0.36)));
  const robot = new Robot(gltf, "ur30", 0.13);
  const baseM = Tm(0, 0, 0.4, PI); robot.root.matrixAutoUpdate = false; robot.root.matrix.copy(baseM); root.add(robot.root);
  // ventosa 4 coppe sul flangia (tool0, Z uscente)
  const vt = grp(cyl(m.paint2, 0.045, 0.06, 0, 0, 0), box(m.dark, 0.32, 0.2, 0.02, 0, 0, 0.06), box(m.signal, 0.08, 0.08, 0.025, 0, 0, 0.035));
  for (const sx of [-1, 1]) for (const sy of [-1, 1]) vt.add(cyl(m.rubber, 0.028, 0.05, sx * 0.088, sy * 0.06, 0.08, 20, 0.018));
  robot.tool0.add(vt);
  for (const lk of ["base_link_inertia", "shoulder_link", "upper_arm_link", "forearm_link", "wrist_1_link", "wrist_2_link", "wrist_3_link"]) {
    items.push({ label: "UR30 · " + lk.replace("_link", "").replace("_", " "), meshes: robot.parts.filter((p) => p.link === lk).map((p) => p.mesh), robot: true });
  }
  items.push({ label: "ventosa 4 coppe", obj: vt, robot: true });
  // scatole 600x400x300 (origine: centro della faccia superiore)
  const N = 8, pezzi = [], pg = new THREE.Group();
  const geo = new THREE.BoxGeometry(0.6, 0.4, 0.3).translate(0, 0, -0.15);
  const nastro = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.06, 0.002).translate(0, 0, 0.001), M({ color: 0xc9b38a, roughness: 0.6 }));
  for (let k = 0; k < N; k++) { const b = new THREE.Mesh(geo, m.card); b.castShadow = b.receiveShadow = true; b.add(nastro.clone()); b.matrixAutoUpdate = false; pezzi.push(b); pg.add(b); }
  root.add(add("scatole 600×400×300 · 18 kg", pg));

  const kin = new Cinematica("ur30", baseM, 0.13);
  const P = new Piano(kin, [0, -1.9, 1.9, -1.57, -1.57, 0]);
  const giu = (x, y, z) => posa([x, y, z], [0, 0, -1], [0, 1, 0]);
  P.line = "home"; P.to(giu(-0.3, 0.45, 1.0), 0.01); P.joints(P.q, 0.4);
  const slot = [[0.3015, 1.1605], [-0.3015, 1.1605], [0.3015, 0.7575], [-0.3015, 0.7575]];
  const pickZ = ctop + 0.3, stopY = 0;
  for (let k = 0; k < N; k++) {
    const [sx, sy] = slot[k % 4], sz = 0.147 + 0.3 * (Math.floor(k / 4) + 1);
    const tP = P.t + 0.55; // istante di arrivo sotto la ventosa
    const ks = P.keys[k] = [];
    ks.push({ t: 0, kind: "hide" });
    ks.push({ t: Math.max(0.001, tP - 2.4), kind: "lerp", d: 2.1, M0: Tm(cx, y0 + 0.3, pickZ), M1: Tm(cx, stopY, pickZ) });
    P.line = "presa:" + k;
    P.to(giu(cx, stopY, pickZ + 0.2), 0.55).to(giu(cx, stopY, pickZ), 0.25).gr(1, 0.14);
    P.keys[k].push({ t: P.t - 0.001, kind: "static", M: Tm(cx, stopY, pickZ) });
    P.attach(k).to(giu(cx, stopY, pickZ + 0.2), 0.25);
    P.line = "deposito:" + k;
    const zA = Math.max(sz + 0.15, pickZ + 0.2);
    P.to(giu((cx + sx) / 2 - 0.15, (stopY + sy) / 2, zA + 0.05), 0.42).to(giu(sx, sy, sz + 0.07), 0.4).to(giu(sx, sy, sz), 0.28).gr(0, 0.12).detach(k, Tm(sx, sy, sz)).to(giu(sx, sy, sz + 0.07), 0.22);
    P.mark("posato");
  }
  P.line = "fine"; P.to(giu(-0.3, 0.45, 1.0), 0.6); P.wait(2.0);
  return {
    root, items, robot, piano: P, pezzi, n: N,
    centro: new THREE.Vector3(-0.25, 0.3, 0.6), cam: { r: 5.6, el: 0.42, az: -0.75 },
    lineMap: (script) => mapLinee(script, (l) => /^\s*presa\(\)/.test(l) ? "presa" : /^\s*deposito\(/.test(l) ? "deposito" : /pallet completo/.test(l) ? "fine" : null),
    anima: () => null,
  };
}

// ================= SCENA 3: asservimento CNC =================
export function cellaCnc(m, gltf) {
  const items = []; const add = (label, obj) => { items.push({ label, obj }); return obj; };
  const root = new THREE.Group();
  root.add(add("pavimento", grp(pavimento(m, 8, 7, 0.4, 0.2), striscia(m, [[-1.0, -1.25], [2.0, -1.25]]))));
  root.add(add("recinzione", recinzione(m, [[0.55, 1.5], [-1.1, 1.5], [-1.1, -1.4]])));
  // piattaforma CM-18 (cella_main m_ur10e_cnc): piano 1,2 x 0,7 a 0,85 m
  const plat = grp(box(m.paint2, 1.16, 0.66, 0.8, 0, 0.35, 0), box(m.inox, 1.2, 0.7, 0.05, 0, 0.35, 0.8), box(m.signal, 1.2, 0.02, 0.05, 0, 0.0, 0.8));
  root.add(add("piattaforma CM-18", plat));
  // centro di lavoro con porta automatica
  const X0 = 0.62, cnc = new THREE.Group();
  cnc.add(box(m.paint, 1.1, 1.3, 0.95, X0 + 0.55, 0.25, 0));
  cnc.add(box(m.paint, 1.1, 0.35, 1.1, X0 + 0.55, -0.225, 0.95));
  cnc.add(box(m.paint, 1.1, 0.3, 1.1, X0 + 0.55, 0.75, 0.95));
  cnc.add(box(m.paint, 1.1, 1.3, 0.25, X0 + 0.55, 0.25, 2.05));
  cnc.add(box(m.paint, 0.9, 0.65, 1.1, X0 + 0.65, 0.275, 0.95)); // retro del vano
  cnc.children[cnc.children.length - 1].position.x = X0 + 0.75;
  cnc.add(box(m.black, 0.02, 0.65, 0.65, X0 + 0.3, 0.275, 0.95)); cnc.children[cnc.children.length - 1].position.x = X0 + 0.32;
  cnc.add(box(m.signal, 0.02, 1.3, 0.06, X0 - 0.01, 0.25, 1.98));
  cnc.add(box(m.dark, 1.12, 1.32, 0.12, X0 + 0.55, 0.25, 0));
  cnc.add(box(m.glass, 0.5, 0.02, 0.4, X0 + 0.6, -0.41, 1.1), box(m.paint2, 0.6, 0.015, 0.5, X0 + 0.6, -0.405, 1.05));
  cnc.add(box(m.dark, 0.35, 0.02, 0.06, X0 + 0.6, -0.41, 1.75));
  cnc.add(box(m.screen, 0.02, 0.28, 0.2, X0 - 0.01, 0.78, 1.45));
  // morsa
  const vx = 0.86, vy = 0.24, vz = 1.0;
  cnc.add(box(m.dark, 0.3, 0.4, 0.05, vx, vy, 0.95), box(m.steel, 0.16, 0.2, vz - 1.0 + 0.04, vx, vy, 1.0));
  const ganF = box(m.steel, 0.03, 0.16, 0.05, vx + 0.045, vy, vz + 0.04), ganM = box(m.steel, 0.03, 0.16, 0.05, vx - 0.06, vy, vz + 0.04);
  cnc.add(ganF, ganM);
  // mandrino che scende durante la lavorazione
  const mand = grp(cyl(m.paint2, 0.07, 0.35, 0, 0, 0.12), cyl(m.steel, 0.02, 0.12, 0, 0, 0));
  mand.position.set(vx, vy, 1.4); cnc.add(mand);
  const porta = grp(box(m.paint2, 0.04, 0.66, 0.66, 0, 0, 0), box(m.glass, 0.045, 0.4, 0.36, 0, 0, 0.18));
  porta.position.set(X0 - 0.03, 0.275, 0.95); cnc.add(porta);
  const luce = new THREE.Mesh(new THREE.SphereGeometry(0.025, 12, 8), new THREE.MeshStandardMaterial({ color: 0x222222, emissive: 0xf2c200, emissiveIntensity: 0 }));
  luce.position.set(X0 - 0.02, -0.33, 2.15); cnc.add(luce);
  root.add(add("centro di lavoro CNC · porta e morsa", cnc));
  // vassoio grezzi e vaschetta finiti
  const tray = grp(box(m.dark, 0.3, 0.3, 0.025, -0.25, 0.3, 0.85));
  for (let i = 0; i < 4; i++) for (const sy of [-0.035, 0.035]) for (const jj of [0, 1]) tray.add(box(m.paint2, 0.05, 0.02, 0.012, -0.25 + (i - 1.5) * 0.065, 0.3 + (jj - 0.5) * 0.14 + sy, 0.875));
  root.add(add("vassoio grezzi", tray));
  const bin = grp(box(m.signal, 0.3, 0.26, 0.012, 0.25, 0.52, 0.85), box(m.signal, 0.3, 0.012, 0.14, 0.25, 0.39, 0.85), box(m.signal, 0.3, 0.012, 0.14, 0.25, 0.65, 0.85), box(m.signal, 0.012, 0.26, 0.14, 0.1, 0.52, 0.85), box(m.signal, 0.012, 0.26, 0.14, 0.4, 0.52, 0.85));
  root.add(add("vaschetta B · finiti", bin));
  const rbx = 0, rby = -0.35, rbz = 0.85;
  root.add(add("piedistallo", piedistallo(m, rbx, rby, rbz)));
  const robot = new Robot(gltf, "ur10e", 0.172);
  const baseM = Tm(rbx, rby, rbz, PI / 2); robot.root.matrixAutoUpdate = false; robot.root.matrix.copy(baseM); root.add(robot.root);
  for (const lk of ["base_link_inertia", "shoulder_link", "upper_arm_link", "forearm_link", "wrist_1_link", "wrist_2_link", "wrist_3_link", "gripper"]) {
    items.push({ label: lk === "gripper" ? "pinza Robotiq 2F-85" : "UR10e · " + lk.replace("_link", "").replace("_", " "), meshes: robot.parts.filter((p) => p.link === lk).map((p) => p.mesh), robot: true });
  }
  // grezzi Ø50x120, asse lungo Y; origine al centro
  const N = 8, pezzi = [], pg = new THREE.Group();
  const gRaw = new THREE.CylinderGeometry(0.025, 0.025, 0.12, 28), gFin = new THREE.CylinderGeometry(0.019, 0.019, 0.06, 28).translate(0, 0.03, 0);
  const gFin2 = new THREE.CylinderGeometry(0.025, 0.025, 0.06, 28).translate(0, -0.03, 0);
  for (let k = 0; k < N; k++) {
    const raw = new THREE.Mesh(gRaw, m.raw), fin = grp(new THREE.Mesh(gFin, m.fin), new THREE.Mesh(gFin2, m.fin));
    raw.castShadow = true; fin.children.forEach((c) => (c.castShadow = true)); fin.visible = false;
    const p = grp(raw, fin); p.matrixAutoUpdate = false; p.userData = { raw, fin }; pezzi.push(p); pg.add(p);
  }
  root.add(add("grezzi Ø50×120 acciaio", pg));

  const kin = new Cinematica("ur10e", baseM, 0.172);
  const P = new Piano(kin, [0, -1.75, 1.6, -1.42, -1.5708, 0]);
  const giu = (x, y, z) => posa([x, y, z], [0, 0, -1], [1, 0, 0]); // dita lungo X: stringono il tondo
  const fuori = [0.4, 0.22, 1.36];
  P.line = "home"; P.to(giu(0.1, 0.1, 1.3), 0.01); P.joints(P.q, 0.4);
  const src = [];
  for (let jj = 0; jj < 2; jj++) for (let i = 0; i < 4; i++) src.push([-0.25 + (i - 1.5) * 0.065, 0.3 + (jj - 0.5) * 0.14, 0.875 + 0.012 + 0.025]);
  pezzi.forEach((_, k) => P.key(k, { kind: "static", M: Tm(...src[k]) }));
  const cz = vz + 0.065;
  const pts = { src, vise: [vx - 0.008, vy, cz], fuori };
  for (let k = 0; k < N; k++) {
    const [sx, sy, sz] = src[k];
    P.line = "prendi:" + k;
    P.to(giu(sx, sy, sz + 0.12), 0.5).to(giu(sx, sy, sz), 0.24).gr(1, 0.14).attach(k).to(giu(sx, sy, sz + 0.12), 0.22);
    P.line = "carica:" + k;
    P.mark("apri").to(giu(...fuori), 0.5).to(giu(vx - 0.008, vy, cz + 0.12), 0.34).to(giu(vx - 0.008, vy, cz), 0.24).mark("serra").gr(0, 0.12).detach(k, Tm(vx - 0.008, vy, cz)).to(giu(vx - 0.008, vy, cz + 0.12), 0.2).to(giu(...fuori), 0.3);
    P.line = "ciclo:" + k;
    P.mark("chiudi").wait(0.45).mark("lav0").wait(1.5).mark("lav1"); (P.fin = P.fin || {})[k] = P.t; P.wait(0.1).mark("apri2").wait(0.4);
    P.line = "scarica:" + k;
    P.to(giu(vx - 0.008, vy, cz + 0.12), 0.32).to(giu(vx - 0.008, vy, cz), 0.22).mark("libera").gr(1, 0.12).attach(k).to(giu(vx - 0.008, vy, cz + 0.12), 0.2).to(giu(...fuori), 0.3).mark("chiudi2");
    const bxp = 0.25 + ((k % 4) - 1.5) * 0.06, byp = 0.52, bzp = 0.875 + 0.025 + Math.floor(k / 4) * 0.05;
    P.to(giu(bxp, byp, 1.1), 0.45).gr(0, 0.1);
    const Mrel = P.tcp().multiply([...P.keys[k]].reverse().find((x) => x.kind === "att").off);
    P.key(k, { kind: "lerp", d: 0.28, fall: true, M0: Mrel, M1: Tm(bxp, byp, bzp) }).wait(0.15);
    P.mark("posato");
  }
  P.line = "fine"; P.to(giu(0.1, 0.1, 1.3), 0.6); P.wait(1.5);
  // stati di porta, morsa, mandrino in funzione del tempo
  const iv = (a, b, t) => { // ultimo evento tra a/b prima di t
    let la = -1, lb = -1; for (const x of P.marks[a] || []) if (x <= t) la = x; for (const x of P.marks[b] || []) if (x <= t) lb = x; return [la, lb];
  };
  return {
    root, items, robot, piano: P, pezzi, n: N, pts, kin,
    centro: new THREE.Vector3(0.3, 0.15, 1.0), cam: { r: 4.5, el: 0.4, az: -2.7 },
    lineMap: (script) => mapLinee(script, (l) => { const m2 = /^\s*(prendi|carica|ciclo|scarica)\(/.exec(l); return m2 ? m2[1] : /textmsg\("lotto/.test(l) ? "fine" : /^\s*movej/.test(l) ? "home" : null; }),
    anima(t) {
      // porta: aperta tra apri/apri2 e chiudi/chiudi2
      const ev = []; for (const n of ["apri", "apri2"]) for (const x of P.marks[n]) ev.push([x, 1]); for (const n of ["chiudi", "chiudi2"]) for (const x of P.marks[n]) ev.push([x, 0]);
      ev.sort((a, b) => a[0] - b[0]);
      let st = 0, t0 = -9, prev = 0; for (const [x, v] of ev) if (x <= t) { prev = st; st = v; t0 = x; }
      const u = ease((t - t0) / 0.4); const ap = prev + (st - prev) * u;
      porta.position.y = 0.275 + 0.68 * ap;
      const [ls, ll] = iv("serra", "libera", t); const ch = ls > ll ? ease((t - ls) / 0.12) : 1 - ease((t - ll) / 0.12);
      ganM.position.x = vx - 0.06 + 0.018 * Math.max(0, Math.min(1, ch));
      const [l0, l1] = iv("lav0", "lav1", t); const lav = l0 > l1 && l0 >= 0;
      mand.position.z = lav ? 1.4 - 0.22 * ease((t - l0) / 0.3) : 1.4 - 0.22 * (1 - ease((t - l1) / 0.3)) * (l1 >= 0 ? 1 : 0);
      mand.rotation.z = lav ? t * 40 : 0;
      luce.material.emissiveIntensity = lav ? 2.5 : 0.15;
      return null;
    },
  };
}
