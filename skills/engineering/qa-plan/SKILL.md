---
name: qa-plan
description: >-
  Use this when the user asks you to write a QA plan from a spec before the code exists.
---

# QA plan

You write the plan that will prove the change works.

Proof is what someone will observe when they run the real thing. Reading
the code is not proof. Passing unit tests are not proof.

The code does not exist yet. Plan from the spec and the repo as it is.

## Input

- **Spec**: the desired outcome. A file, a ticket, or text. No spec → stop
  and ask.
- **QA plan path**: where to write the plan. Outside the repo, so it never
  lands in the diff. Not given → stop and ask.
- **How to validate** (optional): steps the spec or the user named. They go
  into the plan as is.

## 1. Define success

From the spec, list the observable outcomes: what a user or a downstream
system sees when the change works. One line each. Add the failure case the
spec implies (bad input, missing data) when there is one.

## 2. Find the harness

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

**CRITICAL**: The plan must validate as close to the production environment
as possible. A sandbox run if it can, or at least a local docker setup
similar to production.

Probe what could block the run, read-only: is Docker up, does the compose
file exist, is a needed secret or seed missing. Do not start services.

## 3. Write the plan

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

## Boundaries

- Do not edit product code. Do not start services. Do not run the checks.
- Put scratch files in a temp directory outside the repo. Leave the repo's
  diff as you found it.
- Mocked or seeded data only. Never touch production, shared environments,
  real credentials, or customer data.
