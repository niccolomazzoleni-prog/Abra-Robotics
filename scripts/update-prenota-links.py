#!/usr/bin/env python3
"""Replace all 'Prenota una chiamata' / 'Book a call' button hrefs with Google Calendar URL."""

import os, re
from bs4 import BeautifulSoup

BASE = '/Users/niccolomazzoleni/Abra-Robotics'
CALENDAR_URL = 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ22FrpPdyPVRihi4eXPQlljTcG2toa8XF2d8W-QX-L9cKMaXqozq_YsHym56LEdTs9WsnqlTHeF'

SKIP_DIRS = {'admin', 'scripts', '.git', 'node_modules', '__pycache__', 'apps-script'}
SKIP_STEMS = {'index.backup', 'restyle-preview', 'index-zenixa', '_amr_catalog_fragment',
              '_template', '_template-amr', '_template-cobot', '_template-compact'}

# Italian and English trigger texts
PRENOTA_TEXTS = {'prenota una chiamata', 'prenota una call', 'book a call', 'prenota chiamata'}

updated_files = 0
updated_links = 0

for root_dir, dirs, files in os.walk(BASE):
    dirs[:] = sorted([d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')])
    for fname in files:
        if not fname.endswith('.html'):
            continue
        stem = fname[:-5]
        if stem in SKIP_STEMS:
            continue

        fpath = os.path.join(root_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        changed = 0

        for a in soup.find_all('a', href=True):
            text = a.get_text(strip=True).lower().rstrip(' →')
            if any(t in text for t in PRENOTA_TEXTS):
                if a['href'] != CALENDAR_URL:
                    a['href'] = CALENDAR_URL
                    a['target'] = '_blank'
                    a['rel'] = 'noopener noreferrer'
                    changed += 1

        if changed:
            rel = os.path.relpath(fpath, BASE)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            updated_files += 1
            updated_links += changed
            print(f'  {rel}: {changed} link(s)')

print(f'\nDone: {updated_links} links updated across {updated_files} files')
