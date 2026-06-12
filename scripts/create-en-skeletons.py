#!/usr/bin/env python3
"""
Create English skeleton pages in /en/ with correct HTML structure.
Mechanical transformations only: paths, links, canonical, hreflang, lang attribute.
Italian text is preserved for translation agents.
"""

import os
import re
import json

BASE = '/Users/niccolomazzoleni/Abra-Robotics'

SKIP_STEMS = {
    '_template', '_template-amr', '_template-cobot', '_template-compact',
    'index.backup', 'restyle-preview', 'index-zenixa', '_amr_catalog_fragment',
}
SKIP_DIRS = {'admin', 'scripts', '.git', 'node_modules', 'en', '__pycache__', 'apps-script'}

os.makedirs(f'{BASE}/en/prodotti', exist_ok=True)
print('Created /en/ and /en/prodotti/')

pages = []

for root_dir, dirs, files in os.walk(BASE):
    dirs[:] = sorted([d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')])

    for fname in sorted(files):
        if not fname.endswith('.html'):
            continue
        stem = fname[:-5]
        if stem in SKIP_STEMS:
            continue

        rel = os.path.relpath(os.path.join(root_dir, fname), BASE).replace(os.sep, '/')
        parts = rel.split('/')
        if len(parts) > 2:
            continue  # only root and prodotti/ pages

        is_product = rel.startswith('prodotti/')

        en_stem = stem + '-en'
        en_rel = (f'en/prodotti/{en_stem}.html' if is_product else f'en/{en_stem}.html')

        it_canonical = ('https://abrarobotics.com/' if rel == 'index.html'
                        else f'https://abrarobotics.com/{rel}')
        en_canonical = f'https://abrarobotics.com/{en_rel}'

        src_path = os.path.join(BASE, rel)
        dst_path = os.path.join(BASE, en_rel)

        with open(src_path, 'r', encoding='utf-8') as f:
            html = f.read()

        # 1. HTML lang
        html = re.sub(r'<html([^>]*)\blang="it"', r'<html\1lang="en"', html)
        html = re.sub(r"<html([^>]*)\blang='it'", r"<html\1lang='en'", html)

        # 2. Remove existing canonical and og:url (will re-add below)
        html = re.sub(r'[ \t]*<link rel="canonical"[^>]*/?>\n?', '', html)
        html = re.sub(r'[ \t]*<meta property="og:url"[^>]*/?>\n?', '', html)

        # 3. Fix asset paths
        if is_product:
            html = html.replace('href="../style.css"', 'href="../../style.css"')
            html = html.replace('src="../script.js"',  'src="../../script.js"')
            html = re.sub(r'src="\.\./scripts/', 'src="../../scripts/', html)
            html = re.sub(r'src="\.\./images/', 'src="../../images/', html)
            html = re.sub(r'href="\.\./images/', 'href="../../images/', html)
            html = re.sub(r'src="\.\./logos/',  'src="../../logos/', html)
            html = re.sub(r'href="\.\./logos/', 'href="../../logos/', html)
            html = re.sub(r'src="\.\./fonts/',  'src="../../fonts/', html)
            html = re.sub(r'href="\.\./fonts/', 'href="../../fonts/', html)
            html = html.replace('href="product.css"', 'href="../../prodotti/product.css"')
        else:
            html = html.replace('href="style.css"', 'href="../style.css"')
            html = html.replace('src="script.js"',  'src="../script.js"')
            html = re.sub(r'src="scripts/',  'src="../scripts/', html)
            html = re.sub(r'src="images/',   'src="../images/', html)
            html = re.sub(r'href="images/',  'href="../images/', html)
            html = re.sub(r'src="logos/',    'src="../logos/', html)
            html = re.sub(r'href="logos/',   'href="../logos/', html)
            html = re.sub(r'src="fonts/',    'src="../fonts/', html)
            html = re.sub(r'href="fonts/',   'href="../fonts/', html)

        # 4. Fix internal .html links (add -en suffix before " or #)
        # Must not touch: https://, mailto:, tel:, wa.me, #-only anchors, .css, .js, .png, .jpg, .svg
        def add_en_suffix(m):
            name, tail = m.group(1), m.group(2)
            return f'href="{name}-en.html{tail}'

        if is_product:
            # Links to root pages: href="../PAGE.html[#"] => href="../PAGE-en.html[#"]
            html = re.sub(
                r'href="\.\./([a-z0-9][a-z0-9_-]*)\.html([#"])',
                lambda m: f'href="../{m.group(1)}-en.html{m.group(2)}',
                html
            )
            # Links to product pages (same folder): href="PAGE.html[#"] => href="PAGE-en.html[#"]
            html = re.sub(
                r'href="([a-z0-9][a-z0-9_-]*)\.html([#"])',
                lambda m: f'href="{m.group(1)}-en.html{m.group(2)}',
                html
            )
        else:
            # Links to root pages: href="PAGE.html[#"] => href="PAGE-en.html[#"]
            html = re.sub(
                r'href="([a-z0-9][a-z0-9_-]*)\.html([#"])',
                lambda m: f'href="{m.group(1)}-en.html{m.group(2)}',
                html
            )
            # Links to product pages: href="prodotti/PAGE.html[#"] => href="prodotti/PAGE-en.html[#"]
            html = re.sub(
                r'href="prodotti/([a-z0-9][a-z0-9_-]*)\.html([#"])',
                lambda m: f'href="prodotti/{m.group(1)}-en.html{m.group(2)}',
                html
            )

        # 5. Insert canonical + og:url after <head>
        canonical_line = f'  <link rel="canonical" href="{en_canonical}">'
        html = re.sub(r'(<head>)', r'\1\n' + canonical_line, html, count=1)

        if 'og:title' in html:
            og_url_line = f'  <meta property="og:url" content="{en_canonical}">'
            html = re.sub(
                r'(<meta property="og:title")',
                og_url_line + r'\n  \1',
                html, count=1
            )

        # 6. Add hreflang before </head>
        hreflang = (
            f'  <link rel="alternate" hreflang="it" href="{it_canonical}">\n'
            f'  <link rel="alternate" hreflang="en" href="{en_canonical}">\n'
            f'  <link rel="alternate" hreflang="x-default" href="{it_canonical}">\n'
        )
        html = html.replace('</head>', hreflang + '</head>', 1)

        # 7. Robots: keep noindex only on -lc pages
        if not stem.endswith('-lc'):
            html = re.sub(
                r'<meta name="robots" content="noindex[^"]*">',
                '<meta name="robots" content="index, follow">',
                html
            )

        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(html)

        pages.append({
            'src': rel,
            'dst': en_rel,
            'it_canonical': it_canonical,
            'en_canonical': en_canonical,
            'is_product': is_product,
        })
        print(f'  {en_rel}')

print(f'\nDone: {len(pages)} EN skeleton files')

with open(f'{BASE}/.en-pages.json', 'w', encoding='utf-8') as f:
    json.dump(pages, f, indent=2, ensure_ascii=False)
print('Saved page list to .en-pages.json')
