// Unitree G1 29 DoF su mesh vere (unitree_mujoco g1_29dof.xml, decimate) + IK numerica (DLS)
// e camminata procedurale. Mondo Z in alto, metri, come MuJoCo / Isaac.
import * as THREE from 'three';
import { toCreasedNormals } from 'three/addons/utils/BufferGeometryUtils.js';

const clamp01 = x => Math.max(0, Math.min(1, x));
const _v = new THREE.Vector3(), _v2 = new THREE.Vector3(), _q = new THREE.Quaternion(), _q2 = new THREE.Quaternion();

export async function loadG1(base) {
  const [meta, bin] = await Promise.all([
    fetch(base + 'g1.json').then(r => r.json()),
    fetch(base + 'g1.bin').then(r => r.arrayBuffer()),
  ]);
  const mats = {
    l: new THREE.MeshStandardMaterial({ color: 0xc8cbd0, metalness: 0.88, roughness: 0.3 }),
    d: new THREE.MeshStandardMaterial({ color: 0x2a2c30, metalness: 0.55, roughness: 0.45 }),
  };
  const root = new THREE.Group(); root.name = 'G1';
  const bodies = {}, joints = {};
  for (const b of meta.bodies) {
    const o = new THREE.Object3D(); o.name = b.name;
    o.position.set(...b.pos);
    const q0 = new THREE.Quaternion(b.quat[1], b.quat[2], b.quat[3], b.quat[0]);
    o.quaternion.copy(q0);
    o.userData.q0 = q0;
    (b.parent ? bodies[b.parent] : root).add(o);
    bodies[b.name] = o;
    if (b.joint) {
      const j = { name: b.joint, body: o, q0, axis: new THREE.Vector3(...b.axis), lo: b.range[0], hi: b.range[1], q: 0 };
      joints[b.joint] = j;
    }
    for (const m of b.meshes) {
      const qv = new Uint16Array(bin, m.vo, m.vn * 3);
      const pos = new Float32Array(m.vn * 3);
      for (let i = 0; i < m.vn; i++) for (let k = 0; k < 3; k++) pos[i * 3 + k] = m.lo[k] + qv[i * 3 + k] / 65535 * m.sc[k];
      const idx = m.i32 ? new Uint32Array(bin, m.fo, m.fn * 3) : new Uint16Array(bin, m.fo, m.fn * 3);
      let g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      g.setIndex(new THREE.BufferAttribute(idx.slice(), 1));
      g = toCreasedNormals(g, 0.55);
      const mesh = new THREE.Mesh(g, mats[m.c]);
      mesh.castShadow = true; mesh.receiveShadow = true;
      o.add(mesh);
    }
  }
  return new G1(root, bodies, joints, mats);
}

function setJ(j, q) {
  j.q = Math.min(j.hi, Math.max(j.lo, q));
  _q.setFromAxisAngle(j.axis, j.q);
  j.body.quaternion.copy(j.q0).multiply(_q);
}

// risolve A x = b (n<=6) con eliminazione di Gauss
function solve(A, b, n) {
  const M = A.map((r, i) => [...r, b[i]]);
  for (let c = 0; c < n; c++) {
    let p = c; for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
    [M[c], M[p]] = [M[p], M[c]];
    const d = M[c][c] || 1e-9;
    for (let r = 0; r < n; r++) if (r !== c) { const f = M[r][c] / d; for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k]; }
  }
  return M.map((r, i) => r[n] / (M[i][i] || 1e-9));
}

