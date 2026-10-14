---
name: implement-mr-and-autopilot
description: >-
  Use this when the user asks you to fully implement and autopilot an MR from
  a commit-by-commit plan (preferred), a spec, a design doc, or a task in the
  chat. This assumes no user interaction until the whole loop is complete.
disable-model-invocation: true
---

# Implement MR and Autopilot

Ship one MR. Do not plan: no `feature-plan`, no `grilling`.

## Input

The **source** is one of:

- A commit-by-commit plan: a file with a `## Plan` section. Preferred.
- A spec or a design doc.
- A task described in the chat.

No source → stop and ask.

The source is the truth for scope, tests, and settled decisions. Do not
relitigate them.

**Commits:**

- The source has a commit list → one loop per commit, in order.
- No commit list → the whole task is one commit.

**Which MR** (only for plans with `### MR <N>` headings):

- One heading → that MR.
- Several, and the user named one → that one.
- Several, and the user named none → ask which. Ask nothing else.

State your reading (source, MR, commits) in your first message, then start.

## Branch

Work in this workspace. No worktree unless the user asks.

Before the first commit:

- On a feature branch for this task → stay on it.
- On the default branch (`main`/`master`) → pull, then cut a branch. Match
  the naming of recent branches in `git log --oneline`. Use the ticket key
  from the source when there is one (e.g. `EDATA-1790/xpath-consistency`).

Never commit to the default branch.

## Loop — once per commit

### 1. Implement

Launch the `implementer` subagent. It runs
[feature-implement](../feature-implement/SKILL.md) and leaves the diff
unstaged.

**Source is a file:**

```text
/feature-implement @<source-file> commit <K>

Commit <K> is one commit of the list in the ## Plan section<, under ### MR N —
include only if the plan has MR headings>. Implement only commit <K>.
Decisions above the plan are settled — follow them, do not relitigate.
```

No commit list → send only `/feature-implement @<source-file>`.

**Source is the chat:** the subagent cannot see this chat. Write the task and
every piece of context it needs into the prompt:

```text
/feature-implement

<the task: what to build, and the decisions already made>
<the context: files, symbols, and constraints from the chat>
<only with a commit list: the full list, then "Implement only commit <K>.">
```

### 2. Review

Launch the `reviewer` subagent:

```text
Fixed point: HEAD. Review the uncommitted diff.

Spec: <@source-file, commit <K> | the task text you sent in step 1>.
Only commit <K> is in scope: later commits are not missing work.
Decisions in the spec are settled — do not relitigate them.
```

No commit list → drop the "Only commit <K>" line.

### 3. Commit

Commit the reviewer's result as is. Message: the project's commit-message
rule (usually `:gitmoji: slug`, max 50 characters). Use the commit's title
from the plan when it fits.

## After the last commit

- Run the full lint and test suites the repo (including integration and e2e).
  Fix anything red.
- Then run Bugbot on the full MR and see if there are any bugs,
  if there are, run the `implementer` subagent to fix them, then run
  the `reviewer` subagent once again. Commit the fixes (if any).
- Finally, launch the `validator` subagent. Optionally you can pass it specifics on
  how to validate the work if you have it, maybe in the spec or defined by the user:

  ```text
  Spec: <@source-file | the task text>. Prove its desired outcome works.
  Change: the commits since <base-branch>.
  ```

  - **works** → open the MR.
  - **does not work** → send the failing outcomes and their evidence to the
    `implementer` as the task, run the `reviewer`, commit, then validate
    again. Still failing → stop and report to the user.
  - **unproven** → open the MR, and list the gaps in its description.

Do not open an MR on a red tree.

## Open the MR

Mirror the two most recent merged MRs on this repo.

- Title: ticket key (when there is one) + short product title.
- Description: brief and product-focused — what the product gains, not a
  file tour.

## Keep it merge-ready

Run the `autopilot` skill, wait at least 10 minutes for comments. Do not merge.
