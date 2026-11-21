---
name: build-feature
description: Build, change or fix one feature: build it, run the checks, show it to the user, and save it once they say it works. Use when the user asks to add, change or fix something in an app made with /make-app, or to build the next feature. /make-app runs it as step 5.
---

# Build a feature

Build one feature at a time. A feature is done only when every check passes and the user says it works.

If `docs/DESIGN.md` has no `<!-- make-app:how-built -->` marker yet, the earlier steps aren't done: say so in one line and run `make-app` instead.

## Workflow

1. **Pick the work.**
   - The user asked for something already in `docs/DESIGN.md`: find its task with `bd list`. If it's a "Later" feature with no task, create one the way `prepare-to-build` does, without `--parent`.
   - The user asked for something new: see "New ideas" first.
   - The user reported something broken: see "Fixes".
   - Otherwise: take the top of `bd ready` and say in one line what's next ("Next up: guests can request a booking"). If `bd ready` is empty, say what's done and ask what to build next. Stop there.

   Then `bd show <id>` and `bd update <id> --claim`.
2. **Build it.** Read the root `AGENTS.md`, the glossary (the root `GLOSSARY.md`, or the module glossaries listed in `GLOSSARY-MAP.md` for the modules the task touches), and section 10 of `docs/DESIGN.md`. If a tool from section 10 is missing on this computer, explain, ask, then install it.
   - Other modules are used only through their front door.
   - Add only the tools and setup this feature needs.
   - When a module first gets code, write `modules/<name>/AGENTS.md`: its job, its front door (what it offers, what it needs), the information it owns, where its checks live. Keep it short and update it when the front door changes.
3. **Check it.**
   - Write one check per example in the task's acceptance. Each check calls only the module's front door.
   - Run every check in the project. Fix until all pass.
   - Never change an existing check to make it pass. Change one only when the user changed the rule behind it, and tell them.
   - Open the app and click through the feature yourself.
4. **Show it.** Shape 1: open the HTML file in the user's browser. Otherwise: start the app on their computer and give them the link. Tell them the check result in one line ("all 14 checks pass"), then walk them through the acceptance examples: "try booking May 3 twice".
5. **Ask: "Does this work the way you wanted?"**
   - **No:** write down what's wrong in the task (`bd update <id> --append-notes "..."`), fix it, and go back to step 3.
   - **Yes:** this is their approval to save. `bd close <id> --reason "<one line>"`, commit with a plain message ("Guests can request a booking"), and back up (`git push`, then `bd dolt push`) if there is a remote. Then offer the next task from `bd ready`.

When every first-version task is closed, tell the user the first version is done and offer to pick the next feature from "Later".

## New ideas

1. Run `grilling` with the Skill tool, kept to this one feature.
2. Write the decisions into the right sections of `docs/DESIGN.md` and new terms into the right glossary.
3. If it doesn't fit the current modules, say so in plain words and agree a new split with the user (as in `find-modules`) before building. Update section 9 and the glossaries.
4. Ask whether it's for now or later. Now: create its task as `prepare-to-build` does. Later: leave it in "Later".

## Fixes

1. Reproduce the problem.
2. Turn the user's description into a plain example and add it to the task (create a bug task with `bd create "<problem>" -t bug -p 0` if there is none).
3. Write a check for that example, see it fail, then fix. Continue from step 3 of the workflow.

## When things go wrong

- A check fails and you can't see why: tell the user in plain words what's not working yet. Never show raw output, and never call the feature done.
- The design and the user's new request disagree: ask which is right, then update `docs/DESIGN.md`.
