// Postazione di magazzino stilizzata (Z in alto, metri): tavolo, cassetta rossa con manico, nastro a rulli,
// scatola con lembi, nastratrice, quadro NASTRO 1, scaffale. Proporzioni dalla scena Isaac di ~/g1_prompt.
import * as THREE from 'three';

export const LAYOUT = {
  home: { x: -1.35, y: 0.05, yaw: 0 },
  table: { x: -0.35, y: 1.28, w: 1.2, d: 0.66, h: 0.74 },
  box: { x: -0.32, y: 1.16, L: 0.42, W: 0.2, H: 0.16, hh: 0.065 },
  conv: { x0: -0.9, x1: 4.9, y: -0.95, w: 0.5, z: 0.5 },
  carton: { x: 1.25, L: 0.48, W: 0.34, H: 0.27 },
  taper: { x: 3.45 },
  panel: { x: 2.45, y: -0.3, z: 1.08 },
  ship: 4.45,
};

const M = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.6, metalness: 0.05, ...o });
function box(w, d, h, mat, x, y, z, parent) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, d, h), mat);
  m.position.set(x, y, z); m.castShadow = true; m.receiveShadow = true; parent && parent.add(m); return m;
}
function cyl(r, h, mat, parent, seg = 20) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, seg), mat);
  m.castShadow = true; m.receiveShadow = true; parent && parent.add(m); return m;
}
function labelTex(lines, { w = 512, h = 128, bg = '#f2c200', fg = '#111', font = '800 64px Archivo', align = 'center' } = {}) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const g = c.getContext('2d'); g.fillStyle = bg; g.fillRect(0, 0, w, h);
  g.fillStyle = fg; g.font = font; g.textAlign = align; g.textBaseline = 'middle';
  const L = Array.isArray(lines) ? lines : [lines];
  L.forEach((s, i) => g.fillText(s, align === 'center' ? w / 2 : 24, h * (i + 1) / (L.length + 1)));
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}
function plane(w, h, tex, parent) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshStandardMaterial({ map: tex, roughness: 0.7 }));
  parent && parent.add(m); return m;
}

