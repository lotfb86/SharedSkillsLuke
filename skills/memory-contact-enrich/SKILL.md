---
name: memory-contact-enrich
description: >
  Enrich the memory-kb contact registry into compounding person pages. For each contact
  with new activity, build or update knowledge/concepts/people/{slug}.md by scanning
  daily logs, inferring company from email domain, and optionally WebSearching for
  role/company details. Idempotent, batched, wikilinks into existing concepts.
  Triggers on: "enrich contacts", "update person pages", "build contact pages",
  "refresh contact registry", "contact enrich", "/memory-contact-enrich".
user_invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch
---

# Contact Enrichment for Memory Knowledge Base

Compound the contact registry into searchable person pages. Each person gets one file
in `knowledge/concepts/people/` that grows over time as new interactions land in
`daily/` logs. Built for team-wide memory — Luke *and* Jesse lose context on recurring
contacts, not just new ones.

## Process

### 1. Resolve the memory-kb root

Detect the active memory-kb directory in this order:

1. `$HOME/Documents/RandomStuff/memory-kb/` (Jesse's path)
2. `$HOME/random stuff/memory-kb/` (Luke's path)
3. If neither exists, ask the user for the path and stop.

Let `KB` = the resolved absolute path. All subsequent paths are relative to `KB`.

### 2. Load the contact registry

Read `{KB}/state/calendar-contacts.json`. If the file doesn't exist or has zero contacts,
report "No contacts to enrich" and stop.

### 3. Select enrichment candidates

A contact is a candidate if **all** of these are true:

- `event_count >= 2` (filter one-off meeting attendees)
- Not in the exclusion set (see below)
- Either:
  - No person page exists at `knowledge/concepts/people/{slug}.md`, OR
  - Page exists but its `updated` frontmatter date is older than `last_seen`, OR
  - Page exists with `enrichment_tier: 1` and `event_count >= 3` (eligible for Tier 2 upgrade)

**Exclusions (skip always):**
- Luke's own emails: `luke@ruh.ai`, `lukevanvalin@gmail.com`, `luke@rapidinnovation.io`
- Jesse's own emails: `jesse@ruh.ai`, `jesse@rapidinnovation.io`, `jesseanglen@gmail.com`
- Generic/system: anything matching `noreply@`, `no-reply@`, `support@`, `notifications@`, `calendar-notification@`, `@resource.calendar.google.com`
- Unknown-name contacts where the registry has no `name` AND the email local-part is <3 chars

**Slug rule:**
- Primary: lowercase first-last from `name`, hyphenated (e.g., "Jack Smith" → `jack-smith`)
- Fallback if no name: email local-part, lowercase (`jsmith@pcl.com` → `jsmith`)
- Collision: append `-` + domain stem (`jsmith-pcl`)

### 4. Cap the batch

Process at most **5 candidates per run** (prevents cost blowouts and lets the user review
output before the next batch). Order candidates by `last_seen` descending — most recent
first. If more than 5 candidates exist, report the count at the end.

### 5. Tier 1 enrichment (always)

For each candidate, gather:

**Identity signals:**
- `email` and `name` from the registry
- **Company** inferred from email domain, using this logic:
  - Strip common TLDs (`.com`, `.io`, `.ai`, `.co`) and subdomains
  - Skip generic-email domains: `gmail.com`, `yahoo.com`, `hotmail.com`, `outlook.com`, `icloud.com`, `me.com` → company = `Unknown (personal email)`
  - Otherwise, company = title-cased domain stem (`pcl.com` → `PCL`, `dondlinger.com` → `Dondlinger`)

**Daily-log scan:**
- Grep `{KB}/daily/*.md` for the contact's full name AND their email
- For each matching daily log, extract:
  - The entry heading (e.g., `## Calendar: PCL Workshop @ 10:00-11:30 PT`)
  - The date (from the filename)
  - Any `### Decisions Made`, `### Action Items`, or `### Key Exchanges` bullets under that entry
- Build a `meeting_history` array: `[{date, title, decisions, actions, source_path}, ...]`

**Concept cross-reference:**
- Grep `{KB}/knowledge/concepts/*.md` (excluding `people/`) for the contact's name
- For each hit, record the concept slug for a `[[wikilink]]` in the Related Concepts section

### 6. Tier 2 enrichment (opt-in, conditional)

Run Tier 2 only if **all** of:
- Contact has `event_count >= 3`
- Either the person page has never been Tier-2 enriched, OR `last_seen` is newer than the
  last Tier 2 run by 30+ days
- User hasn't passed `--no-web` in the invocation

Tier 2 actions:
- `WebSearch` for `"{Full Name}" {Company}` — extract role/title if a high-confidence
  match appears (LinkedIn, company site, press releases)
- `WebSearch` for `{Company} news` — capture 1-2 recent newsworthy items (funding,
  launches, leadership changes) from the past 90 days
- Only record facts with a source URL. Never invent role/title from inference alone.

If Tier 2 finds nothing verifiable, set `enrichment_tier: 1` and skip web fields.

### 7. Write or update the person page

Path: `{KB}/knowledge/concepts/people/{slug}.md`

**If new file**, use this template:

```markdown
---
title: {Full Name}
aliases: [{email local-part}, {any nicknames found in logs}]
tags: [contact, {company-slug}]
source: multi
people: ["{Full Name}"]
sources:
  - daily/YYYY-MM-DD.md
email: {email}
company: {Company}
role: {Title or empty}
first_seen: YYYY-MM-DD
last_seen: YYYY-MM-DD
event_count: N
enrichment_tier: 1
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# {Full Name}

## Core
{2-4 sentence summary: who they are, how we know them, what matters most for the next
conversation. Pull from daily logs, not invention.}

## Identity
- **Email:** {email}
- **Company:** {Company}  ({[[company-concept-link]] if the concept exists})
- **Role:** {Title if known, else "Unknown"}
- **First met:** {first_seen}
- **Last seen:** {last_seen}
- **Total interactions:** {event_count}

## Relationship Context
{Paragraph: how we know them, what stage the relationship is in (prospect / active
deal / closed / vendor / peer), what they care about. Pull from meeting-history
decisions and exchanges. If unknown, write "No context yet — first enrichment pass.".}

## Topics Discussed
{Bulleted list of distinct topics surfaced in meeting history. Use [[wikilinks]] to
concept articles that already cover those topics.}

## Meeting History
{Reverse-chronological list — newest first. One line per meeting:}
- YYYY-MM-DD — {Meeting title} — {1-line outcome} ([daily/YYYY-MM-DD.md]({relative path}))

## Open Items
{Pull from `### Action Items` in daily logs that reference this person. Format as
checkbox list. Omit section if none.}
- [ ] {action}

## Notes
{Free-form: communication style, preferences, things the user has flagged to remember.
Start empty; append over time. Add "(auto-generated — edit freely)" on first creation.}

## Related Concepts
{[[wikilinks]] to concepts found in Step 5's cross-reference scan.}

## Sources
{Every daily log that contributed. Include specific claims:}
- daily/YYYY-MM-DD.md — {what this log contributed, e.g., "first meeting, role mentioned"}
```

**If updating existing file:**

1. Read the current file. Preserve everything in `## Notes` verbatim (user-editable).
2. Merge new `meeting_history` entries into `## Meeting History` (deduplicate by date + title).
3. Update frontmatter: `last_seen`, `event_count`, `updated`, and (if Tier 2 ran) `role`, `enrichment_tier: 2`, `sources` additions.
4. Refresh `## Core` only if the contact's recency or role changed materially.
5. Append new topics and related concepts; don't remove existing ones.
6. Append new daily-log references to `## Sources`.

### 8. Update the contact registry

Back in `{KB}/state/calendar-contacts.json`, for each enriched contact add/update:

```json
{
  "last_enriched": "ISO-timestamp",
  "enrichment_tier": 1 | 2,
  "page_path": "knowledge/concepts/people/{slug}.md"
}
```

Preserve all other fields. Never remove contacts.

### 9. Update the knowledge index

Append a row to `{KB}/knowledge/index.md` for each new person page. Update the `Updated`
column for modified pages. Skip if the page was unchanged.

Format: `| [[people/{slug}]] | {1-line summary from Core} | daily logs | YYYY-MM-DD |`

### 10. Append to the operations log

Add one entry to `{KB}/knowledge/log.md`:

```
[ISO-timestamp] CONTACT_ENRICH: {N} contacts processed, {M} new pages, {K} updated, {L} Tier 2 runs
```

### 11. Report to user

Summarize in the chat response:
- Number of candidates found vs. processed (flag if capped at 5)
- Names of people enriched (with page paths as markdown links)
- Any Tier 2 findings worth highlighting (new roles, recent company news)
- Any candidates skipped and why (e.g., "3 skipped: under event_count threshold")

## Invocation Modes

- **Default:** batch of 5, Tier 1 always, Tier 2 where eligible
- **`--no-web`:** Tier 1 only, skip all WebSearch calls
- **`--person "{name or email}"`:** force-enrich one specific contact, bypass batch cap
- **`--dry-run`:** report what would be enriched without writing files

## Anti-Patterns

- **Don't** invent roles, titles, or company facts. Every claim needs a source
  (daily log reference or web URL).
- **Don't** overwrite the `## Notes` section — it's user-curated.
- **Don't** create pages for contacts with `event_count = 1` — noise risk.
- **Don't** skip the `updated` frontmatter bump — breaks idempotency.
- **Don't** exceed 5 contacts per run without explicit user override.
- **Don't** Tier-2 enrich the same contact more than once every 30 days.

## Chaining

This skill composes naturally after `memory-calendar-ingest` (fresh contacts) and
`memory-email-ingest` (fresh interactions) and before `memory-compile` (so person
pages are current when concepts are built). Typical morning flow:

```
memory-calendar-ingest → memory-email-ingest → memory-contact-enrich → memory-compile
```
