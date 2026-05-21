---
name: feature-design
description: >-
  Consolidates recon or grilling session markdown (`grill-me` / `grill-with-docs`) into a single Technical Design Document
  (TDD): authoritative scope, boundaries, decisions, and verification — primary
  input for `/feature-plan` (attach TDD + Jira key). Use for design consolidation,
  frozen decisions after grilling, or a TDD handoff before commit planning. Not
  test-driven development.
disable-model-invocation: true
---

# Feature design (TDD)

**TDD** here means **Technical Design Document** (not test-driven development).

Turn **messy upstream artifacts** into one **read-only TDD** that states the **final agreed engineering shape** of the feature. **`/feature-plan` uses this file as its main design input** (with the Jira key). The TDD is **still not** the plan: no commits, no gitmojis, no ordered implementation slices.

**Scope of work:** **Consolidate and reshape** the source doc(s) only. **Do not** repeat full **`/feature-recon`** (deep)-style codebase exploration unless the user explicitly asks — recon (light or deep) already paid the mapping cost; the TDD distills it for planning. Treat **`/feature-recon-light`** output as authoritative for **paths** once **Code map** is filled.

## Inputs (pick one or combine)

| Source                       | Typical shape                                                                               | How to use it                                                                                                                                                                                                                                                  |
| ---------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Recon (light)** (`/feature-recon-light`) | Same file shape as deep, often sparse **Approaches**; strong **Code map** | Treat **Code map** as the canonical path set; lift it into **Implementation surface**; use **Open Questions** / **Grill log** for decisions. |
| **Recon** (`/feature-recon`, deep) | `# Recon: …`, Ticket Summary, **Code map**, Codebase Findings, Approaches, Recommendation, Open Questions | Lift **Recommendation** as the chosen approach; fold resolved open questions into **Decisions**; drop superseded approaches or summarize them under **Alternatives discarded**; carry **high-signal** reuse/touch hints into **Implementation surface** only when present in source. |
| **Grilling** (`grill-me` / `grill-with-docs`) | Question tables (Q1…), decision log; with-docs: CONTEXT/ADR edits, checklists mixed with narrative | Treat **resolved rows** and the **decision log** as authoritative; collapse duplicate Q↔A into a single **Decision register**; separate **intentional TBDs** (names TBD in code) from **unresolved design** (must be closed or listed as explicit follow-ups). |

If the user provides **both**, the **TDD** wins on **conflicts** in this order: **latest explicit user answer in the grilling log** (`grill-me` or `grill-with-docs`) > **recon recommendation** > **older recon text**. Call out any remaining conflict in **Open follow-ups** and stop claiming **design is frozen** until resolved.

## Implementation surface (lift rules)

-   **Start from Code map:** the TDD **Implementation surface** section should begin by copying the recon **Code map (canonical)** table (prune rows that are out of scope for this TDD; do not add new paths unless sourced from a **grilling** answer (`grill-me` / `grill-with-docs`), new user instructions, or explicit user-requested verification).
-   **Grill deltas:** any path introduced only during **`grill-me` or `grill-with-docs`** must appear in **Sources** (or the merged recon file) and be tied to a **Decision** id (`Dn`) in **Implementation surface** or **Decisions** so planners know why it exists.
-   **Anti-drift:** every path listed under **Implementation surface** must be traceable to **Sources** or a documented user instruction in-session. If you cannot trace it, remove the path or add the missing source to **Sources** before freezing.
-   **`/feature-plan` contract:** treat **Implementation surface** (including **Canonical paths**) as the default **read/grep allowlist** for codebase validation unless the user directs otherwise or the repo clearly contradicts the TDD (then fix the TDD or stop — do not broaden exploration silently).

## What this artifact is / is not

| Is                                                                                                | Is not                                                                                     |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Single source of truth for **what** to build and **why**                                          | Commit-by-commit plan or vertical slices                                                   |
| **Primary input** for `/feature-plan` (attach this doc + ticket); implementers can rely on it too | Living scratchpad (that stays in the recon / grill file)                                   |
| Names ownership, boundaries, invariants, test strategy at design level                            | File-level task checklist unless it encodes **contract** (e.g. “two test layers required”) |

## Optimal TDD shape for AI → commit plan

Order and shape the TDD so a later agent can **derive commits without re-deriving design**:

