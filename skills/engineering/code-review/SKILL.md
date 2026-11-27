---
name: code-review
description: 'Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".'
---

Review a diff with one subagent per review skill in this folder. They run in parallel so they don't pollute each other's context, then this skill aggregates their findings. When the caller asks for fixes, step 5 applies them.

When you run as a subagent, "ask the user" below means stop and ask the parent.

## Process

### 1. Pin the diff

Whatever the user said is the fixed point (a commit SHA, branch name, tag, `main`, `HEAD~5`, etc.). If they didn't specify one, ask for it.

Capture the diff command once:

- **Committed work:** `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.
- **Uncommitted work** (the caller says so, and names the directory: this workspace or a worktree path): in that directory, `git diff HEAD` plus the untracked files from `git status --porcelain`. The three-dot command misses it.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here, not inside the review sub-agents.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. A path or text the user passed as an argument.
2. Issue references in the commit messages or branch name (`#123`, `Closes #45`, GitLab `!67`, Jira `ABC-123`), fetched with the tracker tools you have (GitLab, Jira).
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, pass `Spec: none`.

### 3. Spawn one subagent per review

Each subdirectory of `~/code/skills/skills/engineering/code-review/` that contains a `SKILL.md` is one review. Spawn one subagent per skill, together, in the foreground. Use `subagent_type: generalPurpose` and name the model explicitly: the one the caller names, else Composer 2.5.

Same prompt for each, with that skill's name:

```text
Read-only. Do not edit files.
Read ~/code/skills/skills/engineering/code-review/<name>/SKILL.md and follow it.

Diff: <diff command>
Commits: <commit list>
Spec: <path or fetched contents, and which part is in scope. none when there is no spec.>
<Extra checks from the caller, if any.>
```

Extra checks add to a review, never replace it. Always run every review skill, even when the caller says "review only". A skill that does not apply reports that and stops.

### 4. Aggregate

Present each report under its own heading, named for the skill (`## Standards`, `## Spec`, …), verbatim or lightly cleaned. Do **not** merge or rerank findings across reviews (see _Why separate reviews_).

End with a one-line summary: total findings per review, and the worst issue _within each review_ (if any). Don't pick a single winner across reviews: that's the reranking the separation exists to prevent.

Stop here unless the caller asked for fixes.

### 5. Fix (only when asked)

Apply the findings, Spec first, then the other reviews. Spec fixes change behaviour; the others then shape the result. Where a Spec fix touched the lines another finding quotes, re-check that finding against the new code.

- **Spec (a) missing or partial** → implement it.
- **Spec (b) scope creep** → remove it, unless the spec needs it to work; then keep it and say why.
- **Spec (c) wrong** → fix it at the root cause.
- **Standards, hard** → fix it.
- **Standards, judgement call** → fix it when you agree; otherwise leave it and say why in one line.
- **Any other review** → a hard finding, fix it. A judgement call, fix it when you agree; otherwise leave it and say why in one line.

Change only what a finding names. Keep every `ponytail:` comment and the simplification it marks. Keep every test in the diff. New non-trivial logic gets one small runnable check.

Then run the repo's tests, typecheck, and lint on the touched paths. A fix that breaks a check and you can't repair → revert it and mark it left.

Tag each finding in the step 4 report **fixed** or **left: <reason>**. Leave changes unstaged. Do not commit.

## Why separate reviews

A change can pass one review and fail another:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one review from masking another.
