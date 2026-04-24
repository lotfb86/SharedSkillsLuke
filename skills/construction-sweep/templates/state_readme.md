# {{STATE}} — construction sweep

This folder holds the per-state data for the `construction-sweep` skill.

## Files

- `master.csv` — one row per unique builder in {{STATE}}. Multi-county builders have pipe-separated `counties` field. Portable — drop into Sheets / CRM.
- `seen.json` — dedup index (placeId / domain / phone / name+city → row idx). Do not edit by hand.
- `processed.txt` — newline-separated list of counties already swept. Used to pick next county.
- `counties.json` — full {{STATE}} county list with seats. Order = sweep default.
- `<county>_raw.json` — per-county Apify Google Maps dump (keep for debugging, re-runs).
- `<county>_new.json` — records not seen in other counties.
- `<county>_classified.json` — classifier output (keeps + rejects).
- `<county>_fc.json` / `<county>_fb.json` — Firecrawl + Facebook enrichment.

## Resume

To continue sweep: invoke `/construction-sweep {{STATE}}` — skill picks next county from `counties.json` minus `processed.txt`.

To re-run a specific county: `/construction-sweep {{STATE}} <County>` (will re-classify + re-enrich but respects dedup).

## Sharing

Zip this entire folder → teammate unzips → they can continue the sweep from where you stopped. Their `master.csv` merges automatically on next county because `seen.json` keeps the dedup keys.

## Schema

See skill's `SETUP.md` §"Master CSV schema" for column definitions.
