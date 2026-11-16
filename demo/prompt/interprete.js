// Interprete a sole regole (come "L0" della pipeline vera): legge la frase, completa con valori tipici,
// calcola schema di posa, pinza, payload, tempi e controlli. Nessuna libreria, nessuna chiamata esterna.
// Il caso di riferimento (frase esatta dei due scenari) resta quello registrato: vedi `costruisci`.
import { SCENARI } from "./scenari.js";

export const num = (v, d = 1) => v.toFixed(d).replace(".", ",");
const f2 = (s) => parseFloat(String(s).replace(",", "."));
const NUMW = { uno: 1, una: 1, due: 2, tre: 3, quattro: 4, cinque: 5, sei: 6, sette: 7, otto: 8, nove: 9, dieci: 10, undici: 11, dodici: 12 };
const NOMI = { scatole: ["scatola", "scatole"], cartoni: ["cartone", "cartoni"], sacchi: ["sacco", "sacchi"], casse: ["cassa", "casse"] };
const ROBOT = {
  ur3e: { n: "UR3e", pay: 3, reach: 0.5 }, ur5e: { n: "UR5e", pay: 5, reach: 0.85 }, ur10e: { n: "UR10e", pay: 12.5, reach: 1.3 },
  ur16e: { n: "UR16e", pay: 16, reach: 0.9 }, ur20: { n: "UR20", pay: 20, reach: 1.75 }, ur30: { n: "UR30", pay: 30, reach: 1.3 },
};
const RHO = { acciaio: 7850, alluminio: 2700, ottone: 8500, plastica: 1200 };
const PALLET = {
  eur: { nome: "EUR", PL: 1200, PW: 800, txt: "EUR 1200×800" },
  ind: { nome: "industriale", PL: 1200, PW: 1000, txt: "industriale 1200×1000" },
  mezzo: { nome: "mezzo pallet", PL: 800, PW: 600, txt: "mezzo pallet 800×600" },
};
const ALT_PAL = 144, ALT_MAX = 1800, CARICO_MAX = 1000, CUP_N = 147.75, G = 9.81; // 4 coppe Ø56 = 591 N
const PX = 0, PY = 0.959, CX = -0.715, CTOP = 0.652, ZBASE = 0.4;

// ---------------------------------------------------------------- lettura della frase
const NUMRE = "(\\d+(?:[.,]\\d+)?)";
const mm = (v, u, def) => { // valore + unità → millimetri; senza unità: ≥100 mm, ≥10 cm, altrimenti metri
  if (u === "mm") return v; if (u === "cm") return v * 10; if (u === "m") return v * 1000;
  return def ? def(v) : v;
};

