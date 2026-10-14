---
name: feature-plan
description: >-
  Use this when the user has an approved spec or design and wants a
  commit-by-commit vertical-slice implementation plan. Appends ## Plan to the
  source file.
disable-model-invocation: true
---

# Feature Plan

Turn an approved source into the smallest coherent sequence of commits.

Optimize for the final code, not for tiny commits. The final result must be
KISS and YAGNI: no dead code, temporary scaffolding, speculative hooks, or
abstractions that the desired outcome does not need.

## Input

The source is an approved spec or design file. It must contain the settled
scope, decisions, code areas, tests, and constraints.

- A Jira key or URL may help locate the source. Jira is not the source.
- Read Confluence only when the user asks.
- No source file → ask for it.
- An unresolved decision or `TBD` that blocks ordering → ask about that one
  point.

Do not run fresh recon. If the source lacks the facts needed for a safe plan,
say what is missing.

## Build the plan

Read the source end to end. Later accepted decisions override earlier open
questions.

First, picture the smallest final implementation that satisfies the source.
Every planned file, type, helper, dependency, flag, and config must serve a
required outcome or an existing contract.

Then split that final implementation into commits.

### Commit rules

Each commit:

- Has one clear intent.
- Leaves the code buildable and runnable.
- Includes the tests that prove its behavior.
- Defines and uses new code on a live path.
- Adds a dependency only when it first uses it.
- Is easy to review on its own.

Every behavior commit must be a vertical slice: one outcome through every
layer it needs, from the entrypoint through the domain and integration to its
tests.

A refactor-only commit is the one exception. Use one only when the final
design needs it. All refactor-only commits must come before all behavior
commits. Each must leave the code green, add no product behavior, and enable
a named vertical slice. Once behavior commits start, no later refactor-only
commit is allowed.

Do not:

- Split work only to make commits smaller.
- Leave dead code or unused abstractions between commits.
- Mix unrelated cleanup with behavior.
- Add future-proofing that the source does not require.
- Put behavior and its tests in separate commits.

The whole sequence must end in the simplest design that meets the source.
If two commits create needless scaffolding that a single coherent commit
avoids, use one commit.

Commit titles use gitmoji and stay within 50 characters.

## Write the plan

Append `---` and `## Plan` to the source file. If `## Plan` already exists at
the end, replace that section only. Never edit the source above it.

Keep the strategy short. Do not repeat decisions already in the source. Use
this template:

```markdown
---

## Plan

### Vertical slice strategy

<How the commits build the smallest final implementation. Put every required
refactor first and name the vertical slice it enables. Every later commit is
a vertical slice.>

### Commits

1. `<gitmoji> <title ≤50 chars incl. gitmoji>`

   - Outcome
   - Changes
   - Tests
   - Why this boundary

2. `<gitmoji> <title ≤50 chars incl. gitmoji>`
   - Outcome
   - Changes
   - Tests
   - Why this boundary

<!-- repeat -->
```

## Finish

Summarize the plan and point to the file. Ask for approval. After approval,
remind the user:

`/implement-pr-and-autopilot @<source-file>`
