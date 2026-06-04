---
name: workshop-followup
description: >
  Generate a polished post-workshop follow-up package for a Ruh AI client engagement:
  an HTML takeaway document, a PDF export, and a short cover email in Luke's voice.
  Use this skill whenever the user has just finished a Ruh AI workshop with a client
  (typically a Claude Code / AI enablement session led by Jesse and/or Luke) and needs
  to send the attendees a follow-up. Input is a transcript (file path or pasted text)
  and a recording link; the skill auto-discovers attendees from Google Calendar when
  available, does light company research from recipient email domains, runs a six-pass
  extraction over the transcript to capture Jesse-isms, attendee Q&A, identified use
  cases, prompts shared in chat, commitments, and personalization hooks — then renders
  the artifacts into the client's working directory under `Workshop-N/`. The output
  matches the house style established for Taurus Builders and Dondlinger.
  Triggers on: "workshop follow-up", "workshop followup", "workshop takeaway",
  "workshop recap", "post-workshop email", "after-meeting follow-up", "workshop wrap-up",
  "build the takeaway", "send the workshop email", "Workshop #N takeaway",
  "Workshop #N insights", "follow up on the [Company] workshop".
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

# Workshop Follow-up Generator

## Overview

After every Ruh AI workshop with a client, we send a follow-up package:

