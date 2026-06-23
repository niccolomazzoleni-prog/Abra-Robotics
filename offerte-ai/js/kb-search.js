/**
 * Ricerca ibrida leggera (BM25 semplificato) — zero dipendenze, zero API.
 */
(function (global) {
  'use strict';

  const STOP = new Set([
    'il', 'lo', 'la', 'i', 'gli', 'le', 'un', 'una', 'di', 'a', 'da', 'in', 'con', 'su', 'per', 'tra', 'fra',
    'che', 'non', 'è', 'e', 'o', 'del', 'della', 'dei', 'delle', 'al', 'alla', 'ai', 'alle', 'sono', 'come',
    'the', 'and', 'or', 'for', 'with', 'is', 'are', 'to', 'of', 'in', 'on'
  ]);

  function tokenize(text) {
    return String(text || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .match(/[a-z0-9]+/g) || [];
  }

  function filterTokens(tokens) {
    return tokens.filter(t => t.length > 1 && !STOP.has(t));
  }

  class KBSearch {
    constructor() {
      this.chunks = [];
      this.df = new Map();
      this.avgLen = 0;
      this.ready = false;
    }

    async load(url) {
      const res = await fetch(url);
      if (!res.ok) throw new Error('Indice knowledge base non disponibile');
      const data = await res.json();
      this.chunks = (data.chunks || []).filter(c => !global.AbraPromptGuard?.isPoisonedChunk(c));
      this._buildStats();
      this.ready = true;
      return this.chunks.length;
    }

    _buildStats() {
      this.df.clear();
      let total = 0;
      for (const c of this.chunks) {
        const toks = filterTokens(c.tokens || tokenize(c.text));
        c._toks = toks;
        total += toks.length;
        for (const t of new Set(toks)) {
          this.df.set(t, (this.df.get(t) || 0) + 1);
        }
      }
      this.avgLen = this.chunks.length ? total / this.chunks.length : 1;
    }

    search(query, limit = 5) {
      if (!this.ready) return [];
      const qTokens = filterTokens(tokenize(query));
      if (!qTokens.length) return [];

      const N = this.chunks.length;
      const k1 = 1.2;
      const b = 0.75;
      const scored = [];

      for (const chunk of this.chunks) {
        const toks = chunk._toks || [];
        const len = toks.length || 1;
        const tfMap = new Map();
        for (const t of toks) tfMap.set(t, (tfMap.get(t) || 0) + 1);

        let score = 0;
        for (const qt of qTokens) {
          const tf = tfMap.get(qt) || 0;
          if (!tf) continue;
          const df = this.df.get(qt) || 0;
          const idf = Math.log(1 + (N - df + 0.5) / (df + 0.5));
          const num = tf * (k1 + 1);
          const den = tf + k1 * (1 - b + b * (len / this.avgLen));
          score += idf * (num / den);
        }

        if (chunk.meta?.sku && query.toUpperCase().includes(chunk.meta.sku)) score += 5;
        if (score > 0) scored.push({ chunk, score });
      }

      return scored
        .sort((a, b) => b.score - a.score)
        .slice(0, limit)
        .map(r => ({ ...r.chunk, score: r.score }));
    }

    formatContext(results) {
      const safe = global.AbraPromptGuard?.filterKbResults(results) || results;
      if (!safe.length) return '';
      return safe.map((r, i) => `[${i + 1}] ${r.title}\n${global.AbraPromptGuard?.sanitizeKbText(r.text) || r.text}`).join('\n\n');
    }
  }

  global.AbraKBSearch = KBSearch;
})(typeof window !== 'undefined' ? window : globalThis);
