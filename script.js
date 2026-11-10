// === Endpoint form (primario + secondario in parallelo) ===
// Primario — deployment live al 12 luglio 2026 (funzionante, foglio Niccolò 1nXl0…).
window.GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbw1WeoJYZltyorwQ-8Nftg0DdiOXOV-Zl3MlRegJS2ybhAzaRaqZNpTRamEbHJe2NtK/exec';
// Secondario — DISABILITATO (2026-08-10): POST fallisce con "autorizzazione documento".
// Redeploy Code.gs + condividi foglio 15zvBH… con gio@, poi ripristina l'URL sotto.
// window.GOOGLE_SCRIPT_URL_SECONDARY = 'https://script.google.com/macros/s/AKfycbxPPfh3qZRF0GwnKJicY5rcgdMSRoW_liBenRQValdCPSCM2MrZR_Y6fwrAZOHgCrDW/exec';
window.GOOGLE_SCRIPT_URL_SECONDARY = '';
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

// reCAPTCHA (~360 KB) solo quando qualcuno inizia a compilare un modulo:
// non rallenta pagine e Core Web Vitals di chi non scrive nulla.
(function loadRecaptcha() {
  if (!RECAPTCHA_SITE_KEY) return;
  let loaded = false;
  function load() {
    if (loaded) return;
    loaded = true;
    const s = document.createElement('script');
    s.src = 'https://www.google.com/recaptcha/api.js?render=' + RECAPTCHA_SITE_KEY;
    s.async = true;
    document.head.appendChild(s);
  }
  ['focusin', 'pointerdown', 'touchstart'].forEach((ev) => {
    document.addEventListener(ev, (e) => {
      if (e.target && e.target.closest && e.target.closest('form')) load();
    }, { passive: true });
  });
  // Carica anche quando un modulo entra in vista: il token è pronto prima del clic su "Invia".
  const forms = document.querySelectorAll('.contact-form, .quote-form-top');
  if (forms.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      if (entries.some((en) => en.isIntersecting)) { load(); io.disconnect(); }
    }, { rootMargin: '400px' });
    forms.forEach((f) => io.observe(f));
  }
})();