export function buildScene(scene) {
  const W = { objs: {} };
  const L = LAYOUT;
  // pavimento: resina grigio-blu come la scena Isaac, giunti e corsie gialle
  const fc = document.createElement('canvas'); fc.width = fc.height = 1024;
  const g = fc.getContext('2d');
  g.fillStyle = '#2f3a46'; g.fillRect(0, 0, 1024, 1024);
  for (let i = 0; i < 2600; i++) { g.fillStyle = `rgba(${Math.random() < .5 ? '255,255,255' : '0,0,0'},${Math.random() * 0.035})`; g.fillRect(Math.random() * 1024, Math.random() * 1024, 2 + Math.random() * 30, 1 + Math.random() * 3); }
  g.strokeStyle = 'rgba(15,20,26,.55)'; g.lineWidth = 3; g.strokeRect(0, 0, 1024, 1024);
  const ft = new THREE.CanvasTexture(fc); ft.wrapS = ft.wrapT = THREE.RepeatWrapping; ft.repeat.set(14, 14); ft.colorSpace = THREE.SRGBColorSpace; ft.anisotropy = 8;
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(56, 56), new THREE.MeshStandardMaterial({ map: ft, roughness: 0.42, metalness: 0.1 }));
  floor.receiveShadow = true; scene.add(floor);
  const yel = M(0xe8b400, { roughness: 0.5 }), blk = M(0x15171a);
  // corsie pedonali gialle
  for (const [x, y, w, d] of [[1.6, 0.62, 7.6, 0.06], [1.6, -2.05, 7.6, 0.06], [-2.15, -0.7, 0.06, 2.7]]) box(w, d, 0.004, yel, x, y, 0.002, scene).castShadow = false;
  // strisce zebrate davanti al nastro
  const zc = document.createElement('canvas'); zc.width = 256; zc.height = 32; const zg = zc.getContext('2d');
  for (let i = -2; i < 18; i++) { zg.fillStyle = i % 2 ? '#e8b400' : '#15171a'; zg.beginPath(); zg.moveTo(i * 16, 32); zg.lineTo(i * 16 + 16, 0); zg.lineTo(i * 16 + 32, 0); zg.lineTo(i * 16 + 16, 32); zg.fill(); }
  const zt = new THREE.CanvasTexture(zc); zt.colorSpace = THREE.SRGBColorSpace; zt.wrapS = THREE.RepeatWrapping; zt.repeat.set(8, 1);
  const zeb = new THREE.Mesh(new THREE.PlaneGeometry(5.6, 0.1), new THREE.MeshStandardMaterial({ map: zt, roughness: 0.6 }));
  zeb.position.set(2.0, -0.62, 0.003); zeb.receiveShadow = true; scene.add(zeb);

  // capannone: muro di fondo, pilastri, scaffalature porta-pallet sullo sfondo
  const wallM = M(0x6d747c, { roughness: 0.9 });
  box(40, 0.2, 9, wallM, 2, 9.5, 4.5, scene).castShadow = false;
  box(0.2, 30, 9, wallM, -12, 0, 4.5, scene).castShadow = false;
  box(0.2, 30, 9, wallM, 16, 0, 4.5, scene).castShadow = false;
  box(40, 0.2, 1.1, M(0x2c4f7c), 2, 9.38, 0.55, scene);
  const upr = M(0x2e6fb8, { roughness: 0.5, metalness: 0.3 }), beam = M(0xe07a1f, { roughness: 0.5, metalness: 0.2 });
  const card = M(0xc49a6c, { roughness: 0.85 }), card2 = M(0xb48a5c, { roughness: 0.85 });
  const rackRow = (x0, y, n, levels = 4) => {
    for (let i = 0; i <= n; i++) for (const dy of [0, 1.0]) box(0.08, 0.08, levels * 1.5 + 0.2, upr, x0 + i * 2.7, y + dy, (levels * 1.5 + 0.2) / 2, scene);
    for (let i = 0; i < n; i++) for (let l = 1; l <= levels; l++) {
      const z = l * 1.5 - 0.6; const cx = x0 + i * 2.7 + 1.35;
      for (const dy of [0, 1.0]) box(2.62, 0.08, 0.12, beam, cx, y + dy, z, scene).castShadow = false;
      for (let k = 0; k < 3; k++) if ((i * 7 + l * 3 + k) % 5 !== 0) {
        const hh = 0.5 + ((i + l + k) % 3) * 0.18;
        box(0.78, 0.9, hh, (i + k + l) % 2 ? card : card2, cx - 0.86 + k * 0.86, y + 0.5, z + 0.06 + hh / 2, scene).castShadow = false;
      }
    }
  };
  rackRow(-7.5, 7.8, 8); rackRow(-7.5, 5.4, 2); rackRow(5.6, 5.4, 3);
  // pilastri e luci a soffitto
  for (const x of [-6, 2, 10]) box(0.4, 0.4, 9, M(0xb9bec4), x, 3.2, 4.5, scene);
  const lampM = new THREE.MeshBasicMaterial({ color: 0xfff6e0 });
  for (const x of [-4, 0, 4, 8]) for (const y of [-2, 2, 6]) box(1.6, 0.25, 0.06, lampM, x, y, 8.4, scene).castShadow = false;

  // scaffale A con taniche (come la scena vera)
  const shelf = new THREE.Group(); shelf.position.set(-2.55, 2.35, 0); scene.add(shelf);
  for (const x of [-0.9, 0.9]) for (const y of [-0.25, 0.25]) box(0.06, 0.06, 2.0, upr, x, y, 1.0, shelf);
  for (const z of [0.25, 0.66, 1.05, 1.55]) { box(1.86, 0.56, 0.03, M(0xd9c7a3), 0, 0, z, shelf); box(1.86, 0.04, 0.08, M(0xe6c200), 0, -0.29, z, shelf).castShadow = false; }
  const tcol = [0x6fd38a, 0xf06e5e, 0xf2d03a];
  for (let i = 0; i < 6; i++) {
    const t = box(0.22, 0.14, 0.2, M(tcol[i % 3], { roughness: 0.4 }), -0.65 + i * 0.26, -0.05, 0.66 + 0.115, shelf);
    box(0.03, 0.03, 0.08, M(0x333333), 0, 0, 0.13, t); box(0.12, 0.025, 0.02, M(0x333333), 0, 0, 0.17, t);
    plane(0.16, 0.06, labelTex(['OLIO', 'SGRASS.', 'REFRIG.'][i % 3], { w: 256, h: 96, bg: '#f4f4f0', font: '700 44px Archivo' }), t).position.set(0, -0.0705, -0.01);
    t.children[t.children.length - 1].rotation.x = Math.PI / 2;
  }
  for (let i = 0; i < 4; i++) box(0.4, 0.42, 0.34, card, -0.66 + i * 0.44, 0, 0.27 + 0.17, shelf);
  for (let i = 0; i < 3; i++) box(0.5, 0.42, 0.36, card2, -0.55 + i * 0.55, 0, 1.06 + 0.18, shelf);
  const sA = plane(0.9, 0.22, labelTex('SCAFFALE A'), shelf); sA.position.set(0, -0.32, 1.85); sA.rotation.x = Math.PI / 2;

  // tavolo
  const T = L.table, steel = M(0x9da3aa, { metalness: 0.7, roughness: 0.35 });
  const table = new THREE.Group(); table.position.set(T.x, T.y, 0); scene.add(table);
  box(T.w, T.d, 0.04, M(0x4d5560, { roughness: 0.55, metalness: 0.2 }), 0, 0, T.h - 0.02, table);
  box(T.w, 0.02, 0.06, yel, 0, -T.d / 2, T.h - 0.04, table).castShadow = false;
  for (const sx of [-1, 1]) for (const sy of [-1, 1]) box(0.05, 0.05, T.h - 0.04, steel, sx * (T.w / 2 - 0.05), sy * (T.d / 2 - 0.05), (T.h - 0.04) / 2, table);
  box(T.w - 0.1, T.d - 0.1, 0.02, steel, 0, 0, 0.18, table);

  // cassetta attrezzi rossa con manico
  const B = L.box;
  const tb = new THREE.Group(); tb.name = 'cassetta';
  const red = M(0xd4302a, { roughness: 0.38, metalness: 0.1 }), dk = M(0x1d1f22, { roughness: 0.5 });
  box(B.L, B.W, B.H * 0.62, red, 0, 0, B.H * 0.31, tb);
  box(B.L + 0.006, B.W + 0.006, 0.012, dk, 0, 0, B.H * 0.62, tb);
  box(B.L, B.W, B.H * 0.36, red, 0, 0, B.H * 0.62 + B.H * 0.18 + 0.006, tb);
  for (const sx of [-1, 1]) { box(0.035, 0.02, 0.03, dk, sx * 0.17, -B.W / 2 - 0.006, B.H * 0.62, tb); }
  for (const sx of [-1, 1]) box(0.02, 0.03, B.hh, dk, sx * 0.1, 0, B.H + B.hh / 2, tb);
  const hb = cyl(0.014, 0.22, M(0xf2c200, { roughness: 0.4 }), tb); hb.rotation.z = Math.PI / 2; hb.position.set(0, 0, B.H + B.hh);
  scene.add(tb); W.objs.cassetta = tb;
  W.boxRest = new THREE.Vector3(B.x, B.y, T.h);

  // nastro a rulli
  const C = L.conv, cl = C.x1 - C.x0, cx = (C.x0 + C.x1) / 2;
  const conv = new THREE.Group(); scene.add(conv);
  const frameM = M(0x2f6db5, { roughness: 0.45, metalness: 0.3 });
  for (const s of [-1, 1]) { box(cl, 0.05, 0.12, frameM, cx, C.y + s * (C.w / 2 + 0.025), C.z - 0.04, conv); box(cl, 0.054, 0.02, yel, cx, C.y + s * (C.w / 2 + 0.025), C.z + 0.03, conv).castShadow = false; }
  for (let x = C.x0 + 0.2; x < C.x1; x += 0.9) for (const s of [-1, 1]) box(0.05, 0.05, C.z - 0.1, frameM, x, C.y + s * (C.w / 2), (C.z - 0.1) / 2, conv);
  const nR = Math.floor(cl / 0.085);
  const rG = new THREE.CylinderGeometry(0.024, 0.024, C.w, 14); rG.rotateX(0);
  const rollers = new THREE.InstancedMesh(rG, M(0xb9c0c8, { metalness: 0.85, roughness: 0.28 }), nR);
  const m4 = new THREE.Matrix4();
  for (let i = 0; i < nR; i++) { m4.makeTranslation(C.x0 + 0.05 + i * 0.085, C.y, C.z - 0.024); rollers.setMatrixAt(i, m4); }
  rollers.castShadow = true; rollers.receiveShadow = true; conv.add(rollers);
  // fasce di movimento (si vedono scorrere quando il nastro è in marcia)
  const stc = document.createElement('canvas'); stc.width = 256; stc.height = 16; const sg = stc.getContext('2d');
  sg.fillStyle = 'rgba(0,0,0,0)'; sg.fillRect(0, 0, 256, 16); sg.fillStyle = 'rgba(242,194,0,.9)';
  for (let i = 0; i < 4; i++) sg.fillRect(i * 64, 0, 18, 16);
  const stt = new THREE.CanvasTexture(stc); stt.wrapS = THREE.RepeatWrapping; stt.repeat.set(cl / 0.6, 1);
  const flow = new THREE.Mesh(new THREE.PlaneGeometry(cl, 0.016), new THREE.MeshBasicMaterial({ map: stt, transparent: true, opacity: 0 }));
  flow.position.set(cx, C.y - C.w / 2 - 0.053, C.z + 0.0); flow.rotation.x = Math.PI / 2; conv.add(flow);
  W.flow = flow; W.flowTex = stt;

  // scatola di cartone con 4 lembi incernierati
  const K = L.carton, kraft = M(0xc79a63, { roughness: 0.88 }), kraftIn = M(0xa77c4a, { roughness: 0.9, side: THREE.DoubleSide });
  const cart = new THREE.Group(); cart.name = 'scatola';
  const th = 0.008;
  box(K.L, K.W, th, kraftIn, 0, 0, th / 2, cart);
  for (const s of [-1, 1]) { box(K.L, th, K.H, kraft, 0, s * K.W / 2, K.H / 2, cart); box(th, K.W, K.H, kraft, s * K.L / 2, 0, K.H / 2, cart); }
  const lab = plane(0.16, 0.08, labelTex(['ORDINE 4512', '▮▮▯▮▯▮▮▯▮'], { w: 256, h: 128, bg: '#f4f4f0', font: '700 34px JetBrains Mono' }), cart);
  lab.position.set(0.08, -K.W / 2 - 0.006, K.H * 0.55); lab.rotation.x = Math.PI / 2;
  const flaps = [];
  const mkFlap = (len, wid, px, py, axis, sign) => {
    const piv = new THREE.Group(); piv.position.set(px, py, K.H); cart.add(piv);
    const f = box(axis === 'x' ? len : wid, axis === 'x' ? wid : len, th, kraftIn, 0, 0, 0, piv);
    if (axis === 'x') f.position.y = sign * wid / 2; else f.position.x = sign * wid / 2;
    piv.userData = { axis, sign }; flaps.push(piv); return piv;
  };
  mkFlap(K.L, K.W / 2, 0, -K.W / 2, 'x', 1); mkFlap(K.L, K.W / 2, 0, K.W / 2, 'x', -1);
  mkFlap(K.W, K.L / 2 * 0.6, -K.L / 2, 0, 'y', 1); mkFlap(K.W, K.L / 2 * 0.6, K.L / 2, 0, 'y', -1);
  W.setFlaps = (open) => { // open 1 = aperti (a 110° verso l'esterno), 0 = chiusi
    flaps.forEach((p, i) => {
      const a = (Math.PI - 0.35) * Math.min(1, Math.max(0, open * (i < 2 ? 1 : 1.0)));
      if (p.userData.axis === 'x') p.rotation.x = -p.userData.sign * a; else p.rotation.y = p.userData.sign * a;
    });
  };
  const tape = box(K.L + 0.02, 0.05, 0.003, M(0xc8b38a, { roughness: 0.3, metalness: 0.05, transparent: true, opacity: 0.92 }), 0, 0, K.H + th + 0.002, cart);
  tape.scale.x = 0.001; W.tape = tape;
  scene.add(cart); W.objs.scatola = cart;
  W.cartonZ = C.z;

  // nastratrice (bianca, fasce gialle, rotolo di scotch in cima) a cavallo del nastro
  const NT = new THREE.Group(); NT.position.set(L.taper.x, C.y, 0); scene.add(NT);
  const white = M(0xeceeef, { roughness: 0.55 });
  const tw = 0.95, td = 0.98, thh = 1.3, op = 0.64, oh = 0.46;
  box(tw, (td - op) / 2, thh, white, 0, -(op / 2 + (td - op) / 4), thh / 2, NT);
  box(tw, (td - op) / 2, thh, white, 0, (op / 2 + (td - op) / 4), thh / 2, NT);
  box(tw, op, thh - (C.z + oh), white, 0, 0, (C.z + oh) + (thh - C.z - oh) / 2, NT);
  box(tw, op, C.z - 0.06, white, 0, 0, (C.z - 0.06) / 2, NT);
  for (const z of [0.42, 1.0]) for (const s of [-1, 1]) box(tw + 0.004, 0.006, 0.06, yel, 0, s * (td / 2 + 0.002), z, NT).castShadow = false;
  box(tw + 0.01, td + 0.01, 0.05, yel, 0, 0, thh + 0.02, NT);
  for (let i = 0; i < 6; i++) box(0.012, op / 6 - 0.01, oh * 0.62, M(0x2b2e33, { roughness: 0.8 }), -tw / 2 - 0.01, -op / 2 + op / 12 + i * op / 6, C.z + oh * 0.69, NT);
  const roll = cyl(0.11, 0.06, M(0xe9dcc0, { roughness: 0.6 }), NT, 28); roll.position.set(0, 0, thh + 0.16); roll.rotation.x = Math.PI / 2;
  const core = cyl(0.045, 0.062, M(0x5a4636), NT); core.position.copy(roll.position); core.rotation.x = Math.PI / 2;
  const ntl = plane(0.5, 0.11, labelTex('NASTRATRICE', { bg: '#15171a', fg: '#f2c200', font: '800 60px Archivo' }), NT);
  ntl.position.set(0, -td / 2 - 0.004, 1.18); ntl.rotation.x = Math.PI / 2;
  W.taperRoll = roll;

  // quadro NASTRO 1 su palo, pulsanti a fungo
  const P = L.panel;
  const pan = new THREE.Group(); pan.position.set(P.x, P.y, 0); pan.rotation.z = Math.PI / 2; scene.add(pan); // fronte verso -x
  cyl(0.03, P.z - 0.12, steel, pan).rotation.x = Math.PI / 2; pan.children[0].position.z = (P.z - 0.12) / 2;
  box(0.36, 0.12, 0.26, white, 0, 0, P.z, pan);
  const pl = plane(0.3, 0.07, labelTex('NASTRO 1', { bg: '#eceeef', fg: '#15171a', font: '800 70px Archivo' }), pan);
  pl.position.set(0, 0.061, P.z + 0.085); pl.rotation.x = -Math.PI / 2; pl.rotation.x = Math.PI / 2; pl.rotation.y = Math.PI;
  const bcols = [0x2fbf5a, 0xe23b30, 0xf2c200, 0x3a8ee6], btn = [];
  for (let i = 0; i < 4; i++) {
    const base = cyl(0.026, 0.02, M(0x222428), pan); base.rotation.x = Math.PI / 2; base.position.set(0.12 - i * 0.08, 0.07, P.z - 0.01);
    const cap = cyl(0.021, 0.022, M(bcols[i], { roughness: 0.3, emissive: bcols[i], emissiveIntensity: 0.12 }), pan); cap.rotation.x = Math.PI / 2; cap.position.set(0.12 - i * 0.08, 0.088, P.z - 0.01);
    btn.push(cap);
  }
  const bl = plane(0.34, 0.035, labelTex('AVVIO   STOP   RESET   SCATOLA', { w: 1024, h: 104, bg: '#eceeef', fg: '#222', font: '700 52px JetBrains Mono' }), pan);
  bl.position.set(0, 0.061, P.z - 0.075); bl.rotation.x = Math.PI / 2; bl.rotation.y = Math.PI;
  W.buttons = btn; W.buttonPos = i => new THREE.Vector3(P.x - 0.1, P.y + 0.12 - i * 0.08, P.z - 0.01);
  const beacon = cyl(0.03, 0.08, M(0x2fbf5a, { emissive: 0x2fbf5a, emissiveIntensity: 0.0, transparent: true, opacity: 0.9 }), pan);
  beacon.rotation.x = Math.PI / 2; beacon.position.set(0.14, 0, P.z + 0.18); W.beacon = beacon;

  // cartelli appesi
  const sign = (txt, bg, x, y, z) => { const s = plane(0.84, 0.2, labelTex(txt, { bg, fg: '#111' }), scene); s.position.set(x, y, z); s.rotation.x = Math.PI / 2; return s; };
  sign('IMBALLAGGIO', '#f08a24', 1.25, -1.35, 2.05); sign('SPEDIZIONI', '#2fbf5a', 4.9, -1.35, 2.05);
  for (const x of [1.25, 4.9]) { const r = cyl(0.008, 6.3, steel, scene, 6); r.position.set(x, -1.35, 5.2); r.rotation.x = Math.PI / 2; }
  // pallet con scatole spedite in fondo al nastro
  box(1.0, 0.8, 0.12, M(0x8a6a44), 5.6, -0.95, 0.06, scene);
  for (let i = 0; i < 3; i++) box(0.46, 0.34, 0.27, kraft, 5.35 + (i % 2) * 0.5, -1.12 + Math.floor(i / 2) * 0.36, 0.255, scene);

  return W;
}

