---
name: feature-implement
description: >-
  Implements a piece of work from a spec, a ticket, a task in the prompt, or
  one commit of a plan, leaving an unstaged diff. Use when the user runs /feature-implement.
disable-model-invocation: true
---

# Feature Implement

Implement the work described in the spec, ticket, or plan the user gives you.
Your job is correct code. Code quality is the reviewer's job.

## Input

- **A spec or plan file, a ticket reference, or a task written in the
  prompt.** Ticket (Jira `ABC-123`, GitLab issue) → fetch it from the tracker
  and state its title before starting. Ambiguous reference → ask.
- **Optional: one commit of the plan's commit list.** Implement only that
  commit. The rest of the list is out of scope.

The spec is the source of truth. Do not relitigate the decisions it settles.

## Work

- Read the spec and the code the change touches. Trace the real flow before
  you edit.
- Write tests at the seams the spec names. Spec silent → test the behaviour
  you add or change.
- Run typecheck and single test files regularly, and the full test suite once
  at the end. Prefer the repo's Make targets.
- Fix what this work breaks. Pre-existing failures → report them, do not
  chase them.

## Finish

Leave all changes unstaged. Do not commit.

Report:

- What you implemented.
- Files changed.
- Verification commands run, with pass/fail.
- Tests you did not add, and why.
- Work left for later commits.
