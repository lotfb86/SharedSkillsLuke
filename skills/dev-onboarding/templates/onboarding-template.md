# {CLIENT_NAME} — {AGENT_PRODUCT_NAME}
## Developer Onboarding & Build Context Document

**Audience:** Ruh.AI engineering team assuming the build of the {CLIENT_NAME} {AGENT_PRODUCT_NAME}.
**Assumes:** Zero prior exposure to {CLIENT_NAME}, zero {INDUSTRY} background, general familiarity with Ruh's agent framework (soul/brain/memory/skills).
**Author:** {AUTHOR_NAME}
**Last updated:** {DATE}
**Status:** {DEAL_STATUS}

---

## 0. TL;DR for the Engineer Who Only Reads One Page

- **What we're building:** {ONE_SENTENCE_AGENT_DESCRIPTION}
- **What the client does:** {CLIENT_COMPANY_ONE_LINER}
- **Why they bought:** {CORE_PAIN_ONE_SENTENCE_WITH_NAMED_SOURCE_OF_TRUTH}
- **The crucial POC/discovery finding:** {KEY_LEARNING_FROM_POC_OR_DISCOVERY}
- **The commercial envelope:** {FEES_TIMELINE_TERMS_SUMMARY}
- **The non-negotiables from IT:** {HARDWARE_OS_NETWORK_SECURITY_CONSTRAINTS}

If any of those bullets surprises you, read the rest.

---

## 1. The Client

### 1.1 Company

- **Legal/brand name:** {NAME_INCLUDING_FORMER_NAMES}
- **Owner:** {OWNERSHIP_STRUCTURE}
- **HQ:** {HEADQUARTERS}
- **Revenue:** {ANNUAL_REVENUE}
- **Footprint:** {GEOGRAPHIC_SCOPE}
- **Scope of trade:** {WHAT_THEY_DO}
- **Project profile:** {TYPICAL_PROJECT_MIX}
- **Sweet spot:** {PROJECT_SIZE_RANGE_AND_DURATION}
- **Labor / delivery model (important):** {HOW_WORK_GETS_DONE_SUBBED_OR_INHOUSE}

### 1.2 Key People

{ONE_PARAGRAPH_ON_TEAM_STRUCTURE_ESPECIALLY_THE_TIER_1_SOURCE_OF_TRUTH_HUMAN}

| Name | Role | Why you'll hear their name |
|---|---|---|
| **{LEAD_SOURCE_OF_TRUTH_NAME}** | {ROLE} | {WHY_CRITICAL — flag as Tier-1 memory authority} |
| **{NEXT_KEY_PERSON}** | {ROLE} | {WHY} |
| **{NEXT_KEY_PERSON}** | {ROLE} | {WHY} |
| **{IT_CONTACT}** | Solo IT / IT lead | {WHY — often a bus-factor-of-1 blocker on infrastructure} |
| **{OTHER}** | {ROLE} | {WHY} |

### 1.3 Why They Bought (Stated Pains)

Design decisions should trace back to at least one:

1. **{PAIN_1}** → {BUSINESS_IMPACT}
2. **{PAIN_2}** → {BUSINESS_IMPACT}
3. **{PAIN_3}** → {BUSINESS_IMPACT}
4. **{PAIN_4}** → {BUSINESS_IMPACT}
5. **{PAIN_5}** → {BUSINESS_IMPACT}

**The deepest pain is {CORE_PAIN}: {RESTATE_IN_PRODUCT_TERMS}.** Every architecture decision should be reviewed against that north star.

---

## 2. {INDUSTRY} 101 (Just Enough to Be Dangerous)

If you have never worked in {INDUSTRY}, read this section. It will save you a week.

### 2.1 What a {DELIVERABLE} actually is

{2-3_PARAGRAPHS_PLAIN_LANGUAGE}

### 2.2 Why this work is hard

- **{DIFFICULTY_1}:** {EXPLANATION}
- **{DIFFICULTY_2}:** {EXPLANATION}
- **{DIFFICULTY_3}:** {EXPLANATION}

**This is why the agent exists.** {ONE_SENTENCE_CONNECTING_INDUSTRY_DIFFICULTY_TO_AGENT_VALUE}

### 2.3 Glossary — Say These Back Without Flinching

