#!/usr/bin/env python3
"""Rules-based classifier for builders vs trades/suppliers/services.

Reads <state_dir>/<county>_new.json, writes <state_dir>/<county>_classified.json.

Rules (in order):
1. Name pattern reject (handyman, plumber, etc.) UNLESS primary is a kept category
2. Primary category hard reject (single-trade, supplier, service)
   - Rescue if 2+ building categories in categories[]
3. Vague primary + no website + no extra cats → reject
   - UNLESS name has builder signal (Builders, Custom Homes, Construction)
4. Primary in keep list → KEEP
5. Any building-scope category in categories[] → KEEP
6. Otherwise REJECT

Usage: python3 classify_county.py <county> <state_dir>
"""
import sys, json, re
from pathlib import Path

HARD_REJECT_PRIMARY = {
    'plumber', 'electrician', 'hvac contractor', 'roofing contractor', 'concrete contractor', 'masonry contractor',
    'painter', 'landscaper', 'landscape designer', 'landscaping supply store', 'tree service', 'arborist service',
    'handyman/handywoman/handyperson', 'saw mill', 'logging contractor', 'trucking company', 'mover',
    'waste management service', 'hardware store', 'well drilling contractor', 'sandblasting service', 'welder',
    'auto repair shop', 'towing service', 'mechanic', 'janitorial service', 'drafting service', 'home inspector',
    'real estate agency', 'real estate developer', 'real estate', 'website designer', 'garden center', 'crane service',
    'house cleaning service', 'water damage restoration service', 'fire damage restoration service',
    'restoration service', 'drainage service', 'civil engineer', 'civil engineering company', 'engineer',
    'shed builder', 'portable building manufacturer', 'sheet metal contractor', 'truss manufacturer',
    'metal fabricator', 'ready mix concrete supplier', 'sand & gravel supplier', 'container supplier',
    'lumber store', 'wood supplier', 'animal feed store', 'souvenir store', 'forestry service',
    'telecommunications contractor', 'dryer vent cleaning service', 'self-storage facility', 'fence supply store',
    'concrete product supplier', 'drilling contractor', 'gravel pit', 'asphalt contractor', 'paving contractor',
    'air duct cleaning service', 'excavating contractor', 'housing society', 'dock builder', 'cleaning service',
    'electric generator shop', 'real estate consultant', 'landscape architect', 'pond contractor', 'mill',
    'road construction machine repair service', 'water works', 'fence contractor', 'siding contractor',
    'garden center', 'pet supply store', 'boiler supplier', 'repair service', 'equipment rental agency',
    'retaining wall supplier', 'electric vehicle charging station', 'snow removal service', 'property maintenance',
    'building consultant', 'architecture firm', 'construction material wholesaler', 'garage builder',
    'gazebo builder', 'facade builder', 'security system supplier',
}

KEEP_PRIMARY = {
    'general contractor', 'home builder', 'custom home builder', 'construction company', 'contractor',
    'remodeler', 'log home builder', 'modular home builder', 'design-build',
    'road construction company', 'building firm',
}

KEEP_ANY = {
    'home builder', 'custom home builder', 'general contractor', 'construction company',
    'log home builder', 'modular home builder', 'remodeler',
}

NAME_REJECT_PAT = re.compile(
    r'\b(handyman|plumbing|electric(?!\w)|hvac|roofing|concrete|masonry|painting|landscaping|'
    r'tree service|sawmill|logging|trucking|moving|hardware|well drilling|sandblast|welder|welding|'
    r'auto repair|towing|mechanic|janitorial|drafting|home inspector|realty|website|garden center|'
    r'cleaning|restoration|engineering|shed |portable building|sheet metal|truss|metal fab|'
    r'ready mix|sand & gravel|container|lumber co|wood supplier|souvenir|forestry|telecom|'
    r'dryer vent|storage|fence supply|drilling|sealcoat|asphalt|excavating|excavation|'
    r'electric co\.?|janitor|property maintenance|crane |towing|mover|air conditioning)\b',
    re.I,
)

VAGUE_PRIMARY = {'construction company', 'contractor'}


def classify(r):
    name = (r.get('title') or '').strip()
    primary = (r.get('categoryName') or '').lower().strip()
    cats = [c.lower().strip() for c in (r.get('categories') or [])]
    cats_set = set(cats)
    website = (r.get('website') or '').strip()

    # Hard name reject
    if NAME_REJECT_PAT.search(name) and primary not in KEEP_PRIMARY and primary != 'construction company':
        return False, 'name pattern suggests single-trade'

    # Hard primary reject
    if primary in HARD_REJECT_PRIMARY:
        building_cats = cats_set & KEEP_ANY
        if len(building_cats) >= 2:
            return True, f'rescued: primary={primary} but {len(building_cats)} building cats'
        # Name-signal rescue even for rejected primary (e.g. "Sasquatch Builders" w/ Roofing primary)
        if re.search(r'\b(builders?|custom homes?)\b', name, re.I) and 'contractor' in cats_set:
            return True, f'rescued: name=builders + contractor in cats despite primary={primary}'
        return False, f'primary rejected: {primary}'

    # Vague primary + thin metadata → reject unless name has builder signal
    if primary in VAGUE_PRIMARY and not website and len(cats) <= 1:
        if re.search(r'\b(builders?|custom homes?|construction)\b', name, re.I):
            return True, f'vague cats but name has builder signal: {name}'
        return False, 'vague primary, no website, no secondary cats'

    # Primary in keep list
    if primary in KEEP_PRIMARY:
        return True, f'primary: {primary}'

    # Any building cat
    if cats_set & KEEP_ANY:
        return True, f'has building cat: {sorted(cats_set & KEEP_ANY)[0]}'

    return False, f'no signal: primary={primary}'


def main():
    if len(sys.argv) != 3:
        print('usage: classify_county.py <county> <state_dir>', file=sys.stderr)
        sys.exit(2)
    county, state_dir = sys.argv[1], Path(sys.argv[2])
    cl = county.lower()
    data = json.load(open(state_dir / f'{cl}_new.json'))

    keeps, rejects = [], []
    for r in data:
        ok, reason = classify(r)
        r['classification_keep'] = ok
        r['classification_reason'] = reason
        (keeps if ok else rejects).append(r)

    out = {'keeps': keeps, 'rejects': rejects, 'total': len(data)}
    json.dump(out, open(state_dir / f'{cl}_classified.json', 'w'), indent=2)
    print(f'total={len(data)} keeps={len(keeps)} rejects={len(rejects)}')
    with_web = sum(1 for k in keeps if k.get('website'))
    with_fb = sum(1 for k in keeps if k.get('facebooks'))
    print(f'keeps with website: {with_web}  with FB: {with_fb}')


if __name__ == '__main__':
    main()
