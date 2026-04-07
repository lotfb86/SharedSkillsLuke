# MSA Document Structure Reference

This reference contains the section-by-section structure, formatting specifications, and boilerplate language for generating Ruh AI Master Services Agreements.

## Document Formatting

### Page Setup
- **Paper:** US Letter (8.5" x 11")
- **Margins:** 1 inch all sides (top, bottom, left, right)
- **Bottom margin for body pages:** 0.75 inches (to accommodate footer)

### Typography
| Element | Font | Size | Color | Weight |
|---------|------|------|-------|--------|
| Company name (cover) | Georgia | 26pt | #1E2761 | Bold |
| Document title (cover) | Georgia | 22pt | #1E2761 | Bold |
| Subtitle (cover) | Calibri | 13pt | #4472C4 | Italic |
| Heading 1 (sections) | Georgia | 16pt | #1E2761 | Bold |
| Heading 2 (subsections) | Georgia | 13pt | #1E2761 | Bold |
| Heading 3 (labels) | Georgia | 11pt | #4472C4 | Bold |
| Body text | Calibri | 11pt | #2D2D2D | Regular |
| Table header | Calibri | 10pt | #FFFFFF on #1E2761 | Bold |
| Table body | Calibri | 10pt | #2D2D2D | Regular |
| Header/footer | Calibri | 8-9pt | #888888 | Regular |

### Colors
| Use | Hex | Description |
|-----|-----|-------------|
| Primary | `1E2761` | Navy — headings, borders, table headers |
| Accent | `4472C4` | Blue — subtitles, labels, proposed language markers |
| Body text | `2D2D2D` | Dark gray — all body content |
| Light gray | `888888` | Headers, footers, captions |
| Table border | `B4C6E7` | Light blue — table gridlines |

### Section Dividers
- Heading 1 paragraphs get a bottom border: 4pt solid, color `1E2761`, 4pt space
- Use page breaks before major sections (Sections 4+)

### Headers and Footers
- **Header:** `RUH.AI  |  [Client Name]  |  Master Services Agreement & Proposal` — navy brand name (Georgia 9pt bold), gray details (Calibri 8pt), bottom border
- **Footer:** `Confidential  |  Ruh AI, Inc.  |  Page [N]` — right-aligned, Calibri 8pt gray

---

## Section-by-Section Content Guide

### Cover Page

```
[6 blank paragraphs for spacing]

RUH.AI
Autonomous AI Solutions for Enterprise

[bottom border accent line]

[2 blank paragraphs]

Master Services Agreement & Proposal
[Phase Label — e.g., "Phase 1: AI Marketing Engine"]

[blank paragraph]

Prepared Exclusively For
[Client Company Name]
[Client Contact 1, Title  |  Client Contact 2, Title]

[4 blank paragraphs]

Presented by Ruh AI, Inc.
[Provider Contact 1, Title  |  Provider Contact 2, Title]
[Month Year  |  Confidential]
```

### Executive Summary

Summarize in 2-3 paragraphs:
1. Client's current state and reputation (acknowledge their strengths)
2. The gap or opportunity this engagement addresses
3. What this proposal covers (phase scope) and the dual nature of the document (business proposal + MSA)

### Section 1: Market Opportunity (if applicable)

Only include if market/keyword data is available from source materials.

- **Market context** — Why the client's niche is underserved
- **Keyword research table** — Keyword, Monthly Searches, Est. CPC, Competition, Client Fit
- **Comparison table** — Keywords the client should avoid (high competition)
- Frame data honestly: note that volumes are national, local is lower but so is competition

### Section 2: Cost Analysis

- **Annual cost comparison table:** Traditional alternative vs. Ruh AI agent
  - Columns: Cost Category | Traditional | Ruh AI
  - Rows: Setup fee, monthly retainer, annual cost, token costs, ad spend, content output, 24/7 operation, scalability
- **Year 1 total comparison** — Highlight savings
- **Projected results tables** (if applicable) — Conservative and moderate scenarios
- **Bottom line framing** — Use revenue opportunity language, NOT specific ROI multipliers

### Section 3: Scope of Work

