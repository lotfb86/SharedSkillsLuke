---
name: msa-generation
description: >
  Generate enterprise Master Services Agreements (MSAs) with accompanying proposals as
  Word documents (.docx). Use this skill whenever the user asks to create an MSA, master
  services agreement, service agreement, SaaS agreement, platform license agreement, or
  AI agent deployment contract. Also trigger when the user wants to formalize a client
  engagement that involves ongoing platform access, agent deployment, or technology licensing.
  This skill ingests meeting transcripts, presentations (.pptx), notes, and directory context
  to produce a complete MSA with scope of work, pricing, IP protections, performance milestones,
  and data portability provisions. Produces a polished, branded Ruh AI MSA ready for client
  signature.
  Triggers on: "MSA", "master services agreement", "service agreement", "create an MSA",
  "put together a contract", "draft the agreement", "formalize this deal", "SaaS agreement",
  "platform license", "agent deployment contract", "write up the MSA", "generate the contract".
allowed-tools: Bash, Read, Write, Glob, Grep, Agent
---

# MSA Generation Skill

## Overview

This skill creates enterprise-grade Master Services Agreements with integrated business proposals as branded .docx files. The MSA is designed for AI agent deployment engagements where Ruh AI builds, deploys, and operates autonomous agents on its proprietary platform for a client.

The generated MSA combines a business proposal (market opportunity, cost analysis, scope of work) with binding legal terms (IP, payment, termination, performance milestones, data portability) in a single document ready for signature.

## When to Use

- User says "create an MSA" or "put together a contract" for a client
- User wants to formalize an AI agent deployment engagement
- User has meeting notes, transcripts, or presentations from a client discovery call and needs to turn them into a formal agreement
- User mentions master services agreement, service agreement, or platform license
- User references a client conversation and needs a comprehensive proposal + contract document

## Step 1: Gather Context and Information

Before generating the MSA, collect information from all available sources. The skill should actively ingest:

### Source Materials to Look For

1. **Meeting transcripts** — Extract client pain points, current state, desired outcomes, budget signals, key stakeholders, and any verbal commitments
2. **Presentations (.pptx)** — Extract scope details, phasing, pricing, and deliverables from existing slide decks. Use `python3 -c "from pptx import Presentation; ..."` to extract text
3. **Notes and documents** — Read any .md, .txt, .docx, or .pdf files the user points to
4. **Directory context** — Scan the working directory for relevant files (proposals, keyword research, competitor analysis, etc.)

### Required Information

Collect from sources or ask the user for anything missing:

| Field | Description | Example |
|-------|-------------|---------|
| Client Company | Legal entity name | Spyder Construction, LLC |
| Client State | State of organization | Colorado |
| Client City | Principal place of business | Littleton, Colorado |
| Client Contacts | Name(s) and title(s) of signers | Charlie Pappas, CEO; Damien Krebsbach, VP of Sales |
| Agent Type | What kind of agent is being deployed | AI Marketing Engine |
| Phase Label | Phase number and name | Phase 1: AI Marketing Engine |
| Build Fee | One-time build and deployment fee | $20,000 |
| Monthly Fee | Ongoing platform license fee | $2,000/month |
| Payment Split | Build fee installment structure | 50% on signing, 50% on go-live |
| PPC/Ad Spend | Recommended client ad budget (separate) | $3,000–$6,000/month |
| Token Cost Estimate | Estimated monthly LLM API costs | $50–$300/month |
| Timeline | Build and deployment timeline | 8 weeks (2 discovery, 4 build, 2 testing) |
| Initial Term | Contract duration | 12 months |

### Optional Information (use defaults if not provided)

