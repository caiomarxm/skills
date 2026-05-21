---
name: grill-with-docs
description: >-
  Grilling session that challenges your plan against the domain model, sharpens
  terminology, records decisions in a feature-plan file, and flags CONTEXT.md /
  ADR follow-ups. Use when stress-testing a plan with documentation awareness.
disable-model-invocation: true
---

# Grill with docs

<what-to-do>

**Interview me relentlessly about every aspect of this plan until we reach a shared understanding.**
Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

- **CONTEXT-MAP:** when scope spans multiple modules or features, open the repo's context map if present (e.g. `extension/src/CONTEXT-MAP.md` in Crawling UI — refresh with `npm run context-map` from `extension/` if the map may be stale).
- **CONTEXT.md:** glob `**/CONTEXT.md` under the user's stated scope (or next to paths on an attached **Code map** / recon). Skim **Vocabulary**, **Invariants**, **Owns** (bus, flags, state) before deep-reading implementation files. If a slice has no `CONTEXT.md`, say so and lean on code plus architecture docs — do not invent files.
- **Shape / caps:** use [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) so any edit you propose matches section order and limits.
- **ADRs / decision logs:** if the repo has ADRs or `docs/**` decision notes, open only those that overlap the topic — skip entirely when none exist.

NOTE: The user should provide either an existing feature-plan markdown file (`docs/feature-plans/EDATA-XXX-<slug>.md`) or a Jira ticket. If they provide a file, append a `## Grilling Session` section and log every question, recommendation, answer, and decision there as the session progresses. If they provide a Jira ticket, read it with MCP to understand the work, bootstrap `docs/feature-plans/EDATA-XXX-<slug>.md` from the ticket content, add `## Grilling Session` at the bottom, then start the interview and log every question, recommendation, answer, and decision there.

</what-to-do>

<supporting-info>

## Domain awareness

During codebase exploration, also look for existing documentation.

### File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Read the repo's `CONTEXT-MAP.md` (or equivalent) to find bounded contexts relevant to the plan before opening individual `CONTEXT.md` files.

If the user names a decision file, use it. Otherwise look for an attached or relevant `docs/feature-plans/<KEY>-*.md`; if none exists, propose creating one in `docs/feature-plans/`.

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first implemented term, relationship, flow, or invariant is resolved and should be documented. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Record accepted decisions

Register answers in the feature-plan / decision file, but only the decisions you make together. Do not append every question, rejected path, transcript fragment, or unresolved option. Keep each entry compact: decision, rationale, notable rejected alternative if it matters, and any follow-up doc/code action. If an accepted decision changes an earlier entry, update the existing entry instead of appending a contradiction.

### Flag CONTEXT.md follow-ups

Do not edit `CONTEXT.md` during the grilling session. When a decision implies that implemented language, relationships, flows, or invariants should change, record that implication in the feature-plan / decision file as a follow-up context update.

Use [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) to describe the expected shape of that follow-up, but leave the actual `CONTEXT.md` patch to a separate documentation update. `CONTEXT.md` is a compact bounded-context snapshot: responsibility, language, relationships, flows, and invariants; it is not a future spec, scratch pad, or repository for planning decisions.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR and keep the decision in the feature-plan file. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

</supporting-info>