export function interpreta(testo) {
  let t = " " + String(testo || "").toLowerCase().replace(/[×✕]/g, "x").replace(/ /g, " ") + " ";
  const prendi = (re) => { const m = re.exec(t); if (!m) return null; t = t.slice(0, m.index) + " ".repeat(m[0].length) + t.slice(m.index + m[0].length); return m; };

  // processo
  const CNC = /\b(cnc|tornio|torni|fresa|fresatrice|asserviment\w*|macchina utensile|macchine utensili|lathe|centro di lavoro)\b/;
  const PAL = /pallet|bancal|scatol|cartoni|cartone|sacchi|sacco|\bcasse\b|\bcassa\b|catasta/;
  const DEB = /billett|grezz|pressa|pezzi tondi|pezzo tondo|\bcarico\b|\bscarico\b|\bmacchina\b/;
  let processo = null;
  if (/pallettiz|palletiz/.test(t)) processo = "pallet";
  else if (CNC.test(t)) processo = "cnc";
  else if (PAL.test(t)) processo = "pallet";
  else if (DEB.test(t)) processo = "cnc";

  const c = {}; // campi letti dal testo
  // robot
  let m = prendi(/\bur\s?-?(3e|5e|10e|16e|20|30)\b/); if (m) c.robot = "ur" + m[1];
  // diametro e lunghezza (Ø50, d50, diametro 50, Ø50x120, lunghi 120 mm)
  m = prendi(new RegExp("(?:ø|⌀|\\bd(?![a-z]))\\s*" + NUMRE + "\\s*x\\s*" + NUMRE + "\\s*(mm|cm)?"));
  if (m) { c.d = mm(f2(m[1]), m[3]); c.Lp = mm(f2(m[2]), m[3]); }
  if (c.d == null) {
    m = prendi(new RegExp("(?:ø|⌀|\\bdiametro(?:\\s+di)?|\\bdiam\\.?|\\bdia\\.?|\\bd(?![a-z]))\\s*" + NUMRE + "\\s*(mm|cm)?"));
    if (m) c.d = mm(f2(m[1]), m[2]);
  }
  if (c.Lp == null) {
    m = prendi(new RegExp("(?:\\blung\\w*|\\bl\\s*=)\\s*(?:di\\s*|circa\\s*)?" + NUMRE + "\\s*(mm|cm)?"));
    if (m) c.Lp = mm(f2(m[1]), m[2]);
  }
  m = prendi(new RegExp("\\balt[oaei]\\w*\\s*(?:di\\s*|circa\\s*)?" + NUMRE + "\\s*(mm|cm)?")); if (m) c.altezza = mm(f2(m[1]), m[2], (v) => (v < 10 ? v * 1000 : v < 100 ? v * 10 : v));
  // massa
  m = prendi(new RegExp(NUMRE + "\\s*(?:kg|kili|chili|kilogramm\\w*|kilo)\\b"));
  if (m) c.mass = f2(m[1]);
  else { m = prendi(new RegExp(NUMRE + "\\s*(?:grammi|gr|g)\\b")); if (m) c.mass = f2(m[1]) / 1000; }
  // strati
  m = prendi(new RegExp("(\\d+|" + Object.keys(NUMW).join("|") + ")\\s*(?:strati|strato|layer|piani|livelli)\\b"));
  if (m) c.strati = NUMW[m[1]] || parseInt(m[1], 10);
  // cadenza
  const UN = "(?:pezzi|pz|scatole|cartoni|sacchi|colli|casse|cicli)?";
  m = prendi(new RegExp(NUMRE + "\\s*" + UN + "\\s*(?:\\/|al\\s+|all'|l'|per\\s+|a\\s+)\\s*(?:ora|h)\\b")) || prendi(new RegExp(NUMRE + "\\s*(?:pezzi|pz|scatole|cartoni|sacchi|colli|casse)\\s+orari\\b"));
  if (m) c.rate = f2(m[1]);
  else {
    m = prendi(new RegExp(NUMRE + "\\s*" + UN + "\\s*(?:\\/|al\\s+|per\\s+)\\s*(?:min|minuto)\\b"));
    if (m) c.rate = f2(m[1]) * 60;
    else { m = prendi(new RegExp("ogni\\s+" + NUMRE + "\\s*(s|sec|secondi|min|minuti)\\b")); if (m) { const s = /^m/.test(m[2]) ? f2(m[1]) * 60 : f2(m[1]); if (s > 0) c.rate = 3600 / s; } }
  }
  // materiale
  m = /acciaio|inox|alluminio|aluminium|alluminum|\balu\b|ottone|plastic\w*|\bpom\b|nylon|pvc|\babs\b|delrin/.exec(t);
  if (m) c.mat = /allum|alu/.test(m[0]) ? "alluminio" : /ottone/.test(m[0]) ? "ottone" : /acciaio|inox/.test(m[0]) ? "acciaio" : "plastica";
  // tipo di collo
  if (/sacch|\bsacco\b/.test(t)) c.tipo = "sacchi"; else if (/cartone|cartoni/.test(t)) c.tipo = "cartoni"; else if (/\bcass[ae]\b|cassett/.test(t)) c.tipo = "casse"; else if (/scatol/.test(t)) c.tipo = "scatole";

  // pallet: nomi e misure; dimensioni del collo: prima catena di tre numeri, oppure due
  const kw = []; { const r = /europallet|epal|pallet|bancale|bancali/g; let k; while ((k = r.exec(t))) kw.push({ s: k.index, e: k.index + k[0].length }); }
  if (/europallet|epal|\beur2?\b/.test(t)) c.pal = "eur";
  else if (/industrial\w*/.test(t)) c.pal = "ind";
  else if (/mezzo\s+(?:pallet|bancale)|half\s*pallet|mezzo\b/.test(t)) c.pal = "mezzo";
  const CH = new RegExp(NUMRE + "\\s*x\\s*" + NUMRE + "(?:\\s*x\\s*" + NUMRE + ")?\\s*(mm|cm|m)?(?![a-z0-9])", "g");
  const catene = []; { let k; while ((k = CH.exec(t))) catene.push({ s: k.index, e: k.index + k[0].length, v: [k[1], k[2], k[3]].filter((x) => x != null).map(f2), u: k[4] }); }
  const NOTI = [[1200, 800], [1200, 1000], [800, 600], [1000, 1200], [800, 1200]];
  const conv = (ch) => { // catena → millimetri, oppure null se non è una misura
    const mx = Math.max(...ch.v); let v;
    if (ch.u) v = ch.v.map((x) => mm(x, ch.u));
    else if (mx >= 100) v = ch.v.slice(); else if (mx >= 10) v = ch.v.map((x) => x * 10); else if (ch.v.some((x) => x % 1 !== 0)) v = ch.v.map((x) => x * 1000); else return null; // "2x2" è uno schema
    return v.every((x) => x >= 20 && x <= 2500) ? v : null;
  };
  let box = null, palMis = null;
  for (const ch of catene) {
    const v = conv(ch); if (!v) continue;
    if (v.length === 3) { if (!box) box = v; continue; }
    const vicino = kw.some((k) => (ch.s >= k.e && /^[\s\W]*(?:(?:eur|epal|da|di|dimensioni|misura|formato|tipo)\W*)*$/.test(t.slice(k.e, ch.s))) || (k.s >= ch.e && /^[\s\W]*$/.test(t.slice(ch.e, k.s))));
    const noto = NOTI.some(([a, b]) => v[0] === a && v[1] === b);
    if ((vicino || noto || (v[0] >= 700 && v[1] >= 700)) && !palMis) palMis = [Math.max(v[0], v[1]), Math.min(v[0], v[1])];
    else if (!box && !(vicino || noto)) box = v;
  }
  if (palMis) { const k = Object.keys(PALLET).find((x) => PALLET[x].PL === palMis[0] && PALLET[x].PW === palMis[1]); c.pal = k || "x"; c.palMis = palMis; }
  if (box) { c.L = box[0]; c.W = box[1]; if (box.length === 3) c.H = box[2]; }
  if (c.altezza && c.H == null) c.H = c.altezza;
  return { processo, campi: c };
}

