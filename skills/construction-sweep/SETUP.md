# construction-sweep — Setup Guide for Claude Code

**Version:** 1.0.0
**Audience:** Another Claude Code instance setting up this skill on a new machine.
**What you're installing:** A skill that runs a county-by-county scrape of construction builders into a state-level master CSV with cross-county dedup, classification, and website/FB enrichment.

---

## What this skill does

Given a state name (e.g. `/construction-sweep Idaho`), the skill:
1. Initializes a per-state folder with master CSV + dedup index + county list
2. Picks the next unprocessed county (N-to-S default order)
3. Scrapes Google Maps via Apify (`compass/crawler-google-places`) with 7 builder search terms
4. Dedups against all previously-scraped counties (placeId > domain > phone > name+city)
5. Runs a rules-based classifier to drop single-trade contractors/suppliers/services, keep GCs + home builders
6. Enriches websites (Firecrawl markdown) and Facebook pages (Apify `apify/facebook-pages-scraper`) in parallel
7. Extracts license numbers, years in business, services summary, scope, emails
8. Appends new records to master CSV, backfills overlapping records with new data
9. Logs the county in `processed.txt` so the next run continues from there

Cost per county: $0.50 (rural) to $1.50 (metro). State of 40-50 counties: $25-$50.

---

## Prerequisites checklist

Before proceeding, verify each. Report missing items to the user and HALT:

### 1. Python 3.10+
```bash
python3 --version
```
Need 3.10+. If missing → user installs via homebrew (`brew install python@3.12`) or python.org.

### 2. Firecrawl API key
```bash
test -f ~/.firecrawl_key && echo "FC key present" || echo "FC KEY MISSING"
```
If missing: user creates account at https://firecrawl.dev, grabs API key, then:
```bash
echo "fc-XXXXXXXXXXXXXXXXXXXXXX" > ~/.firecrawl_key
chmod 600 ~/.firecrawl_key
```
Key format: `fc-` prefix + 32 hex chars.

### 3. Apify MCP configured
```bash
grep -l 'apify' ~/.claude.json 2>/dev/null || echo "APIFY MCP MISSING"
```
If missing: user adds Apify to MCP settings. Apify account needed at https://apify.com. The MCP server handles auth — Claude should NOT need `APIFY_TOKEN` in shell env.

Verify MCP tools are available:
- `mcp__Apify__call-actor`
- `mcp__Apify__get-actor-run`
- `mcp__Apify__get-actor-output`

### 4. Public Apify API access (unauth)
No setup — used for polling `/v2/actor-runs/<id>` status. No token needed for reads. Test:
```bash
curl -s https://api.apify.com/v2/actor-runs/nonexistent | head -c 200
```
Should return `404` or error JSON — confirms connectivity.

---

## Installation steps

### Step 1: Place skill folder
The skill folder (this folder, containing SKILL.md + SETUP.md + scripts/ + data/ + templates/) must live at:
```
~/.claude/skills/construction-sweep/
```

If cloning from the shared repo:
```bash
# Option A: symlink from the shared repo
ln -s /path/to/SharedSkillsLuke/skills/construction-sweep ~/.claude/skills/construction-sweep

# Option B: copy
cp -R /path/to/SharedSkillsLuke/skills/construction-sweep ~/.claude/skills/construction-sweep
```

Verify:
```bash
ls ~/.claude/skills/construction-sweep/SKILL.md
```

### Step 2: Verify skill is discoverable
In Claude Code, the skill's `description:` frontmatter in SKILL.md is how Claude finds it. After install, the skill should appear in the available-skills list. If it doesn't appear after a session restart, check SKILL.md frontmatter syntax.

### Step 3: Smoke test on dummy state
```bash
cd /tmp && mkdir -p test-sweep && cd test-sweep
python3 ~/.claude/skills/construction-sweep/scripts/bootstrap_state.py Idaho .
```

Expected output:
```
created ./Idaho/master.csv
created ./Idaho/seen.json
created ./Idaho/processed.txt
created ./Idaho/counties.json with 44 counties
created ./Idaho/README.md

state dir ready: ./Idaho
```

Then verify the county picker works:
```bash
python3 ~/.claude/skills/construction-sweep/scripts/pick_next_county.py ./Idaho
```
Expected: `Boundary\tBonners Ferry\t44`

Cleanup: `rm -rf /tmp/test-sweep`

### Step 4: Ready

Tell the user: **"Skill `/construction-sweep` installed. Try: `/construction-sweep Idaho --dry-run` to pick the first county."**

---

## File inventory