// marcatori gialli: target IK, percorso a terra, impronte
export function buildMarkers(scene) {
  const Y = 0xf2c200;
  const grp = new THREE.Group(); scene.add(grp);
  const mk = () => {
    const g = new THREE.Group();
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.045, 0.004, 8, 36), new THREE.MeshBasicMaterial({ color: Y, transparent: true, opacity: 0.95, depthTest: false }));
    const ring2 = ring.clone(); ring2.rotation.x = Math.PI / 2;
    const dot = new THREE.Mesh(new THREE.SphereGeometry(0.011, 10, 8), new THREE.MeshBasicMaterial({ color: Y, depthTest: false }));
    const lineG = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
    const line = new THREE.Line(lineG, new THREE.LineDashedMaterial({ color: Y, dashSize: 0.02, gapSize: 0.015, transparent: true, opacity: 0.8, depthTest: false }));
    g.add(ring, ring2, dot); g.renderOrder = 10; [ring, ring2, dot, line].forEach(o => o.renderOrder = 10);
    grp.add(g); grp.add(line); g.userData.line = line; g.visible = false; line.visible = false; return g;
  };
  const M = { hand: { L: mk(), R: mk() } };
  // percorso a terra
  const pathMat = new THREE.LineDashedMaterial({ color: Y, dashSize: 0.08, gapSize: 0.05, transparent: true, opacity: 0.9 });
  const path = new THREE.Line(new THREE.BufferGeometry(), pathMat); path.position.z = 0.006; grp.add(path); M.path = path;
  const goal = new THREE.Mesh(new THREE.RingGeometry(0.16, 0.19, 40), new THREE.MeshBasicMaterial({ color: Y, transparent: true, opacity: 0.9, side: THREE.DoubleSide }));
  goal.position.z = 0.007; grp.add(goal); M.goal = goal;
  const arrow = new THREE.Mesh(new THREE.ConeGeometry(0.05, 0.12, 3), goal.material); arrow.rotation.z = -Math.PI / 2; goal.add(arrow); arrow.position.x = 0.27;
  M.setPath = (pts, end) => {
    if (!pts) { path.visible = false; goal.visible = false; return; }
    path.geometry.dispose(); path.geometry = new THREE.BufferGeometry().setFromPoints(pts.map(p => new THREE.Vector3(p.x, p.y, 0)));
    path.computeLineDistances(); path.visible = true;
    goal.visible = true; goal.position.set(end.x, end.y, 0.007); goal.rotation.z = end.yaw;
  };
  M.setHand = (s, tgt, from, vis) => {
    const g = M.hand[s]; g.visible = vis; g.userData.line.visible = vis;
    if (!vis) return;
    g.position.copy(tgt);
    const pa = g.userData.line.geometry.attributes.position; pa.setXYZ(0, from.x, from.y, from.z); pa.setXYZ(1, tgt.x, tgt.y, tgt.z); pa.needsUpdate = true;
    g.userData.line.computeLineDistances();
  };
  // impronte dei passi
  const fpM = new THREE.MeshBasicMaterial({ color: Y, transparent: true, opacity: 0.5 });
  const fpG = new THREE.PlaneGeometry(0.2, 0.075);
  M.feet = []; for (let i = 0; i < 16; i++) { const f = new THREE.Mesh(fpG, fpM.clone()); f.position.z = 0.008; f.visible = false; grp.add(f); M.feet.push(f); }
  M.group = grp;
  return M;
}
