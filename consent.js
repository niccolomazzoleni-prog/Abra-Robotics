// Banner consenso cookie (Linee guida Garante 10/06/2021) integrato con le campagne:
// - Google Consent Mode v2: il default "denied" e la scelta salvata sono impostati
//   dallo snippet inline in <head> (prima di Tag Manager); qui solo interfaccia e aggiornamenti.
// - Meta Pixel: in pagina parte con fbq('consent','revoke'), qui diventa 'grant' solo col consenso marketing.
// - Tag Manager riceve l'evento "abra_consent_update" (statistiche / marketing) per i tag non Google.
(function () {
  'use strict';
  var KEY = 'abra_consent';
  var VERSION = 1;
  var MAX_AGE = 180 * 24 * 3600 * 1000; // la scelta si richiede dopo 6 mesi

  function read() {
    try {
      var c = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (c && c.v === VERSION && Date.now() - c.ts < MAX_AGE) return c;
    } catch (e) {}
    return null;
  }

  function apply(c) {
    var g = function (v) { return v ? 'granted' : 'denied'; };
    window.dataLayer = window.dataLayer || [];
    if (typeof window.gtag !== 'function') window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'update', {
      analytics_storage: g(c.analytics),
      ad_storage: g(c.marketing),
      ad_user_data: g(c.marketing),
      ad_personalization: g(c.marketing),
    });
    if (typeof window.fbq === 'function') window.fbq('consent', c.marketing ? 'grant' : 'revoke');
    window.dataLayer.push({ event: 'abra_consent_update', consent_analytics: !!c.analytics, consent_marketing: !!c.marketing });
  }

  function save(analytics, marketing) {
    var c = { v: VERSION, ts: Date.now(), analytics: !!analytics, marketing: !!marketing };
    try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {}
    window.abraConsent = c;
    apply(c);
    close();
  }

  var banner;
  function close() { if (banner) { banner.remove(); banner = null; } }

  function prefix() {
    var p = location.pathname;
    if (/\/en\/(prodotti|blog)\//.test(p)) return '../../';
    if (/\/(prodotti|blog|en|editor)\//.test(p)) return '../';
    return '';
  }

  var CSS = '.consent-banner{position:fixed;left:16px;right:16px;bottom:16px;z-index:2147483000;max-width:760px;margin:0 auto;background:#0a0a0a;color:#f5f5f5;border-radius:12px;padding:14px 44px 14px 16px;box-shadow:0 12px 40px rgba(0,0,0,.3);font:14px/1.45 Satoshi,-apple-system,BlinkMacSystemFont,sans-serif}' +
    '.consent-text{margin:0 0 10px;font-size:13px;color:#e5e5e5}.consent-text a{color:#fff;text-decoration:underline}' +
    '.consent-prefs{display:grid;gap:6px;margin:0 0 10px;font-size:13px}.consent-prefs[hidden]{display:none}.consent-prefs label{display:flex;gap:8px;align-items:center}' +
    '.consent-actions{display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end}' +
    '.consent-btn{font:inherit;font-weight:600;font-size:13px;padding:8px 14px;border-radius:8px;border:1px solid #fff;background:transparent;color:#fff;cursor:pointer}' +
    '.consent-btn[hidden]{display:none}' +
    '.consent-x{position:absolute;top:6px;right:8px;width:32px;height:32px;border:0;background:transparent;color:#fff;font-size:22px;line-height:1;cursor:pointer}' +
    '.consent-open{cursor:pointer}' +
    '@media (max-width:520px){.consent-actions{justify-content:stretch}.consent-btn{flex:1 1 28%;padding:8px 6px}}';

  function open(showPrefs) {
    if (!document.getElementById('consent-css')) {
      var st = document.createElement('style');
      st.id = 'consent-css';
      st.textContent = CSS;
      document.head.appendChild(st);
    }
    close();
    var en = document.documentElement.lang === 'en' || location.pathname.indexOf('/en/') >= 0;
    var c = read() || { analytics: false, marketing: false };
    var T = en ? {
      text: 'We use technical cookies and, with your consent, statistics (Google Analytics) and marketing cookies (Google Ads, Meta) to measure visits and campaigns.',
      policy: 'Cookie Policy', reject: 'Reject', accept: 'Accept all', prefs: 'Customise', save: 'Save choices',
      tech: 'Technical (always on)', stats: 'Statistics: Google Analytics', mkt: 'Marketing: Google Ads, Meta Pixel', close: 'Close and reject',
      policyHref: (/\/en\/(prodotti|blog)\//.test(location.pathname) ? '../' : '') + 'cookie-policy-en.html',
    } : {
      text: 'Usiamo cookie tecnici e, con il tuo consenso, cookie di statistica (Google Analytics) e di marketing (Google Ads, Meta) per misurare visite e campagne.',
      policy: 'Cookie Policy', reject: 'Rifiuta', accept: 'Accetta tutti', prefs: 'Personalizza', save: 'Salva le scelte',
      tech: 'Tecnici (sempre attivi)', stats: 'Statistiche: Google Analytics', mkt: 'Marketing: Google Ads, Meta Pixel', close: 'Chiudi e rifiuta',
      policyHref: prefix() + 'cookie-policy.html',
    };
    banner = document.createElement('div');
    banner.className = 'consent-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Preferenze cookie');
    banner.innerHTML =
      '<button type="button" class="consent-x" aria-label="' + T.close + '">×</button>' +
      '<p class="consent-text">' + T.text + ' <a href="' + T.policyHref + '">' + T.policy + '</a></p>' +
      '<div class="consent-prefs"' + (showPrefs ? '' : ' hidden') + '>' +
        '<label><input type="checkbox" checked disabled> ' + T.tech + '</label>' +
        '<label><input type="checkbox" name="analytics"' + (c.analytics ? ' checked' : '') + '> ' + T.stats + '</label>' +
        '<label><input type="checkbox" name="marketing"' + (c.marketing ? ' checked' : '') + '> ' + T.mkt + '</label>' +
      '</div>' +
      '<div class="consent-actions">' +
        '<button type="button" class="consent-btn" data-act="reject">' + T.reject + '</button>' +
        '<button type="button" class="consent-btn" data-act="prefs">' + T.prefs + '</button>' +
        '<button type="button" class="consent-btn" data-act="save" hidden>' + T.save + '</button>' +
        '<button type="button" class="consent-btn consent-btn-primary" data-act="accept">' + T.accept + '</button>' +
      '</div>';
    document.body.appendChild(banner);
    var prefs = banner.querySelector('.consent-prefs');
    var btnSave = banner.querySelector('[data-act="save"]');
    var btnPrefs = banner.querySelector('[data-act="prefs"]');
    if (showPrefs) { btnSave.hidden = false; btnPrefs.hidden = true; }
    banner.addEventListener('click', function (e) {
      var act = e.target.getAttribute('data-act');
      if (e.target.classList.contains('consent-x') || act === 'reject') save(false, false);
      else if (act === 'accept') save(true, true);
      else if (act === 'prefs') { prefs.hidden = false; btnSave.hidden = false; btnPrefs.hidden = true; }
      else if (act === 'save') save(prefs.querySelector('[name="analytics"]').checked, prefs.querySelector('[name="marketing"]').checked);
    });
  }

  // Link "Preferenze cookie" nel footer di ogni pagina, per cambiare idea in qualsiasi momento.
  function footerLink() {
    var legal = document.querySelector('.footer-legal') || document.querySelector('.footer-bottom');
    if (!legal || legal.querySelector('.consent-open')) return;
    var a = document.createElement('a');
    a.href = '#';
    a.className = 'consent-open';
    a.textContent = document.documentElement.lang === 'en' ? 'Cookie preferences' : 'Preferenze cookie';
    a.addEventListener('click', function (e) { e.preventDefault(); open(true); });
    legal.appendChild(a);
  }

  window.abraConsentOpen = function () { open(true); };

  function init() {
    // Il vecchio avviso "solo cookie tecnici" non vale piu'.
    try { localStorage.removeItem('abra_cookie_notice'); } catch (e) {}
    footerLink();
    var c = read();
    if (c) { window.abraConsent = c; return; }
    open(false);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
