---
name: consulting-engagement-letter
description: >
  Generate professional consulting engagement letters as Word documents (.docx).
  Use this skill whenever the user asks for an engagement letter, consulting agreement,
  statement of work for consulting or coaching, training engagement proposal, or any
  letter that outlines the terms of a consulting/coaching/training engagement with a client.
  Also trigger when the user mentions 'SOW', 'letter of engagement', 'consulting proposal',
  'coaching agreement', or wants to formalize a client conversation into a professional
  document for signature. Produces a polished, branded Ruh AI engagement letter with
  outcome-based framing, pricing, guarantee, and signature blocks.
  Triggers on: "engagement letter", "consulting agreement", "SOW", "statement of work",
  "letter of engagement", "consulting proposal", "coaching agreement", "put together a letter",
  "send them something to sign", "formalize this engagement".
allowed-tools: Bash, Read, Write, Glob
---

# Engagement Letter Generator

## Overview

This skill creates professional consulting engagement letters as branded .docx files. The letters are outcome-based (never hourly), include a satisfaction guarantee, an agent build credit offer, and are ready for client signature.

## When to Use

- User says "create an engagement letter" or "put together an engagement letter"
- User wants to formalize a consulting, coaching, or training engagement
- User references a client conversation and needs a professional proposal document
- User mentions SOW, letter of engagement, consulting proposal, or coaching agreement
- User wants to send a client something to sign for a consulting engagement

## Step 1: Gather Information

Before generating the letter, collect the following. If the user has already provided some of this in conversation, extract it — don't re-ask. For anything missing, ask the user.

### Required Information

| Field | Description | Example |
|-------|-------------|---------|
| Client Name | Primary contact / decision maker | David Gallo |
| Company Name | Client's company | Gallo Construction |
| Participants | Who will be in the sessions (names if known, or just count) | David Gallo, David, Ryan |
| Engagement Type | What are we helping them with? | Claude AI enablement, workflow automation |
| The Outcome | What will participants walk away with? | Configured Claude environment, custom Skills, working workflows |
| Price | Flat fee for the engagement | $5,000 |

### Optional Information (use defaults if not provided)

| Field | Default |
|-------|---------|
| Client Address | [Address] / [City, State ZIP] (placeholder) |
| Max Participants | 5 |
| Additional Participant Fee | $1,500 per person |
| Payment Split | 50% on signing, 50% on completion |
| Payment Methods | Wire transfer, ACH, or check |
| Delivery Method | Video conference (Zoom or Google Meet) |
| Completion Window | 4 weeks from kickoff |
| Engagement Expiry | Must complete within 60 days of signing |
| Letter Valid For | 30 days from date |
| Refund Request Window | 14 days after final session |
| Agent Build Credit Window | 6 months |
| Sender Name | Jesse Anglen |
| Sender Title | Co-Founder & CEO, Ruh AI |
| Sender Contact | [email] \| [phone] |

## Step 2: Generate the Letter

Use the `docx` npm package to generate a professional .docx file. The full reference template is at `references/letter-template.js` within this skill's directory.

To locate the template at runtime:

```bash
# The template lives alongside this SKILL.md
SKILL_DIR="$(find ~/.claude/skills/engagement-letter/references -name 'letter-template.js' 2>/dev/null | head -1)"
# Fallback: check the shared repo
if [ -z "$SKILL_DIR" ]; then
  SKILL_DIR="$(find ~/SharedSkillsLuke/skills/engagement-letter/references -name 'letter-template.js' 2>/dev/null | head -1)"
fi
```

### Generation Process

1. Read the reference template at `references/letter-template.js`
2. Create a copy of the script in a temporary working directory
3. Modify the `CONFIG` object with all the gathered client information
4. Ensure `docx` is available: `npm list -g docx >/dev/null 2>&1 || npm install -g docx`
5. Run `node <script>` to generate the .docx
6. Present the generated file to the user

### Document Structure

The engagement letter follows this exact structure:

1. **Header** — Ruh AI branding with company name and tagline
2. **Date & Addressee** — Today's date, client name, company, address
3. **Opening Paragraph** — Thank them, reference the conversation, state purpose
4. **Section 1: The Outcome** — What participants walk away with (outcome-based, never hourly)
5. **Section 2: How We Get There** — Four phases: Discovery → Plan → Build → Verify & Handoff
6. **Section 3: Participants** — Named list, additional participant pricing, max group size
7. **Section 4: Investment** — Pricing table (flat fee, no hourly), payment terms
8. **Section 5: Logistics** — Delivery method, scheduling, completion window
9. **Section 6: Prerequisites** — What participants need ready (Claude subscription, desktop app, tool access)
10. **Section 7: Scope & Boundaries** — What's NOT included (agent builds, retainers, licensing, strategy consulting)
11. **Section 8: Term & Cancellation** — Validity, cancellation terms, deposit policy, completion deadline
12. **Section 9: Satisfaction Guarantee** — Full refund if no value gained, attendance required, 14-day request window
13. **Section 10: Agent Build Credit** — Full engagement fee credited toward agent build within 6 months
14. **Closing** — Warm sign-off from sender
15. **Signature Block** — Signature, printed name, title, date lines for client

## Critical Rules

- **NEVER quantify hours.** The engagement is a flat fee for an outcome. Do not mention hours, hourly rates, or time estimates anywhere in the letter.
- **Outcome-first framing.** Lead with what they get, not what we do. The "How We Get There" section describes the progression without quantifying time.
- **Use the four phases exactly:** Discovery → Plan → Build → Verify & Handoff.
- **Always include the satisfaction guarantee and agent build credit** unless the user explicitly says to remove them.
- **Brand colors:** Primary: `1B3A5C` (dark navy), Accent: `666666` (gray for subtitles/notes).
- **Font:** Arial throughout. Title 18pt, H1 16pt, H2 13pt, body 11pt.
- **Page size:** US Letter (12240 x 15840 DXA), 1-inch margins.

## Customization Points

The user may want to customize:

- **The Outcome section** — Different deliverables based on engagement type. For AI enablement it's configured environments, custom Skills, working workflows, documentation, and confidence to continue. For other engagements, adapt accordingly.
- **How We Get There** — The four phases stay the same but the description within Build should reflect what's actually being built.
- **Scope & Boundaries** — Adjust what's excluded based on what the engagement IS.
- **Price and payment terms** — May want different splits, different totals, or different payment methods.
- **Agent Build Credit window** — Default 6 months but may vary.
- **Prerequisites** — Different depending on whether it's Claude training, agent consulting, etc.
- **Follow-up teaser** — Optional paragraph mentioning future agent work. Include if relevant to the conversation, omit if not.
- **Sender** — Default is Jesse Anglen but could be Luke or another team member.

## Step 3: Deliver

1. Generate the .docx using the process above
2. Tell the user where the file was saved
3. Offer to adjust any section before they send it to the client

## Dependencies

- `docx` npm package (`npm install -g docx` if not already installed)
- Node.js
- The reference template at `references/letter-template.js`
