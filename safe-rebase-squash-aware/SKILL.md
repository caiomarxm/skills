---
name: safe-rebase-squash-aware
description: Rebase a feature branch onto a target branch when history may include squash merges, stacked branches, parallel topic merges on the target, or rewritten commits. Use when a user asks to rebase carefully and avoid fork-point confusion.
disable-model-invocation: true
---

# Safe Rebase (Squash-Aware)

## When To Use

Use this skill when the branch must be rebased onto another local branch, and the target may include **squash merges**, **stacked branches**, **topic merges on the target that are not ancestors of your branch**, or **rewritten history** that can confuse `--fork-point` or a naive `merge-base`.

## Goal

Identify the correct anchor commit (the last commit that should **not** be replayed), then rebase with `git rebase --onto` so only intended commits are moved.

## Failure Modes `merge-base` Alone Does Not Catch

`git merge-base HEAD <target>` finds the **latest common ancestor in the graph**. That is correct for topology, but it can still pick an anchor that is **too old** for intent:

1. **Squash merge on target** — Your individual commits never became ancestors of `target`; the replay range `<merge-base>..HEAD` still contains patches that are **already applied** on `target` as one squashed commit (different hashes). Replaying them causes duplicate logic or conflicts.

2. **Parallel topic work on target** — After the merge-base, `target` gained a merge commit + topic branch (e.g. “extract module X”) while your branch evolved the **same area** on a **different line** (your commits are not descendants of that topic). The merge-base remains the old fork, so a naive replay re-applies **superseded** refactors and collides with what landed on `target`.

3. **Rewritten / replaced commits on target** — Same symptom as (1): ancestry does not reflect “already integrated.”

**Lesson:** Anchor choice must be validated against **what landed on `target` after the merge-base**, not only against the merge-base hash.

## Workflow

1. Check branch state and target existence.
2. Propose a **candidate** anchor (merge-base with parent and/or target).
3. **Validate** candidate against commits on `target` after that anchor; adjust anchor forward on your branch if `target` already absorbed overlapping work.
4. Rebase with `git rebase --onto <target> <anchor>`.
5. Verify commit range and branch divergence.
6. Report whether a force push is required.

## Commands

### 1) Preflight

```bash
git rev-parse --abbrev-ref HEAD
git branch --list "<target-branch>"
git status --short
```

If there are uncommitted tracked changes, stop and ask the user whether to stash/commit first.

### 2) Candidate Anchor (Ancestry Only — Not Sufficient Alone)

Prefer this order:

1. **Known parent branch in stacked flow** (best signal when the parent’s commits are still the same objects on your branch):

```bash
git merge-base HEAD <parent-branch>
```

Use as candidate when `<parent-branch>` represents work you intentionally stacked on, and you know how that parent was merged into `target` (merge vs squash).

2. **Direct base with target** (fallback candidate):

```bash
git merge-base HEAD <target-branch>
```

### 3) Mandatory Validation Before Rebase

Let `<candidate>` be the chosen merge-base (or another explicit commit: “everything after this on my branch should be replayed”).

**A — What did `target` gain after the candidate?**

```bash
git log --oneline --decorate <candidate>..<target-branch>
```

- If this range is **non-empty**, scan commit subjects (and merges) for refactors, renames, or tickets that **overlap** the themes of your branch’s pending work.
- If overlap is plausible, **inspect** whether those `target` commits supersede part of your stack. If yes, move the anchor **forward along your branch** to the **last** commit you consider already represented on `target` (exclusive end of replay), then re-check `git log <new-candidate>..HEAD` until the replay list matches intent.

**B — What will you replay?**

```bash
git log --oneline <candidate>..HEAD
```

The range `<candidate>..HEAD` must contain **exactly** the commits that should be replayed onto `target`. If the first commit in this list touches the same modules as recent `target`-only merges, suspect a **too-old** anchor.

**C — Optional graph context**

```bash
git log --oneline --decorate --graph --boundary HEAD <target-branch> <parent-branch>
```

**D — Squash equivalence (patch-id) is a weak hint**

```bash
git cherry -v <target-branch> HEAD
```

Every commit marked `+` can still be “effectively already on `target`” via a squash merge (patch-id match is not guaranteed). Use cherry as a secondary signal, not proof.

### 4) Rebase (No Fork-Point)

```bash
git rebase --onto <target-branch> <anchor>
```

Do not use `--fork-point` in this workflow.

### 5) Conflict Signal: Wrong Anchor

If **the first replayed commit** produces **large conflicts** in the same subsystem that `git log <original-merge-base>..<target>` showed was recently refactored on `target`, **stop** and treat anchor as too old:

```bash
git rebase --abort
```

Pick a **later** anchor on your branch (parent of the first commit you still need), re-run `git log <anchor>..HEAD` for sanity, then:

```bash
git rebase --onto <target-branch> <anchor>
```

Do not stack conflict resolutions for commits that `target` already subsumed unless the user explicitly wants to keep and merge both lines.

### 6) Post-Checks

```bash
git status -sb
git log --oneline --decorate --graph --max-count=20
```

Confirm:

- Branch tip now sits on `target` history.
- Only intended commits were rewritten.
- No unintended dropped commits (compare `git log --oneline <old-merge-base>..<old-HEAD>` themes vs new replay list if needed).

## Conflict Handling (Mechanical)

- Resolve conflicts file by file.
- `git add <resolved-files>`
- `git rebase --continue`
- If the chosen anchor is wrong, abort and restart from section 3–4:

```bash
git rebase --abort
```

## Reporting Template

Use this structure in the final message:

1. Rebase target and command used (`--onto` + anchor).
2. Whether conflicts occurred; if aborted and re-anchored, say why (e.g. parallel topic merge on target).
3. New branch relation to remote (`ahead/behind`).
4. If history was rewritten, suggest:

```bash
git push --force-with-lease
```

## Guardrails

- Never use destructive reset commands.
- Never force-push automatically unless user asks.
- Preserve unrelated local changes and untracked files.
