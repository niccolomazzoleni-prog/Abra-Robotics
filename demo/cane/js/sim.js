// Simulazione lato browser della console Go2: mondo a scatole (stesso formato di pc_tools/mondo_sim.py),
// LiDAR L2 a raggi veri contro le scatole, mappa a voxel stile KISS-SLAM, griglia di occupazione da 0,2 m,
// frontiere ed A* come autonomy/navigatore_slam.py (celle 0,2 m, ostacoli gonfiati), stima EKF + ArUco.

export const RIS = 0.2;            // celle della griglia (m), come navigatore_slam.py
const GONFIA = 0.36;               // raggio di sicurezza del cane (m)
const VOX = 0.075, VOX_PAV = 0.18; // voxel della mappa punti (pareti / pavimento)

// generatore pseudo-casuale deterministico (la regia deve essere ripetibile)
export function rng(seed) {
  let s = seed >>> 0;
  return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}

export class Mondo {
  constructor(nome, d) {
    this.nome = nome;
    this.limiti = d.limiti; this.partenza = d.partenza; this.zone = d.zone || {};
    this.n = d.lo.length;
    this.lo = new Float32Array(d.lo.flat()); this.hi = new Float32Array(d.hi.flat());
    // ostacoli per il cane: base sotto 0,5 m e cima sopra 0,1 m (Mondo.ostacoli)
    this.ost = [];
    for (let i = 0; i < this.n; i++) if (this.lo[i * 3 + 2] < 0.5 && this.hi[i * 3 + 2] > 0.1) this.ost.push(i);
  }
  // primo urto del raggio: {t, b} (b = indice scatola, -1 pavimento), t = Infinity se nulla
  raggio(ox, oy, oz, dx, dy, dz, portata, da = 0) {
    let best = portata, bb = -2;
    const ix = 1 / dx, iy = 1 / dy, iz = 1 / dz, lo = this.lo, hi = this.hi;
    for (let i = da, k = da * 3; i < this.n; i++, k += 3) {
      let t1 = (lo[k] - ox) * ix, t2 = (hi[k] - ox) * ix;
      let tmin = t1 < t2 ? t1 : t2, tmax = t1 < t2 ? t2 : t1;
      t1 = (lo[k + 1] - oy) * iy; t2 = (hi[k + 1] - oy) * iy;
      tmin = Math.max(tmin, Math.min(t1, t2)); tmax = Math.min(tmax, Math.max(t1, t2));
      if (tmax < tmin) continue;
      t1 = (lo[k + 2] - oz) * iz; t2 = (hi[k + 2] - oz) * iz;
      tmin = Math.max(tmin, Math.min(t1, t2)); tmax = Math.min(tmax, Math.max(t1, t2));
      if (tmax < tmin || tmax < 0) continue;
      const t = tmin > 0 ? tmin : tmax;
      if (t < best) { best = t; bb = i; }
    }
    if (dz < -1e-6) { const tp = -oz / dz; if (tp < best) { best = tp; bb = -1; } }
    return bb === -2 ? null : { t: best, b: bb };
  }
  distanza(x, y) {   // distanza dall'ostacolo vero più vicino (per il log "vicino=")
    const [x0, x1, y0, y1] = this.limiti; let m = Math.min(x - x0, x1 - x, y - y0, y1 - y);
    for (const i of this.ost) {
      const dx = Math.max(this.lo[i * 3] - x, 0, x - this.hi[i * 3]), dy = Math.max(this.lo[i * 3 + 1] - y, 0, y - this.hi[i * 3 + 1]);
      m = Math.min(m, Math.hypot(dx, dy));
    }
    return m;
  }
}