// Token reCAPTCHA con tempo massimo: se Google è lento o bloccato, il lead parte comunque.
function getRecaptchaToken(action, ms) {
  if (!RECAPTCHA_SITE_KEY || !window.grecaptcha) return Promise.resolve('');
  const token = new Promise((resolve) => {
    try {
      window.grecaptcha.ready(() => {
        window.grecaptcha.execute(RECAPTCHA_SITE_KEY, { action }).then(resolve, () => resolve(''));
      });
    } catch (_) { resolve(''); }
  });
  return Promise.race([token, new Promise((resolve) => setTimeout(() => resolve(''), ms))]);
}

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
    : (isEn ? 'Message sent! We will usually get back to you within 12 business hours.' : 'Messaggio inviato! Ti contattiamo di norma entro 12 ore lavorative.');
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

    const token = await getRecaptchaToken('contact', 4000);
    if (token) payload.recaptcha_token = token;

    try {
      await postLeadToGoogleScripts(payload);
      if (window.AbraAds && window.AbraAds.trackLead) window.AbraAds.trackLead();
      if (window.gtag) gtag('event', 'generate_lead', { form_id: form.id || form.className.split(' ')[0] || 'form', page_path: location.pathname });
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
    ? 'We will usually get back to you within 12 business hours.'
    : 'Ti ricontattiamo di norma entro 12 ore lavorative.';
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

  const isMenuOpen = () => mobileMenu.style.display === 'flex';
  const setMenu = (open) => {
    mobileMenu.style.display = open ? 'flex' : 'none';
    menuToggle.classList.toggle('active', open);
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Chiudi menu' : 'Menu');
    document.body.classList.toggle('menu-open', open);
  };

  // Pulsante "Chiudi" in cima al menu (aggiunto qui: vale per tutte le pagine)
  const closeBtn = document.createElement('button');
  closeBtn.type = 'button';
  closeBtn.className = 'mobile-menu-close';
  closeBtn.setAttribute('aria-label', 'Chiudi menu');
  closeBtn.innerHTML = '<span aria-hidden="true">✕</span> Chiudi';
  closeBtn.addEventListener('click', () => setMenu(false));
  mobileMenu.prepend(closeBtn);

  menuToggle.addEventListener('click', () => setMenu(!isMenuOpen()));

  // Close mobile menu on link click
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => setMenu(false));
  });

  // Chiudi toccando fuori dal menu (senza attivare quello che c'e' sotto), con Esc o allargando la finestra
  document.addEventListener('click', (e) => {
    if (!isMenuOpen() || mobileMenu.contains(e.target) || menuToggle.contains(e.target)) return;
    e.preventDefault();
    e.stopPropagation();
    setMenu(false);
  }, true);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isMenuOpen()) { setMenu(false); menuToggle.focus(); }
  });
  window.addEventListener('resize', () => {
    if (isMenuOpen() && window.innerWidth > 1024) setMenu(false);
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
if (navbar) window.addEventListener('scroll', () => {
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

// Contatti: ogni clic su WhatsApp, prenotazione, modulo, telefono o mail va in Analytics (contact_click) e Meta Pixel.
// I link WhatsApp senza testo ricevono un messaggio già scritto con la pagina e "(rif. SITO)": il CRM li riconosce.
const ABRA_WA_NUMBER = '393408592926';
const ABRA_CALL_URL = 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ22FrpPdyPVRihi4eXPQlljTcG2toa8XF2d8W-QX-L9cKMaXqozq_YsHym56LEdTs9WsnqlTHeF';
function abraIsIt() { return (document.documentElement.lang || 'it').slice(0, 2) === 'it'; }
function abraWaText() {
  const h1 = document.querySelector('h1');
  let page = ((h1 && h1.textContent) || (document.title || '').split(/\s[|–—]\s|\s-\s/)[0]).replace(/\s+/g, ' ').trim();
  if (page.length > 60) page = page.slice(0, 60).replace(/\s+\S*$/, '') + '…';
  return abraIsIt()
    ? `Ciao Abra Robotics, vi scrivo dal sito${page ? ` (pagina: ${page})` : ''}. (rif. SITO)`
    : `Hi Abra Robotics, I'm writing from your website${page ? ` (page: ${page})` : ''}. (rif. SITO)`;
}
function abraWaLink() { return `https://wa.me/${ABRA_WA_NUMBER}?text=${encodeURIComponent(abraWaText())}`; }
document.addEventListener('click', (e) => {
  const el = e.target.closest('a, button');
  if (!el) return;
  const href = el.getAttribute('href') || '';
  const txt = el.textContent.trim().toLowerCase();
  let method = el.dataset.contact || null;
  if (!method) {
    if (el.classList.contains('wa-btn') || /wa\.me\//.test(href)) method = 'whatsapp';
    else if (/calendar\.google\.com\/calendar\/appointments/.test(href)) method = 'call';
    else if (/^tel:/.test(href)) method = 'phone';
    else if (/^mailto:/.test(href)) method = 'email';
    else if (txt.includes('prenota') || txt.includes('chiama') || txt.includes('book a call')) method = 'call';
  }
  if (!method) return;
  if (method === 'whatsapp' && new RegExp(`wa\\.me/${ABRA_WA_NUMBER}(?![0-9])`).test(href) && !/[?&]text=/.test(href)) {
    el.setAttribute('href', abraWaLink());
  }
  const placement = el.closest('#wa-bar') ? 'barra' : el.closest('[class*="abra-cw"]') ? 'chat' : 'pagina';
  if (window.gtag) gtag('event', 'contact_click', { contact_method: method, contact_placement: placement, page_path: location.pathname });
  if (window.fbq) {
    const name = { whatsapp: 'whatsapp', call: 'prenota_chiamata', form: 'modulo', phone: 'telefono', email: 'email' }[method];
    if (name) fbq('track', 'Contact', { content_name: name });
  }
}, true);

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

// Barra contatti: compare solo quando si scorre verso l'alto (oltre la prima schermata), vetro scuro trasparente con
// sfocatura leggera; tre strade: WhatsApp, prenota una call, modulo. Si chiude con la X e resta chiusa per la visita.
// Tiene l'id "wa-bar" (le pagine lo hanno già nell'HTML e la chat lo usa per non sovrapporsi).
(function () {
  const CLOSED_KEY = 'abra_dock_closed';
  const ICON = {
    whatsapp: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.47-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.08-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.28-.2-.57-.35M12.05 21.79h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 7c0 5.45-4.44 9.88-9.88 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.69 1.45c6.55 0 11.89-5.34 11.89-11.9 0-3.17-1.24-6.16-3.48-8.4"/></svg>',
    call: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" d="M7 3v3M17 3v3M4 9h16M5 5h14a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1z"/></svg>',
    form: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" d="M4 6h16v12H4zM4 7l8 6 8-6"/></svg>',
  };
  const CSS = `
#wa-bar.contact-dock{position:fixed;left:50%;bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:9000;display:flex;align-items:center;gap:6px;
  padding:6px 6px 6px 18px;border-radius:999px;background:rgba(14,14,14,.68);-webkit-backdrop-filter:blur(14px) saturate(160%);backdrop-filter:blur(14px) saturate(160%);
  border:1px solid rgba(255,255,255,.14);box-shadow:0 10px 30px rgba(0,0,0,.18);color:#fff;font:500 14px/1 Geist,Satoshi,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  transform:translate(-50%,calc(100% + 30px));opacity:0;visibility:hidden;transition:transform .35s cubic-bezier(.2,.8,.2,1),opacity .25s ease,visibility 0s linear .35s}
#wa-bar.contact-dock.on{transform:translate(-50%,0);opacity:1;visibility:visible;transition:transform .35s cubic-bezier(.2,.8,.2,1),opacity .25s ease}
#wa-bar .cd-label{color:rgba(255,255,255,.88);margin-right:6px;white-space:nowrap}
#wa-bar .cd-btn{display:inline-flex;align-items:center;justify-content:center;gap:7px;height:38px;padding:0 15px;border-radius:999px;color:#fff;text-decoration:none;white-space:nowrap;
  background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.14);font:inherit;cursor:pointer;transition:background .2s}
#wa-bar .cd-btn:hover{background:rgba(255,255,255,.2)}
#wa-bar .cd-btn svg{width:17px;height:17px;flex:none}
#wa-bar .cd-short{display:none}
#wa-bar .cd-wa svg{color:#5fe39a}
#wa-bar .cd-close{width:32px;height:32px;margin-left:2px;border:0;border-radius:50%;background:transparent;color:rgba(255,255,255,.7);font:400 20px/1 sans-serif;cursor:pointer}
#wa-bar .cd-close:hover{color:#fff;background:rgba(255,255,255,.1)}
@media (max-width:600px){
  #wa-bar.contact-dock{left:10px;right:10px;padding:6px;gap:6px;transform:translateY(calc(100% + 30px))}
  #wa-bar.contact-dock.on{transform:none}
  #wa-bar .cd-label{display:none}
  #wa-bar .cd-btn{flex:1 1 0;min-width:0;height:44px;padding:0 6px;gap:6px;font-size:14px}
  #wa-bar .cd-btn svg{width:16px;height:16px}
  #wa-bar .cd-long{display:none}
  #wa-bar .cd-short{display:inline}
  #wa-bar .cd-close{width:28px;flex:none}
}
@media (prefers-reduced-motion:reduce){#wa-bar.contact-dock,#wa-bar.contact-dock.on{transition:none}}`;

  function dockHtml() {
    const it = abraIsIt();
    return `<span class="cd-label">${it ? 'Parliamone:' : "Let's talk:"}</span>
<a class="cd-btn cd-wa wa-btn" data-contact="whatsapp" href="${abraWaLink()}" target="_blank" rel="noopener">${ICON.whatsapp}<span>WhatsApp</span></a>
<a class="cd-btn cd-call" data-contact="call" href="${ABRA_CALL_URL}" target="_blank" rel="noopener">${ICON.call}<span class="cd-long">${it ? 'Prenota una call' : 'Book a call'}</span><span class="cd-short">Call</span></a>
<a class="cd-btn cd-form" data-contact="form" href="${it ? '/#contatti' : '/en/index-en.html#contatti'}">${ICON.form}<span class="cd-long">${it ? 'Scrivici' : 'Write to us'}</span><span class="cd-short">${it ? 'Scrivici' : 'Write'}</span></a>
<button class="cd-close" type="button" aria-label="${it ? 'Chiudi' : 'Close'}">&times;</button>`;
  }

  function init() {
    let closed = false;
    try { closed = sessionStorage.getItem(CLOSED_KEY) === '1'; } catch (e) { /* storage non disponibile */ }
    let bar = document.getElementById('wa-bar');
    if (!bar) {
      bar = document.createElement('div');
      bar.id = 'wa-bar';
      document.body.appendChild(bar);
    }
    if (bar.dataset.dock === '1') return;
    bar.dataset.dock = '1';
    if (!document.getElementById('contact-dock-css')) {
      const st = document.createElement('style');
      st.id = 'contact-dock-css';
      st.textContent = CSS;
      document.head.appendChild(st);
    }
    bar.className = 'contact-dock';
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', abraIsIt() ? 'Contatti' : 'Contact');
    bar.innerHTML = dockHtml();
    document.body.classList.remove('has-wa-bar');
    if (closed) return;

    // Il modulo: se è nella pagina ci si scorre sopra, altrimenti si va a quello della home.
    const form = document.querySelector('.contact-form, .quote-form-top');
    bar.querySelector('.cd-form').addEventListener('click', (e) => {
      if (!form) return;
      e.preventDefault();
      form.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setTimeout(() => { const f = form.querySelector('input:not([type=hidden]), textarea'); if (f) f.focus({ preventScroll: true }); }, 700);
    });

    let shown = false, formInView = false, lastY = window.scrollY, ticking = false;
    const relayout = () => window.dispatchEvent(new Event('resize')); // la chat ricalcola la sua posizione
    function set(on) {
      if (on === shown) return;
      shown = on;
      bar.classList.toggle('on', on);
      setTimeout(relayout, 380);
    }
    function consentOpen() { const c = document.querySelector('.consent-banner'); return !!(c && c.offsetParent !== null); }
    function update() {
      ticking = false;
      const y = window.scrollY, d = y - lastY;
      if (Math.abs(d) < 6) return;
      lastY = y;
      if (d < 0 && y > window.innerHeight * 0.6 && !formInView && !consentOpen()) set(true);
      else if (d > 0 || y < 120) set(false);
    }
    window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    if (form && 'IntersectionObserver' in window) {
      new IntersectionObserver((en) => { formInView = en.some((x) => x.isIntersecting); if (formInView) set(false); }, { threshold: 0.15 }).observe(form);
    }
    bar.querySelector('.cd-close').addEventListener('click', () => {
      set(false);
      try { sessionStorage.setItem(CLOSED_KEY, '1'); } catch (e) { /* ignore */ }
      setTimeout(() => { bar.style.display = 'none'; relayout(); }, 400);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

// Cookie / privacy informational notice (technical cookies only)
// Avviso cookie sostituito dal banner di consenso (consent.js).

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
  if (location.pathname.includes('/prodotti/') || location.pathname.includes('/blog/')) depth = 1;
  if (location.pathname.includes('/en/')) depth = Math.max(depth, 1);
  if (location.pathname.includes('/en/prodotti/') || location.pathname.includes('/en/blog/')) depth = 2;
  // Versioni estere (/de/, /fr/, ...): una cartella in piu', due per il loro blog
  var lang = /^\/(de|fr|es|nl|da|sv|no|fi|pl|cs|uk)\//.exec(location.pathname);
  if (lang) depth = location.pathname.indexOf('/blog/') >= 0 ? 2 : 1;
  var prefix = depth ? '../'.repeat(depth) : '';

  var s = document.createElement('script');
  s.src = prefix + 'offerte-ai/js/widget.js?v=20261110';
  s.setAttribute('data-base', prefix + 'offerte-ai/');
  s.setAttribute('data-abra-chat-widget', '1');
  s.defer = true;
  // Dopo il load + idle: widget, CSS e immagini della chat non competono con il primo rendering (LCP mobile).
  function inject() { document.body.appendChild(s); }
  function schedule() {
    if ('requestIdleCallback' in window) requestIdleCallback(inject, { timeout: 3000 });
    else setTimeout(inject, 1);
  }
  if (document.readyState === 'complete') schedule();
  else window.addEventListener('load', schedule, { once: true });
})();

// reCAPTCHA v3: il badge è nascosto via CSS, quindi la nota va mostrata sotto ogni modulo con email
(function addRecaptchaNote() {
  if (!RECAPTCHA_SITE_KEY) return;
  const en = window.location.pathname.includes('/en/');
  const text = en
    ? 'Protected by reCAPTCHA: Google <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Privacy Policy</a> and <a href="https://policies.google.com/terms" target="_blank" rel="noopener">Terms</a> apply.'
    : 'Protetto da reCAPTCHA: si applicano la <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Privacy Policy</a> e i <a href="https://policies.google.com/terms" target="_blank" rel="noopener">Termini</a> di Google.';
  function run() {
    document.querySelectorAll('form').forEach(f => {
      if (!f.querySelector('input[type="email"]') || f.querySelector('.recaptcha-note')) return;
      const p = document.createElement('p');
      p.className = 'recaptcha-note';
      p.innerHTML = text;
      f.appendChild(p);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();

// Articoli del blog: barra di avanzamento in cima con i minuti che mancano alla fine.
// Se il browser ha fatto l'accesso all'editor (/editor/), compare anche "Modifica".
(function articleReadingProgress() {
  function run() {
    const content = document.querySelector('.article-content');
    if (!content) return;
    const words = (content.innerText || '').trim().split(/\s+/).length;
    const totalMin = Math.max(1, Math.round(words / 200));
    const bar = document.createElement('div');
    bar.className = 'read-progress';
    bar.setAttribute('role', 'progressbar');
    bar.setAttribute('aria-label', 'Avanzamento lettura');
    bar.setAttribute('aria-valuemin', '0');
    bar.setAttribute('aria-valuemax', '100');
    bar.innerHTML = '<div class="read-progress-fill"></div><span class="read-progress-label"></span>';
    document.body.appendChild(bar);
    const fill = bar.firstChild;
    const label = bar.lastChild;
    let ticking = false;
    function update() {
      ticking = false;
      const rect = content.getBoundingClientRect();
      const start = rect.top + window.scrollY - window.innerHeight * 0.25;
      const end = rect.bottom + window.scrollY - window.innerHeight;
      const p = Math.min(1, Math.max(0, (window.scrollY - start) / Math.max(1, end - start)));
      fill.style.transform = 'scaleX(' + p + ')';
      bar.setAttribute('aria-valuenow', String(Math.round(p * 100)));
      const left = Math.ceil(totalMin * (1 - p));
      label.textContent = p >= 0.99 ? 'Finito' : (left <= 1 ? 'Meno di 1 min alla fine' : left + ' min alla fine');
      bar.classList.toggle('is-visible', window.scrollY > 120);
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    update();

    let editorOn = false;
    try { editorOn = localStorage.getItem('abra-editor') === '1'; } catch (e) {}
    const m = location.pathname.match(/\/blog\/([a-z0-9-]+)\.html$/);
    if (editorOn && m) {
      const a = document.createElement('a');
      a.className = 'article-edit-btn';
      a.href = '/editor/?file=' + encodeURIComponent('blog/' + m[1] + '.html');
      a.textContent = 'Modifica articolo';
      document.body.appendChild(a);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();
