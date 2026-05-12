// Contact form → Google Sheets
// Replace this URL with your deployed Google Apps Script URL
const GOOGLE_SCRIPT_URL = 'INSERISCI_QUI_IL_TUO_URL_APPS_SCRIPT';

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