// mappa SLAM: voxel di punti (KISS-SLAM tiene una mappa a voxel), griglia 2D, maschera "visto" per la rivelazione
export class Mappa {
  constructor(mondo, maxPunti = 420000) {
    this.mondo = mondo;
    const [x0, x1, y0, y1] = mondo.limiti;
    this.x0 = x0 - 1; this.y0 = y0 - 1;
    this.W = Math.ceil((x1 - x0 + 2) / RIS); this.H = Math.ceil((y1 - y0 + 2) / RIS);
    const N = this.W * this.H;
    this.occ = new Uint8Array(N);       // conteggio urti ostacolo (sticky)
    this.lib = new Uint8Array(N);       // 1 = pavimento visto libero
    this.visto = new Float32Array(N);   // 0..1 rivelazione (sale nel tempo)
    this.vistoT = new Uint8Array(N);    // bersaglio
    this.boxVisto = new Float32Array(Math.max(1, mondo.n)); this.boxVistoT = new Uint8Array(Math.max(1, mondo.n));
    this.costo = new Float32Array(N); this.costoSporco = true;
    this.vox = new Set();
    this.maxPunti = maxPunti; this.pos = new Float32Array(maxPunti * 3); this.nasc = new Float32Array(maxPunti); this.np = 0;
    this.nuovi0 = 0; this.velVisto = 1.6; this.velBox = 0.9;
  }
  cella(x, y) { return [Math.floor((x - this.x0) / RIS), Math.floor((y - this.y0) / RIS)]; }
  idx(i, j) { return (i < 0 || j < 0 || i >= this.W || j >= this.H) ? -1 : j * this.W + i; }
  centro(i, j) { return [this.x0 + (i + 0.5) * RIS, this.y0 + (j + 0.5) * RIS]; }
  stato(k) { return this.occ[k] >= 2 ? 1 : this.lib[k] ? 0 : -1; }

