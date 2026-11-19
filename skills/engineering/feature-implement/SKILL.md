---
name: feature-implement
description: >-
  Makes product code correct from a spec, a ticket, or a task in the prompt,
  leaving an unstaged diff. Does not polish style: run code-review on the
  diff afterwards. Use when the user runs /feature-implement, or when
  implement-pr-and-autopilot launches it.
disable-model-invocation: true
---

# Feature Implement

You make the code correct. Correct means: it does what the task asks,
handles the cases the task implies, and breaks nothing that worked before.

Style, naming, structure, and repo conventions are not your job.
`code-review` handles them after you. Spend that effort on correctness.

## Input

- **A spec or plan file, a ticket reference, or a task written in the
  prompt.** Ticket (Jira `ABC-123`, GitLab issue) → fetch it from the tracker
  and state its title before starting. Ambiguous reference → ask.
- **Optional: findings to fix** (from a validation run or Bugbot). Then the
  findings are the task, and the spec is context.

The spec is the source of truth. Do not relitigate the decisions it settles.
A commit list in the spec does not bind you: build the whole scope in one
pass. Commits are organized at the end.

## Understand first

Read the spec and every file the change touches. Trace the real flow end
to end before you edit. A small change in the wrong place is a second bug.

## Scope

- Build only what the task asks. Speculative need → skip it, report it.
- Touch only what the change needs. Unrelated code that looks wrong →
  leave it, report it.
- Bug fix = root cause, not symptom. Before you edit a function, grep every
  caller. Fix it once, where all callers route through. Patching only the
  path the report names leaves sibling callers broken.

## Never cut

Input validation at trust boundaries. Error handling that prevents data
loss. Security measures. Accessibility basics. Anything explicitly
requested. Calibration knobs on anything that touches the physical world
(clocks, sensors, hardware).

## Known ceilings

A deliberate simplification with a known limit (global lock, O(n²) scan,
naive heuristic) gets a `ponytail:` comment naming the limit and the
upgrade path: `# ponytail: global lock, per-account locks if throughput matters`.

## Tests

Write tests at the seams the spec names. Spec silent → test the behaviour
you add or change. Non-trivial logic (a branch, a loop, a parser, a money or
security path) gets at least the smallest check that fails if the logic
breaks. Trivial one-liners need none.

Run typecheck and single test files as you go, and the full test suite once
at the end. Prefer the repo's Make targets. Fix what this work breaks.
Pre-existing failures → report them, do not chase them.

## Finish

Leave all changes unstaged. Do not commit.

Report:

- What you implemented, and the files changed.
- What you skipped: `skipped: X, add when Y.`
- Assumptions you made where the task was unclear.
- Verification commands run, with pass/fail.
- Tests you did not add, and why.
