---
name: construction-sweep
description: County-by-county scrape of construction builders (GCs, home builders, remodelers). Dedups across counties, classifies vs trades/suppliers, enriches via Firecrawl websites + Facebook pages. Outputs one master CSV per state.
triggers:
  - "/construction-sweep"
  - "sweep construction"
  - "scrape builders"
---

# construction-sweep

**Purpose:** Build a state-level database of construction builders by running a repeatable per-county pipeline: Apify Google Maps scrape → cross-county dedup → rules classifier → Firecrawl + FB enrichment → append to master CSV.

**First time on this machine?** Read `SETUP.md` in this skill dir FIRST. Verify prereqs before invoking.

## Invocation

User types one of:
- `/construction-sweep <State>` — pick next undone county, run full pipeline
- `/construction-sweep <State> <County>` — run specific county
- `/construction-sweep <State> --status` — show progress, stats, next county
- `/construction-sweep <State> --bootstrap` — initialize state folder (idempotent)
- `/construction-sweep <State> --dry-run` — confirm next county + est cost, no API calls

State folder defaults to `./<State>/` in cwd. Override with `--dir <path>`.

## Pipeline (per county)

Each step writes a checkpoint file so a crash doesn't restart from scratch. Resume by re-running same county — skill detects completed stages and skips.

| # | Stage | Script | Input | Output | Wait |
|---|---|---|---|---|---|
| 1 | Bootstrap state | `scripts/bootstrap_state.py <state> <dir>` | state name | master.csv + seen.json + processed.txt + counties.json | — |
| 2 | Pick next county | `scripts/pick_next_county.py <dir>` | state dir | county name | — |
| 3 | Confirm w/ user | (inline) | — | yes/no | user |
| 4 | Scrape GMaps | Apify MCP `compass/crawler-google-places` async | county + state | runId | 5-15 min poll |
| 5 | Pull dataset | Apify API `/v2/datasets/<id>/items` | datasetId | `<county>_raw.json` | — |
| 6 | Dedup county | `scripts/dedup_county.py <county> <raw> <dir>` | raw.json | `<county>_new.json` + updated seen.json + master backfills | — |
| 7 | Classify | `scripts/classify_county.py <county> <dir>` | new.json | `<county>_classified.json` | — |
| 8 | Prep enrichment | `scripts/prep_enrichment.py <county> <dir>` | classified.json | `<county>_fc_urls.json` + `<county>_fb_input.json` | — |
| 9a | FC batch submit | `scripts/submit_firecrawl.py <county> <dir>` | fc_urls.json | FC batchId | 3-8 min poll |
| 9b | FB batch submit | Apify MCP `apify/facebook-pages-scraper` async | fb_input.json | Apify runId | 3-8 min poll |
| 10a | FC pull | `scripts/pull_firecrawl.py <county> <batchId> <dir>` | batchId | `<county>_fc.json` | — |
| 10b | FB pull | Apify API dataset pull | runId | `<county>_fb.json` | — |
| 11 | Append | `scripts/append_county.py <county> <dir>` | all above | master.csv row per KEEP + seen.json update | — |
| 12 | Log | append to `processed.txt` | — | — | — |

## Credentials required

- **Firecrawl API key**: `~/.firecrawl_key` (chmod 600). Get from firecrawl.dev.
- **Apify**: MCP server configured in `~/.claude.json`. Skill uses `mcp__Apify__call-actor` + public `/v2/actor-runs/<id>` endpoint (no token needed for status polls).

If either missing, abort + tell user what to install. SETUP.md has exact commands.

## Sleep/poll pattern

Use `ScheduleWakeup` tool for polling:
- After Apify scrape launch → sleep 240s, then poll `/v2/actor-runs/<runId>` for SUCCEEDED
- After FC + FB parallel launch → sleep 270s (cache-warm window), poll both
- Repeat with shorter sleeps (60-120s) if still RUNNING

**Do NOT poll in a tight loop.** Each poll burns context. Sleep ≥60s between checks.

## Error handling

| Symptom | Fix |
|---|---|
| Apify scrape fails or 0 items | Check input, retry once. If still fails, flag county + skip. |
| Firecrawl "we do not support this site" | URL in blocklist. Check `data/blocklists.json`, strip bad URL, resubmit. |
| FC pagination returns <expected | Bump `max_pages` to 100 in pull_firecrawl.py. |
| `zsh: read-only variable: status` | Rename var to `st`. |
| APIFY_TOKEN empty | Use unauth'd `/v2/actor-runs/<id>` for status. Only the MCP call-actor needs auth, MCP handles it. |
| NoneType on .lower() | Add `or ''` guards. |
| Classifier rejects obvious builder | Check if name has "Builders"/"Custom Homes"/"Construction" — manual rescue and add rule to classifier. |

Full troubleshooting in SETUP.md.

## Cost estimates

Per county (rural): ~$0.50-0.80
Per county (metro): ~$1.00-1.50
Per state (40-50 counties): ~$25-50

Breakdown:
- Apify GMaps scrape: $0.10-0.40 (7 search terms × 40 places × ~$0.002)
- Firecrawl website scrape: $0.01 × keeps with websites (~$0.20-0.80)
- Apify FB scrape: $0.01 × keeps with FB (~$0.05-0.30)

## Output schema (master.csv)

27 columns, one row per unique builder. Key columns:
- `business_name`, `counties` (pipe-sep, e.g. "Kootenai|Bonner")
- `phone`, `website`, `email_primary`, `all_emails`, `facebook`, `instagram`, `linkedin`
- `google_rating`, `google_reviews_count`
- `years_in_business`, `license_numbers` (pipe-sep)
- `services_summary`, `scope` (residential/commercial/civil/mixed)
- `category_primary`, `categories_all`, `classification_reason`
- `place_id` (dedup key)

Full schema: SETUP.md §"Master CSV schema".

## Extending to new states

1. Check if state has entry in `data/counties_by_state.json`
2. If not, user can run `--bootstrap <State>` which prompts for county list OR pulls from census FIPS (future)
3. State folder created in cwd. All per-state data stays there. Master CSV is portable.

## Sharing results

Master CSV is self-contained. Drop `<State>/master.csv` into Sheets or CRM. `counties` field pipe-separated for easy splitting.

For teammate handoff: zip `<State>/` folder — includes master + seen index + processed list, so another teammate can resume the sweep from where it stopped.

## Updates

When skill improves (classifier rules, blocklists, scripts):
1. `cd ~/.claude/skills/construction-sweep && git pull`
2. State folders unaffected — only skill internals change
3. Check `CHANGELOG.md` for breaking changes

See SETUP.md for install/update workflows.