  _punto(x, y, z, t) {
    const v = z < 0.04 ? VOX_PAV : VOX;
    const key = Math.floor(x / v + 2000) + Math.floor(y / v + 2000) * 8192 + (Math.floor(z / v) + 4 + (v === VOX_PAV ? 0 : 200)) * 67108864;
    if (this.vox.has(key) || this.np >= this.maxPunti) return false;
    this.vox.add(key);
    const k = this.np++;
    this.pos[k * 3] = x; this.pos[k * 3 + 1] = y; this.pos[k * 3 + 2] = z; this.nasc[k] = t;
    return true;
  }
  // una scansione: integra punti, libero lungo il raggio (fino a 9 m), occupato sugli ostacoli
  integra(o, punti, t) {
    const [oi, oj] = this.cella(o[0], o[1]);
    let nuovi = 0;
    for (let p = 0; p < punti.n; p++) {
      const x = punti.xyz[p * 3], y = punti.xyz[p * 3 + 1], z = punti.xyz[p * 3 + 2], b = punti.b[p];
      if (this._punto(x, y, z, t)) nuovi++;
      const [ci, cj] = this.cella(x, y);
      const kc = this.idx(ci, cj);
      if (kc < 0) continue;
      this.vistoT[kc] = 1;
      if (b >= 0) {
        this.boxVistoT[b] = 1;
        if (this.mondo.lo[b * 3 + 2] < 0.5 && z < 1.6 && z > 0.06) { if (this.occ[kc] < 250) { this.occ[kc]++; if (this.occ[kc] === 2) this.costoSporco = true; } }
      }
      // libero lungo il raggio 2D
      const dx = ci - oi, dy = cj - oj, n = Math.max(Math.abs(dx), Math.abs(dy));
      const lim = Math.min(n - 1, 45);
      for (let s = 0; s <= lim; s++) {
        const k = this.idx(oi + Math.round(dx * s / n), oj + Math.round(dy * s / n));
        if (k < 0) break;
        if (this.occ[k] >= 2) break;
        if (!this.lib[k]) { this.lib[k] = 1; this.costoSporco = true; }
        this.vistoT[k] = 1;
      }
      if (b === -1 && n <= 45 && !this.lib[kc] && this.occ[kc] < 2) { this.lib[kc] = 1; this.costoSporco = true; }
    }
    return nuovi;
  }
  aggiornaVisto(dt) {
    const a = Math.min(1, dt * this.velVisto);
    for (let k = 0; k < this.visto.length; k++) if (this.vistoT[k] && this.visto[k] < 1) this.visto[k] = Math.min(1, this.visto[k] + a);
    const b = Math.min(1, dt * this.velBox);
    for (let k = 0; k < this.boxVisto.length; k++) if (this.boxVistoT[k] && this.boxVisto[k] < 1) this.boxVisto[k] = Math.min(1, this.boxVisto[k] + b);
  }
  // costo A*: ostacoli gonfiati bloccati, fascia vicina penalizzata, ignoto attraversabile ma più caro
  costi() {
    if (!this.costoSporco) return this.costo;
    this.costoSporco = false;
    const { W, H } = this, c = this.costo, r = Math.ceil(GONFIA / RIS), r2 = Math.ceil(0.8 / RIS);
    for (let k = 0; k < c.length; k++) c[k] = this.lib[k] ? 1 : 2.2;
    for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) {
      if (this.occ[j * W + i] < 2) continue;
      for (let b = -r2; b <= r2; b++) for (let a = -r2; a <= r2; a++) {
        const ii = i + a, jj = j + b; if (ii < 0 || jj < 0 || ii >= W || jj >= H) continue;
        const d = Math.hypot(a, b) * RIS, k = jj * W + ii;
        if (d <= GONFIA) c[k] = Infinity; else if (c[k] !== Infinity) c[k] = Math.max(c[k], 1 + 5 * (0.8 - d) / (0.8 - GONFIA));
      }
    }
    // bordo dell'area
    for (let i = 0; i < W; i++) { c[i] = c[(H - 1) * W + i] = Infinity; }
    for (let j = 0; j < H; j++) { c[j * W] = c[j * W + W - 1] = Infinity; }
    return c;
  }
  // frontiere: celle libere confinanti con l'ignoto, raggruppate
  frontiere() {
    const { W, H } = this, c = this.costi(), f = new Uint8Array(W * H), lista = [];
    for (let j = 1; j < H - 1; j++) for (let i = 1; i < W - 1; i++) {
      const k = j * W + i;
      if (!this.lib[k] || this.occ[k] >= 2 || c[k] === Infinity) continue;
      const ign = (q) => !this.lib[q] && this.occ[q] < 2;
      if (ign(k - 1) || ign(k + 1) || ign(k - W) || ign(k + W)) { f[k] = 1; lista.push(k); }
    }
    const gruppi = [], fatto = new Uint8Array(W * H);
    for (const k0 of lista) {
      if (fatto[k0]) continue;
      const g = [], coda = [k0]; fatto[k0] = 1;
      while (coda.length) {
        const k = coda.pop(); g.push(k);
        const i = k % W, j = (k / W) | 0;
        for (let b = -1; b <= 1; b++) for (let a = -1; a <= 1; a++) {
          const q = (j + b) * W + i + a; if (q >= 0 && q < W * H && f[q] && !fatto[q]) { fatto[q] = 1; coda.push(q); }
        }
      }
      if (g.length >= 4) gruppi.push(g);
    }
    return { celle: gruppi.flat(), gruppi };
  }
}