class Chain {
  constructor(robot, names, effBody, effLocal, rest) {
    this.j = names.map(n => robot.joints[n]);
    this.eff = robot.bodies[effBody]; this.effLocal = effLocal;
    this.top = this.j[0].body; this.rest = rest || this.j.map(() => 0);
  }
  pe(out) { return out.copy(this.effLocal).applyMatrix4(this.eff.matrixWorld); }
  get q() { return this.j.map(j => j.q); }
  set q(v) { this.j.forEach((j, i) => setJ(j, v[i])); }
  solve(target, tq, { iters = 6, wRot = 0.4, lambda = 0.06, restW = 0.0, maxStep = 0.3, rest = this.rest } = {}) {
    const n = this.j.length, m = tq ? 6 : 3;
    const pe = new THREE.Vector3(), pj = new THREE.Vector3(), aj = new THREE.Vector3(), c = new THREE.Vector3();
    let err = 0;
    for (let it = 0; it < iters; it++) {
      this.top.updateMatrixWorld(true);
      this.pe(pe);
      const e = [target.x - pe.x, target.y - pe.y, target.z - pe.z];
      err = Math.hypot(e[0], e[1], e[2]);
      if (tq) {
        this.eff.getWorldQuaternion(_q2);
        _q.copy(tq).multiply(_q2.invert());
        if (_q.w < 0) { _q.x *= -1; _q.y *= -1; _q.z *= -1; _q.w *= -1; }
        const s = Math.sqrt(1 - Math.min(1, _q.w * _q.w)), ang = 2 * Math.acos(Math.min(1, _q.w));
        const k = s > 1e-6 ? ang / s : 2;
        e.push(_q.x * k * wRot, _q.y * k * wRot, _q.z * k * wRot);
      }
      const J = [];
      for (let i = 0; i < n; i++) {
        const b = this.j[i].body;
        b.getWorldPosition(pj); b.getWorldQuaternion(_q2);
        aj.copy(this.j[i].axis).applyQuaternion(_q2);
        c.subVectors(pe, pj); c.crossVectors(aj, c);
        J.push(tq ? [c.x, c.y, c.z, aj.x * wRot, aj.y * wRot, aj.z * wRot] : [c.x, c.y, c.z]);
      }
      const A = [];
      for (let r = 0; r < m; r++) { A.push([]); for (let s = 0; s < m; s++) { let v = 0; for (let i = 0; i < n; i++) v += J[i][r] * J[i][s]; A[r].push(v + (r === s ? lambda * lambda : 0)); } }
      const y = solve(A, e, m);
      for (let i = 0; i < n; i++) {
        let dq = 0; for (let r = 0; r < m; r++) dq += J[i][r] * y[r];
        dq += restW * (rest[i] - this.j[i].q);
        dq = Math.max(-maxStep, Math.min(maxStep, dq));
        setJ(this.j[i], this.j[i].q + dq);
      }
    }
    this.top.updateMatrixWorld(true);
    return err;
  }
}

const LEG = s => [`${s}_hip_pitch_joint`, `${s}_hip_roll_joint`, `${s}_hip_yaw_joint`, `${s}_knee_joint`, `${s}_ankle_pitch_joint`, `${s}_ankle_roll_joint`];
const ARM = s => [`${s}_shoulder_pitch_joint`, `${s}_shoulder_roll_joint`, `${s}_shoulder_yaw_joint`, `${s}_elbow_joint`, `${s}_wrist_roll_joint`, `${s}_wrist_pitch_joint`, `${s}_wrist_yaw_joint`];

