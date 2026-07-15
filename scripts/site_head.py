# -*- coding: utf-8 -*-
"""Fragmenti HTML condivisi per <head> pagine pubbliche."""


def render_favicon_links(prefix: str = "") -> str:
    """Tag favicon standard per tutte le pagine."""
    p = prefix
    return f"""<link href="{p}images/favicon.svg" rel="icon" type="image/svg+xml"/>
<link href="{p}images/favicon-32x32.png" rel="icon" sizes="32x32" type="image/png"/>
<link href="{p}images/apple-touch-icon.png" rel="apple-touch-icon"/>"""
