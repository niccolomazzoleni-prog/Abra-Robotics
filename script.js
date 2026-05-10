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

// Fade-in animation on scroll
const observerOptions = {
  threshold: 0.15,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.card, .use-case, .step, .stat, .about-stat, .report-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
  observer.observe(el);
});

// Add visible class styles
document.head.insertAdjacentHTML('beforeend', `
  <style>
    .visible {
      opacity: 1 !important;
      transform: translateY(0) !important;
    }
  </style>
`);
