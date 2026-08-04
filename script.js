// === Endpoint form (primario + secondario in parallelo) ===
// Primario — deployment live al 12 luglio 2026 (funzionante, foglio Niccolò 1nXl0…).
window.GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbw1WeoJYZltyorwQ-8Nftg0DdiOXOV-Zl3MlRegJS2ybhAzaRaqZNpTRamEbHJe2NtK/exec';
// Secondario — nuovo deploy Abra_Deployment (Code.gs aggiornato + foglio 15zvBH…); attivo quando pubblico.
window.GOOGLE_SCRIPT_URL_SECONDARY = 'https://script.google.com/macros/s/AKfycbxPPfh3qZRF0GwnKJicY5rcgdMSRoW_liBenRQValdCPSCM2MrZR_Y6fwrAZOHgCrDW/exec';
const GOOGLE_SCRIPT_URL = window.GOOGLE_SCRIPT_URL;

function getGoogleScriptLeadEndpoints() {
  return [...new Set(
    [window.GOOGLE_SCRIPT_URL, window.GOOGLE_SCRIPT_URL_SECONDARY]
      .map(function (u) { return String(u || '').trim(); })
      .filter(Boolean)
  )];
}

function encodeLeadPayloadForAppsScript(payload) {
  var params = new URLSearchParams();
  Object.keys(payload || {}).forEach(function (key) {
    var val = payload[key];
    if (val === undefined || val === null) return;
    params.append(key, String(val));
  });
  return params;
}

function postLeadToGoogleScripts(payload) {
  var body = encodeLeadPayloadForAppsScript(payload).toString();
  return Promise.allSettled(getGoogleScriptLeadEndpoints().map(function (url) {
    return fetch(url, {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
      body: body
    });
  }));
}

window.getGoogleScriptLeadEndpoints = getGoogleScriptLeadEndpoints;
window.postLeadToGoogleScripts = postLeadToGoogleScripts;
window.encodeLeadPayloadForAppsScript = encodeLeadPayloadForAppsScript;

// reCAPTCHA v3 — inserisci la site key dopo registrazione su https://www.google.com/recaptcha/admin
// Lascia vuoto per disabilitare (la validazione server-side resta attiva)
const RECAPTCHA_SITE_KEY = '6LeozTQtAAAAAJ8MLsZiT7a5mdol2TSR043VP0-2';

window._formLoadTime = Date.now();

(function loadRecaptcha() {
  if (!RECAPTCHA_SITE_KEY) return;
  const s = document.createElement('script');
  s.src = 'https://www.google.com/recaptcha/api.js?render=' + RECAPTCHA_SITE_KEY;
  s.async = true;
  document.head.appendChild(s);
})();

(function initHeroVideo() {
  const video = document.querySelector('.hero-video');
  if (!video) return;
  const base = window.location.pathname.includes('/en/') ? '../images/' : 'images/';
  const sources = {
    mobile: base + 'hero-bg-mobile.mp4',
    desktop: base + 'hero-bg-desktop.mp4',
  };
  const mql = window.matchMedia('(max-width: 768px)');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saveData = !!(navigator.connection && navigator.connection.saveData);

  function apply() {
    if (reduceMotion || saveData) {
      video.removeAttribute('autoplay');
      video.pause();
      return;
    }
    const src = mql.matches ? sources.mobile : sources.desktop;
    if (video.dataset.activeSrc === src) return;
    video.dataset.activeSrc = src;
    video.innerHTML = '';
    const source = document.createElement('source');
    source.src = src;
    source.type = 'video/mp4';
    video.appendChild(source);
    video.load();
    const playPromise = video.play();
    if (playPromise && playPromise.catch) playPromise.catch(function () {});
  }

  // Non competere con FCP/LCP: carica il video dopo il first paint.
  function schedule() {
    if ('requestIdleCallback' in window) {
      requestIdleCallback(apply, { timeout: 2000 });
    } else {
      setTimeout(apply, 1);
    }
  }
  if (document.readyState === 'complete') schedule();
  else window.addEventListener('load', schedule, { once: true });
  mql.addEventListener('change', apply);
})();

