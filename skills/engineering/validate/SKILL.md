---
name: validate
description: >-
  Use this to prove a change works with real evidence. Two modes: `plan`
  writes a QA plan from the spec before the code exists; `run` executes a QA
  plan against the change, as close to production as the repo allows:
  services in Docker with mocked data, a live driver, a real CLI or API call.
  Never edits product code.
---

# Validate

You prove that the change works. Proof is what you observe when you run the
real thing. Reading the code is not proof. Passing unit tests are not proof.

## Input

- **Mode**: `plan` or `run`. Not given → `plan` when there is no QA plan
  yet, `run` when there is one.
- **Spec**: the desired outcome. A file, a ticket, or text. No spec → stop
  and ask.
- **QA plan path**: where `plan` writes the plan, and where `run` reads it.
  Outside the repo, so it never lands in the diff.
- **Change** (`run` only): the fixed point, the uncommitted diff, or the
  files changed, to aim your checks.
- **How to validate** (optional): steps the spec or the user named. They go
  into the plan as is.

## Plan mode

The code does not exist yet. Plan from the spec and the repo as it is.

### 1. Define success

From the spec, list the observable outcomes: what a user or a downstream
system sees when the change works. One line each. Add the failure case the
spec implies (bad input, missing data) when there is one.

### 2. Find the harness

Look before you build. Search the repo for what already runs it: Makefile
targets, `docker-compose` files, live drivers, end-to-end or integration
suites, seed scripts, dev servers, and the run instructions in `README` or
`docs/`.

Then pick, per outcome, the highest rung that can run:

1. The real services in containers, driven through the real entrypoint
   (HTTP endpoint, worker task, CLI, UI through a live driver), with mocked
   or seeded data.
2. The real entrypoint in one process, with external systems stubbed at the
   network edge.
3. An integration test across the module boundaries the change touches.

Below rung 3 is not evidence. On a lower rung, say why the higher ones
cannot run.

Probe what could block the run, read-only: is Docker up, does the compose
file exist, is a needed secret or seed missing. Do not start services.

### 3. Write the plan

Write it to the QA plan path:

```markdown
# QA plan: <feature>

Spec: <path or ticket>

## Checks

### 1. <outcome, one line>

- **Rung:** <1 | 2 | 3> — <the harness>
- **Steps:** <setup, data, the exact command or action>
- **Pass when:** <the value or state that proves it; the broken code would
  not produce it>

<!-- repeat per outcome, failure cases included -->

## Prerequisites

<what must be up or present: containers, seeds, env vars. Mark anything
missing today.>

## Gaps

<outcomes no rung can prove, and why. "None" when none.>
```

Report the path, the number of checks, and any blockers or gaps.

## Run mode

Follow the QA plan. It was approved; do not drop or weaken a check.

### 1. Run and observe

Run each check. Each must be able to fail: assert on the plan's
**Pass when**. Capture raw evidence: the command, its exit code, log lines,
HTTP responses, database rows, screenshots.

Blocked (Docker down, missing secret) → try the next rung down, and say so.
A step that does not fit the code as built → adapt the step, keep the
**Pass when**, and say what you changed. Never report a check as passing
without evidence.

### 2. Report

**Verdict:** **works**, **does not work**, or **unproven**. **works** only
when every check passed with evidence.

Per check:

- The outcome.
- How you checked it: the rung and the command, and any change from the plan.
- The evidence: short, quoted output.
- Pass or fail.

Then:

- **Harness:** the exact steps to re-run your checks.
- **Gaps:** checks you could not prove, and why.

## Boundaries

- Do not edit product code. Fix nothing. A failure is a finding.
- Put scratch files (scripts, fixtures, compose overrides) in a temp
  directory outside the repo. Leave the repo's diff as you found it.
- Mocked or seeded data only. Never touch production, shared environments,
  real credentials, or customer data.
- Stop every container and process you started.
