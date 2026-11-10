// Scenari pre-scriptati: piano di Claude (passi + chiamate alle abilità vere del playground) e timeline del movimento.
import * as THREE from 'three';
import { Timeline, ease } from './robot.js';
import { LAYOUT } from './scene.js';

const V = (x, y, z) => new THREE.Vector3(x, y, z);
const HALF = Math.PI / 2;
const qGrip = yaw => new THREE.Quaternion().setFromEuler(new THREE.Euler(0, 0.35, yaw, 'ZYX'));
const qPress = yaw => new THREE.Quaternion().setFromEuler(new THREE.Euler(0, 0.35, yaw, 'ZYX'));

// posizione "in mano" durante il trasporto, nel riferimento del bacino
function carry(tl, side = 'R') {
  return t => {
    const b = tl.basePose(t), c = Math.cos(b.yaw), s = Math.sin(b.yaw);
    const lx = 0.3, ly = side === 'R' ? -0.17 : 0.17, z = 0.84;
    return V(b.x + lx * c - ly * s, b.y + lx * s + ly * c, z);
  };
}

// orientamento della mano in trasporto: segue il busto (non resta fisso nel mondo mentre il robot gira)
const carryQ = tl => t => qGrip(tl.basePose(t).yaw);

// presa della cassetta dal tavolo; ritorna i tempi chiave
function pickToolbox(tl) {
  const B = LAYOUT.box, T = LAYOUT.table;
  const handle = V(B.x, B.y, T.h + B.H + B.hh);
  const t0 = tl.t;
  tl.walk(B.x - 0.13, 0.74, HALF);
  const tA = tl.t;
  tl.hand('R', 0.15, handle.clone().add(V(0.02, -0.12, 0.16)), 0, qGrip(HALF));
  tl.hand('R', 1.05, handle.clone().add(V(0, -0.02, 0.14)), 1, qGrip(HALF));
  tl.hand('R', 1.75, handle.clone().add(V(0, 0, 0.012)), 1, qGrip(HALF));
  tl.hand('R', 2.05, handle.clone().add(V(0, 0, 0.012)), 1, qGrip(HALF));
  tl.ev(2.0, 'attach', 'cassetta');
  tl.hand('R', 2.9, handle.clone().add(V(0, -0.05, 0.2)), 1, qGrip(HALF));
  tl.stand(3.0, { crouch: t => ease((t - tA - 0.5) / 0.8) * (1 - ease((t - tA - 2.2) / 0.7)) });
  const tB = tl.t;
  return { t0, tA, tB, handle };
}

function placeAt(tl, standX, standY, dropP, label) {
  const high = label === 'scatola' ? 0.26 : 0.1;
  const t0 = tl.t;
  tl.hand('R', 0.7, carry(tl), 1, carryQ(tl));
  tl.walk(standX, standY, -HALF);
  const tA = tl.t;
  tl.hand('R', 0.0, carry(tl), 1, carryQ(tl));
  tl.hand('R', 0.9, dropP.clone().add(V(0, 0.05, high)), 1, qGrip(-HALF));
  tl.hand('R', 1.6, dropP.clone(), 1, qGrip(-HALF));
  tl.ev(1.75, 'release', { obj: 'cassetta', where: label, p: dropP.clone() });
  tl.hand('R', 2.5, dropP.clone().add(V(0, 0.08, 0.2)), 0.6, qGrip(-HALF));
  tl.hand('R', 3.2, null, 0);
  tl.stand(3.3, { crouch: t => ease((t - tA - 0.4) / 0.8) * (1 - ease((t - tA - 2.0) / 0.8)) });
  return { t0, tA, tB: tl.t };
}