| File | Role | Inputs | Outputs |
|---|---|---|---|
| `SKILL.md` | Skill entry, runtime rules | — | — |
| `SETUP.md` | This file (install guide) | — | — |
| `scripts/bootstrap_state.py <State> [<dir>]` | Init state folder | state name, optional dir | master.csv, seen.json, processed.txt, counties.json, README.md |
| `scripts/pick_next_county.py <state_dir>` | Select next undone | state dir | tab-sep: name, seat, remaining |
| `scripts/dedup_county.py <county> <raw.json> <state_dir>` | Cross-county dedup | raw records | new.json + master backfills + seen updates |
| `scripts/classify_county.py <county> <state_dir>` | Rules classifier | new.json | classified.json ({keeps, rejects, total}) |
| `scripts/prep_enrichment.py <county> <state_dir>` | Build FC+FB URL lists | classified.json | `<county>_fc_urls.json`, `<county>_fb_input.json` |
| `scripts/submit_firecrawl.py <county> <state_dir>` | Launch FC batch | fc_urls.json | `<county>_fc_batch.json` (batch id) |
| `scripts/pull_firecrawl.py <county> <state_dir>` | Pull completed FC (paginated) | fc_batch.json | `<county>_fc.json` |
| `scripts/append_county.py <county> <state_dir>` | Merge all → master | classified + fc + fb | master.csv append + seen.json update + processed.txt append |
| `scripts/merge_helpers.py` | Shared: domain/phone/fb norm, licenses, years, scope, emails, schema | — | (imported) |
| `data/counties_by_state.json` | County catalog | — | (read by bootstrap + pick) |
| `data/blocklists.json` | URLs to skip for FC/FB | — | (read by prep_enrichment) |
| `templates/state_readme.md` | Dropped into each state dir on bootstrap | — | — |

---

## Data storage layout

```
<cwd>/<State>/
├── master.csv                 # One row per unique builder. 27 cols. Portable.
├── seen.json                  # {place_id, domain, phone, name_city} → row idx
├── processed.txt              # Newline list of completed counties
├── counties.json              # Copy of state's county list w/ seats
├── README.md                  # Per-state guide
├── <county>_raw.json          # Apify GMaps dump, full
├── <county>_new.json          # Post-dedup new records only
├── <county>_classified.json   # {keeps: [...], rejects: [...], total: N}
├── <county>_fc_urls.json      # URL list submitted to Firecrawl
├── <county>_fc_batch.json     # FC batch id (for polling)
├── <county>_fc.json           # FC results (flat list)
├── <county>_fb_input.json     # Apify FB input {startUrls: [...]}
└── <county>_fb.json           # Apify FB dataset results
```

---

## Master CSV schema

27 columns. One row per unique builder. Multi-county builders have pipe-separated `counties`.

| Col | Type | Source | Notes |
|---|---|---|---|
| `business_name` | str | Apify `title` | — |
| `classification_reason` | str | classifier | why kept |
| `category_primary` | str | Apify `categoryName` | — |
| `categories_all` | str (pipe) | Apify `categories` | — |
| `address` | str | Apify | — |
| `city` | str | Apify | — |
| `counties` | str (pipe) | sweep | e.g. `"Kootenai\|Bonner"` |
| `state` | str | Apify or state arg | — |
| `postal_code` | str | Apify | — |
| `phone` | str | Apify | — |
| `website` | str | Apify | — |
| `email_primary` | str | merged | FB > FC > Apify priority |
| `all_emails` | str (pipe) | merged | dedup'd |
| `facebook` | str | Apify `facebooks[0]` | — |
| `instagram` | str (pipe) | Apify | — |
| `linkedin` | str (pipe) | Apify | — |
| `google_rating` | float | Apify `totalScore` | — |
| `google_reviews_count` | int | Apify `reviewsCount` | — |
| `years_in_business` | str | FC + FB text | e.g. "since 1998" |
| `license_numbers` | str (pipe) | FC + FB text | RCE-#### (ID), CCB#### (OR), WA-style |
| `services_summary` | str | FC markdown | best-sentence heuristic |
| `scope` | str | FC + FB text | residential/commercial/civil/mixed |
| `facebook_likes` | int | FB scrape | — |
| `facebook_followers` | int | FB scrape | — |
| `facebook_description` | str | FB `intro` | — |
| `search_term_source` | str | Apify | which query brought it in |
| `place_id` | str | Apify | dedup key |

---

## Pipeline flow (per county invocation)

Claude executes these steps. Checkpoint files enable mid-pipeline resume.

