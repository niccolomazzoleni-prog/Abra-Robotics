# -*- coding: utf-8 -*-
"""Navbar canonica condivisa — unica fonte di verità per tutte le pagine pubbliche."""


def render_site_nav(prefix: str = "") -> str:
    """Restituisce <nav> + <div class="mobile-menu"> con href relativi al prefisso."""
    p = prefix
    img = f"{p}images/logo.png"
    home = f"{p}index.html"
    return f"""  <!-- Navbar -->
  <nav class="navbar">
    <div class="container navbar-inner">
      <a href="{home}" class="logo"><img src="{img}" alt="Abra Robotics" class="logo-img"></a>
      <div class="nav-links">
        <div class="nav-item-dropdown">
          <button class="nav-dropdown-trigger" type="button">Prodotti <span class="nav-caret">▾</span></button>
          <div class="nav-dropdown-panel">
            <a href="{p}manifattura-logistica.html#cobot">Cobot</a>
            <a href="{p}catalogo-cobot.html">Catalogo cobot</a>
            <a href="{p}manifattura-logistica.html#amr">AMR</a>
            <a href="{p}quadrupedi.html">Quadrupedi</a>
            <a href="{p}umanoidi.html">Umanoidi</a>
            <a href="{p}accessori.html">Accessori</a>
            <a href="{p}catalogo-unitree.html">Catalogo completo</a>
            <a href="{p}listino-unitree.html">Listino prezzi</a>
          </div>
        </div>
        <a href="{p}assessment.html">Trova il robot giusto</a>
        <a href="{p}finanziamenti.html">Finanziamenti</a>
        <div class="nav-item-dropdown">
          <button class="nav-dropdown-trigger" type="button">Per chi <span class="nav-caret">▾</span></button>
          <div class="nav-dropdown-panel">
            <a href="{p}manifattura-logistica.html">Manifattura e Logistica</a>
            <a href="{p}universita-ricerca.html">Università e Ricerca</a>
          </div>
        </div>
        <a href="{home}#chi-siamo">Chi siamo</a>
      </div>
      <a href="{home}#cta-finale" class="btn btn-primary btn-sm">Prenota una chiamata</a>
      <button class="menu-toggle" aria-label="Menu">
        <span></span>
        <span></span>
      </button>
    </div>
  </nav>

  <!-- Mobile Menu -->
  <div class="mobile-menu">
    <div class="mobile-dropdown">
      <button class="mobile-dropdown-trigger" type="button">Prodotti <span class="nav-caret">▾</span></button>
      <div class="mobile-dropdown-panel">
        <a href="{p}manifattura-logistica.html#cobot">Cobot</a>
        <a href="{p}manifattura-logistica.html#amr">AMR</a>
        <a href="{p}quadrupedi.html">Quadrupedi</a>
        <a href="{p}umanoidi.html">Umanoidi</a>
        <a href="{p}accessori.html">Accessori</a>
        <a href="{p}catalogo-unitree.html">Catalogo completo</a>
        <a href="{p}listino-unitree.html">Listino prezzi</a>
      </div>
    </div>
    <a href="{p}assessment.html">Trova il robot giusto</a>
    <a href="{p}finanziamenti.html">Finanziamenti</a>
    <div class="mobile-dropdown">
      <button class="mobile-dropdown-trigger" type="button">Per chi <span class="nav-caret">▾</span></button>
      <div class="mobile-dropdown-panel">
        <a href="{p}manifattura-logistica.html">Manifattura e Logistica</a>
        <a href="{p}universita-ricerca.html">Università e Ricerca</a>
      </div>
    </div>
    <a href="{home}#chi-siamo">Chi siamo</a>
    <a href="{home}#cta-finale" class="btn btn-primary">Prenota una chiamata</a>
  </div>"""
