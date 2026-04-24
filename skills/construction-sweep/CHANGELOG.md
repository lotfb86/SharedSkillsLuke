# Changelog

## 1.0.0 — 2026-04-24

Initial release. Extracted from the Idaho pilot (Kootenai + Bonner + Boundary, 310 builders).

**Features:**
- Per-state folder with master CSV + dedup index
- Cross-county dedup (placeId > domain > phone > name+city)
- Rules classifier: 60+ hard-reject primaries, name-signal rescue for vague metadata
- Firecrawl website enrichment with pagination + blocklist
- Apify Facebook page enrichment
- License extraction: RCE- (ID), CCB# (OR), keyword-anchored generic
- Scope detection: residential / commercial / civil / mixed
- Year-in-business extraction
- Idempotent bootstrap
- Resume-safe via checkpoint files

**Curated counties:** Idaho (44), Washington (39), Montana (56), Oregon (36).
Others can be added to `data/counties_by_state.json`.

**Lessons encoded:**
- Blocklist: facebook/instagram/yelp/solarroadways/rymaps/merchantcircle/acehardware
- License regex requires contractor keyword context (avoids image-filename false positives)
- Classifier rescues "Builders"/"Custom Homes" names with vague primary
- FC pagination cap 100 pages (previously 20 missed 28% of results)
- Shell var `status` is zsh-reserved, rename to `st`
- Apify `/v2/actor-runs/<id>` works unauthenticated for status polls