function pressButton(tl, idx, W) {
  const bp = W.buttonPos(idx);
  tl.walk(bp.x - 0.4, bp.y + 0.13, 0);
  const tA = tl.t;
  tl.hand('R', 0.2, bp.clone().add(V(-0.16, 0, 0.05)), 0, qPress(0));
  tl.hand('R', 1.0, bp.clone().add(V(-0.12, 0, 0.02)), 1, qPress(0));
  tl.hand('R', 1.55, bp.clone().add(V(-0.005, 0, 0)), 1, qPress(0));
  tl.hand('R', 1.85, bp.clone().add(V(-0.005, 0, 0)), 1, qPress(0));
  tl.ev(1.6, 'press', idx);
  tl.hand('R', 2.5, bp.clone().add(V(-0.18, 0, 0)), 0.7, qPress(0));
  tl.hand('R', 3.1, null, 0);
  tl.stand(3.2);
  return { tA, tB: tl.t };
}

export const SCENARI = [
  {
    id: 'nastro', chip: 'Cassetta sul nastro',
    prompt: 'Prendi la cassetta rossa dal tavolo e mettila sul nastro',
    cost: '0,07 $', model: 'Claude Opus 5.5', clip: 'sim_cassetta_manico',
    reply: 'Ho preso la cassetta rossa dal tavolo per il manico, con la mano destra, e l\'ho appoggiata sul nastro davanti all\'imballaggio. Il nastro resta fermo: non mi hai chiesto di avviarlo.',
    build(robot, W) {
      const tl = new Timeline(robot, LAYOUT.home);
      tl.stand(0.5);
      const p = pickToolbox(tl);
      const C = LAYOUT.conv;
      const drop = V(0.5, -0.83, C.z + LAYOUT.box.H + LAYOUT.box.hh + 0.012);
      const q = placeAt(tl, 0.62, -0.36, drop, 'nastro');
      tl.walk(0.62, 0.05, -HALF).stand(0.8).end();
      tl.step('Avvicinati al tavolo', 'vai("tavolo")', p.t0, p.tA, { path: true });
      tl.step('Alza il braccio destro sopra il manico', 'prendi("cassetta rossa") · pre-posa', p.tA, p.tA + 1.05);
      tl.step('Aggancia il manico dall\'alto', 'prendi · presa dall\'alto, una mano', p.tA + 1.05, p.tA + 2.05);
      tl.step('Solleva di 20 cm', 'prendi · verifica presa', p.tA + 2.05, p.tB);
      tl.step('Porta la cassetta al nastro', 'vai("nastro")', q.t0, q.tA, { path: true });
      tl.step('Rilascia sul nastro', 'appoggia("nastro")', q.tA, q.tA + 2.5);
      tl.step('Ritira il braccio e riferisci', 'fine(messaggio)', q.tA + 2.5, tl.T);
      return tl;
    },
  },
  {
    id: 'spedisci', chip: 'Inscatola e spedisci',
    prompt: 'Metti la cassetta rossa nella scatola dell\'ordine 4512 e spediscila',
    cost: '0,09 $', model: 'Claude Opus 5.5', clip: 'sim_in_scatola',
    reply: 'Ho messo la cassetta rossa nella scatola dell\'ordine 4512 e ho premuto AVVIO. I lembi li chiude il piegalembi della nastratrice, poi lo scotch: la scatola è arrivata alle spedizioni.',
    build(robot, W) {
      const tl = new Timeline(robot, LAYOUT.home);
      tl.stand(0.5);
      const p = pickToolbox(tl);
      const K = LAYOUT.carton, C = LAYOUT.conv;
      const drop = V(K.x, -0.86, C.z + 0.012 + LAYOUT.box.H + LAYOUT.box.hh + 0.02);
      const q = placeAt(tl, K.x + 0.12, -0.4, drop, 'scatola');
      const tP0 = tl.t;
      const r = pressButton(tl, 0, W);
      tl.ev(r.tA + 1.6 - tl.t, 'run', 0.34);
      tl.walk(LAYOUT.panel.x - 0.75, 0.15, -0.5).stand(5.2).end();
      tl.step('Avvicinati al tavolo', 'vai("tavolo")', p.t0, p.tA, { path: true });
      tl.step('Aggancia il manico della cassetta', 'prendi("cassetta rossa")', p.tA, p.tA + 2.05);
      tl.step('Solleva', 'prendi · verifica presa', p.tA + 2.05, p.tB);
      tl.step('Porta alla scatola 4512', 'vai("imballaggio")', q.t0, q.tA, { path: true });
      tl.step('Appoggia sul fondo della scatola', 'metti_in_scatola()', q.tA, q.tB);
      tl.step('Premi AVVIO sul quadro', 'premi("AVVIO") · policy RL', tP0, r.tB, { rl: true });
      tl.step('Lembi e scotch: nastratrice', 'piegalembi + nastratrice (linea)', r.tB, r.tB + 6.5);
      tl.step('Riferisci', 'fine(messaggio)', r.tB + 6.5, tl.T);
      return tl;
    },
  },
  {
    id: 'premi', chip: 'Avvia il nastro',
    prompt: 'Avvia il nastro.',
    cost: '0,05 $', model: 'Claude Opus 5.5', clip: 'rl_premi',
    reply: 'Avvio il nastro come richiesto. Attenzione: la scatola all\'imballaggio è aperta e vuota. Con il nastro in marcia verrà chiusa, sigillata con lo scotch e spedita vuota. Il nastro resta in marcia finché qualcuno non preme STOP.',
    real: true,
    build(robot, W) {
      const tl = new Timeline(robot, LAYOUT.home);
      tl.stand(0.5);
      const t0 = tl.t;
      const r = pressButton(tl, 0, W);
      tl.ev(r.tA + 1.6 - tl.t, 'run', 0.34);
      tl.stand(7.5).end();
      tl.step('Vai al quadro NASTRO 1', 'vai("quadro")', t0, r.tA, { path: true });
      tl.step('Porta il dito su AVVIO e premi', 'premi("AVVIO") · policy RL PPO', r.tA, r.tA + 2.0, { rl: true });
      tl.step('Ritira la mano', 'premi · ritorno programmato', r.tA + 2.0, r.tB);
      tl.step('Controlla la linea e riferisci', 'fine(messaggio)', r.tB, tl.T);
      return tl;
    },
  },
  {
    id: 'rifiuto', chip: 'Articolo che non c\'è',
    prompt: 'Metti nella scatola una tanica di olio motore 10W40.',
    cost: '0,03 $', model: 'Claude Opus 5.5', clip: null, real: true,
    reply: 'Non ho trovato olio motore 10W40. Allo scaffale oli ci sono solo taniche da 2 litri di olio idraulico, refrigerante e sgrassante. Non ho messo niente nella scatola: è ancora vuota e aperta alla stazione di imballaggio, e il nastro è fermo. Per continuare, dimmi quale articolo vuoi.',
    build(robot, W) {
      const tl = new Timeline(robot, LAYOUT.home);
      tl.stand(0.6);
      const t0 = tl.t;
      tl.segs.push({ type: 'stand', t0: tl.t, t1: tl.t + 3.4, a: { ...tl.pose }, b: { ...tl.pose } });
      tl.t += 3.4; tl.stand(0.6).end();
      tl.look = t => 0.75 * ease((t - t0) / 0.8) * (1 - ease((t - t0 - 2.6) / 0.8));
      tl.step('Cerca "olio motore 10W40" nel catalogo', 'stato della scena · scaffale A', t0, t0 + 1.6);
      tl.step('Articolo assente: nessun movimento', 'fine(messaggio)', t0 + 1.6, tl.T);
      return tl;
    },
  },
];

// testo libero -> scenario più vicino (parole chiave), come fa il router vero ma senza modello
export function route(text) {
  const s = text.toLowerCase();
  if (/10w|motore|non c'è|olio motore/.test(s)) return SCENARI[3];
  if (/scatola|spedis|ordine|4512/.test(s)) return SCENARI[1];
  if (/avvia|avvio|premi|pulsante|nastro\.?$/.test(s) && !/cassetta|prendi/.test(s)) return SCENARI[2];
  if (/cassetta|prendi|nastro|manico|tavolo/.test(s)) return SCENARI[0];
  return null;
}
