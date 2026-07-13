/**
 * Orchestratore RAG + quote + LLM opzionale (con prompt-guard).
 */
(function (global) {
  'use strict';

  class RAGChat {
    constructor(opts = {}) {
      this.kb = new global.AbraKBSearch();
      this.quote = new global.AbraQuoteEngine();
      this.history = [];
      this.opts = {
        indexUrl: opts.indexUrl || 'data/knowledge-index.json',
        pricesUrl: opts.pricesUrl || '../listini/pubblico/end-user.json',
        rulesUrl: opts.rulesUrl || 'data/offerte-regole.json',
        onStatus: opts.onStatus || (() => {}),
      };
      this.ready = false;
    }

    async init() {
      this.opts.onStatus('Caricamento knowledge base…');
      try {
        await this.kb.load(this.opts.indexUrl);
      } catch {
        await this.kb.load('data/knowledge-index.json');
      }
      this.opts.onStatus('Caricamento listini…');
      try {
        await this.quote.load(this.opts.pricesUrl, this.opts.rulesUrl);
      } catch {
        await this.quote.load('data/sample-prices.json', this.opts.rulesUrl);
      }
      if (global.AbraOfferDraft) {
        await global.AbraOfferDraft.init(this.quote);
      }
      this.ready = true;
      this.opts.onStatus('Pronto');
    }

    async _wantsFormalOffer(userText) {
      if (global.AbraOfferDraft?.isFormalRfq(userText)) return true;
      return global.AbraLLM?.classifyRfqIntent?.(userText) || false;
    }

    _normalizeQuery(text) {
      return String(text || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    }

    _expandSearchQuery(text) {
      const lower = this._normalizeQuery(text);
      const parts = [text];
      if (/poc|proof|prova\s+concept|pilota/.test(lower) && /umanoid|g1|h1|r1|tessile|manifattur|industri/.test(lower)) {
        parts.push('PoC umanoidi industriale integrazione step listino');
      }
      if (/assistenz|riparaz|garanzia|manutenz|supporto\s+post/.test(lower)) {
        parts.push('assistenza riparazione garanzia costi tempi step');
      }
      if (/tessile|tessuti|textile/.test(lower)) {
        parts.push('PoC manifattura ispezione pick-place');
      }
      if (/pick.?place|scatole|piantana|gantry|punto\s*[ab]|r1-d|g1-d/.test(lower)) {
        parts.push('PoC manifattura pick-place dual-arm piantana certificazione');
      }
      return parts.join(' ');
    }

    _tryConsultingReply(userText, ragResults) {
      const lower = this._normalizeQuery(userText);
      const isPickPlace = /pick.?place|scatole|punto\s*[ab]|piantana|gantry|manifattur.*poc/.test(lower)
        && /g1|r1|h2|umanoid|dual|biped|piantana|mobile|fiss/.test(lower);
      const isPoc = (/poc|proof|prova\s+concept|pilota|struttur/.test(lower)
        && /umanoid|g1|robot|tessile|manifattur|industri/.test(lower)) || isPickPlace;
      const isSupport = /assistenz|riparaz|garanzia|manutenz|quanto\s+costa.*(assist|ripar)|quanto\s+dura/.test(lower);

      const hit = (re) => (ragResults || []).find(r => re.test(r.title + ' ' + r.text));
      const pocHit = hit(/poc|umanoidi industri|5 step|pick.?place|piantana|dual-arm/i);
      const supHit = hit(/assistenza|riparazione|garanzia/i);

      if (isPickPlace && pocHit) {
        return (
          '**PoC pick-place manifattura — come scegliere la piattaforma**\n\n' +
          '| Priorità | Scelta tipica |\n' +
          '|----------|---------------|\n' +
          '| Certificazione / cella fissa | **R1-D o G1-D su piantana fissa** |\n' +
          '| Layout che cambia | **R1-D / G1-D mobile** o rail |\n' +
          '| Budget PoC contenuto | **G1-U2** mono-arm |\n' +
          '| Demo / mobilità | **G1 bipede** o **H2** (fase 2, non primo PoC prod) |\n\n' +
          '**Step Abra:** brief → scelta architettura → PoC lab (~€ 10.560) → pilot cella (~€ 19.360) → report.\n\n' +
          'Per **preventivo formale** con R1-D + G1-U2 a confronto: scrivi «preventivo PoC pick-place manifattura».\n\n' +
          '_Dettagli peso scatole, distanza A→B e vincoli safety in call._'
        );
      }

      if (isPoc && pocHit) {
        return (
          '**PoC umanoidi in azienda — percorso Abra (5 step)**\n\n' +
          '1. **Call scoperta** — task, layout, KPI\n' +
          '2. **Scelta piattaforma** — es. G1-U1 (lab) o G1-U2 (manipolazione)\n' +
          '3. **PoC in laboratorio Abra** — integrazione ROS/SDK\n' +
          '4. **Pilot on-site** (opz.) — test in reparto + formazione\n' +
          '5. **Report + preventivo fase 2**\n\n' +
          '**Integrazione PoC (solo servizi, IVA escl.):** base **€ 10.560** · standard **€ 19.360** · avanzata **€ 30.800** ' +
          '(€ 110/h · 8 h/giorno). Robot e sensori **a listino separato**.\n\n' +
          'Per **tessile/manifattura**: use case tipici ispezione qualità, pick-place leggero, telepresenza — da definire in call. ' +
          'Durata indicativa PoC completo: **8–14 settimane**.\n\n' +
          '_Vuoi un preventivo formale? Descrivi reparto e task prioritario, oppure apri **Crea offerta**._'
        );
      }

      if (isSupport && supHit) {
        return (
          '**Assistenza e riparazione Abra**\n\n' +
          '**Step:** contatto → diagnosi remota → preventivo → intervento (lab o on-site) → collaudo.\n\n' +
          '**Costi indicativi (IVA escl.):**\n' +
          '• Ingegneria / diagnosi / riparazione: **€ 110/ora**\n' +
          '• Giornata tecnico on-site: **€ 880** (8 h)\n' +
          '• Formazione operatore: **€ 890**/giornata\n' +
          '• Ricambi Unitree: **a preventivo**\n\n' +
          '**Tempi indicativi:** diagnosi remota 1–3 gg lavorativi · ricambi 2–6 sett se import · riparazione 3–10 gg dopo pezzi.\n\n' +
          '**Garanzia:** 12 mesi produttore Unitree (salvo condizioni modello). Danni da urto/uso improprio esclusi.\n\n' +
          '_Per aprire ticket: WhatsApp o info@abrarobotics.com con modello, serial e foto del problema._'
        );
      }
      return null;
    }

    _offlineReply(query, ragResults, autoQuote) {
      const parts = [];

      if (autoQuote && autoQuote.lines?.length) {
        parts.push(this.quote.formatQuote(autoQuote));
        parts.push('\n→ Apri "Crea offerta" (offerta.html) per personalizzare voci, cliente ed export PDF.');
      } else if (ragResults.length) {
        parts.push('Ecco cosa ho trovato nella knowledge base:\n');
        ragResults.slice(0, 3).forEach(r => {
          parts.push(`**${r.title}**\n${global.AbraPromptGuard.sanitizeKbText(r.text)}`);
        });
      } else {
        parts.push(
          'Non ho trovato informazioni precise. Prova con uno SKU (es. G1-U1, GO2-EDU) o chiedi tempi di consegna / finanziamenti.\n\n' +
          'Per una risposta rapida: **WhatsApp** (pulsante in basso nella chat) oppure info@abrarobotics.com'
        );
      }

      const cfg = global.AbraLLM.loadConfig();
      if (cfg.mode === 'offline') {
        parts.push('\n\n_Risposta da knowledge base Abra. Per assistenza diretta usa WhatsApp o il modulo contatto._');
      }

      return parts.join('\n\n');
    }

    async ask(userText) {
      if (!this.ready) throw new Error('Assistente non inizializzato');

      const guard = global.AbraPromptGuard.analyzeInput(userText);
      const searchQuery = this._expandSearchQuery(guard.cleanQuery || userText);
      const ragResults = global.AbraPromptGuard.filterKbResults(this.kb.search(searchQuery, 8));
      const autoQuote = this.quote.tryAutoQuote(searchQuery) || this.quote.tryAutoQuote(userText);
      let quoteBlock = autoQuote?.lines?.length ? this.quote.formatQuote(autoQuote) : '';

      this.history.push({ role: 'user', content: guard.sanitized });

      let offerDraft = null;
      const wantsOffer = await this._wantsFormalOffer(userText);
      if (wantsOffer && global.AbraOfferDraft) {
        try {
          this.opts.onStatus('Preparazione preventivo…');
          offerDraft = global.AbraOfferDraft.build(userText, this.quote);
          if (offerDraft) {
            global.AbraOfferDraft.saveSession(offerDraft);
            quoteBlock += (quoteBlock ? '\n\n' : '') +
              '=== PREVENTIVO FORMALE GENERATO (usa questi dati, non inventare prezzi) ===\n' +
              global.AbraOfferDraft.formatChatIntro(offerDraft);
          }
        } catch (e) {
          quoteBlock += `\n\n(Errore generazione preventivo: ${e.message})`;
        }
      }

      let reply = null;
      const cfg = global.AbraLLM.loadConfig();
      const deliveryInfo = this.quote._tryDeliveryInfo?.(userText);
      const consultingReply = this._tryConsultingReply(userText, ragResults);

      if (guard.flags.severe) {
        reply = global.AbraPromptGuard.hardRefusal(guard.flags, quoteBlock);
      } else if (guard.flags.priceClaim && quoteBlock) {
        reply = global.AbraPromptGuard.hardRefusal({ leak: true }, quoteBlock);
      } else if (autoQuote?.ranked) {
        reply = this.quote.formatQuote(autoQuote);
      } else if (consultingReply) {
        reply = consultingReply;
        if (quoteBlock) reply += '\n\n' + quoteBlock;
      } else if (deliveryInfo) {
        reply = deliveryInfo;
        if (quoteBlock) reply += '\n\n' + quoteBlock;
      } else if (cfg.mode !== 'offline') {
        try {
          this.opts.onStatus('Generazione risposta AI…');
          reply = await global.AbraLLM.generateReply(
            guard.cleanQuery,
            ragResults,
            quoteBlock,
            this.history,
            guard.flags
          );
        } catch (e) {
          reply = this._offlineReply(searchQuery, ragResults, autoQuote);
          reply += `\n\n_(AI non disponibile: ${e.message}. Risposta da KB offline.)_`;
        }
      }

      if (!reply) reply = this._offlineReply(searchQuery, ragResults, autoQuote);

      reply = global.AbraPromptGuard.validateOutput(reply, quoteBlock, guard.flags);

      if (offerDraft) {
        const intro = global.AbraOfferDraft.formatChatIntro(offerDraft);
        if (!/preventivo formale|totale.*configurazione|totale quotato/i.test(reply)) {
          reply = reply.trim() + '\n\n' + intro;
        }
      }

      this.history.push({ role: 'assistant', content: reply });
      this.opts.onStatus('Pronto');
      return { reply, sources: ragResults, quote: autoQuote, offerDraft };
    }

    clearHistory() {
      this.history = [];
    }
  }

  global.AbraRAGChat = RAGChat;
})(typeof window !== 'undefined' ? window : globalThis);
