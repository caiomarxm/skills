---
name: weekly-status-update
description: Generate a Slack-style weekly status update for an engineering epic, combining merged work (from git), in-flight tickets (from Jira when available), and upcoming milestones into a BLUF, product-centered summary. Use when the user asks for a weekly update, status update, epic update, progress report, or asks to draft a Slack post summarizing the week's shipped work.
---

# Weekly Status Update

Produce a concise, product-centered Slack post that summarizes an epic’s progress for the week.

## Workflow

1. **Pull merged work from git** — in the repo the user is working in:

   ```bash
   git log --since="<date>" --until="<date>" --pretty=format:"%h|%ci|%an|%s" --all
   git log --since="<date>" --until="<date>" --merges --pretty=format:"%h|%ci|%s"
   ```

   Use the date range the user gives (e.g. "April 25 to April 30"). If none given, default to the last 7 days. Do **not** run `git fetch`.

2. **Pull Jira tickets when the user mentions tickets, status, or "what we worked on"** — if an Atlassian MCP is available, query for tickets the user resolved, transitioned, or created in the window:

   ```text
   assignee = currentUser()
   AND (resolved >= '<from>'
        OR (status changed AFTER '<from>')
        OR (created >= '<from>'))
   ORDER BY updated DESC
   ```

   Categorize results into: **Done** (resolutiondate in window), **In flight** (status In Progress / Code review, updated in window), **Planned** (created in window, status Backlog / To Do — usually epic-breakdown work).

3. **Group changes by product theme, not by MR or ticket.** Multiple MRs/tickets that ship one user-visible capability MUST be unified into a single line in _What did we do this week?_ Exclude items resolved on/before the user’s cutoff date.

4. **Ask for the things git/Jira can’t tell you** (use `AskQuestion` when available, otherwise inline). Skip any the user already provided:

   - Initiative / epic name for the title line (if multiple are active)
   - _Goal_ framing: yearly vs quarterly outcomes (if they use that structure)
   - Upcoming milestones (dates + what ships) — don’t invent these
   - Risks, blockers, mitigations, and SME / dependency watch items
   - Whether last week’s milestones were hit (so the recap can acknowledge follow-through or deferrals)

5. **Draft using the template below**, then output as a single fenced code block so the user can copy-paste into Slack.

6. **Self-check** before returning:

   - _Status summary_ is a tight PM-readable paragraph (not a bullet list).
   - _What did we do this week?_ lines are outcomes, not implementation detail (no module names, file paths, framework names, lint/build jargon).
   - _Risks, Blockers & Mitigations_ matches the _Status_ color and names real mitigations where possible.
   - Themed items are unified (no duplicate lines for the same capability).
   - Frame deferrals as deliberate trades when they appear in narrative or risks.
   - Post is scannable: short paragraphs, no wall of text; prefer a handful of strong lines per section over long lists.

## Output Template

Slack formatting: use `*asterisks*` for **bold** labels and `_underscores_` for _italic_ emphasis inside sentences (e.g. deadlines, dependency names, initiative codenames). Apply both where they improve scanability; don’t bold entire paragraphs.

```
*<Initiative / epic name> — Weekly Update | <Month Day, Year>*

*Goal*: <One line, or two lines when the audience expects horizon split. When splitting, use bold sublabels and optional italic for emphasis, e.g.>
*YEARLY*: <Annual / north-star outcome.>
*QUARTERLY*: <Near-term outcome; scope, decisions, or execution readiness — so _who_ knows _what_ by _when_.>

*Status*: <status emoji> <green | yellow | red>
*Status summary*: <Single short paragraph: charter/progress headline, key dates, main risk + mitigation owner if any.>

*What did we do this week?*

- :white_check_mark: <Done outcome — past tense, product-centered.>
- :white_check_mark: <Done outcome.>
- :in-progress-icon: <In flight / scheduled — what happens next and why it matters.>
- :white_check_mark: <Optional: unify multiple MRs/tickets into one line if same capability.>


*Risks, Blockers & Mitigations*
- <Risk or theme — plain lines or light bullets; each should imply or state mitigation when known.>
- <Another risk / blocker.>
- <Optional: SME PTO, CI/CD, auth variance across tools, cross-team dependencies — framed as impact, not tech trivia.>


*Upcoming milestones*
:date: <MMM DD> — <what ships or what decision lands> (<dependency, owner, or ticket ID, optional>)
:date: <MMM DD> — <...>
```

