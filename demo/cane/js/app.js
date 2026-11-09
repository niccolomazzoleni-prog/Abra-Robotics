// Console Go2 — vetrina 3D. Dati veri: mondi di pc_tools/mondo_sim.py, mesh Go2 di unitree_mujoco (decimate),
// camminata registrata dalla policy go2_deploy/models/policy_ts_gs.pt in MuJoCo, marcatori ArUco DICT_4X4_50.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { toCreasedNormals } from 'three/addons/utils/BufferGeometryUtils.js';
import { Mondo, Mappa, Lidar, Cane, astar, rng, RIS } from './sim.js';

THREE.Object3D.DEFAULT_UP.set(0, 0, 1);
const Q = new URLSearchParams(location.search);
const REGIA = Q.get('regia') === '1';
const SALTA = +(Q.get('salta') || 0);
const LITE = Q.get('lite') === '1';
const DURATA = 45;
const $ = (s) => document.querySelector(s);
if (REGIA) document.body.classList.add('regia');

// marcatori ArUco veri DICT_4X4_50 (cv2.aruco.generateImageMarker, 6x6 col bordo nero)
const ARUCO = { 3: '000000010010010010001000001100000000', 7: '000000011000001000011110000100000000', 8: '000000011110011100011010010100000000', 11: '000000000010000010010100001110000000', 12: '000000000000011100010110001110000000', 21: '000000010110000000000100010110000000' };

// ---------------------------------------------------------------- renderer
const canvas = $('#vista');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance', preserveDrawingBuffer: false });
renderer.setPixelRatio(REGIA ? 1 : Math.min(devicePixelRatio, 1.75));
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 0.95;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x07080a);
scene.fog = new THREE.FogExp2(0x07080a, 0.018);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.35;
const camera = new THREE.PerspectiveCamera(40, 16 / 9, 0.05, 400);
camera.layers.enable(1);
const camRS = new THREE.PerspectiveCamera(42, 16 / 9, 0.08, 60);   // RealSense D435i (colore 69° x 42°)
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true; controls.dampingFactor = 0.08; controls.maxPolarAngle = Math.PI * 0.47; controls.minDistance = 1.2; controls.maxDistance = 90;
controls.enabled = !REGIA;
controls.addEventListener('start', () => { if (segui) { segui = false; document.querySelector('#bSegui')?.classList.remove('on'); } });

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(512, 512), 0.6, 0.5, 0.78);
if (!LITE) composer.addPass(bloom);
composer.addPass(new OutputPass());

scene.add(new THREE.HemisphereLight(0x9fb3c8, 0x0b0b0c, 0.32));
const sole = new THREE.DirectionalLight(0xfff4e0, 0.85); sole.position.set(-8, -12, 22); scene.add(sole);
const luceCane = new THREE.PointLight(0xffe7b0, 2.5, 6, 1.6);   // luce di cortesia sul cane (si vede anche al buio)
scene.add(luceCane);

// ---------------------------------------------------------------- uniformi condivise (rivelazione del mondo)
const U = {
  uVisto: { value: null }, uBox: { value: null }, uNBox: { value: 1 }, uG: { value: new THREE.Vector4() },
  uLim: { value: new THREE.Vector4() }, uForza: { value: 0 }, uGhost: { value: REGIA ? 0.0 : 0.07 }, uT: { value: 0 },
};
function rivela(mat, conBox) {
  mat.onBeforeCompile = (sh) => {
    for (const k in U) sh.uniforms[k] = U[k];
    sh.vertexShader = sh.vertexShader
      .replace('#include <common>', '#include <common>\nvarying vec3 vWP;' + (conBox ? '\nattribute float bid; varying float vBid;' : ''))
      .replace('#include <fog_vertex>', '#include <fog_vertex>\nvWP = (modelMatrix * vec4(transformed, 1.0)).xyz;' + (conBox ? ' vBid = bid;' : ''));
    sh.fragmentShader = sh.fragmentShader
      .replace('#include <common>', '#include <common>\nuniform sampler2D uVisto; uniform sampler2D uBox; uniform float uNBox, uForza, uGhost, uT; uniform vec4 uG; varying vec3 vWP;' + (conBox ? ' varying float vBid;' : ''))
      .replace('#include <dithering_fragment>', `
        float rv = texture2D(uVisto, (vWP.xy - uG.xy) / uG.zw).r;
        ${conBox ? 'rv = max(rv, texture2D(uBox, vec2((vBid + 0.5) / uNBox, 0.5)).r);' : ''}
        float rr = max(rv, uForza);
        vec3 bordo = vec3(0.37, 0.83, 0.9) * smoothstep(0.0, 0.3, rv) * (1.0 - smoothstep(0.3, 1.0, rv)) * 0.14 * (1.0 - uForza);
        gl_FragColor.rgb = gl_FragColor.rgb * mix(uGhost, 1.0, rr) + bordo;
        #include <dithering_fragment>`);
  };
  mat.customProgramCacheKey = () => 'rivela' + (conBox ? 'B' : '');
  return mat;
}

// ---------------------------------------------------------------- caricamento
const [MONDI, ANIM, MESH] = await Promise.all([
  fetch('dati/mondi.json').then((r) => r.json()), fetch('dati/go2_anim.json').then((r) => r.json()), fetch('dati/go2_mesh.bin').then((r) => r.arrayBuffer())]);

// ---------------------------------------------------------------- Go2 (mesh vere)
const cane3d = new THREE.Group(); scene.add(cane3d);
const base3d = new THREE.Group(); cane3d.add(base3d);
const corpi = ANIM.corpi.map(() => { const g = new THREE.Group(); base3d.add(g); return g; });
const materiali = {};
function materiale(rgba) {
  const k = rgba.join(',');
  if (!materiali[k]) {
    const [r, g, b] = rgba; let m;
    if (r < 0.05) m = new THREE.MeshStandardMaterial({ color: 0x141518, roughness: 0.62, metalness: 0.05, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1 });
    else if (r > 0.99) m = new THREE.MeshStandardMaterial({ color: 0xe9e9e6, roughness: 0.55, metalness: 0.0, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1 });
    else if (r > 0.85) m = new THREE.MeshStandardMaterial({ color: 0xb9bcbf, roughness: 0.45, metalness: 0.15 });
    else if (r < 0.2) m = new THREE.MeshStandardMaterial({ color: 0x1c1d20, roughness: 0.5, metalness: 0.2 });
    else m = new THREE.MeshStandardMaterial({ color: 0x9a9fa6, roughness: 0.55, metalness: 0.08 });
    materiali[k] = m;
  }
  return materiali[k];
}
for (const c of ANIM.mesh) {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(MESH, c.vo, c.vn * 3), 3));
  g.setIndex(new THREE.BufferAttribute(c.it === 'u16' ? new Uint16Array(MESH, c.io, c.in) : new Uint32Array(MESH, c.io, c.in), 1));
  corpi[c.b].add(new THREE.Mesh(toCreasedNormals(g, 0.7), materiale(c.rgba)));
}
// clip: F x B x 7 (pos, quat MuJoCo wxyz) -> quaternioni three
function preparaClip(c) {
  const B = ANIM.corpi.length, F = c.n, p = new Float32Array(F * B * 3), q = new Float32Array(F * B * 4);
  for (let f = 0; f < F; f++) for (let b = 0; b < B; b++) {
    const r = c.rel[f], o = b * 7;
    p.set([r[o], r[o + 1], r[o + 2]], (f * B + b) * 3);
    q.set([r[o + 4], r[o + 5], r[o + 6], r[o + 3]], (f * B + b) * 4);
  }
  return { F, B, p, q, base: c.base, v: c.v };
}
const CLIP = { cammina: preparaClip(ANIM.clip.cammina), fermo: preparaClip(ANIM.clip.fermo) };
const _qa = new THREE.Quaternion(), _qb = new THREE.Quaternion(), _qf = new THREE.Quaternion(), _pa = new THREE.Vector3(), _pb = new THREE.Vector3(), _pf = new THREE.Vector3();
const anima = { fase: 0, peso: 0 };
function posaCane(dt) {
  const s = (Math.abs(cane.v) + 0.3 * Math.abs(cane.w)) / CLIP.cammina.v;
  anima.fase = (anima.fase + dt * ANIM.fps * Math.max(s, anima.peso > 0.02 ? 0.35 : 0)) % CLIP.cammina.F;
  anima.peso += (Math.min(1, s * 4) - anima.peso) * Math.min(1, dt * 6);
  const C = CLIP.cammina, Fm = CLIP.fermo, f0 = Math.floor(anima.fase), f1 = (f0 + 1) % C.F, a = anima.fase - f0, w = anima.peso;
  for (let b = 0; b < C.B; b++) {
    _pa.fromArray(C.p, (f0 * C.B + b) * 3); _pb.fromArray(C.p, (f1 * C.B + b) * 3); _pa.lerp(_pb, a);
    _qa.fromArray(C.q, (f0 * C.B + b) * 4); _qb.fromArray(C.q, (f1 * C.B + b) * 4); _qa.slerp(_qb, a);
    _pf.fromArray(Fm.p, b * 3); _qf.fromArray(Fm.q, b * 4);
    corpi[b].position.copy(_pf.lerp(_pa, w)); corpi[b].quaternion.copy(_qf.slerp(_qa, w));
  }
  const b0 = C.base[f0], b1 = C.base[f1], bf = Fm.base[0], L = (i) => bf[i] + ((b0[i] + (b1[i] - b0[i]) * a) - bf[i]) * w;
  base3d.position.set(0, 0, L(0)); base3d.rotation.set(L(1), L(2), 0, 'ZYX');
  cane3d.position.set(cane.x, cane.y, 0); cane3d.rotation.set(0, 0, cane.yaw);
}
// anello giallo e ombra finta sotto il cane
const anello = new THREE.Mesh(new THREE.RingGeometry(0.52, 0.56, 64), new THREE.MeshBasicMaterial({ color: 0xf2c200, transparent: true, opacity: 0.85, depthWrite: false }));
anello.position.z = 0.012; anello.layers.set(1); cane3d.add(anello);
const freccia = new THREE.Mesh(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0.62, 0.12, 0), new THREE.Vector3(0.82, 0, 0), new THREE.Vector3(0.62, -0.12, 0)]).setIndex([0, 1, 2]),
  new THREE.MeshBasicMaterial({ color: 0xf2c200, side: THREE.DoubleSide }));