function injectContactHoneypots() {
  document.querySelectorAll('.contact-form, .quote-form-top').forEach(form => {
    if (form.querySelector('input[name="website"]')) return;
    const hp = document.createElement('input');
    hp.type = 'hidden';
    hp.name = 'website';
    form.appendChild(hp);
  });
}

function validateContactForm(form) {
  const hp = form.querySelector('input[name="website"]');
  if (hp && hp.value.trim()) return false;

  if (Date.now() - window._formLoadTime < 3000) return false;

  const invalid = [...form.querySelectorAll('[required]')].filter(f => !f.value.trim());
  if (invalid.length) {
    invalid[0].focus();
    invalid[0].reportValidity();
    return false;
  }

  const nome = (form.querySelector('[name="nome"]')?.value || '').trim();
  const email = (form.querySelector('[name="email"]')?.value || '').trim();
  const telefono = (form.querySelector('[name="telefono"]')?.value || '').trim();
  const messaggio = (form.querySelector('[name="messaggio"]')?.value || '').trim();

  if (nome.length < 2) {
    const f = form.querySelector('[name="nome"]');
    if (f) { f.focus(); f.setCustomValidity('Inserisci il tuo nome completo.'); f.reportValidity(); f.setCustomValidity(''); }
    return false;
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
    const f = form.querySelector('[name="email"]');
    if (f) { f.focus(); f.setCustomValidity('Inserisci un indirizzo email valido.'); f.reportValidity(); f.setCustomValidity(''); }
    return false;
  }
  if (telefono.replace(/\D/g, '').length < 6) {
    const f = form.querySelector('[name="telefono"]');
    if (f) { f.focus(); f.setCustomValidity('Inserisci un numero di telefono valido.'); f.reportValidity(); f.setCustomValidity(''); }
    return false;
  }
  if (messaggio.length < 5) {
    const f = form.querySelector('[name="messaggio"]');
    if (f) { f.focus(); f.setCustomValidity('Inserisci un messaggio.'); f.reportValidity(); f.setCustomValidity(''); }
    return false;
  }
  return true;
}

function buildContactPayload(form) {
  const payload = Object.fromEntries(new FormData(form).entries());
  if (!payload.azienda && payload.istituzione) payload.azienda = payload.istituzione;
  payload.prodotto = payload.prodotto || form.dataset.product || '';
  payload.origine = form.dataset.origine || payload.prodotto || payload.origine || 'Form contatti';
  payload.pagina = document.title;
  payload.url = location.href;
  payload.timestamp = new Date().toISOString();
  payload.form_load_time = window._formLoadTime || 0;
  if (window.AbraAds && window.AbraAds.getGclid) {
    payload.gclid = payload.gclid || window.AbraAds.getGclid();
  }
  return payload;
}

function contactFormDepthPrefix() {
  const p = location.pathname;
  let depth = 0;
  if (p.includes('/en/prodotti/') || p.includes('/en/blog/')) depth = 2;
  else if (p.includes('/prodotti/') || p.includes('/blog/') || p.includes('/en/')) depth = 1;
  return depth ? '../'.repeat(depth) : '';
}

function getThankYouHref() {
  const isEn = location.pathname.includes('/en/');
  return contactFormDepthPrefix() + (isEn ? 'lp-thank-you-en/' : 'lp-thank-you/');
}

function showInlineFormSuccess(form, feedback) {
  if (!feedback) return false;
  const isEn = document.documentElement.lang === 'en' || location.pathname.includes('/en/');
  const msg = form.classList.contains('quote-form-top')
    ? (isEn ? 'Request sent! We will get back to you within 12 hours.' : 'Richiesta inviata! Ti ricontattiamo entro 12 ore.')
    : (isEn ? 'Message sent! We will contact you within 2 business hours.' : 'Messaggio inviato! Ti contattiamo entro 2 ore lavorative.');
  const base = feedback.className.split(' ').filter(c => c && c !== 'success' && c !== 'error')[0] || 'form-feedback';
  feedback.className = base + ' success';
  feedback.textContent = msg;
  form.reset();
  return true;
}

injectContactHoneypots();

