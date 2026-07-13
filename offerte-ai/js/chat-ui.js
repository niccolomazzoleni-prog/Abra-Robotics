/**
 * UI chat — stile assistant-ui / ChatGPT + feedback inline.
 */
(function (global) {
  'use strict';

  const STORAGE_KEY = 'abra_feedback_log';
  const PENDING_KB_KEY = 'abra_feedback_pending_kb';
  const CHAT_WA_URL = 'https://wa.me/393408592926?text=' + encodeURIComponent('Ciao Abra Robotics, vorrei informazioni su ');
  const CHAT_GAS_URL = () => (typeof window !== 'undefined' && window.GOOGLE_SCRIPT_URL)
    || 'https://script.google.com/macros/s/AKfycbw1WeoJYZltyorwQ-8Nftg0DdiOXOV-Zl3MlRegJS2ybhAzaRaqZNpTRamEbHJe2NtK/exec';

  function uid() {
    return 'fb-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 7);
  }

  function escapeHtml(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function formatBotHtml(text) {
    let html = escapeHtml(text);
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/_(.+?)_/g, '<em>$1</em>');
    html = html.replace(/(€\s?[\d.,]+)/g, '<span class="price-highlight">$1</span>');
    html = html.replace(/\n/g, '<br>');
    return html;
  }

  const FeedbackStore = {
    all() {
      try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); }
      catch { return []; }
    },
    save(entry) {
      const log = this.all();
      log.push(entry);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(log.slice(-500)));
      return entry;
    },
    update(id, patch) {
      const log = this.all().map(e => e.id === id ? { ...e, ...patch, updated_at: new Date().toISOString() } : e);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(log));
    },
    exportJsonl() {
      const log = this.all();
      if (!log.length) return '';
      return log.map(e => JSON.stringify(e)).join('\n');
    },
    exportFinetuneJsonl() {
      return this.all()
        .filter(e => e.correction || e.rating === 1)
        .map(e => JSON.stringify({
          messages: [
            { role: 'system', content: global.AbraLLM?.SYSTEM_PROMPT || 'Assistente Abra Robotics' },
            { role: 'user', content: e.question },
            { role: 'assistant', content: e.correction || e.answer },
          ],
          meta: { feedback_id: e.id, rating: e.rating },
        }))
        .join('\n');
    },
    download(filename, content, mime) {
      const blob = new Blob([content], { type: mime || 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = filename;
      a.click();
    },
    queueForKb(entry) {
      const q = JSON.parse(localStorage.getItem(PENDING_KB_KEY) || '[]');
      const meta = entry.scenario_meta || {};
      q.push({
        title: entry.question.slice(0, 120),
        question: entry.question,
        body: entry.correction || entry.answer,
        feedback_id: entry.id,
        action: entry.action || 'feedback',
        family: meta.family || entry.family || '',
        industry: entry.industry || meta.industry || '',
        scenario_id: meta.scenarioId || (meta.seed ? 'seed' : ''),
        created_at: new Date().toISOString(),
      });
      localStorage.setItem(PENDING_KB_KEY, JSON.stringify(q));
    },
    pendingKb() { return JSON.parse(localStorage.getItem(PENDING_KB_KEY) || '[]'); },
    clearPendingKb() {
      localStorage.setItem(PENDING_KB_KEY, '[]');
    },
    exportPendingKbJsonl() {
      const items = this.pendingKb();
      if (!items.length) return '';
      return items.map(it => JSON.stringify({
        id: it.feedback_id || uid(),
        timestamp: it.created_at || new Date().toISOString(),
        question: it.question || it.title,
        correction: it.body,
        action: it.action || 'expert_quiz',
        model_mode: 'expert-quiz',
        rating: 1,
        scenario_meta: {
          family: it.family,
          industry: it.industry,
          scenarioId: it.scenario_id,
        },
        industry: it.industry,
      })).join('\n');
    },
    exportPendingKbMarkdown() {
      const items = this.pendingKb();
      if (!items.length) return '';
      let md = '# Feedback — knowledge (export Lab)\n\n';
      md += '_Import: `python scripts/merge_feedback_to_kb.py feedback-export.jsonl`_\n\n';
      for (const it of items) {
        const fam = it.family ? `[${it.family}] ` : '';
        md += `## ${fam}${it.title}\n\n`;
        if (it.industry) md += `**Contesto settore:** ${it.industry}\n\n`;
        md += `**Domanda cliente:** ${it.question || it.title}\n\n`;
        md += `**Risposta consulente Abra:**\n\n${it.body}\n\n`;
      }
      return md;
    },
    exportTrainingPack() {
      return {
        feedback: this.exportJsonl(),
        finetune: this.exportFinetuneJsonl(),
        kbMd: this.exportPendingKbMarkdown(),
        kbJsonl: this.exportPendingKbJsonl(),
      };
    },
  };

  function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
  }

  function tokenizeForStream(text) {
    return String(text || '').match(/\S+\s*|\n/g) || [text];
  }

  class ChatUI {
    constructor(container, opts = {}) {
      this.container = typeof container === 'string' ? document.querySelector(container) : container;
      this.opts = {
        title: opts.title || 'Assistente Abra',
        subtitle: opts.subtitle || 'Listini & offerte',
        avatarLetter: opts.avatarLetter || 'A',
        variant: opts.variant || 'compact',
        theme: opts.theme || 'default',
        showFeedback: opts.showFeedback !== false,
        feedbackMode: opts.feedbackMode || 'compact',
        onSend: opts.onSend || (async () => ''),
        onFeedback: opts.onFeedback || (() => {}),
        suggestions: opts.suggestions || [],
        showContact: opts.showContact !== false,
      };
      this._typingEl = null;
      this._renderShell();
      this._bind();
    }

    _renderShell() {
      this.container.classList.add('abra-chat-app');
      if (this.opts.variant === 'thread') this.container.classList.add('abra-chat-thread');
      if (this.opts.theme === 'platinum') this.container.classList.add('abra-chat-platinum');
      this.container.innerHTML = `
        <header class="chat-app-header">
          <div class="chat-avatar">${escapeHtml(this.opts.avatarLetter)}</div>
          <div class="chat-app-title">
            <strong>${escapeHtml(this.opts.title)}</strong>
            <span class="chat-app-sub">${escapeHtml(this.opts.subtitle)}</span>
          </div>
          <span class="chat-app-status online" id="chat-app-status" title="Online"></span>
        </header>
        <div class="chat-empty" id="chat-empty">
          <div class="chat-empty-icon">💬</div>
          <p>Chiedi prezzi, bundle o tempi di consegna</p>
        </div>
        <div class="chat-app-messages" id="chat-app-messages" role="log" aria-live="polite"></div>
        <footer class="chat-app-compose-wrap">
          <form class="chat-app-compose" id="chat-app-form">
            <div class="compose-inner">
              <textarea id="chat-app-input" rows="1" placeholder="Scrivi la tua domanda…" autocomplete="off"></textarea>
              <button type="submit" id="chat-app-send" aria-label="Invia">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M3.4 20.4l17.45-7.48c.81-.35.81-1.49 0-1.84L3.4 3.6c-.66-.29-1.39.2-1.39.91L2 9.12c0 .5.37.93.87.99L15 12 2.87 13.89c-.5.07-.87.5-.87 1l.01 4.61c0 .71.73 1.2 1.39.91z"/></svg>
              </button>
            </div>
            <p class="compose-hint" id="chat-compose-hint">Invio per inviare · Shift+Invio a capo</p>
          </form>
          ${this.opts.showContact ? `
          <div class="chat-compose-footer">
            <a class="chat-footer-link" href="${CHAT_WA_URL}" target="_blank" rel="noopener noreferrer">WhatsApp</a>
            <button type="button" class="chat-footer-link chat-contact-toggle" id="chat-contact-toggle">Modulo contatto</button>
          </div>
          <div class="chat-contact-panel hidden" id="chat-contact-panel">
            <form class="chat-contact-form" id="chat-contact-form">
              <input type="text" name="_gotcha" class="chat-contact-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
              <label class="chat-contact-field"><span>Nome *</span><input name="nome" required autocomplete="name"></label>
              <label class="chat-contact-field"><span>Email *</span><input name="email" type="email" required autocomplete="email"></label>
              <label class="chat-contact-field"><span>Telefono</span><input name="telefono" type="tel" autocomplete="tel"></label>
              <label class="chat-contact-field"><span>Messaggio</span><textarea name="messaggio" rows="2" placeholder="Di cosa hai bisogno?"></textarea></label>
              <button type="submit" class="chat-contact-submit">Invia</button>
            </form>
          </div>` : ''}
          ${this.opts.suggestions.length ? `
          <details class="chat-suggestions-fold">
            <summary>Esempi di domanda</summary>
            <div class="chat-app-chips chat-app-chips-thread" id="chat-app-chips"></div>
          </details>` : ''}
        </footer>`;

      this.messagesEl = this.container.querySelector('#chat-app-messages');
      this.emptyEl = this.container.querySelector('#chat-empty');
      this.inputEl = this.container.querySelector('#chat-app-input');
      this.statusEl = this.container.querySelector('#chat-app-status');
      this.sendBtn = this.container.querySelector('#chat-app-send');

      if (this.opts.showContact) this._bindContact();

      const chips = this.container.querySelector('#chat-app-chips');
      if (chips && this.opts.suggestions.length) {
        chips.innerHTML = this.opts.suggestions.map(s =>
          `<button type="button" class="chat-chip" data-q="${escapeHtml(s)}">${escapeHtml(s)}</button>`
        ).join('');
      }
    }

    _bind() {
      this.container.querySelector('#chat-app-form').addEventListener('submit', e => this._handleSend(e));
      this.container.querySelector('#chat-app-chips')?.addEventListener('click', e => {
        const btn = e.target.closest('.chat-chip');
        if (!btn) return;
        this.inputEl.value = btn.dataset.q;
        this.container.querySelector('#chat-app-form').requestSubmit();
      });
      this.inputEl.addEventListener('keydown', e => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this.container.querySelector('#chat-app-form').requestSubmit(); }
      });
      this.inputEl.addEventListener('input', () => {
        this.inputEl.style.height = 'auto';
        this.inputEl.style.height = Math.min(this.inputEl.scrollHeight, 140) + 'px';
      });
    }

    _bindContact() {
      const toggle = this.container.querySelector('#chat-contact-toggle');
      const panel = this.container.querySelector('#chat-contact-panel');
      const form = this.container.querySelector('#chat-contact-form');
      if (!toggle || !panel || !form) return;

      toggle.addEventListener('click', () => {
        panel.classList.toggle('hidden');
        toggle.setAttribute('aria-expanded', panel.classList.contains('hidden') ? 'false' : 'true');
        if (!panel.classList.contains('hidden')) {
          form.querySelector('[name="nome"]')?.focus();
          this.scrollBottom();
        }
      });

      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const hp = form.querySelector('[name="_gotcha"]');
        if (hp?.value.trim()) return;

        const nome = form.querySelector('[name="nome"]')?.value.trim();
        const email = form.querySelector('[name="email"]')?.value.trim();
        if (!nome || !email) {
          form.reportValidity();
          return;
        }

        const btn = form.querySelector('.chat-contact-submit');
        const orig = btn.textContent;
        btn.disabled = true;
        btn.textContent = 'Invio…';

        const payload = {
          nome,
          email,
          telefono: form.querySelector('[name="telefono"]')?.value.trim() || '',
          messaggio: form.querySelector('[name="messaggio"]')?.value.trim() || '',
          origine: 'Chat Abra',
          pagina: document.title,
          url: location.href,
          timestamp: new Date().toISOString(),
        };

        try {
          await fetch(CHAT_GAS_URL(), {
            method: 'POST',
            mode: 'no-cors',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
          });
          if (window.fbq) window.fbq('track', 'Lead');
          form.reset();
          panel.classList.add('hidden');
          toggle.setAttribute('aria-expanded', 'false');
          this.appendBot('**Grazie!** Abbiamo ricevuto la tua richiesta. Un consulente Abra ti ricontatta entro **2 ore lavorative**. Puoi anche scriverci su WhatsApp.', {});
          global.AbraUI?.toast?.('Richiesta inviata', 'ok');
        } catch {
          this.appendBot('Invio non riuscito. Scrivi a **info@abrarobotics.com** o usa **WhatsApp**.', {});
        } finally {
          btn.disabled = false;
          btn.textContent = orig;
        }
      });
    }

    _hideEmpty() {
      if (this.emptyEl) this.emptyEl.style.display = 'none';
    }

    setStatus(text, online = true) {
      if (!this.statusEl) return;
      this.statusEl.title = text;
      this.statusEl.className = 'chat-app-status ' + (online ? 'online' : 'busy');
    }

    appendUser(text) {
      this._hideEmpty();
      return this._appendRow('user', text, {});
    }

    async appendBotStreamed(text, meta = {}, opts = {}) {
      const minWait = opts.minWaitMs ?? 900;
      const wordDelay = opts.wordDelayMs ?? 32;
      await sleep(minWait);
      this.hideTyping();
      this._hideEmpty();
      const row = this._appendRow('bot', '', meta);
      const bubble = row.querySelector('.chat-bubble.bot');
      bubble.classList.add('streaming');
      const tokens = tokenizeForStream(text);
      let acc = '';
      for (const tok of tokens) {
        acc += tok;
        bubble.textContent = acc;
        this.scrollBottom();
        await sleep(wordDelay + Math.floor(Math.random() * 18));
      }
      bubble.innerHTML = formatBotHtml(text);
      bubble.classList.remove('streaming');
      if (meta.sources?.length) this._attachSources(row, meta.sources);
      if (meta.quote?.lines?.length && !meta.offerDraft) this._attachQuoteCard(row, meta.quote);
      if (meta.offerDraft) this._attachOfferPreview(row, meta.offerDraft);
      if (this.opts.showFeedback && meta.feedbackId) this._attachFeedback(row, meta);
      return row;
    }

    appendBot(text, meta = {}) {
      this._hideEmpty();
      const row = this._appendRow('bot', text, meta);
      if (meta.sources?.length) this._attachSources(row, meta.sources);
      if (meta.quote?.lines?.length && !meta.offerDraft) this._attachQuoteCard(row, meta.quote);
      if (meta.offerDraft) this._attachOfferPreview(row, meta.offerDraft);
      if (this.opts.showFeedback && meta.feedbackId) this._attachFeedback(row, meta);
      return row;
    }

    _attachSources(row, sources) {
      const pills = document.createElement('div');
      pills.className = 'source-pills';
      sources.slice(0, 4).forEach(s => {
        const p = document.createElement('span');
        p.className = 'source-pill';
        p.textContent = s.title?.slice(0, 36) || s.id;
        p.title = s.text || s.title;
        pills.appendChild(p);
      });
      row.querySelector('.chat-bubble-wrap').appendChild(pills);
    }

    _attachOfferPreview(row, offer) {
      if (!global.AbraOfferDraft?.renderPreviewHtml) return;
      const wrap = document.createElement('div');
      wrap.className = 'chat-offer-preview';
      const t = global.AbraOfferDraft.builder?.recalculate(offer) || { subtotal: 0, opzioni: [] };
      const mainTotal = t.opzioni?.length
        ? t.opzioni.map(o => `${o.nome.split('(')[0].trim()}: € ${(global.AbraUI?.formatEuro || (n => n))(o.totale)}`).join(' · ')
        : `€ ${(global.AbraUI?.formatEuro || (n => n))(t.subtotal)} IVA escl.`;
      wrap.innerHTML = `
        <div class="chat-offer-preview-head">
          <span class="chat-offer-preview-label">Preventivo formale · ${offer.line_items.length} righe</span>
          <div class="chat-offer-preview-actions">
            <button type="button" class="chat-offer-toggle">Espandi</button>
            <button type="button" class="chat-offer-pdf">Scarica PDF</button>
            <a href="offerta.html" class="chat-offer-open">Modifica →</a>
          </div>
        </div>
        <div class="chat-offer-preview-total">${t.opzioni?.length > 1 ? 'Totali configurazione: ' : 'Totale quotato: '}<strong>${mainTotal}</strong></div>
        <div class="chat-offer-preview-body offer-preview-body collapsed">${global.AbraOfferDraft.renderPreviewHtml(offer)}</div>`;
      const body = wrap.querySelector('.chat-offer-preview-body');
      wrap.querySelector('.chat-offer-toggle').addEventListener('click', () => {
        body.classList.toggle('collapsed');
        wrap.querySelector('.chat-offer-toggle').textContent = body.classList.contains('collapsed') ? 'Espandi' : 'Comprimi';
      });
      wrap.querySelector('.chat-offer-pdf').addEventListener('click', () => {
        global.AbraOfferDraft.saveSession(offer);
        global.AbraOfferDraft.downloadPdf(offer);
      });
      wrap.querySelector('.chat-offer-open').addEventListener('click', () => {
        global.AbraOfferDraft.saveSession(offer);
      });
      row.querySelector('.chat-bubble-wrap').appendChild(wrap);
    }

    _attachQuoteCard(row, quote) {
      const card = document.createElement('a');
      card.className = 'quote-card';
      card.href = 'offerta.html';
      card.addEventListener('click', () => {
        if (quote?.lines?.length) {
          sessionStorage.setItem('abra_chat_quote_prefill', JSON.stringify({
            skus: quote.lines.map(l => l.sku).filter(Boolean),
            margin_key: 'end_user',
            ts: Date.now(),
          }));
        }
      });
      card.innerHTML = `<span class="quote-card-label">Preventivo calcolato</span>
        <strong>€ ${(global.AbraUI?.formatEuro || (n => n))(quote.total_eur || quote.subtotal)}</strong>
        <span class="quote-card-cta">Apri in Crea offerta →</span>`;
      row.querySelector('.chat-bubble-wrap').appendChild(card);
    }

    _appendRow(role, text, meta) {
      const wrap = document.createElement('article');
      const time = new Date().toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });
      if (role === 'bot') {
        wrap.className = 'chat-row chat-row-bot';
        if (meta.isScenario) wrap.classList.add('chat-row-scenario');
        if (meta.labSystem) wrap.classList.add('chat-row-lab-system');
        wrap.innerHTML = `
          <div class="chat-avatar chat-avatar-sm">${escapeHtml(this.opts.avatarLetter)}</div>
          <div class="chat-bubble-wrap">
            <div class="chat-bubble bot">${formatBotHtml(text)}</div>
            <time class="chat-meta">${time}</time>
          </div>`;
      } else {
        wrap.className = 'chat-row chat-row-user';
        wrap.innerHTML = `
          <div class="chat-bubble-wrap user-wrap">
            <div class="chat-bubble user">${escapeHtml(text)}</div>
            <time class="chat-meta">${time}</time>
          </div>`;
      }
      if (meta.feedbackId) wrap.dataset.feedbackId = meta.feedbackId;
      this.messagesEl.appendChild(wrap);
      this.scrollBottom();
      return wrap;
    }

    _attachFeedback(row, meta) {
      if (this.opts.feedbackMode === 'lab') {
        this._attachFeedbackLab(row, meta);
        return;
      }
      this._attachFeedbackLegacy(row, meta);
    }

    _attachFeedbackLab(row, meta) {
      const fbId = meta.feedbackId;
      const block = document.createElement('div');
      block.className = 'chat-feedback-lab';
      block.innerHTML = `
        <p class="fb-lab-title">Com'è andata questa risposta?</p>
        <div class="fb-lab-choices">
          <button type="button" class="fb-lab-btn fb-lab-good" data-act="good">Va bene</button>
          <button type="button" class="fb-lab-btn fb-lab-fix" data-act="fix">Da correggere</button>
          <button type="button" class="fb-lab-btn fb-lab-kb" data-act="kb">Integra in knowledge</button>
        </div>
        <p class="fb-lab-status" hidden></p>
        <div class="fb-lab-panel hidden">
          <label class="fb-lab-label">Come avrebbe dovuto rispondere?</label>
          <textarea rows="3" placeholder="Scrivi la risposta corretta…"></textarea>
          <div class="fb-lab-panel-actions">
            <button type="button" class="fb-lab-save">Salva correzione</button>
            <button type="button" class="fb-lab-cancel">Annulla</button>
          </div>
        </div>`;

      row.querySelector('.chat-bubble-wrap').appendChild(block);

      const choices = block.querySelector('.fb-lab-choices');
      const status = block.querySelector('.fb-lab-status');
      const panel = block.querySelector('.fb-lab-panel');
      const notify = (msg) => {
        this.opts.onFeedback();
        global.AbraUI?.toast?.(msg || 'Feedback salvato', 'ok');
      };

      const setDone = (text, variant) => {
        choices.hidden = true;
        status.hidden = false;
        status.textContent = text;
        status.dataset.variant = variant || '';
        panel.classList.add('hidden');
      };

      block.addEventListener('click', e => {
        const btn = e.target.closest('.fb-lab-btn');
        if (!btn || choices.hidden) return;
        const act = btn.dataset.act;

        if (act === 'good') {
          FeedbackStore.update(fbId, { rating: 1, action: 'approved' });
          setDone('✓ Registrato: risposta valida per il training', 'good');
          notify('Risposta segnata come valida');
        } else if (act === 'fix') {
          panel.classList.remove('hidden');
          panel.querySelector('textarea').focus();
          row.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        } else if (act === 'kb') {
          const entry = FeedbackStore.all().find(x => x.id === fbId);
          if (entry) {
            FeedbackStore.queueForKb(entry);
            FeedbackStore.update(fbId, { rating: 1, action: 'queued_kb' });
            setDone('📚 In coda per la knowledge base (esporta dal pannello a destra)', 'kb');
            notify('Aggiunto alla knowledge');
          }
        }
      });

      panel.querySelector('.fb-lab-save').addEventListener('click', () => {
        const correction = panel.querySelector('textarea').value.trim();
        if (!correction) return;
        FeedbackStore.update(fbId, { correction, rating: -1, action: 'corrected' });
        const entry = FeedbackStore.all().find(x => x.id === fbId);
        if (entry && entry.action !== 'queued_kb') {
          FeedbackStore.queueForKb({ ...entry, correction });
          FeedbackStore.update(fbId, { action: 'corrected_kb' });
        }
        const bubble = row.querySelector('.chat-bubble.bot');
        bubble.innerHTML = formatBotHtml(correction);
        bubble.classList.add('corrected');
        setDone('✎ Correzione salvata + in coda KB', 'fix');
        notify('Correzione e knowledge aggiornati');
      });
      panel.querySelector('.fb-lab-cancel').addEventListener('click', () => panel.classList.add('hidden'));
    }

    _attachFeedbackLegacy(row, meta) {
      const bar = document.createElement('div');
      bar.className = 'chat-feedback';
      bar.innerHTML = `
        <button type="button" class="fb-btn" data-act="up" aria-label="Utile"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 10v12M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2a3.13 3.13 0 0 1 3 3.88Z"/></svg></button>
        <button type="button" class="fb-btn" data-act="down" aria-label="Non utile"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 14V2M9 18.12 10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H20a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.76a2 2 0 0 0-1.79 1.11L12 22a3.13 3.13 0 0 1-3-3.88Z"/></svg></button>
        <button type="button" class="fb-btn fb-label" data-act="correct">Correggi</button>
        <button type="button" class="fb-btn fb-label" data-act="kb">+ KB</button>`;

      const panel = document.createElement('div');
      panel.className = 'fb-correction-panel hidden';
      panel.innerHTML = `
        <textarea rows="3" placeholder="Risposta corretta…"></textarea>
        <div class="fb-panel-actions">
          <button type="button" class="fb-save">Salva correzione</button>
          <button type="button" class="fb-cancel">Annulla</button>
        </div>`;

      row.querySelector('.chat-bubble-wrap').appendChild(bar);
      row.querySelector('.chat-bubble-wrap').appendChild(panel);

      const fbId = meta.feedbackId;
      const notify = () => { this.opts.onFeedback(); global.AbraUI?.toast?.('Feedback salvato', 'ok'); };

      bar.addEventListener('click', e => {
        const btn = e.target.closest('.fb-btn');
        if (!btn) return;
        const act = btn.dataset.act;
        bar.querySelectorAll('.fb-btn').forEach(b => b.classList.remove('active'));
        if (act === 'up') {
          FeedbackStore.update(fbId, { rating: 1, action: 'approved' });
          btn.classList.add('active');
          notify();
        } else if (act === 'correct') {
          panel.classList.toggle('hidden');
          if (!panel.classList.contains('hidden')) {
            panel.querySelector('textarea').focus();
            row.scrollIntoView({ block: 'center', behavior: 'smooth' });
          }
        } else if (act === 'down') {
          FeedbackStore.update(fbId, { rating: -1, action: 'rejected' });
          btn.classList.add('active');
          panel.classList.remove('hidden');
          row.scrollIntoView({ block: 'center', behavior: 'smooth' });
        } else if (act === 'kb') {
          const entry = FeedbackStore.all().find(x => x.id === fbId);
          if (entry) {
            FeedbackStore.queueForKb(entry);
            FeedbackStore.update(fbId, { action: 'queued_kb' });
            btn.textContent = '✓ KB';
            btn.disabled = true;
            notify();
          }
        }
      });

      panel.querySelector('.fb-save').addEventListener('click', () => {
        const correction = panel.querySelector('textarea').value.trim();
        if (!correction) return;
        FeedbackStore.update(fbId, { correction, rating: -1, action: 'corrected' });
        const bubble = row.querySelector('.chat-bubble.bot');
        bubble.innerHTML = formatBotHtml(correction);
        bubble.classList.add('corrected');
        panel.classList.add('hidden');
        notify();
      });
      panel.querySelector('.fb-cancel').addEventListener('click', () => panel.classList.add('hidden'));
    }

    showTyping() {
      this.hideTyping();
      this._hideEmpty();
      const el = document.createElement('article');
      el.className = 'chat-row chat-row-bot chat-typing-row';
      el.innerHTML = `
        <div class="chat-avatar chat-avatar-sm">${escapeHtml(this.opts.avatarLetter)}</div>
        <div class="chat-bubble bot typing"><span></span><span></span><span></span></div>`;
      this.messagesEl.appendChild(el);
      this._typingEl = el;
      this.scrollBottom();
    }

    hideTyping() { this._typingEl?.remove(); this._typingEl = null; }
    scrollBottom() { this.messagesEl.scrollTop = this.messagesEl.scrollHeight; }

    async _handleSend(e) {
      e.preventDefault();
      const q = this.inputEl.value.trim();
      if (!q) return;
      this.inputEl.value = '';
      this.inputEl.style.height = 'auto';
      this.appendUser(q);
      this.sendBtn.disabled = true;
      this.showTyping();
      this.setStatus('Sta scrivendo…', false);
      try {
        const result = await this.opts.onSend(q);
        if (result?.silent) {
          this.hideTyping();
          this.setStatus('Online', true);
          this.sendBtn.disabled = false;
          this.inputEl.focus();
          return;
        }
        const reply = typeof result === 'string' ? result : (result?.reply ?? '');
        const skipFeedback = !!result?.skipFeedback;
        const fbId = skipFeedback ? null : uid();
        if (!skipFeedback && fbId) {
          FeedbackStore.save({
            id: fbId,
            timestamp: new Date().toISOString(),
            question: q,
            answer: reply,
            sources: (result.sources || []).map(s => ({ id: s.id, title: s.title, score: s.score, text: s.text })),
            quote: result.quote || null,
            model_mode: global.AbraLLM?.loadConfig?.().mode || 'offline',
            rating: null, correction: null, action: 'pending',
          });
        }
        await this.appendBotStreamed(reply, {
          feedbackId: fbId,
          answer: reply,
          sources: result.sources || [],
          quote: result.quote || null,
          offerDraft: result.offerDraft || null,
          labSystem: skipFeedback,
        });
        this.setStatus('Online', true);
      } catch (err) {
        this.hideTyping();
        this.appendBot('Errore: ' + err.message, { labSystem: true });
        this.setStatus('Errore', false);
      }
      this.sendBtn.disabled = false;
      this.inputEl.focus();
    }

    setComposePlaceholder(text) {
      if (this.inputEl) this.inputEl.placeholder = text;
    }

    setComposeHint(text) {
      const el = document.getElementById('chat-compose-hint');
      if (el) el.textContent = text;
    }
  }

  global.AbraFeedbackStore = FeedbackStore;
  global.AbraChatUI = ChatUI;
})(typeof window !== 'undefined' ? window : globalThis);
