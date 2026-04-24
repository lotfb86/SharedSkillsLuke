#!/usr/bin/env python3
"""Pull a completed Firecrawl batch (paginated).

Usage: python3 pull_firecrawl.py <county> <state_dir>
Reads <state_dir>/<county>_fc_batch.json for the batch id.
Writes <state_dir>/<county>_fc.json (flat list of {markdown, metadata, ...}).
"""
import sys, os, json, urllib.request, urllib.error
from pathlib import Path

MAX_PAGES = 100


def main():
    if len(sys.argv) != 3:
        print('usage: pull_firecrawl.py <county> <state_dir>', file=sys.stderr)
        sys.exit(2)
    county, state_dir = sys.argv[1], Path(sys.argv[2])
    cl = county.lower()
    batch = json.load(open(state_dir / f'{cl}_fc_batch.json'))
    batch_id = batch['id']

    key = (Path.home() / '.firecrawl_key').read_text().strip()
    url = f'https://api.firecrawl.dev/v1/batch/scrape/{batch_id}'
    all_data = []
    page = 0
    status = 'unknown'
    while url and page < MAX_PAGES:
        req = urllib.request.Request(url, headers={'Authorization': f'Bearer {key}'})
        r = json.load(urllib.request.urlopen(req))
        status = r.get('status', status)
        all_data.extend(r.get('data', []))
        url = r.get('next')
        page += 1

    if status != 'completed':
        print(f'WARN: batch status={status} (expected "completed") — you may need to wait longer', file=sys.stderr)

    json.dump(all_data, open(state_dir / f'{cl}_fc.json', 'w'), indent=2)
    print(f'FC pulled: items={len(all_data)} pages={page} status={status}')


if __name__ == '__main__':
    main()