#### 3.1 Deliverables
Bullet list of what's being built and deployed. For content-producing agents, frame volume as capacity with quality-controlled practical target.

#### 3.2 Timeline
- Weeks 1-2: Discovery
- Weeks 3-6: Build
- Weeks 7-8: Testing and go-live
- Ongoing: Autonomous operation with monthly reporting

#### 3.3 What Client Provides
- Platform access (CMS, Google Ads, etc.)
- Discovery call time
- Ad spend budget (separate from Ruh AI fees)
- Primary point of contact
- Content reviewer designation (weekly digest, 48-hour flag window)

### Section 4: Master Services Agreement

#### 4.1 Services
Provider builds and deploys the agent as described in Section 3. Agent operates on Provider's proprietary platform, accessible via web interface and integrated third-party services.

#### 4.2 Engagement Structure
**This is a SaaS/license engagement, not work-for-hire.** Client licenses access to the Agent and platform. No transfer of IP. Analogous to a SaaS deployment customized for Client's business.

### Section 5: Fees & Payment Terms

#### 5.1 Fee Schedule
Table with: Fee Component | Amount | Description
- Build & Deployment Fee (one-time)
- Monthly Platform License
- LLM Token Costs (variable, with two options: Provider invoices at cost, or Client maintains own API accounts)
- Ad Spend (client-controlled, separate)

#### 5.2 Payment Terms
- Build fee: 50% on execution, 50% on go-live
- Monthly fee: invoiced first business day, Net 15
- Token costs: monthly in arrears at actual cost, Net 15
- Late payments: 1.5% per month

### Section 6: Intellectual Property & Ownership

#### 6.1 Provider IP
All IP created or deployed by Provider — agent software, platform architecture, AI models, agent configurations, prompt engineering, workflow automations, integration frameworks, proprietary tools and methodologies — is and remains sole and exclusive property of Provider.

#### 6.2 License Grant
Non-exclusive, non-transferable, non-sublicensable, revocable license to access and use the Agent through Provider's platform for Client's internal business purposes during the term.

#### 6.3 Client Data
Client retains ownership of proprietary business data (customer lists, project data, financial info, brand assets). Provider uses Client Data solely for performing Services.

#### 6.4 Content Ownership
Marketing materials generated by the Agent are owned by Client. Underlying systems, templates, workflows, and AI configurations remain Provider's IP.

#### 6.5 No Reverse Engineering
Client shall not reverse engineer, decompile, or attempt to derive source code, algorithms, or architecture.

#### 6.6 Data Portability & Transition Assistance
**(a)** Upon termination, Provider delivers within 30 days in portable formats (CSV, JSON, PDF):
  - (i) Keyword research, market segmentation, content strategy docs
  - (ii) PPC campaign configurations, ad copy, targeting, performance data
  - (iii) Content calendar and publishing schedule
  - (iv) Analytics reports and dashboards
  - (v) Any other Client-specific data and configurations

**(b)** 30-day transition period, up to 10 hours, at no additional charge — walkthrough of campaigns, content architecture, operational docs.

**(c)** Explicit carve-out: nothing grants rights to Provider's platform, agent software, AI models, prompt engineering, or underlying technology. Data portability applies solely to Client-specific outputs, not Provider IP.

### Section 7: Term & Termination

#### 7.1 Initial Term
Commences on Effective Date, continues for [Initial Term] following go-live.

#### 7.2 Renewal
Auto-renews for successive [Renewal Term] periods unless [Non-renewal Notice] days' written notice.

#### 7.3 Termination for Convenience
After Initial Term, either party may terminate on [Convenience Notice] days' written notice.

#### 7.4 Termination for Cause
Immediate termination if: (a) material breach not cured within [Cure Period] days; or (b) insolvency/bankruptcy.

#### 7.5 Effect of Termination
- License terminates; Agent ceases operation
- Provider returns/destroys Client Data within 30 days on request
- Client pays all accrued fees
- Client retains ownership of all generated content

#### 7.6 Survival
IP, Confidentiality, and Limitation of Liability survive termination.

### Section 8: Confidentiality