| Term | Meaning |
|---|---|
| **{TERM}** | {PLAIN_LANGUAGE_DEFINITION} |
| ... | ... |

---

## 3. How {CLIENT_NAME} Works Today

You must internalize this workflow. The agent does not replace it — it *wraps* it.

### 3.1 The Canonical Inputs to Any {DELIVERABLE}

{NUMBERED_LIST_OF_INPUT_SYSTEMS_WITH_DETAILS_ON_EACH}

### 3.2 The {DELIVERABLE} Workflow, Start to Finish

{NUMBERED_WORKFLOW_STEPS_AS_THEY_EXIST_TODAY}

**What the agent changes:** {PLAIN_STATEMENT_OF_DELTA}

### 3.3 File System of Record

- **{SYSTEM_NAME} is the ground truth.** Tree looks like: `{STRUCTURE}`.
- Each project folder contains: {WHAT_IS_IN_EACH_FOLDER}.
- **{N} historical records live here.** This is the training-data corpus.
- **{EGRESS_POSTURE}** {CRITICAL_IF_BLOCKED}

### 3.4 Other Systems in the Stack

| System | Purpose | Day-1 integration? |
|---|---|---|
| **{SYSTEM}** | {PURPOSE} | {YES_NO_WITH_NOTE} |

**Integration guidance from Jesse/Luke:** {ANY_NAMED_PREFERENCES_FROM_TRANSCRIPTS}

---

## 4. The Agent: Product Specification

### 4.1 Four-Layer Architecture

| Layer | Function | {CLIENT} Analog |
|---|---|---|
| **Soul** | Core identity, values. | {CONCRETE_EXAMPLE_FOR_THIS_CLIENT} |
| **Brain** | Problem-solving methodology. | {CONCRETE_EXAMPLE} |
| **Memory** | Historical knowledge, learned patterns. | {CONCRETE_EXAMPLE} |
| **Skills** | Specific capabilities, refined through feedback. | {CONCRETE_EXAMPLE} |

**The initial skill file** ({PATH_TO_SKILL_FILE_OR_STATEMENT_IT_MUST_BE_BUILT_IN_WEEK_1}) is the agent's brain baseline. {SUMMARY_OF_WHAT_IT_DEFINES}

### 4.2 Inputs the Agent Accepts

**Required:**
- {REQUIRED_INPUT_1}
- {REQUIRED_INPUT_2}

**Standard:**
- {STANDARD_INPUT_1}
- {STANDARD_INPUT_2}

**Supplementary:**
- {SUPPLEMENTARY_INPUT_1}

### 4.3 Authority Hierarchy

This is one of the most important architectural requirements. The memory model must be **role-aware**, not flat.

| Tier | Role | Who | Memory write permission |
|---|---|---|---|
| **Tier 1 — {DOMAIN_1}** | {ROLE} | **{NAMED_PERSON}** | {DESCRIPTION_OF_AUTHORITATIVE_WRITES} |
| **Tier 1 — {DOMAIN_2}** | {ROLE} | {NAMED_PERSON} | {DESCRIPTION} |
| **Tier 2** | {ROLE} | {NAMED_PERSON_OR_TBD} | Writes are logged and flagged for Tier-1 confirmation. |
| **Tier 3** | {ROLE} | {GROUP_DESCRIPTION} | Writes are proposals — routed to Tier 1 for approve/veto. |

**Why this matters:** {EXPLANATION_OF_DRIFT_PREVENTION}

**Implementation implications:**
- Identity-aware feedback ingestion from day one.
- Lane tagging on every memory write.
- {ANY_OTHER_CLIENT_SPECIFIC_NUANCE}

**Do not ship a flat memory model.** Retrofitting tiers after the fact means untangling contaminated memory from weeks of training.

### 4.4 Outputs the Agent Produces (Every {RUN}, Every Time)

The client's human equivalents produce ~{CURRENT_COUNT} of these. The agent produces all {TARGET_COUNT} on every run:

1. **{OUTPUT_1}** — {DESCRIPTION}, see `{EXEMPLAR_FILE_IF_POC_EXISTS}`.
2. **{OUTPUT_2}** — {DESCRIPTION}.
... (continue through full deliverable contract)

### 4.5 The POC Lessons