document.querySelectorAll('.contact-form, .quote-form-top').forEach(form => {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    e.stopImmediatePropagation();
    if (!validateContactForm(form)) return;
    const submitBtn = form.querySelector('.form-submit') || form.querySelector('[type="submit"]');
    const feedback = form.querySelector('.form-feedback') || form.querySelector('.quote-form-feedback');
    const origText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Invio in corso...';
    if (feedback) { feedback.className = feedback.className.split(' ')[0]; feedback.textContent = ''; }

    const payload = buildContactPayload(form);

    if (RECAPTCHA_SITE_KEY && window.grecaptcha) {
      try {
        payload.recaptcha_token = await window.grecaptcha.execute(RECAPTCHA_SITE_KEY, { action: 'contact' });
      } catch (_) {}
    }

    try {
      await postLeadToGoogleScripts(payload);
      if (window.AbraAds && window.AbraAds.trackLead) window.AbraAds.trackLead();
      if (window.fbq) fbq('track', 'Lead');
      if (showInlineFormSuccess(form, feedback)) return;
      form.reset();
      window.location.href = getThankYouHref();
    } catch {
      if (feedback) { feedback.className = feedback.className.split(' ')[0] + ' error'; feedback.textContent = 'Errore nell\'invio. Scrivi direttamente a info@abrarobotics.com.'; }
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = origText;
    }
  }, true);
});

// Response-time note below every submit button
(function () {
  const isEn = document.documentElement.lang === 'en' || window.location.pathname.includes('/en/');
  const msg = isEn
    ? 'We will get back to you within 2 business hours.'
    : 'Ti ricontattiamo entro 2 ore lavorative.';
  document.querySelectorAll('.contact-form, .quote-form-top').forEach(form => {
    const btn = form.querySelector('.form-submit, [type="submit"]');
    if (!btn) return;
    const note = document.createElement('p');
    note.className = 'form-note';
    note.style.marginTop = '10px';
    note.textContent = msg;
    btn.insertAdjacentElement('afterend', note);
  });
})();

// Mobile menu toggle
const menuToggle = document.querySelector('.menu-toggle');
const mobileMenu = document.querySelector('.mobile-menu');

if (menuToggle && mobileMenu) {
  // a11y: collega il toggle al menu ed esponi lo stato aperto/chiuso
  if (!mobileMenu.id) mobileMenu.id = 'mobile-menu';
  menuToggle.setAttribute('aria-controls', mobileMenu.id);
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.setAttribute('aria-haspopup', 'true');

  menuToggle.addEventListener('click', () => {
    const isOpen = mobileMenu.style.display === 'flex';
    mobileMenu.style.display = isOpen ? 'none' : 'flex';
    menuToggle.classList.toggle('active');
    menuToggle.setAttribute('aria-expanded', String(!isOpen));
  });

  // Close mobile menu on link click
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      mobileMenu.style.display = 'none';
      menuToggle.classList.remove('active');
      menuToggle.setAttribute('aria-expanded', 'false');
    });
  });

  // Mobile dropdown accordion (con stato ARIA)
  mobileMenu.querySelectorAll('.mobile-dropdown-trigger').forEach((trigger, i) => {
    const dd = trigger.closest('.mobile-dropdown');
    const panel = dd && dd.querySelector('.mobile-dropdown-panel');
    if (panel && !panel.id) panel.id = `mobile-dd-panel-${i}`;
    trigger.setAttribute('aria-haspopup', 'true');
    trigger.setAttribute('aria-expanded', 'false');
    if (panel) trigger.setAttribute('aria-controls', panel.id);
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const open = dd.classList.toggle('open');
      trigger.setAttribute('aria-expanded', String(open));
    });
  });
}

// Dropdown desktop (apertura via CSS hover/focus-within): sincronizza aria-expanded
document.querySelectorAll('.nav-item-dropdown').forEach((item, i) => {
  const trigger = item.querySelector('.nav-dropdown-trigger');
  const panel = item.querySelector('.nav-dropdown-panel');
  if (!trigger) return;
  if (panel && !panel.id) panel.id = `nav-dd-panel-${i}`;
  trigger.setAttribute('aria-haspopup', 'true');
  trigger.setAttribute('aria-expanded', 'false');
  if (panel) trigger.setAttribute('aria-controls', panel.id);
  const setExpanded = (v) => trigger.setAttribute('aria-expanded', String(v));
  item.addEventListener('mouseenter', () => setExpanded(true));
  item.addEventListener('mouseleave', () => setExpanded(false));
  item.addEventListener('focusin', () => setExpanded(true));
  item.addEventListener('focusout', () => setExpanded(false));
});