freccia.position.z = 0.012; freccia.layers.set(1); cane3d.add(freccia);
{
  const cv = document.createElement('canvas'); cv.width = cv.height = 64; const x = cv.getContext('2d');
  const gr = x.createRadialGradient(32, 32, 2, 32, 32, 32); gr.addColorStop(0, 'rgba(0,0,0,0.75)'); gr.addColorStop(1, 'rgba(0,0,0,0)');
  x.fillStyle = gr; x.fillRect(0, 0, 64, 64);
  const ombra = new THREE.Mesh(new THREE.PlaneGeometry(1.1, 0.7), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(cv), transparent: true, depthWrite: false }));
  ombra.position.z = 0.006; cane3d.add(ombra);
}

// ---------------------------------------------------------------- stato del mondo
let mondo, mappa, lidar, cane, mondo3d, R;   // R = rng di scena
let puntiGeo, scia, griglia, gTex, vTex, bTex, percorso3d, meta3d, marcatori = [], extra3d = [];
const S = { modo: REGIA ? 'fermo' : 'esplora', meta: null, missione: [], iMis: 0, zone: [], iZona: 0, pausa: 0, nero: [], fronti: { celle: [], gruppi: [] },
  bersaglio: null, scans: 0, nuovi: 0, storia: [], deriva: 0, driftAng: 0, ultimoAr: null, arVisti: [], batt: 86.4, lidarOn: !REGIA,
  tSim: 0, tLog: 0, tPlan: 0, tFront: 0, tGrid: 0, tScan: 0, tAr: 0, arOra: {}, percorsoInfo: null, esploraFine: false, area: 0 };

const piano = (w, h) => new THREE.PlaneGeometry(w, h);
function texPavimento() {
  const cv = document.createElement('canvas'); cv.width = cv.height = 512; const x = cv.getContext('2d');
  x.fillStyle = '#2a2c2f'; x.fillRect(0, 0, 512, 512);
  const r = rng(5);
  for (let i = 0; i < 9000; i++) { const v = 34 + r() * 18 | 0; x.fillStyle = `rgba(${v},${v + 1},${v + 3},0.35)`; x.fillRect(r() * 512, r() * 512, 1 + r() * 2, 1 + r() * 2); }
  x.strokeStyle = 'rgba(0,0,0,0.45)'; x.lineWidth = 2;
  for (let i = 0; i <= 4; i++) { x.beginPath(); x.moveTo(i * 128, 0); x.lineTo(i * 128, 512); x.stroke(); x.beginPath(); x.moveTo(0, i * 128); x.lineTo(512, i * 128); x.stroke(); }
  const t = new THREE.CanvasTexture(cv); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  return t;
}
const TEX_PAV = texPavimento();
function testoSprite(txt, col = '#f2c200', px = 96) {
  const cv = document.createElement('canvas'); cv.width = cv.height = 128; const x = cv.getContext('2d');
  x.font = `800 ${px}px Archivo, Arial Narrow, sans-serif`; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = col; x.fillText(txt, 64, 70);
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(cv), depthWrite: false, transparent: true }));
  s.layers.set(1); return s;
}
function texAruco(id) {
  const bits = ARUCO[id], cv = document.createElement('canvas'); cv.width = cv.height = 80; const x = cv.getContext('2d');
  x.fillStyle = '#f4f4f0'; x.fillRect(0, 0, 80, 80);
  for (let j = 0; j < 6; j++) for (let i = 0; i < 6; i++) if (bits[j * 6 + i] === '0') { x.fillStyle = '#0b0b0b'; x.fillRect(10 + i * 10, 10 + j * 10, 10, 10); }
  const t = new THREE.CanvasTexture(cv); t.magFilter = THREE.NearestFilter; t.colorSpace = THREE.SRGBColorSpace; return t;
}

