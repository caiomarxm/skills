---
name: feature-recon
description: >-
  Deep feature recon: read Jira, explore codebase, external research, and produce
  a structured recon file with 2-4 approaches at docs/feature-plans/<KEY>-<slug>.md.
  Use for fuzzy scope, trade-offs, or unfamiliar areas. Input for feature-design
  and feature-plan. Pair with feature-recon-light when only a code map is needed.
disable-model-invocation: true
---

# Feature recon (deep)

Read a Jira ticket, explore the codebase, research externally, and produce a **structured recon file** with possible approaches — input for **`feature-design`** (TDD), then `/feature-plan`.

**When to use deep vs light**

| Mode | Skill / command | Use when |
| --- | --- | --- |
| **Light** | `feature-recon-light` / `/feature-recon-light` | Scope is clear, **`grill-me` / `grill-with-docs`**-first workflow, or you only need a **code map** + ticket context before design. |
| **Deep** | `feature-recon` / `/feature-recon` (this doc) | Fuzzy scope, heavy trade-offs, unfamiliar area, or you want **2–4 approaches** + **Recommendation**. |

Deep recon **reuses the same file** as light (append); do not create a second recon file for the same ticket.

## The Recon File

The recon file at `docs/feature-plans/<JIRA-KEY>-<brief-description>.md` (e.g., `docs/feature-plans/EDATA-790-click-tracking.md`) is a **living scratchpad** — create it as soon as you have the ticket title and **write to it as you go**. The `<brief-description>` is a kebab-case slug derived from the ticket title (3–5 words, drop filler words like "add"/"the"/"a"). Every discovery, finding, and question gets recorded the moment it surfaces. This ensures:

-   Nothing is lost between steps or across tool calls
-   Earlier findings are available to reference when reasoning about later steps
-   The file is always up-to-date — there is no separate "write-up" phase at the end

**Exploration discipline**

-   **File over chat:** any meaningful codebase fact (paths, flows, constraints) must appear in the recon file — not only in the chat transcript.
-   **Code map is canonical:** whenever you identify a relevant path, add or update a row in **Code map (canonical)**. Later phases (`feature-design`, `/feature-plan`) should treat that table as the default **read allowlist** unless the user expands scope.
-   **Cap after the first full pass:** avoid open-ended re-exploration. Additional reads should target **Open Questions**, **Approaches**, or explicit user asks — and new paths must be added to **Code map** when validated.

Start with the template structure (see below) and fill sections incrementally as each step produces findings. Sections that haven't been reached yet stay empty.

### Template

```markdown
# Recon: <JIRA-KEY> — <Ticket Title>

**Recon depth:** deep

## Ticket Summary

-   **Title:** ...
-   **Description:** ...
-   **Acceptance Criteria:**
    -   ...
-   **Non-goals:** ...
-   **Linked Tickets:**
    -   EDATA-XXX — Title (Status)

## Confluence Notes

(Omit section if no Confluence page was provided)

## Code map (canonical)

| Path (repo-relative) | Role (one line) |
| --- | --- |

## Codebase Findings

### Implementation Surface

### Existing Patterns (how similar features work)

### Reuse Opportunities

### What Changes vs. What Doesn't

**Changes:**

**Unchanged:**

## External Research

(Omit section if no research was needed)

## Approaches

### 1. <Approach Name>

-   **Summary:** ...
-   **Fits existing patterns?** ...
-   **Complexity:** ...
-   **Trade-offs:** ...
-   **Risk:** ...

### 2. <Approach Name>

...

## Recommendation

<Which approach and why>

## Open Questions

-   ...

## Grill log

_(Optional — if used with `grill-me` or `grill-with-docs`: Q / answer / decision ref as the session progresses.)_
```

## Parameters

This skill expects:

-   **Jira ticket** (required) — either a ticket key (e.g., `EDATA-790`) or a full URL (e.g., `https://checkr.atlassian.net/browse/EDATA-790`). When only a key is provided, resolve it against the base URL `https://checkr.atlassian.net/browse/`.
-   **Confluence page URL** (optional) — full URL to related design docs or specs.