export class G1 {
  constructor(root, bodies, joints, mats) {
    this.root = root; this.bodies = bodies; this.joints = joints; this.mats = mats;
    this.pelvis = bodies.pelvis;
    this.palm = new THREE.Vector3(0.115, 0, 0.0);
    const legRest = [-0.32, 0, 0, 0.66, -0.34, 0];
    this.legs = { L: new Chain(this, LEG('left'), 'left_ankle_roll_link', new THREE.Vector3(), legRest), R: new Chain(this, LEG('right'), 'right_ankle_roll_link', new THREE.Vector3(), legRest) };
    this.arms = {
      L: new Chain(this, ARM('left'), 'left_wrist_yaw_link', this.palm, [0.05, 0.2, 0, 1.0, 0, 0, 0]),
      R: new Chain(this, ARM('right'), 'right_wrist_yaw_link', this.palm, [0.05, -0.2, 0, 1.0, 0, 0, 0]),
    };
    // posizioni di riferimento a q=0 (piedi a terra con bacino a 0.793)
    this.pelvis.position.set(0, 0, 0.793); this.pelvis.quaternion.identity();
    this.root.updateMatrixWorld(true);
    this.footOff = {};
    for (const s of ['L', 'R']) { const p = this.legs[s].pe(new THREE.Vector3()); this.footOff[s] = p.clone(); }
    this.ankleH = this.footOff.L.z; // altezza della caviglia dal suolo
    for (const s of ['L', 'R']) this.footOff[s].z = 0;
    // posa di riposo delle braccia
    for (const s of ['L', 'R']) this.arms[s].j.forEach((j, i) => setJ(j, this.arms[s].rest[i]));
    this.root.updateMatrixWorld(true);
    this.handRest = {};
    for (const s of ['L', 'R']) { const p = this.arms[s].pe(new THREE.Vector3()); this.pelvis.worldToLocal(p); this.handRest[s] = p; }
    this.waist = { yaw: joints.waist_yaw_joint, roll: joints.waist_roll_joint, pitch: joints.waist_pitch_joint };
    this.palmWorld = { L: new THREE.Vector3(), R: new THREE.Vector3() };
    this.first = true;
  }
  set(j, q) { setJ(this.joints[j], q); }
  // st = stato calcolato dalla timeline: base {x,y,z,yaw,pitch,roll}, feet {L:{p,yaw},R:{...}}, hands {L:{p,w},R}, waist {yaw,pitch}
  body(st) {
    const b = st.base;
    this.pelvis.position.set(b.x, b.y, b.z);
    this.pelvis.quaternion.setFromEuler(new THREE.Euler(b.roll || 0, b.pitch || 0, b.yaw, 'ZYX'));
    setJ(this.waist.yaw, st.waist?.yaw || 0); setJ(this.waist.pitch, st.waist?.pitch || 0); setJ(this.waist.roll, st.waist?.roll || 0);
    this.root.updateMatrixWorld(true);
    if (this.first) for (const s of ['L', 'R']) { this.legs[s].j.forEach((j, i) => setJ(j, this.legs[s].rest[i])); this.arms[s].j.forEach((j, i) => setJ(j, this.arms[s].rest[i])); }
    const it = this.first ? 40 : 6; this.first = false;
    this.root.updateMatrixWorld(true);
    for (const s of ['L', 'R']) {
      const f = st.feet[s];
      _v.set(f.p.x, f.p.y, f.p.z + this.ankleH);
      const tq = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, f.pitch || 0, f.yaw, 'ZYX'));
      this.legs[s].solve(_v, tq, { iters: it, wRot: 0.5, lambda: 0.07, restW: 0.03, maxStep: 0.15 });
    }
  }
  // bersaglio della mano: riposo (con oscillazione e accucciata) -> punto richiesto, pesato da w
  armTarget(st, s, h = st.hands[s]) {
    const rest = new THREE.Vector3().copy(this.handRest[s]);
    if (h.swing) rest.x += h.swing;
    if (h.restOff) rest.add(h.restOff);
    this.pelvis.localToWorld(rest);
    const tgt = h.p ? rest.lerp(h.p, h.w) : rest;
    const wr = h.q && h.p ? clamp01((h.w - 0.35) / 0.45) : 0;
    return { tgt, tq: wr > 0 ? h.q : null, wr };
  }
  // Braccia: per ogni chiave della timeline l'IK viene risolta una volta sola, con calma e da più pose di partenza
  // (bake); fra due chiavi si interpola nello spazio dei giunti e ogni fotogramma corregge solo di poco, partendo
  // sempre dalla posa interpolata. Niente memoria fra fotogrammi = niente salti, e lo stesso t dà la stessa posa.
  bake(tl) {
    tl.armQ = { L: [], R: [] };
    const saveFirst = this.first;
    for (const s of ['L', 'R']) {
      const arm = this.arms[s], sg = s === 'R' ? 1 : -1;
      const seeds = [arm.rest, [-0.9, -0.15 * sg, 0, 0.7, 0, -0.2, 0], [-1.5, -0.25 * sg, 0.3 * sg, 0.5, 0, -0.4, 0], [-0.4, -0.3 * sg, 0, 1.3, 0, 0, 0]];
      let prev = arm.rest;
      for (const k of tl.hands[s]) {
        const st = tl.eval(k.t);
        this.first = true; this.body(st);
        const p = typeof k.p === 'function' ? k.p(k.t) : k.p, q = typeof k.q === 'function' ? k.q(k.t) : k.q;
        const { tgt, tq, wr } = this.armTarget(st, s, { p, w: p ? k.w : 0, q, swing: 0, restOff: st.hands[s].restOff });
        let best = null;
        for (const seed of [prev, ...seeds]) {
          arm.q = seed;
          for (let pass = 0; pass < 3; pass++) arm.solve(tgt, tq, { iters: 30, wRot: 0.35 * wr, lambda: 0.05, restW: 0.02, maxStep: 0.12 });
          const e = arm.pe(new THREE.Vector3()).distanceTo(tgt);
          let r = 0; if (tq) { arm.eff.getWorldQuaternion(_q2); r = 2 * Math.acos(Math.min(1, Math.abs(_q2.dot(tq)))); }
          const qv = arm.q; let dist = 0; qv.forEach((x, i) => { dist += (x - prev[i]) ** 2; });
          const cost = e + 0.04 * r * wr + 0.01 * Math.sqrt(dist);
          if (!best || cost < best.cost) best = { cost, q: qv, e, r };
        }
        tl.armQ[s].push(best.q); prev = best.q;
        if (s === 'R') (tl.armErr ??= []).push({ t: k.t, e: best.e, r: best.r });
      }
    }
    this.first = saveFirst || true;
  }
  apply(st) {
    if (st.tl && !st.tl.armQ) this.bake(st.tl);
    this.body(st);
    for (const s of ['L', 'R']) {
      const h = st.hands[s], arm = this.arms[s];
      const { tgt, tq, wr } = this.armTarget(st, s);
      const Q = st.tl?.armQ?.[s];
      if (Q && h.ka != null) {
        const qa = Q[h.ka], qb = Q[h.kb], base = qa.map((x, i) => x + (qb[i] - x) * h.u);
        arm.q = base;
        // fra due chiavi diverse conta il moto dei giunti (morbido); vicino alle chiavi e quando si tiene, il bersaglio
        const c = h.pin ? 1 : 1 - Math.sin(Math.PI * h.u);
        if (c < 1) { arm.top.updateMatrixWorld(true); tgt.lerpVectors(arm.pe(_v), tgt, c); }
        arm.solve(tgt, tq, { iters: 5, wRot: 0.3 * wr * c, lambda: 0.08, restW: 0.12, rest: base, maxStep: 0.08 });
      } else arm.solve(tgt, tq, { iters: 6, wRot: 0.12, lambda: 0.06, restW: 0.05, maxStep: 0.2 });
      arm.pe(this.palmWorld[s]);
    }
  }
  reset() { this.first = true; }
}