```
1. bootstrap_state.py <State>           → ensure state dir exists
2. pick_next_county.py <state_dir>      → pick next undone county
3. CONFIRM w/ user (est cost, county+seat) — skip on --yes
4. Apify call-actor compass/crawler-google-places (async)
     input: {
       locationQuery: "<County> County, <State>, USA",
       searchStringsArray: [general contractor, home builder, custom home builder,
                            construction company, commercial construction,
                            road construction, civil contractor],
       maxCrawledPlacesPerSearch: 40
     }
   → runId
5. ScheduleWakeup(240s), poll /v2/actor-runs/<runId> until SUCCEEDED
6. Pull /v2/datasets/<datasetId>/items → <county>_raw.json
7. dedup_county.py <County> <raw> <state_dir>    → <county>_new.json
8. classify_county.py <County> <state_dir>       → <county>_classified.json
9. prep_enrichment.py <County> <state_dir>       → fc_urls + fb_input
10. IN PARALLEL:
      a. submit_firecrawl.py <County> <state_dir>   → FC batch id
      b. Apify call-actor apify/facebook-pages-scraper (async) → FB runId
11. ScheduleWakeup(270s), poll both until done
12. pull_firecrawl.py <County> <state_dir>     → <county>_fc.json
    Apify /v2/datasets/<fb_dataset>/items      → <county>_fb.json
13. append_county.py <County> <state_dir>      → master.csv + seen.json + processed.txt appended
14. Report stats, ask about next county
```

### Sleep/poll guidance

- Apify GMaps scrape: 5-15 min typical. Sleep 240s first check.
- Firecrawl batch: 3-8 min typical for 20-80 URLs. Sleep 270s first check.
- Apify FB scrape: 2-5 min typical. Included in 270s window above.
- If still RUNNING after first poll, sleep 120s, check again. Avoid polls <60s apart.

---

## Troubleshooting (known failures)

| Symptom | Cause | Fix |
|---|---|---|
| `"We apologize for the inconvenience but we do not support this site"` (FC) | Blocked domain in batch | Add substring to `data/blocklists.json` firecrawl list, resubmit |
| FC returns <60% of submitted URLs | Pagination cap too low | `MAX_PAGES` in `pull_firecrawl.py` — default 100 |
| `zsh: read-only variable: status` | Reserved var | Rename shell var to `st` |
| `APIFY_TOKEN` empty in bash | MCP holds token, not shell | Use public `/v2/actor-runs/<id>` endpoint for status polls; use MCP for actor launches |
| `NoneType is not subscriptable` on `.lower()` | Missing `title`/`city` | Guards added in helpers (`or ''`) |
| Classifier rejects obvious builder | Vague primary + name has signal | Classifier has name-rescue rule for "Builders"/"Custom Homes"/"Construction". If still missed, manually move from `rejects` to `keeps` in classified.json |
| License regex false positives (image filenames) | DSCF0300, IMG_001 matched WA pattern | Helpers reject `^(DSC[FN]\|IMG\|PHOTO\|PIC\|P\d)` and standalone "License/Lic/Contractor" |
| Cross-county overlap ~0 | Different micro-markets | Normal for rural adjacent counties. Big regional brands (Hayden, StanCraft, Lexar) drive most overlap in metro-adjacent sweeps |
| `state "X" not in counties_by_state.json` | State not curated yet | Add entry to `data/counties_by_state.json` with ordered `[{name, seat}]` list. County lookup from Census FIPS: https://www.census.gov/geographies/reference-files/ |
| FC batch fails submit (400) | One URL in batch is blocked | FC fails the whole batch. Add URL's domain to blocklist, resubmit |

---

## Adding a new state

1. Find state's counties + seats (Wikipedia or Census FIPS)
2. Edit `data/counties_by_state.json`:
   ```json
   "California": [
     {"name": "Del Norte", "seat": "Crescent City"},
     ...
   ]
   ```
3. Order = sweep default. Options:
   - **North→South** (best for dedup overlap with adjacent counties)
   - **By population descending** (metro first, rural last)
   - **Alphabetical** (least effort)
4. Commit to repo so teammates get it.

---

## Updating the skill

```bash
cd ~/.claude/skills/construction-sweep  # or the shared repo path
git pull
```

State folders in cwd are independent — skill updates don't touch per-state data. Check `CHANGELOG.md` for breaking changes.

---

## Security / privacy

- Data scraped: business names, addresses, phones, public emails, public social links
- No PII beyond what's on a public business listing
- Firecrawl key: store in `~/.firecrawl_key` with 0600 perms. Don't commit keys.
- Apify: auth via MCP only. Token stays in MCP config.
- `master.csv` may contain personal emails of business owners — treat as contact list, follow CAN-SPAM if sending.

---

## Reporting issues

If Claude hits an error not in the troubleshooting table:
1. Write details to `<State>/_ISSUES.md` with:
   - County + step + timestamp
   - Full error + stack trace (if Python)
   - Relevant input (first 500 chars of raw.json or similar)
2. Notify the user with a clear "halted at step X" message
3. Suggest manual next step (retry, skip county, check key)
4. Do NOT silently continue past errors
