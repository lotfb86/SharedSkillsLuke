#!/usr/bin/env python3
"""Append new county KEEPS with enrichment into master.csv + update seen.json.

Merges: classified keeps + Firecrawl markdown + FB page info → one row each.

Usage: python3 append_county.py <county> <state_dir>
Requires in state_dir:
  master.csv, seen.json
  <county>_classified.json  ({keeps:[...], rejects:[...]})
  <county>_fc.json          (Firecrawl batch results, optional)
  <county>_fb.json          (FB Apify dataset items, optional)
"""
import sys, os, json, csv, re
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merge_helpers import (
    norm_domain, norm_phone, norm_fb_slug,
    extract_licenses, extract_years, detect_scope, services_summary, extract_emails,
    MASTER_COLS,
)


def main():
    if len(sys.argv) != 3:
        print('usage: append_county.py <county> <state_dir>', file=sys.stderr)
        sys.exit(2)
    county, state_dir = sys.argv[1], Path(sys.argv[2])
    cl = county.lower()
    state_name = json.load(open(state_dir / 'counties.json')).get('state', '')

    cls = json.load(open(state_dir / f'{cl}_classified.json'))
    keeps = cls.get('keeps', [])

    # FC: domain -> markdown (longest per domain)
    fc_map = {}
    fc_path = state_dir / f'{cl}_fc.json'
    if fc_path.exists():
        data = json.load(open(fc_path))
        items = data.get('data') if isinstance(data, dict) else data
        for it in items or []:
            md = it.get('markdown') or ''
            meta = it.get('metadata') or {}
            url = meta.get('sourceURL') or meta.get('url') or ''
            d = norm_domain(url)
            if d and (d not in fc_map or len(md) > len(fc_map[d])):
                fc_map[d] = md
    else:
        print(f'WARN no FC data at {fc_path}', file=sys.stderr)

    # FB: slug -> page record
    fb_map = {}
    fb_path = state_dir / f'{cl}_fb.json'
    if fb_path.exists():
        for it in json.load(open(fb_path)):
            pn = it.get('pageName') or ''
            pu = it.get('pageUrl') or ''
            slug = norm_fb_slug(pu)
            if pn and pn != 'people' and slug:
                fb_map[slug] = it
                fb_map[pn.lower()] = it
            elif slug:
                fb_map[slug] = it
    else:
        print(f'WARN no FB data at {fb_path}', file=sys.stderr)

    with open(state_dir / 'master.csv') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or MASTER_COLS
        master = list(reader)

    seen = json.load(open(state_dir / 'seen.json'))
    appended = 0
    for k in keeps:
        website = k.get('website') or ''
        dom = norm_domain(website)
        md = fc_map.get(dom, '')
        fb_urls = k.get('facebooks') or []
        fb_row = None
        for u in fb_urls:
            s = norm_fb_slug(u)
            if s in fb_map:
                fb_row = fb_map[s]; break
            m = re.search(r'id=(\d+)', u)
            if m and m.group(1) in fb_map:
                fb_row = fb_map[m.group(1)]; break
        fb_info_text, fb_emails, fb_likes, fb_followers, fb_desc = '', [], '', '', ''
        if fb_row:
            fb_info_text = ' '.join(fb_row.get('info') or []) + ' ' + (fb_row.get('intro') or '')
            if fb_row.get('email'):
                fb_emails.append(fb_row['email'])
            fb_likes = fb_row.get('likes', '') or ''
            fb_followers = fb_row.get('followers', '') or ''
            fb_desc = fb_row.get('intro', '') or ''
        combined = md + '\n' + fb_info_text
        licenses = extract_licenses(combined)
        years = extract_years(combined)
        scope = detect_scope(combined)
        fc_emails = extract_emails(md) if md else []
        all_emails = []
        for e in (k.get('emails') or []) + fb_emails + fc_emails:
            el = e.lower().strip()
            if el and el not in all_emails:
                all_emails.append(el)
        row = {col: '' for col in fieldnames}
        row.update({
            'business_name': k.get('title', ''),
            'classification_reason': k.get('classification_reason', ''),
            'category_primary': k.get('categoryName', ''),
            'categories_all': '|'.join(k.get('categories') or []),
            'address': k.get('address', ''),
            'city': k.get('city', ''),
            'counties': county,
            'state': k.get('state', '') or state_name,
            'postal_code': k.get('postalCode', ''),
            'phone': k.get('phone', ''),
            'website': website,
            'email_primary': all_emails[0] if all_emails else '',
            'all_emails': '|'.join(all_emails),
            'facebook': (fb_urls or [''])[0],
            'instagram': '|'.join(k.get('instagrams') or []),
            'linkedin': '|'.join(k.get('linkedIns') or []),
            'google_rating': k.get('totalScore') or '',
            'google_reviews_count': k.get('reviewsCount') or '',
            'years_in_business': years,
            'license_numbers': '|'.join(licenses),
            'services_summary': services_summary(md) or (fb_row.get('intro', '') if fb_row else ''),
            'scope': scope,
            'facebook_likes': fb_likes,
            'facebook_followers': fb_followers,
            'facebook_description': fb_desc,
            'search_term_source': k.get('searchString', ''),
            'place_id': k.get('placeId', ''),
        })
        master.append(row)
        idx = len(master) - 1
        if k.get('placeId'):
            seen['place_id'][k['placeId']] = idx
        if dom:
            seen['domain'].setdefault(dom, idx)
        ph = norm_phone(k.get('phone', ''))
        if len(ph) >= 10:
            seen['phone'].setdefault(ph, idx)
        nc = ((k.get('title') or '').lower().strip() + '|' + (k.get('city') or '').lower().strip())
        if nc.strip('|'):
            seen['name_city'].setdefault(nc, idx)
        appended += 1

    with open(state_dir / 'master.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(master)
    with open(state_dir / 'seen.json', 'w') as f:
        json.dump(seen, f, indent=2)

    # Log processed
    proc_path = state_dir / 'processed.txt'
    existing = set()
    if proc_path.exists():
        existing = {line.strip() for line in proc_path.read_text().splitlines() if line.strip()}
    if county not in existing:
        with open(proc_path, 'a') as f:
            f.write(county + '\n')

    print(f'appended {appended} new {county} rows. master total: {len(master)}')


if __name__ == '__main__':
    main()
