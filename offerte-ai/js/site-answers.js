/**
 * Risposte istantanee del widget chat sul sito (zero backend, zero LLM).
 *
 * Fonte prezzi: listini/pubblico/end-user.json (SKU -> nome, prezzo_eur, slug, categoria,
 * prezzo_da, prezzo_listino_eur). Nessun prezzo viene inventato: se un prodotto non è nel
 * listino, la risposta rimanda a WhatsApp / call / modulo contatto.
 *
 * I link sono relativi alla root del sito (es. "prodotti/unitree-g1.html"): la UI li risolve.
 */
(function (global) {
  'use strict';

  const WA_NUMBER = '393408592926';
  const WA_DISPLAY = '+39 340 859 2926';
  const EMAIL = 'info@abrarobotics.com';
  const BOOKING_URL = 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ22FrpPdyPVRihi4eXPQlljTcG2toa8XF2d8W-QX-L9cKMaXqozq_YsHym56LEdTs9WsnqlTHeF';
  const DELIVERY = '4–6 settimane';
  const LISTINO_URL = 'listino-unitree.html';
  const UMANOIDI_URL = 'umanoidi.html';
  const QUADRUPEDI_URL = 'quadrupedi.html';

  /* ---------- formattazione ---------- */

  /** 23997.41 -> "23.997,41 €" · 45000 -> "45.000 €" (niente ",00" sui prezzi tondi). */
  function formatEuro(n) {
    const cents = Math.round(Math.abs(Number(n) || 0) * 100);
    const int = Math.floor(cents / 100);
    const dec = cents % 100;
    const intStr = String(int).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return (Number(n) < 0 ? '-' : '') + intStr + (dec ? ',' + String(dec).padStart(2, '0') : '') + ' €';
  }

  function waUrl(text) {
    // encodeURIComponent non codifica le parentesi, che romperebbero i link markdown
    return 'https://wa.me/' + WA_NUMBER + '?text=' +
      encodeURIComponent(text || 'Ciao Abra Robotics, vorrei informazioni').replace(/\(/g, '%28').replace(/\)/g, '%29');
  }

  function mdLink(label, href) {
    return '[' + String(label).replace(/[[\]]/g, '') + '](' + href + ')';
  }

  function productUrl(item) {
    return item && item.slug ? 'prodotti/' + item.slug : LISTINO_URL;
  }

  function cleanName(nome) {
    return String(nome || '').replace(/\s+/g, ' ').trim();
  }

  /* ---------- normalizzazione testo ---------- */

  const CANON = {
    batteria: 'battery', batterie: 'battery',
    caricatore: 'charger', caricabatterie: 'charger', caricabatteria: 'charger', caricatori: 'charger',
    telecomando: 'remote', telecomandi: 'remote', controller: 'remote', radiocomando: 'remote',
    mano: 'hand', mani: 'hand', hands: 'hand',
    pinza: 'gripper', pinze: 'gripper',
    braccio: 'arm', bracci: 'arm', arms: 'arm',
    telaio: 'frame', protezione: 'protection',
    telecamera: 'camera', videocamera: 'camera',
    tattile: 'tactile', tattili: 'tactile', tactil: 'tactile',
    std: 'standard', ult: 'ultimate', prof: 'professional', ultra: 'ultimate',
    ruote: 'wheel', ruota: 'wheel', wheels: 'wheel',
  };

  // parole che non identificano mai un prodotto
  const STOP = new Set((
    'il lo la i gli le un una uno di da in con su per tra fra e ed o od del della dello dei delle degli al alla allo ai alle agli ' +
    'dal dalla dai dalle nel nella nei nelle sul sulla che chi non come cosa quale quali quanto quanta quanti quante ' +
    'costa costano costo costi prezzo prezzi prezzario listino euro eur iva esclusa escluso inclusa incluso ' +
    'mi ci vi si ti me te lei voi noi io tu e è ha hanno ho sono sei siamo vorrei voglio posso potete volevo sapere info informazioni ' +
    'dimmi dammi mostra mostrami vedere avere comprare acquistare ordinare ciao buongiorno salve grazie per favore ' +
    'the and or for with of a an to is are how much price prices cost what which ' +
    'single singolo singola versione version package pacchetto unitree robot robotico modello modelli configurazione configurazioni ' +
    'kit set nuovo nuova tutti tutte tutto'
  ).split(/\s+/));

  const MERGE_LETTERS = new Set(['a', 'd', 'w', 'x']);          // H2-A, H2-D, G1-D, R1-A, Go2-W, AS2-X…
  const VARIANT_WORDS = new Set(['standard', 'smart', 'ultimate', 'professional', 'edu', 'plus', 'pro', 'flagship']);

  function normalize(s) {
    return String(s || '')
      .toLowerCase()
      .normalize('NFD').replace(/[̀-ͯ]/g, '')
      .replace(/\+/g, ' plus ')
      .replace(/\b(go|as|h|g|r|b)\s+([12])(?![0-9])/g, '$1$2');    // "go 2" -> "go2", "h 2" -> "h2"
  }

  /**
   * Tokenizza nome prodotto o domanda.
   * forKey=true  -> chiave prodotto: "H2-D" -> ["h2d"]
   * forKey=false -> domanda: "H2-D" -> ["h2"(consumed), "h2d"]
   */
  function analyze(text, forKey) {
    const raw = normalize(text).split(/[^a-z0-9]+/).filter(Boolean).map(t => CANON[t] || t);
    const out = [];
    for (let i = 0; i < raw.length; i++) {
      const t = raw[i];
      if (/^\d+$/.test(t)) continue;
      if (t.length === 1) {
        const next = raw[i + 1];
        const prev = out[out.length - 1];
        if (next && /\d/.test(next)) continue;                      // "g1 e h2", "go2 a 3000"
        if (prev && /\d/.test(prev.t) && MERGE_LETTERS.has(t)) {
          if (forKey) prev.t += t;
          else { prev.consumed = true; out.push({ t: prev.t + t }); }
          continue;
        }
        if (prev && (VARIANT_WORDS.has(prev.t) || /\d/.test(prev.t))) out.push({ t, letter: true });
        continue;
      }
      if (STOP.has(t)) continue;
      out.push({ t });
    }
    return out;
  }

  /* ---------- famiglie (allineate a umanoidi.html / quadrupedi.html) ---------- */

  const FAMILIES = [
    { id: 'g1d', label: 'Unitree G1-D', kind: 'umanoidi', tokens: ['g1d'], re: /^G1D-(STD|ULT)-[A-Z]$/,
      href: UMANOIDI_URL + '#fam-g1-d', claim: 'dual-arm su piantana (Standard) o base mobile (Ultimate)' },
    { id: 'g1', label: 'Unitree G1', kind: 'umanoidi', tokens: ['g1'],
      re: /^G1-(AIR|U\d+|U4-37DOF|COMP|PRO|E|EDU-(ULT|PROF)-[A-Z]|EDU-BOXING)$/,
      href: UMANOIDI_URL + '#fam-g1', claim: 'bipede compatto per ricerca, didattica ed eventi' },
    { id: 'h2ad', label: 'Unitree H2-A / H2-D', kind: 'umanoidi', tokens: ['h2a', 'h2d'],
      re: /^H2-(A-STD-[A-Z]|D|D-(STD|ULT)-[A-Z])$/, sub: { h2a: /^H2-A-/, h2d: /^H2-D(-|$)/ },
      href: UMANOIDI_URL + '#fam-h2-ad', claim: 'busto H2 dual-arm (H2-A) o su base mobile (H2-D)',
      subClaim: { h2a: 'busto H2 dual-arm per manipolazione', h2d: 'H2 dual-arm su base mobile con colonna di sollevamento' } },
    { id: 'h2', label: 'Unitree H2', kind: 'umanoidi', tokens: ['h2'],
      re: /^H2-(AIR|EDU|EDU-SMART-[A-Z]|PLUS|PLUS-SMART|PLUS-ULT-[A-Z])$/,
      href: UMANOIDI_URL + '#fam-h2', claim: 'umanoide full-size per R&D avanzata' },
    { id: 'r1a', label: 'Unitree R1-A', kind: 'umanoidi', tokens: ['r1a', 'a5', 'a7', 'a5d', 'a7d'],
      re: /^R1-A[57]-/, sub: { a5: /^R1-A5-/, a7: /^R1-A7-/, a5d: /^R1-A5-D-/, a7d: /^R1-A7-D-/ },
      href: UMANOIDI_URL + '#fam-r1-a', claim: 'busto R1 dual-arm per banchi di lavoro e didattica',
      subClaim: { a5: 'busto R1 con braccia A5', a7: 'busto R1 con braccia A7', a5d: 'R1-A5 su chassis mobile', a7d: 'R1-A7 su chassis mobile' } },
    { id: 'r1', label: 'Unitree R1', kind: 'umanoidi', tokens: ['r1'],
      re: /^R1-(AIR|BASIC|U\d|EDU-PROF-[A-Z])$/,
      href: UMANOIDI_URL + '#fam-r1', claim: 'bipede entry-level' },
    { id: 'go2w', label: 'Unitree Go2-W', kind: 'quadrupedi', tokens: ['go2w'],
      re: /^GO2W-(U\d|STD|SCREEN-3IN1|SCREEN-GIMBAL)$/, href: QUADRUPEDI_URL, claim: 'quadrupede su ruote' },
    { id: 'go2', label: 'Unitree Go2', kind: 'quadrupedi', tokens: ['go2'],
      re: /^GO2-(AIR|PRO|EDU-(STD|SMART|LASER|ULT)|X|SCREEN-DC(-3IN1|-GIMBAL)?|GAS)$/,
      href: QUADRUPEDI_URL, claim: 'quadrupede compatto per ricerca, didattica e ispezione' },
    { id: 'as2w', label: 'Unitree As2-W', kind: 'quadrupedi', tokens: ['as2w'],
      re: /^(AS2-W|AS2W-(X|EDU-STD|EDU-SMART|EDU-PLUS|EDU-ULT))$/, href: QUADRUPEDI_URL, claim: 'As2 su ruote' },
    { id: 'as2', label: 'Unitree As2', kind: 'quadrupedi', tokens: ['as2', 'a2s'],
      re: /^AS2-(AIR|EDU|EDU-SMART|EDU-LASER|EDU-ULT|X|PRO)$/, href: QUADRUPEDI_URL, claim: 'quadrupede IP54 per sorveglianza e ispezione' },
    { id: 'a2w', label: 'Unitree A2-W', kind: 'quadrupedi', tokens: ['a2w'],
      re: /^A2W-(STD|PRO)$/, href: QUADRUPEDI_URL, claim: 'A2 su ruote' },
    { id: 'a2', label: 'Unitree A2', kind: 'quadrupedi', tokens: ['a2'],
      re: /^A2-(STD|PRO)$/, href: QUADRUPEDI_URL, claim: 'quadrupede industriale, payload 25 kg' },
    { id: 'b2w', label: 'Unitree B2-W', kind: 'quadrupedi', tokens: ['b2w'],
      re: /^B2W(-LIDAR)?$/, href: QUADRUPEDI_URL, claim: 'B2 su ruote' },
    { id: 'b2', label: 'Unitree B2', kind: 'quadrupedi', tokens: ['b2'],
      re: /^B2(-LIDAR)?$/, href: QUADRUPEDI_URL, claim: 'quadrupede industriale heavy-duty' },
    { id: 'z1', label: 'Braccio Unitree Z1', kind: 'bracci', tokens: ['z1'],
      re: /^ARM-Z1-/, href: LISTINO_URL, claim: 'braccio robotico 6 assi' },
    { id: 'd1', label: 'Braccio Unitree D1', kind: 'bracci', tokens: ['d1', 'd1t'],
      re: /^(D1-ARM|D1T-STD|D1T-FULL)$/, href: LISTINO_URL, claim: 'braccio leggero / Mobile ALOHA' },
  ];

  const ROBOT_CATS = new Set(['UMANOIDI', 'QUADRUPEDI']);
  const FAMILY_TOKENS = new Set([].concat(...FAMILIES.map(f => f.tokens)));

  /* ---------- intent ---------- */

  const RE = {
    price: /prezz|cost[aio]|quant[oi]\b|quanto viene|listino|€|\beuro\b|budget|spesa|pagare|tariff|cifra|economic|\bcaro\b|\bcare\b|price|how much/,
    delivery: /consegn|tempi\b|tempo\b|quando arriv|arriva|disponibil|delivery|lead time|in stock|pronta consegna|settiman/,
    contact: /parla(re)? con|un tecnico|al tecnico|tecnico abra|persona reale|\bumano\b|operatore|consulent|commerciale|chiamat|telefon|whatsapp|contatt|\bcall\b|videocall|appuntament|prenot|richiam|e-?mail|preventivo (su misura|personalizzat)|sentire qualcuno/,
    greet: /^(ciao|salve|buongiorno|buonasera|hey|hello|hi|ehi)\b[\s!.,?]*$/,
    thanks: /^(grazie|ok grazie|perfetto|ottimo|va bene|ok)\b[\s!.,?]*(mille|tante)?[\s!.]*$/,
    humanoidCat: /umanoid|humanoid|bipede|bipedi/,
    quadCat: /quadruped|robot ?cane|cane ?robot|robodog|robot dog|quattro zampe|cagnolin/,
    accessoriesCat: /accessor|ricamb|component|mani\b|pinze|bracci\b|batterie\b/,
    allPrices: /tutti i prezzi|listino completo|listino prezzi|lista prezzi|vedere (il )?listino|dove (trovo|sono|vedo) (i )?prezz|prezzi (dei|di tutti)|catalogo/,
    vat: /\biva\b|dazio|dogan|spedizion|trasporto|spese di spedizione/,
    payment: /pagament|pagare a rate|rate\b|acconto|anticipo|bonifico|carta di credito/,
    warranty: /garanzi|assistenz|riparaz|post.?vendita|manutenz/,
    specs: /specific|scheda|caratterist|dimension|peso|pesa|autonomia|dof|gradi di liberta|sensor|come funziona|cosa fa|velocita|altezza|payload/,
    formalRfq: /preventivo|offerta formale|quotazione|intestat|poc\b|proof of concept|integrazion|sorveglianz|perlustraz|termocamer|payload|pick.?place|noleggi/,
  };

  /* ---------- motore ---------- */

  class SiteAnswers {
    constructor(opts = {}) {
      this.prices = {};
      this.kb = opts.kb || null;
      this.items = [];
      this.vocab = new Set();
      this.robotVocab = new Set();
      this.last = null; // contesto conversazione (ultima famiglia / prodotto)
      this.ready = false;
    }

    async load(pricesUrl) {
      const res = await fetch(pricesUrl);
      if (!res.ok) throw new Error('Listino non disponibile (' + res.status + ')');
      this.setPrices(await res.json());
      return this.items.length;
    }

    setPrices(prices) {
      this.prices = prices || {};
      this.items = Object.keys(this.prices).map(sku => {
        const p = this.prices[sku] || {};
        const codeKey = analyze(sku, true).map(x => x.t);
        const nameKey = analyze(String(p.nome || '').split('(')[0], true).map(x => x.t);
        // "G1-04" -> ["g1"]: un nome ridotto al solo codice famiglia non deve catturare "g1"
        const keys = [codeKey, nameKey].filter(k => k.length &&
          !(k.length === 1 && FAMILY_TOKENS.has(k[0]) && k.join() !== codeKey.join()));
        const union = new Set([].concat(...keys, analyze(p.nome || '', true).map(x => x.t)));
        const family = FAMILIES.find(f => f.re.test(sku)) || null;
        return {
          sku,
          nome: cleanName(p.nome || sku),
          prezzo: Number(p.prezzo_eur),
          prezzoListino: Number(p.prezzo_listino_eur) || 0,
          da: !!p.prezzo_da,
          note: p.note || '',
          slug: p.slug || '',
          categoria: p.categoria || '',
          keys,
          union,
          family,
          isRobot: ROBOT_CATS.has(p.categoria) || !!family,
        };
      }).filter(it => Number.isFinite(it.prezzo) && it.prezzo > 0);

      this.vocab.clear();
      this.robotVocab.clear();
      for (const it of this.items) {
        for (const t of it.union) {
          this.vocab.add(t);
          if (it.isRobot) this.robotVocab.add(t);
        }
      }
      this.ready = true;
    }

    get(sku) { return this.items.find(i => i.sku === sku) || null; }

    familyMembers(fam, filterToken) {
      let list = this.items.filter(it => fam.re.test(it.sku));
      if (filterToken && fam.sub && fam.sub[filterToken]) {
        const sub = fam.sub[filterToken];
        const filtered = list.filter(it => sub.test(it.sku));
        if (filtered.length) list = filtered;
      }
      return list.sort((a, b) => a.prezzo - b.prezzo);
    }

    /** Cerca prodotti / famiglie nel testo. */
    findProducts(text) {
      const toks = analyze(text, false);
      const all = new Set(toks.map(x => x.t));
      const free = new Set(toks.filter(x => !x.consumed).map(x => x.t));

      // 1) match esatti: tutte le parole di una chiave SKU presenti nella domanda
      let exact = [];
      for (const it of this.items) {
        let best = null;
        for (const k of it.keys) {
          if (k.every(t => all.has(t)) && (!best || k.length > best.length)) best = k;
        }
        if (best) exact.push({ it, key: best });
      }
      exact = exact.filter(a => !exact.some(b => b !== a &&
        b.key.length > a.key.length && a.key.every(t => b.key.includes(t))));

      // 2) famiglie citate
      const families = [];
      for (const f of FAMILIES) {
        const tok = f.tokens.find(t => free.has(t));
        if (tok) families.push({ fam: f, token: tok });
      }

      // parole "prodotto" extra (es. "edu", "smart", "lidar") utili per filtrare la famiglia
      const famTokens = FAMILY_TOKENS;
      const extra = [...all].filter(t => this.vocab.has(t) && !famTokens.has(t) && !toks.find(x => x.t === t && x.consumed));
      const accessoryWords = extra.filter(t => !this.robotVocab.has(t));

      // match esatto che coincide col solo codice famiglia (es. "B2", "H2-D") -> vista famiglia
      // oppure SKU "da" legacy fuori famiglia (es. G1D-STANDARD) quando la famiglia ha le configurazioni
      const famCodeOnly = exact.length && families.length && exact.every(e =>
        (e.key.length === 1 && families.some(f => f.fam.tokens.includes(e.key[0]))) || (e.it.da && !e.it.family));

      // "h2 edu smart": H2-EDU combacia ma "smart" resta fuori -> meglio le configurazioni Smart della famiglia
      const narrowTokens = extra.filter(t => !accessoryWords.includes(t));
      const leavesOut = exact.length && families.length && exact.every(e =>
        narrowTokens.some(t => !e.key.includes(t)));
      const narrowedFamily = leavesOut && families.some(({ fam, token }) =>
        this.familyMembers(fam, token).some(m => narrowTokens.every(t => m.union.has(t))));

      if (exact.length && !famCodeOnly && !narrowedFamily) {
        const robotsFirst = exact.map(e => e.it);
        return { mode: 'products', items: dedupe(robotsFirst).slice(0, 8), families };
      }

      if (families.length) {
        if (accessoryWords.length) {
          // "batteria go2", "mano h2"… -> accessori della famiglia
          const need = [...new Set(families.map(f => f.token).concat(accessoryWords))];
          const acc = this.items.filter(it => need.every(t => it.union.has(t) ||
            (famTokens.has(t) && [...it.union].some(u => u.startsWith(t)))));
          if (acc.length) return { mode: 'products', items: acc.sort((a, b) => a.prezzo - b.prezzo).slice(0, 8), families };
        }
        const groups = families.slice(0, 4).map(({ fam, token }) => {
          let members = this.familyMembers(fam, token);
          const filt = extra.filter(t => !accessoryWords.includes(t));
          if (filt.length) {
            const narrowed = members.filter(m => filt.every(t => m.union.has(t)));
            if (narrowed.length) members = narrowed;
          }
          return { fam, token, members, narrowed: filt.length > 0 };
        }).filter(g => g.members.length);
        if (groups.length) return { mode: 'families', groups };
      }

      if (accessoryWords.length || extra.length >= 2) {
        const need = extra;
        const hits = this.items.filter(it => need.every(t => it.union.has(t)));
        if (hits.length && hits.length <= 12) {
          return { mode: 'products', items: hits.sort((a, b) => a.prezzo - b.prezzo).slice(0, 8), families: [] };
        }
      }
      return null;
    }

    /* ---------- blocchi di risposta ---------- */

    priceLine(it, opts = {}) {
      const price = (it.da ? 'da ' : '') + formatEuro(it.prezzo);
      let s = '**' + price + '**';
      if (opts.vat) s += ' IVA esclusa';
      if (it.prezzoListino && it.prezzoListino > it.prezzo + 0.5) {
        s += ' (prezzo di listino ' + formatEuro(it.prezzoListino) + ')';
      }
      return s;
    }

    kbBlurb(sku) {
      const chunks = this.kb && this.kb.chunks;
      if (!chunks) return '';
      const c = chunks.find(ch => ch.id === 'sku:' + sku);
      if (!c || !c.text) return '';
      let t = String(c.text).split(/Prezzo End-User [\d.]+ EUR\.\s*/)[1] || '';
      t = t.split(/\s*Specifiche:/)[0].replace(/\s*IVA esclusa.*$/i, '').trim();
      const m = t.match(/^(.{40,240}?[.!?])(\s|$)/);
      return m ? m[1] : (t.length <= 240 ? t : '');
    }

    footer() {
      return '_Prezzi IVA esclusa, spedizione e dazio inclusi · consegna in ' + DELIVERY + '._';
    }

    ctaLine(subject) {
      return 'Preventivo su misura? ' + mdLink('WhatsApp', waUrl('Ciao Abra Robotics, vorrei un preventivo per ' + (subject || 'un robot Unitree'))) +
        ' · ' + mdLink('Prenota una call', BOOKING_URL);
    }

    answerProducts(items, families) {
      const lines = [];
      if (items.length === 1) {
        const it = items[0];
        lines.push('**' + it.nome + '**');
        lines.push('Prezzo: ' + this.priceLine(it, { vat: true }));
        if (/range|preordine|soggetto a variazioni|conferma su preventivo/i.test(it.note)) {
          lines.push('_' + it.note.replace(/^A partire da\s*—\s*/i, '').replace(/IVA esclusa,?\s*spedizione e dazio inclusi\.?\s*/i, '').trim() + '_');
        }
        const blurb = this.kbBlurb(it.sku);
        if (blurb) lines.push(blurb);
        const links = [mdLink('Scheda prodotto →', productUrl(it))];
        if (it.family) links.push(mdLink('Tutte le configurazioni ' + it.family.label.replace('Unitree ', ''), it.family.href));
        else links.push(mdLink('Listino completo', LISTINO_URL));
        lines.push(links.join(' · '));
        lines.push(this.footer());
        lines.push(this.ctaLine(it.nome));
        this.last = { skus: [it.sku], families: it.family ? [it.family.id] : [] };
      } else {
        lines.push('Ecco i prezzi dal listino ufficiale:');
        items.forEach(it => lines.push('• ' + mdLink(it.nome, productUrl(it)) + ' — ' + this.priceLine(it)));
        const fams = dedupe(items.map(i => i.family).filter(Boolean));
        if (fams.length === 1) lines.push(mdLink('Tutte le configurazioni ' + fams[0].label.replace('Unitree ', '') + ' →', fams[0].href));
        else lines.push(mdLink('Listino completo →', LISTINO_URL));
        lines.push(this.footer());
        lines.push(this.ctaLine());
        this.last = { skus: items.map(i => i.sku), families: fams.map(f => f.id) };
      }
      return lines.join('\n');
    }

    answerFamilies(groups) {
      const lines = [];
      if (groups.length === 1) {
        const { fam, token, members, narrowed } = groups[0];
        const min = members[0];
        let label = fam.label;
        if (fam.sub && fam.sub[token]) label = 'Unitree ' + token.toUpperCase().replace(/^(H2|R1)([AD])/, '$1-$2').replace(/^A([57])D$/, 'R1-A$1-D').replace(/^A([57])$/, 'R1-A$1');
        const count = members.length;
        lines.push('**' + label + '** — ' + ((fam.subClaim && fam.subClaim[token]) || fam.claim) + '.');
        lines.push('Prezzo: **' + (count > 1 || min.da ? 'da ' : '') + formatEuro(min.prezzo) + '** IVA esclusa' +
          (count > 1 ? ' (' + count + ' configurazioni' + (narrowed ? ' corrispondenti' : '') + ')' : '') + '.');
        const show = count <= 6 ? members : members.slice(0, 5);
        show.forEach(it => lines.push('• ' + mdLink(it.nome, productUrl(it)) + ' — ' + this.priceLine(it)));
        lines.push(mdLink(count > show.length ? 'Vedi tutte le ' + count + ' configurazioni →' : 'Pagina famiglia →', fam.href));
        lines.push(this.footer());
        lines.push(this.ctaLine(label));
      } else {
        lines.push('Prezzi di partenza dal listino ufficiale:');
        groups.forEach(({ fam, members }) => {
          const min = members[0];
          lines.push('• ' + mdLink(fam.label, fam.href) + ' — da **' + formatEuro(min.prezzo) + '**' +
            (members.length > 1 ? ' · ' + members.length + ' configurazioni' : ''));
        });
        lines.push(this.footer());
        lines.push('Dimmi il modello esatto (es. «G1 EDU», «H2-D») e ti do prezzo e scheda.');
      }
      this.last = { skus: [], families: groups.map(g => g.fam.id) };
      return lines.join('\n');
    }

    answerCategory(kind) {
      const order = kind === 'umanoidi'
        ? ['g1', 'g1d', 'h2', 'h2ad', 'r1', 'r1a']
        : ['go2', 'go2w', 'as2', 'as2w', 'a2', 'a2w', 'b2', 'b2w'];
      const fams = order.map(id => FAMILIES.find(f => f.id === id)).filter(Boolean);
      const title = kind === 'umanoidi' ? 'Umanoidi Unitree' : 'Quadrupedi Unitree';
      const lines = ['**' + title + ' — prezzi di partenza**'];
      fams.forEach(f => {
        const m = this.familyMembers(f);
        if (!m.length) return;
        lines.push('• ' + mdLink(f.label.replace('Unitree ', ''), f.href) + ' — da **' + formatEuro(m[0].prezzo) + '**' +
          (m.length > 1 ? ' · ' + m.length + ' config.' : '') + ' — ' + f.claim);
      });
      lines.push(mdLink(kind === 'umanoidi' ? 'Tutti gli umanoidi →' : 'Tutti i quadrupedi →', kind === 'umanoidi' ? UMANOIDI_URL : QUADRUPEDI_URL) +
        ' · ' + mdLink('Listino completo', LISTINO_URL));
      lines.push(this.footer());
      lines.push('Scrivimi il modello (es. «' + (kind === 'umanoidi' ? 'G1-U2' : 'Go2 EDU') + '») per il prezzo esatto.');
      this.last = { skus: [], families: fams.map(f => f.id) };
      return lines.join('\n');
    }

    answerAllPrices() {
      return [
        'Tutti i prezzi pubblici sono nel ' + mdLink('listino Unitree 2026', LISTINO_URL) + ' (cerca per modello o SKU).',
        '• ' + mdLink('Umanoidi', UMANOIDI_URL) + ' — G1, G1-D, H2, H2-A/H2-D, R1, R1-A',
        '• ' + mdLink('Quadrupedi', QUADRUPEDI_URL) + ' — Go2, Go2-W, As2, A2, B2',
        this.footer(),
        'Oppure chiedimi direttamente: «quanto costa il G1?», «prezzo H2-D».',
      ].join('\n');
    }

    answerDelivery(found) {
      const lines = [
        '**Consegna in ' + DELIVERY + '** dalla conferma d\'ordine, per umanoidi, quadrupedi e accessori Unitree.',
        'I prezzi di listino includono già **spedizione e dazio** (IVA esclusa). Per configurazioni speciali confermiamo la data in fase d\'ordine.',
      ];
      if (found && found.mode === 'families') {
        const g = found.groups[0];
        lines.push(mdLink(g.fam.label, g.fam.href) + ': da **' + formatEuro(g.members[0].prezzo) + '** IVA esclusa.');
      } else if (found && found.mode === 'products') {
        const it = found.items[0];
        lines.push(mdLink(it.nome, productUrl(it)) + ': ' + this.priceLine(it, { vat: true }) + '.');
      }
      lines.push('Vuoi una data precisa? ' + mdLink('Scrivici su WhatsApp', waUrl('Ciao Abra Robotics, vorrei sapere i tempi di consegna per ')) + '.');
      return lines.join('\n');
    }

    answerContact() {
      return [
        'Ti mettiamo in contatto con un tecnico Abra:',
        '• **WhatsApp** ' + mdLink(WA_DISPLAY, waUrl('Ciao Abra Robotics, vorrei parlare con un tecnico')) + ' — risposta rapida in orario lavorativo',
        '• ' + mdLink('Prenota una call gratuita', BOOKING_URL) + ' — scegli tu giorno e ora',
        '• Email ' + mdLink(EMAIL, 'mailto:' + EMAIL),
        'Preferisci essere richiamato? Lascia i tuoi dati nel modulo qui sotto.',
      ].join('\n');
    }

    answerVat() {
      return [
        'I prezzi del listino pubblico sono **IVA esclusa** e includono **spedizione in Italia e dazio doganale** (salvo diversa indicazione sulla scheda).',
        'L\'IVA (22%) si applica in fattura; per ordini B2B con P.IVA serve la ragione sociale.',
        'Consegna in ' + DELIVERY + '. ' + mdLink('Listino completo →', LISTINO_URL),
      ].join('\n');
    }

    answerPayment() {
      return [
        'Condizioni standard: **50% all\'ordine, 50% prima della spedizione**, salvo accordi diversi.',
        'Molti progetti sono finanziabili (Industria 4.0 / Transizione 5.0, bandi PNRR): facciamo una verifica gratuita.',
        'Per un\'offerta formale: ' + mdLink('WhatsApp', waUrl('Ciao Abra Robotics, vorrei un\'offerta formale per ')) + ' · ' + mdLink('Prenota una call', BOOKING_URL),
      ].join('\n');
    }

    greeting() {
      return [
        'Ciao! Sono l\'assistente di Abra Robotics, supply chain ufficiale Unitree in Italia.',
        'Posso darti subito **prezzi dal listino ufficiale** (es. «quanto costa il G1?», «prezzo H2-D»), tempi di consegna e contatti con un tecnico.',
      ].join('\n');
    }

    /** Estratto KB "pubblico" (FAQ sito, assistenza, cobot/AMR) — mai i prezzi Unitree del KB (possono essere vecchi). */
    kbAnswer(text) {
      if (!this.kb || typeof this.kb.search !== 'function') return null;
      const guard = global.AbraPromptGuard;
      let res = this.kb.search(text, 8);
      if (guard && guard.filterKbResults) res = guard.filterKbResults(res);
      const blocked = /stripe|quiz|sinonimi|regola-fondamentale|cosa-chied|preventivo-formale|domanda-tipica|escalation|varianti-e-sku|prezzi|spedizione|risposta-abra/;
      const allowedSrc = /index\.html|faq-vendita|faq-assistenza|faq-gamma|faq-poc|prodotti-a2|prodotti-as2|faq-sorveglianza|listino-integrazione|amr-products|cobot-products/;
      res = res.filter(r => allowedSrc.test(r.source || '') && !blocked.test(r.id || '') && String(r.text || '').length > 80);
      if (!res.length) return null;
      const top = res[0];
      if ((top.score || 0) < 2.5) return null;
      let body = String(top.text || '');
      if (/Risposta:/.test(body)) body = body.split('Risposta:')[1];
      else body = body.split('\n').slice(1).join('\n') || body;
      body = body.replace(/Prezzo ([\d.]+) EUR\./g, (m, n) => 'Prezzo ' + formatEuro(parseFloat(n)) + ' IVA esclusa.')
        .replace(/\bSKU [\w-]+\.?/g, '')
        .replace(/\(\)\.?/g, '')
        .trim();
      if (body.length > 520) {
        const cut = body.slice(0, 520);
        const lastBreak = Math.max(cut.lastIndexOf('\n'), cut.lastIndexOf('. '));
        body = cut.slice(0, lastBreak > 200 ? lastBreak + 1 : 520).trim() + ' …';
      }
      const title = String(top.title || '').replace(/^\[[^\]]+\]\s*/, '');
      return '**' + title + '**\n' + body + '\n' + 'Vuoi approfondire con un tecnico? ' +
        mdLink('WhatsApp', waUrl('Ciao Abra Robotics, ' + title)) + ' · ' + mdLink('Prenota una call', BOOKING_URL);
    }

    notFound() {
      return [
        'Non ho una risposta precisa a questa domanda, ma un tecnico Abra può aiutarti subito:',
        '• ' + mdLink('WhatsApp ' + WA_DISPLAY, waUrl('Ciao Abra Robotics, ')),
        '• ' + mdLink('Prenota una call gratuita', BOOKING_URL),
        'Per i prezzi prova a scrivere il modello (es. «G1», «Go2 EDU», «H2-D») oppure apri il ' + mdLink('listino completo', LISTINO_URL) + '.',
      ].join('\n');
    }

    /**
     * Risposta deterministica, o null se serve il motore RAG / LLM.
     * @returns {{reply:string, intent:string, actions?:Array}|null}
     */
    answer(text) {
      if (!this.ready) return null;
      const q = String(text || '').trim();
      if (!q) return null;
      const lower = normalize(q);
      const wantsPrice = RE.price.test(lower);

      if (RE.greet.test(lower)) return { intent: 'greeting', reply: this.greeting() };
      if (RE.thanks.test(lower)) {
        return { intent: 'thanks', reply: 'Figurati! Se ti serve altro — prezzi, consegne o un preventivo su misura — sono qui.' };
      }

      const found = this.findProducts(q);
      const words = lower.split(/\s+/).filter(Boolean).length;

      // preventivi strutturati (PoC, sorveglianza…) -> motore offerte esistente
      if (RE.formalRfq.test(lower) && words >= 6 && !/^(prezz|quanto)/.test(lower)) return null;

      if (RE.contact.test(lower) && !(found && wantsPrice)) {
        return { intent: 'contact', reply: this.answerContact(), actions: [{ type: 'contact', label: 'Apri il modulo contatto' }] };
      }
      if (RE.delivery.test(lower) && !/prezz|cost/.test(lower)) {
        return { intent: 'delivery', reply: this.answerDelivery(found) };
      }
      if (RE.vat.test(lower) && !found) return { intent: 'vat', reply: this.answerVat() };
      if (RE.payment.test(lower) && !found) return { intent: 'payment', reply: this.answerPayment() };

      if (found) {
        if (!wantsPrice && RE.warranty.test(lower)) return null; // domanda tecnica: lascia al KB
        const intro = !wantsPrice && RE.specs.test(lower)
          ? 'Specifiche complete, foto e dotazione sono nella scheda di ogni configurazione:\n' : '';
        if (found.mode === 'products') return { intent: 'price', reply: intro + this.answerProducts(found.items, found.families) };
        return { intent: 'price', reply: intro + this.answerFamilies(found.groups) };
      }

      if (RE.allPrices.test(lower)) return { intent: 'price', reply: this.answerAllPrices() };
      if (RE.humanoidCat.test(lower) && (wantsPrice || words <= 4)) return { intent: 'price', reply: this.answerCategory('umanoidi') };
      if (RE.quadCat.test(lower) && (wantsPrice || words <= 4)) return { intent: 'price', reply: this.answerCategory('quadrupedi') };

      // "quanto costa?" dopo aver parlato di un modello (solo se la domanda non nomina altro)
      const content = analyze(q, false);
      if (wantsPrice && this.last && !content.length && words <= 4 && !/robot/.test(lower)) {
        if (this.last.skus.length) {
          const items = this.last.skus.map(s => this.get(s)).filter(Boolean);
          if (items.length) return { intent: 'price', reply: this.answerProducts(items, []) };
        }
        if (this.last.families.length) {
          const groups = this.last.families.map(id => FAMILIES.find(f => f.id === id)).filter(Boolean)
            .map(fam => ({ fam, token: fam.tokens[0], members: this.familyMembers(fam) })).filter(g => g.members.length);
          if (groups.length) return { intent: 'price', reply: this.answerFamilies(groups.slice(0, 4)) };
        }
      }

      if (wantsPrice && !content.length) {
        return { intent: 'price', reply: 'Di quale robot vuoi il prezzo?\n' + this.answerAllPrices() };
      }
      if (RE.accessoriesCat.test(lower) && wantsPrice) {
        return { intent: 'price', reply: 'Mani, pinze, batterie e ricambi sono tutti nel ' + mdLink('listino completo', LISTINO_URL) + ' con prezzo e scheda.\nScrivimi il modello (es. «batteria G1», «mano H2») per il prezzo esatto.\n' + this.footer() };
      }
      return null;
    }
  }

  function dedupe(arr) {
    return arr.filter((x, i) => arr.indexOf(x) === i);
  }

  SiteAnswers.formatEuro = formatEuro;
  SiteAnswers.waUrl = waUrl;
  SiteAnswers.analyze = analyze;
  SiteAnswers.FAMILIES = FAMILIES;
  SiteAnswers.CONTACT = { WA_NUMBER, WA_DISPLAY, EMAIL, BOOKING_URL, DELIVERY };

  global.AbraSiteAnswers = SiteAnswers;
})(typeof window !== 'undefined' ? window : globalThis);
