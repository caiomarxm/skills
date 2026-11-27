---
name: validate
description: >-
  Use this when the user asks you to prove a change works by running an approved QA plan
---

# Validate

You prove that the change works. Proof is what you observe when you run the
real thing. Reading the code is not proof. Passing unit tests are not proof.

You run the approved plan. You do not write a new one. `qa-plan` writes it.

## Input

- **Spec**: the desired outcome. A file, a ticket, or text. No spec → stop
  and ask.
- **QA plan path**: the approved plan to run. Missing, or no plan at that
  path → stop. Do not write one.
- **Change**: the fixed point, the uncommitted diff, or the files changed,
  to aim your checks.

## Run

Follow the QA plan. It was approved; do not drop or weaken a check.

The rungs, highest first:

1. The real services in containers, driven through the real entrypoint
   (HTTP endpoint, worker task, CLI, UI through a live driver), with mocked
   or seeded data.
2. The real entrypoint in one process, with external systems stubbed at the
   network edge.
3. An integration test across the module boundaries the change touches.

Below rung 3 is not evidence.

**CRITICAL**: You MUST validate as close to the production environment as
possible. This means a sandbox run if you can, or at least a local docker
setup similar to production.

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
- Do not rewrite the QA plan. A step that does not fit the code as built is
  noted in the report, not edited into the plan.
- Put scratch files (scripts, fixtures, compose overrides) in a temp
  directory outside the repo. Leave the repo's diff as you found it.
- Mocked or seeded data only. Never touch production, shared environments,
  real credentials, or customer data.
- Stop every container and process you started.
