---
name: commit-story
description: >-
  Use this when the work is done and validated, and the diff needs to become
  a sequence of vertical-slice commits that tell a story. Takes an
  uncommitted diff or a branch's commits and rewrites them into commits a
  reviewer can read in order. The final tree never changes.
---

# Commit Story

Turn a finished diff into the smallest coherent sequence of commits. The
code is already final and validated. You change how it is told, never what
it is.

## Input

- **The diff.** Uncommitted changes in this workspace (the usual case), or
  the commits on this branch since its base. No diff → stop.
- **Optional: the spec.** Use it to name the outcomes. A commit list in the
  spec is a hint for the story, not a contract: the final code may have
  moved away from it.

## 1. Freeze the final state

Before touching history, save the exact final tree so nothing can be lost:

- Uncommitted diff: `git add -A && git commit -m "wip: final state"`.
- Branch commits: nothing to commit.

Then `git branch <branch>-story-backup` and note `FINAL=$(git rev-parse HEAD)`
and `BASE=<merge-base with the default branch, or the HEAD before the wip
commit>`. Report the backup branch name. It is the undo path.

## 2. Plan the story

Read `git diff $BASE $FINAL` end to end. Then group it into commits.

Each commit:

- Has one clear intent.
- Leaves the code buildable and its tests green.
- Includes the tests that prove its behavior.
- Defines and uses new code on a live path.
- Adds a dependency only when it first uses it.
- Is easy to review on its own.

Every behavior commit is a vertical slice: one outcome through every layer
it needs, from the entrypoint through the domain and integration to its
tests.

A refactor-only commit is the one exception. Use one only when the diff
contains one. All refactor-only commits come before all behavior commits.
Each must leave the code green, add no product behavior, and enable a named
vertical slice.

Do not:

- Split work only to make commits smaller. One commit is a fine story.
- Leave dead code or unused abstractions between commits.
- Put behavior and its tests in separate commits.
- Invent intermediate code the final diff never needed, beyond what keeps a
  commit green.

Commit titles follow the repo's commit-message rule (usually
`:gitmoji: slug`, max 50 characters). Match recent `git log` titles.

## 3. Build the commits

`git reset --mixed $BASE`. The working tree is now `FINAL`, nothing staged.

For each planned commit, in order:

- Files wholly in this commit → `git add <file>`.
- Files split across commits → write the intermediate version this commit
  needs, `git add` it, then restore the final version after the commit with
  `git checkout $FINAL -- <file>`. Never stage a hunk from memory: read the
  file at `$FINAL` first.
- `git commit` with the planned title.

The last commit takes everything left. `git status` must be clean.

## 4. Verify

- **Same tree.** `git diff $FINAL HEAD` must be empty. Not empty → the
  story lost or changed code. Fix it before anything else.
- **Every commit green.** `git rebase --exec "<fast build + tests of the
  touched paths>" $BASE`. A commit fails → move the missing piece into it
  (or merge it with its neighbour), then verify again.

## Finish

Keep the backup branch. Report its name and the commit list: title, then
one line on its outcome.