// ---------------------------------------------------------------- valori tipici (= caso di riferimento)
const RIF_PALLET = { tipo: "scatole", L: 600, W: 400, H: 300, mass: 18, pal: "eur", strati: 4, robot: "ur30" };
const RIF_CNC = { d: 50, Lp: 120, mat: "acciaio", rate: 40 };

function completaPallet(c) {
  const e = {}, mancanti = [], letti = [];
  const pick = (k, nomeCampo, def) => { if (c[k] != null) { e[k] = true; return c[k]; } return def; };
  const L = pick("L", "dimensioni", RIF_PALLET.L), W = pick("W", "dimensioni", RIF_PALLET.W);
  const H = pick("H", "altezza", RIF_PALLET.H);
  const dimOk = c.L != null && c.H != null;
  if (dimOk) letti.push("dimensioni"); else mancanti.push(c.L != null ? "altezza" : "dimensioni");
  const mass = pick("mass", "massa", RIF_PALLET.mass); (c.mass != null ? letti : mancanti).push("massa");
  const palK = c.pal || "eur"; (c.pal ? letti : mancanti).push("pallet");
  const pal = c.pal === "x" ? { nome: "personalizzato", PL: c.palMis[0], PW: c.palMis[1], txt: c.palMis[0] + "×" + c.palMis[1] } : PALLET[palK];
  if (c.strati != null) letti.push("strati"); else mancanti.push("strati");
  const robot = c.robot || RIF_PALLET.robot; (c.robot ? letti : mancanti).push("robot");
  if (c.rate != null) letti.push("cadenza");
  const tipo = c.tipo || "scatole";
  return { campi: { tipo, L: Math.max(L, W), W: Math.min(L, W), H, mass, pal, palK, strati: c.strati ?? null, robot, rate: c.rate ?? null }, esplicito: { dim: dimOk, mass: c.mass != null, pal: !!c.pal, strati: c.strati != null, robot: !!c.robot, tipo: !!c.tipo }, mancanti, letti };
}
function completaCnc(c) {
  const mancanti = [], letti = [];
  (c.d != null ? letti : mancanti).push("diametro"); (c.Lp != null ? letti : mancanti).push("lunghezza");
  (c.mat ? letti : mancanti).push("materiale"); (c.rate != null ? letti : mancanti).push("cadenza");
  const d = c.d ?? RIF_CNC.d, Lp = c.Lp ?? RIF_CNC.Lp, mat = c.mat || RIF_CNC.mat, rate = c.rate ?? RIF_CNC.rate;
  return { campi: { d, Lp, mat, rate, massa: c.d == null ? c.mass ?? null : null }, esplicito: { d: c.d != null, L: c.Lp != null, mat: !!c.mat, rate: c.rate != null, massa: c.d == null && c.mass != null }, mancanti, letti };
}

