#!/usr/bin/env python3
"""Split a county's raw scrape into (new, seen) using <state>/seen.json.

For SEEN records: add county to master row's `counties`, backfill empty fields.
For NEW records: emit to <state_dir>/<county>_new.json for downstream classify/enrich.

Usage: python3 dedup_county.py <county> <raw.json> <state_dir>
"""
import sys, json, csv, os
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merge_helpers import norm_domain, norm_phone


def add_county(existing, county):
    counties = [c.strip() for c in (existing or '').split('|') if c.strip()]
    if county not in counties:
        counties.append(county)
    return '|'.join(counties)


def backfill(row, raw):
    if not row.get('phone') and raw.get('phone'):
        row['phone'] = raw['phone']
    if not row.get('website') and raw.get('website'):
        row['website'] = raw['website']
    if not row.get('email_primary') and raw.get('emails'):
        row['email_primary'] = raw['emails'][0]
        row['all_emails'] = '|'.join(raw['emails'])
    if not row.get('facebook') and raw.get('facebooks'):
        row['facebook'] = raw['facebooks'][0]
    if not row.get('instagram') and raw.get('instagrams'):
        row['instagram'] = '|'.join(raw['instagrams'])
    if not row.get('linkedin') and raw.get('linkedIns'):
        row['linkedin'] = '|'.join(raw['linkedIns'])
    if not row.get('google_rating') and raw.get('totalScore'):
        row['google_rating'] = raw['totalScore']
    if not row.get('google_reviews_count') and raw.get('reviewsCount'):
        row['google_reviews_count'] = raw['reviewsCount']
    return row


def main():
    if len(sys.argv) != 4:
        print('usage: dedup_county.py <county> <raw.json> <state_dir>', file=sys.stderr)
        sys.exit(2)
    county, raw_path, state_dir = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    master_path = state_dir / 'master.csv'
    seen_path = state_dir / 'seen.json'

    raw = json.load(open(raw_path))
    seen = json.load(open(seen_path))

    # Within-county dedup by placeId
    uniq = {}
    for r in raw:
        pid = r.get('placeId')
        if not pid or pid in uniq:
            continue
        uniq[pid] = r
    print(f'within-county uniq: {len(uniq)}', file=sys.stderr)

    with open(master_path) as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        master = list(reader)

    new_records = []
    updated_count = 0
    for pid, r in uniq.items():
        idx = seen['place_id'].get(pid)
        if idx is None:
            d = norm_domain(r.get('website', ''))
            if d:
                idx = seen['domain'].get(d)
        if idx is None:
            ph = norm_phone(r.get('phone', ''))
            if len(ph) >= 10:
                idx = seen['phone'].get(ph)
        if idx is None:
            nc = (r.get('title') or '').lower().strip() + '|' + (r.get('city') or '').lower().strip()
            if nc.strip('|'):
                idx = seen['name_city'].get(nc)
        if idx is not None and idx < len(master):
            master[idx]['counties'] = add_county(master[idx]['counties'], county)
            master[idx] = backfill(master[idx], r)
            updated_count += 1
            seen['place_id'].setdefault(pid, idx)
            d = norm_domain(r.get('website', ''))
            if d:
                seen['domain'].setdefault(d, idx)
            ph = norm_phone(r.get('phone', ''))
            if len(ph) >= 10:
                seen['phone'].setdefault(ph, idx)
        else:
            new_records.append(r)

    with open(master_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(master)

    with open(seen_path, 'w') as f:
        json.dump(seen, f, indent=2)

    new_path = state_dir / f'{county.lower()}_new.json'
    with open(new_path, 'w') as f:
        json.dump(new_records, f, indent=2)

    print(f'county={county} total_uniq={len(uniq)} updated_existing={updated_count} new={len(new_records)}')
    print(f'new records -> {new_path}')


if __name__ == '__main__':
    main()