// A* 8-connesso sulla griglia dei costi (come _astar di navigatore_slam.py)
export function astar(mappa, da, a) {
  const { W, H } = mappa, c = mappa.costi();
  let [si, sj] = mappa.cella(da[0], da[1]), [gi, gj] = mappa.cella(a[0], a[1]);
  const s = mappa.idx(si, sj); let g = mappa.idx(gi, gj);
  if (s < 0 || g < 0) return null;
  if (c[g] === Infinity) {    // meta dentro un ostacolo gonfiato: cella libera più vicina
    let best = -1, bd = 1e9;
    for (let r = 1; r < 8 && best < 0; r++) for (let b = -r; b <= r; b++) for (let q = -r; q <= r; q++) {
      const k = mappa.idx(gi + q, gj + b); if (k >= 0 && c[k] !== Infinity) { const d = q * q + b * b; if (d < bd) { bd = d; best = k; } }
    }
    if (best < 0) return null; g = best; gi = g % W; gj = (g / W) | 0;
  }
  const N = W * H, gs = new Float32Array(N).fill(Infinity), da_ = new Int32Array(N).fill(-1), chiuso = new Uint8Array(N);
  const heap = [], push = (k, f) => { heap.push([f, k]); let i = heap.length - 1; while (i > 0) { const p = (i - 1) >> 1; if (heap[p][0] <= heap[i][0]) break; [heap[p], heap[i]] = [heap[i], heap[p]]; i = p; } };
  const pop = () => { const top = heap[0], last = heap.pop(); if (heap.length) { heap[0] = last; let i = 0; for (;;) { const l = 2 * i + 1, r = l + 1; let m = i; if (l < heap.length && heap[l][0] < heap[m][0]) m = l; if (r < heap.length && heap[r][0] < heap[m][0]) m = r; if (m === i) break; [heap[m], heap[i]] = [heap[i], heap[m]]; i = m; } } return top; };
  const h = (k) => { const i = k % W, j = (k / W) | 0; const dx = Math.abs(i - gi), dy = Math.abs(j - gj); return (dx + dy + (Math.SQRT2 - 2) * Math.min(dx, dy)); };
  gs[s] = 0; push(s, h(s)); let esplorate = 0;
  const avvio = c[s] === Infinity;   // se parte dentro la fascia gonfiata, può uscirne
  while (heap.length) {
    const [, k] = pop(); if (chiuso[k]) continue; chiuso[k] = 1; esplorate++;
    if (k === g) break;
    const i = k % W, j = (k / W) | 0;
    for (let b = -1; b <= 1; b++) for (let a2 = -1; a2 <= 1; a2++) {
      if (!a2 && !b) continue;
      const ii = i + a2, jj = j + b; if (ii < 0 || jj < 0 || ii >= W || jj >= H) continue;
      const q = jj * W + ii; let cq = c[q];
      if (cq === Infinity) { if (!(avvio && gs[k] < 3)) continue; cq = 6; }
      if (a2 && b && (c[j * W + ii] === Infinity || c[jj * W + i] === Infinity) && !avvio) continue;
      const ng = gs[k] + cq * (a2 && b ? Math.SQRT2 : 1);
      if (ng < gs[q]) { gs[q] = ng; da_[q] = k; push(q, ng + h(q)); }
    }
  }
  if (!chiuso[g]) return null;
  const celle = []; for (let k = g; k >= 0; k = da_[k]) celle.push(k);
  celle.reverse();
  // da celle a punti, poi accorcia con linea di vista sulla griglia
  const pts = celle.map((k) => mappa.centro(k % W, (k / W) | 0));
  const libera = (p, q) => {
    const n = Math.ceil(Math.hypot(q[0] - p[0], q[1] - p[1]) / (RIS * 0.5));
    for (let s2 = 1; s2 < n; s2++) { const [i, j] = mappa.cella(p[0] + (q[0] - p[0]) * s2 / n, p[1] + (q[1] - p[1]) * s2 / n); const k = mappa.idx(i, j); if (k < 0 || c[k] > 2.3) return false; }
    return true;
  };
  const corto = [pts[0]]; let i0 = 0;
  while (i0 < pts.length - 1) {
    let j = pts.length - 1; while (j > i0 + 1 && !libera(pts[i0], pts[j])) j--;
    corto.push(pts[j]); i0 = j;
  }
  corto[0] = [da[0], da[1]];
  let lung = 0; for (let k = 1; k < corto.length; k++) lung += Math.hypot(corto[k][0] - corto[k - 1][0], corto[k][1] - corto[k - 1][1]);
  return { punti: corto, celle: celle.length, esplorate, lung };
}

