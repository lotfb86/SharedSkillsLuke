#!/usr/bin/env python3
"""Initialize a state folder for the sweep pipeline.

Creates: <dir>/
  master.csv     — empty CSV with 27-col header
  seen.json      — empty dedup index {place_id,domain,phone,name_city}
  processed.txt  — empty file
  counties.json  — copied from data/counties_by_state.json[<state>]
  README.md      — copied from templates/state_readme.md

Idempotent. Does not overwrite existing files.

Usage: python3 bootstrap_state.py <State> [<dir>]
Default dir: ./<State>/
"""
import sys, os, json, csv, shutil
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merge_helpers import MASTER_COLS

SKILL_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_ROOT / 'data'
TEMPLATE_DIR = SKILL_ROOT / 'templates'


def main():
    if len(sys.argv) < 2:
        print('usage: bootstrap_state.py <State> [<dir>]', file=sys.stderr)
        sys.exit(2)
    state = sys.argv[1]
    state_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd() / state
    state_dir.mkdir(parents=True, exist_ok=True)

    # master.csv
    master_path = state_dir / 'master.csv'
    if not master_path.exists():
        with open(master_path, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=MASTER_COLS)
            w.writeheader()
        print(f'created {master_path}')
    else:
        print(f'exists:  {master_path}')

    # seen.json
    seen_path = state_dir / 'seen.json'
    if not seen_path.exists():
        json.dump({'place_id': {}, 'domain': {}, 'phone': {}, 'name_city': {}}, open(seen_path, 'w'), indent=2)
        print(f'created {seen_path}')
    else:
        print(f'exists:  {seen_path}')

    # processed.txt
    proc_path = state_dir / 'processed.txt'
    if not proc_path.exists():
        proc_path.touch()
        print(f'created {proc_path}')
    else:
        print(f'exists:  {proc_path}')

    # counties.json
    counties_path = state_dir / 'counties.json'
    if not counties_path.exists():
        source = DATA_DIR / 'counties_by_state.json'
        if not source.exists():
            print(f'WARN: {source} missing — skill data files not installed', file=sys.stderr)
            sys.exit(3)
        all_counties = json.load(open(source))
        if state not in all_counties:
            print(f'ERR: state "{state}" not in counties_by_state.json. Available: {sorted(all_counties.keys())}', file=sys.stderr)
            print(f'Add your state entry to {source} with ordered county list.', file=sys.stderr)
            sys.exit(4)
        json.dump({'state': state, 'counties': all_counties[state]}, open(counties_path, 'w'), indent=2)
        print(f'created {counties_path} with {len(all_counties[state])} counties')
    else:
        print(f'exists:  {counties_path}')

    # README.md
    readme_path = state_dir / 'README.md'
    template = TEMPLATE_DIR / 'state_readme.md'
    if not readme_path.exists() and template.exists():
        text = template.read_text().replace('{{STATE}}', state)
        readme_path.write_text(text)
        print(f'created {readme_path}')

    print(f'\nstate dir ready: {state_dir}')


if __name__ == '__main__':
    main()
