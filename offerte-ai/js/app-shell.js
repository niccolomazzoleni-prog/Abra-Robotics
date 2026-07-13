/**
 * Shell app condiviso: nav, toast, utilità UI.
 */
(function (global) {
  'use strict';

  function toast(msg, type = 'info') {
    let root = document.getElementById('abra-toast-root');
    if (!root) {
      root = document.createElement('div');
      root.id = 'abra-toast-root';
      root.className = 'abra-toast-root';
      document.body.appendChild(root);
    }
    const el = document.createElement('div');
    el.className = 'abra-toast abra-toast-' + type;
    el.textContent = msg;
    root.appendChild(el);
    requestAnimationFrame(() => el.classList.add('show'));
    setTimeout(() => { el.classList.remove('show'); setTimeout(() => el.remove(), 300); }, 3200);
  }

  function renderNav(active) {
    const isAdmin = active === 'admin';
    const navItems = isAdmin ? [
      { id: 'chat', label: 'Lab Training', href: '../offerte-ai/index.html' },
      { id: 'offerta', label: 'Crea offerta', href: '../offerte-ai/offerta.html' },
      { id: 'demo', label: 'Widget demo', href: '../offerte-ai/demo.html' },
      { id: 'admin', label: 'Admin', href: 'offerte-ai.html' },
    ] : [
      { id: 'chat', label: 'Lab Training', href: 'index.html' },
      { id: 'offerta', label: 'Crea offerta', href: 'offerta.html' },
      { id: 'demo', label: 'Widget demo', href: 'demo.html' },
      { id: 'admin', label: 'Admin', href: '../admin/offerte-ai.html' },
    ];
    const logoSrc = '../images/logo.png';
    const siteHref = isAdmin ? '../index.html' : '../index.html';
    return `<nav class="app-nav" aria-label="Sezioni">
      <a class="app-nav-brand" href="${siteHref}">
        <img src="${logoSrc}" alt="Abra Robotics" width="120" height="32">
      </a>
      <div class="app-nav-links">${navItems.map(i =>
        `<a href="${i.href}" class="app-nav-link${active === i.id ? ' active' : ''}">${i.label}</a>`
      ).join('')}<a href="${siteHref}" class="app-nav-link app-nav-link-site">← Sito</a></div>
    </nav>`;
  }

  function mountNav(active) {
    const mount = document.getElementById('app-nav-mount');
    if (mount) mount.innerHTML = renderNav(active);
  }

  function formatEuro(n) {
    return Number(n).toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  global.AbraUI = { toast, mountNav, renderNav, formatEuro };
})(typeof window !== 'undefined' ? window : globalThis);
