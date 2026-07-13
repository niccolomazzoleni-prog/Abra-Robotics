/* Area offerte riservata — password in data/offers-auth.json (sessione 8 h). */
(function () {
  'use strict';

  const AUTH_URL = (() => {
    const p = window.location.pathname;
    if (p.includes('/samples/')) return '../../data/offers-auth.json';
    if (p.includes('/offerte-ai/')) return '../data/offers-auth.json';
    return '/data/offers-auth.json';
  })();
  const SESSION_KEY = 'abra_offers_until';
  const SESSION_MS = 8 * 60 * 60 * 1000;
  const FALLBACK_HASH = 'bf4392f1e156b8a0ba52592e03f0141e26cbffdc840fac611c34905b4463c12e';

  function notifyUnlock() {
    document.dispatchEvent(new CustomEvent('abra-offers-unlock'));
  }

  window.AbraOffersAuth = {
    isUnlocked() {
      if (window.AbraAdmin?.isUnlocked?.()) return true;
      return Date.now() < Number(sessionStorage.getItem(SESSION_KEY) || 0);
    },
    unlock() {
      sessionStorage.setItem(SESSION_KEY, String(Date.now() + SESSION_MS));
      notifyUnlock();
    },
    logout() {
      sessionStorage.removeItem(SESSION_KEY);
      location.reload();
    },
    whenUnlocked(fn) {
      if (this.isUnlocked()) fn();
      else document.addEventListener('abra-offers-unlock', fn, { once: true });
    },
  };

  async function sha256(text) {
    const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
    return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
  }

  function gateHtml() {
    return `
      <div id="offer-gate" style="position:fixed;inset:0;z-index:9999;background:#fafafa;display:flex;align-items:center;justify-content:center;padding:24px;font-family:'Satoshi',system-ui,sans-serif;">
        <form id="offer-login-form" style="width:100%;max-width:400px;background:#fff;border:1px solid #e5e5e5;border-radius:12px;padding:28px;box-shadow:0 8px 32px rgba(0,0,0,0.08);">
          <p style="font-size:0.72rem;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;color:#7c4dd6;margin:0;">Abra Robotics · offerte riservate</p>
          <h2 style="margin:8px 0 16px;font-size:1.5rem;">Accesso preventivi</h2>
          <p style="color:#525252;font-size:0.88rem;line-height:1.5;margin-bottom:20px;">
            Le offerte commerciali sono riservate al team Abra. Inserisci la password per visualizzare e stampare in PDF.
          </p>
          <label style="display:block;font-size:0.78rem;font-weight:700;margin-bottom:6px;">Password offerte</label>
          <input type="password" id="offer-pwd" required autocomplete="current-password" style="width:100%;padding:10px 12px;border:1px solid #e5e5e5;border-radius:8px;margin-bottom:14px;font:inherit;">
          <button type="submit" style="width:100%;padding:12px;border:none;border-radius:8px;background:#0a0a0a;color:#fff;font-weight:700;font:inherit;cursor:pointer;">Accedi</button>
          <p id="offer-login-err" style="color:#b91c1c;font-size:0.82rem;margin-top:12px;display:none;"></p>
        </form>
      </div>`;
  }

  async function initGate() {
    if (window.AbraOffersAuth.isUnlocked()) {
      notifyUnlock();
      return;
    }

    const auth = await fetch(AUTH_URL).then(r => r.json()).catch(() => ({}));
    const expected = auth.password_sha256 || FALLBACK_HASH;

    document.body.insertAdjacentHTML('afterbegin', gateHtml());
    document.body.style.overflow = 'hidden';
    const wrap = document.querySelector('.offer-sample-wrap, .offer-shell, .oai-page');
    if (wrap) wrap.style.visibility = 'hidden';

    document.getElementById('offer-login-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const err = document.getElementById('offer-login-err');
      err.style.display = 'none';
      const pwd = document.getElementById('offer-pwd').value;
      try {
        const hash = await sha256(pwd);
        if (hash !== expected) throw new Error('Password errata.');
        window.AbraOffersAuth.unlock();
        document.getElementById('offer-gate').remove();
        document.body.style.overflow = '';
        if (wrap) wrap.style.visibility = '';
      } catch (ex) {
        err.textContent = ex.message || 'Errore accesso';
        err.style.display = 'block';
      }
    });
  }

  document.addEventListener('DOMContentLoaded', initGate);
})();
