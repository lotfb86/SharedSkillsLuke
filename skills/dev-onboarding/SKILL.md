---
name: dev-onboarding
description: >
  Turn a deal folder (transcripts, proposals, MSA, POC outputs, skill files) into a
  structured developer onboarding document that brings a Ruh.AI engineering team from
  zero context to productive in ~4 hours. The output covers: who the client is, industry
  primer, current-state workflow, agent product spec, technical architecture, training
  pipeline, commercial + SLA envelope, risks and gotchas, and prioritized open questions.
  Use this skill whenever a deal has closed (verbal or signed) and the dev team needs to
  assume the build. Delivers markdown, Word (.docx), and PDF outputs in the same folder.
  Triggers on: "dev onboarding doc", "dev team onboarding", "engineering handoff",
  "bring dev team up to speed", "developer onboarding", "handoff doc", "turn this folder
  into a dev doc", "build context doc", "engineering brief", "onboard the engineers",
  "scaffold for the build team", "dev team context document".
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent
---

# Dev Team Onboarding Document Generator

## Overview

This skill turns a **deal folder** — transcripts, proposals, an MSA, POC outputs, a skill file — into a comprehensive onboarding document that a Ruh.AI engineering team can read to ramp on a new agent-build. The output is a single markdown file plus polished .docx and .pdf versions, all saved alongside the source materials.

The pattern: Ruh sells an autonomous AI agent to a client, the deal closes, and a new engineering team now has to build it without having sat in the sales calls. This skill extracts everything they need to be productive.

---

## When to Use

Trigger when any of the following happens:

- A Ruh.AI deal has just closed (verbal or signed) and the build team needs to be onboarded.
- The user says something like "create a dev onboarding doc for [deal]", "turn this folder into a dev handoff", "bring the engineering team up to speed", "make me a build context doc", "engineering brief for [client]".
- The user references a folder of meeting transcripts + proposals + POC materials and asks for a consolidated ramp-up document.

**Do NOT use this skill for:**
- Client-facing deliverables (those use `product-deck-skill` or `ruh-proposal`).
- Creating the initial sales proposal (that's `ruh-proposal` or `consulting-engagement-letter`).
- Writing the agent's skill file (that's the SKILL.md inside the build itself, not this skill).

---

## Inputs You Expect in the Deal Folder

Not all will be present for every deal. Work with what's there and flag what's missing.

