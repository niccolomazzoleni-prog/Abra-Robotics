#!/usr/bin/env python3
"""Add hreflang tags to Italian HTML pages pointing to their English counterparts."""

import os, json

BASE = '/Users/niccolomazzoleni/Abra-Robotics'

with open(f'{BASE}/.en-pages.json', encoding='utf-8') as f:
    pages = json.load(f)

updated = skipped = 0

for page in pages:
    it_path = os.path.join(BASE, page['src'])
    if not os.path.exists(it_path):
        print(f'  MISSING: {page["src"]}')
        continue

    with open(it_path, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'hreflang' in html:
        skipped += 1
        continue

    it_canonical = page['it_canonical']
    en_canonical = page['en_canonical']

    hreflang = (
        f'  <link rel="alternate" hreflang="it" href="{it_canonical}">\n'
        f'  <link rel="alternate" hreflang="en" href="{en_canonical}">\n'
        f'  <link rel="alternate" hreflang="x-default" href="{it_canonical}">\n'
    )

    html = html.replace('</head>', hreflang + '</head>', 1)

    with open(it_path, 'w', encoding='utf-8') as f:
        f.write(html)

    updated += 1

print(f'Done: {updated} updated, {skipped} skipped (already had hreflang)')