// LiDAR Unitree L2 (4D, 360° x 96°): direzioni non ripetitive, rumore 2 cm, sul muso del cane
export class Lidar {
  constructor(seed = 3) { this.r = rng(seed); this.raggiScan = 1100; this.portata = 30; }
  scansione(mondo, ox, oy, oz, yaw) {
    const n = this.raggiScan, xyz = new Float32Array(n * 3), b = new Int16Array(n); let m = 0, liberi = 0;
    for (let k = 0; k < n; k++) {
      const az = this.r() * Math.PI * 2;
      const el = Math.asin(this.r() * (Math.sin(0.79) + Math.sin(0.9)) - Math.sin(0.9)); // -52° .. +45°
      const ce = Math.cos(el), dx = ce * Math.cos(az + yaw), dy = ce * Math.sin(az + yaw), dz = Math.sin(el);
      const h = mondo.raggio(ox, oy, oz, dx, dy, dz, this.portata);
      if (!h || h.t < 0.3) continue;
      if (h.t > 2.0 && h.b !== -1) liberi++;
      const t = h.t + (this.r() - 0.5) * 0.04;
      xyz[m * 3] = ox + dx * t; xyz[m * 3 + 1] = oy + dy * t; xyz[m * 3 + 2] = Math.max(0, oz + dz * t); b[m] = h.b; m++;
    }
    return { n: m, xyz, b, liberi };
  }
}

// Cane: cinematica uniciclo (vx, wz) con limiti come la sport mode, inseguimento del percorso
export class Cane {
  constructor(x, y, yaw) {
    this.x = x; this.y = y; this.yaw = yaw; this.v = 0; this.w = 0; this.vmax = 0.6;
    this.percorso = null; this.iSeg = 1; this.guida = [x, y]; this.err = 0; this.dist = 0;
  }
  passo(dt, mondo) {
    let vc = 0, wc = 0;
    const P = this.percorso;
    if (P && P.length > 1) {
      // punto guida a 0,9 m lungo il percorso (pure pursuit)
      while (this.iSeg < P.length - 1 && Math.hypot(P[this.iSeg][0] - this.x, P[this.iSeg][1] - this.y) < 0.5) this.iSeg++;
      let g = P[this.iSeg];
      const fine = P[P.length - 1], dFine = Math.hypot(fine[0] - this.x, fine[1] - this.y);
      const a = P[this.iSeg - 1], ab = [g[0] - a[0], g[1] - a[1]], L = Math.hypot(...ab) || 1;
      let s = ((this.x - a[0]) * ab[0] + (this.y - a[1]) * ab[1]) / L + 0.9;
      if (s < L) g = [a[0] + ab[0] * s / L, a[1] + ab[1] * s / L];
      this.guida = g;
      let err = Math.atan2(g[1] - this.y, g[0] - this.x) - this.yaw;
      err = Math.atan2(Math.sin(err), Math.cos(err)); this.err = err;
      wc = Math.max(-1.2, Math.min(1.2, 2.2 * err));
      vc = Math.abs(err) > 1.0 ? 0 : this.vmax * Math.max(0, Math.cos(err)) ** 2 * Math.min(1, dFine / 0.6 + 0.25);
      if (dFine < 0.18) { this.percorso = null; vc = 0; wc = 0; this.arrivato = true; }
    }
    // rampe come la sport mode
    const av = 1.2 * dt, aw = 3.0 * dt;
    this.v += Math.max(-av, Math.min(av, vc - this.v)); this.w += Math.max(-aw, Math.min(aw, wc - this.w));
    const nx = this.x + Math.cos(this.yaw) * this.v * dt, ny = this.y + Math.sin(this.yaw) * this.v * dt;
    if (mondo.distanza(nx, ny) > 0.22) { this.x = nx; this.y = ny; this.dist += Math.abs(this.v) * dt; } else { this.v = 0; this.bloccato = true; }
    this.yaw += this.w * dt;
    this.yaw = Math.atan2(Math.sin(this.yaw), Math.cos(this.yaw));
  }
}