| Input | What it provides | How to handle if missing |
|---|---|---|
| **Meeting transcripts** (`.txt`, `.md`, Fireflies/Otter/Bubbles exports) | Authority hierarchy, IT constraints, customer pain, verbal commitments, unspoken process nuance. | Ask the user if there are any recordings or notes; if truly none, proceed with a caveat in the doc. |
| **Proposals** (`.md`, `.pdf`, `.pptx`) | Scope, pricing, timeline, deliverables. The final (accepted) version is the source of truth. | Ask which version was accepted; warn the user if only drafts exist. |
| **MSA / contract** (`.docx`, `.pdf`) | Commercial terms, milestone definitions, performance exit ramps, IP boundary, SLA, data portability. | Flag explicitly — without the MSA, §7 (Commercial + SLA) is speculative. |
| **POC output packages** (folders with `*_Master_*Package*.md`, `*_RFQ_*.md`, `*_Decision_Log*.md`, etc.) | The deliverable contract in action. Shows the dev team what the agent actually produces. | Skip §4.5 (POC Lessons); note the gap. |
| **Agent skill file** (`SKILL.md` pre-training baseline) | The agent's brain design — phases, standards, scope buckets, authority hierarchy. | Note that the dev team will need to draft it in Week 1 discovery. |
| **Memory files** (`memory/*.md` from the user's auto-memory) | Project history, team context, prior decisions. | Not required, but read if present — they often contain critical backstory. |

---

## PHASE 1: Inventory the Deal Folder

Before reading anything, run a directory scan. Produce an inventory so you know what you're working with.

```bash
ls -la <deal-folder>
# and for any subdirectories:
find <deal-folder> -maxdepth 3 -type f | sort
```

**Classify each file** into one of the input categories above. Note:
- Which transcripts exist and their apparent stage (first discovery / POC debrief / commercial close / etc. — often inferrable from filename or first lines).
- Which proposal version is latest / final. Look for filenames like `FINAL`, `V2`, `_signed`, or go by modification date.
- Whether a POC output folder exists and is complete (multiple deliverables) vs. partial.
- Whether the MSA is signed (check for signature-block text) or still a draft.
- Whether any memory files contain relevant project context.

**Output of Phase 1:** a short inventory summary posted back to the user, noting:
- ✅ What's present and will feed into each section of the doc.
- ⚠ What's missing and what the downstream impact will be.

If critical inputs are missing (no transcripts AND no proposal), stop and ask the user where to find them before proceeding.

---

## PHASE 2: Extract in Parallel

Read the artifacts and extract structured facts. **Use subagents aggressively** — transcripts can be 80k+ tokens each and will blow out your context if you read them directly.

### Transcripts → delegate to a subagent

For each transcript (or the set as a whole), spawn a `general-purpose` agent with a focused prompt. The prompt must:
- Identify the call's stage, participants, and approximate date.
- Pull out: technical/process details (tools, file locations, workflow steps), authority structure cues, integration constraints, client fears/objections, verbal commitments from our side, named preferences, terminology the dev team will need.
- Return a summary of ~1500-2500 words structured as: Call 1 / Call 2 / ... / Cross-call themes / Hard technical constraints / Industry terminology glossary.
- Explicitly exclude anything that's already in the written proposal.

Do NOT read transcripts directly unless they're short (<10k tokens).

### Proposal → read directly

Read the final proposal end-to-end. Extract:
- The exact scope statement ("what we're building").
- Timeline and phase breakdown.
- Pricing structure (build fee + monthly license + token costs).
- Deliverables list (what the agent produces on every estimate/run).
- Authority hierarchy if mentioned.
- ROI framing and any performance claims.

### MSA → read directly, focus on specific sections

Read §1 (Engagement), §3 (Scope), §6 (IP), §9 (Performance & SLA), and Exhibit A (Milestones). Extract:
- Exact fee amounts and payment terms.
- Milestone table with dates, definitions, and remedies.
- The exit-ramp clause (usually M6) — this is the single most important commercial gate for engineering.
- IP boundary (what we keep vs. what the client keeps).
- Data portability obligations on termination.
- SLA targets.

### POC outputs → read the Master Estimator Package (or equivalent) in full

The Master Package is the deliverable contract in action. Read it end to end — it shows the dev team what "good output" looks like. Also read any Decision Log, Takeoff Interpretation, and RFQ packets for pattern reference.

### Memory files → read if present

If the user has auto-memory files for the project, read them. They often contain the deal's backstory that isn't in any transcript.

---

## PHASE 3: Clarifying Questions — ASK BEFORE WRITING

Before producing the document, assemble a list of clarifying questions from gaps you discovered in Phase 2. Common patterns:

- **Authority hierarchy ambiguity:** "Is the lead estimator/estimator-equivalent a co-founder or a senior employee? Are they accessible to us, or do we work through a proxy?"
- **Training corpus curation:** "Who picks the N historical projects for training? What rubric?"
- **Infrastructure choices:** "Lenovo box or VM? Direct API calls or tenant-hosted proxy?"
- **Integration priorities:** "Which system is Day-1 vs. phase-2?"
- **Commercial timing:** "Is the build fee invoice-ready or gated on signature?"
- **Milestone definitions:** "What counts as a 'routine' case for the autonomous-target milestone?"
- **Naming gaps:** "What's the lead estimator's actual name?"

Post these questions to the user and **wait for answers**. Do not produce a doc with a lot of `[TBD]` placeholders — the whole point is to give engineering a dense, answered brief.

**Exception:** if the user explicitly says "draft it with placeholders, I'll fill in later," proceed, but clearly mark every placeholder with `⏳` and list them at the end of §9 for follow-up.

---

## PHASE 4: Produce the Onboarding Document

Use the template at `templates/onboarding-template.md` as the structural skeleton. Fill every section with extracted facts, not boilerplate.

### Sections (11 total)

1. **TL;DR for the Engineer Who Only Reads One Page** — 6-8 bullets covering: what we're building, what the client does, why they bought, the crucial POC/discovery finding, commercial envelope, non-negotiables from IT.
2. **The Client** — company facts (revenue, footprint, trade, project profile, labor model), key people table (with Tier-1 authority at the top), why they bought (stated pains).
3. **Industry 101** — plain-language primer for engineers who have never worked in this industry. Include: what the deliverable actually is, why it's hard, glossary of terms the dev team will hear.
4. **How the Client Works Today** — the canonical inputs, current workflow start-to-finish, file system of record, rest of the stack.
5. **The Agent: Product Specification** — four-layer architecture (Soul/Brain/Memory/Skills) mapped to the client's context, inputs the agent accepts, **authority hierarchy** (this is critical — memory model must be role-aware, not flat), outputs the agent produces every run, POC lessons.
6. **Technical Architecture & Infrastructure** — deployment target (hardware + OS), LLM access (account, rate limits), integrations (Day-1 vs. phase-2), security posture, image/vision handling, handwritten-input handling.
7. **The Training Pipeline** — **§6.0 philosophy extraction** if the client has a "source of truth" human whose judgment must be encoded (Lead Estimator, Lead Underwriter, etc.), the recursive training loop, expected trajectory, source of training projects, skill-file mechanics, build phases.
8. **Commercial + SLA Envelope** — fee structure, Exhibit A milestones with the exit ramp called out explicitly, SLA, IP boundary.
9. **Risks, Gotchas, and Engineering Landmines** — 10-15 bullets of things that will bite the dev team if they design around the happy path.
10. **Open Questions** — structured into Resolved / Luke (or user) action items / For Week-1 discovery with the client / Deferred. Number them for easy reference.
11. **Directory Contents + Recommended Reading Order** — what each file in the folder is, and the order a new engineer should read them in (target: ~4 hours to ramp).

### Voice and tone

- **Direct, dense, specific.** Every paragraph earns its place. No filler.
- **Concrete names and numbers.** If the client's CEO is named, use the name. If the deal is $30K + $2K/mo, use the numbers. Never write around specifics.
- **Flag the critical path.** Use bold, callout boxes, or ⚠ symbols for the 2-3 decisions that, if missed, sink the build.
- **First-person plural when referring to Ruh** ("we're building", "our job is to..."), third-person for the client.
- **No hallucinations.** If a fact didn't come from an artifact you read, mark it or ask the user. Lazy certainty is worse than flagged uncertainty.

---

## PHASE 5: Build the Outputs (.md / .docx / .pdf)

Write the completed markdown to `<deal-folder>/<CLIENT>_DEV_TEAM_ONBOARDING.md`.

Then run:

```bash
bash ~/.claude/skills/dev-onboarding/scripts/build_outputs.sh \
    "<deal-folder>/<CLIENT>_DEV_TEAM_ONBOARDING.md"
```

This produces `<CLIENT>_DEV_TEAM_ONBOARDING.docx` and `<CLIENT>_DEV_TEAM_ONBOARDING.pdf` alongside the markdown, using a US Letter reference doc with 0.75" margins for tighter table rendering.

**Do not include a pandoc-generated TOC.** It renders as an empty heading in LibreOffice-exported PDFs (the field doesn't auto-refresh). Section numbering + headings are enough for navigation.

If pandoc or LibreOffice (`soffice`) isn't installed, the script will note the missing dependency. Install via `brew install pandoc` and ensure LibreOffice is available at `soffice`.

---

## PHASE 6: Report Back

Summarize to the user:

1. **Where the files are** (3 paths: `.md`, `.docx`, `.pdf`).
2. **Page count + size** of the PDF.
3. **Top 3-5 action items** the user needs to resolve before Week-1 kickoff (pulled from §10 Open Questions).
4. **Any critical gaps** you couldn't close from the artifacts — things that should go into Week-1 discovery or need a follow-up conversation.
5. **Offer** to iterate on any section, produce a Week-1 discovery agenda, or generate companion artifacts (one-pager for client, extraction-interview protocol, etc.).

---

## Critical Rules

1. **Delegate transcript reading to subagents.** A single transcript can exceed 80k tokens. Use the `general-purpose` agent with a focused extraction prompt.
2. **Ask clarifying questions BEFORE writing.** A doc with 15 `[TBD]` placeholders is worse than no doc.
3. **Flag missing artifacts.** If there's no MSA, don't fake §7. Say so explicitly.
4. **Authority hierarchy is architecturally critical.** Identify the single source-of-truth human on the client side early. If they're not the same as the primary sales contact, that's the most important callout in the doc.
5. **Exit-ramp milestones matter.** If the MSA has a pro-rated refund or termination clause tied to a specific milestone (e.g., Month 6 autonomous target), call it out with its own ⚠. Engineering measurement infrastructure should be built to detect it early.
6. **Never invent commercial terms.** Fees, timelines, milestones, IP — these come from the MSA or the proposal, never from inference.
7. **Write for engineers who don't know the industry.** Include a glossary. Define every term the first time it appears. Assume zero prior exposure to the client's domain.
8. **Preserve the client's system of record.** Unless explicitly told otherwise, the dev team's job is to *wrap* existing tools, not replace them. Say so in the architecture section.
9. **Every open question gets an owner.** Luke/user to confirm, client to answer in Week 1 discovery, deferred to phase 2, etc. No orphaned questions.
10. **Output format is markdown + .docx + .pdf, in that order.** The markdown is the editable source. The .docx is for collaborative annotation. The .pdf is the frozen artifact.
