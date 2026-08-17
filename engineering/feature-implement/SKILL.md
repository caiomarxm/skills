---
name: feature-implement
description: >-
  Implements exactly one commit from an approved feature design, leaving a
  clean unstaged diff for human review. Use when the user runs /feature-implement
  with a feature design file and commit number, or asks to implement one planned
  commit from a feature design.
disable-model-invocation: true
---

# Feature Implement

Implement exactly one commit from an approved feature design, leaving a clean unstaged diff for human review.

This command picks up where `/feature-plan` left off. Treat the feature design as the source of truth for intent, boundaries, commit scope, implementation hints, and verification expectations.

## Input

This command expects two pieces of input after `/feature-implement`:

- **Feature design file** (required) — a path or file reference to the approved feature design.
- **Commit number** (required) — the single commit from the design's commit plan to implement.

Example usage:

```text
/feature-implement @docs/feature-plans/EDATA-1398-crawlingui-ui-ux-improvements-after-refactor-feature-design.md commit 1
```

If either input is missing or ambiguous, stop and ask for the missing value. Do not infer a commit number.

## Non-Negotiables

- Implement one commit only.
- Leave all changes unstaged for human review.
- Do not create commits.
- Do not rewrite history.
- Do not stage files unless the user explicitly overrides this command.
- Do not broaden scope beyond the selected commit unless the design says the dependency is required for that commit.
- Prefer the design's recon and implementation surface over fresh broad exploration.

## Step 1 — Load The Feature Design

Read the provided feature design file. Extract and keep visible while working:

- Intent.
- Acceptance mapping.
- Scope and out-of-scope.
- Architecture boundaries.
- Contracts and invariants.
- Implementation surface and recon hints.
- Testing and verification guidance.
- The selected commit's title, purpose, code areas, tests, and reason for isolation.

If the design contradicts the user's request, stop and ask before coding.

## Step 2 — Build The Commit Execution Card

Before editing, produce a short execution card for the selected commit:

- **Commit:** number and title.
- **Purpose:** one or two sentences from the design.
- **Likely files:** files from the selected commit plus relevant recon paths.
- **Rules/docs to read:** only rules, context files, or architecture docs relevant to the selected commit.
- **Tests required:** tests explicitly called out for this commit, or why this commit is style-only and should not add direct style assertions.
- **Verification:** targeted commands to run after implementation.
- **Out of scope:** nearby work from other commits that must not be pulled in.

Use this card as the working contract. If implementation reveals that the card is wrong, update the user before expanding scope.

## Step 3 — Inspect Narrowly

Trust the feature design first. Read only the files needed to implement the selected commit.

Use the design's recon paths and commit-specific code areas to find:

- Existing conventions and local patterns.
- Public APIs and ownership boundaries.
- Existing tests that should be extended.
- Existing Makefile or package scripts for scoped verification.

When a task crosses several modules or the needed files are unclear, delegate focused exploration to sub-agents instead of widening the main context. Ask explorers for paths, symbols, ownership notes, test targets, and risks rather than full file dumps.

## Step 4 — Implement The Selected Commit

Implement the smallest coherent diff that satisfies the selected commit.

- Follow existing conventions and local patterns.
- Keep behavior, ownership, and contracts unchanged unless the selected commit explicitly changes them.
- Prefer strong types and readable functional style where the codebase supports it.
- Keep style-only changes in styling/theme layers when the design asks for visual polish.
- Add abstractions only when they remove real duplication or match an existing local pattern.
- Fix issues inside this commit's scope immediately; do not leave known breakage for a later commit.

## Step 5 — Add Or Update Commit-Specific Tests

Each selected commit must have its own test decision.

- For behavior changes, add or update targeted tests in the same commit scope.
- For accessibility-visible UI changes, test visible labels, roles, states, tooltips, modal behavior, and user outcomes.
- For style-only/theme commits, do not add direct style snapshots or theme-output assertions unless the design explicitly requires them. Instead, verify by typecheck, lint, and manual review notes.
- Extend existing tests before adding new test files when that better matches local conventions.
- If no automated test is appropriate, record why in the final review prompt.

## Step 6 — Verify With The Smallest Useful Commands

Prefer repository Make targets when available, especially scoped targets for touched paths. If no Make target exists, use the nearest package scripts or test runner conventions already present in the repo.

Verification should normally include:

- Targeted tests for the selected commit's touched behavior.
- Scoped lint and format checks for touched paths.
- Typecheck or compile when shared types, providers, exported APIs, or cross-module contracts are touched.
- Full test/lint/compile only when the selected commit has broad blast radius or the repo has no reliable scoped alternative.

Fix any errors introduced by this work. Do not chase unrelated pre-existing failures unless they block verification; report them clearly instead.

## Step 7 — Prompt Human Review

Stop with changes unstaged. Report:

- What was implemented for the selected commit.
- Files changed.
- Tests and verification commands run, with pass/fail status.
- Any tests intentionally not added and why.
- Manual review notes, especially for visual polish or UX details.
- Any follow-up work that belongs to later commits in the design.

Ask the user to review the unstaged diff. Do not commit.

## Mental Model

The feature design is the map. The selected commit is the boundary. The output is a reviewable unstaged diff with its own verification story.
