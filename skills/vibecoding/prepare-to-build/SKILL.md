---
name: prepare-to-build
description: Choose how the app is built and tested, write README.md and AGENTS.md, and turn the first version into tasks, for an app made with /make-app. Use when the user wants to choose or change how their app is built. /make-app runs it as step 4.
---

# Prepare to build

Decide how the app is built and tested, write the project's instructions, and turn the first version into tasks that each end in something the user can try.

If the user calls this step directly:
- The modules aren't done yet (no `<!-- make-app:modules -->` in `docs/DESIGN.md`): say so in one line and run `make-app` instead.
- This step is already marked done: ask what they want to change, and explain in plain words what the change costs before touching anything. Changing tools after features exist can mean rebuilding them.

## Workflow

1. **Agree the shape.** Read `docs/DESIGN.md`. Recommend one shape based on its People, numbers of users and devices, with one line on why, and let the user pick:
   1. **One file you open in your browser.** Only you use it, data stays on your computer, no hosting, no cost.
   2. **A website for you and a few people.** Shared data, simple login, a small monthly hosting cost.
   3. **A full web app for many users.** Accounts, a server, a database, real hosting.
   4. **A phone app.** Say honestly that it's harder, and that shape 2 or 3 working well on phones is often enough.
2. **Pick the tools.** You choose; the user doesn't need to. Few, well-known, free to start. Defaults:

   | Shape | Default |
   |---|---|
   | 1 | Plain HTML, CSS and JavaScript. Each module is its own JavaScript file in `modules/<name>/`. A small Node script with no packages bundles them into one HTML file in `dist/`. Checks run with `node --test`. Data in the browser's storage. |
   | 2 | A TypeScript web app (Vite) with a hosted service for login and data (e.g. Supabase, free tier). Checks with Vitest. |
   | 3 | TypeScript client and server, PostgreSQL. Checks with Vitest. A module that spans both splits its folder inside (`modules/<name>/client/`, `modules/<name>/server/`), never moves. |
   | 4 | Expo (React Native). Checks with Jest. |

   Use another tool when the design needs it, and say why. If the user names a tool they want, use it, and flag any real problem with it in one line.
3. **Install.** For each tool not yet on the computer (Node, say): explain in one line, wait for a yes, then install it (Windows `winget install OpenJS.NodeJS.LTS`, macOS `brew install node`).
4. **Write section 10.** Add it to `docs/DESIGN.md` in the user's language: the shape, each tool in one plain sentence, how the parts fit, how the checks work, how to open or run the app.
5. **Write the project files** (templates below): `README.md`, and the root `AGENTS.md`, which replaces the starter from install but keeps its routing rule. `CLAUDE.md` stays as the single line `@AGENTS.md`. Module `AGENTS.md` files come later, when a module first gets code.
6. **Create the tasks.** See "Tasks".
7. **Mark it done.** Add the line `<!-- make-app:how-built -->` just above the section 10 heading. Do this last: it tells `make-app` this step is finished.
8. **Finish.** Commit "Ready to build", back up (`git push`, then `bd dolt push`) if there is a remote, and tell the user what the first feature will be.

If section 10 exists without the marker, this step was cut off: check which of steps 3–6 are done (tools, files, tasks in `bd list`) and carry on from there.

## Tasks

Tasks are vertical: each one is a feature from start to finish (the module front doors and the screen), so every finished task is something the user can try. Never make a setup-only or scaffolding task. The first task is the smallest useful feature; it sets up only the tools, the check command and the bundling it needs, and later tasks add what they need.

1. `bd create "<First version, in the user's language>" -t epic -p 1`. Note the ID it prints.
2. For each first-version feature in section 7: `bd create "<feature>" -t task -p 1 --parent <epic-id> -l "<every module it touches>"`.
3. Fill each task: `bd update <id> --description "..." --design "..." --acceptance "..."`. For long text or quotes, pass `--description=-` and pipe the text in.
   - description: what it is, in the user's language, plus which user story in `docs/DESIGN.md` it comes from.
   - design: which module front doors it adds or changes.
   - acceptance: the checks, as plain examples from the design doc's rules and stories, in the user's language. "Ana books boat 1 for May 3. Bob tries the same day. Bob is told it's taken."
4. When a feature needs another one first: `bd dep add <later-task> <earlier-task>`.
5. Run `bd ready` and confirm the first task is at the top.

"Later" features get no tasks; they stay in `docs/DESIGN.md`.

## README.md template

```markdown
# <App name>

<Section 1 of the design doc.>

## Open it

<One or two steps.>

## Change it

Open Claude Code in this folder and say what you want.
```

In the user's language.

## AGENTS.md template

```markdown
# <App name>

## Start here
For any request about this app, use /make-app.

## The domain
<One line per module: name and job.>
Design: docs/DESIGN.md. Words: <GLOSSARY.md or GLOSSARY-MAP.md>.

## Building
- Each module lives in modules/<name>/. Other modules use it only through its front door, never its insides.
- Tasks are vertical: each ends in something the user can try.
- Tools: <from section 10>.

## Checks
- Checks call only a module's front door, and mirror the plain examples in the task's acceptance one to one.
- Run every check with `<command>` before calling anything done.
- Never change a check to make it pass. Change it only when the user changes the rule behind it, and tell them.

## Tasks
This project uses beads (`bd`): `bd ready`, `bd show <id>`, `bd update <id> --claim`, `bd close <id>`. No markdown to-do lists.
Back up with `git push`, then `bd dolt push`: git alone doesn't carry the tasks.

## Talking to the user
The user may not code. Use their language and everyday words. Explain before installing anything.
```

In English.

## Done when

- `docs/DESIGN.md` has the `<!-- make-app:how-built -->` marker.
- `README.md` and `AGENTS.md` are written, and `CLAUDE.md` is `@AGENTS.md`.
- `bd ready` shows the first feature task.
