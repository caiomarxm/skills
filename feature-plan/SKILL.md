---
name: feature-plan
description: >-
  Produces a commit-by-commit vertical-slice implementation plan and appends
  ## Plan to an approved feature design or feature-plan source file. Use when
  the user runs /feature-plan, asks for commit planning, or has a TDD ready for
  implementation ordering.
disable-model-invocation: true
---

# Feature Plan

## Main goal (non-negotiable)

Produce a **solid commit-by-commit plan** whose commits are **vertical slices** wherever the TDD allows: each slice should, when possible, **cut through the stack** (UI → domain → integration → tests) for **one coherent behavior or user-visible increment**, stay **reviewable in isolation**, and **ship green** with tests in the same commit.

**Horizontal-only** steps (wide rename, extract-without call sites, dependency-only prep) are allowed **only** when the TDD’s **workstream dependencies** or **invariants** require preparing the ground first — then **return to vertical slices** immediately after.

This command **appends** **`## Plan`** to the **same** feature-plan source file. It does not replace the existing recon, decisions, notes, or source body.

---

## Heart and soul — commit planning principles

These rules define **what a good plan looks like**. The generated **Commits** list must satisfy every one.

### Each commit must

- Be **semantically coherent** — one clear story per commit.
- Be **reviewable in isolation** — a reviewer can understand and judge one diff.
- Be **buildable / runnable** — the tree stays green after each commit.
- Prefer a **vertical slice** — one end-to-end thread of value (or one enforced invariant path) plus the **tests that prove it**, in the **same** commit when feasible.
- Tell a clear step in the overall narrative — ordering must respect the TDD’s **workstream dependencies**.
- Include **both definition and usage** of anything new (no dead exports, no handler without sender).

### Each commit must not

- Introduce **unused** classes, functions, flags, or configs.
- **Mix refactors with behavior changes** — refactors are ground-prep; behavior commits wire on top.
- Combine **format-only / rename-only** churn with logic changes.
- Add **dependencies** before the commit that **first uses** them.

### Structure rules (numbered)

1. **One intent per commit** — answers exactly: _What changed, and why?_
2. **Class + usage in the same commit** — new module is **called** or integrated on a **live path**. **Usage = live code path.**
3. **Dependencies only when used** — add libs/internal deps in the first consuming commit.
4. **Refactors prepare the ground; features follow** — refactor commits: **zero** new product behavior; tests updated for shape only. Then vertical **feature** slices.
5. **Tests ship with the behavior commit** — no trailing “tests only” commit for new behavior.
6. **Commit titles** — gitmoji + **≤50 characters** total (gitmoji included); intent over mechanics.

Examples:

- `:sparkles: add request validator and enforce at entrypoint`
- `:recycle: split pricing logic from order aggregation`

---

## Parameters (feature-plan file is primary)

- **Primary input:** the existing feature-plan source file — usually **`docs/feature-plans/<JIRA-KEY>-*.md`**. The user **attaches** it or has it in context; that file is what you read first and what you **append the plan to**.
- The feature-plan source file is authoritative for scope, accepted decisions, code map, implementation notes, testing guidance, non-goals, and ordering constraints.
- **Optional:** Jira key or URL — use only for identifying the right feature-plan file if needed. Do **not** fetch Jira or use it to add new scope unless the user explicitly asks.
- **Optional:** Confluence URL — use only if the user explicitly asks for extra constraints; never a substitute for the feature-plan source file.

Example usage (ticket optional if the feature-plan file is attached and self-identifying):

```
/feature-plan EDATA-790
/feature-plan https://checkr.atlassian.net/browse/EDATA-790
```

---

## Step 1 — Read the feature-plan source file

1. Open the provided feature-plan source file. Read it **carefully end-to-end** — ticket summary, code map, findings, recommendation, grilling/session decisions, implementation notes, testing guidance, non-goals, and explicit implementation order.
2. Treat later accepted decisions as the source of truth over earlier exploratory questions. A historical **Open Questions** section does not block planning if the same file later records accepted decisions that resolve those questions.
3. Stop and ask the user only when the file has an explicit unresolved blocker: missing source file, missing accepted decisions, `TBD`, "decision pending", incomplete/unclear implementation order, or session/status language saying the plan is not ready.
4. If no feature-plan source file is attached or findable for the ticket — **stop**: ask the user for the feature-plan file. **Do not** plan from Jira alone and **do not** perform fresh recon to manufacture a plan.
5. Do **not** edit the source body above the plan — only append or replace **`## Plan`** in Step 3.

---

## Step 2 — Extract commit-planning inputs

Do not perform fresh codebase reconnaissance. The job of this command is to transform the already-researched feature-plan source file into a commit-by-commit implementation plan.

Extract only what is needed to order and describe commits:

- Accepted decisions and decision constraints.
- Explicit implementation order and workstream dependencies.
- Behavior changes vs. visual/style-only changes.
- Code areas from the code map and implementation surface.
- Required tests and verification.
- Non-goals, guardrails, and "what does not change".
- Any implementation notes that affect commit boundaries.

If the source file does not contain enough information to produce a safe commit plan, stop and ask for the missing decision or ask the user to re-run the upstream recon/grilling command. Do not fill gaps by exploring the codebase.

---

## Step 3 — Write the plan and append

### Where

- **Append** to that same feature-plan source file: after the document body, insert `---` then **`## Plan`**.
- If **`## Plan`** already exists at the bottom, **replace** from `## Plan` through end-of-file.
- **Never** delete or rewrite the source body above the separator.

### What

The appended block adds **vertical-slice commit ordering** only — no duplicate decision tables. The **Commits** list is the bulk of the plan; keep **Vertical slice strategy** short and source-derived. Use **only** this template:

```markdown
---

## Plan

### Vertical slice strategy

<a few sentences: how commits chain as vertical slices, any required horizontal prep first, respect TDD workstream deps.>

### Commits

1. `<gitmoji> <title ≤50 chars incl. gitmoji>`

   - Purpose
   - Code areas touched
   - Tests added/updated in this commit
   - Why this is its own commit (**call out vertical slice** or why prep-only horizontal step)
   - Optional when useful: Depends on / Source anchors / Guardrails / Verification

2. `<gitmoji> <title ≤50 chars incl. gitmoji>`
   - Purpose
   - Code areas touched
   - Tests added/updated in this commit
   - Why this is its own commit (**call out vertical slice** or why prep-only horizontal step)
   - Optional when useful: Depends on / Source anchors / Guardrails / Verification

<!-- repeat -->
```

### Finish

1. Append the filled template.
2. Summarize in chat; point to the file.
3. Ask for review/approval; edits touch only the **`## Plan`** block.
4. After approval, remind: `/feature-implement <JIRA-KEY>` (or ticket from the feature-plan source file).
