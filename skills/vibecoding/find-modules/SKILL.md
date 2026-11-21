---
name: find-modules
description: Split the app into parts (modules), agree them with the user in plain words, and record them in docs/DESIGN.md and the glossaries, for an app made with /make-app. Use when the user wants to see or change how their app is split into parts. /make-app runs it as step 3.
---

# Find the modules

Split the app into parts. Each part has one job, keeps its own information, and offers a small front door to the other parts. Later each part becomes one deep module: a lot of work hidden behind a simple interface.

With the user, say "parts of your app", never "bounded context" or "domain".

If the user calls this step directly:
- There is no `docs/DESIGN.md` yet: say so in one line and run `make-app` instead.
- Section 9 is already marked done: start from the current split and change only what the user asks. Update section 9, the glossaries, and any module `AGENTS.md` files the change affects. Keep the marker.

## Workflow

1. **Find the parts.** Read `docs/DESIGN.md` and `GLOSSARY.md`, then think hard. Use the whole vision, including "Later" features.
   - Information and rules that change together belong in one part. Each piece of information has exactly one owner.
   - If a word means different things to different people ("booking" for a guest vs. an owner), there is probably a border there.
   - If a part's front door would be as big as its inside, merge it into another part.
   - Use as few parts as the app needs. A personal single-file app may have 2–3. Never invent parts to look thorough.
2. **Show them.** One short card per part, then a small map of which part needs which:

   > **Bookings**: handles who reserved which boat, and when.
   > Does: request a booking, accept or decline, cancel.
   > Keeps: bookings.
   > Needs: Boats (to check the boat exists), Payments (to charge).

   ```
   Bookings → Boats     (checks the boat exists)
   Bookings → Payments  (charges the guest)
   ```
3. **Test the split.** Run `domain-modeling` with the Skill tool. There is no code yet, so its code checks and ADRs don't apply, and module folders are `modules/<name>/`, not the `src/` layout it shows. Put concrete cases to the user that cross borders ("a guest cancels after paying: which part gives the refund?"). Change the split from their answers until every case has a clear owner and the user agrees. If an answer adds or changes a rule, update that section of `docs/DESIGN.md` right away.
4. **Record.** Add section 9 to `docs/DESIGN.md`, in the user's language. For each part: name, job, features (pointing to the user stories in section 3, each tagged first version or later), the information it owns, what it offers other parts, and what it needs from them. End with the map.
5. **Split the glossary.** Folder names are English kebab-case: `modules/<name>/`.
   - One part, or no term differs between parts: keep the single root `GLOSSARY.md`.
   - Otherwise: give each part a `modules/<name>/GLOSSARY.md` with the terms it uses. A term that means different things in two parts gets its own definition in each. Write a root `GLOSSARY-MAP.md` listing each part and how they relate (format in `domain-modeling`), and delete the root `GLOSSARY.md`.
6. **Mark it done.** Add the line `<!-- make-app:modules -->` just above the section 9 heading. Do this last: it tells `make-app` this step is finished.
7. **Finish.** Commit "Modules", run `git push` if there is a remote, and tell the user in two sentences what the parts are.

If section 9 exists without the marker, this step was cut off: check which of steps 4–5 are done and carry on from there.

## Done when

- `docs/DESIGN.md` has the `<!-- make-app:modules -->` marker and the user agreed to the split.
- Every term is in the glossary of each part that uses it.
