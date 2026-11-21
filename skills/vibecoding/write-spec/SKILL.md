---
name: write-spec
description: Interview the user about their app and write every decision down, then compile docs/DESIGN.md, for an app made with /make-app. Use when the user wants to work out or rethink what their app should do. /make-app runs it as step 2.
---

# Write the spec

Turn the user's idea into `docs/DESIGN.md`: one design doc that holds every decision from the interview, for the whole vision, in plain words.

The draft (`docs/DESIGN-DRAFT.md`) is the working file. The design doc (`docs/DESIGN.md`) is the result. Losing a decision between the two is the worst failure of this step.

If the user calls this step directly:
- Setup isn't done (see the table in `make-app`): say so in one line and run `make-app` instead.
- `docs/DESIGN.md` exists and there is no draft: interview only about what the user wants to change, write the decisions straight into the right sections of `docs/DESIGN.md` and the glossary, and commit. Don't recompile. If a change no longer fits the modules, say so and offer to rethink the split.

## Workflow

1. **Start or resume.**
   - No draft: create it from the draft template below, with the user's idea word for word under "The idea".
   - Draft exists: read it, tell the user in one line where you left off, and carry on from "Still open".
   - Draft and `docs/DESIGN.md` both exist: the compile was cut off. Go to step 5.
2. **Interview.** Run `grilling` and `domain-modeling` with the Skill tool and follow both, plus the rules under "Interview rules".
3. **Agree on the first version.** When the frontier is empty and every concern is handled, propose the smallest set of features that is useful on its own. Log the user's answer as a decision.
4. **Compile.** Think hard, then write `docs/DESIGN.md` with the design doc sections below. Every decision not marked "Replaced" must land in a section. No decision IDs, no tech.
5. **Check.** Start a fresh subagent with none of this conversation and this prompt:

   > Read `docs/DESIGN-DRAFT.md` and `docs/DESIGN.md`. List every decision (by ID) that is missing from DESIGN.md, has a changed meaning there, or is marked "Replaced" but appears in DESIGN.md as current. Reply "clean" if there are none.

   Fix everything it lists, then run a fresh check again. Repeat until it replies "clean". If it is still not clean after three rounds, tell the user in plain words which decisions you can't place, and ask.
6. **Finish.** Tell the user in two or three sentences what the design says and link `docs/DESIGN.md`; say reading it is optional. Delete the draft. Commit "Design complete" and run `git push` if there is a remote.

## Interview rules

- **Size the app first.** The first question settles who uses the app, how many people, and whether it's personal or shared. The answer decides which items in `CONCERNS.md` apply.
- **Concerns.** Before the second question, read [CONCERNS.md](./CONCERNS.md). Each item is either asked about or written under "Concerns" in the draft as "doesn't apply" with a one-line reason. Don't ask about items that clearly don't apply.
- **Write before you ask.** After every answer, write the decision into the draft with the next ID (D1, D2…), then ask the next question. When a decision replaces an older one, mark the old one "Replaced by Dn" and keep it. Keep "Still open" current.
- **Terms.** When a word is settled, add it to the root `GLOSSARY.md` straight away, in the format of `domain-modeling`. Glossary entries are in English; if the user speaks another language, add their word: "**Booking** (*Reserva*): …".
- **No code yet.** The code checks and ADRs in `domain-modeling` don't apply in this step.
- **Facts are yours.** Prices, limits, licenses, laws, existing services: send a subagent to find out and write the answer under "Facts". Never ask the user for a fact.
- **The whole vision.** Capture every feature the user wants, even far-off ones. The parts of the app are drawn from the whole vision.
- **"You decide."** If the user says so, pick, log it with "(agent's pick)" and tell them in one line.
- **Save as you go.** Commit the draft and glossary after each topic, with the message "Spec: <topic>".

## Draft template

```markdown
# <App name>: design draft

## The idea
<the user's words>

## Decisions
- **D1 — <title>.** <decision>

## Facts

## Concerns
- <item>: asked (D4) | doesn't apply (<reason>)

## Still open
```

## Design doc sections

Written in the user's language and everyday words. Headings may be translated.

1. **In one paragraph**: what the app is and who it's for.
2. **People**: each kind of user and what they can do.
3. **What it does**: user stories grouped by area. "As a <person>, I want <thing>, so that <reason>."
4. **Rules**: the business rules ("a boat can't be booked twice for the same day").
5. **What it keeps**: the information the app stores.
6. **When things go wrong**: mistakes, lost data, misuse.
7. **First version / Later**: which features are built first; the rest.
8. **Not doing**: what is out of scope.

`find-modules` adds section 9 and `prepare-to-build` adds section 10 later.

## Done when

- `docs/DESIGN.md` exists, the last check said "clean", and the draft is deleted.
- Every term from the interview is in `GLOSSARY.md`.