{IF_POC_EXISTS — one paragraph per POC project with: name, size/scope, inputs given, agent output, delta vs. reality, lesson learned}

**A known failure mode from the POC:** {SPECIFIC_ENGINEERING_PROBLEM_OBSERVED}

---

## 5. Technical Architecture & Infrastructure

### 5.1 Deployment Target

- **Hardware:** {CLIENT_SPECIFIED_HARDWARE}
- **OS:** {OS_AND_REASON_IF_CONSTRAINED}
- **Network placement:** {ON_PREM_VS_CLOUD_VS_HYBRID}
- **Provisioning:** {WHO_OWNS_IT}

### 5.2 LLM Access

- **Licensing model:** {CLIENT_BOUGHT_DIRECT_OR_RUH_PROVIDES}
- **Token billing:** {PASS_THROUGH_OR_BUNDLED}
- **Rate-limit behavior:** {HOW_AGENT_CHECKPOINTS_AND_RESUMES}
- **Token cost projection:** {MONTHLY_ESTIMATE_IF_KNOWN}

### 5.3 {PRIMARY_FILE_INTEGRATION} (Day 1)

- {ACCESS_TYPE_AND_PATH}
- {SCOPE_OF_ACCESS}
- {WRITE_VS_READ}
- {EGRESS_CONSTRAINTS}

### 5.4 Email Interface (Day 1)

- Dedicated mailbox: `{PROPOSED_ADDRESS}`
- Inbound / outbound flow: {DESCRIPTION}
- Auth: {PATTERN}

### 5.5 Future Integrations (Not Day 1 — But Architect For Them)

| System | Purpose | Notes |
|---|---|---|
| **{SYSTEM}** | {PURPOSE} | {PHASE_AND_ANY_NAMED_PREFERENCES} |

### 5.6 Security Posture

- {TENANT_BOUNDARY_STATEMENT}
- {IT_OWNER}
- {COMPLIANCE_POSTURE}
- {CLIENT_DATA_OWNERSHIP_PER_MSA}
- **Data portability on termination:** {MSA_OBLIGATIONS_SUMMARIZED}

### 5.7 {DOMAIN_SPECIFIC_HANDLING_1} (Hard Requirement)

{ANY_KNOWN_PROCESSING_CHALLENGES_FROM_POC — e.g., large image sets, handwritten inputs, multi-page PDFs, unstructured photo batches}

### 5.8 {DOMAIN_SPECIFIC_HANDLING_2}

{ANY_OTHER_INPUT_TYPE_NEEDING_SPECIAL_HANDLING}

---

## 6. The Training Pipeline

### 6.0 The Prerequisite: Extract the {SOURCE_OF_TRUTH_ROLE}'s Philosophy

{IF_APPLICABLE — client has a human source-of-truth whose judgment must be encoded. Spell out:
- Who this person is.
- Their accessibility (day-to-day vs. approval-only).
- Why Week 1-2 discovery is an extraction interview with them, not a generic Q&A.
- How the sustaining conduit (often a senior subordinate) relays corrections after the initial extraction.
- That the training loop compares agent output to THEIR historical work product.}

### 6.1 The Recursive Loop

```
For each training project in the corpus:
  1. RECEIVE  — Agent gets original inputs.
  2. EXECUTE  — Agent produces output using current skill file.
  3. COMPARE  — We show the agent the client's actual output for the same project.
  4. ANALYZE  — Agent identifies every delta.
  5. REWRITE  — Agent rewrites its skill file to align.
  6. VALIDATE — Agent re-runs with updated skills.
  7. REPEAT   — Next project, with accumulated learning.
```

**This is recursive self-improvement against real ground truth, not synthetic fine-tuning.** We edit the skill file (prompts + structured config) between runs. LLM weights never change.

### 6.2 Expected Trajectory

- **Projects 1–20:** Large deltas. Agent learning rates, preferences, conventions.
- **Projects 20–80:** Deltas narrow. Edge-case refinement.
- **Projects 80–N:** Matching within tolerance. Remaining deltas are judgment calls.

**Convergence target (per milestone exhibit):** {MILESTONE_TARGETS}

### 6.3 Source of Training Projects

- Total historical corpus: {N_AVAILABLE}
- Training on: {N_CURATED}
- **Curation owned by:** {NAMED_CURATORS}
- **First delivery:** {FIRST_BATCH_DESCRIPTION}
- **Selection bias we want:** {CURATION_RUBRIC}

