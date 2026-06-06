# -*- coding: utf-8 -*-
"""Fragmenti HTML condivisi per pagine pubbliche catalogo/listino."""

SITE_NAV = """
  <div class="top-bar">
    <p>Listino pubblico End-User · IVA esclusa · <a href="listino-unitree.html">Tabella prezzi</a> · <a href="catalogo-unitree.html">Catalogo</a></p>
  </div>
  <nav class="navbar">
    <div class="container navbar-inner">
      <a href="index.html" class="logo"><img src="images/logo.png" alt="Abra Robotics" class="logo-img"></a>
      <div class="nav-links">
        <div class="nav-item-dropdown">
          <button class="nav-dropdown-trigger" type="button">Prodotti <span class="nav-caret">▾</span></button>
          <div class="nav-dropdown-panel">
            <a href="quadrupedi.html">Quadrupedi</a>
            <a href="umanoidi.html">Umanoidi G1</a>
            <a href="r1-d.html">R1-D Dual-Arm</a>
            <a href="accessori.html">Accessori</a>
            <a href="catalogo-unitree.html">Catalogo completo</a>
            <a href="listino-unitree.html">Listino prezzi</a>
          </div>
        </div>
        <a href="assessment.html">Trova il robot giusto</a>
        <a href="finanziamenti.html">Finanziamenti</a>
        <a href="index.html#chi-siamo">Chi siamo</a>
      </div>
      <a href="index.html#cta-finale" class="btn btn-primary btn-sm">Prenota una chiamata</a>
      <button class="menu-toggle" aria-label="Menu"><span></span><span></span></button>
    </div>
  </nav>
  <div class="mobile-menu">
    <a href="quadrupedi.html">Quadrupedi</a>
    <a href="umanoidi.html">Umanoidi G1</a>
    <a href="r1-d.html">R1-D Dual-Arm</a>
    <a href="accessori.html">Accessori</a>
    <a href="catalogo-unitree.html">Catalogo completo</a>
    <a href="listino-unitree.html">Listino prezzi</a>
    <a href="assessment.html">Trova il robot giusto</a>
    <a href="index.html#cta-finale" class="btn btn-primary">Prenota una chiamata</a>
  </div>
"""

SITE_FOOTER = """
  <footer class="footer">
    <div class="container footer-grid">
      <div class="footer-brand">
        <a href="index.html" class="logo"><img src="images/logo.png" alt="Abra Robotics" class="logo-img"></a>
        <p class="footer-desc">Distributore ufficiale Unitree in Italia. Prezzi End-User pubblici — prezzi Gold solo in area admin interna.</p>
      </div>
      <div class="footer-nav">
        <span class="footer-heading">Listini pubblici</span>
        <a href="catalogo-unitree.html">Catalogo completo</a>
        <a href="listino-unitree.html">Tabella prezzi</a>
      </div>
      <div class="footer-nav">
        <span class="footer-heading">Prodotti</span>
        <a href="umanoidi.html">Umanoidi G1</a>
        <a href="r1-d.html">R1-D Dual-Arm</a>
        <a href="quadrupedi.html">Quadrupedi</a>
        <a href="accessori.html">Accessori</a>
      </div>
      <div class="footer-contact">
        <span class="footer-heading">Contatti</span>
        <a href="mailto:info@abrarobotics.com">info@abrarobotics.com</a>
        <a href="index.html#cta-finale" class="btn btn-primary btn-sm">Prenota una chiamata</a>
      </div>
    </div>
    <div class="container footer-bottom">
      <p class="footer-copy">&copy; 2026 Abra Robotics. Listino End-User pubblico — non include prezzi distributore Gold.</p>
    </div>
  </footer>
"""

PUBLIC_NOTICE = """
    <p class="pub-notice" style="margin-top:12px;padding:12px 16px;background:var(--gray-50);border:1px solid var(--gray-200);border-radius:8px;font-size:0.88rem;color:var(--gray-600);max-width:720px;">
      <strong>Pagina pubblica.</strong> Mostra solo prezzi End-User (IVA esclusa, spedizione e dazio inclusi).
      I prezzi Gold distributore sono visibili solo in <code>admin/listini.html</code> (area interna, non indicizzata).
    </p>
"""