1. **`Workshop-N-Takeaway.html`** (Workshop #1) or **`Workshop-N-Insights.html`** (Workshop #2+) — a polished single-page recap with company-specific use cases, attributed Jesse-isms, action items, and a prompt appendix.
2. **`Workshop-N-Takeaway.pdf`** / **`Workshop-N-Insights.pdf`** — print-ready export of the same.
3. **`email-draft.md`** + **`email-draft.txt`** — a short, warm cover email in Luke's voice that references specific moments from the meeting.

This skill produces all three from a transcript and a recording link.

The reference precedents live at:
- `~/Library/Mobile Documents/com~apple~CloudDocs/Ruh.AI/Taurus Builders/Workshop #1/`
- `~/Library/Mobile Documents/com~apple~CloudDocs/Ruh.AI/Taurus Builders/Workshop #2/`
- `~/Library/Mobile Documents/com~apple~CloudDocs/Ruh.AI/Dondlinger/`

When in doubt about style or voice, read the corresponding artifact from those folders.

## Hard rules — what makes a takeaway correct

The output is only as good as how specifically it names what happened in the meeting. The bar:

- **Every concept must be attributed.** If Jesse named a rule ("Amelia Bedelia rule", "Convince me you understand"), quote him by name. If a participant pushed back or had an aha moment, name them.
- **Use cases must use the company's actual vocabulary.** Not "document automation" — "plan comparison on the Acadian project," "Procore RFI triage," "permit filing in [their county]."
- **Prompts Jesse shared in chat go in the appendix.** They'd be lost when the meeting ended — preserving them is half the value of the doc.
- **The email opener names every attendee** by first name. The email body references at least two specific moments from the meeting (a tool, a person, a config change, a question that got answered).
- **No generic AI-enablement copy.** If the same paragraph could appear in any other client's follow-up, rewrite it.

## Step 1: Discover the meeting context

Goal: figure out who attended, when the meeting happened, and what the client is.

### 1a. Inputs the user typically provides

- **Transcript** — pasted text or a path to a transcript file (`.txt`, `.md`, `.vtt`, `.docx`). **Expect the user to provide this directly most of the time.** See "Transcript sourcing" below.
- **Recording link** — often a Bubbles `app.usebubbles.com/...` URL. (Bubbles links go in the doc but provide no usable transcript — don't try to fetch from them.)
- Optionally: workshop number (#1, #2, etc.) — if not given, infer from the client folder

If the user only gave the recording link without a transcript, **ask for the transcript before generating** — without it, the output collapses to generic AI-enablement copy. The whole value of this skill is in the specifics.

### Transcript sourcing — order of precedence

1. **User-provided text/path** (default). Luke usually brings the transcript with the request. Use it as-is.
2. **Fireflies.ai** — the only platform we can auto-fetch from. If the recording link points to Fireflies, or if the user mentions Fireflies, invoke `/memory-fireflies-ingest` in single-transcript fetch mode to pull the full transcript. (See that skill's docs.)
3. **Bubbles** — black-box. The `app.usebubbles.com/...` link is useful as the embedded recording link in the takeaway doc, but Claude cannot extract the transcript from it. If the meeting was recorded on Bubbles and no transcript was provided, **stop and ask** Luke to paste it in. Do not attempt to scrape Bubbles. Do not generate from the summary alone.
4. **Other platforms (Otter, Zoom, Teams native)** — treat like Bubbles. Ask Luke for the transcript text.

### 1b. Auto-discover attendees via Google Calendar (preferred)

Use the Google Calendar MCP to find the meeting. Search strategy:

1. Determine the likely meeting date — first try the transcript metadata, then ask the user "when was the meeting?" if unclear.
2. Call `mcp__58747be3-4bf7-43e7-80a5-17347d5e8b7d__list_events` for the meeting date (single day or ±1 day window).
3. Match by:
   - Event title containing the client company name OR
   - Attendee emails matching the client domain OR
   - Description / location containing "Ruh" and the company name
4. Once matched, pull:
   - **Full attendee list** (catches people who didn't speak much in the transcript)
   - **Official meeting title** (informs the HTML title)
   - **Event description** (sometimes contains agenda or Bubbles link)
   - **Start time** (used in the meta line of the HTML)

### 1c. Fallback when Calendar isn't available

If the Google Calendar MCP returns nothing useful (no permissions, no match, or no MCP server connected), fall back to:

1. Extract every unique email address mentioned in the transcript.
2. Extract every named speaker.
3. Ask the user: "Calendar lookup didn't find the meeting. Can you confirm the attendee list and their emails?"
4. Proceed once the user confirms.

Always tell the user which path you used (calendar vs. fallback) so they can verify.

## Step 2: Light company research — private context only

This research is for **prompt-shaping context, not output content**. The takeaway and email never have a "Company Background" section. Research exists so the LLM understands the audience.

### How light is light

- **One or two pages max** via WebFetch. Usually one is enough.
- Target the company's homepage or About page.
- Capture only: industry / sub-vertical, geographic reach, any noteworthy posture (expanding into new markets, recently rebranded, acquired, etc.).
- If the transcript already makes the company's nature obvious, **skip the research entirely**.

### Process

1. Parse the recipient domain from any attendee email (e.g., `joe@elkstonebasements.com` → `elkstonebasements.com`).
2. Run one WebSearch: `"<Company Name> <industry hint from transcript>"`.
3. Optionally WebFetch the homepage to confirm industry and geographic reach.
4. Hold the resulting one-paragraph mental model privately. Use it to steer:
   - **Use-case framing** in §5 (a residential remodeler gets permit research; a commercial GC gets RFI triage)
   - **Action items** in §7 (an expanding company gets nudged toward scalable workflows; a single-office shop gets nudged toward day-one wins)

Never paste the research findings into the artifacts. The audience knows who they are.

## Step 3: Six-pass transcript extraction

Read the transcript thoroughly. For each pass below, scan with a different lens. Capture quotes verbatim when the wording matters.

### Pass 1 — Jesse-isms
**What to look for:** Every Jesse turn that introduces a named rule, mental model, principle, warning, or punchy directive.

Examples from precedent meetings:
- "Amelia Bedelia rule" — be literal in your instructions
- "Convince me you understand" — make Claude restate the task before doing it
- "If Claude tells you it can't, don't believe it. Tell it to figure it out."
- "Your job and my job in a world where AI does the work is to make sure that our inputs are really, really high quality and to review the output."

**Output:** A list of 4–8 named concepts + 1–2 verbatim Jesse quotes that anchor the philosophy section.

### Pass 2 — Q&A from attendees
**What to look for:** Moments where an attendee asked something substantive and Jesse (or Luke) gave a useful answer. Capture who asked, what they asked, what they got back.

**Output:** A list of 3–6 Q&A pairs, each with the attendee's name. These inform what to emphasize in the recap and what concerns to acknowledge in the email.

### Pass 3 — Use cases identified for THIS company
**What to look for:** Moments where an attendee said "we do X" or "we struggle with Y" and Claude was shown solving X or Y — using the company's actual tools and project names.

**Output:** 5–7 use cases, each titled with a verb-noun phrase ("Plan Comparison", "Drawing Takeoffs", "Permit Filing"), each described in 1–3 sentences using the company's vocabulary.

### Pass 4 — Artifacts shared
**What to look for:**
- **Prompts Jesse typed into chat** (these die when the meeting ends — preserving them is critical)
- **Code or config shown on screen** (connector toggles, settings flips, MCP installs)
- **Links shared** (tools, repos, docs)

**Output:** A numbered appendix list. For each prompt, capture the verbatim text AND a one-sentence context of when/why it was used.

### Pass 5 — Commitments
**What to look for:** What did each attendee say they'd try, install, or do next?

**Output:** A list of action items, attributed where possible (e.g., "Nick: turn on Procore connector org-wide"). Generic items ("explore Claude") go last; specific named commitments go first.

### Pass 6 — Personalization hooks
**What to look for:** The unique-to-this-meeting moments. Who pushed back? Who had the aha? Who did something live that no one else has done? What in-jokes formed?

**Output:** 3–5 specific lines that can be sprinkled into the email and the recap to prove the doc was written for *this* meeting and no other. (Example from Taurus: "the connector config Nick turned on at the org level.")

## Step 4: Render the artifacts

### 4a. HTML takeaway

Read `references/takeaway-template.html` from this skill's directory. It contains the full house-style HTML with `{{HANDLEBARS}}` placeholders. Replace placeholders with values derived from Step 1 (meeting context), Step 2 (private company brief — used to steer, not to print), and Step 3 (extraction passes).

Section order (matches Taurus Workshop #1):

1. **Hero header** — `RUH.AI` logo + `[CLIENT] WORKSHOP #N` chip
2. **Title** — `Workshop #N` + gradient `Takeaway` (or `Insights` for #2+)
3. **Meeting meta** — date, duration, attendee count
4. **Attendees** — comma-separated names
5. **Executive Summary** — one-line thesis (e.g., "Your team is now set up on the most capable AI tooling available today.") + 1–2 paragraphs of context
6. **What We Covered → Session Topics** — numbered list of demo segments
7. **Key Concepts → Things to Remember** — named principles from Pass 1, plus a `quote-block` for the lead Jesse quote
8. **Identified Use Cases → "Where [Company] Can Apply This"** — numbered `callout` boxes from Pass 3
9. **Security & Data → Data Practices & Trust** — only if security came up substantively in the meeting; otherwise omit
10. **Next Steps → Action Items for [Company]** — checklist from Pass 5, ending with a "Stuck on something?" dark callout
11. **Looking Ahead → Workshop #N+1 Preview** — short list of likely next-session topics
12. **Meeting recording link box** — the link the user supplied
13. **Appendix → Key Prompts** — Pass 4 prompts with context

Save to `<client-dir>/Workshop-N/Workshop-N-Takeaway.html` (or `Workshop-N-Insights.html` for #2+).

### 4b. PDF export

Convert the HTML to PDF using Chrome headless:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="<client-dir>/Workshop-N/Workshop-N-Takeaway.pdf" \
  "file://<client-dir>/Workshop-N/Workshop-N-Takeaway.html"
```

If headless Chrome isn't available, fall back to `wkhtmltopdf` or tell the user the PDF step needs to be done manually.

### 4c. Cover email

Read `references/email-template.md` from this skill's directory. Fill the placeholders. The email must:

- Open with "Hey [comma-separated first names of all attendees],"
- Use "Really appreciated the time with you guys" or close variant
- Reference at least two specific moments from the meeting (a person + what they did, OR a tool + how it was applied)
- Use 5 bullets describing what's inside the takeaway
- Close with the standard nudges:
  - "Give Claude real work."
  - "Note your friction points — they become the agenda for the next session."
  - "If Claude tells you it can't do something, don't believe it."
  - "Shoot me or Jesse a note anytime."

Save both `email-draft.md` and `email-draft.txt` in `<client-dir>/Workshop-N/`.

## Step 5: Visual Render Review — MANDATORY, NEVER SKIP

After rendering the HTML and PDF in Step 4, **you must visually verify the output before delivering it to the user.** This is a hard rule, not a suggestion. If the user sends an artifact that didn't render correctly without you having reviewed it, that is a quality-control failure the skill exists to prevent. The user is the second line of defense, not the first — you are.

### What to do

1. **Read the PDF visually** using the Read tool with the `pages` parameter:
   - For PDFs ≤10 pages: read in one call with no `pages` argument.
   - For PDFs >10 pages: read in chunks like `pages: "1-5"`, then `pages: "6-10"`, then `pages: "11-N"`. The Read tool requires the `pages` parameter on PDFs over 10 pages.
   - First confirm page count with: `pdfinfo <file>.pdf | grep -i pages` (or `mdls -name kMDItemNumberOfPages <file>.pdf` on macOS).

2. **Check every section against this rubric:**

   | Section | What to verify |
   |---|---|
   | **Hero header** | RUH logo SVG renders with the FULL ~13-dot pattern (not a truncated 2-dot version). [Client] chip on the right. Gradient "Takeaway"/"Insights" portion of the title displays. Meeting metadata (Date / Duration / Format) readable. |
   | **Attendees** | Client chips visible, none clipped. Two-tier rendering: client chips above, Ruh.AI chips below. |
   | **Executive Summary** | Thesis title bold. Body paragraph readable. "The Big Idea" purple callout box rendering with its border and gradient background. |
   | **Session Topics** | All numbered topic cards present. Numbered icon boxes filled with the purple gradient (not empty). Body text not overflowing the card. |
   | **Key Concepts** | Bullet list with bold lead-ins. Purple-dot bullets rendering. Quote block with purple left border, italic Jesse quote, purple attribution. |
   | **Use Cases** | Each callout box rendering with the gradient purple background and numbered icon. No collapsed/empty boxes. |
   | **Security & Data** (if included) | Dark purple callout with white text rendering correctly. Bolded sub-headings readable on the dark background. |
   | **Action Items** | Each item has an unfilled checkbox square + bold lead-in + body. "Stuck on something?" dark callout at the bottom of the section. |
   | **Workshop #N+1 Preview** | Bulleted concept list with strong-tagged topic names. |
   | **Meeting recording link box** | Purple callout with the link visible. |
   | **Appendix prompts** | Each prompt in a monospace font, light purple background box. Line breaks preserved inside the prompt block. No truncation of long prompts. |
   | **Footer** | RUH logo with FULL 13-dot pattern (this is the most common rendering bug — the footer SVG is often copy-paste-truncated to just 2 paths). Divider. [CLIENT] chip. `ruh.ai` + client website links. Tagline. |
   | **Pagination** | No section split awkwardly (heading on one page, body on the next). No callout box split across pages. No orphaned single lines. |

3. **Common rendering failures to specifically watch for:**

   - **Partial SVG logo** — only 2 of the 13 paths render in the footer (or hero). Caused by template copy-paste truncation. The full SVG should produce a circular dot-arrangement; a 2-path version shows just 2 isolated dots. **This is a real fix, not cosmetic — re-edit the HTML to include all 13 paths and re-export the PDF.**
   - **Gradient text rendering as a colored rounded box** — `-webkit-background-clip:text` sometimes fails in headless Chrome PDF print, producing a filled gradient rectangle instead of clipped gradient text. Cosmetic. Flag it but don't block delivery — the title is still readable.
   - **Missing fonts** — if Google Fonts didn't load, the doc renders in Times/serif. The whole tone of the doc collapses. Real issue. Re-export with a fresh Chrome run.
   - **Text overflow** — long content (especially verbatim Jesse prompts in the appendix) breaking out of their container boxes. Real issue.
   - **Broken pagination** — section title at the bottom of page N with the body starting on page N+1. Adjust the HTML with `page-break-inside: avoid` on the section if it's egregious.
   - **Empty sections** — a section-label header with nothing under it (means a `{{PLACEHOLDER}}` didn't get filled). Real issue. Backfill before delivery.
   - **PDF size anomaly** — a PDF that suddenly went from ~50 KB to ~1 MB on the same content usually means fonts now loaded fully (good — first export probably had fallback fonts). A PDF that went from 1 MB to 50 KB usually means fonts didn't load (bad — re-export).

4. **Report findings to the user before listing the file paths.** Use this format:

   ```
   Render review: <PASSED | N issues found>
   - <N> pages total
   - <Real issue 1>: <description> → <fix taken>
   - <Cosmetic issue 1>: <description> → <flagged, no action>
   ```

   For **Real** issues: fix them, re-export the PDF, and re-run the vision review. Do not deliver until they're resolved.

   For **Cosmetic** issues: flag them so the user can decide whether to act on them. Deliver the artifacts.

5. **If no issues:** state explicitly "Render review passed — N pages, all sections rendered cleanly" and move to Step 6.

### Why this step is mandatory

If the user sends a takeaway with a broken logo, a clipped section, or a misrendered callout, that lands as a quality issue on the client side — and the client is paying $5,000 for the workshop. The whole point of this skill is send-ready artifacts. The vision review is the last line of defense. The user is the second. If they're in a hurry and just forward the file, the skill should never have let it through.

## Step 6: Deliver

1. List the three (or four with PDF) output file paths as clickable markdown links.
2. Tell the user which discovery path was used (calendar vs. manual) and what was found.
3. Mention which sections of the takeaway might need a human eye — for example, "I omitted the Security section because it didn't come up — flag if you want it added."
4. Offer to adjust any section.

## File locations

- **Working directory:** infer from the transcript path or ask. Convention is `~/Library/Mobile Documents/com~apple~CloudDocs/Ruh.AI/[Client]/`.
- **Workshop subfolder:** `Workshop-N/` (hyphenated, no `#`, no space) — create if missing. **Convention rule:** the `#` character breaks file:// URLs and markdown hyperlinks (browsers treat it as a URL fragment), and spaces require quoting in shell commands. `Workshop-1/`, `Workshop-2/`, `Workshop-3/` survives every link type cleanly. Legacy folders from earlier sessions (Taurus Builders, Dondlinger) may use the old `Workshop #1/` form — they still work in Finder, but rename them to the new convention if you want clean clickable links across the board.
- **Filenames:**
  - Workshop #1: `Workshop-1-Takeaway.html`, `Workshop-1-Takeaway.pdf`
  - Workshop #2+: `Workshop-N-Insights.html`, `Workshop-N-Insights.pdf`
  - Email always: `email-draft.md`, `email-draft.txt`

## Dependencies

- Google Calendar MCP (preferred for attendee discovery) — falls back gracefully when unavailable
- WebSearch + WebFetch for one-page company research
- Google Chrome (headless) for PDF export — fallback available
- The reference templates at `references/takeaway-template.html` and `references/email-template.md`
- The transcript-extraction playbook at `references/extraction-prompts.md`

## When to NOT use this skill

- The meeting wasn't a workshop (e.g., a sales call, a discovery call) — use a different recap pattern
- The client wasn't ours — this is for Ruh AI engagements specifically
- No transcript is available — the value is in the specifics; without a transcript the output would be generic
