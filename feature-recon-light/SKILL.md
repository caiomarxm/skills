---
name: feature-recon-light
description: >-
  Bootstrap a Jira ticket recon file with canonical code map (light depth) at
  docs/feature-plans/<KEY>-<slug>.md. Use when scope is clear, before grill-me
  or grill-with-docs or feature-design, or when you only need a path allowlist.
  Escalate to feature-recon (deep) for approaches and trade-offs.
disable-model-invocation: true
---

# Feature recon (light)

Bootstrap a ticket recon file with **Jira context** and a **canonical code map** (implementation surface only). Use when scope is already clear, when you will **`grill-me` or `grill-with-docs` first** without a full deep pass, or when you only need a path allowlist before design.

**Output:** the same living recon file as deep recon (`docs/feature-plans/<JIRA-KEY>-<slug>.md`), but **without** approaches, deep pattern mining, or external research unless the ticket explicitly needs it.

**Next steps (typical):** `grill-me` or `grill-with-docs` (optional) → **`feature-design`** (TDD) → `/feature-plan`. Escalate to **`feature-recon`** (deep) if Open Questions pile up, scope is fuzzy, or you need 2–4 approaches compared.

---

## The recon file

Same path and “living scratchpad” rules as **`feature-recon`** (deep): one file per ticket slug, **write findings to the file as you go**, do not leave map-only discoveries in chat.

### Template (light)

Initialize or extend the file with this shape (sections can stay sparse; **Code map** should be non-empty before you stop).

```markdown
# Recon: <JIRA-KEY> — <Ticket Title>

**Recon depth:** light

## Ticket Summary

- **Title:** ...
- **Description:** ...
- **Acceptance Criteria:**
  - ...
- **Non-goals:** ...
- **Linked Tickets:**
  - EDATA-XXX — Title (Status)

## Confluence Notes

(Omit if no Confluence URL was provided.)

## Code map (canonical)

| Path (repo-relative) | Role (one line) |
| -------------------- | --------------- |

## Codebase Findings

### Implementation Surface

<Short bullets — entrypoints, owners, message boundaries if any.>

### Existing Patterns

(Omit in light unless one pattern is obvious from a single file skim.)

### Reuse Opportunities

(Omit unless obvious.)

### What Changes vs. What Doesn't

**Changes:**

**Unchanged:**

(Omit subsections if unknown — list under Open Questions instead.)

## Approaches

_(Deferred — use **`feature-recon`** (deep) if you need 2–4 approaches + recommendation.)_

## Recommendation

_(Deferred — or a single provisional sentence if the ticket already dictates one obvious path.)_

## Open Questions

- ...

## Grill log

_(Optional — append Q / answer / decision ref while using `grill-me` or `grill-with-docs`.)_
```

---

## Parameters

- **Jira ticket** (required) — key or full `https://checkr.atlassian.net/browse/...` URL (same as deep recon).
- **Confluence page URL** (optional).

Examples:

```
/feature-recon-light EDATA-790
/feature-recon-light https://checkr.atlassian.net/browse/EDATA-790
```

---

## Step 1 — Jira and bootstrap the recon file

Same as deep recon **Step 1**: fetch Jira (MCP `getJiraIssue`, `cloudId: "95385d81-cba9-4876-9fe8-c7bc1357f516"`, `responseContentFormat: "markdown"`), glob `docs/feature-plans/<JIRA-KEY>-*.md`, **reuse** existing file or create from the **light** template above. Fill **Ticket Summary**.

---

## Step 2 — Confluence (if URL provided)

Same as deep recon **Step 2** (`getConfluencePage`, `contentFormat: "markdown"`). Keep notes short.

---

## Step 3 — Codebase exploration (bounded)

Goal: **Code map** + a tight **Implementation Surface** — not deep pattern archaeology.

1. Read **`.cursor/rules/architecture-rules.mdc`** to pick the right component docs; load **only** what you need to orient (same table as deep recon Step 3.1 — do not read extension docs for a backend-only ticket).
2. **Glob / grep / narrow reads** to list modules the ticket likely touches. Prefer directory listing and symbol search over reading whole files.
3. For each candidate path, add a **Code map** row: `path` + **one line** role.
4. **Implementation Surface**: bullets that name owners, entrypoints, and boundaries (sidepanel vs content vs background, messaging, persistence), still brief.
5. **Stop** when the map covers the likely touch set or you hit diminishing returns — note gaps in **Open Questions** instead of deep-diving.

**Rules**

- **All paths you opened meaningfully** belong in **Code map** (canonical allowlist for later `feature-design` / `/feature-plan`).
- **No chat-only findings** — if you learned it, it goes in the file.
- **Do not** run the deep recon “read surrounding code deeply” pass here; that is **`feature-recon`** (deep).

---

## Step 4 — Present and hand off

Summarize in chat: ticket one-liner, **Code map** highlights, **Open Questions**.

Remind the user: optional **`grill-me`** or **`grill-with-docs`** (with this file attached) → **`feature-design`** → `/feature-plan`. If scope or trade-offs are still unclear, run **`feature-recon`** (deep) on the **same** file (append; do not start a duplicate).
