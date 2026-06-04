# Cover Email Template

This is the short cover email Luke sends with the workshop takeaway attached. It's written in Luke's voice. Reference: `Taurus Builders/Workshop #1/email-draft.md`.

## Hard rules for this email

1. **The opener names every attendee by first name**, comma-separated. Skip titles. Not "Hi team" — name them.
2. **The first paragraph references something specific that happened in the meeting** — not "great workshop" but "honestly you picked it up faster than most teams I've seen run through this for the first time" or "[Specific person] turning on [specific config] at the org level."
3. **Use exactly five bullets** describing what's inside the takeaway document. Each bullet starts with a bold lead-in and one sentence of explanation. Match the precedent — see template body below.
4. **The closing paragraph gives the play forward** — what they should DO this week (give Claude real work) and what to do with friction (write it down, it becomes next session's agenda).
5. **The last line before sign-off references a Jesse-ism from the meeting** — "if Claude tells you it can't do something, don't believe it" is the canonical one but use whatever named rule came up in THIS meeting.
6. **Sign-off is "Luke"** — single first name, no title, no signature block.

## Template (with placeholders)

```
**Subject:** Workshop #{{N}} {{LABEL}} + Next Steps

---

Hey {{ATTENDEE_FIRST_NAMES_COMMA_SEP}},

{{OPENER_PARAGRAPH}}

Attached is the {{LABEL_LOWER}} document from Workshop #{{N}}. It's meant to be a resource you can come back to as you start putting Claude Code to work in your day-to-day. A few things worth calling out:

- **{{BULLET_1_LEAD}}**{{BULLET_1_BODY}}
- **{{BULLET_2_LEAD}}**{{BULLET_2_BODY}}
- **{{BULLET_3_LEAD}}**{{BULLET_3_BODY}}
- **{{BULLET_4_LEAD}}**{{BULLET_4_BODY}}
- **{{BULLET_5_LEAD}}**{{BULLET_5_BODY}}

The meeting recording link is inside the doc as well if you want to revisit anything.

{{NEXT_STEPS_PARAGRAPH}}

Shoot me or Jesse a note anytime if you get stuck. {{JESSE_ISM_LINE}}

{{CLOSING_LINE}}

Luke
```

## Reference: filled-in Taurus #1 version (for tone calibration)

```
**Subject:** Workshop #1 Takeaway + Next Steps

---

Hey Nick, David, Wade, Ryan,

Really appreciated the time with you guys yesterday. That was a fun session, and honestly you picked it up faster than most teams I've seen run through this for the first time.

Attached is the takeaway document from Workshop #1. It's meant to be a resource you can come back to as you start putting Claude Code to work in your day-to-day. A few things worth calling out:

- **A full recap of what we covered**, from install and setup all the way through the live plan comparison demo, skills, Procore automation, and the connector config Nick turned on at the org level.
- **The key concepts** that will make or break how useful this is for you. The Amelia Bedelia rule, "convince me you understand," and the reminder to always review the output are the ones I'd keep top of mind.
- **Six use cases we identified for Taurus specifically**, including plan comparison, estimate template automation, drawing takeoffs, Procore workflows, email triage, and permit filing.
- **A clean action list** for the week ahead, plus a preview of what Workshop #2 will cover once you've had some time to run with it.
- **An appendix with the three prompts Jesse shared in the chat** during the session. These would have been lost when the meeting ended, so we grabbed them and included context for how to use each one.

The meeting recording link is inside the doc as well if you want to revisit anything.

From here, the play is to just start using it. Give Claude real work. When you hit a wall or something doesn't behave the way you expect, write it down. Those friction points become the agenda for the next session, and that's where we'll unlock the bigger wins like scheduled automations and nested skills.

Shoot me or Jesse a note anytime if you get stuck. And like Jesse mentioned, if Claude tells you it can't do something, don't believe it. Tell it to figure it out.

Looking forward to the next one.

Luke
```

## How to fill each placeholder

| Placeholder | How to derive |
|---|---|
| `{{N}}` | Workshop number (1, 2, 3) |
| `{{LABEL}}` | "Takeaway" for #1; "Insights" for #2+ |
| `{{LABEL_LOWER}}` | "takeaway" / "insights" |
| `{{ATTENDEE_FIRST_NAMES_COMMA_SEP}}` | Client attendees only (no Ruh staff), Oxford comma optional. e.g., "Nick, David, Wade, Ryan" or "Joe" |
| `{{OPENER_PARAGRAPH}}` | 1–2 sentences. Must include a specific moment from the meeting — a person who did something, a tool that came up, an aha moment. Pull from Pass 6 (personalization hooks). |
| `{{BULLET_N_LEAD}}` + `{{BULLET_N_BODY}}` | Five bullets, matching this pattern: <br>1. **A full recap of what we covered**, from [specific demo] through [specific demo], [specific demo], and [specific personalized moment]. <br>2. **The key concepts** that will make or break how useful this is for you. [Name 2–3 concepts from Pass 1]. <br>3. **N use cases we identified for [Company] specifically**, including [list 4–6 use case names from Pass 3]. <br>4. **A clean action list** for the week ahead, plus a preview of Workshop #N+1. <br>5. **An appendix with the N prompts Jesse shared in the chat** — preserved with context for each. |
| `{{NEXT_STEPS_PARAGRAPH}}` | The "from here, the play is..." paragraph. Tell them to give Claude real work; note friction points; tease bigger wins coming in the next session. |
| `{{JESSE_ISM_LINE}}` | A Jesse rule from THIS meeting (Pass 1), framed as "And like Jesse mentioned, [rule]." Default to the "if Claude tells you it can't, don't believe it" line if no clear winner. |
| `{{CLOSING_LINE}}` | One short line. Default: "Looking forward to the next one." Customize if a specific next step was discussed. |

## Voice anti-patterns (do NOT do these)

- ❌ "I hope this email finds you well"
- ❌ "It was a pleasure meeting with you"
- ❌ "Please find attached"
- ❌ Generic "AI is transformative" framing
- ❌ Numbered lists where a bulleted list would do
- ❌ Sign-offs longer than "Luke" — no "Best," / "Cheers," / "Warm regards,"
- ❌ Anything that could appear unchanged in any other client's follow-up

## Save outputs

Both:
- `email-draft.md` — with the `**Subject:**` line + horizontal rule
- `email-draft.txt` — plain text version, no markdown

Save to `<client-dir>/Workshop #N/`.