// ---------------------------------------------------------------- pallettizzazione: schema, pinza, payload, tempi
const posizioni = (P) => { // tutte le posizioni del pallet pieno: [x, y, quota faccia superiore, strato]
  const out = [];
  for (let l = 0; l < P.strati; l++) for (const [x, y] of P.schema) out.push([x, y, 0.147 + P.Hm * (l + 1), l]);
  return out;
};
function basePallet(c) {
  const Lm = c.L / 1000, Wm = c.W / 1000, H = c.H / 1000, PL = c.pal.PL, PW = c.pal.PW;
  const A = [Math.floor(PL / c.L), Math.floor(PW / c.W)], B = [Math.floor(PL / c.W), Math.floor(PW / c.L)];
  const rot = B[0] * B[1] > A[0] * A[1];
  const [nx, ny] = rot ? B : A, perStrato = nx * ny;
  const bx = rot ? Wm : Lm, by = rot ? Lm : Wm, pX = bx + 0.003, pY = by + 0.003;
  const schema = []; // ordine di posa: dalla fila lontana alla vicina, dal lato lontano dalla rulliera
  for (let j = ny - 1; j >= 0; j--) for (let i = nx - 1; i >= 0; i--) schema.push([(i - (nx - 1) / 2) * pX + PX, PY + (j - (ny - 1) / 2) * pY]);
  const strMax = Math.floor((ALT_MAX - ALT_PAL) / c.H);
  const strati = c.strati ?? (strMax >= 4 ? 4 : Math.max(strMax, 1));
  const rob = ROBOT[c.robot];
  const P = { ...c, Lm, Wm, Hm: H, rot, nx, ny, perStrato, schema, strMax, strati, nTot: perStrato * strati, rob, pickZ: CTOP + H, stopY: Math.min(0, 0.3 - Wm / 2) };
  const pos = posizioni(P);
  let d = 0; for (const [x, y, z] of pos) d += Math.hypot(x - CX, y - P.stopY, z - P.pickZ);
  P.dAvg = pos.length ? d / pos.length : 0;
  P.fRaw = 3 + 2.8 * P.dAvg * (1 + 0.03 * c.mass) + 6 * Math.sqrt(Lm * Wm); // + manovra: collo più largo = più lento
  return P;
}
let _fRif = 0;
export function modelloPallet(c) {
  const P = basePallet(c);
  if (!_fRif) _fRif = basePallet({ ...completaPallet(RIF_PALLET).campi, strati: 4 }).fRaw;
  P.palTxt = c.pal.txt; P.palEtichetta = /^mezzo/.test(c.pal.txt) ? c.pal.txt : "pallet " + c.pal.txt;
  P.payload = c.mass + 2; P.pct = Math.round((100 * P.payload) / P.rob.pay);
  const sic4 = (4 * CUP_N) / (c.mass * G);
  P.coppe = sic4 >= 2 ? 4 : (6 * CUP_N) / (c.mass * G) >= 2 ? 6 : 8;
  P.forza = P.coppe * CUP_N; P.sicurezza = P.forza / (c.mass * G);
  P.altezza = ALT_PAL + P.strati * c.H; P.carico = P.perStrato * P.strati * c.mass;
  P.ciclo = Math.max(4, (12.6 * P.fRaw) / _fRif); P.cadenza = 3600 / P.ciclo;
  // portata: posizione "sopra" di ogni deposito, a partire dalla base del robot (z 0,4 m)
  const pos = posizioni(P), fuori = new Set(); let ok = 0;
  for (const [x, y, z, l] of pos) { if (Math.hypot(x, y, z + 0.147 - ZBASE) <= P.rob.reach) ok++; else fuori.add(l + 1); }
  P.raggiunte = ok; P.strRev = [...fuori].sort((a, b) => a - b);
  P.mostrate = Math.min(12, P.perStrato * Math.min(P.strati, 2)); P.strMostrati = Math.ceil(P.mostrate / P.perStrato);
  P.fuori = null;
  if (P.perStrato < 1) P.fuori = "La scatola è più grande del pallet: oltre la portata di un cobot standard.";
  else if (P.strMax < 1) P.fuori = "La scatola è troppo alta per un pallet da 1,8 m: oltre la portata di un cobot standard.";
  else if (P.payload > P.rob.pay) P.fuori = `${n1(c.mass)} kg (${n1(P.payload)} con la pinza): oltre la portata di un cobot, ${P.rob.pay} kg dell'${P.rob.n}.`;
  return P;
}
const n1 = (v) => num(v, Math.abs(v - Math.round(v)) > 0.05 ? 1 : 0);
const rangeTxt = (a) => { // [3,4] → "strati 3–4"
  const r = []; let i = 0;
  while (i < a.length) { let j = i; while (j + 1 < a.length && a[j + 1] === a[j] + 1) j++; r.push(j > i ? a[i] + "–" + a[j] : String(a[i])); i = j + 1; }
  return (a.length > 1 ? "strati " : "strato ") + r.join(", ");
};
const kgTxt = (v) => n1(v) + " kg";

