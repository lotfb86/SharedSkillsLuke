#!/usr/bin/env python3
"""Build Firecrawl URL list + FB Apify input from classified keeps.

Applies data/blocklists.json to strip URLs known to break FC or be low-value.

Usage: python3 prep_enrichment.py <county> <state_dir>
Emits: <state_dir>/<county>_fc_urls.json, <state_dir>/<county>_fb_input.json
"""
import sys, json, os
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
BLOCKLIST_PATH = SKILL_ROOT / 'data' / 'blocklists.json'


def main():
    if len(sys.argv) != 3:
        print('usage: prep_enrichment.py <county> <state_dir>', file=sys.stderr)
        sys.exit(2)
    county, state_dir = sys.argv[1], Path(sys.argv[2])
    cl = county.lower()

    blocklists = json.load(open(BLOCKLIST_PATH)) if BLOCKLIST_PATH.exists() else {'firecrawl': [], 'facebook': []}
    fc_block = blocklists.get('firecrawl', [])
    fb_block = blocklists.get('facebook', [])

    cls = json.load(open(state_dir / f'{cl}_classified.json'))
    fc_urls, fb_urls = [], []
    for k in cls.get('keeps', []):
        w = (k.get('website') or '').strip()
        if w and not any(b in w.lower() for b in fc_block):
            fc_urls.append(w)
        fbs = k.get('facebooks') or []
        if fbs:
            u = fbs[0]
            if not any(b in u.lower() for b in fb_block):
                fb_urls.append(u)

    json.dump(fc_urls, open(state_dir / f'{cl}_fc_urls.json', 'w'), indent=2)
    json.dump({'startUrls': [{'url': u} for u in fb_urls]}, open(state_dir / f'{cl}_fb_input.json', 'w'), indent=2)
    print(f'fc_urls={len(fc_urls)} fb_urls={len(fb_urls)}')


if __name__ == '__main__':
    main()
