#!/usr/bin/env python3
"""Select next unprocessed county from counties.json minus processed.txt.

Usage: python3 pick_next_county.py <state_dir>
Prints: <county>\t<seat>\t<remaining_count>
Exits 1 if no counties remain.
"""
import sys, json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print('usage: pick_next_county.py <state_dir>', file=sys.stderr)
        sys.exit(2)
    sd = Path(sys.argv[1])
    counties = json.load(open(sd / 'counties.json'))['counties']
    processed = set()
    proc_path = sd / 'processed.txt'
    if proc_path.exists():
        processed = {line.strip() for line in proc_path.read_text().splitlines() if line.strip()}

    for c in counties:
        name = c['name'] if isinstance(c, dict) else c
        if name not in processed:
            seat = c.get('seat', '') if isinstance(c, dict) else ''
            remaining = sum(1 for x in counties if (x['name'] if isinstance(x, dict) else x) not in processed)
            print(f'{name}\t{seat}\t{remaining}')
            return

    print('all_done\t\t0', file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main()
