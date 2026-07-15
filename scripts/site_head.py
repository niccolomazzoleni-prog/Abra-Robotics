# -*- coding: utf-8 -*-
"""Fragmenti HTML condivisi per <head> pagine pubbliche."""


def render_favicon_links(prefix: str = "") -> str:
    """Tag favicon standard — Nasalization via PNG/ICO (affidabile ovunque)."""
    p = prefix
    return f"""<link href="{p}favicon.ico" rel="icon" sizes="any"/>
<link href="{p}images/favicon-32x32.png" rel="icon" type="image/png" sizes="32x32"/>
<link href="{p}images/favicon-16x16.png" rel="icon" type="image/png" sizes="16x16"/>
<link href="{p}images/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"/>"""


def render_llms_link(prefix: str = "") -> str:
    """Discovery llms.txt per crawler AI."""
    p = prefix
    return f'<link href="{p}llms.txt" rel="alternate" type="text/plain" title="LLM site summary"/>'