function schedaPallet(P, r) {
  const [sg, pl] = NOMI[P.tipo], e = r.esplicito, S = (k) => (e[k] ? "testo" : "tipico");
  const spec = [
    ["processo", "pallettizzazione", "regole"],
    ["pezzo", `${sg} ${P.L}×${P.W}×${P.H} mm`, e.dim ? "testo" : "tipico"],
    ["massa", kgTxt(P.mass), S("mass")],
    ["pallet", P.palTxt, S("pal")],
    ["strati", `${P.strati} · schema ${P.nx}×${P.ny}${P.rot ? " ruotato" : ""} · ${P.perStrato} per strato`, S("strati")],
    ["robot", P.rob.n, S("robot")],
    ["pinza", `ventosa ${P.coppe} coppe Ø56`, "calcolo"],
    ["alimentazione", "rulliera, 0,35 m/s", "calcolo"],
    ["payload", `${n1(P.payload)} kg su ${P.rob.pay} kg (${P.pct}%)`, "calcolo"],
  ];
  if (P.rate) spec.push(["cadenza richiesta", `${Math.round(P.rate)} ${pl}/ora`, "testo"]);
  spec.push(["animazione", `${P.mostrate} ${pl} su ${P.nTot} · ${P.strMostrati > 1 ? "strati 1–2" : "strato 1"}`, "calcolo"]);
  const ver = [];
  ver.push([P.sicurezza >= 2 ? "ok" : "warn", "tenuta ventosa", `${Math.round(P.forza)} N · sicurezza ${num(P.sicurezza, 1)}`]);
  ver.push([P.pct <= 90 ? "ok" : "warn", "payload robot", `${n1(P.payload)} kg su ${P.rob.pay} kg`]);
  ver.push([P.carico <= CARICO_MAX ? "ok" : "warn", "carico pallet", `${Math.round(P.carico)} kg su ${CARICO_MAX} kg`]);
  ver.push([P.altezza <= ALT_MAX ? "ok" : "warn", "altezza pallet", `${num(P.altezza / 1000, 2)} m su ${num(ALT_MAX / 1000, 1)} m`]);
  ver.push(["ok", "tempo ciclo", `≈ ${num(P.ciclo, 1)} s / ${sg} (stima)`]);
  const cad = [P.rate && P.cadenza < P.rate ? "warn" : "ok", "cadenza", P.rate && P.cadenza < P.rate ? `${Math.round(P.cadenza)}/ora contro ${Math.round(P.rate)} richieste` : `${num(P.cadenza / 60, 1)} ${pl}/min · ${Math.round(P.cadenza)}/ora`];
  ver.push(cad);
  ver.push(P.strRev.length ? ["warn", "raggiungibilità", `${P.raggiunte}/${P.nTot} posizioni: ${rangeTxt(P.strRev)} da rivedere`] : ["ok", "raggiungibilità", `${P.raggiunte}/${P.nTot} posizioni`]);
  return { spec, ver };
}

