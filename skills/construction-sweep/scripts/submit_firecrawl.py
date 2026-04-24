#!/usr/bin/env python3
"""Submit a Firecrawl batch scrape for <county>_fc_urls.json.

Requires ~/.firecrawl_key (chmod 600).

Usage: python3 submit_firecrawl.py <county> <state_dir>
Prints: FC batch id + polling URL (written to <state_dir>/<county>_fc_batch.json)
"""
import sys, os, json, urllib.request
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print('usage: submit_firecrawl.py <county> <state_dir>', file=sys.stderr)
        sys.exit(2)
    county, state_dir = sys.argv[1], Path(sys.argv[2])
    cl = county.lower()

    key_path = Path.home() / '.firecrawl_key'
    if not key_path.exists():
        print(f'ERR: {key_path} missing. See SETUP.md §Credentials.', file=sys.stderr)
        sys.exit(3)
    key = key_path.read_text().strip()

    urls = json.load(open(state_dir / f'{cl}_fc_urls.json'))
    if not urls:
        print('no URLs to submit; skipping FC batch', file=sys.stderr)
        sys.exit(0)

    payload = {'urls': urls, 'formats': ['markdown'], 'onlyMainContent': True, 'waitFor': 2000}
    req = urllib.request.Request(
        'https://api.firecrawl.dev/v1/batch/scrape',
        data=json.dumps(payload).encode(),
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
    )
    r = json.load(urllib.request.urlopen(req))
    out = {'id': r.get('id'), 'url': r.get('url'), 'n_submitted': len(urls)}
    json.dump(out, open(state_dir / f'{cl}_fc_batch.json', 'w'), indent=2)
    print(f'FC batch id={out["id"]} n={len(urls)}')


if __name__ == '__main__':
    main()
