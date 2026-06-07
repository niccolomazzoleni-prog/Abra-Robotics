// === ENDPOINT UNICO per TUTTI i form del sito ===
// Tutti i form (contatti home/pagine, box "Richiedi informazioni" sulle schede) inviano qui.
// Incolla l'URL del Web App Google Apps Script (vedi apps-script/README.md). Una sola riga da cambiare.
window.GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbyQHcWp5OFlAssEajk03akHm2T_JlxAf_-SwWkKP773dXIt0Q0WvAJ1HtNdKl5E54vc/exec';
const GOOGLE_SCRIPT_URL = window.GOOGLE_SCRIPT_URL;

document.querySelectorAll('.contact-form').forEach(form => {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = form.querySelector('.form-submit');
    const feedback = form.querySelector('.form-feedback');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Invio in corso...';
    feedback.className = 'form-feedback';
    feedback.textContent = '';

    const payload = Object.fromEntries(new FormData(form).entries());
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
      feedback.className = 'form-feedback success';
      feedback.textContent = 'Messaggio inviato! Ti contatteremo entro 12 ore.';
      if (window.AbraAds && window.AbraAds.trackLead) window.AbraAds.trackLead();
      form.reset();
    } catch {
      feedback.className = 'form-feedback error';
      feedback.textContent = 'Errore nell\'invio. Scrivi direttamente a info@abrarobotics.com.';
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Invia la richiesta';
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