// programma URScript dai parametri veri (stessa struttura del programma registrato: presa() / deposito())
export function scriptPallet(P) {
  const f = (v, d = 4) => v.toFixed(d).replace(/^-0\.0+$/, (s) => s.slice(1)); // niente "-0.0000"
  const ori = (rot) => (rot ? "2.2214, -2.2214, 0.0000" : "0.0000, -3.1416, -0.0000");
  const pose = (x, y, z, rot) => `p[${f(x)}, ${f(y)}, ${f(z)}, ${ori(rot)}]`;
  const [sg] = NOMI[P.tipo];
  const base = P.pickZ - ZBASE;
  const L = [
    "def gemello_pallettizzazione():",
    `  # generato da gemello: ${P.rob.n} + ventosa ${P.coppe} coppe D56 (generica), pallet ${P.palTxt},`,
    `  # ${sg} ${P.L}x${P.W}x${P.H} mm ${P.mass.toFixed(1)} kg, ${P.perStrato} per strato x ${P.strati} strati (schema ${P.nx}x${P.ny}${P.rot ? ", scatole ruotate" : ""})`,
    "  # parametri letti dalla frase e completati con valori tipici: verificare su URSim prima del reale",
    "  set_tcp(p[0, 0, 0.130, 0, 0, 0])",
    "  set_payload(2.00)",
    "  def presa():",
    "    while not get_standard_digital_in(0):",
    "      sync()",
    "    end",
    `    movej(${pose(CX, P.stopY, base + 0.198, false)}, a=1.2, v=1.0)`,
    `    movel(${pose(CX, P.stopY, base, false)}, a=0.8, v=0.25)`,
    "    set_standard_digital_out(0, True)",
    "    sleep(0.35)",
    `    set_payload(${(P.mass + 2).toFixed(2)})`,
    `    movel(${pose(CX, P.stopY, base + 0.198, false)}, a=0.8, v=0.35)`,
    "  end",
    "  def deposito(sopra, posa):",
    "    movej(sopra, a=1.0, v=0.8)",
    "    movel(posa, a=0.5, v=0.15)",
    "    set_standard_digital_out(0, False)",
    "    sleep(0.25)",
    "    set_payload(2.00)",
    "    movel(sopra, a=0.8, v=0.35)",
    "  end",
  ];
  if (P.nTot <= 48) {
    let k = 0;
    for (let l = 0; l < P.strati; l++) for (const [x, y] of P.schema) {
      const z = 0.147 + P.Hm * (l + 1) - ZBASE;
      L.push(`  # ${sg} ${++k}`, "  presa()", `  deposito(${pose(x, y, z + 0.147, P.rot)}, ${pose(x, y, z, P.rot)})`);
    }
  } else { // pallet grande: si scrive uno strato e lo si ripete in quota
    L.push("  def strato(q):");
    let k = 0;
    for (const [x, y] of P.schema) {
      const z = 0.147 + P.Hm - ZBASE, q = "p[0, 0, q, 0, 0, 0]";
      L.push(`    # ${sg} ${++k} dello strato`, "    presa()", `    deposito(pose_add(${pose(x, y, z + 0.147, P.rot)}, ${q}), pose_add(${pose(x, y, z, P.rot)}, ${q}))`);
    }
    L.push("  end");
    for (let l = 0; l < P.strati; l++) L.push(`  strato(${f(l * P.Hm)})   # strato ${l + 1} di ${P.strati}`);
  }
  L.push('  textmsg("pallet completo")', "end", "gemello_pallettizzazione()");
  return L.join("\n");
}

