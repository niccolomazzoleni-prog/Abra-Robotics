// G1 Playground — dashboard 3D: prompt -> piano di Claude -> esecuzione del G1 (mockup vendibile).
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { loadG1, Timeline, ease } from './robot.js';
import { buildScene, buildMarkers, LAYOUT } from './scene.js';
import { SCENARI, route } from './scenari.js';
import { SYSTEM, ROBOTS, TAKES, RL } from './data.js';

const Q = new URLSearchParams(location.search);
const REGIA = Q.get('regia') === '1';
const FREEZE = Q.has('freeze'); // solo per le prove: tempo fermo all'istante ?t=
let frozen = null;
const NOW = () => FREEZE ? (frozen ??= performance.now()) : performance.now();
const $ = id => document.getElementById(id);
const fmt = (x, d = 1) => x.toLocaleString('it-IT', { minimumFractionDigits: d, maximumFractionDigits: d });
const clamp01 = x => Math.max(0, Math.min(1, x));
const lerp = (a, b, t) => a + (b - a) * t;
if (REGIA) document.body.classList.add('regia');

// ------------------------------------------------------------------ renderer e scena
const canvas = $('c3d');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(REGIA ? 1 : Math.min(2, window.devicePixelRatio));
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0f1216);
scene.fog = new THREE.Fog(0x0f1216, 7.5, 21);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.45;

const camera = new THREE.PerspectiveCamera(REGIA ? 36 : 40, 1, 0.05, 80);
camera.up.set(0, 0, 1);
camera.position.set(1.0, -6.8, 3.4);
const controls = new OrbitControls(camera, canvas);
controls.target.set(1.1, 0.35, 0.45);
controls.enableDamping = true; controls.dampingFactor = 0.08;
controls.maxPolarAngle = Math.PI * 0.49; controls.minDistance = 1.2; controls.maxDistance = 14;
controls.enabled = !REGIA;

const hemi = new THREE.HemisphereLight(0xdfe8f5, 0x2a2622, 0.6); hemi.position.set(0, 0, 10); scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff3e2, 2.3);
sun.position.set(-3.5, -4.5, 8); sun.target.position.set(1, 0, 0);
sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -5, right: 6, top: 5, bottom: -5, near: 1, far: 20 });
sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.02;
scene.add(sun, sun.target);
const rim = new THREE.DirectionalLight(0xb8d4ff, 0.9); rim.position.set(4, 6, 4); scene.add(rim);
const spot = new THREE.SpotLight(0xffe8b0, 0, 7, 0.5, 0.6); spot.position.set(-1.3, -1.2, 3.6); scene.add(spot, spot.target);

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(256, 256), 0.32, 0.5, 0.86);
composer.addPass(bloom);
composer.addPass(new OutputPass());

const W = buildScene(scene);
const MK = buildMarkers(scene);
let robot;