Example usage:

```
/feature-recon EDATA-790
/feature-recon https://checkr.atlassian.net/browse/EDATA-790
/feature-recon EDATA-790 https://checkr.atlassian.net/wiki/spaces/DAE/pages/123456/My+Design+Doc
```

---

## Step 1 — Read the Jira Ticket and Bootstrap the Recon File

**First action:** fetch the ticket via MCP (`getJiraIssue` with `cloudId: "95385d81-cba9-4876-9fe8-c7bc1357f516"`, `responseContentFormat: "markdown"`).

**Then create the recon file** at `docs/feature-plans/<JIRA-KEY>-<brief-description>.md`, where `<brief-description>` is a kebab-case slug derived from the ticket title (3–5 words, drop filler words like "add"/"the"/"a"; e.g., title `"Add click tracking to recorder"` → `click-tracking`, file → `EDATA-790-click-tracking.md`). Initialize it with the template above (title and empty sections).

Before creating the file, **check whether one already exists** for this ticket via a glob like `docs/feature-plans/<JIRA-KEY>-*.md`. If a recon file already exists, reuse it instead of creating a duplicate.

Extract and **write to the Ticket Summary section**:

-   **Title and description** — the full problem statement
-   **Acceptance criteria** — specific conditions for "done"
-   **Non-goals / out-of-scope** — explicit boundaries
-   **Labels, priority, story points** — sizing signals
-   **Linked tickets** — blockers, dependencies, related work. For each linked ticket, fetch its title and status (a single `searchJiraIssuesUsingJql` call with `key in (...)` is more efficient than individual fetches).

If the ticket is thin on detail, note what's missing in **Open Questions** — do not invent requirements.

---

## Step 2 — Read Confluence Documentation (if provided)

Fetch the page via MCP (`getConfluencePage` with `contentFormat: "markdown"`).

Extract and **write to the Confluence Notes section**:

-   Architectural overviews and diagrams
-   Design decisions and their rationale
-   Constraints (performance, compatibility, security)
-   Open questions or unresolved alternatives from the doc itself

If no Confluence page is provided, skip this step.

---

## Step 3 — Codebase Exploration

Explore the code methodically. The goal is to **map the implementation surface** — understand where this feature would live, what exists nearby, and what patterns are established. **Update the Codebase Findings section** as you discover each piece.

### 3.0 — Parallel exploration (subagents)

When the ticket likely touches **several modules or layers** you have not narrowed yet, prefer **parallel explore subagents** over long serial grep → read loops in the main thread. Follow **`.cursor/rules/explore-first.mdc`** (scope, one question per agent, explicit return shape, small budget).

Each subagent prompt should include:

-   **Scope** — one directory or a short explicit path list (not the whole repo).
-   **One focused question** — e.g. “Where are outbound automap messages defined and who sends them?” not “how does the extension work?”
-   **Return contract** — **paths**, **symbol names**, optional **one-line role** text suitable for **Code map** rows; avoid full-file dumps.

Run **2–5** independent explore tasks when questions split cleanly; **you** merge results into **Code map**, **Implementation Surface**, and subsections **3.3–3.5** so the recon file stays the single source of truth.

### 3.1 — Load relevant project rules

Read `.cursor/rules/architecture-rules.mdc` first to understand the overall structure and which component docs to load. Then read the docs relevant to the feature's component(s):

| Component | Rules/docs to read                                                                                                        |
| --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Extension | `docs/extension/EXTENSION-ARCHITECTURE.md`, `docs/extension/BROWSER-ABSTRACTIONS.md`, `.cursor/rules/extension-rules.mdc` |
| Maestro   | `docs/maestro/MAESTRO-ARCHITECTURE.md`, `docs/maestro/CODING-PATTERNS.md`, `.cursor/rules/maestro-rules.mdc`              |

Only load what's relevant — don't read extension docs for a backend-only feature.

### 3.2 — Locate the implementation surface

