// === ENDPOINT UNICO per TUTTI i form del sito ===
// Tutti i form (contatti home/pagine, box "Richiedi informazioni" sulle schede) inviano qui.
// Incolla l'URL del Web App Google Apps Script (vedi apps-script/README.md). Una sola riga da cambiare.
window.GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbyQHcWp5OFlAssEajk03akHm2T_JlxAf_-SwWkKP773dXIt0Q0WvAJ1HtNdKl5E54vc/exec';
const GOOGLE_SCRIPT_URL = window.GOOGLE_SCRIPT_URL;

const contactForm = document.getElementById('contact-form');
const formFeedback = document.getElementById('form-feedback');

if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = contactForm.querySelector('.form-submit');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Invio in corso...';
    formFeedback.className = 'form-feedback';
    formFeedback.textContent = '';

    const payload = Object.fromEntries(new FormData(contactForm).entries());
    payload.origine = payload.prodotto || 'Form contatti';
    payload.pagina = document.title;
    payload.url = location.href;
    payload.timestamp = new Date().toISOString();

    try {
      await fetch(GOOGLE_SCRIPT_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      formFeedback.className = 'form-feedback success';
      formFeedback.textContent = 'Messaggio inviato! Ti contatteremo entro 12 ore.';
      contactForm.reset();
    } catch {
      formFeedback.className = 'form-feedback error';
      formFeedback.textContent = 'Errore nell\'invio. Scrivi direttamente a info@abrarobotics.com.';
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Invia la richiesta';
    }
  });
}

// Mobile menu toggle
const menuToggle = document.querySelector('.menu-toggle');
const mobileMenu = document.querySelector('.mobile-menu');

menuToggle.addEventListener('click', () => {
  const isOpen = mobileMenu.style.display === 'flex';
  mobileMenu.style.display = isOpen ? 'none' : 'flex';
  menuToggle.classList.toggle('active');
});

// Close mobile menu on link click
mobileMenu.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    mobileMenu.style.display = 'none';
    menuToggle.classList.remove('active');
  });
});

// Mobile dropdown accordion
mobileMenu.querySelectorAll('.mobile-dropdown-trigger').forEach(trigger => {
  trigger.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    trigger.closest('.mobile-dropdown').classList.toggle('open');
  });
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

const animatedElements = document.querySelectorAll(
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