function resize() {
  const r = canvas.parentElement.getBoundingClientRect();
  const w = Math.max(10, r.width), h = Math.max(10, r.height);
  renderer.setSize(w, h, false); composer.setSize(w, h);
  camera.aspect = w / h;
  const base = REGIA ? 36 : 40; // in verticale allarga il campo per tenere la postazione intera
  camera.fov = camera.aspect >= 1.15 ? base : THREE.MathUtils.radToDeg(2 * Math.atan(Math.tan(THREE.MathUtils.degToRad(base / 2)) * 1.15 / camera.aspect));
  camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(canvas.parentElement);

// ------------------------------------------------------------------ stato del mondo
const K = LAYOUT.carton, C = LAYOUT.conv, B = LAYOUT.box;
const cartonY = -0.88;
const world = {};
function resetWorld() {
  Object.assign(world, { held: null, placed: null, pressT: null, runT: null, runV: 0, evi: 0, inCarton: false });
  W.objs.cassetta.position.copy(W.boxRest); W.objs.cassetta.rotation.set(0, 0, 0);
  W.objs.scatola.position.set(K.x, cartonY, C.z); W.setFlaps(1); W.tape.scale.x = 0.001;
  W.buttons.forEach(b => { b.position.y = 0.088; b.material.emissiveIntensity = 0.12; });
  W.flow.material.opacity = 0; W.beacon.material.emissiveIntensity = 0;
}

const IDLE = { tl: null };
let run = null; // { sc, tl, t0, steps, done }
function idleTimeline() {
  const tl = new Timeline(robot, LAYOUT.home); tl.stand(1e6).end(); return tl;
}

function updateWorld(t, st, tl) {
  // eventi
  const evs = tl.events;
  while (world.evi < evs.length && evs[world.evi].t <= t) {
    const e = evs[world.evi++];
    if (e.name === 'attach') world.held = e.data;
    if (e.name === 'release') { world.held = null; world.placed = { ...e.data, t: e.t, from: W.objs.cassetta.position.clone() }; }
    if (e.name === 'press') world.pressT = e.t;
    if (e.name === 'run') { world.runT = e.t; world.runV = e.data; }
  }
  const box = W.objs.cassetta;
  const cartX = world.runT != null ? Math.min(LAYOUT.ship, K.x + (t - world.runT) * world.runV * ease(Math.min(1, (t - world.runT) / 0.6) + 0.0001) ) : K.x;
  W.objs.scatola.position.x = cartX;
  if (world.held) {
    const p = robot.palmWorld.R;
    box.position.set(p.x, p.y, p.z - B.H - B.hh + 0.004);
    box.rotation.set(0, 0, st.base.yaw - Math.PI / 2);
    // niente compenetrazioni: il fondo resta sopra il piano del tavolo / del nastro
    const T = LAYOUT.table;
    if (Math.abs(p.x - T.x) < T.w / 2 + 0.1 && Math.abs(p.y - T.y) < T.d / 2 + 0.06) box.position.z = Math.max(box.position.z, T.h);
    if (p.x > C.x0 && p.x < C.x1 && Math.abs(p.y - C.y) < C.w / 2 + 0.08) box.position.z = Math.max(box.position.z, C.z + 0.002);
  } else if (world.placed) {
    const pl = world.placed;
    const u = ease((t - pl.t) / 0.35);
    const tgt = pl.p.clone(); tgt.z -= B.H + B.hh + 0.012;
    if (pl.where === 'scatola') { tgt.x = cartX; tgt.y = cartonY; tgt.z = C.z + 0.008; }
    box.position.lerpVectors(pl.from, tgt, u);
    box.rotation.set(0, 0, -Math.PI);
  }
  // linea: piegalembi, scotch, nastro, pulsanti
  W.setFlaps(1 - ease((cartX - 2.55) / 0.38));
  W.tape.scale.x = Math.max(0.001, clamp01((cartX - 2.95) / 0.55));
  const running = world.runT != null && t >= world.runT;
  W.flow.material.opacity = running ? 0.85 : 0;
  if (running) W.flowTex.offset.x = -((t - world.runT) * world.runV) / 0.6 * 1.0;
  W.beacon.material.emissiveIntensity = running ? 2.2 : 0;
  W.taperRoll.rotation.y = running && cartX > 2.9 && cartX < 4.0 ? (t * 3) : W.taperRoll.rotation.y;
  W.buttons.forEach((b, i) => {
    const pr = world.pressT != null && i === 0 ? clamp01(1 - Math.abs(t - world.pressT - 0.12) / 0.25) : 0;
    b.position.y = 0.088 - 0.009 * pr;
    b.material.emissiveIntensity = 0.12 + (i === 0 && running ? 1.4 : 0) + pr * 1.5;
  });
}

const _a = new THREE.Vector3();
function updateMarkers(t, st, tl, show) {
  const seg = tl.segs.find(s => t >= s.t0 && t < s.t1);
  if (show && seg && seg.type === 'walk') {
    const pts = [];
    for (let k = 0; k <= 24; k++) { const tt = lerp(Math.max(t, seg.t0), seg.t1, k / 24); const b = tl.basePose(Math.min(tt, seg.t1 - 1e-4)); pts.push(b); }
    MK.setPath(pts, seg.b);
  } else MK.setPath(null);
  const L = show ? tl.landings(t) : [];
  MK.feet.forEach((f, i) => {
    const l = L[i];
    f.visible = !!l;
    if (l) { f.position.set(l.p.x + 0.035 * Math.cos(l.yaw), l.p.y + 0.035 * Math.sin(l.yaw), 0.008); f.rotation.z = l.yaw; f.material.opacity = l.now ? 0.85 : Math.max(0.12, 0.55 - i * 0.07); }
  });
  for (const s of ['L', 'R']) {
    const h = st.hands[s];
    const vis = show && h.p && h.w > 0.05;
    if (vis) { _a.copy(h.p); MK.setHand(s, _a, robot.palmWorld[s], true); MK.hand[s].scale.setScalar(0.8 + 0.2 * Math.sin(t * 6)); }
    else MK.setHand(s, null, null, false);
  }
}

// ------------------------------------------------------------------ UI: robot, coda, piano, RL
const TH = { sim_presa_tanica: 'Presa della tanica dallo scaffale', sim_cassetta_manico: 'Cassetta di viti presa per la maniglia', sim_in_scatola: 'Appoggio nella scatola dell\'ordine 4512', rl_premi: 'Pressione di AVVIO con la policy RL (valutazione 8/8)' };
function thumbFor(p) {
  if (/tanica/i.test(p)) return 'sim_presa_tanica';
  if (/viti|cassetta/i.test(p)) return 'sim_cassetta_manico';
  if (/nastro|spedis|avvia|ferma/i.test(p)) return 'rl_premi';
  return 'sim_in_scatola';
}
const ICON = { g1: 'G1', g1_d: 'G1D', h2: 'H2', go2: 'GO2', a2: 'A2' };
let selRobot = 'g1';
function renderRobots() {
  const want = ['g1', 'g1_d', 'h2', 'go2', 'a2'];
  $('robots').innerHTML = want.map(k => ROBOTS.find(r => r.key === k)).filter(Boolean).map(r => {
    const cls = r.stato === 'attivo' ? 'on' : (r.stato.includes('addestr') ? 'tr' : '');
    const stt = r.stato.replace('in addestramento', 'in addestr.');
    const nm = r.nome.replace(/\s*\(.*$/, '').replace('Unitree ', '');
    return `<li data-k="${r.key}" class="${r.key === selRobot ? 'sel' : ''}"><span class="ico">${ICON[r.key]}</span><div><div class="nm">${nm}</div><div class="sub">${r.tipo} · ${r.locomotion.split(/[,(:]/)[0]}</div></div><span class="tag ${cls}">${stt}</span></li>`;
  }).join('');
}
$('robots').addEventListener('click', e => {
  const li = e.target.closest('li'); if (!li) return;
  selRobot = li.dataset.k; renderRobots();
  const r = ROBOTS.find(x => x.key === selRobot);
  const nt = $('notice');
  if (selRobot === 'g1') { nt.classList.add('hidden'); setChipsEnabled(true); return; }
  nt.innerHTML = `<span class="eyebrow">Robot selezionato</span><h3>${r.nome}</h3>
    <dl><dt>Stato</dt><dd>${r.stato}</dd><dt>Scena</dt><dd>${r.scene}</dd><dt>Locomozione</dt><dd>${r.locomotion}</dd><dt>Sa fare</dt><dd>${r.skills.join(' · ')}</dd></dl>
    <p>In questa vetrina la scena 3D interattiva è quella del G1 nel magazzino. Nel playground vero ${r.key.toUpperCase()} riceve i prompt dalla stessa coda.</p>
    <button class="btn sm" id="backG1">Torna al G1</button>`;
  nt.classList.remove('hidden'); setChipsEnabled(false);
  $('backG1').onclick = () => { selRobot = 'g1'; renderRobots(); nt.classList.add('hidden'); setChipsEnabled(true); };
});

const jobs = [];
function renderQueue() {
  const hist = TAKES.slice(0, 9).map(t => ({
    prompt: t.prompt, thumb: thumbFor(t.prompt), type: t.type === 'eval' ? 'valutazione' : 'comando',
    meta: `${t.sim_s ? fmt(t.sim_s) + ' s sim · ' : ''}${fmt(t.wall_s / 60)} min calcolo`, done: true, id: t.id,
  }));
  const all = [...jobs.slice().reverse(), ...hist];
  $('qcount').textContent = `${jobs.filter(j => !j.done).length} in corso · ${all.length} lavori`;
  $('queue').innerHTML = all.map((j, i) => `<li class="${j.done ? '' : 'run'}" data-clip="${j.thumb}" data-i="${i}">
    <span class="th" style="background-image:url(media/${j.thumb}.jpg)"></span>
    <div><div class="pr">${j.prompt}</div>
    <div class="meta"><span class="tag ${j.done ? '' : 'live'}">${j.done ? (j.ok === false ? 'non riuscito' : j.type) : (j.phase || 'in corso')}</span><span>${j.meta || ''}</span></div>
    ${j.done ? '' : `<div class="bar"><i style="width:${(j.p * 100).toFixed(0)}%"></i></div>`}</div></li>`).join('');
}
$('queue').addEventListener('click', e => { const li = e.target.closest('li'); if (li) openClip(li.dataset.clip); });

function openClip(name) {
  if (!name) return;
  const v = $('clipv'); v.src = `media/${name}.mp4`; v.poster = `media/${name}.jpg`;
  $('cliptxt').textContent = `${TH[name] || ''} · NVIDIA Isaac Lab 3.0, fisica PhysX`;
  $('clipov').classList.remove('hidden'); v.currentTime = 0; v.play().catch(() => {});
}
$('clipx').onclick = () => { $('clipov').classList.add('hidden'); $('clipv').pause(); };

// RL: curve vere da TensorBoard
let rlKey = 'premi';
const RLINFO = {
  premi: { name: 'premi (pulsanti del quadro)', state: 'in servizio', data: RL.premi, x0: 0,
    stats: [['Ambienti paralleli', '2048'], ['Iterazioni PPO', '300 · 16 min GPU'], ['Riuscita in addestramento', '62 / 64', 'y'], ['Valutazione nella scena', '8 / 8 · 0 cadute', 'y']],
    note: 'Claude sceglie il pulsante, la policy porta il dito e preme. Pre-posa e ritorno sono programmati.' },
  chiudi: { name: 'chiudi lembi della scatola', state: 'candidata', data: RL.chiudi, x0: 3700,
    stats: [['Iterazioni PPO', '3700 → 4400'], ['Riuscita in addestramento', 'fino a 100%'], ['Valutazione nella scena', '0 / 2', 'y'], ['Stato', 'non in servizio']],
    note: 'Non supera la valutazione nella scena completa: i lembi li chiude il piegalembi della nastratrice. Dichiarato, non nascosto.' },
};
function drawRL() {
  const cv = $('rlc'), r = cv.getBoundingClientRect(), dpr = Math.min(2, devicePixelRatio);
  cv.width = r.width * dpr; cv.height = r.height * dpr;
  const g = cv.getContext('2d'); g.scale(dpr, dpr);
  const w = r.width, h = r.height, pl = 30, pr = 30, pt = 24, pb = 18;
  const I = RLINFO[rlKey], rew = I.data.mean_reward, suc = I.data.success_rate;
  const xs = rew.map(p => p[0]), xmin = Math.min(...xs), xmax = Math.max(...xs);
  const ymin = Math.min(0, ...rew.map(p => p[1])), ymax = Math.max(...rew.map(p => p[1]));
  const X = x => pl + (x - xmin) / (xmax - xmin) * (w - pl - pr), Y = y => pt + (1 - (y - ymin) / (ymax - ymin)) * (h - pt - pb), Ys = y => pt + (1 - y) * (h - pt - pb);
  g.font = '9px JetBrains Mono'; g.fillStyle = '#5a6066'; g.strokeStyle = '#2a2e33'; g.lineWidth = 1;
  for (let i = 0; i <= 4; i++) { const yy = pt + i * (h - pt - pb) / 4; g.beginPath(); g.moveTo(pl, yy); g.lineTo(w - pr, yy); g.stroke(); }
  g.textAlign = 'right'; g.fillText(Math.round(ymax), pl - 4, pt + 3); g.fillText(Math.round(ymin), pl - 4, h - pb + 3);
  g.textAlign = 'left'; g.fillText('100%', w - pr + 4, pt + 3); g.fillText('0%', w - pr + 4, h - pb + 3);
  g.textAlign = 'center'; g.fillText(`iterazione ${xmin} → ${xmax}`, w / 2, h - 4);
  // riuscita (ciano, area)
  g.beginPath(); suc.forEach((p, i) => i ? g.lineTo(X(p[0]), Ys(p[1])) : g.moveTo(X(p[0]), Ys(p[1])));
  g.strokeStyle = 'rgba(95,212,230,.75)'; g.lineWidth = 1; g.stroke();
  // ricompensa (giallo)
  g.beginPath(); rew.forEach((p, i) => i ? g.lineTo(X(p[0]), Y(p[1])) : g.moveTo(X(p[0]), Y(p[1])));
  g.strokeStyle = '#f2c200'; g.lineWidth = 2; g.stroke();
  g.textAlign = 'left'; g.font = '600 9px JetBrains Mono';
  g.fillStyle = '#f2c200'; g.fillText('■ ricompensa media', pl, 9);
  g.fillStyle = '#5fd4e6'; g.fillText('■ riuscita (asse destro)', pl + 118, 9);
  $('rlstats').innerHTML = `<div class="full"><span class="tag ${I.state === 'in servizio' ? 'on' : 'tr'}">${I.state}</span> ${I.name} · PPO, Isaac Lab</div>` +
    I.stats.map(s => `<div>${s[0]}<b class="${s[2] || ''}">${s[1]}</b></div>`).join('') + `<div class="full">${I.note}</div>`;
}
document.querySelectorAll('.tab').forEach(b => b.onclick = () => { document.querySelectorAll('.tab').forEach(x => x.classList.toggle('on', x === b)); rlKey = b.dataset.k; drawRL(); });
new ResizeObserver(drawRL).observe($('rlc'));

function demoJob(prompt, thumb, dur, phases, endMeta, ok = true) {
  const j = { prompt, thumb, type: 'valutazione', p: 0, done: false, t0: NOW(), dur, phases, endMeta, ok };
  jobs.push(j); renderQueue(); return j;
}
$('bEval').onclick = () => demoJob('Prova 8 volte a premere AVVIO (policy RL)', 'rl_premi', 9000, ['episodio 1/8', 'episodio 4/8', 'episodio 8/8'], 'riuscite 8/8 · 0 cadute (risultato vero press_eval_rl2)');
$('bTrain').onclick = () => demoJob('Addestra premi: PPO, 2048 ambienti, 300 iterazioni', 'rl_premi', 12000, ['iter 40/300', 'iter 160/300', 'iter 300/300'], '62/64 in addestramento (replica della corsa del 4 nov)');

// ------------------------------------------------------------------ chip ed esecuzione
let spend = 0;
function setChipsEnabled(on) { document.querySelectorAll('.chip').forEach(c => c.disabled = !on); $('psend').disabled = !on; }
$('chips').innerHTML = SCENARI.map((s, i) => `<button class="chip ${s.real ? 'real' : ''}" data-i="${i}" type="button"><b>${String(i + 1).padStart(2, '0')}</b>${s.chip}</button>`).join('');
$('chips').addEventListener('click', e => { const b = e.target.closest('.chip'); if (!b) return; const sc = SCENARI[+b.dataset.i]; $('pin').value = sc.prompt; submit(sc.prompt); });
$('pform').addEventListener('submit', e => { e.preventDefault(); submit($('pin').value || $('pin').placeholder); });
$('bReset').onclick = () => { run = null; resetWorld(); robot.reset(); IDLE.tl = idleTimeline(); IDLE.t0 = NOW(); setStatus('Pronto · magazzino riportato allo stato iniziale', false); };
let follow = false;
$('bFollow').onclick = () => { follow = !follow; $('bFollow').classList.toggle('on', follow); };

function setStatus(txt, busy) { $('statustxt').textContent = txt; $('status').classList.toggle('busy', !!busy); }

function submit(text, opts = {}) {
  if (run && !run.finished) { setStatus('Il robot sta eseguendo il comando precedente: il nuovo andrebbe in coda (in questa vetrina, attendi la fine)', true); return; }
  const sc = route(text);
  const plan = $('plan');
  if (!sc) {
    plan.innerHTML = `<p class="q">${esc(text)}</p><div class="reply"><span class="eyebrow">Claude · nessun movimento</span>In questa vetrina il G1 conosce la scena del magazzino: tavolo, cassetta rossa, nastro, scatola dell'ordine 4512 e quadro NASTRO 1. Prova con uno degli esempi qui sotto.</div>`;
    $('planmeta').textContent = 'fuori scena';
    return;
  }
  start(sc, text, opts.offset || 0, opts.thinkMs ?? 1500);
}
const esc = s => s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));

