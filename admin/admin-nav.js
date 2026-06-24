/** Nav admin condivisa — mount su #admin-nav-mount con AbraAdminNav.mount('stats') */
(function () {
  'use strict';

  const LINKS = [
    { id: 'home', href: 'index.html', label: 'Home' },
    { id: 'stats', href: 'statistiche.html', label: 'Statistiche' },
    { id: 'listini', href: 'listini.html', label: 'Listini' },
    { id: 'immagini', href: 'immagini.html', label: 'Immagini' },
    { id: 'knowledge', href: 'knowledge.html', label: 'Knowledge' },
    { id: 'offerte', href: 'offerte-ai.html', label: 'Offerte AI' },
  ];

  function mount(activeId) {
    const el = document.getElementById('admin-nav-mount');
    if (!el) return;
    el.innerHTML = `<nav class="admin-nav" aria-label="Admin">
      ${LINKS.map((l) =>
        `<a href="${l.href}" class="${activeId === l.id ? 'is-active' : ''}">${l.label}</a>`
      ).join('')}
      <span class="spacer"></span>
      <a href="../offerte-ai/index.html" class="admin-nav-ext">Lab</a>
      <button type="button" class="btn btn-secondary btn-sm" onclick="AbraAdmin.logout()">Esci</button>
    </nav>`;
  }

  window.AbraAdminNav = { mount, links: LINKS };
})();
