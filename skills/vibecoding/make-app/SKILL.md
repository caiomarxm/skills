---
name: make-app
description: Take an app idea to a working app, step by step, for people who don't code. Sets up the project, interviews the user into a full design, splits it into parts, prepares the build, then builds and checks one feature at a time. Use when the user has an idea for an app, site or tool, wants to make or build an app, or asks for any change, fix or new feature in an app this flow created (its AGENTS.md says to use /make-app). Not for coding work in a codebase this flow did not create.
---

# Make an app

You take a person who may not code from an idea to a working app. This skill is the way in: it runs the step skills for them with the Skill tool, so they never need to know the step names. They may also call a step directly (`/build-feature add dark mode`); each step checks that the earlier ones are done.

When a step ends and the next one starts, mention its name once ("next time you can also type /build-feature to go straight here").

## Talking to the user

- Use the user's language and everyday words. Say "parts of your app", not "bounded contexts"; "checks", not "tests". If a technical word can't be avoided, explain it in one line.
- Before installing anything or doing anything on the internet for them, say what and why in one line, and wait for a yes.
- Report in two or three sentences. Never paste raw command output; say what it means.

## Find where the project is

Check these in order. Run the step of the first row that matches.

| Check | Step |
|---|---|
| The folder holds an existing codebase this flow didn't create (source or package files, no `docs/DESIGN.md` or `docs/DESIGN-DRAFT.md`) | Stop. Say this flow only starts new apps for now. |
| No `.git/`, `git` or `bd` not installed on this computer, or `bd ready` fails | `set-up-repo` |
| `docs/DESIGN-DRAFT.md` exists, or no `docs/DESIGN.md` | `write-spec` (it resumes the draft if there is one) |
| `docs/DESIGN.md` has no `<!-- make-app:modules -->` marker | `find-modules` |
| `docs/DESIGN.md` has no `<!-- make-app:how-built -->` marker | `prepare-to-build` |
| Otherwise | `build-feature` |

Find sections by these markers, never by heading text: headings are in the user's language.

## Run the steps

1. Tell the user in one line what happens now, in plain words:
   - `set-up-repo`: "getting your project folder ready"
   - `write-spec`: "working out exactly what your app should do"
   - `find-modules`: "splitting your app into parts"
   - `prepare-to-build`: "choosing how to build it"
   - `build-feature`: "building the next feature"
2. Run the step. Pass on what the user said (their idea, or "add dark mode").
3. When a step from `set-up-repo` to `prepare-to-build` ends, check again and go on to the next step, unless the user wants to stop for now. When `build-feature` ends, wait for the user's next request.

Each step writes its marker (or deletes the draft) as its very last action, so a step cut off halfway is picked up again on the next run.

If the user asks for something a later step does ("just build it"), say in one sentence why the current step comes first, then carry on with it. If they ask to set up GitHub, run `set-up-repo`.

If the user asks to update these skills, follow "Update" in https://github.com/caiomarxm/skills/blob/main/skills/vibecoding/README.md.
