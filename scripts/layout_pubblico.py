# -*- coding: utf-8 -*-
"""Fragmenti HTML condivisi per pagine pubbliche catalogo/listino."""

from site_nav import render_site_footer, render_site_nav

SITE_NAV = f"""
  <div class="top-bar">
    <p>Listino pubblico End-User · IVA esclusa · <a href="listino-unitree.html">Tabella prezzi</a> · <a href="catalogo-unitree.html">Catalogo</a></p>
  </div>
{render_site_nav("")}
"""

SITE_FOOTER = "\n" + render_site_footer("") + "\n"

PUBLIC_NOTICE = """
"""