function liberaScena() {
  for (const o of [mondo3d, puntiGeo, scia, griglia, percorso3d, meta3d, ...marcatori.map((m) => m.mesh), ...extra3d]) {
    if (!o) continue; scene.remove(o);
    o.traverse?.((c) => { c.geometry?.dispose(); });
  }
  marcatori = []; extra3d = [];
}
function caricaMondo(nome) {
  liberaScena();
  mondo = new Mondo(nome, MONDI[nome]); mappa = new Mappa(mondo); lidar = new Lidar(9);
  R = rng(17);
  const [px, py, pyaw] = mondo.partenza; cane = new Cane(px, py, pyaw);
  Object.assign(S, { meta: null, missione: [], iMis: 0, iZona: 0, pausa: 0, nero: [], bersaglio: null, scans: 0, storia: [], deriva: 0, ultimoAr: null, esploraFine: false, percorsoInfo: null });
  S.zone = Object.entries(mondo.zone).map(([k, z]) => ({ nome: k, x: z.x, y: z.y, stato: 'da fare' }));
  const [x0, x1, y0, y1] = mondo.limiti, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
  mondo3d = new THREE.Group(); scene.add(mondo3d);
  // texture rivelazione
  vTex = new THREE.DataTexture(new Uint8Array(mappa.W * mappa.H), mappa.W, mappa.H, THREE.RedFormat); vTex.magFilter = vTex.minFilter = THREE.LinearFilter; vTex.unpackAlignment = 1; vTex.needsUpdate = true;
  bTex = new THREE.DataTexture(new Uint8Array(mondo.n), mondo.n, 1, THREE.RedFormat); bTex.unpackAlignment = 1; bTex.needsUpdate = true;
  U.uVisto.value = vTex; U.uBox.value = bTex; U.uLim.value.set(x0, x1, y0, y1); U.uNBox.value = mondo.n; U.uG.value.set(mappa.x0, mappa.y0, mappa.W * RIS, mappa.H * RIS);
  // pavimento
  const pav = new THREE.Mesh(piano(x1 - x0 + 0.4, y1 - y0 + 0.4), rivela(new THREE.MeshStandardMaterial({ map: TEX_PAV, roughness: 0.82, metalness: 0.0 })));
  pav.material.map = TEX_PAV.clone(); pav.material.map.repeat.set((x1 - x0) / 4, (y1 - y0) / 4); pav.material.map.needsUpdate = true;
  pav.position.set(cx, cy, 0); mondo3d.add(pav);
  // scatole (stesse di mondo_sim.py), colori per tipo
  const box = new THREE.BoxGeometry(1, 1, 1).toNonIndexed();
  const bp = box.attributes.position.array, bn = box.attributes.normal.array;
  const muri = MONDI[nome].lo.length >= 4 ? 4 : 0;
  const recinto = (d) => Math.min(d[0], d[1]) < 0.12 && d[2] > 1.4;
  const geoScatole = (filtro) => {
    const pos = [], nor = [], col = [], bid = [];
    for (let i = 0; i < mondo.n; i++) {
      const lo = [mondo.lo[i * 3], mondo.lo[i * 3 + 1], mondo.lo[i * 3 + 2]], hi = [mondo.hi[i * 3], mondo.hi[i * 3 + 1], mondo.hi[i * 3 + 2]];
      if (i < muri) hi[2] = Math.min(hi[2], 1.1);       // muri perimetrali in sezione (il LiDAR usa l'altezza vera)
      const d = [hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]];
      if (!filtro(i, d)) continue;
      let hex;
      if (i < muri) hex = 0x2b2e32;
      else if (recinto(d)) hex = 0xf2c200;              // recinzione cella robot
      else if (d[2] > 2.4) hex = 0x30353b;              // presse, forno, scaffali
      else if (d[2] < 0.3) hex = 0x5a4029;              // bancali
      else hex = 0x44474b;
      const c = new THREE.Color(hex);
      for (let v = 0; v < bp.length; v += 3) {
        pos.push(lo[0] + (bp[v] + 0.5) * d[0], lo[1] + (bp[v + 1] + 0.5) * d[1], lo[2] + (bp[v + 2] + 0.5) * d[2]);
        nor.push(bn[v], bn[v + 1], bn[v + 2]);
        const top = bn[v + 2] > 0.5 ? 1.45 : 1; col.push(c.r * top, c.g * top, c.b * top); bid.push(i);
      }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); g.setAttribute('bid', new THREE.Float32BufferAttribute(bid, 1));
    return g;
  };
  mondo3d.add(new THREE.Mesh(geoScatole((i, d) => !recinto(d)), rivela(new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.66, metalness: 0.2 }), true)));
  mondo3d.add(new THREE.Mesh(geoScatole((i, d) => recinto(d)), rivela(new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.5, transparent: true, opacity: 0.28, depthWrite: false, side: THREE.DoubleSide }), true)));
  // spigoli
  const ep = [], eb = [];
  for (let i = 0; i < mondo.n; i++) {
    const lo = [mondo.lo[i * 3], mondo.lo[i * 3 + 1], mondo.lo[i * 3 + 2]], hi = [mondo.hi[i * 3], mondo.hi[i * 3 + 1], mondo.hi[i * 3 + 2]];
    if (i < muri) hi[2] = Math.min(hi[2], 1.1);
    const P = (a, b, c) => [a ? hi[0] : lo[0], b ? hi[1] : lo[1], c ? hi[2] : lo[2]];
    const E = [[0, 0, 0, 1, 0, 0], [0, 1, 0, 1, 1, 0], [0, 0, 1, 1, 0, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 1, 0], [1, 0, 0, 1, 1, 0], [0, 0, 1, 0, 1, 1], [1, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 0, 1], [0, 1, 0, 0, 1, 1], [1, 1, 0, 1, 1, 1]];
    for (const e of E) { ep.push(...P(e[0], e[1], e[2]), ...P(e[3], e[4], e[5])); eb.push(i, i); }
  }
  const ge = new THREE.BufferGeometry(); ge.setAttribute('position', new THREE.Float32BufferAttribute(ep, 3)); ge.setAttribute('bid', new THREE.Float32BufferAttribute(eb, 1));
  mondo3d.add(new THREE.LineSegments(ge, rivela(new THREE.LineBasicMaterial({ color: 0x8a939c, transparent: true, opacity: 0.55 }), true)));
  // strisce di sicurezza gialle sul pavimento attorno alle macchine alte
  for (let i = muri; i < mondo.n; i++) {
    const h = mondo.hi[i * 3 + 2], lx = mondo.hi[i * 3] - mondo.lo[i * 3], ly = mondo.hi[i * 3 + 1] - mondo.lo[i * 3 + 1];
    if (h < 2.4 || Math.min(lx, ly) < 0.5) continue;
    const linea = new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints([[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([a, b]) => new THREE.Vector3(a * (lx / 2 + 0.6), b * (ly / 2 + 0.6), 0))),
      rivela(new THREE.LineBasicMaterial({ color: 0xd8b000 })));
    linea.position.set((mondo.lo[i * 3] + mondo.hi[i * 3]) / 2, (mondo.lo[i * 3 + 1] + mondo.hi[i * 3 + 1]) / 2, 0.008); mondo3d.add(linea);
  }
  // zone di pattuglia
  for (const z of S.zone) {
    const anelloZ = new THREE.Mesh(new THREE.RingGeometry(0.62, 0.68, 48), new THREE.MeshBasicMaterial({ color: 0xf2c200, transparent: true, opacity: 0.7, depthWrite: false }));
    anelloZ.position.set(z.x, z.y, 0.02); anelloZ.layers.set(1); mondo3d.add(anelloZ);
    const t = testoSprite(z.nome); t.position.set(z.x, z.y, 1.1); t.scale.set(0.6, 0.6, 0.6); mondo3d.add(t);
  }
  piazzaMarcatori();
  // nuvola di punti (mappa SLAM)
  const pg = new THREE.BufferGeometry();
  const pa = new THREE.BufferAttribute(mappa.pos, 3).setUsage(THREE.DynamicDrawUsage), na = new THREE.BufferAttribute(mappa.nasc, 1).setUsage(THREE.DynamicDrawUsage);
  pg.setAttribute('position', pa); pg.setAttribute('nasc', na); pg.setDrawRange(0, 0);
  puntiGeo = new THREE.Points(pg, MAT_PUNTI); puntiGeo.frustumCulled = false; puntiGeo.layers.set(1); scene.add(puntiGeo); puntiGeo.userData.caricati = 0;
  // scia: ultime scansioni
  const NS = 8 * lidar.raggiScan, sg = new THREE.BufferGeometry();
  sg.setAttribute('position', new THREE.BufferAttribute(new Float32Array(NS * 3), 3).setUsage(THREE.DynamicDrawUsage));
  sg.setAttribute('nasc', new THREE.BufferAttribute(new Float32Array(NS).fill(-99), 1).setUsage(THREE.DynamicDrawUsage));
  scia = new THREE.Points(sg, MAT_SCIA); scia.frustumCulled = false; scia.layers.set(1); scia.userData.i = 0; scene.add(scia);
  // griglia di occupazione + frontiere
  gTex = new THREE.DataTexture(new Uint8Array(mappa.W * mappa.H * 4), mappa.W, mappa.H, THREE.RGBAFormat); gTex.magFilter = gTex.minFilter = THREE.NearestFilter; gTex.needsUpdate = true;
  MAT_GRIGLIA.uniforms.uTex.value = gTex; MAT_GRIGLIA.uniforms.uN.value.set(mappa.W, mappa.H);
  griglia = new THREE.Mesh(piano(mappa.W * RIS, mappa.H * RIS), MAT_GRIGLIA);
  griglia.position.set(mappa.x0 + mappa.W * RIS / 2, mappa.y0 + mappa.H * RIS / 2, 0.018); griglia.layers.set(1); griglia.renderOrder = 2; scene.add(griglia);
  // meta
  meta3d = new THREE.Group(); meta3d.visible = false; meta3d.layers.set(1);
  const mr = new THREE.Mesh(new THREE.RingGeometry(0.26, 0.32, 48), new THREE.MeshBasicMaterial({ color: 0xffd21a, transparent: true, depthWrite: false })); mr.position.z = 0.03; mr.layers.set(1);
  const raggio = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 2.4, 8).rotateX(Math.PI / 2).translate(0, 0, 1.2), new THREE.MeshBasicMaterial({ color: 0xffd21a, transparent: true, opacity: 0.55 })); raggio.layers.set(1);
  meta3d.add(mr, raggio); meta3d.userData.anello = mr; scene.add(meta3d);
  aggiornaPercorso(null);
  // zone HUD
  $('#zone').innerHTML = S.zone.map((z, i) => `<li data-i="${i}"><b>${z.nome}</b><span>x ${fmt(z.x, 1)} · y ${fmt(z.y, 1)}</span><span>da fare</span></li>`).join('') || '<li>nessuna zona</li>';
  // camera interattiva
  const L = Math.max(x1 - x0, y1 - y0);
  controls.target.set(cane.x + 2.5, cane.y - 0.5, 0); camera.position.set(cane.x - 3.5, cane.y + 6.5, 7.5); controls.update();
  logga(`SLAM Abra (KISS-SLAM) avviato  sorgente sim:${nome}  LiDAR L2 ${lidar.raggiScan * 10} punti/s`, 'ev');
}

