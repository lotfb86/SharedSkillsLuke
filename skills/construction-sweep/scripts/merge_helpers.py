#!/usr/bin/env python3
"""Shared helpers: domain/phone normalization, license/years extraction, scope detection, email extraction."""
import re, datetime
from urllib.parse import urlparse


def norm_domain(u: str) -> str:
    """Normalize URL to bare domain (no www, no path)."""
    if not u:
        return ''
    try:
        p = urlparse(u if '://' in u else 'http://' + u)
        host = (p.netloc or p.path).lower().replace('www.', '').strip('/')
        return host.split('/')[0]
    except Exception:
        return ''


def norm_phone(p: str) -> str:
    """Reduce phone to digits only."""
    return re.sub(r'\D', '', p or '')


def norm_fb_slug(u: str) -> str:
    """Reduce a Facebook URL to its slug/id for dedup."""
    if not u:
        return ''
    u = u.lower().strip()
    u = re.sub(r'https?://(www\.)?(m\.)?facebook\.com/', '', u)
    u = re.sub(r'^facebook\.com/', '', u)
    u = u.rstrip('/')
    u = u.split('?')[0].split('#')[0]
    return u


EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')

# License patterns — require explicit contractor-license context to avoid image-file false positives
LIC_PATTERNS = [
    re.compile(r'\bRCE[- ]?\d{3,7}\b'),                                              # Idaho RCE (distinctive)
    re.compile(r'\bCCB\s*#?\s*\d{4,7}\b'),                                           # Oregon CCB (distinctive)
    re.compile(r'(?:License|Lic\.?|Contractor|Reg(?:istration)?)\s*#?\s*([A-Z]{2,8}\*?\d{2,6}[A-Z0-9]{1,4})', re.I),
    re.compile(r'(?:License|Lic\.?|Contractor|Reg(?:istration)?)\s*#\s*(\d{4,8})', re.I),
    re.compile(r'\bGC\s*#\s*([A-Z0-9-]{4,15})'),
    re.compile(r'\b(?:ID|WA|OR|ID #|WA #|OR #)\s*#?\s*([A-Z]{4,8}\*?\d{2,4}[A-Z0-9]{1,4})'),
]

YEAR_IN_BIZ = [
    re.compile(r'\b(?:over|more than|for)\s+(\d{2,3})\+?\s*years\b', re.I),
    re.compile(r'\b(\d{2,3})\+\s*years\s+of\s+(?:experience|service|building|construction)', re.I),
    re.compile(r'\bsince\s+(19|20)(\d{2})\b', re.I),
    re.compile(r'\bfounded\s+in\s+(19|20)(\d{2})\b', re.I),
    re.compile(r'\bestablished\s+in\s+(19|20)(\d{2})\b', re.I),
    re.compile(r'\bfamily[- ]owned\s+(?:and\s+operated\s+)?since\s+(19|20)(\d{2})\b', re.I),
]

SCOPE_WORDS = {
    'residential': ['custom home', 'new home', 'home build', 'residential', 'single family', 'dream home', 'remodel'],
    'commercial':  ['commercial', 'office building', 'retail', 'warehouse', 'tenant improvement', 'restaurant build'],
    'civil':       ['civil', 'road', 'bridge', 'highway', 'site work', 'sitework', 'excavation', 'paving', 'grading', 'utilities', 'infrastructure'],
}


def detect_scope(text: str) -> str:
    t = (text or '').lower()
    hits = {k: sum(1 for w in words if w in t) for k, words in SCOPE_WORDS.items()}
    nonzero = {k: v for k, v in hits.items() if v > 0}
    if not nonzero:
        return ''
    if len(nonzero) > 1:
        return 'mixed'
    return next(iter(nonzero))


def extract_years(text: str) -> str:
    now = datetime.datetime.now().year
    for p in YEAR_IN_BIZ:
        m = p.search(text or '')
        if m:
            g = m.groups()
            if len(g) == 1:
                return f"{g[0]} years"
            year = int(g[0] + g[1])
            if 1900 <= year <= now:
                return f"since {year}"
    return ''


def extract_licenses(text: str):
    found = set()
    for p in LIC_PATTERNS:
        for m in p.findall(text or ''):
            s = m.strip() if isinstance(m, str) else ''
            if not s:
                continue
            # Filter obvious false positives (image-filename patterns)
            if re.match(r'^(DSC[FN]|IMG|PHOTO|PIC|P\d)', s, re.I):
                continue
            if s.lower() in {'licensed', 'license', 'lic', 'contractor'}:
                continue
            found.add(s)
    return sorted(found)


def extract_emails(text: str):
    emails = set(m.lower() for m in EMAIL_RE.findall(text or ''))
    bogus = {'example@example.com', 'email@example.com', 'you@yoursite.com', 'name@example.com'}
    return sorted(e for e in emails if e not in bogus and not e.endswith('.png') and not e.endswith('.jpg'))


def services_summary(md: str) -> str:
    if not md:
        return ''
    lines = [l.strip() for l in md.split('\n') if l.strip()]
    for l in lines:
        low = l.lower()
        if any(skip in low for skip in ['cookie', 'privacy', 'subscribe', 'sign up', 'follow us', 'menu', 'home ·', 'all rights reserved', '©']):
            continue
        if len(l) < 40:
            continue
        if l.startswith('#') or l.startswith('!'):
            continue
        if l.startswith('[') and l.endswith(')'):
            continue
        if re.search(r'\b(build|construct|remodel|contract|home|house|commercial|residential|design)\w*', l, re.I):
            return l[:300]
    for l in lines:
        if 60 <= len(l) <= 300 and not l.startswith(('#', '!', '[', '*', '-')):
            return l
    return ''


# Master CSV schema — 27 columns
MASTER_COLS = [
    'business_name', 'classification_reason', 'category_primary', 'categories_all',
    'address', 'city', 'counties', 'state', 'postal_code',
    'phone', 'website', 'email_primary', 'all_emails',
    'facebook', 'instagram', 'linkedin',
    'google_rating', 'google_reviews_count',
    'years_in_business', 'license_numbers', 'services_summary', 'scope',
    'facebook_likes', 'facebook_followers', 'facebook_description',
    'search_term_source', 'place_id',
]