| Principle | Why it helps `/feature-plan` |
| --- | --- |
| **Stable decision IDs** (`D1`, `D2`, …) | Commits and recon summary can cite decisions; avoids re-arguing settled points. |
| **Invariants as MUST / MUST NOT** | Hard constraints become refactor-vs-feature boundaries and review checks. |
| **Workstream dependencies** (not commits) | A short **partial order** (“A before B”) gives vertical-slice ordering without pretending to be git history. |
| **Acceptance mapping** | Table linking ticket AC to TDD sections/decisions keeps commits traceable to “done”. |
| **Implementation surface** | Distilled paths from source material — **start from recon Code map**; hints for `/feature-plan` Step 2, not a second recon pass. |
| **Explicit non-goals** | Stops the planner from inventing scope creep. |
| **Split “design unknown” vs “name TBD in code”** | Open follow-ups block planning; implementation-time TBDs do not. |
| **Tables and bullets over prose** | Easier to parse, less ambiguity, fewer tokens wasted. |

## Workflow

1. **Read** the user-provided path(s) (and Jira link inside the doc if present). **Do not** re-walk the codebase like a recon unless the user explicitly requests verification or the source material is missing critical facts — then ask or do the minimum lookup.
2. **Classify** into: intent, scope, boundaries, invariants, decisions, workstream order, testing contract, implementation surface hints, implementation-time TBDs, open follow-ups.
3. **Deduplicate**: one row per decision; merge redundant Q↔A and narrative repeats.
4. **Write** the TDD using the template below (omit empty sections; **keep heading names stable** so planners can skim).
5. **Handoff**: end with attaching this file for **`/feature-plan <KEY>`**; if **Open follow-ups** is non-empty, instruct to resolve before planning.

## Output location and naming

- Default directory: **`docs/feature-plans/`** in the active repo (same family as recon).
- Filename: **`<JIRA-KEY>-<kebab-slug>-feature-design.md`**
  - Reuse **`<kebab-slug>`** from the source recon when it exists (e.g. `EDATA-1348-html-json-format-features-feature-design.md` beside `EDATA-1348-html-json-format-features.md`).
  - If only a grilling session file exists (`grill-me` / `grill-with-docs` log), use **ticket key + short slug from the ticket title** (3–5 words).
- Do **not** delete or rewrite the source recon / grill file unless the user explicitly asks.

## TDD template (copy this shape)

```markdown
# Technical design: <JIRA-KEY> — <short title>

| Field       | Value |
| --- | --- |
| **Jira** | <link or key> |
| **Sources** | <paths to recon and/or grilling session log (`grill-me` / `grill-with-docs`)> |
| **Status** | TDD — <frozen / pending follow-ups> |

## Intent

<2–4 sentences: problem, user/engineering outcome, what “done” means.>

## Acceptance mapping

| AC (from Jira) | Satisfied by (TDD section / decision ID) |
| --- | --- |
| … | … |

(Omit if ticket has no AC list.)

## Scope

### In scope

- …

### Out of scope / deferred

- …

## Architecture and boundaries

<Modules, layers, public surfaces, ownership. Table OK.>

## Contracts and invariants

- **MUST** …
- **MUST NOT** …

## Decisions (authoritative)

| ID | Decision | Rationale |
| --- | --- | --- |
| D1 | … | … |

## Alternatives considered

- **<Name>** — discarded because …

## Workstream dependencies

<Order-only hints between coarse workstreams, not commits. Example: “Content-script gate must exist before sidepanel asserts on capture signal” or “Extract shared helper (no behavior change) before moving format UI”. Bullets or numbered partial order.>

## Testing and verification

<Layers, journeys, what must be true at design level — enough for the planner to attach tests to the right commits.>

## Implementation surface (hints)

### Canonical paths (from recon)

| Path (repo-relative) | Role (one line) |
| --- | --- |

<Bullets for extra modules / test files **only if** called out in source docs or grill decisions — consolidation, not fresh recon. Omit this entire section if empty.>

## Implementation-time TBDs

<Symbol names, exact spy hooks, etc. Allowed to stay open for coding; must not disguise unresolved design.>

## Open follow-ups

<Design/product/security unknowns. Empty = none. Planning should block until cleared.>

## Next step

<Attach this file and run `/feature-plan <JIRA-KEY>` (or resolve Open follow-ups first).>
```

## Quality bar

- **`/feature-plan` contract**: the TDD is **self-contained** for engineering intent (Jira for AC wording; this file for resolved design). **Sources** row is for audit only.
- **No ghost options**: one chosen approach unless Open follow-ups says otherwise.
- **No duplicate decision tables**: merge grill + recon into **Decisions** once.
- **Traceability**: **Sources** lists upstream paths.
- **Proportional**: small ticket → short TDD; do not pad.