// Navbar background on scroll
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 10) {
    navbar.style.boxShadow = '0 1px 8px rgba(0,0,0,0.04)';
  } else {
    navbar.style.boxShadow = 'none';
  }
});

// Scroll-triggered fade-in with stagger
const observerOptions = {
  threshold: 0.12,
  rootMargin: '0px 0px -40px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const animatedElements = prefersReducedMotion ? [] : document.querySelectorAll(
  '.card, .use-case, .step, .about-stat, .report-card, .faq-item, .social-proof-stat'
);

animatedElements.forEach((el, i) => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  // Stagger within parent: find siblings of same type
  const parent = el.parentElement;
  const siblings = Array.from(parent.children).filter(c => c.tagName === el.tagName || c.classList.contains(el.classList[0]));
  const indexInParent = siblings.indexOf(el);
  el.style.transition = `opacity 0.6s ease ${indexInParent * 0.1}s, transform 0.6s ease ${indexInParent * 0.1}s`;
  observer.observe(el);
});

// Visible class + honeypot hide
document.head.insertAdjacentHTML('beforeend', `
  <style>
    .visible {
      opacity: 1 !important;
      transform: translateY(0) !important;
    }
  </style>
`);

// Meta Pixel — eventi click globali
document.addEventListener('click', (e) => {
  if (!window.fbq) return;
  const el = e.target.closest('a, button');
  if (!el) return;
  // WhatsApp
  if (el.classList.contains('wa-btn') || (el.href && el.href.includes('wa.me'))) {
    fbq('track', 'Contact', { content_name: 'whatsapp' });
  }
  // Prenota una chiamata
  const txt = el.textContent.trim().toLowerCase();
  if (txt.includes('prenota') || txt.includes('chiama') || txt.includes('chiamata')) {
    fbq('track', 'Contact', { content_name: 'prenota_chiamata' });
  }
});

// FAQ accordion (button pattern — schede compatte)
(function () {
  document.querySelectorAll('.faq-list .faq-item button.faq-question').forEach((btn) => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      if (!item) return;
      const open = item.classList.contains('open');
      item.closest('.faq-list')?.querySelectorAll('.faq-item.open').forEach((el) => {
        if (el !== item) el.classList.remove('open');
      });
      item.classList.toggle('open', !open);
    });
  });
})();

// WhatsApp bar — visibile al reload; se chiusa, riappare dopo 2 minuti
(function () {
  const WA_REOPEN_MS = 2 * 60 * 1000;
  const LEGACY_KEY = 'abra_wa_bar_closed';
  const WA_SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="#fff" style="flex-shrink:0"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>';

  let reopenTimer = null;

  function waBarHtml() {
    return `<div class="wa-bar" id="wa-bar">
    <p>Vuoi ricevere più informazioni?</p>
    <a href="https://wa.me/393408592926" target="_blank" rel="noopener" class="wa-btn">${WA_SVG} Contattaci su WhatsApp</a>
    <button class="wa-bar-close" id="wa-bar-close" aria-label="Chiudi">&times;</button>
  </div>`;
  }

  function showWaBar(bar) {
    bar.style.display = '';
    document.body.classList.add('has-wa-bar');
  }

  function hideWaBar(bar) {
    bar.style.display = 'none';
    document.body.classList.remove('has-wa-bar');
    clearTimeout(reopenTimer);
    reopenTimer = setTimeout(() => showWaBar(bar), WA_REOPEN_MS);
  }

  function initWaBar() {
    try { localStorage.removeItem(LEGACY_KEY); } catch (e) { /* ignore */ }

    let bar = document.getElementById('wa-bar');
    if (!bar) {
      document.body.insertAdjacentHTML('beforeend', waBarHtml());
      bar = document.getElementById('wa-bar');
    }
    if (!bar || bar.dataset.waInit === '1') return;
    bar.dataset.waInit = '1';

    showWaBar(bar);

    const closeBtn = document.getElementById('wa-bar-close');
    if (closeBtn) closeBtn.addEventListener('click', () => hideWaBar(bar));

    bar.addEventListener('mousemove', (e) => {
      const r = bar.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width) * 100;
      const y = ((e.clientY - r.top) / r.height) * 100;
      const angle = Math.atan2(e.clientY - (r.top + r.height / 2), e.clientX - (r.left + r.width / 2)) * (180 / Math.PI);
      bar.style.setProperty('--wa-mx', `${x}%`);
      bar.style.setProperty('--wa-my', `${y}%`);
      bar.style.setProperty('--wa-angle', `${angle}deg`);
    });
    bar.addEventListener('mouseleave', () => {
      bar.style.setProperty('--wa-mx', '50%');
      bar.style.setProperty('--wa-my', '50%');
      bar.style.setProperty('--wa-angle', '0deg');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWaBar);
  } else {
    initWaBar();
  }
})();