// marcatori ArUco: facce verso il libero, distanti fra loro (come mappa.esempio.json: z 0,5 m, lato 0,2 m)
function piazzaMarcatori() {
  const cand = [], ids = Object.keys(ARUCO).map(Number);
  for (let i = 0; i < mondo.n; i++) {
    const lo = [mondo.lo[i * 3], mondo.lo[i * 3 + 1], mondo.lo[i * 3 + 2]], hi = [mondo.hi[i * 3], mondo.hi[i * 3 + 1], mondo.hi[i * 3 + 2]];
    if (hi[2] < 0.75) continue;
    const c = [(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2];
    for (const [nx, ny] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const px = nx ? (nx > 0 ? hi[0] : lo[0]) : c[0], py = ny ? (ny > 0 ? hi[1] : lo[1]) : c[1];
      const lato = nx ? hi[1] - lo[1] : hi[0] - lo[0];
      if (lato < 0.6) continue;
      if (mondo.distanza(px + nx * 1.2, py + ny * 1.2) < 0.7) continue;
      cand.push({ x: px + nx * 0.012, y: py + ny * 0.012, z: 0.55, nx, ny });
    }
  }
  const scelti = [];
  const rr = rng(4);
  cand.sort(() => rr() - 0.5);
  for (const c of cand) { if (scelti.every((s) => Math.hypot(s.x - c.x, s.y - c.y) > 4.5)) scelti.push(c); if (scelti.length >= 6) break; }
  scelti.forEach((c, k) => {
    c.id = ids[k % ids.length];
    const m = new THREE.Mesh(new THREE.PlaneGeometry(0.26, 0.26), rivela(new THREE.MeshBasicMaterial({ map: texAruco(c.id), color: 0x9c9c98 })));
    m.position.set(c.x, c.y, c.z); m.lookAt(c.x + c.nx, c.y + c.ny, c.z); scene.add(m); c.mesh = m;
    marcatori.push(c);
  });
}

// ---------------------------------------------------------------- materiali dati
const MAT_PUNTI = new THREE.ShaderMaterial({
  uniforms: { uT: { value: 0 }, uS: { value: 30 }, uA: { value: 1 }, uLim: U.uLim },
  vertexShader: `attribute float nasc; uniform float uT, uS; uniform vec4 uLim; varying vec3 vC;
    void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.0); gl_Position = projectionMatrix * mv;
      float age = max(uT - nasc, 0.0), fl = exp(-age * 2.4), pav = step(position.z, 0.04);
      vec3 c = mix(vec3(0.16, 0.55, 0.68), vec3(0.55, 0.92, 1.0), clamp(position.z / 4.0, 0.0, 1.0));
      c = mix(c, vec3(0.10, 0.34, 0.42), pav);
      vC = mix(c * 0.85, vec3(1.0, 0.93, 0.62) * 1.15, fl * (1.0 - 0.75 * pav));
      gl_PointSize = clamp(uS * (1.0 + 1.3 * fl) * (1.0 - 0.3 * pav) / -mv.z, 1.3, 7.0);
      // muri perimetrali disegnati in sezione: i loro punti sopra il taglio non si mostrano
      bool fuori = position.x < uLim.x - 0.02 || position.x > uLim.y + 0.02 || position.y < uLim.z - 0.02 || position.y > uLim.w + 0.02;
      if (fuori && position.z > 1.12) gl_Position = vec4(2.0, 2.0, 2.0, 1.0); }`,
  fragmentShader: `uniform float uA; varying vec3 vC; void main(){ vec2 d = gl_PointCoord - 0.5; if (dot(d, d) > 0.25) discard; gl_FragColor = vec4(vC, uA); }`,
  transparent: true, depthWrite: true,
});
const MAT_SCIA = new THREE.ShaderMaterial({
  uniforms: { uT: { value: 0 }, uS: { value: 30 }, uA: { value: 1 }, uLim: U.uLim },
  vertexShader: `attribute float nasc; uniform float uT, uS; uniform vec4 uLim; varying float vA;
    void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.0); gl_Position = projectionMatrix * mv;
      bool fuori = position.x < uLim.x - 0.02 || position.x > uLim.y + 0.02 || position.y < uLim.z - 0.02 || position.y > uLim.w + 0.02;
      if (fuori && position.z > 1.12) gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
      float age = uT - nasc; vA = age < 0.0 ? 0.0 : exp(-age * 2.6) * mix(1.0, 0.18, step(position.z, 0.04));
      gl_PointSize = clamp(uS * 1.1 / -mv.z, 1.5, 6.0); }`,
  fragmentShader: `uniform float uA; varying float vA; void main(){ vec2 d = gl_PointCoord - 0.5; if (dot(d, d) > 0.25 || vA < 0.02) discard; gl_FragColor = vec4(vec3(0.45, 0.95, 1.0) * (0.5 + 0.9 * vA), vA * uA * 0.8); }`,
  transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
});
const MAT_GRIGLIA = new THREE.ShaderMaterial({
  uniforms: { uTex: { value: null }, uN: { value: new THREE.Vector2(1, 1) }, uT: { value: 0 }, uA: { value: 1 } },
  vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
  fragmentShader: `uniform sampler2D uTex; uniform vec2 uN; uniform float uT, uA; varying vec2 vUv;
    void main(){ vec2 g = vUv * uN; vec2 f = fract(g); vec4 c = texture2D(uTex, (floor(g) + 0.5) / uN);
      float e = step(0.07, f.x) * step(0.07, f.y);
      vec4 col = vec4(0.0);
      if (c.r > 0.6) col = vec4(0.80, 0.80, 0.77, 0.50 * e + 0.06);
      else if (c.r > 0.2) col = vec4(0.93, 0.92, 0.88, 0.025 + 0.04 * e);
      if (c.g > 0.5 && c.r < 0.6) col = vec4(1.0, 0.36, 0.30, 0.05 + 0.10 * e);
      if (c.b > 0.7) col = vec4(0.40, 0.90, 1.0, (0.45 + 0.4 * sin(uT * 4.0 + g.x * 0.6 + g.y * 0.4)) * e);
      else if (c.b > 0.3) col = vec4(1.0, 0.80, 0.0, (0.75 + 0.25 * sin(uT * 6.0)) * e);
      gl_FragColor = vec4(col.rgb * (c.b > 0.3 ? 1.15 : 1.0), col.a * uA); }`,
  transparent: true, depthWrite: false,
});
const MAT_PERCORSO = new THREE.ShaderMaterial({
  uniforms: { uT: { value: 0 }, uA: { value: 1 } },
  vertexShader: 'attribute float lungo; attribute float lato; varying float vL; varying float vS; void main(){ vL = lungo; vS = lato; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
  fragmentShader: `uniform float uT, uA; varying float vL; varying float vS;
    void main(){ float a = fract((vL - uT * 1.1) / 0.55); float chev = step(abs(vS) * 0.35 + 0.15, a) * step(a, abs(vS) * 0.35 + 0.42);
      float core = 1.0 - smoothstep(0.15, 0.35, abs(vS));
      vec3 c = vec3(1.0, 0.78, 0.0); gl_FragColor = vec4(c * (0.95 + 0.6 * chev), (0.38 + 0.5 * max(chev, core)) * uA); }`,
  transparent: true, depthWrite: false, side: THREE.DoubleSide,
});

function aggiornaPercorso(P) {
  if (percorso3d) { scene.remove(percorso3d); percorso3d.geometry.dispose(); percorso3d = null; }
  if (!P || P.length < 2) { meta3d && (meta3d.visible = false); return; }
  // il nastro parte 0,45 m davanti al cane (non copre le zampe)
  P = P.slice(); while (P.length > 2 && Math.hypot(P[1][0] - P[0][0], P[1][1] - P[0][1]) < 0.45) P.splice(1, 1);
  { const d = Math.hypot(P[1][0] - P[0][0], P[1][1] - P[0][1]); if (d > 0.45) P[0] = [P[0][0] + (P[1][0] - P[0][0]) * 0.45 / d, P[0][1] + (P[1][1] - P[0][1]) * 0.45 / d]; }
  const pos = [], lu = [], la = [], ix = []; let L = 0; const w = 0.075;
  for (let i = 0; i < P.length; i++) {
    const a = P[Math.max(0, i - 1)], b = P[Math.min(P.length - 1, i + 1)];
    let dx = b[0] - a[0], dy = b[1] - a[1]; const n = Math.hypot(dx, dy) || 1; dx /= n; dy /= n;
    if (i > 0) L += Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]);
    pos.push(P[i][0] - dy * w, P[i][1] + dx * w, 0.035, P[i][0] + dy * w, P[i][1] - dx * w, 0.035);
    lu.push(L, L); la.push(-1, 1);
    if (i > 0) { const k = i * 2; ix.push(k - 2, k - 1, k, k - 1, k + 1, k); }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('lungo', new THREE.Float32BufferAttribute(lu, 1)); g.setAttribute('lato', new THREE.Float32BufferAttribute(la, 1)); g.setIndex(ix);
  percorso3d = new THREE.Mesh(g, MAT_PERCORSO); percorso3d.layers.set(1); percorso3d.renderOrder = 3; percorso3d.visible = livelli.percorso; scene.add(percorso3d);
  const f = P[P.length - 1]; meta3d.position.set(f[0], f[1], 0); meta3d.visible = livelli.percorso;
}