// parametri per la cella 3D
export function parCellaPallet(P) {
  const slots = [];
  for (let k = 0; k < P.mostrate; k++) { const l = Math.floor(k / P.perStrato), [x, y] = P.schema[k % P.perStrato]; slots.push([x, y, l]); }
  return { tipo: P.tipo, L: P.Lm, W: P.Wm, H: P.Hm, mass: P.mass, palL: P.pal.PL / 1000, palW: P.pal.PW / 1000, palTxt: P.palEtichetta, rot: P.rot, coppe: P.coppe, robot: P.rob.n, slots, stopY: P.stopY, sicuro: true };
}

// ---------------------------------------------------------------- asservimento CNC
export function modelloCnc(c) {
  const r = c.d / 2000, Lm = c.Lp / 1000;
  const massa = c.massa != null ? c.massa : Math.PI * r * r * Lm * RHO[c.mat];
  const payload = massa * 2 + 0.9, ciclo = 32, T = 3600 / c.rate;
  const forza = Math.min(235, Math.max(20, Math.round((55 * massa) / 1.85 / 5) * 5));
  const M = { ...c, massa, payload, ciclo, T, forza, pct: Math.round((100 * payload) / 12.5), pinzaOk: c.d <= 85, cadOk: T >= ciclo, fuori: null };
  if (massa + 0.9 > 12.5) M.fuori = `${n1(massa)} kg a pezzo (${n1(massa + 0.9)} kg con la pinza): oltre la portata di un cobot, 12,5 kg dell'UR10e.`;
  else if (c.d > 200 || c.Lp > 600) M.fuori = "Pezzo troppo grande per la pinza di un cobot standard.";
  return M;
}
function schedaCnc(M, r) {
  const e = r.esplicito, S = (k) => (e[k] ? "testo" : "tipico"), art = `grezzo tondo Ø${num(M.d, M.d % 1 ? 1 : 0)}×${num(M.Lp, M.Lp % 1 ? 1 : 0)} ${M.mat}`;
  const spec = [
    ["processo", "asservimento_cnc", "regole"],
    ["pezzo", art, e.d && e.L ? "testo" : "tipico"],
    ["materiale", M.mat, S("mat")],
    ["massa", `${num(M.massa, 2)} kg`, e.massa ? "testo" : "calcolo"],
    ["cadenza", `${num(M.rate, M.rate % 1 ? 1 : 0)} pezzi/ora`, S("rate")],
    ["robot", "UR10e (portata 12,5 kg)", "calcolo"],
    ["pinza", `Robotiq 2F-85 · corsa 85 mm · ${M.forza} N`, "calcolo"],
    ["cella", "m_ur10e_cnc · porta + morsa", "calcolo"],
    ["alimentazione", "vassoio, pezzi orientati", "calcolo"],
  ];
  const ver = [
    M.pinzaOk ? ["ok", "pinza", `Ø${num(M.d, M.d % 1 ? 1 : 0)} su corsa 85 mm`] : ["warn", "pinza", `Ø${num(M.d, 0)} su corsa 85 mm: serve una pinza più grande`],
    [M.payload <= 12.5 ? "ok" : "warn", "payload", `${n1(M.payload)} kg su 12,5 kg${M.payload <= 12.5 ? "" : " (con margine ×2)"}`],
    M.cadOk ? ["ok", "tempo ciclo", `≈ ${M.ciclo} s · margine su ${Math.round(M.T)} s`] : ["warn", "tempo ciclo", `≈ ${M.ciclo} s contro ${Math.round(M.T)} s richiesti: serve una pinza doppia`],
  ];
  return { spec, ver };
}

