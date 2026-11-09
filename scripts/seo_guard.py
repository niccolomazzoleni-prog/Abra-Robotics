"""SEO guard for the redesign: snapshot what search engines see on every page, then block any page
where a layout change altered it by mistake.

    python3 scripts/seo_guard.py snapshot            # record the baseline (run once, before changing pages)
    python3 scripts/seo_guard.py check               # compare the current pages with the baseline
    python3 scripts/seo_guard.py check --allow lp-unitree.html,software.html   # pages whose content changes on purpose

What is compared, per page (outside menu, footer and scripts, which the redesign replaces; the header with
the hero, H1 and intro is kept, and so are breadcrumbs):
title, meta description, meta robots, canonical, hreflang links, H1, H2/H3 headings, visible text,
JSON-LD structured data and the internal links in the content. Menu and footer links are not compared
one by one: instead the check makes sure every page in the sitemap is still linked from somewhere.

The baseline lives in _proposte/ (never published). Exit code 1 when any page is blocked.
"""
import argparse, hashlib, html, json, os, re, subprocess, sys
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(ROOT, '_proposte', 'seo-baseline.json')
SKIP = re.compile(r'^(proposte|index-v\d|v\d|_proposte/|editor/|scripts/)')
CHROME = ['footer', 'script', 'style', 'noscript', 'svg']
CHROME_CLASSES = ['navbar', 'lp-navbar', 'site-foot', 'lpu-footer', 'footer', 'footer-legal', 'top-bar', 'announcement-bar',
                  'cookie-banner', 'chat-widget']
FIELDS = ['title', 'description', 'robots', 'canonical', 'hreflang', 'h1', 'headings', 'text', 'jsonld', 'links']


def pages():
    out = subprocess.run(['git', 'ls-files', '*.html'], cwd=ROOT, capture_output=True, text=True).stdout.split()
    return sorted(p for p in out if not SKIP.match(p) and os.path.exists(os.path.join(ROOT, p)))


def norm(t):
    return ' '.join(html.unescape(t or '').split())


def internal(href):
    if not href or href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
        return None
    if href.startswith(('http://', 'https://', '//')):
        m = re.match(r'(?:https?:)?//(?:www\.)?abrarobotics\.com(/[^#?]*)?', href)
        return (m.group(1) or '/') if m else None
    return href.split('#')[0].split('?')[0] or None


def extract(path):
    raw = open(os.path.join(ROOT, path), encoding='utf-8', errors='ignore').read()
    soup = BeautifulSoup(raw, 'lxml')
    head = soup.head or soup

    def meta(name):
        m = head.find('meta', attrs={'name': name})
        return norm(m.get('content')) if m else ''

    canon = head.find('link', rel='canonical')
    hreflang = sorted([l.get('hreflang', ''), l.get('href', '')] for l in head.find_all('link', rel='alternate') if l.get('hreflang'))
    jsonld = []
    for s in soup.find_all('script', type='application/ld+json'):
        try:
            jsonld.append(json.dumps(json.loads(s.string or s.get_text()), sort_keys=True, ensure_ascii=False))
        except Exception:
            jsonld.append(norm(s.get_text()))
    body = soup.body or soup
    for tag in body.find_all(CHROME):
        tag.decompose()
    for tag in body.find_all('nav'):                    # menus go, breadcrumbs stay
        label = ' '.join(tag.get('class', [])) + ' ' + (tag.get('aria-label') or '')
        if 'breadcrumb' not in label.lower():
            tag.decompose()
    for cls in CHROME_CLASSES:
        for tag in body.select('.' + cls):
            tag.decompose()
    text = norm(body.get_text(' '))
    links = sorted({u for a in body.find_all('a') if (u := internal(a.get('href')))})
    return {
        'title': norm(soup.title.get_text()) if soup.title else '',
        'description': meta('description'),
        'robots': meta('robots'),
        'canonical': canon.get('href', '') if canon else '',
        'hreflang': hreflang,
        'h1': [norm(h.get_text()) for h in body.find_all('h1')],
        'headings': [norm(h.get_text()) for h in body.find_all(['h2', 'h3'])],
        'text': hashlib.sha1(text.encode()).hexdigest(),
        'text_len': len(text),
        'text_sample': text[:400],
        'jsonld': sorted(jsonld),
        'links': links,
        'all_links': sorted({u for a in BeautifulSoup(raw, 'lxml').find_all('a') if (u := internal(a.get('href')))}),
    }


def resolve(src_page, href):
    """Turn a link found on src_page into a repo path, to see which pages are linked from somewhere."""
    if href.startswith('/'):
        p = href.lstrip('/')
    else:
        p = os.path.normpath(os.path.join(os.path.dirname(src_page), href))
    if p in ('', '.'):
        p = 'index.html'
    if p.endswith('/'):
        p += 'index.html'
    if not os.path.splitext(p)[1]:
        p += '.html'
    return p


def snapshot():
    data = {p: extract(p) for p in pages()}
    os.makedirs(os.path.dirname(BASELINE), exist_ok=True)
    json.dump(data, open(BASELINE, 'w'), ensure_ascii=False)
    print(f'baseline: {len(data)} pages -> {os.path.relpath(BASELINE, ROOT)}')


def check(allow):
    base = json.load(open(BASELINE))
    now = {p: extract(p) for p in pages()}
    blocked, changed_ok = {}, []
    for p, b in base.items():
        if p not in now:
            blocked[p] = ['page missing']
            continue
        diffs = [f for f in FIELDS if b[f] != now[p][f]]
        if diffs:
            (changed_ok.append((p, diffs)) if p in allow else blocked.__setitem__(p, diffs))
    # orphans: sitemap pages that were linked from somewhere before and are not any more
    def linked(d):
        out = set()
        for src, v in d.items():
            out |= {resolve(src, h) for h in v['all_links']}
        return out
    before, after = linked(base), linked(now)
    orphans = sorted(p for p in base if p in before and p not in after and p in now)
    for p in orphans:
        blocked.setdefault(p, []).append('no longer linked from any page')
    new = sorted(set(now) - set(base))

    print(f'checked {len(base)} pages: {len(blocked)} blocked, {len(changed_ok)} changed on purpose, {len(new)} new')
    for p, d in sorted(blocked.items())[:60]:
        print('  BLOCK', p, ', '.join(d))
        for f in d:
            if f in base.get(p, {}) and f != 'text':
                print('     before:', str(base[p][f])[:160]); print('     after: ', str(now[p][f])[:160])
            elif f == 'text':
                print('     text length', base[p]['text_len'], '->', now[p]['text_len'])
    if len(blocked) > 60:
        print(f'  ... and {len(blocked) - 60} more')
    for p, d in changed_ok:
        print('  allowed', p, ', '.join(d))
    for p in new[:20]:
        print('  new page', p)
    return 1 if blocked else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['snapshot', 'check'])
    ap.add_argument('--allow', default='', help='comma-separated pages whose content changes on purpose')
    a = ap.parse_args()
    if a.mode == 'snapshot':
        snapshot()
    else:
        sys.exit(check({x.strip() for x in a.allow.split(',') if x.strip()}))