// ---------------------------------------------------------------- comportamento (navigatore_slam.py)
function pianifica(meta, etichetta) {
  const t0 = performance.now();
  const r = astar(mappa, [cane.x, cane.y], meta);
  if (!r) { logga(`NAV A* nessun percorso verso (${fmt(meta[0], 1)},${fmt(meta[1], 1)}): meta scartata`, 'ev'); return false; }
  cane.percorso = r.punti; cane.iSeg = 1; cane.arrivato = false; S.meta = meta; S.percorsoInfo = r;
  aggiornaPercorso(r.punti);
  if (etichetta) logga(`NAV ${etichetta} meta=(${fmt(meta[0], 1)},${fmt(meta[1], 1)}) A* ${fmt(r.lung, 1)} m, ${r.celle} celle, ${r.esplorate} esplorate, ${fmt(performance.now() - t0, 1)} ms`, 'ev');
  return true;
}
function scegliFrontiera() {
  const F = S.fronti; let best = null, bs = -1;
  for (const g of F.gruppi) {
    let sx = 0, sy = 0; for (const k of g) { const [x, y] = mappa.centro(k % mappa.W, (k / mappa.W) | 0); sx += x; sy += y; }
    const cx = sx / g.length, cy = sy / g.length;
    if (S.nero.some((n) => Math.hypot(n[0] - cx, n[1] - cy) < 1.2)) continue;
    let bk = g[0], bd = 1e9; for (const k of g) { const [x, y] = mappa.centro(k % mappa.W, (k / mappa.W) | 0); const d = Math.hypot(x - cx, y - cy); if (d < bd) { bd = d; bk = k; } }
    const [tx, ty] = mappa.centro(bk % mappa.W, (bk / mappa.W) | 0);
    const d = Math.hypot(tx - cane.x, ty - cane.y);
    if (d < 0.8) continue;
    let dyaw = Math.abs(Math.atan2(Math.sin(Math.atan2(ty - cane.y, tx - cane.x) - cane.yaw), Math.cos(Math.atan2(ty - cane.y, tx - cane.x) - cane.yaw)));
    const sc = Math.pow(g.length, 0.7) / (d + 2.5) * (1.25 - 0.25 * dyaw / Math.PI);
    if (sc > bs) { bs = sc; best = { g, x: tx, y: ty, n: g.length }; }
  }
  return best;
}
function comportamento(dt) {
  if (S.modo === 'esplora') {
    const fermo = !cane.percorso;
    let bOk = false;
    if (S.bersaglio) for (const k of S.fronti.celle) { const [x, y] = mappa.centro(k % mappa.W, (k / mappa.W) | 0); if (Math.hypot(x - S.bersaglio.x, y - S.bersaglio.y) < 1.2) { bOk = true; break; } }
    if (fermo || (!bOk && S.tSim - (S.tScelta || 0) > 2.5)) {
      const b = scegliFrontiera();
      if (!b) {
        if (!S.esploraFine && S.scans > 30) { S.esploraFine = true; logga(`ESPLORA nessuna frontiera raggiungibile: mappa completa, ${S.area | 0} m² · passo in pattuglia`, 'ev'); setModo('pattuglia', true); }
        return;
      }
      S.tScelta = S.tSim;
      S.bersaglio = b;
      if (!pianifica([b.x, b.y], `esplora frontiera ${b.n} celle`)) S.nero.push([b.x, b.y]);
    }
  } else if (S.modo === 'pattuglia' && S.zone.length) {
    if (S.pausa > 0) { S.pausa -= dt; if (S.pausa <= 0) { S.iZona = (S.iZona + 1) % S.zone.length; vaiZona(); } return; }
    if (!cane.percorso) {
      const z = S.zone[S.iZona];
      if (Math.hypot(z.x - cane.x, z.y - cane.y) < 0.6) {
        z.stato = 'controllata'; S.pausa = 2.5; aggiornaZone();
        const esiti = ['nessuna persona, passaggio libero', 'porta chiusa, nessun oggetto a terra', 'quadro chiuso, nessuna anomalia'];
        logga(`PATTUGLIA zona ${z.nome}: foto scattata · ${esiti[S.iZona % esiti.length]}`, 'ev');
      } else vaiZona();
    }
  } else if (S.modo === 'missione' && S.missioneAttiva) {
    if (!cane.percorso) {
      if (S.iMis < S.missione.length) { const p = S.missione[S.iMis]; if (Math.hypot(p.x - cane.x, p.y - cane.y) < 0.4) { logga(`NAV missione punto ${S.iMis + 1}/${S.missione.length} raggiunto`, 'ev'); S.iMis++; } else pianifica([p.x, p.y], `missione punto ${S.iMis + 1}`); }
      else { S.iMis = 0; logga('NAV missione completata · ripeto il giro (pattuglia)', 'ev'); }
    }
  } else if (S.modo === 'punto' && cane.arrivato && S.meta) {
    logga(`NAV arrivato a (${fmt(S.meta[0], 1)},${fmt(S.meta[1], 1)}) · in attesa di una nuova meta`, 'ev'); S.meta = null; cane.arrivato = false; aggiornaPercorso(null);
  }
}
function vaiZona() { const z = S.zone[S.iZona]; S.zone.forEach((q, i) => q.ora = i === S.iZona); aggiornaZone(); pianifica([z.x, z.y], `pattuglia zona ${z.nome}`); }

