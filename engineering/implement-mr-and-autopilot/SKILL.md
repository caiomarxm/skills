---
name: implement-mr-and-autopilot
description: >-
  Use this when the user asks you to fully implement and autopilot an MR from a
  commit-by-commit feature plan. This assumes no user interaction until the whole
  loop is complete.
disable-model-invocation: true
---

# Implement MR and Autopilot

Ship one MR from an approved feature plan. Planning is done — do not run `feature-plan` or `grilling`.

## Inputs

**Feature plan** — the file with a `## Plan` section (often a grilling log or feature design). This is the only thing you must be given. If it is missing, stop and ask.

**Which MR** — resolve it yourself, do not open with a question:

- Plan has no `### MR <N>` headings, just one commit list → that list is the MR. Start.
- Plan has exactly one `### MR <N>` heading → that is the MR. Start.
- Plan has several MRs and the user named one → do that one.
- Plan has several MRs and the user named none → ask which, and only that.

Say which reading you took in your first message, then get going. Asking a question the plan already answers costs the user a round-trip for nothing.

The plan is the source of truth: commits, tests, guardrails, and settled decisions. Do not relitigate them.

## Branch

Work **in this workspace**. Do not make a worktree unless the user asks.

Before the first commit, check what branch you are on:

- Already on a feature branch for this ticket → stay on it.
- On the default branch (`main`/`master`) → pull latest, then cut a branch first. Name it to match recent branches in `git log --oneline`, using the ticket key from the plan filename (e.g. `EDATA-1790/xpath-consistency`).

Never commit this work directly onto the default branch.

## Bar

**KISS and YAGNI.** Smallest diff that satisfies the commit. No new abstractions, names, or layers the plan does not already use. Match surrounding code and tests.

## Loop — once per commit, in plan order

### 1. Implement (Composer 2.5)

Dispatch a `generalPurpose` subagent, `model: "composer-2.5"`. It runs [feature-implement](../feature-implement/SKILL.md) and **must leave the diff unstaged**. Prompt:

```text
/feature-implement @<plan-file> commit <K>

The commit list is in the ## Plan section<, under ### MR N — include only if the
plan actually has MR headings>. Implement only commit <K>.
Decisions above the plan are settled — follow them, do not relitigate.

KISS and YAGNI. Smallest thing that satisfies the commit. No new abstractions,
no new vocabulary, no second-caller generalising. If you name a concept the
plan does not already name, stop.

Validate with unit tests and linting. Report what you changed, what you ran, and what you
deliberately did not do.
```

### 2. Bugbot (Grok 4.6)

After the implementer returns, run the `review-bugbot` skill on **this commit's unstaged diff** (`Diff: uncommitted changes`). Launch the `bugbot` subagent with `model: "cursor-grok-4.6-high"`.

Fix real findings. Skip noise. Re-run the tests that prove the fix.

### 3. Your review, then commit

Do not rubber-stamp. Read the whole diff:

- It does what this commit says. Nothing from a later commit leaked in.
- Project architecture rules still hold.
- Tests assert behavior, not implementation, and ship in the same commit.

Then commit. Format: project commit-message rule (usually `:gitmoji: value`, max 50 characters). Use the plan's title when it already fits.

## After every commit is in

Run the full lint and test suites the repo (or the plan) names. Fix anything red. Do not open an MR on a red tree.

## Open the MR

Mirror the two most recent merged MRs on this repo.

- Title: ticket key + short product title.
- Description: brief, product-focused — what the product gains, not a file tour.

## Then keep it merge-ready

Run the `autopilot` skill. Do not merge it yourself.