| Field | Default |
|-------|---------|
| Provider Entity | Ruh AI, Inc. |
| Provider State | Delaware corporation |
| Provider Location | Northern Idaho |
| Provider Contacts | Jesse Anglen, CEO; Luke Van Valin, VP of Sales |
| Renewal Term | 12-month auto-renewal |
| Non-renewal Notice | 30 days |
| Termination for Convenience Notice | 60 days (after initial term) |
| Cure Period | 30 days |
| Late Payment Interest | 1.5% per month |
| Confidentiality Survival | 3 years |
| Liability Cap | 12 months fees |
| Governing Law | State of the client (show good faith) |
| Transition Assistance | 30 days, up to 10 hours |
| Payment Terms | Net 15 |
| Content Review Window | 48 hours |

## Step 2: Build the Market Opportunity Section

If source materials contain keyword research, competitive analysis, or market data, build a compelling market opportunity section. This section should include:

1. **Market Context** — Why this client's niche is underserved digitally
2. **Keyword Data** — Actual search volumes, CPC estimates, competition levels (if available)
3. **Competitive Landscape** — What competitors are (or aren't) doing online
4. **Cost Comparison** — AI agent vs. traditional agency (annual cost table)

### ROI Framing Rules

**CRITICAL: Never use specific ROI multipliers or inflated revenue projections.**

- Frame returns as "revenue opportunity" not "ROI"
- Use language like "closing even one additional deal per quarter would represent a significant return relative to the marketing investment"
- Never state specific multipliers (e.g., "12x–125x return")
- Never project specific revenue ranges from the marketing investment alone
- Let the client's own knowledge of their job values and close rates fill in the math
- The goal is credibility, not hype

## Step 3: Generate the MSA Document

Use python-docx to generate the .docx file. The full reference structure is at `references/msa-structure.md` within this skill's directory.

### Generation Process

1. Read the reference structure at `references/msa-structure.md` for section-by-section guidance
2. Create a Python script using python-docx to generate the document
3. Populate all sections with gathered information
4. Ensure python-docx is available: `python3 -c "import docx" 2>/dev/null || python3 -m pip install python-docx`
5. Run the script to generate the .docx
6. Present the generated file to the user

### Document Structure

The MSA follows this exact structure:

1. **Cover Page** — Ruh AI branding, document title, phase label, client name, contacts, date, confidential
2. **Executive Summary** — Client's current state, the opportunity, what this proposal covers
3. **Section 1: Market Opportunity** — Digital landscape, keyword data, competitive analysis (if applicable)
4. **Section 2: Cost Analysis** — AI agent vs. traditional alternative, annual comparison table, projected results
5. **Section 3: Scope of Work** — Deliverables, timeline, what client provides
6. **Section 4: Master Services Agreement** — Services description, engagement structure (SaaS/license, not work-for-hire)
7. **Section 5: Fees & Payment Terms** — Fee schedule table, payment terms, late payment
8. **Section 6: Intellectual Property & Ownership** — Provider IP, license grant, client data, content ownership, no reverse engineering, **data portability & transition assistance**
9. **Section 7: Term & Termination** — Initial term, renewal, termination for convenience/cause, effect of termination, survival
10. **Section 8: Confidentiality** — Mutual obligations, exclusions, survival period
11. **Section 9: Limitation of Liability & Performance** — Liability cap, performance disclaimer, third-party platforms, **performance milestones**, **service levels (SLA)**
12. **Section 10: General Provisions** — Independent contractor, governing law, entire agreement, notices, severability, assignment (with client termination right on assignment)
13. **Signature Page** — Signature blocks for both parties

### Key Provisions That Must Be Included

These provisions are non-negotiable and reflect our commitment to fair dealing:

#### Data Portability (Section 6.6)
Upon termination, deliver to client within 30 days:
- All keyword research, market segmentation, content strategy docs
- PPC campaign configurations, ad copy, audience targeting, performance data
- Content calendars and publishing schedules
- Analytics reports and dashboards
- 30-day transition assistance (up to 10 hours, no charge)
- Explicit carve-out: nothing grants rights to Provider's platform, agent code, AI models, or underlying technology

#### Performance Milestones (Section 9.4)
- Milestones conditioned on client fulfilling their obligations (ad spend, content publishing, platform access)
- If client fails their obligations, corresponding milestone is waived
- Month 6 exit ramp: client can terminate with 30 days' notice if milestone missed (and client met all obligations)
- Pro-rated build fee refund on early termination
- Mutual adjustment clause for market changes
- Measurement via shared analytics dashboards

#### Content Volume Framing
- Present as "capacity to produce up to X per day"
- State practical target as quality-controlled output (e.g., "15–25 high-quality articles per week")
- Include content review process: weekly digest, 48-hour flag window, 1-business-day removal

#### Service Levels
- 99% monthly uptime (excluding scheduled maintenance)
- 24-hour response for unscheduled disruptions
- Scheduled maintenance during off-peak hours (10 PM – 6 AM local)

#### Assignment
- Neither party assigns without consent
- Provider may assign in M&A
- Client gets 30-day termination right upon Provider assignment

## Critical Rules

- **This is a SaaS/license engagement, not work-for-hire.** Always frame as client licensing access to the agent and platform, not purchasing ownership of software or IP.
- **Protect the underlying technology.** All platform code, agent architecture, prompt engineering, workflow automations, and AI models remain Provider's exclusive property. The data portability provisions only cover client-specific outputs and configurations.
- **Performance milestones must be conditioned on client obligations.** Never commit to outcomes that depend on client actions (ad spend, content publishing) without conditioning the milestone on the client fulfilling those obligations.
- **ROI claims must be credible.** Use revenue opportunity framing. Never use specific multipliers. Let the math speak for itself.
- **Content volume = capacity, not commitment.** Frame as what the agent can do, with practical quality-controlled targets.
- **Governing law should favor the client's state** as a good-faith gesture, unless the user specifies otherwise.
- **Brand styling:** Primary color `1E2761` (navy), accent `4472C4` (blue). Font: Georgia for headings, Calibri for body. US Letter page size with 1-inch margins.

## Step 4: Customize Performance Milestones

Performance milestones must be tailored to the specific engagement. For each milestone:

1. **Define the metric** — What is being measured (traffic, leads, content published, etc.)
2. **Set a conservative threshold** — Should be easily achievable if both parties perform; set at ~50% of realistic expectations
3. **Define the client obligation** — What must the client do for this milestone to apply
4. **Define the remedy** — What happens if missed (remediation plan, termination right, refund)

### Example Milestone Structure (Marketing Agent)

| Timeframe | Milestone | Client Obligation | Remedy |
|-----------|-----------|-------------------|--------|
| Month 3 | 75+ content pages published and indexed | Client publishes 80%+ of delivered content within 5 business days | Remediation plan within 10 days |
| Month 4 | PPC campaigns live, 1,000+ impressions/mo | Client maintains $3K/mo minimum ad spend | Remediation plan within 10 days |
| Month 6 | 750 organic visits/mo OR 3 qualified leads/mo | Client maintained all obligations for preceding 3 months | Client may terminate; pro-rated build refund |
| Month 9 | 1,500 organic visits/mo AND 5 qualified leads/mo | All obligations maintained continuously | Remediation plan; good-faith discussion |
| Month 12 | 3,000 organic visits/mo | All obligations maintained continuously | No auto-renewal if missed |

For non-marketing agents (estimation, personnel, operations), adjust milestones to the relevant KPIs (e.g., estimate turnaround time, hire-to-start time, error rates).

## Step 5: Deliver

1. Generate the .docx using the process above
2. Tell the user where the file was saved
3. Offer to adjust any section before sending to the client
4. Offer to generate a companion slide deck if needed (reference the `ruh-proposal` skill)

## Dependencies

- `python-docx` Python package (`python3 -m pip install python-docx` if not already installed)
- Python 3
- The reference structure at `references/msa-structure.md`