Find the modules, packages, and layers the feature will touch:

-   Entry points (routes, providers, components, message handlers)
-   Services and business logic
-   Data models and DTOs
-   Shared utilities

**Write findings to Implementation Surface.**

### 3.3 — Read surrounding code deeply

For each area identified, read enough to understand:

-   Call graphs and data flow
-   Constructor signatures and dependency injection
-   Naming conventions and code style
-   Error handling patterns
-   How similar features were built (the strongest signal for how this one should be built)

**Write findings to Existing Patterns.**

### 3.4 — Identify what changes and what doesn't

-   Where new logic belongs
-   What existing code must change vs. stay untouched
-   What can be reused or extended

**Write findings to What Changes vs. What Doesn't.**

### 3.5 — Identify reuse opportunities

Look for existing code that partially meets the feature's needs:

-   Functions that could be generalized
-   Logic buried in larger functions that could be extracted
-   Duplication that the feature would worsen if not consolidated
-   Dead code in the affected area

**Write findings to Reuse Opportunities.**

---

## Step 4 — External Research (when needed)

Use web search when the feature involves:

-   **Unfamiliar libraries or APIs** — look up current docs, best practices, common pitfalls
-   **Design patterns you're unsure about** — find authoritative guidance
-   **Third-party service integration** — check API docs, rate limits, auth mechanisms
-   **Performance or security concerns** — look up benchmarks, known vulnerabilities

Skip this step when the feature is purely internal logic with well-understood patterns.

**Write findings to External Research** with links to sources.

---

## Step 5 — Enumerate Approaches

List **2–4 distinct approaches** for implementing the feature. Each approach should be a plausible way to deliver the acceptance criteria.

For each approach, **write to the Approaches section**:

| Field                       | What to write                                                                  |
| --------------------------- | ------------------------------------------------------------------------------ |
| **Name**                    | Short label (e.g., "Provider-based with context", "Event-driven with pub/sub") |
| **Summary**                 | 2–3 sentences describing the approach                                          |
| **Fits existing patterns?** | How well it aligns with conventions found in Step 3                            |
| **Complexity**              | Rough size: S / M / L — and what drives it                                     |
| **Trade-offs**              | What you gain, what you give up                                                |
| **Risk**                    | Anything that could go wrong or is uncertain                                   |

### Recommend one approach

After listing all approaches, **write the Recommendation section** with a brief justification. The recommendation should weigh:

1. Alignment with existing codebase patterns (highest weight)
2. Simplicity and readability
3. Extensibility for likely follow-up work
4. Risk and unknowns

If two approaches are genuinely close, say so — the user will decide.

---

## Step 6 — Present and Iterate

Summarize the recon in your response:

1. **Ticket** — one-liner on what the feature is
2. **Key codebase findings** — where it lives, notable patterns
3. **Approaches** — bullet list with the recommendation highlighted
4. **Open questions** — anything the user needs to clarify

Then **wait for the user to respond**. The recon is the start of a design conversation, not a one-shot handoff. Expect an iterative loop where:

-   The user answers open questions — update the recon file, reassess approaches if answers shift the trade-offs
-   The user pushes back on the recommendation — explore their concern, update the analysis
-   The user asks to dig deeper into a specific approach — prototype, show code sketches, trace call paths, research further. Write findings back to the recon file.
-   New constraints surface — add them to the ticket summary, re-evaluate approaches
-   The user asks "what would X look like?" — investigate and record in the recon file

**Keep the recon file updated throughout this conversation.** It is the shared artifact both sides refine until the design is settled.

The loop ends when the user **explicitly chooses an approach** and signals readiness to plan. At that point, mark the chosen approach in the Recommendation section and remind the user to run **`feature-design`** (TDD) when the shape should be frozen, then **`/feature-plan <JIRA-KEY>`** with the TDD attached.

**Handoff:** `grill-me` / `grill-with-docs` and `feature-design` should **lift paths from Code map** and the distilled findings — they should not re-walk the repository for the same map unless the user asks or material contradicts the file.
