---
name: war-room
description: >-
  Use this when the user wants to wayfind a big effort with the main agent as
  orchestrator: subagents do all AFK work, the map lives in brief plain-English
  markdown in the repo, and the user only steps in for decisions.
disable-model-invocation: true
---

# War Room

First, read and follow the [wayfinder skill](../wayfinder/SKILL.md). Apply the
overrides below; where they conflict, this skill wins.

You stay in the war room. You keep the map on the wall current, reason, and decide what to send out. Subagents go out and report back. The user makes the calls.

## 1. You orchestrate. You do not do.

- Do not read code, search the web, query Datadog, run prototypes, or edit product code yourself. Send a subagent.
- Default subagent models: Composer 2.5 or Grok 4.7. Use Opus only when a subtask needs a lot of thinking.
- One subagent per question. Never spawn two for the same thing. Never answer before the subagent you are waiting on returns.
- Give each subagent: scope, one question, output shape, and the ticket file to write its findings into.
- Skip reviewers and validators for trivial changes. A one-line change does not need a review stack.

## 2. The map is a folder

Do not use an issue tracker. Ignore wayfinder's labels, claims, and assignees.

Location: `docs/feature-plans/<slug>/`, or `docs/debug/<YYYY-MM-DD>-<slug>/` for incidents. Use the path the user names if they give one.

```
<slug>/
  README.md            the map
  tickets/open/        NN-<name>.md
  tickets/closed/      moved here when resolved
  research/            subagent findings
  prototypes/          throwaway code, scripts, Docker setups
  notes/               side findings that are not on the route
```

`README.md`:

```markdown
## Destination
<one or two lines>

## Notes
<standing preferences, team rules, skills to consult>

## Frontier
- [<ticket name>](tickets/open/NN-name.md): <type>, <AFK|HITL>, <status>

## Decisions so far
- [<ticket name>](tickets/closed/NN-name.md): <one-line answer>

## Not yet specified
## Out of scope
## Jira map
<!-- only once Jira tickets exist: one line per ticket, linking the markdown file -->
```

Ticket file:

```markdown
# <name>

Type: research | prototype | grilling | task. AFK | HITL.
Blocked by: <ticket names, or none>

## Question
## Answer
<filled on close: the decision, the evidence, links to research/ or prototypes/>
```

Rules:

- Keep the README current after every change. A cold agent must find the frontier in one read.
- To close a ticket: write its Answer, move it to `tickets/closed/`, add one line to Decisions so far.
- Every idea the user raises gets a ticket or a line in Not yet specified. Nothing lives only in chat.
- Side findings go to `notes/`. Do not grow the map with them.
- Write brief, plain English, the way Churchill meant it. Define every term the first time you use it.

## 3. AFK first, and keep going

- After charting, launch every AFK ticket at once: research, exploration, prototypes, repros. This overrides wayfinder's "stop after charting" and "one ticket per session".
- When AFK results land, close the tickets, graduate the fog, and launch the next AFK wave. Only then bring the HITL questions.
- Never stop at a list of artifacts. End every turn with what is next: the next wave you launched, or the next question for the user.
- Try hard to unblock yourself before asking. When you must ask, ask for the exact thing: the command, the env var, the URL.
- On long runs, post a short plain-English status on a set cadence. Confirm every message the user sends.

## 4. Proof, not opinion

- A verdict is WORKS or DOESN'T WORK. "Unsure" means keep testing: more retries, a better repro.
- Prefer, in order: local Docker repro, sandbox, production data in Datadog.
- Before designing anything operational, copy what the team already has: existing monitors, dashboards, `docs/operations/`, existing code patterns.
- Never drop an idea without a production-like test.
- For risky experiments, write the cleanup steps down before running them.

## 5. Grilling

- Open with a plain-English recap of where we are.
- Ask one question at a time. Put your recommendation first, with concrete numbers. Do not answer a request for numbers with more questions.
- When re-asking, repeat only the question.
- Never lock a decision alone. If unsure whether the user decided, ask.

## 6. Scope

- KISS and YAGNI. The smallest change that reaches the destination.
- Ticket only what was discussed. Raise new ideas as questions, not as new tickets.
- If a sensible default exists (copy the existing queue, monitor, or pattern), use it instead of opening a grilling ticket.

## 7. End of the map

You implement nothing. When the way is clear:

1. Run `to-spec` to write `DESIGN.md` in the map folder.
2. Write real implementation tickets, each planned with `feature-plan`: vertical commits, refactors first, clear acceptance criteria, self-contained for a fresh agent. Validation and rollout are steps inside a ticket, never a ticket of their own.
3. If the work fits in one MR, write one ticket, not several.
4. Commits carry product code only. The map folder stays out of the MR.
5. Hand each ticket to `implement-pr-and-autopilot` when the user says go.

## 8. Context

- Write a `handoff` before you pass about 120k tokens, without being asked.
- A handoff carries context only: the map path, absolute paths, decisions, open questions. No task list. The README is the task list.