function start(sc, text, offset = 0, thinkMs = 1500) {
  resetWorld(); robot.reset();
  const tl = sc.build(robot, W);
  const now = NOW();
  run = { sc, tl, text, tPlan: now, t0: now + thinkMs - offset * 1000, thinkMs, finished: false, shown: 0 };
  const job = { prompt: text, thumb: sc.clip || 'sim_in_scatola', type: 'comando', p: 0, done: false, phase: 'pianifica' };
  jobs.push(job); run.job = job; renderQueue();
  $('clipov').classList.add('hidden');
  const plan = $('plan');
  plan.innerHTML = `<p class="q">${esc(text)}</p><div class="thinking" id="think"><i></i><i></i><i></i> ${sc.model} sta pianificando…</div>
    <ol id="steps">${tl.steps.map((s, i) => `<li data-i="${i}"><span class="ck"></span><div><div class="lb">${s.label}${s.rl ? '<span class="rlb">RL</span>' : ''}</div><div class="tl"><code>${s.tool}</code></div></div></li>`).join('')}</ol>
    <div id="replybox"></div>`;
  $('planmeta').textContent = `${tl.steps.length} passi · ${sc.cost}`;
  setStatus(`${sc.model} trasforma il comando in un piano…`, true);
}

function updatePlan(now) {
  if (!run) return;
  const { tl, sc } = run;
  const t = (now - run.t0) / 1000;
  const sinceP = (now - run.tPlan) / 1000;
  const lis = document.querySelectorAll('#steps li');
  // i passi compaiono uno alla volta durante la pianificazione
  const showN = Math.min(lis.length, Math.max(0, Math.floor((sinceP - run.thinkMs / 1000 * 0.45) / (run.thinkMs / 1000 * 0.5 / lis.length))));
  lis.forEach((li, i) => {
    if (i < showN || t > 0) li.classList.add('in');
    const s = tl.steps[i];
    li.classList.toggle('run', t >= s.t0 && t < s.t1);
    li.classList.toggle('done', t >= s.t1);
    li.querySelector('.ck').textContent = t >= s.t1 ? '✓' : '';
  });
  const th = $('think');
  if (th && t >= 0) { th.innerHTML = `Piano pronto · ${tl.steps.length} passi · costo del prompt <b class="num">${sc.cost}</b>`; th.classList.remove('thinking'); th.classList.add('thinking', 'ok'); if (!run.costed) { run.costed = true; spend += parseFloat(sc.cost.replace(',', '.')); $('spend').textContent = fmt(spend, 2) + ' $'; } }
  const job = run.job;
  if (t < 0) { job.phase = 'pianifica'; job.p = clamp01(sinceP / (run.thinkMs / 1000)) * 0.08; }
  else if (!run.finished) {
    const cur = tl.steps.findIndex(s => t < s.t1);
    job.p = 0.08 + 0.92 * clamp01(t / tl.T); job.phase = `passo ${Math.max(1, cur + 1)}/${tl.steps.length}`;
    setStatus(`In esecuzione · ${tl.steps[Math.max(0, cur)].label.toLowerCase()} · passo ${cur + 1} di ${tl.steps.length}`, true);
    if (t >= tl.T) {
      run.finished = true; job.done = true; job.meta = `${fmt(tl.T)} s · ${sc.cost}`;
      $('replybox').innerHTML = `<div class="reply"><span class="eyebrow">Risposta di Claude · esito verificato</span>${sc.reply}</div>` +
        (sc.clip ? `<div class="acts"><button class="btn sm" id="bClip">▶ Ripresa vera Isaac</button></div>` : '');
      if (sc.clip) $('bClip').onclick = () => openClip(sc.clip);
      setStatus('Fatto · scrivi il prossimo comando', false);
    }
  }
  if ((now | 0) % 6 === 0 || run.finished) renderQueueThrottled();
}
let lastQ = 0;
function renderQueueThrottled() { const n = NOW(); if (n - lastQ > 250) { lastQ = n; renderQueue(); } }
function updateDemoJobs(now) {
  let ch = false;
  for (const j of jobs) if (!j.done && j.dur) {
    j.p = clamp01((now - j.t0) / j.dur); j.phase = j.phases[Math.min(j.phases.length - 1, Math.floor(j.p * j.phases.length))];
    if (j.p >= 1) { j.done = true; j.meta = j.endMeta; }
    ch = true;
  }
  if (ch) renderQueueThrottled();
}

