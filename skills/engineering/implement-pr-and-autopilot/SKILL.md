---
name: implement-pr-and-autopilot
description: >-
  Use this when the user asks you to fully implement and autopilot a PR from
  a spec, a design doc, a plan, or a task in the chat.
disable-model-invocation: true
---

# Implement PR and Autopilot

The flow: QA plan → user OK → implement → review → check → validate →
commit → open the PR.

The work stays uncommitted until it is validated. Then it is one commit.

## You orchestrate. You do not do.

- Do not read code, edit files, run tests, review diffs, or validate
  yourself. Send a subagent. Git housekeeping is yours: pull, cut the
  branch, commit the validated diff.
- You hold the source, the QA plan path, and the subagent reports. You
  decide the next step from the reports.
- Never act on a step before the subagent you are waiting on returns.

## Subagents

Launch each with `subagent_type: generalPurpose` and a model from the
budget. Its prompt starts with the skill to follow, by absolute path (expand
`~` to `$HOME`):

```text
Read ~/code/skills/skills/engineering/<skill>/SKILL.md and follow it.
```

Budget:

- qa-plan, validate: Composer 2.5, or Grok 4.7 when the validation is very
  hard
- Implement, check, open PR: Composer 2.5
- Review: Composer 2.5, and its own sub-agents use Composer 2.5

## Input

The **source** is one of:

- A spec, a design doc, or a plan file.
- A task described in the chat.

No source → stop and ask.

The source is the truth for scope, tests, and settled decisions. Do not
relitigate them. The whole scope is built in one pass. A commit list in
the source is not an order of work.

**Which PR** (only for sources with `### PR <N>` or `### MR <N>` headings):

- One heading → that PR.
- Several, and the user named one → that one.
- Several, and the user named none → ask which. Ask nothing else.

State your reading (source, PR) in your first message, then start.

**Spec text.** Every subagent needs the spec. Source is a file → pass
`@<source-file>`, plus `PR <N>` when there are headings. Source is the chat →
the subagent cannot see this chat. Write the task, the decisions already
made, and the files, symbols, and constraints from the chat into one block,
and pass that same block to every subagent.

**QA plan path.** `${TMPDIR:-/tmp}/qa-plans/<repo>-<branch>.md`, resolved to
an absolute path. Outside the repo, so it never lands in the diff.

## Branch

Work in this workspace. No worktree unless the user asks.

Before you start:

- On a feature branch for this task → stay on it.
- On the default branch (`main`/`master`) → pull, then cut a branch. Match
  the naming of recent branches in `git log --oneline`. Use the ticket key
  from the source when there is one (e.g. `EDATA-1790/xpath-consistency`).

Never commit to the default branch.

## 1. QA plan

Launch the `qa-plan` subagent:

```text
Read ~/code/skills/skills/engineering/qa-plan/SKILL.md and follow it.

Spec: <spec text>.
QA plan path: <path>.
<How to validate, when the spec or the user names it.>
```

Then show the plan to the user, written the way the `plain-english` skill
says (plain style): what will be proven, how each check runs, what is
missing to run it, and what cannot be proven. Link the plan file. End with
one ask: OK to start, or what to change?

This is the only stop. Wait for the answer.

- **OK** → step 2. From here on, do not ask the user anything.
- **Changes** → relaunch the plan subagent with the user's words added,
  then show it again.

## 2. Implement

Launch the `feature-implement` subagent:

```text
Read ~/code/skills/skills/engineering/feature-implement/SKILL.md and follow it.

Spec: <spec text>. Build the whole scope in one pass.
Decisions in the spec are settled — do not relitigate them.
The QA plan at <path> says how the work will be proven.
```

## 3. Review

Launch the `code-review` subagent. It must spawn one subagent per review
skill, in parallel, then fix. A lighter review does not count.

```text
Read ~/code/skills/skills/engineering/code-review/SKILL.md and follow it
through step 5: review, then fix.

The diff is uncommitted, in <this workspace | the worktree at PATH>.
Fixed point: HEAD.

Spec: <spec text>.
Decisions in the spec are settled — do not relitigate them.
```

The report must have one heading per review skill. A missing heading means
that review was skipped. Relaunch it with the same prompt.

## 4. Check the tree

Launch a check subagent:

```text
Run the repo's full lint and test suites, including integration and e2e.
Prefer the repo's Make targets. Do not edit files.
Report each command, pass or fail, and the failing output.
```

Then run Bugbot on the uncommitted diff.

Red suites or Bugbot bugs → send them to `feature-implement` as findings,
then review again (step 3) and check again.

## 5. Validate

Launch the `validate` subagent:

```text
Read ~/code/skills/skills/engineering/validate/SKILL.md and follow it.

Spec: <spec text>.
QA plan path: <path>. It is approved.
Change: the uncommitted diff in <this workspace | the worktree at PATH>.
```

- **works** → step 6.
- **does not work** → send the failing checks and their evidence to
  `feature-implement` as findings, review again (step 3), check the tree
  (step 4), then validate again. Still failing → stop and report to the user.
- **unproven** → step 6, and list the gaps in the PR description.

## 6. Commit

Commit the validated diff yourself, as one commit. Do not run
`commit-story`. Do not split the history.

- Never commit to the default branch.
- Match the repo's recent commit message style.
- Do not commit secrets.

## 7. Open the PR

Do not open a PR on a red tree.

Launch a PR subagent:

```text
Read ~/code/skills/skills/engineering/pr/SKILL.md and follow it.

Open the PR for this branch against <default branch>.
Mirror the two most recent merged PRs on this repo.
Title: <ticket key, when there is one> + short product title.
Body: run the pr skill on the full branch diff and this validation report:
<the validate report>. <Gaps to list, when unproven.>
Return the PR URL.
```

## 8. Keep it merge-ready

Run the `autopilot` skill, wait at least 10 minutes for comments. Do not merge.
