/**

 * Generazione preventivo formale da chat — robot + accessori + testo + immagini.

 */

(function (global) {

  'use strict';



  const RFQ_RE = /preventivo|offert|quot|intestat|termocamera|sensori|perlustrazione|sorveglianza|setup|accessori|umidit|gas|fumo|payload|consegna|noleggio|poc|integrazione|quanto cost|configurazione robot/i;

  const POC_TARIFFA = { hourly: 110, hoursPerDay: 8 };



  const OfferDraft = {

    builder: null,

    manifest: {},

    blocchi: [],



    async init(quoteEngine) {

      if (this.builder) return;

      this.builder = new global.AbraOfferBuilder(quoteEngine);

      await this.builder.load('data/offerte-config.json', 'data/voci-extra.json');

      try {

        this.manifest = await fetch('../listini/pubblico/catalogo-manifest.json').then(r => r.json());

      } catch {

        this.manifest = {};

      }

      this.builder.setProductManifest(this.manifest);

      try {

        this.blocchi = (await fetch('data/blocchi-ricorrenti.json').then(r => r.json())).blocchi || [];

      } catch {

        this.blocchi = [];

      }

    },



    isFormalRfq(text) {
      return RFQ_RE.test(String(text || '')) || this._localRfqHints(text);
    },

    _localRfqHints(text) {
      const t = String(text || '').toLowerCase();
      return (/quot|offert|preventiv|prezz|configur|quanto cost|budget|proposta|mi serv|abbiamo bisogno|vorrei/i.test(t))
        && (/robot|unitree|quadruped|go2|as2|\ba2\b|g1|sensor|termic|umanoide|poc|integraz|amr|cobot/i.test(t));
    },



    _scenario(text) {

      const t = String(text || '').toLowerCase();

      if (/sorveglianza|perlustrazione|termocamera|sensori|umidit|gas|fumo|incendio|area confinat|payload|as2|\ba2\b/i.test(t)) {

        return 'sorveglianza-combo';

      }

      if (/go2.*edu|orin nx|orin nano|go2 edu plus|edu\+/i.test(t)) return 'go2-edu-rfq';

      if (/as2|as 2/i.test(t)) return 'as2-standard';

      return 'standard';

    },



    _addExtra(offer, id, qty = 1) {

      const v = this.builder.vociExtra.find(x => x.id === id);

      if (!v) return;

      const prezzo = v.su_richiesta || v.prezzo_eur == null ? 0 : v.prezzo_eur;

      this.builder.addCustomLine(offer, v.nome, prezzo, qty, v.descrizione || '', 'extra');

      const line = offer.line_items[offer.line_items.length - 1];

      if (line && (v.su_richiesta || v.prezzo_eur == null)) line.su_richiesta = true;

    },



    _addSku(offer, sku, qty = 1, opts = {}) {

      if (!this.builder.addCatalogLine(offer, sku, qty, opts)) return false;

      const p = this.builder.quote.getPrice(sku);

      const line = offer.line_items.find(l => l.sku === sku);

      if (line && p?.note) {

        line.descrizione = [line.descrizione, p.note].filter(Boolean).join(' · ');

      }

      return true;

    },



    _insertBlock(offer, id) {

      this.builder.insertRecurringBlock(offer, id, this.blocchi);

    },



    _productHighlight(offer, sku) {

      this.builder.addProductSheetBlock(offer, sku, this.manifest);

    },



    _section(offer, title, body) {

      this.builder.addBlock(offer, { type: 'section', title, body });

    },



    _pocDays(text) {

      const t = String(text || '').toLowerCase();

      if (/avanzat|deployment|produzione|multi.?robot|compless|full stack|scada|integrazione it/i.test(t)) return 35;

      if (/semplice|solo sdk|driver base|ros base|universit/i.test(t)) return 12;

      return 22;

    },



    _addPocHourly(offer, text) {

      const days = this._pocDays(text);

      const hours = days * POC_TARIFFA.hoursPerDay;

      const total = hours * POC_TARIFFA.hourly;

      const fmtEur = n => n.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

      this.builder.addCustomLine(

        offer,

        'Integrazione software / PoC — ingegneria e test campo',

        total,

        1,

        `${days} giornate × ${POC_TARIFFA.hoursPerDay} h/giorno × € ${POC_TARIFFA.hourly}/h = € ${fmtEur(total)} (stima post-brief).`,

        'extra'

      );

    },



    _addTrasfertePoc(offer) {

      this.builder.addCustomLine(

        offer,

        'Trasferte team integrazione (trasporto, vitto, alloggio)',

        0,

        1,

        'Da quantificare a parte in base a sede cliente, numero tecnici e pernottamenti.',

        'extra'

      );

      const line = offer.line_items[offer.line_items.length - 1];

      line.su_richiesta = true;

    },



    _buildSorveglianza(offer, userText, shipQuad) {

      offer.intro =
        'Gentile Cliente,\n\n' +
        'in riferimento alla Sua richiesta, Le sottoponiamo un **preventivo unico** con due blocchi:\n\n' +
        '**1) Applicazione sorveglianza / perlustrazione** (area confinata, possibile umidità, sensori custom): ' +
        'consigliamo **Unitree As2 Pro** o la linea **A2 Standard / A2 Pro**. ' +
        'As2 e A2 sono piattaforme distinte.\n\n' +
        '**2) Alternativa Go2 EDU** (se preferite quella piattaforma): confronto **Standard (Orin Nano)** vs **Smart / EDU+ (Orin NX)**.\n\n' +
        'Per ogni blocco robot: **scegliere una sola configurazione**. Accessori, PoC e spedizione sono condivisi.';



      this._section(offer, 'Blocco A — Sorveglianza (As2 / A2)',

        'Piattaforme adatte a payload sensori e ambienti umidi:\n' +
        '• As2 Pro — compatta IP54, dual camera, ~15 kg payload marcia\n' +
        '• A2 Standard — industriale IP56, 25 kg payload marcia\n' +
        '• A2 Pro — IP67, dual LiDAR, outdoor severo');



      this._addSku(offer, 'AS2-PRO', 1, { opzione_robot: true, principale: true, robot_gruppo: 'sorveglianza' });

      this._addSku(offer, 'A2-STD', 1, { opzione_robot: true, robot_gruppo: 'sorveglianza', alternativa: true });

      this._addSku(offer, 'A2-PRO', 1, { opzione_robot: true, robot_gruppo: 'sorveglianza', alternativa: true });



      this._section(offer, 'Blocco B — Alternativa Go2 EDU',

        'Per confronto, se orientati a Go2 EDU per lab/POC software:\n' +
        '• Go2 EDU Standard — Jetson Orin Nano ~40 TOPS\n' +
        '• Go2 EDU Smart / EDU+ — Jetson Orin NX 100 TOPS');



      this._addSku(offer, 'GO2-EDU-STD', 1, { opzione_robot: true, robot_gruppo: 'go2', alternativa: true });

      this._addSku(offer, 'GO2-EDU-SMART', 1, { opzione_robot: true, robot_gruppo: 'go2', alternativa: true });



      this._productHighlight(offer, 'AS2-PRO');

      this._productHighlight(offer, 'A2-STD');

      this._productHighlight(offer, 'A2-PRO');

      this._productHighlight(offer, 'GO2-EDU-STD');

      this._productHighlight(offer, 'GO2-EDU-SMART');



      this._section(offer, 'Specifiche tecniche — Unitree As2 Pro',

        '• Peso con batteria: ~18 kg · 12 DoF\n' +

        '• Payload marcia: ~15 kg · statico: ~65 kg\n' +

        '• Protezione: IP54\n' +

        '• LiDAR ultra-wide-angle · camera frontale e posteriore\n' +

        '• Autonomia: >4 h · batteria 648 Wh');



      this._section(offer, 'Specifiche tecniche — Unitree A2 / A2 Pro',

        'A2 Standard: ~37 kg, payload 25 kg in marcia, IP56, autonomia >5 h.\n' +

        'A2 Pro: stessa base meccanica con IP67 e dual LiDAR industriale per outdoor e ambienti severi.');



      this._addExtrasFromText(offer, userText);

      this._insertBlock(offer, 'consegna-supporto');

      this.builder.addCustomLine(offer, 'Spedizione e imballo — quadrupede (Italia)', shipQuad, 1,

        'Indicativa — conferma su destinazione.', 'extra');

    },



    build(userText, quoteEngine) {

      if (!this.builder) throw new Error('OfferDraft non inizializzato');

      const scenario = this._scenario(userText);

      const offer = this.builder.createEmpty();

      const cfg = this.builder.config || {};

      const shipQuad = quoteEngine.rules?.shipping_defaults_eur?.quadrupede || 1000;



      offer.template_id = scenario === 'go2-edu-rfq' ? 'standard' : 'industria';

      this.builder.applyTemplate(offer, offer.template_id);

      offer.note_iva = 'Prezzi IVA esclusa. Dazio doganale incluso nel robot. Spedizione indicata a parte.';

      offer.applica_iva = false;

      offer.condizioni = [

        cfg.condizioni_default || '',

        'Le configurazioni robot sono alternative non cumulabili: selezionare una piattaforma per ciascun blocco.',

        'Integrazione / PoC: tariffa ingegneria € 110/h, giornata 8 h (stima in offerta). Trasferte a parte.',

        'Voci «Su richiesta»: importo da confermare dopo definizione payload e sensori.',

      ].filter(Boolean).join('\n\n');



      if (scenario === 'go2-edu-rfq') {

        offer.intro =

          'Gentile Cliente,\n\n' +

          'in riferimento alla Sua richiesta di preventivo formale per Unitree Go2 EDU, ' +

          'Le sottoponiamo il confronto tra configurazione Standard (Orin Nano) e Smart/EDU+ (Orin NX) ' +

          'con eventuali accessori e servizi di integrazione.';



        this._addSku(offer, 'GO2-EDU-STD');

        this._addSku(offer, 'GO2-EDU-SMART');

        this._productHighlight(offer, 'GO2-EDU-STD');

        this._productHighlight(offer, 'GO2-EDU-SMART');

        this._section(offer, 'Cosa include il prezzo robot (Go2 EDU)',

          '• Robot quadrupede completo con batteria\n' +

          '• Controller / telecomando\n' +

          '• LiDAR 4D L2 integrato\n' +

          '• SDK Unitree — ROS 2, Python, C++ (versione EDU)\n' +

          '• Dazio doganale incluso nel listino Abra\n\n' +

          'Non incluso: spedizione (voce separata), IVA, sensori custom, docking, formazione extra.');

        if (/termocamera|sensori|lidar|mid-?360|staffa|accessori|integrazione|poc/i.test(userText)) {

          this._addExtrasFromText(offer, userText);

        }

        this.builder.addCustomLine(offer, 'Spedizione e imballo — quadrupede (Italia)', shipQuad, 1,

          'Indicativa — conferma su destinazione.', 'extra');

      } else if (scenario === 'sorveglianza-combo' || scenario === 'sorveglianza-as2' || scenario === 'as2-standard') {

        this._buildSorveglianza(offer, userText, shipQuad);

      } else {

        const q = quoteEngine.tryAutoQuote(userText);

        if (q?.lines) {

          for (const l of q.lines) {

            if (l.sku) this._addSku(offer, l.sku);

          }

        }

      }



      if (!offer.line_items.length) return null;



      this._insertBlock(offer, 'finanziamenti');

      this._insertBlock(offer, 'perche-abra');

      offer.chiusura =

        'Restiamo a disposizione per una call tecnico-commerciale per definire payload, sensori e fascia PoC definitiva. ' +

        'Invieremo copia PDF via e-mail per Vostra documentazione interna.\n\nCordiali saluti,\nAbra Robotics';



      return offer;

    },



    _addExtrasFromText(offer, text) {

      const t = text.toLowerCase();

      const added = new Set();

      const add = (id) => {

        if (added.has(id)) return;

        added.add(id);

        this._addExtra(offer, id);

      };

      if (/termocamera|termica|radiometric/i.test(t)) add('EXTRA-TERMOCAM');

      if (/gas|multi-gas/i.test(t)) add('EXTRA-SENSOR-GAS');

      if (/fumo|incendio|temperatura/i.test(t)) add('EXTRA-SENSOR-FUMO-TEMP');

      if (/mid-?360|lidar aggiuntivo|lidar extra/i.test(t)) add('EXTRA-LIDAR-MID360');

      if (/staffa|mount|payload/i.test(t)) add('EXTRA-PAYLOAD-MOUNT');

      if (/formazione|training operatore|training on/i.test(t)) add('EXTRA-FORMAZIONE');

      if (/dock|ricarica|charging/i.test(t)) add('EXTRA-DOCK-CHARGE');

      if (scenarioNeedsDefaultExtras(t) || /integrazione|poc|ros|sdk|software/i.test(t)) {

        this._addPocHourly(offer, text);

        this._addTrasfertePoc(offer);

      }

      if (scenarioNeedsDefaultExtras(t)) {

        add('EXTRA-TERMOCAM');

        add('EXTRA-SENSOR-GAS');

        add('EXTRA-SENSOR-FUMO-TEMP');

        add('EXTRA-PAYLOAD-MOUNT');

      }

    },



    formatChatIntro(offer) {
      const t = this.builder.recalculate(offer);
      const onRequest = offer.line_items.filter(l => l.su_richiesta || l.prezzo_unit === 0);
      const robots = offer.line_items.filter(l => l.opzione_robot);
      const skus = offer.line_items.map(l => l.sku).filter(Boolean);

      let msg;
      const hasGo2 = skus.some(s => /^GO2-EDU/i.test(s));
      const hasAs2A2 = skus.some(s => /^AS2|^A2/i.test(s));
      if (hasAs2A2 && hasGo2) {
        msg = 'Ho preparato un preventivo **combinato**: blocco sorveglianza (**As2 / A2**) + alternativa **Go2 EDU** (Standard / Smart), sensori e PoC a tariffa oraria.\n\n';
      } else if (hasAs2A2 && robots.length > 1) {
        msg = 'Ho preparato un preventivo sorveglianza con **As2 Pro**, **A2 Standard** e **A2 Pro** (sceglierne una), più sensori e PoC.\n\n';
      } else if (hasGo2) {
        msg = 'Ho preparato un preventivo formale Go2 EDU con confronto configurazioni Standard (Orin Nano) e Smart/EDU+ (Orin NX).\n\n';
      } else if (robots.length > 1) {
        msg = 'Ho preparato un preventivo formale con ' + robots.length + ' alternative robot (sceglierne una) più accessori e PoC.\n\n';
      } else {
        msg = 'Ho preparato un preventivo formale con le voci richieste.\n\n';
      }

      if (t.gruppi?.length > 1) {

        msg += 'Totali per blocco (IVA escl., sensori su richiesta esclusi):\n';

        for (const g of t.gruppi) {

          msg += `\n**${g.label}**\n`;

          for (const o of g.opzioni) {

            msg += '• ' + o.nome.split('(')[0].trim() + ': € ' + o.totale.toLocaleString('it-IT', { minimumFractionDigits: 2 }) + '\n';

          }

        }

      } else if (t.opzioni?.length > 1) {

        msg += 'Totali per configurazione (IVA escl., sensori su richiesta esclusi):\n';

        for (const o of t.opzioni) {

          msg += '• ' + o.nome.split('(')[0].trim() + ': € ' + o.totale.toLocaleString('it-IT', { minimumFractionDigits: 2 }) + '\n';

        }

      } else {

        msg += 'Totale quotato: € ' + t.subtotal.toLocaleString('it-IT', { minimumFractionDigits: 2 }) + ' (IVA escl.)\n';

      }

      if (onRequest.length) {

        msg += '\nVoci da definire in call: ' + onRequest.map(l => l.nome.split('—')[0].trim()).join(', ') + '\n';

      }

      msg += '\nAnteprima sotto — usa Scarica PDF o Apri in Crea offerta per modificare ed esportare.';

      return msg;

    },



    renderPreviewHtml(offer) {

      return this.builder.renderPreviewFragment(offer);

    },



    downloadPdf(offer) {

      if (!this.builder) throw new Error('OfferDraft non inizializzato');

      this.builder.downloadPdf(offer);

    },



    saveSession(offer) {

      sessionStorage.setItem('abra_offer_draft', JSON.stringify(offer));

      sessionStorage.setItem('abra_chat_quote_prefill', JSON.stringify({

        skus: offer.line_items.map(l => l.sku).filter(Boolean),

        margin_key: offer.margin_key || 'end_user',

        full: true,

        ts: Date.now(),

      }));

    },

  };



  function scenarioNeedsDefaultExtras(t) {

    return /sorveglianza|perlustrazione|sensori|termocamera|umidit/i.test(t);

  }



  global.AbraOfferDraft = OfferDraft;

})(typeof window !== 'undefined' ? window : globalThis);

