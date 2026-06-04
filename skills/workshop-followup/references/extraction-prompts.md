# Transcript Extraction Playbook

Six passes against the workshop transcript. Each pass scans with a different lens. Do them sequentially — earlier passes inform later ones.

When reading the transcript, **track speaker labels carefully**. If the transcript has speaker labels, use them. If not, infer from context (Jesse leads the demos; Luke is often the second Ruh voice; client attendees are named at intro). When uncertain about who said something, mark it `[Speaker?]` and surface that uncertainty.

Quote verbatim when wording matters. Paraphrase when wording is filler.

---

## Pass 1 — Jesse-isms

**Goal:** Capture the named rules, mental models, principles, and punchy directives Jesse uses to teach.

**What to scan for:**

- Phrases that sound like coined terms or named rules (often introduced with "I call this..." or "the rule is...")
- Analogies that are clearly teaching devices (e.g., the "Amelia Bedelia" analogy for literal instruction-following)
- Warnings stated as imperatives ("Never let Claude...", "Always...", "If Claude says X, do Y")
- Mantras Jesse repeats more than once in the meeting

**Reference precedents (these have appeared in past workshops):**

- **The Amelia Bedelia rule** — Claude follows instructions literally; be specific
- **Convince me you understand** — make Claude restate the task before executing
- **Don't believe it when Claude says no** — Claude often gives up early; push it
- **Inputs and review are your job** — humans own input quality and output review
- **Skills compound** — every workflow you teach Claude becomes reusable leverage

**Output format:**

```
NAMED CONCEPTS:
- [Concept name]: [one-sentence definition]
- ...

LEAD QUOTE (use as the quote-block in §Key Concepts):
"[verbatim quote]" — Jesse Anglen
```

Pick 4–8 named concepts. Pick ONE lead quote — the one that best captures the philosophy of the meeting.

---

## Pass 2 — Q&A from attendees

**Goal:** Capture moments where an attendee asked something substantive and got a useful answer.

**What to scan for:**

- Question marks in attendee turns
- Phrases like "what about...", "how would we...", "does that work for...", "can Claude..."
- Concerns about security, data, cost, scale
- Tool-specific questions ("does it work with Procore / Egnyte / Bluebeam...")

**What to skip:**

- Logistical questions ("can you share your screen?", "are you recording this?")
- Yes/no questions that got a yes/no answer

**Output format:**

```
- [Attendee name] asked: [brief paraphrase]
  → [Jesse's answer in 1–2 sentences]
- ...
```

Pick the 3–6 most substantive exchanges. These inform what to emphasize in the recap.

---

## Pass 3 — Use cases identified for THIS company

**Goal:** Build the §Use Cases section using the company's actual vocabulary.

**What to scan for:**

- "We do X" / "Our process is Y" / "We struggle with Z" statements from attendees
- Live demos where Claude tackled something specific the attendee just described
- Project names, tool names, document types specific to the company
- Industry-specific workflows (estimating, takeoffs, RFI triage, permit filing, change orders, schedule pulls)

**Critical rule:** **Use their language, not ours.**
- ❌ "Document comparison automation"
- ✅ "Plan comparison on the Acadian project — old plan set vs. new"

Each use case gets a verb-noun title:
- Plan Comparison
- Drawing Takeoffs
- Estimate Template Automation
- Procore RFI Triage
- Permit Filing
- Email Triage & Briefing
- Subcontractor Follow-Up

**Output format:**

```
1. [Title]
   [1–3 sentence description using the company's vocabulary, including a specific project name or tool if it came up]

2. [Title]
   [...]
```

Aim for 5–7 use cases. Order by what would deliver the fastest win first.

---

## Pass 4 — Artifacts shared

**Goal:** Preserve the prompts and configs that would die when the meeting ends.

**What to scan for:**

- Long blocks of text Jesse typed into Google Meet chat (often pasted in mid-demo)
- Prompts Jesse dictated out loud while demoing
- Configuration steps shown on screen (connector toggles, MCP installs, settings changes)
- Links shared (tools, repos, docs, install guides)

**What to capture for each prompt:**

1. **Title** — short verb-noun (e.g., "Plan Comparison Prompt", "Daily Briefing Prompt")
2. **Context** — one sentence: when in the meeting it was shared and why (e.g., "Wade had old and new plan sets for the Acadian project. Jesse dictated this to demonstrate giving Claude a complex task while requiring confirmation first.")
3. **Verbatim text** — the prompt itself, exact

**Output format:**

```
APPENDIX PROMPTS:

1. [Title]
   Context: [1-sentence context]
   Prompt:
   [verbatim prompt text]

2. [Title]
   ...

OTHER ARTIFACTS:
- Config: [what was toggled, by whom]
- Link: [URL + what it is]
- ...
```

This becomes the §Appendix section of the takeaway.

---

## Pass 5 — Commitments

**Goal:** Build the §Action Items section with attribution.

**What to scan for:**

- Attendees saying "I'm going to..." / "I'll try..." / "I want to..."
- Jesse or Luke suggesting an action that an attendee agreed to ("yeah, do that", "good idea")
- Specific tools or accounts to set up (WhisperFlow, Premium upgrade, MCP install)
- Things to monitor or revisit before Workshop #N+1

**Output format:**

```
ATTRIBUTED COMMITMENTS:
- [Attendee name]: [specific action they agreed to]
- ...

GENERAL ACTION ITEMS:
- [Action everyone should do, in imperative]
- ...
```

Specific named commitments go first in the takeaway's action list. Generic ones go after.

---

## Pass 6 — Personalization hooks

**Goal:** Capture the unique-to-this-meeting moments that prove the doc was written for *this* meeting.

**What to scan for:**

- A specific attendee doing something live that no one else has done ("Nick turned on the connector at the org level")
- Someone pushing back and being convinced (this is gold — name the moment in the email)
- An aha moment ("oh, that's actually really useful")
- Funny moments, asides, references to the company's culture
- A specific project name or job number that came up multiple times

**Output format:**

```
PERSONALIZATION HOOKS:
- [1-sentence hook] — use in: [email body / executive summary / use cases]
- ...
```

3–5 hooks. Each should be specific enough that no other workshop's follow-up could use the same line.

---

## After all six passes

Synthesize a **one-page mental model** of the meeting:

- **Tone:** Was it energetic? Skeptical at first then bought-in? Quiet and observational?
- **Who's the champion?** Often the most engaged attendee — name them.
- **What was the standout demo?** The one moment people will remember.
- **What unanswered questions surfaced?** These feed Workshop #N+1 preview.

This mental model informs the executive summary line, the email opener, and the "Workshop #N+1 Preview" section. Don't write it into the artifacts — use it to shape voice.
