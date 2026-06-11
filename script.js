// === ENDPOINT UNICO per TUTTI i form del sito ===
// Tutti i form (contatti home/pagine, box "Richiedi informazioni" sulle schede) inviano qui.
// Incolla l'URL del Web App Google Apps Script (vedi apps-script/README.md). Una sola riga da cambiare.
window.GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbxLVHzIut6LZScnDY6RqOlCSVdEpSofmW21cNI9v_LeJZ-51o8ZJI0MRwI-kxwd0fZQ/exec';
const GOOGLE_SCRIPT_URL = window.GOOGLE_SCRIPT_URL;

document.querySelectorAll('.contact-form, .quote-form-top').forEach(form => {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = form.querySelector('.form-submit') || form.querySelector('[type="submit"]');
    const feedback = form.querySelector('.form-feedback') || form.querySelector('.quote-form-feedback');
    const origText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Invio in corso...';
    if (feedback) { feedback.className = feedback.className.split(' ')[0]; feedback.textContent = ''; }

    const payload = Object.fromEntries(new FormData(form).entries());
    payload.prodotto = payload.prodotto || form.dataset.product || '';
    payload.origine = payload.prodotto || 'Form contatti';
    payload.pagina = document.title;
    payload.url = location.href;
    payload.timestamp = new Date().toISOString();
    if (window.AbraAds && window.AbraAds.getGclid) {
      payload.gclid = payload.gclid || window.AbraAds.getGclid();
    }

    try {
      await fetch(GOOGLE_SCRIPT_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (feedback) { feedback.className = feedback.className.split(' ')[0] + ' success'; feedback.textContent = 'Messaggio inviato! Ti contatteremo entro 12 ore.'; }
      if (window.AbraAds && window.AbraAds.trackLead) window.AbraAds.trackLead();
      if (window.fbq) fbq('track', 'Lead');
      form.reset();
    } catch {
      if (feedback) { feedback.className = feedback.className.split(' ')[0] + ' error'; feedback.textContent = 'Errore nell\'invio. Scrivi direttamente a info@abrarobotics.com.'; }
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = origText;
    }
  });
});

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

// Visible class
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
    <p>${WA_SVG} Vuoi ricevere più informazioni?</p>
    <a href="https://wa.me/393408592926" target="_blank" rel="noopener" class="wa-btn">Contattaci su WhatsApp</a>
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
