# CONTEXT.md Format

`CONTEXT.md` is a compact bounded-context snapshot for agents and humans: the context's responsibility, ubiquitous language, relationships, flows, and invariants. It describes what is implemented today, not future plans or an implementation manual.

## Location

- Module context: `<module-root>/CONTEXT.md`.
- Module feature context: `<feature-root>/CONTEXT.md`.
- Content-script feature context: `entrypoints/content/features/<F>/CONTEXT.md`.
- If a repo uses root-level contexts, `CONTEXT-MAP.md` lists each context and how they relate.

## Template

```md
# <Context Name>

<One or two sentences: what bounded context this is, what responsibility it owns, and why it exists.>

## Language

- **<Term>** — <one-sentence definition.> _Avoid:_ <misleading aliases>.
- **<Term>** — <one-sentence definition.>

## Relationships

- **<Term A>** owns many **<Term B>**.
- **<Context A>** emits `<event>`; **<Context B>** consumes it to <effect>.
- **<Context A>** depends on **<Context B>** for <specific capability>.

## Flows

- **<Flow name>**: `<trigger>` → <one-sentence outcome using this context's language>.

## Invariants

- <Rule that must remain true for this context to be valid.>
```

## Rules

- **Keep it semantic.** `Language` defines nouns, `Relationships` defines boundaries, `Flows` defines behavior, and `Invariants` defines rules.
- **Be opinionated.** Pick one term for each concept and list misleading aliases in `_Avoid:_`.
- **Keep definitions tight.** One sentence max; define what the concept is, not what it does.
- **Use DDD language.** Bold context terms; use backticks only for code symbols, events, messages, stores, and type names.
- **Consolidate dependencies into relationships.** State ownership, storage ownership, bus events, messaging, and cross-context imports all belong in `Relationships` when they define a boundary.
- **Only include context-specific terms.** General programming concepts do not belong unless this context gives them special meaning.
- **Omit empty sections except the summary.** Do not add placeholders like "none".
- **No implementation manual.** Avoid internal file paths, function inventories, TODOs, changelog narration, or duplicated export lists.

## Caps

- Target ≤60 lines; hard cap ≤80.
- `Language`: ≤7 entries.
- `Relationships`: ≤7 bullets.
- `Flows`: ≤5 bullets.
- `Invariants`: ≤5 bullets.

## When to update

Update the context in the same change when implemented language, relationships, events/messages, state/storage ownership, major flows, or invariants change.
