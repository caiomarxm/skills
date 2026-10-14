---
name: plain-english
description: Rewrite dense assistant text, pasted jargon, or a Markdown file into Caio's voice — short everyday words, BLUF, just enough context. Use when the user says plain english, claudish, tldr this, say that simpler, rewrite that, 5y, caveman, or asks to un-jargon a message or doc.
---

# Plain English rewrite

Un-jargon something that already exists. Write it the way Caio likes to read: day-to-day words, Churchill-brief, bottom line first, one-line refresh when a concept shows up. He does not have the code in his head. Do not change facts. Do not add a second LLM or scripts.

## Target (pick one)

1. **Last assistant message** — default if they say "that", "last reply", or nothing specific
2. **Pasted / quoted blob** — if they included the text
3. **A file** — only if they named a path

If the target is unclear, ask once.

## Style (pick one)

| Trigger | Style | How |
| --- | --- | --- |
| _(default)_ | plain | His voice. BLUF. Short sentences. Everyday words. Keep enough context that the proposal still makes sense. Refresh named concepts in one line |
| tldr / summary | tldr | Half the length or less. Lead with the bottom line. Keep decisions, numbers, paths. Drop hedges and side notes. Omit code fences (original is in the chat/file) |
| 5y / like I'm five | 5y | Very simple words, short sentences, friendly. Simple comparisons for hard ideas |
| caveman | caveman | Blunt, no articles, present tense. Grammar can be dumb; facts cannot |

Keep technical terms, commands, identifiers, and paths in their original form. Leave fenced code unchanged (except tldr, which drops fences). Write in the **same language** as the source, unless they named another.

Output **only the rewrite**. No preamble, no "here's a simpler version", no labels. It should read like a person talking, not a summary deck.

## Files

Default: write `NAME.plain.md` next to `NAME.md`. Keep YAML frontmatter verbatim.

Overwrite the original only if they say overwrite / in place.

Skip files that are already mostly plain, or whose prose (code stripped) is tiny.

## Don't

- Invent facts
- Answer the original question again
- Strip the context that makes the ask or proposal understandable
- Append original + rewrite unless they ask to see both

## This length

Keep the Q / label. Cut the lecture. One reason, then the ask.

**Before**

```
Q1: which Session end reasons make a Search retry-eligible?

My recommendation: error only.

Two reasons.

The classifier is pure over the job aggregate, and at the moment it runs the only failure evidence in existence is ObservedRaidenSessionEndReason — completed | cancelled | error. The richer SearchFailureReason (SOURCE_TIMEOUT vs MAPPING_FAILED and friends) is established during finalization, from what Raiden reports. So G-D22's "1 retry, transient only" cannot be implemented here without first plumbing a failure category into the Session-end observation — that's a change to the extension-to-Maestro contract, not a classifier tweak. Your own CONTEXT.md already warns that the end reason is "sequencing evidence, not an authoritative Search outcome," so leaning on it for a transient/deterministic judgement would contradict the glossary.

And I'd leave cancelled out: an operator ending their own Session isn't a failure, and auto-restarting it fights the person who just stopped it.

So: error only, or do you want cancelled retried as well?
```

**After**

```
Q1: which Session end reasons make a Search retry-eligible?

Retry only on `error`.

At that point all we know is `completed`, `cancelled`, or `error`. The detailed reasons come later, so we can't tell "try again" from "never" yet.

`cancelled` means someone stopped it on purpose. Leave it alone.

`error` only — ok?
```