// Cookie / privacy informational notice (technical cookies only)
(function () {
  const KEY = 'abra_cookie_notice';
  try {
    if (localStorage.getItem(KEY) === 'ok') return;
  } catch (e) { /* localStorage non disponibile: mostra comunque l'avviso */ }

  // Risolvi il percorso della cookie policy (le pagine in /prodotti/ sono in sottocartella)
  const prefix = window.location.pathname.includes('/prodotti/') ? '../' : '';

  const banner = document.createElement('div');
  banner.className = 'cookie-banner';
  banner.setAttribute('role', 'region');
  banner.setAttribute('aria-label', 'Avviso cookie');
  banner.innerHTML = `
    <p>Questo sito utilizza solo cookie e strumenti tecnici necessari al suo funzionamento. Non usiamo cookie di profilazione. Maggiori informazioni nella <a href="${prefix}cookie-policy.html">Cookie Policy</a>.</p>
    <div class="cookie-actions">
      <button type="button" class="cookie-accept">Ho capito</button>
    </div>
  `;
  document.body.appendChild(banner);

  banner.querySelector('.cookie-accept').addEventListener('click', () => {
    try { localStorage.setItem(KEY, 'ok'); } catch (e) { /* ignora */ }
    banner.remove();
  });
})();

// Pageview beacon (first-party stats → Apps Script; una volta per sessione/pagina)
(function () {
  if (location.pathname.includes('/admin/')) return;
  if (location.protocol === 'file:') return;
  var url = (window.GOOGLE_SCRIPT_URL || '').trim();
  if (!url) return;
  var sessKey = 'abra_pv_' + location.pathname;
  try {
    if (sessionStorage.getItem(sessKey)) return;
    sessionStorage.setItem(sessKey, '1');
  } catch (_) {}
  var params = new URLSearchParams(location.search);
  var ref = '';
  try { ref = document.referrer || ''; } catch (_) {}
  try {
    fetch(url, {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: 'pageview',
        path: location.pathname + location.search,
        referrer: ref,
        utm_source: params.get('utm_source') || '',
        utm_medium: params.get('utm_medium') || '',
        utm_campaign: params.get('utm_campaign') || '',
        lang: document.documentElement.lang || 'it',
        mobile: /Mobi|Android/i.test(navigator.userAgent),
        timestamp: new Date().toISOString()
      })
    });
  } catch (_) {}
})();

// Assistente chat (KB offline + WhatsApp / modulo contatto)
(function () {
  if (location.pathname.includes('/admin/')) return;
  if (location.pathname.includes('/offerte-ai/')) return;
  if (document.querySelector('script[data-abra-chat-widget]')) return;

  var depth = 0;
  if (location.pathname.includes('/prodotti/')) depth = 1;
  if (location.pathname.includes('/en/')) depth = Math.max(depth, 1);
  if (location.pathname.includes('/en/prodotti/')) depth = 2;
  var prefix = depth ? '../'.repeat(depth) : '';

  var s = document.createElement('script');
  s.src = prefix + 'offerte-ai/js/widget.js?v=20260715g1';
  s.setAttribute('data-base', prefix + 'offerte-ai/');
  s.setAttribute('data-abra-chat-widget', '1');
  s.defer = true;
  document.body.appendChild(s);
})();