// ---------------------------------------------------------------- passo di simulazione (dt fisso)
const DT = 0.05;
function passoSim(tR) {
  S.tSim += DT;
  if (REGIA) regiaSim(tR);
  cane.passo(DT, mondo);
  if (cane.bloccato) { cane.bloccato = false; if (S.meta) pianifica(S.meta); }
  mappa.aggiornaVisto(DT);
  // LiDAR a 10 Hz
  if (S.lidarOn && S.tSim - S.tScan >= 0.1 - 1e-6) {
    S.tScan = S.tSim;
    const c = Math.cos(cane.yaw), s = Math.sin(cane.yaw);
    const sc = lidar.scansione(mondo, cane.x + c * 0.28, cane.y + s * 0.28, 0.42, cane.yaw);
    S.ultimaScan = sc; S.scans++;
    const n = mappa.integra([cane.x, cane.y], sc, S.tSim);
    S.nuovi = n; S.storia.push(n); if (S.storia.length > 120) S.storia.shift();
    // scia
    const sp = scia.geometry.attributes.position, sn = scia.geometry.attributes.nasc, NS = sn.count;
    for (let k = 0; k < sc.n; k++) { const i = scia.userData.i; sp.array[i * 3] = sc.xyz[k * 3]; sp.array[i * 3 + 1] = sc.xyz[k * 3 + 1]; sp.array[i * 3 + 2] = sc.xyz[k * 3 + 2]; sn.array[i] = S.tSim; scia.userData.i = (i + 1) % NS; }
    sp.needsUpdate = sn.needsUpdate = true;
    if (S.scans % 50 === 0) logga(`SLAM frame=${S.scans} punti=${mappa.np.toLocaleString('it-IT')} voxel=0,075 m icp_err=${fmt(0.008 + R() * 0.01, 3)} m`, 'slam');
  }
  // odometria che deriva, EKF che la riporta giù con gli ArUco
  S.deriva += Math.abs(cane.v) * DT * 0.011 + Math.abs(cane.w) * DT * 0.004;
  S.tAr += DT;
  if (S.tAr > 0.2) { S.tAr = 0; vediMarcatori(); }
  // ripianifica sulla mappa che cresce (1 s), frontiere (0,5 s)
  S.tFront += DT; if (S.tFront > 0.5) { S.tFront = 0; S.fronti = mappa.frontiere(); }
  S.tPlan += DT; if (S.tPlan > 1.0) { S.tPlan = 0; if (cane.percorso && S.meta) pianifica(S.meta); }
  if (S.lidarOn) comportamento(DT);
  S.batt = Math.max(5, S.batt - DT * (0.004 + Math.abs(cane.v) * 0.006));
  S.tLog += DT; if (S.tLog >= 1) { S.tLog = 0; if (cane.percorso) logNav(); }
}
function vediMarcatori() {
  const c = Math.cos(cane.yaw), s = Math.sin(cane.yaw), ox = cane.x + c * 0.33, oy = cane.y + s * 0.33, oz = 0.4;
  S.arVisti = [];
  for (const m of marcatori) {
    const dx = m.x - ox, dy = m.y - oy, dz = m.z - oz, d = Math.hypot(dx, dy, dz);
    if (d > 4.5 || d < 0.4) continue;
    const ang = Math.atan2(Math.sin(Math.atan2(dy, dx) - cane.yaw), Math.cos(Math.atan2(dy, dx) - cane.yaw));
    if (Math.abs(ang) > 0.55) continue;
    if (-(dx * m.nx + dy * m.ny) / Math.hypot(dx, dy) < 0.35) continue;
    const h = mondo.raggio(ox, oy, oz, dx / d, dy / d, dz / d, d - 0.05);
    if (h && h.b !== -1) continue;
    S.arVisti.push(m);
    const ultimo = S.arOra[m.id] || -99;
    if (S.tSim - ultimo > 8) {
      const prima = S.deriva; S.deriva *= 0.22; S.arOra[m.id] = S.tSim;
      S.ultimoAr = { id: m.id, d, t: S.tSim };
      logga(`ARUCO id=${m.id} d=${fmt(d, 2)} m ang=${Math.round(ang * 57.3)}° → EKF corretto, deriva ${fmt(prima, 2)}→${fmt(S.deriva, 2)} m`, 'ar');
    }
  }
}

// ---------------------------------------------------------------- log
const LOG = [];
function ora() {
  const d = REGIA ? new Date(Date.UTC(2026, 10, 5, 21, 14, 0) + S.tSim * 1000) : new Date();
  return REGIA ? d.toISOString().slice(11, 19) : d.toTimeString().slice(0, 8);
}
function logga(txt, cl = 'nav') { LOG.push(`<span class="ora">${ora()}</span> <span class="${cl}">${txt.replace(/</g, '&lt;')}</span>`); if (LOG.length > 40) LOG.shift(); S.logSporco = true; }
function logNav() {
  const g = cane.guida, d = mondo.distanza(cane.x, cane.y), liberi = S.ultimaScan ? S.ultimaScan.liberi : 0;
  logga(`NAV pos=(${fmt(cane.x, 2, '.')},${fmt(cane.y, 2, '.')},${Math.round(cane.yaw * 57.3)}°) guida=(${fmt(g[0], 1, '.')},${fmt(g[1], 1, '.')}) err=${Math.round(cane.err * 57.3)}° archi_liberi=${Math.round(liberi * 0.9)} scelto=${Math.max(0, Math.min(30, Math.round(30 - Math.abs(cane.w) * 14)))} vicino=${fmt(d, 2, '.')} cmd=(${fmt(cane.v, 2, '.')},${fmt(cane.w, 2, '.')}) inviato`);
}
function fmt(v, n = 2, sep = ',') { return (+v).toFixed(n).replace('.', sep); }

// ---------------------------------------------------------------- HUD
function aggiornaZone() {
  document.querySelectorAll('#zone li[data-i]').forEach((li) => { const z = S.zone[+li.dataset.i]; li.className = (z.stato === 'controllata' ? 'ok ' : '') + (z.ora ? 'ora' : ''); li.lastElementChild.textContent = z.stato; });
}
const spark = $('#spark').getContext('2d');
function hud() {
  $('#kPunti').textContent = mappa.np.toLocaleString('it-IT');
  $('#kScan').textContent = S.scans.toLocaleString('it-IT');
  $('#kNuovi').textContent = S.nuovi;
  $('#kModoTag').textContent = S.modo;
  $('#kMeta').textContent = S.meta ? `${fmt(S.meta[0], 1)} · ${fmt(S.meta[1], 1)} m` : '—';
  $('#kPerc').textContent = S.percorsoInfo && cane.percorso ? `${fmt(S.percorsoInfo.lung, 1)} m · ${S.percorsoInfo.celle} celle` : '—';
  $('#kFront').textContent = `${S.fronti.celle.length} celle · ${S.fronti.gruppi.length} gruppi`;
  $('#kArea').textContent = `${Math.round(S.area)} m²`;
  const res = Math.min(0.06, 0.012 + S.deriva * 0.15);
  $('#kStima').textContent = `${fmt(cane.x, 2)} · ${fmt(cane.y, 2)} ±${fmt(res, 2)}`;
  $('#kDeriva').textContent = `${fmt(S.deriva, 2)} m`;
  $('#kAruco').textContent = S.ultimoAr ? `id ${S.ultimoAr.id} · ${fmt(S.ultimoAr.d, 2)} m · ${Math.round(S.tSim - S.ultimoAr.t)} s fa` : '—';
  $('#kPatTag').textContent = S.modo === 'pattuglia' ? 'in giro' : 'in attesa';
  $('#tV').textContent = fmt(cane.v, 2); $('#tW').textContent = fmt(cane.w, 2);
  $('#tPosa').textContent = `${fmt(cane.x, 2)} · ${fmt(cane.y, 2)} · ${Math.round(cane.yaw * 57.3)}°`;
  $('#tDist').textContent = `${fmt(cane.dist, 1)} m`;
  $('#tBat').textContent = `${fmt(S.batt, 1)} % · 28,${(6 + S.batt / 50) | 0} V`;
  $('#tBatBar').style.width = S.batt + '%';
  $('#orologio').textContent = ora();
  $('#tStato').textContent = S.lidarOn ? 'SLAM attivo' : 'LiDAR spento';
  if (S.logSporco) { S.logSporco = false; $('#log').innerHTML = LOG.slice(-6).join('\n'); }
  // spark
  const W = spark.canvas.width, H = spark.canvas.height; spark.clearRect(0, 0, W, H);
  spark.strokeStyle = '#5fd4e6'; spark.lineWidth = 1.5; spark.beginPath();
  const mx = Math.max(50, ...S.storia);
  S.storia.forEach((v, i) => { const x = i / 119 * W, y = H - 3 - v / mx * (H - 6); i ? spark.lineTo(x, y) : spark.moveTo(x, y); });
  spark.stroke();
}
function aggiornaGriglia() {
  const d = gTex.image.data, c = mappa.costi(), N = mappa.W * mappa.H;
  let area = 0;
  for (let k = 0; k < N; k++) {
    const occ = mappa.occ[k] >= 2, lib = mappa.lib[k];
    d[k * 4] = occ ? 255 : lib ? 110 : 0; d[k * 4 + 1] = c[k] === Infinity && (lib || occ) ? 255 : 0; d[k * 4 + 2] = 0; d[k * 4 + 3] = 255;
    if (lib) area++;
  }
  S.area = area * RIS * RIS;
  const bers = S.bersaglio && S.modo === 'esplora' ? new Set(S.bersaglio.g) : null;
  for (const k of S.fronti.celle) d[k * 4 + 2] = bers && bers.has(k) ? 140 : 255;
  gTex.needsUpdate = true;
  const v = vTex.image.data; for (let k = 0; k < N; k++) v[k] = mappa.visto[k] * 255;
  vTex.needsUpdate = true;
  const b = bTex.image.data; for (let i = 0; i < mondo.n; i++) b[i] = mappa.boxVisto[i] * 255;
  bTex.needsUpdate = true;
}
function caricaPunti() {
  const g = puntiGeo.geometry, a = puntiGeo.userData.caricati, n = mappa.np;
  if (n === a) return;
  const p = g.attributes.position, q = g.attributes.nasc;
  p.clearUpdateRanges(); q.clearUpdateRanges();
  p.addUpdateRange(a * 3, (n - a) * 3); q.addUpdateRange(a, n - a);
  p.needsUpdate = q.needsUpdate = true; g.setDrawRange(0, n); puntiGeo.userData.caricati = n;
}