// ------------------------------------------------------------------ regia (?regia=1): ~45 s
const RG = {
  prompt: SCENARI[0].prompt,
  typeA: 2.4, typeB: 7.6, enter: 8.0, planA: 8.6, wakeA: 12.6, wakeB: 15.0, execA: 15.0, cutA: 33.4, cutB: 39.6, titleA: 39.8, END: 45.0,
};
let regia = null;
function regiaInit() {
  $('regia').classList.remove('hidden');
  const off = parseFloat(Q.get('t') || '0');
  regia = { t0: NOW() - off * 1000, phase: '' };
  window.__regiaFine = false;
  $('pin').value = '';
  const v = $('clipv'); v.src = 'media/sim_cassetta_manico.mp4'; v.preload = 'auto'; v.load();
}
const camKeys = [ // t (scena regia), posizione, bersaglio
  [12.0, [-0.3, -0.85, 1.15], [-1.35, 0.1, 0.8]],
  [15.0, [-0.1, -1.6, 1.45], [-1.2, 0.15, 0.9]],
  [18.5, [-1.6, -1.6, 1.7], [-0.4, 0.7, 0.85]],
  [22.5, [0.5, 0.3, 1.35], [-0.4, 1.1, 0.95]],
  [25.5, [0.95, -0.55, 1.55], [-0.15, 0.45, 0.85]],
  [29.0, [1.5, -2.1, 1.3], [0.45, -0.45, 0.8]],
  [33.4, [1.15, -1.95, 1.1], [0.45, -0.7, 0.75]],
];
function camAt(t) {
  let i = 0; while (i < camKeys.length - 2 && camKeys[i + 1][0] <= t) i++;
  const a = camKeys[i], b = camKeys[i + 1];
  const u = ease((t - a[0]) / (b[0] - a[0]));
  const p = new THREE.Vector3(...a[1]).lerp(new THREE.Vector3(...b[1]), u);
  const q = new THREE.Vector3(...a[2]).lerp(new THREE.Vector3(...b[2]), u);
  p.z += 0.02 * Math.sin(t * 0.9); p.x += 0.03 * Math.sin(t * 0.37);
  return [p, q];
}
function regiaFrame(now) {
  const T = (now - regia.t0) / 1000;
  const fade = $('rgFade'), tp = $('rgType'), ti = $('rgTitle'), low = $('rgLower');
  // 1) buio e digitazione
  const n = Math.floor(clamp01((T - RG.typeA) / (RG.typeB - RG.typeA)) * RG.prompt.length);
  $('rgText').textContent = RG.prompt.slice(0, n);
  tp.style.opacity = T < RG.enter ? 1 : 1 - clamp01((T - RG.enter) / 0.5);
  tp.querySelector('.cursor').style.opacity = (T < RG.typeA || T > RG.typeB) ? (Math.floor(T * 2.2) % 2) : 1;
  if (T >= RG.enter - 0.25 && T < RG.enter + 0.2) tp.style.transform = `translate(-50%, -50%) scale(${1 + 0.02 * Math.sin((T - RG.enter + 0.25) * 7)})`;
  // 2) piano: la scena si accende piano, il robot è spento
  const sceneVis = clamp01((T - RG.enter) / 1.6);
  fade.style.opacity = T < RG.cutB ? (1 - sceneVis * 0.82 - clamp01((T - RG.wakeA) / 1.5) * 0.18) : clamp01((T - RG.cutB) / 0.4);
  $('pPlan').style.opacity = T < RG.planA ? 0 : (T < RG.cutA ? 1 : 0);
  $('pPlan').style.transform = T < RG.planA + 0.5 ? `translateX(${(1 - ease((T - RG.planA) / 0.5)) * 40}px)` : 'none';
  document.querySelector('.promptwrap').style.opacity = (T > RG.enter && T < RG.cutA) ? 1 : 0;
  if (T >= RG.enter && !regia.started) {
    regia.started = true; $('pin').value = RG.prompt;
    start(SCENARI[0], RG.prompt, 0, (RG.execA - RG.enter) * 1000);
    run.regia = true;
  }
  if (run && run.regia) {
    run.t0 = regia.t0 + RG.execA * 1000; // tempo della scena ancorato alla regia
    run.tPlan = regia.t0 + RG.enter * 1000;
    run.thinkMs = (RG.planA + 3.0 - RG.enter) * 1000;
  }
  // luci: il robot si "sveglia"
  const wake = clamp01((T - RG.wakeA) / (RG.wakeB - RG.wakeA));
  sun.intensity = lerp(0.35, 2.3, ease(wake)); hemi.intensity = lerp(0.18, 0.9, ease(wake));
  spot.intensity = 30 * (1 - ease(clamp01((T - RG.wakeB) / 2))) * clamp01((T - RG.enter) / 1.5);
  spot.target.position.set(-1.3, 0.05, 0.6);
  // camera
  const [p, q] = T < 12 ? [new THREE.Vector3(-0.3 + 0.03 * T, -0.85, 1.15), new THREE.Vector3(-1.35, 0.1, 0.8)] : camAt(T);
  camera.position.copy(p); camera.lookAt(q);
  // 3) stacco sulla ripresa vera
  const ov = $('clipov'), v = $('clipv');
  if (T >= RG.cutA && T < RG.cutB) {
    if (ov.classList.contains('hidden')) { ov.classList.remove('hidden'); $('clipx').classList.add('hidden'); $('cliptxt').textContent = ''; ov.querySelector('.cliplab').classList.add('hidden'); v.currentTime = 2; v.play().catch(() => {}); }
    const want = 2 + (T - RG.cutA);
    if (Math.abs(v.currentTime - want) > 0.35 && v.readyState >= 2) v.currentTime = want;
    low.style.opacity = T > RG.cutA + 0.4 ? 1 : 0;
    low.innerHTML = 'Ripresa vera · NVIDIA Isaac Lab · fisica PhysX<small>G1 nel magazzino simulato, cassetta presa per la maniglia · registrata il 4 novembre 2026</small>';
  } else if (T >= RG.cutB) { ov.classList.add('hidden'); v.pause(); low.style.opacity = 0; }
  // 4) titolo
  const tt = clamp01((T - RG.titleA) / 0.7);
  ti.style.opacity = T < RG.END - 0.6 ? tt : clamp01((RG.END - T) / 0.6) + 0.0001 * 0;
  ti.querySelector('h1').style.letterSpacing = `${lerp(0.08, -0.02, ease(tt))}em`;
  $('rgSub').style.opacity = clamp01((T - RG.titleA - 1.2) / 0.6);
  if (T >= RG.END) { ti.style.opacity = 0; fade.style.opacity = 1; if (!window.__regiaFine) { window.__regiaFine = true; document.body.dataset.regiaFine = '1'; } }
  return T;
}

