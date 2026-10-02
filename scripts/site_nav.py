# -*- coding: utf-8 -*-
"""Navbar canonica condivisa — unica fonte di verità per tutte le pagine pubbliche."""


def render_top_bar(prefix: str = "", message: str | None = None) -> str:
    """Barra promozionale fissa sopra la navbar."""
    p = prefix
    if message is None:
        message = (
            f'La maggior parte dei progetti è finanziabile. '
            f'<a href="{p}finanziamenti.html">Scopri come →</a>'
        )
    return f"""  <div class="top-bar">
    <p>{message}</p>
  </div>"""


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
            <a href="{p}cobot.html">Cobot</a>
            <a href="{p}amr.html">AMR</a>
            <a href="{p}quadrupedi.html">Quadrupedi</a>
            <a href="{p}umanoidi.html">Umanoidi</a>
            <a href="{p}accessori.html">Accessori</a>
            <a href="{p}catalogo.html">Catalogo completo</a>
            <a href="{p}listino-unitree.html">Listino prezzi</a>
          </div>
        </div>
        <a href="{p}listino-unitree.html">Prezzi</a>
        <a href="{p}assessment.html">Trova il robot giusto</a>
        <a href="{p}finanziamenti.html">Finanziamenti</a>
        <a href="{p}blog.html">Blog</a>
        <div class="nav-item-dropdown">
          <button class="nav-dropdown-trigger" type="button">Per chi <span class="nav-caret">▾</span></button>
          <div class="nav-dropdown-panel">
            <a href="{p}manifattura-logistica.html">Manifattura e Logistica</a>
            <a href="{p}universita-ricerca.html">Università e Ricerca</a>
          </div>
        </div>
        <a href="{p}chi-siamo.html">Chi siamo</a>
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
        <a href="{p}cobot.html">Cobot</a>
        <a href="{p}amr.html">AMR</a>
        <a href="{p}quadrupedi.html">Quadrupedi</a>
        <a href="{p}umanoidi.html">Umanoidi</a>
        <a href="{p}accessori.html">Accessori</a>
        <a href="{p}catalogo.html">Catalogo completo</a>
        <a href="{p}listino-unitree.html">Listino prezzi</a>
      </div>
    </div>
    <a href="{p}listino-unitree.html">Prezzi</a>
    <a href="{p}assessment.html">Trova il robot giusto</a>
    <a href="{p}finanziamenti.html">Finanziamenti</a>
    <a href="{p}blog.html">Blog</a>
    <div class="mobile-dropdown">
      <button class="mobile-dropdown-trigger" type="button">Per chi <span class="nav-caret">▾</span></button>
      <div class="mobile-dropdown-panel">
        <a href="{p}manifattura-logistica.html">Manifattura e Logistica</a>
        <a href="{p}universita-ricerca.html">Università e Ricerca</a>
      </div>
    </div>
    <a href="{p}chi-siamo.html">Chi siamo</a>
    <a href="{home}#cta-finale" class="btn btn-primary">Prenota una chiamata</a>
  </div>"""


def render_site_chrome(prefix: str = "", top_message: str | None = None) -> str:
    """Top bar + navbar + mobile menu."""
    return render_top_bar(prefix, top_message) + "\n\n" + render_site_nav(prefix)


def render_site_footer(prefix: str = "") -> str:
    """Footer unico del sito italiano (sostituito in tutte le pagine tranne le landing lp-*)."""
    p = prefix
    cal = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ22FrpPdyPVRihi4eXPQlljTcG2toa8XF2d8W-QX-L9cKMaXqozq_YsHym56LEdTs9WsnqlTHeF"
    return f"""<footer class="footer">
<div class="container footer-grid">
<div class="footer-brand">
<a class="logo" href="{p}index.html"><img alt="Abra Robotics" class="logo-img" src="{p}images/logo.png" width="180" height="72" decoding="async"/></a>
<p class="footer-desc">Robotica applicata per aziende, università e istituti di ricerca. Hardware, software su misura, formazione e supporto tecnico dedicato.</p>
</div>
<div class="footer-nav">
<span class="footer-heading">Prodotti</span>
<a href="{p}cobot.html">Cobot</a>
<a href="{p}amr.html">AMR</a>
<a href="{p}quadrupedi.html">Quadrupedi</a>
<a href="{p}umanoidi.html">Umanoidi</a>
<a href="{p}accessori.html">Accessori</a>
<a href="{p}catalogo.html">Catalogo completo</a>
<a href="{p}listino-unitree.html">Listino prezzi</a>
</div>
<div class="footer-nav">
<span class="footer-heading">Servizi e risorse</span>
<a href="{p}assessment.html">Trova il robot giusto</a>
<a href="{p}software.html">Software</a>
<a href="{p}finanziamenti.html">Finanziamenti</a>
<a href="{p}manifattura-logistica.html">Manifattura e Logistica</a>
<a href="{p}universita-ricerca.html">Università e Ricerca</a>
<a href="{p}blog.html">Blog</a>
</div>
<div class="footer-contact">
<span class="footer-heading">Contatti</span>
<a href="{p}chi-siamo.html">Chi siamo</a>
<a href="mailto:info@abrarobotics.com">info@abrarobotics.com</a>
<p>Viale Trieste 105<br/>30026 Portogruaro (VE)</p>
<a class="btn btn-primary btn-sm" href="{cal}" rel="noopener noreferrer" target="_blank">Prenota una chiamata</a>
</div>
</div>
<div class="container footer-bottom">
<p class="footer-copy">© 2026 Abra Robotics di Niccolò Mazzoleni. Tutti i diritti riservati. P.IVA 04800170278 — Portogruaro (VE).</p>
<nav aria-label="Note legali" class="footer-legal">
<a href="{p}privacy-policy.html">Privacy Policy</a>
<a href="{p}cookie-policy.html">Cookie Policy</a>
<a href="{p}condizioni-di-vendita.html">Condizioni di vendita</a>
<a href="{p}politica-resi.html">Politica resi</a>
<a href="{p}note-legali.html">Note legali</a>
</nav>
</div>
</footer>"""