### Section behavior (locked)

- **Title line**: `<Initiative / epic name> — Weekly Update | <Date>`. No leading dot or emoji on the title itself.
- **_Goal_**: Epic-level outcomes, not this week’s task list. Use _YEARLY_ / _QUARTERLY_ bold sublabels only when the user (or context) uses that cadence; otherwise one bold-labeled paragraph is fine. Use `_italic_` inside goal text for emphasis (dates, names, “migration vs deprecation”, etc.) sparingly.
- **_Status_**: Status emoji + word (`green`, `yellow`, or `red`) on the same line. Accept common workspace variants, e.g. `:large_green_circle:` / `:green:`, `:large_yellow_circle:` / `:yellow_circle:`, `:red_circle:` / `:red:` — pick one style per post and stay consistent with the thread’s convention.
- **_Status summary_**: **One narrative paragraph** after the bold label (not a bullet list). This is the BLUF; everything below expands it.
- **_What did we do this week?_**: Blank line after the bold section header, then lines prefixed with status emojis (e.g. `:white_check_mark:` done, `:in-progress-icon:` or your org’s in-progress emoji for active / scheduled work). Past tense for completed work; forward-looking is OK for the in-progress line.
- **_Risks, Blockers & Mitigations_**: Blank line after the header. Plain sentences or short `-` bullets; must be PM-legible. Tie severity to the _Status_ color.
- **_Upcoming milestones_**: Renamed from “Next milestones”; same `:date:` line pattern as before.
- **No `Author:` / `Epic:` footer** unless the user explicitly asks for one.
- **Ticket IDs** — optional; include only when they materially help. Don’t pad with IDs the audience won’t open.

## Writing Rules

- **BLUF**: _Status summary_ + first _What did we do_ lines should stand alone for a PM skimming on mobile.
- **Unify themes**: one emoji-line per capability shipped, not one per MR.
- **Exclude pure refactors** unless they unlock user value — then frame the value, not the tech.
- **Frame deferrals as trades** when they appear: “Deferred X to prioritize Y — Y is higher leverage.”
- **Don’t invent milestones or risks.** If unknown, use `[TODO: …]` in the draft and flag it in the reply.

## Example

Input: user asks for a weekly update for “Internal Admin Last Mile,” May 8 2026 window; charter shipped; SMEs being engaged for May 15 estimates; Overseer unblocked after auth docs; risk is SME PTO; mitigating with Dmitry.

Output:

```
*Internal Admin Last Mile — Weekly Update | May 8, 2026*

*Goal*: *YEARLY*: Consolidate Checkr’s internal admin surface onto the existing internal-dashboard platform. *QUARTERLY*: Complete the Overseer migration; decide migration vs. deprecation for the remaining legacy tools; and define scope, effort, and risks for the migration set — so execution can start in Q3.
*Status*: :large_green_circle: green
*Status summary*: Charter and proposal published; SMEs engaged for migrate-vs-deprecate estimates due _May 15_. Overseer migration unblocked this week. Main risk: SME PTO may pressure the _May 15_ deadline — managing with _Dmitry_.

*What did we do this week?*

- :white_check_mark: Project charter and proposal documents approved and published.
- :white_check_mark: Meeting with _Dmitry_ and _Michael_ helped identify SMEs across the tool inventory; we’re now engaging them for effort estimates, risks, and scope.
- :in-progress-icon: Meeting next week with DRIs of adjacent projects whose work overlaps with ours (e.g. _Circuit Breaker_) to align on scope and dependencies.
- :white_check_mark: Overseer migration back on track — auth roles/permissions were undocumented and blocked progress; resolved this week with help from _Oriah_, and the process is now documented for future migrations.


*Risks, Blockers & Mitigations*
- Existing tools have diverse authentication and authorization mechanisms; _Auth0_ integration approach needs evaluation per tool.
- CI/CD pipeline takes over an hour to deploy, which will slow parallel workstreams — determining the best approach to mitigate.
- Some SMEs are on vacation, which may push the estimation deadline. PTO conflicts identified; we believe _May 15_ holds — confirming with _Dmitry_.


*Upcoming milestones*
:date: May 15 — Initial effort estimates for identified tools
```
