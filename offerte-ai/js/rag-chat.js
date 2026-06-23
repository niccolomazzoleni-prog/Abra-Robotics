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
          'Per un preventivo personalizzato: info@abrarobotics.com'
        );
      }

      const cfg = global.AbraLLM.loadConfig();
      if (cfg.mode === 'offline') {
        parts.push('\n\n_Modalità offline: ricerca KB + calcolo prezzi. Per risposte AI attiva Ollama (Gemma 4) o Google AI dall\'admin._');
      }

      return parts.join('\n\n');
    }

    async ask(userText) {
      if (!this.ready) throw new Error('Assistente non inizializzato');

      const guard = global.AbraPromptGuard.analyzeInput(userText);
      const searchQuery = guard.cleanQuery || userText;
      const ragResults = global.AbraPromptGuard.filterKbResults(this.kb.search(searchQuery, 5));
      const autoQuote = this.quote.tryAutoQuote(searchQuery) || this.quote.tryAutoQuote(userText);
      const quoteBlock = autoQuote?.lines?.length ? this.quote.formatQuote(autoQuote) : '';

      this.history.push({ role: 'user', content: guard.sanitized });

      let reply = null;
      const cfg = global.AbraLLM.loadConfig();

      if (guard.flags.severe) {
        reply = global.AbraPromptGuard.hardRefusal(guard.flags, quoteBlock);
      } else if (guard.flags.priceClaim && quoteBlock) {
        reply = global.AbraPromptGuard.hardRefusal({ leak: true }, quoteBlock);
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

      let offerDraft = null;
      if (global.AbraOfferDraft?.isFormalRfq(userText)) {
        try {
          offerDraft = global.AbraOfferDraft.build(userText, this.quote);
          if (offerDraft) {
            global.AbraOfferDraft.saveSession(offerDraft);
            reply = global.AbraOfferDraft.formatChatIntro(offerDraft);
          }
        } catch (e) {
          reply += `\n\n_(Errore generazione preventivo: ${e.message})_`;
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