// ---------------------------------------------------------------- timeline di movimento
export const ease = x => { x = clamp01(x); return x * x * (3 - 2 * x); };
const ease5 = x => { x = clamp01(x); return x * x * x * (x * (6 * x - 15) + 10); };
const angLerp = (a, b, t) => { let d = b - a; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; return a + d * t; };

export class Timeline {
  constructor(robot, start) {
    this.r = robot; this.segs = []; this.t = 0; this.pose = { ...start };
    this.hands = { L: [{ t: 0, p: null, w: 0 }], R: [{ t: 0, p: null, w: 0 }] };
    this.events = []; this.steps = []; this.extra = [];
    this.H = 0.725;
  }
  stand(d, o = {}) { this.segs.push({ type: 'stand', t0: this.t, t1: this.t + d, a: { ...this.pose }, b: { ...this.pose }, ...o }); this.t += d; return this; }
  walk(x, y, yaw, speed = 0.42) {
    const a = { ...this.pose }, b = { x, y, yaw: yaw ?? a.yaw };
    const dist = Math.hypot(b.x - a.x, b.y - a.y);
    let dy = b.yaw - a.yaw; while (dy > Math.PI) dy -= 2 * Math.PI; while (dy < -Math.PI) dy += 2 * Math.PI;
    const d = Math.max(1.4, dist / speed + Math.abs(dy) / 0.9 + 0.4);
    const n = Math.max(3, Math.round(d / 0.42));
    this.segs.push({ type: 'walk', t0: this.t, t1: this.t + d, a, b, n });
    this.pose = { ...b }; this.t += d; return this;
  }
  hand(s, dt, p, w = 1, q = null) { this.hands[s].push({ t: this.t + dt, p, w, q }); return this; }
  ev(dt, name, data) { this.events.push({ t: this.t + dt, name, data }); return this; }
  step(label, tool, t0, t1, extra = {}) { this.steps.push({ label, tool, t0, t1, ...extra }); return this; }
  end() { this.T = this.t; return this; }