Mutual obligations. Standard exclusions (public info, prior knowledge, independent development, third-party receipt). Survives for [Confidentiality Survival] years post-termination.

### Section 9: Limitation of Liability & Performance

#### 9.1 Limitation of Liability
No indirect/incidental/special/consequential/punitive damages. Aggregate liability capped at [Liability Cap] months' fees.

#### 9.2 Performance Disclaimer
Projections are estimates, not guarantees. Performance depends on market conditions, ad spend, competition, website quality, client responsiveness. Provider commits to diligent optimization and transparent reporting.

#### 9.3 Third-Party Platforms
Not responsible for changes to third-party APIs, pricing, terms, or availability.

#### 9.4 Performance Milestones
**(a)** Milestones per Exhibit A, based on scope and market conditions at Effective Date.

**(b)** Each milestone conditioned on Client fulfilling corresponding obligations (ad spend, content publishing, platform access). If Client fails obligations, milestone waived — no remedy applies.

**(c)** If Provider misses milestone and Client met all obligations: written remediation plan within 10 business days.

**(d)** Month 6 exit ramp: if Provider misses Month 6 milestone and Client met obligations, Client may terminate on 30 days' notice with pro-rated build fee refund.

**(e)** Measurement via mutually agreed analytics tools with shared dashboards.

**(f)** Milestones adjustable by mutual written agreement for material market changes.

#### 9.5 Service Levels
99% monthly uptime (excluding scheduled maintenance with 24-hour advance notice). Unscheduled disruptions: 24-hour response with status update and estimated resolution. Scheduled maintenance during off-peak hours (10 PM – 6 AM local time).

### Section 10: General Provisions

#### 10.1 Independent Contractor
No employment, agency, partnership, or joint venture.

#### 10.2 Governing Law
Laws of [Client's State] without conflict of law principles. Disputes in state or federal courts in [Client's State]. (Default to client's state as good faith gesture.)

#### 10.3 Entire Agreement
Supersedes all prior negotiations. Amendments require written instrument signed by both parties.

#### 10.4 Notices
Written, delivered by email with confirmation. Provider: jesse@ruh.ai. Client: designated at execution.

#### 10.5 Severability
Invalid provisions don't affect remaining provisions.

#### 10.6 Assignment
Neither party assigns without consent, except Provider may assign in M&A. **In the event of assignment by Provider, Client shall have the right to terminate this Agreement upon thirty (30) days' written notice following notification of such assignment.**

### Signature Page

```
By signing below, each Party acknowledges that it has read, understood, and agrees
to be bound by the terms and conditions of this Master Services Agreement & Proposal.

________________________________
[Provider Contact Name], [Title]
[Provider Company]
Date: ________________________

________________________________
[Client Contact 1 Name], [Title]
[Client Company]
Date: ________________________

________________________________
[Client Contact 2 Name], [Title] (if applicable)
[Client Company]
Date: ________________________
```

---

## Python-docx Generation Notes

### Key python-docx patterns

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

# Bottom border on a paragraph
def add_bottom_border(p, color="1E2761", size=4):
    pPr = p._p.get_or_add_pPr()
    pPr.append(parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'<w:bottom w:val="single" w:sz="{size}" w:space="4" w:color="{color}"/>'
        f'</w:pBdr>'
    ))

# Cell shading
def add_shading(cell, color):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}" w:val="clear"/>')
    cell._tc.get_or_add_tcPr().append(shading)

# Cell margins
def add_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    ))
```

### Table best practices
- Always use `table.style = 'Table Grid'`
- Set column widths on both the table and individual cells
- Use `add_shading(cell, "1E2761")` for header rows with white text
- Add cell margins for readable padding
- Use `WD_TABLE_ALIGNMENT.CENTER` for table alignment

### Style setup
```python
# Override built-in styles
for level, (font_name, size, color) in {
    1: ('Georgia', 16, NAVY),
    2: ('Georgia', 13, NAVY),
    3: ('Georgia', 11, ACCENT),
}.items():
    h = doc.styles[f'Heading {level}']
    h.font.name = font_name
    h.font.size = Pt(size)
    h.font.bold = True
    h.font.color.rgb = color
```