### 6.4 The Skill File

- Living markdown, versioned with revision history.
- Every correction updates it; training iterations may rewrite sections.
- {CLIENT}'s property on termination per MSA.

### 6.5 Build Phases (From MSA Exhibit A)

| Week | Phase | Deliverable | Client obligation |
|---|---|---|---|
| {WEEKS} | {PHASE} | {DELIVERABLE} | {OBLIGATION} |

---

## 7. Commercial + SLA Envelope (What "Done" Means)

### 7.1 Fee Structure

| Fee | Amount | Timing |
|---|---|---|
| **{BUILD_FEE_NAME}** | {AMOUNT} | {PAYMENT_SCHEDULE} |
| **{RECURRING_FEE_NAME}** | {AMOUNT} | {WHEN_STARTS} |
| **{PASS_THROUGH_NAME}** | {TERMS} | {BILLED_BY_WHOM} |
| **Change orders** | Quoted separately | For new features, new agents, custom UI, or integrations beyond Day-1 scope |

### 7.2 Exhibit A — Performance Milestones

| Milestone | Timeframe | Definition | Remedy if missed |
|---|---|---|---|
| {MILESTONE_1} | {WHEN} | {DEFINITION} | {REMEDY} |
| ... | ... | ... | ... |
| **{EXIT_RAMP_MILESTONE}** | **{WHEN}** | **{DEFINITION_WITH_ANY_LUKE_LOCKED_SCOPE}** | **Exit ramp.** {REFUND_FORMULA} |

**{EXIT_RAMP_MILESTONE} is the one engineering must not miss.** Every other milestone carries only a remediation-plan remedy. {EXIT_RAMP} carries a refund + termination right. Stand up measurement infrastructure (dashboards, autonomous-completion rate, rework rate) from week 1 so we're never surprised.

### 7.3 SLA

- {UPTIME_TARGET}
- {RESPONSE_SLA}
- {MAINTENANCE_WINDOW}
- {PERSONAL_SUPPORT_CONTACT}

### 7.4 IP Boundary

**Ruh retains:** {PROVIDER_IP}
**{CLIENT} retains:** {CLIENT_IP_AND_DATA}
**On termination:** {PORTABILITY_SUMMARY}

---

## 8. Risks, Gotchas, and Engineering Landmines

Read this list carefully. Each of these will bite you if you design around the happy path.

1. **{RISK_1}** — {WHY_AND_MITIGATION}.
2. **{RISK_2}** — {WHY_AND_MITIGATION}.
... (aim for 10-15 specific, actionable risks; no generic platitudes)

---

## 9. Open Questions — Status as of {DATE}

Questions the dev team needs answered. Some resolved; remaining items split between **{USER_NAME} action items** and **Week 1 discovery with the client**.

### Resolved

1. ✅ **{RESOLVED_QUESTION_1}** {ANSWER}
2. ✅ **{RESOLVED_QUESTION_2}** {ANSWER}

### {USER_NAME} action items (pre-kickoff)

{N}. ⏳ **{OPEN_QUESTION}** {CONTEXT_IF_NEEDED}

### For Week 1 discovery with the client

{CATEGORIZE_BY_WHO_TO_ASK: Training data & config | Infrastructure (ask IT lead) | Product (ask ops lead) | Governance (ask execs) | Commercial / timing (ask decision-maker) | Expansion (deferred)}

### Deferred (don't raise in Week 1)

{PHASE_2_AND_BEYOND_QUESTIONS}

---

## 10. Directory Contents (What's in This Folder)

| File | Purpose |
|---|---|
| `{FILE}` | {PURPOSE_AND_WHEN_TO_READ_IT} |
| ... | ... |

---

## 11. Recommended Reading Order for a New Engineer

1. This document (§0 TL;DR + §1 The Client + §2 Industry 101).
2. {NEXT_ARTIFACT_IN_PRIORITY_ORDER}
3. ...

Time budget: ~4 hours to go from zero to productive.

---

*Questions, corrections, and missing context: route to {USER_NAME}. Authority-hierarchy edge cases, industry-specific clarifications, or client-communication questions: route to {USER_NAME} first; {USER_NAME} routes to the client.*