// ---------------------------------------------------------------- comandi utente
const livelli = { nuvola: true, griglia: true, frontiere: true, percorso: true };
const AIUTO = { punto: 'Clicca sul pavimento: il cane calcola il percorso A* sulla mappa e ci va aggirando gli ostacoli.', missione: 'Clicca sul pavimento per aggiungere i punti in ordine (1, 2, 3…), poi «Avvia missione». Il giro si ripete.', esplora: 'Il cane va da solo verso le zone non ancora viste (frontiere) e costruisce la mappa.', pattuglia: 'Giro fra le zone A, B, C con una foto e un controllo in ogni zona.', fermo: 'Cane fermo in piedi.' };
let segui = !REGIA;
function setModo(m, auto) {
  S.modo = m; S.missioneAttiva = false;
  if (!auto) { cane.percorso = null; S.meta = null; S.bersaglio = null; aggiornaPercorso(null); }
  document.querySelectorAll('[data-modo]').forEach((b) => b.classList.toggle('primary', b.dataset.modo === m));
  $('#aiuto').textContent = AIUTO[m]; $('#rigaMissione').hidden = m !== 'missione';
  if (m === 'pattuglia') { S.iZona = 0; S.zone.forEach((z) => z.stato = 'da fare'); vaiZona(); }
  if (m === 'esplora') S.esploraFine = false;
  if (!auto) logga(`CONSOLE modo → ${m}`, 'ev');
}
document.querySelectorAll('[data-modo]').forEach((b) => b.onclick = () => setModo(b.dataset.modo));
$('#bFerma').onclick = () => setModo('fermo');
$('#bSegui').onclick = () => { segui = !segui; $('#bSegui').classList.toggle('on', segui); };
$('#bCancella').onclick = () => { S.missione.forEach((p) => scene.remove(p.sprite)); S.missione = []; S.iMis = 0; cane.percorso = null; aggiornaPercorso(null); };
$('#bAvvia').onclick = () => { if (!S.missione.length) return; S.missioneAttiva = true; S.iMis = 0; logga(`NAV missione avviata: ${S.missione.length} punti`, 'ev'); };
document.querySelectorAll('[data-l]').forEach((c) => c.onchange = () => { livelli[c.dataset.l] = c.checked; applicaLivelli(); });
function applicaLivelli() { puntiGeo.visible = scia.visible = livelli.nuvola; griglia.visible = livelli.griglia || livelli.frontiere; MAT_GRIGLIA.uniforms.uA.value = 1; if (percorso3d) percorso3d.visible = livelli.percorso; meta3d.visible = livelli.percorso && !!percorso3d; }
$('#mondo').onchange = (e) => { caricaMondo(e.target.value); setModo('esplora'); };
let giu = null;
canvas.addEventListener('pointerdown', (e) => { giu = { x: e.clientX, y: e.clientY, t: performance.now() }; });
canvas.addEventListener('pointerup', (e) => {
  if (REGIA || !giu || Math.hypot(e.clientX - giu.x, e.clientY - giu.y) > 6 || performance.now() - giu.t > 600) return;
  const r = canvas.getBoundingClientRect(), ray = new THREE.Raycaster();
  ray.setFromCamera(new THREE.Vector2((e.clientX - r.left) / r.width * 2 - 1, -(e.clientY - r.top) / r.height * 2 + 1), camera);
  const p = new THREE.Vector3(); if (!ray.ray.intersectPlane(new THREE.Plane(new THREE.Vector3(0, 0, 1), 0), p)) return;
  const [x0, x1, y0, y1] = mondo.limiti; if (p.x < x0 || p.x > x1 || p.y < y0 || p.y > y1) return;
  if (S.modo === 'missione') {
    const sp = testoSprite(String(S.missione.length + 1)); sp.position.set(p.x, p.y, 0.5); sp.scale.set(0.5, 0.5, 0.5); scene.add(sp); extra3d.push(sp);
    S.missione.push({ x: p.x, y: p.y, sprite: sp }); $('#bAvvia').textContent = `Avvia missione (${S.missione.length})`;
    return;
  }
  if (S.modo !== 'punto') setModo('punto');
  pianifica([p.x, p.y], 'vai a un punto');
});

// ---------------------------------------------------------------- regia
const TITOLI = [
  [2.6, 7.2, 'LiDAR Unitree L2 · 11 000 punti/s', 'Ogni punto,<br><em>una misura.</em>'],
  [10.5, 15.0, 'KISS-SLAM · voxel 7,5 cm · celle 20 cm', 'La mappa<br>nasce <em>da sola.</em>'],
  [19.5, 24.5, 'frontiere + A* sulla griglia di occupazione', 'Decide<br><em>dove andare.</em>'],
  [29.0, 34.0, 'EKF · odometria + marcatori ArUco · RealSense D435i', 'Sa sempre<br><em>dov’è.</em>'],
];
function regiaSim(t) {
  if (t >= 1.3 && !S.lidarOn) { S.lidarOn = true; }
  mappa.velVisto = t < 14 ? 0.45 : 1.6; mappa.velBox = t < 14 ? 0.3 : 0.9;   // in apertura il mondo si accende piano
  lidar.raggiScan = Math.round(1100 * Math.min(1, Math.max(0.08, (t - 1.3) / 4.5)) ** 1.6) || 60;
  if (t >= 6.2 && S.modo === 'fermo') { S.modo = 'esplora'; cane.vmax = 0.75; logga('ESPLORA avviata: 10 min, vado verso le zone ignote', 'ev'); }
}
const smooth = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
const cam = { p: new THREE.Vector3(), q: new THREE.Vector3(), ok: false, D: new THREE.Vector3(), yaw: 0 };
function inquadratura(i, t) {
  const D = cam.D, y = cam.yaw, f = [Math.cos(y), Math.sin(y)], [x0, x1, y0, y1] = mondo.limiti, L = Math.max(x1 - x0, y1 - y0);
  const C = new THREE.Vector3((x0 + x1) / 2, (y0 + y1) / 2, 0);
  const V = (x, y2, z) => new THREE.Vector3(x, y2, z);
  if (i === 0) { const a = y + 2.35 - 0.05 * t, r = 1.55 - 0.03 * t, l = [Math.sin(a), -Math.cos(a)];   // cane a destra del titolo
    return [V(D.x + Math.cos(a) * r, D.y + Math.sin(a) * r, 0.42 + 0.03 * t), V(D.x + f[0] * 0.2 + l[0] * 0.22, D.y + f[1] * 0.2 + l[1] * 0.22, 0.27), 34]; }
  if (i === 1) { const u = smooth(8, 17, t), a = y + 2.9 + 0.25 * u, r = 1.6 + 8.5 * u; return [V(D.x + Math.cos(a) * r, D.y + Math.sin(a) * r, 0.7 + 7.2 * u), V(D.x + f[0] * 2 * u, D.y + f[1] * 2 * u, 0.3), 38]; }
  if (i === 2) { const M = C.clone().lerp(D, 0.35), a = -1.75 + 0.03 * (t - 17); return [V(M.x + Math.cos(a) * L * 0.62, M.y + Math.sin(a) * L * 0.62, L * 0.62), V(M.x, M.y, 0), 40]; }
  if (i === 3) { const s = 0.04 * (t - 27); return [V(D.x - f[0] * (2.5 - s) - f[1] * 0.7, D.y - f[1] * (2.5 - s) + f[0] * 0.7, 1.3), V(D.x + f[0] * 0.7, D.y + f[1] * 0.7, 0.25), 42]; }
  const u = smooth(37, 44, t); return [V(C.x - L * 0.06, C.y - L * (0.62 - 0.12 * u), L * (0.42 + 0.55 * u)), V(C.x, C.y + L * 0.05, 0), 42];
}
const TAGLI = [0, 8, 17, 27, 37, 1e9];
function regiaCamera(t, dt) {
  cam.D.lerp(new THREE.Vector3(cane.x, cane.y, 0), cam.ok ? 1 - Math.exp(-dt * 2.5) : 1);
  let dy = Math.atan2(Math.sin(cane.yaw - cam.yaw), Math.cos(cane.yaw - cam.yaw)); cam.yaw += dy * (cam.ok ? 1 - Math.exp(-dt * 0.9) : 1);
  let i = 0; while (t >= TAGLI[i + 1]) i++;
  let [p, q, fov] = inquadratura(i, t);
  const w = i > 0 ? 1 - smooth(TAGLI[i], TAGLI[i] + 3.0, t) : 0;
  if (w > 0) { const [p0, q0, f0] = inquadratura(i - 1, t); p.lerp(p0, w); q.lerp(q0, w); fov += (f0 - fov) * w; }
  // braccio a molla: la camera non entra nelle macchine (i muri perimetrali sono in sezione, si ignorano)
  const libera = (pp) => { const dv = pp.clone().sub(q), dl = dv.length(); dv.divideScalar(dl); const h = mondo.raggio(q.x, q.y, q.z, dv.x, dv.y, dv.z, dl, 4); return !(h && h.b >= 0); };
  if (i !== 2 && i !== 4 && !libera(p)) {          // se una macchina copre il cane, la camera sale (gru) invece di entrarci
    let ok = false;
    for (let k2 = 1; k2 <= 14 && !ok; k2++) { const p2 = p.clone(); p2.z += k2 * 0.45; if (libera(p2)) { p.copy(p2); ok = true; } }
  }
  const k = cam.ok ? 1 - Math.exp(-dt * 3.5) : 1; cam.ok = true;
  cam.p.lerp(p, k); cam.q.lerp(q, k);
  camera.position.copy(cam.p); camera.lookAt(cam.q); camera.fov = fov; camera.updateProjectionMatrix();
}
function regiaHud(t) {
  const on = (sel, t0) => document.querySelectorAll(sel).forEach((e, i) => e.classList.toggle('on', t >= t0 + i * 0.35 && t < 41));
  on('#hud .barra', 15.5); on('#hud .col.sx .panel', 16.5); on('#hud .col.dx .tele', 18); on('#hud .log', 18.6); on('#hud .col.dx .cam', 27);
  const tt = TITOLI.find((x) => t >= x[0] && t < x[1]);
  const el = $('#titolo');
  if (tt) { if (el.dataset.k !== tt[0] + '') { el.dataset.k = tt[0]; $('#titEye').textContent = tt[2]; $('#titH').innerHTML = tt[3]; } el.classList.add('on'); } else el.classList.remove('on');
  $('#finale').classList.toggle('on', t >= 40.3);
  $('#velo').style.opacity = t < 1.0 ? 1 : t < 2.2 ? 1 - (t - 1.0) / 1.2 : t > 39.6 ? Math.min(0.62, (t - 39.6) / 1.6 * 0.62) : 0;
}