// ------------------------------------------------------------------ ciclo principale
function frame() {
  requestAnimationFrame(frame);
  const now = NOW();
  let rt = null;
  if (regia) rt = regiaFrame(now);
  let tl, t;
  if (run) { tl = run.tl; t = Math.max(0, (now - run.t0) / 1000); }
  else { tl = IDLE.tl; t = (now - IDLE.t0) / 1000; }
  let st = tl.eval(Math.min(t, tl.T));
  if (tl.look) st.waist.yaw = tl.look(t);
  // in regia, prima della "sveglia" il robot è accucciato e spento
  if (regia && rt != null && rt < RG.wakeB + 0.4) {
    const w = 1 - ease(clamp01((rt - RG.wakeA - 0.3) / (RG.wakeB - RG.wakeA)));
    st.base.z -= 0.13 * w; st.waist.pitch += 0.42 * w; st.base.pitch += 0.1 * w;
    for (const s of ['L', 'R']) st.hands[s].restOff = new THREE.Vector3(-0.06 * w, 0, -0.14 * w);
  }
  robot.apply(st);
  updateWorld(t, st, tl);
  updateMarkers(t, st, tl, !!run && t > 0 && t < tl.T);
  if (run) updatePlan(now);
  updateDemoJobs(now);
  if (follow && !regia) { const p = robot.pelvis.position; controls.target.lerp(new THREE.Vector3(p.x, p.y, 0.75), 0.04); }
  if (!regia) controls.update();
  composer.render();
  $('clock').textContent = new Date().toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });
}

// ------------------------------------------------------------------ avvio
(async () => {
  const s = SYSTEM, m = s.measured[0];
  $('sysline').textContent = `Isaac Lab 3.0 · PhysX · ${s.gpu.replace('NVIDIA GeForce ', '')} ${Math.round(s.vram_gb)} GB · misurato ${fmt(m.rtf, 2)}× tempo reale · Claude Opus 5.5`;
  renderRobots(); renderQueue(); drawRL();
  robot = await loadG1('asset/');
  scene.add(robot.root);
  resetWorld();
  IDLE.tl = idleTimeline(); IDLE.t0 = NOW();
  resize();
  $('loading').style.opacity = 0; setTimeout(() => $('loading').remove(), 600);
  if (Q.get('cam')) { const c = Q.get('cam').split(',').map(Number); camera.position.set(c[0], c[1], c[2]); controls.target.set(c[3], c[4], c[5]); }
  if (REGIA) regiaInit();
  else if (Q.get('demo')) { const sc = SCENARI.find(x => x.id === Q.get('demo')); if (sc) { $('pin').value = sc.prompt; start(sc, sc.prompt, parseFloat(Q.get('t') || '0'), Q.get('t') ? 0 : 1500); } }
  frame();
})();
