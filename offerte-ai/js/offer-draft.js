/**

 * Generazione preventivo formale da chat — robot + accessori + testo + immagini.

 */

(function (global) {

  'use strict';



  const RFQ_RE = /preventivo|offert|quot|intestat|termocamera|sensori|perlustrazione|sorveglianza|setup|accessori|umidit|gas|fumo|payload|consegna|noleggio|poc|integrazione|quanto cost|configurazione robot/i;



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

      if (/go2.*edu|orin nx|orin nano|go2 edu plus|edu\+/i.test(t)) return 'go2-edu-rfq';

      if (/sorveglianza|perlustrazione|termocamera|sensori|umidit|gas|fumo|incendio|area confinat|payload/i.test(t)) {

        return 'sorveglianza-as2';

      }

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



    _pocTierId(text) {

      const t = String(text || '').toLowerCase();

      if (/avanzat|deployment|produzione|multi.?robot|compless|full stack|scada|integrazione it/i.test(t)) {

        return 'EXTRA-POC-ADVANCED';

      }

      if (/semplice|solo sdk|driver base|ros base|universit/i.test(t)) {

        return 'EXTRA-POC-LIGHT';

      }

      return 'EXTRA-POC-STANDARD';

    },



    _addPocTier(offer, text) {

      this._addExtra(offer, this._pocTierId(text));

    },



    _buildSorveglianza(offer, userText, shipQuad) {

      offer.intro =
        'Gentile Cliente,\n\n' +
        'in riferimento alla Sua richiesta per **sorveglianza e perlustrazione** in area con possibile umidità, ' +
        'Le sottoponiamo un **confronto tra tre piattaforme Unitree** — specifiche da documentazione ufficiale unitree.com.\n\n' +
        '**Nota importante:** Unitree **As2** e Unitree **A2** sono prodotti distinti. As2 è la gamma compatta (~18 kg, IP54). ' +
        'A2 Standard e A2 Pro sono la linea industriale intermedia (~37 kg, payload fino a 25 kg in marcia) già a catalogo Abra.\n\n' +
        'Nella tabella: **tre alternative robot** (selezionarne una) più accessori, **integrazione PoC** e spedizione.';



      this._section(offer, 'Confronto piattaforme proposte',

        'Opzione A — Unitree As2 Pro: compatta, IP54, dual camera, payload ~15 kg in marcia. Consigliata per perlustrazione agile.\n\n' +

        'Opzione B — Unitree A2 Standard: industriale IP56, payload 25 kg in marcia, autonomia >5 h.\n\n' +

        'Opzione C — Unitree A2 Pro: IP67, dual LiDAR industriale, ideale per ambienti umidi/ostili e payload elevato.');



      this._addSku(offer, 'AS2-PRO', 1, { opzione_robot: true, principale: true });

      this._addSku(offer, 'A2-STD', 1, { opzione_robot: true, alternativa: true });

      this._addSku(offer, 'A2-PRO', 1, { opzione_robot: true, alternativa: true });



      this._productHighlight(offer, 'AS2-PRO');

      this._productHighlight(offer, 'A2-STD');

      this._productHighlight(offer, 'A2-PRO');



      this._section(offer, 'Specifiche Unitree As2 Pro (fonte unitree.com/As2)',

        '• Peso con batteria: ~18 kg · 12 DoF\n' +

        '• Payload marcia: ~15 kg · statico: ~65 kg\n' +

        '• Protezione: IP54\n' +

        '• LiDAR ultra-wide-angle · camera frontale e posteriore\n' +

        '• Autonomia: >4 h · batteria 648 Wh');



      this._section(offer, 'Specifiche Unitree A2 / A2 Pro (fonte unitree.com)',

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

        '',

        'Specifiche tecniche robot: fonte ufficiale Unitree (unitree.com). Abra Robotics è distributore in Italia.',

        'Robot in tabella: alternative non cumulabili — selezionare una configurazione.',

        'Integrazione / PoC: fascia da € 15.000 a € 50.000 in base a complessità (vedi listino Abra).',

        'Voci "Su richiesta": importo da confermare dopo definizione payload e sensori.',

        'Validità offerta: ' + (offer.validita_giorni || 30) + ' giorni.',

      ].join('\n');



      if (scenario === 'go2-edu-rfq') {

        offer.intro =

          'Gentile Cliente,\n\n' +

          'in riferimento alla Sua richiesta di preventivo formale per Unitree Go2 EDU, ' +

          'Le sottoponiamo il confronto tra configurazione Standard (Orin Nano) e Smart/EDU+ (Orin NX) ' +

          'con eventuali accessori e servizi di integrazione.\n\n' +

          'Specifiche robot secondo documentazione ufficiale Unitree.';



        this._addSku(offer, 'GO2-EDU-STD');

        this._addSku(offer, 'GO2-EDU-SMART');

        this._productHighlight(offer, 'GO2-EDU-STD');

        this._productHighlight(offer, 'GO2-EDU-SMART');

        this._section(offer, 'Cosa include il prezzo robot (Go2 EDU — fonte Unitree)',

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

      } else if (scenario === 'sorveglianza-as2' || scenario === 'as2-standard') {

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

      if (/formazione|training|on-site/i.test(t)) add('EXTRA-FORMAZIONE');

      if (/dock|ricarica|charging/i.test(t)) add('EXTRA-DOCK-CHARGE');

      if (scenarioNeedsDefaultExtras(t) || /integrazione|poc|ros|sdk|software/i.test(t)) {

        add(this._pocTierId(text));

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
      if (skus.some(s => /^GO2-EDU/i.test(s))) {
        msg = 'Ho preparato un preventivo formale Go2 EDU con confronto configurazioni Standard (Orin Nano) e Smart/EDU+ (Orin NX).\n\n';
      } else if (robots.length > 1) {
        msg = 'Ho preparato un preventivo formale con ' + robots.length + ' alternative robot (sceglierne una) più accessori e PoC.\n\n';
      } else {
        msg = 'Ho preparato un preventivo formale con le voci richieste.\n\n';
      }

      if (t.opzioni?.length > 1) {

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