// ---------------------------------------------------------------- render
const SFONDO_RS = new THREE.Color(0x24272b);
const sovra = $('#sovra'), sx = sovra.getContext('2d');
let W = 0, H = 0;
function ridimensiona() {
  const w = innerWidth, h = innerHeight; if (w === W && h === H) return; W = w; H = h;
  renderer.setSize(w, h, false); composer.setSize(w, h); camera.aspect = w / h; camera.updateProjectionMatrix();
  bloom.resolution.set(w / 2, h / 2);
  sovra.width = w * renderer.getPixelRatio(); sovra.height = h * renderer.getPixelRatio();
}
function rettangoloCam() {
  const el = $('#camBox'); const r = el.getBoundingClientRect();
  if (r.width < 20 || getComputedStyle(el.closest('.panel')).opacity < 0.05 || el.offsetParent === null) return null;
  return r;
}
function renderCamRS(rect) {
  const c = Math.cos(cane.yaw), s = Math.sin(cane.yaw);
  camRS.position.set(cane.x + c * 0.36, cane.y + s * 0.36, base3d.position.z + 0.06);
  camRS.lookAt(cane.x + c * 3, cane.y + s * 3, 0.05);
  camRS.aspect = rect.width / rect.height; camRS.updateProjectionMatrix();
  const pr = renderer.getPixelRatio(), y = H - rect.bottom;
  U.uForza.value = 1; const nb = scene.background, fg = scene.fog; scene.fog = null; scene.background = SFONDO_RS; cane3d.visible = false;
  renderer.setScissorTest(true); renderer.setViewport(rect.left, y, rect.width, rect.height); renderer.setScissor(rect.left, y, rect.width, rect.height);
  renderer.autoClear = true; renderer.render(scene, camRS);
  renderer.setScissorTest(false); renderer.setViewport(0, 0, W, H);
  U.uForza.value = 0; scene.background = nb; scene.fog = fg; cane3d.visible = true;
  // riquadri ArUco riconosciuti
  sx.save(); sx.scale(pr, pr); sx.strokeStyle = '#f2c200'; sx.fillStyle = '#f2c200'; sx.lineWidth = 1.5; sx.font = '600 10px JetBrains Mono, monospace';
  for (const m of S.arVisti) {
    const pts = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([a, b]) => {
      const v = new THREE.Vector3(-m.ny * a * 0.13, m.nx * a * 0.13, b * 0.13).add(new THREE.Vector3(m.x, m.y, m.z)).project(camRS);
      return [rect.left + (v.x + 1) / 2 * rect.width, rect.top + (1 - v.y) / 2 * rect.height, v.z];
    });
    if (pts.some((p) => p[2] > 1)) continue;
    sx.beginPath(); pts.forEach((p, i) => i ? sx.lineTo(p[0], p[1]) : sx.moveTo(p[0], p[1])); sx.closePath(); sx.stroke();
    const d = Math.hypot(m.x - cane.x, m.y - cane.y);
    sx.fillText(`ID ${m.id} · ${fmt(d, 2)} m`, Math.min(...pts.map((p) => p[0])), Math.min(...pts.map((p) => p[1])) - 5);
  }
  sx.restore();
}

let tPrec = null, t0 = null, acc = 0, tHud = 0, tGr = 0, fine = false;
function ciclo() {
  requestAnimationFrame(ciclo);
  const ora = performance.now();
  if (t0 === null) { t0 = ora; tPrec = ora; }
  let dt = Math.min(0.25, (ora - tPrec) / 1000); tPrec = ora;
  const tR = (ora - t0) / 1000 + SALTA;
  ridimensiona();
  acc += dt; let n = 0;
  while (acc >= DT && n < 8) { passoSim(tR); acc -= DT; n++; }
  if (n === 8) acc = 0;
  const tv = S.tSim;
  U.uT.value = tv; MAT_PUNTI.uniforms.uT.value = tv; MAT_SCIA.uniforms.uT.value = tv; MAT_GRIGLIA.uniforms.uT.value = tv; MAT_PERCORSO.uniforms.uT.value = tv;
  const pxs = H * renderer.getPixelRatio() / (2 * Math.tan(camera.fov * Math.PI / 360));
  MAT_PUNTI.uniforms.uS.value = 0.016 * pxs; MAT_SCIA.uniforms.uS.value = 0.016 * pxs;
  posaCane(dt);
  luceCane.position.set(cane.x - Math.cos(cane.yaw) * 0.6, cane.y - Math.sin(cane.yaw) * 0.6, 1.4);
  tGr += dt; if (tGr > 0.15) { tGr = 0; aggiornaGriglia(); }
  caricaPunti();
  if (meta3d.visible) { const s = 1 + 0.15 * Math.sin(tv * 5); meta3d.userData.anello.scale.set(s, s, 1); }
  if (REGIA) {
    regiaCamera(tR, dt); regiaHud(tR);
    MAT_GRIGLIA.uniforms.uA.value = smooth(9, 13, tR);
    MAT_PERCORSO.uniforms.uA.value = smooth(12, 14, tR);
    if (tR >= DURATA && !fine) { fine = true; window.__regiaFine = true; }
  } else {
    if (segui) { const d = new THREE.Vector3(cane.x, cane.y, 0).sub(controls.target).multiplyScalar(Math.min(1, dt * 3)); controls.target.add(d); camera.position.add(d); }
    controls.update();
  }
  tHud += dt; if (tHud > 0.2) { tHud = 0; hud(); }
  composer.render(dt);
  sx.clearRect(0, 0, sovra.width, sovra.height);
  const r = rettangoloCam(); if (r) renderCamRS(r);
}

// ---------------------------------------------------------------- avvio
caricaMondo('magazzino');
setModo(REGIA ? 'fermo' : 'esplora', true);
applicaLivelli();
$('#bSegui').classList.toggle('on', segui);
if (REGIA && SALTA > 0) { for (let t = 0; t < SALTA; t += DT) passoSim(t); }
else if (!REGIA) { for (let k = 0; k < 20; k++) passoSim(0); }   // mezzo secondo di LiDAR già acceso
hud();
$('#carica').classList.add('via');
window.__pronto = true;
requestAnimationFrame(ciclo);