  basePose(t) {
    let s = this.segs.find(s => t >= s.t0 && t < s.t1) || (t < 0 ? this.segs[0] : this.segs[this.segs.length - 1]);
    const u = clamp01((t - s.t0) / (s.t1 - s.t0));
    if (s.type === 'walk') {
      const e = ease(u);
      return { x: s.a.x + (s.b.x - s.a.x) * e, y: s.a.y + (s.b.y - s.a.y) * e, yaw: angLerp(s.a.yaw, s.b.yaw, ease5(u)), seg: s, u };
    }
    return { ...s.a, seg: s, u };
  }
  footAt(s, side, pose) {
    const off = this.r.footOff[side];
    const c = Math.cos(pose.yaw), sn = Math.sin(pose.yaw);
    return { p: new THREE.Vector3(pose.x + off.x * c - off.y * sn, pose.y + off.x * sn + off.y * c, 0), yaw: pose.yaw };
  }
  // appoggi futuri dei piedi nel segmento di camminata in corso (per le impronte gialle)
  landings(t) {
    const s = this.segs.find(s => t >= s.t0 && t < s.t1);
    if (!s || s.type !== 'walk') return [];
    const Ts = (s.t1 - s.t0) / s.n, k = Math.floor((t - s.t0) / Ts), out = [];
    for (let i = k; i < s.n; i++) {
      const tl = Math.min(s.t1 - 1e-6, s.t0 + (i + 1) * Ts + Ts * 0.5);
      const f = this.footAt(s, i % 2 === 0 ? 'R' : 'L', this.basePose(tl));
      out.push({ ...f, i, now: i === k });
    }
    return out;
  }
  eval(t) {
    const bp = this.basePose(t), s = bp.seg;
    const st = { tl: this, base: { x: bp.x, y: bp.y, z: this.H, yaw: bp.yaw, pitch: 0, roll: 0 }, feet: {}, hands: {}, waist: { yaw: 0, pitch: 0 }, walking: false };
    if (s.type === 'walk') {
      st.walking = true;
      const Ts = (s.t1 - s.t0) / s.n, tau = t - s.t0;
      const k = Math.min(s.n - 1, Math.floor(tau / Ts));
      const land = i => { const tl = Math.min(s.t1, s.t0 + (i + 1) * Ts + Ts * 0.5); return this.basePose(Math.min(tl, s.t1 - 1e-6)); };
      for (const side of ['L', 'R']) {
        const mine = i => (i % 2 === 0) === (side === 'R'); // passi pari = destro
        let prev = -1; for (let i = 0; i < k; i++) if (mine(i)) prev = i;
        const from = prev < 0 ? this.footAt(s, side, { ...s.a }) : this.footAt(s, side, land(prev));
        if (mine(k)) {
          const to = this.footAt(s, side, land(k));
          const u = clamp01((tau - k * Ts) / Ts), e = ease(u);
          const p = from.p.clone().lerp(to.p, e); p.z = 0.075 * Math.sin(Math.PI * u);
          st.feet[side] = { p, yaw: angLerp(from.yaw, to.yaw, e), pitch: -0.15 * Math.sin(Math.PI * u) };
        } else st.feet[side] = from;
      }
      const ph = tau / Ts;
      const fade = Math.min(1, tau / 0.4, (s.t1 - t) / 0.4);
      st.base.z = this.H - 0.012 * fade * Math.abs(Math.cos(Math.PI * ph));
      const sway = 0.022 * fade * Math.sin(Math.PI * ph);
      st.base.x += -Math.sin(bp.yaw) * sway; st.base.y += Math.cos(bp.yaw) * sway;
      st.base.roll = -0.03 * fade * Math.sin(Math.PI * ph); st.base.pitch = 0.04 * fade;
      st.swing = 0.07 * fade * Math.sin(Math.PI * ph);
    } else {
      st.feet.L = this.footAt(s, 'L', bp); st.feet.R = this.footAt(s, 'R', bp);
      if (s.slump) { // "spento": accucciato, busto in avanti
        const w = s.slump(t);
        st.base.z = this.H - 0.13 * w; st.waist.pitch = 0.45 * w; st.base.pitch = 0.12 * w;
        st.slump = w;
      }
      if (s.crouch) { const w = s.crouch(t); st.base.z -= 0.06 * w; st.base.pitch += 0.1 * w; st.waist.pitch += 0.12 * w; }
    }
    for (const side of ['L', 'R']) {
      const ks = this.hands[side];
      let i = ks.length - 1; while (i > 0 && ks[i].t > t) i--;
      const ib = Math.min(ks.length - 1, i + 1), a = ks[i], b = ks[ib];
      const u = b.t > a.t ? ease(clamp01((t - a.t) / (b.t - a.t))) : 1;
      const w = a.w + (b.w - a.w) * u;
      let p = null;
      const pa = typeof a.p === 'function' ? a.p(t) : a.p, pb = typeof b.p === 'function' ? b.p(t) : b.p;
      if (pa && pb) p = pa.clone().lerp(pb, u); else p = (pa || pb) ? (pa || pb).clone() : null;
      // chiavi con lo stesso bersaglio (tenere il manico, trasportare, riposo): la mano va tenuta lì con precisione
      const pin = (!pa && !pb) || (pa && pb && pa.distanceTo(pb) < 0.02 && Math.abs(a.w - b.w) < 0.02);
      const qa = typeof a.q === 'function' ? a.q(t) : a.q, qb = typeof b.q === 'function' ? b.q(t) : b.q;
      const q = qa && qb ? qa.clone().slerp(qb, u) : (qa || qb || null);
      st.hands[side] = { p, w: p ? w : 0, q, swing: (st.swing || 0) * (side === 'L' ? 1 : -1) * (1 - w), ka: i, kb: ib, u, pin };
      if (st.slump) st.hands[side].restOff = new THREE.Vector3(-0.08 * st.slump, 0, -0.12 * st.slump);
    }
    return st;
  }
}