// ---------------------------------------------------------------- scenari costruiti dal testo
const livelli = (r, extra) => [
  { st: "ok", costo: 0, sec: 0.02, nota: `letto dal testo: ${r.letti.length ? r.letti.join(", ") : "solo il processo"}${r.mancanti.length ? " · valori tipici per: " + r.mancanti.join(", ") : ""}${extra || ""}`, esito: "capito a sole regole · 0 $" },
  { st: "no", costo: 0, sec: 0, nota: "non serve", esito: "non serve" },
  { st: "no", costo: 0, sec: 0, nota: "non serve", esito: "non serve" },
];
const capito = (r) => `${r.letti.length} dati dal testo${r.mancanti.length ? ", tipici: " + r.mancanti.join(", ") : ""}`;
const FONTE = "stime di calcolo dalla spec, non simulate";

// Restituisce { processo, rif, fuori, motivo, scen, par, capito }; processo null = frase non riconosciuta.
export function costruisci(testo) {
  const base = interpreta(testo);
  if (!base.processo) return { processo: null, fuori: true, motivo: "Questo compito non è tra quelli che sappiamo leggere a regole.", testo };
  if (base.processo === "pallet") {
    const r = { ...completaPallet(base.campi) }, P = modelloPallet(r.campi);
    const rif = r.mancanti.length === 0 && !r.campi.rate && r.campi.tipo === "scatole" && P.L === 600 && P.W === 400 && P.H === 300 && P.mass === 18 && r.campi.palK === "eur" && P.strati === 4 && r.campi.robot === "ur30";
    if (rif) return { processo: "pallet", rif: true, scen: SCENARI.pallet, capito: "", testo };
    if (P.fuori) return { processo: "pallet", fuori: true, motivo: P.fuori, testo, spec: schedaPallet(P, r).spec.filter((x) => x[0] !== "animazione"), scen: { id: "pallet", livelli: livelli(r), letti: r.letti, mancanti: r.mancanti } };
    const { spec, ver } = schedaPallet(P, r), [, pl] = NOMI[P.tipo];
    const scen = {
      id: "pallet", dinamico: true, stima: true, testo, allegati: [], livelli: livelli(r), spec,
      cella: `${P.rob.n} · ventosa ${P.coppe} coppe · ${P.palEtichetta}`, pezzi: P.mostrate, unita: `${pl} · ${P.strMostrati > 1 ? "strati 1–2" : "strato 1"}`,
      cicloReale: P.ciclo, cicloTxt: `${num(P.ciclo, 1)} s / ${NOMI[P.tipo][0]} · stima`, file: "pallettizzazione.script", script: scriptPallet(P),
      codiceNota: `URScript dai tuoi parametri · in animazione ${P.mostrate} ${pl} su ${P.nTot} del pallet${P.rob.n !== "UR30" ? " · 3D mostrato con UR30" : ""}`,
      clip: null, verifica: ver, fonteVerifica: FONTE, nomeRobot: P.rob.n,
    };
    return { processo: "pallet", scen, par: parCellaPallet(P), capito: capito(r), testo };
  }
  const r = completaCnc(base.campi), M = modelloCnc(r.campi);
  const rif = r.mancanti.length === 0 && M.d === 50 && M.Lp === 120 && M.mat === "acciaio" && M.rate === 40;
  if (rif) return { processo: "cnc", rif: true, scen: SCENARI.cnc, capito: "", testo };
  if (M.fuori) return { processo: "cnc", fuori: true, motivo: M.fuori, testo, spec: schedaCnc(M, r).spec, scen: { id: "cnc", livelli: livelli(r), letti: r.letti, mancanti: r.mancanti } };
  const { spec, ver } = schedaCnc(M, r);
  ver.push(["warn", "non simulato", "asportazione di truciolo"]);
  const scen = {
    id: "cnc", dinamico: true, stima: true, testo, allegati: [], livelli: livelli(r), spec,
    cella: "UR10e · Robotiq 2F-85 · CNC con porta automatica", pezzi: 8, unita: "pezzi lavorati",
    cicloReale: M.ciclo, cicloTxt: `≈ ${M.ciclo} s / pezzo (stima)`, file: "asservimento_cnc.script", script: null,
    codiceNota: "URScript ricostruito dai tuoi parametri e dai punti della cella", clip: null, verifica: ver, fonteVerifica: FONTE,
  };
  return { processo: "cnc", scen, par: { d: M.d, Lp: M.Lp, mat: M.mat, massa: M.massa, rate: M.rate, forza: M.forza, ok: M.pinzaOk }, capito: capito(r), testo };
}
