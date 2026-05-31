/* ──────────────────────────────────────────────
   Shared product-page behaviour (Abra Robotics)
   Used by every Unitree humanoid product page.
   Gallery reads image sources from the thumbnails
   in the DOM, so no per-page image array is needed.
─────────────────────────────────────────────── */

/* ── Gallery Slider ── */
(function () {
  const mainImg = document.getElementById('gallery-main-img');
  const thumbs = Array.from(document.querySelectorAll('.gallery-thumb'));
  if (!mainImg || !thumbs.length) return;

  const images = thumbs.map(t => t.querySelector('img').getAttribute('src'));
  let current = 0;

  function setImage(index) {
    current = (index + images.length) % images.length;
    mainImg.classList.add('fade');
    setTimeout(() => {
      mainImg.src = images[current];
      mainImg.classList.remove('fade');
    }, 150);
    thumbs.forEach((t, i) => t.classList.toggle('active', i === current));
  }

  const prev = document.getElementById('gallery-prev');
  const next = document.getElementById('gallery-next');
  if (prev) prev.addEventListener('click', () => setImage(current - 1));
  if (next) next.addEventListener('click', () => setImage(current + 1));
  thumbs.forEach((t, i) => t.addEventListener('click', () => setImage(i)));
})();

/* ── Animated Counters ── */
(function () {
  function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }
  function animateCounter(el, target, duration) {
    const start = performance.now();
    (function update(now) {
      const p = Math.min((now - start) / duration, 1);
      el.textContent = Math.round(easeOutCubic(p) * target);
      if (p < 1) requestAnimationFrame(update);
      else el.textContent = target;
    })(performance.now());
  }
  const statsEl = document.getElementById('stats-section');
  if (!statsEl) return;
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.querySelectorAll('.counter').forEach(c =>
        animateCounter(c, parseInt(c.dataset.target, 10), 1800)
      );
      obs.unobserve(entry.target);
    });
  }, { threshold: 0.5 });
  obs.observe(statsEl);
})();

/* ── Parallax Collage ── */
(function () {
  const colA = document.getElementById('parallax-col-a');
  const colB = document.getElementById('parallax-col-b');
  const container = document.getElementById('parallax-container');
  if (!colA || !colB || window.matchMedia('(max-width: 768px)').matches) return;

  let ticking = false;
  window.addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const center = container.getBoundingClientRect().top + container.offsetHeight / 2 - window.innerHeight / 2;
      colA.style.transform = `translateY(${center * -0.06}px)`;
      colB.style.transform = `translateY(${40 + center * -0.03}px)`;
      ticking = false;
    });
  }, { passive: true });
})();

/* ── Lazy Video Autoplay ── */
(function () {
  const videos = document.querySelectorAll('.feature-video[data-src]');
  if (!videos.length) return;
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const video = entry.target;
      const poster = video.nextElementSibling;
      if (entry.isIntersecting) {
        if (!video.src) { video.src = video.dataset.src; video.load(); }
        video.play().then(() => { if (poster) poster.classList.add('hidden'); }).catch(() => {});
      } else {
        video.pause();
      }
    });
  }, { threshold: 0.4 });
  videos.forEach(v => obs.observe(v));
})();

/* ── Scroll fade-in ── */
(function () {
  const els = document.querySelectorAll('.feature-card, .product-stat, .step, .parallax-img-wrap, .key-spec, .spec-mini-card, .comp-model-card');
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('visible'); obs.unobserve(entry.target); }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  els.forEach((el) => {
    const siblings = Array.from(el.parentElement.children).filter(c => c.classList[0] === el.classList[0]);
    const idx = siblings.indexOf(el);
    el.style.opacity = '0';
    el.style.transform = 'translateY(24px)';
    el.style.transition = `opacity 0.6s ease ${idx * 0.1}s, transform 0.6s ease ${idx * 0.1}s`;
    obs.observe(el);
  });
})();
