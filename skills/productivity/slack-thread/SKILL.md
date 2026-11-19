---
name: slack-thread
description: >-
  Draft Slack threads in Caio's style and save them to a local Markdown file.
  Use when the user asks to draft or write a Slack thread, continue an existing
  thread, post an update to a channel, or turn research into a Slack discussion.
  Searches Slack for an existing thread first. Never posts or saves a Slack draft.
---

# Slack thread

Write the thread Caio would post: bottom line first, short everyday words, and
a clear decision or question. Keep facts, names, numbers, links, and identifiers
exact. Write in the source language unless the user asks for another.

## Hard rules

- Never post, schedule, or save a draft in Slack. Write a local Markdown file;
  Caio edits and posts it.
- Before drafting, search Slack for the same project, ticket, place, or decision.
  Search public channels first. Include private channels when the target or
  supplied context is private.
- Read the full relevant thread, not only the search result.
- If the same discussion exists, draft a reply there. Do not create a new parent.
- Do not invent facts, decisions, owners, mentions, links, or dates. Mark a
  missing mention as `@owner` rather than guessing.
- No bold section headers. Use short plain headers such as `What changed`,
  `Where we are`, `The tech challenge`, `Questions`, or `Open questions`.

## Workflow

1. Name the one decision, answer, or ask the thread needs.
2. Search Slack with 2–3 narrow queries using the strongest identifiers:
   project name, ticket, county, system, or exact phrase.
3. Choose:
   - Existing discussion found: draft a reply and include its thread link.
   - No matching discussion: draft a new parent plus replies.
4. Save the draft:
   - Use the path the user gives.
   - Otherwise write `slack-thread-<short-topic>.md` beside the source document,
     or in the current project root when there is no source file.
5. Report the file path and whether it is a new thread or an existing-thread
   reply. Do not paste the whole draft into chat unless asked.

## New thread format

**Parent**

`:thread:` plus `:warning:` when the topic carries material risk, then:

```text
:thread::warning: <Topic>: <direct question or conclusion> – @owner1 @owner2

(<one line: why this matters>)
```

**Replies, in order**

1. `tl;dr:` in 2–3 sentences. Give the answer, proposal, or ask first.
2. Context under short headers. Use short bullets for facts, numbers, and links.
   Use `:warning:` for the one fact people must not miss.
3. `Questions` or `Open questions`. Each item must be a direct question someone
   can answer.
4. Optional closer:
   `Feel free to tag along anyone that helps us decide the direction!`
   Add `( + @people for viz )` only when useful.

Split long content into replies. One reply should do one job. Remove repeated
context and anything that does not help answer the thread's question.

## Existing-thread reply format

Start by saying what changed since the earlier discussion. Then use:

```text
:thread: Picking this back up for <project>: <direct question> – @owners

tl;dr: <what changed, the proposed direction, and the ask>

<short context header>
- <new fact>
- <new fact>

Questions
1. <direct question>
2. <direct question>
```

Include whether the reply should also be sent to the channel only when the user
needs broad visibility.

## File wrapper

```markdown
# Draft: <channel or topic>

Status: draft. Not posted. Caio edits and posts.

Where: <new parent in #channel, or reply in existing thread>
Thread: <existing thread URL, when applicable>

---

<message blocks>
```

## Examples

### New parent plus replies

```text
Parent

:thread::warning: MI Wayne: What Happens Now That the Court Site Changed? – @jamie @jazmin.bell

(Missing data after website change could stop us from going live)

Reply 1

tl;dr: IHR is disabled in MI. The new site shows only the past 7 years of
criminal cases and hides several case outcomes. We are waiting on the MI
Supreme Court before deciding next steps.

Reply 2

What changed

- The new MOCCS site is live, with a statewide search form.
- Wayne County now shows only criminal cases from the past 7 years.
- :warning: MOCCS hides dismissed, withdrawn, not guilty, and other outcomes.

Reply 3

Open questions

1. With the hidden case types, is the PAT still viable?
2. Do we keep working on the Wayne scraper, or pause for the Supreme Court?
```

### Reply in an existing thread

```text
:thread: Picking this back up for scrapy-hub (EDATA-2237): OK to use one
single-use Ramp card per payment? – @Mariah Arnold @Joel Shure

tl;dr: Same project, one change to the approved design. Instead of storing one
long-lived card, scrapy-hub would create a capped card for each payment and
close it right after. Is that OK?

What changes

- Vault holds a Ramp API credential, not a card.
- The card number lives only in memory. It is never logged or stored.

Questions

1. Is the API credential OK in a separate Vault mount?
2. Can we test this flow with the existing Ramp test fund?
```

## Final check

- The first line says why people should care.
- The `tl;dr:` contains the answer or ask, not background.
- The thread asks for one decision.
- Every question has a likely owner and can be answered directly.
- Facts and links came from the supplied material or Slack.
- The draft is local and nothing was posted to Slack.
