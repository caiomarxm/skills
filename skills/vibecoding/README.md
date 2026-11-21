# Vibecoding

Skills that take someone who doesn't code from an app idea to a working app, in Claude Code. The person starts with `/make-app`, which runs these steps for them. Each step can also be called on its own (`/build-feature add dark mode`), and it sends the person back to `/make-app` if an earlier step isn't done:

1. **Set up** (`set-up-repo`): git, beads, a private GitHub backup.
2. **Spec** (`write-spec`): an interview that writes every decision down, then one design doc, `docs/DESIGN.md`.
3. **Modules** (`find-modules`): split the app into parts, each with one job.
4. **Prepare** (`prepare-to-build`): shape, tools, testing, `README.md`, `AGENTS.md`, beads tasks.
5. **Build** (`build-feature`): one feature at a time: build, check, show, save.

It also uses two skills from this repo: `grilling` and `domain-modeling`.

## Install (for agents)

The user says something like "install vibecoding from caiomarxm/skills". Install into the user's project folder, not globally. Don't install any software in this step: `/make-app` does that later, after asking.

1. **Check the folder.** It must be empty, or a project this flow started. If it holds another codebase, say so and stop.
2. **Download this repo** into a temporary folder. No git needed.

   Windows (PowerShell):

   ```powershell
   $tmp = Join-Path $env:TEMP "vibecoding-skills"
   Invoke-WebRequest https://github.com/caiomarxm/skills/archive/refs/heads/main.zip -OutFile "$tmp.zip"
   Expand-Archive "$tmp.zip" -DestinationPath $tmp -Force
   ```

   macOS or Linux:

   ```bash
   tmp=$(mktemp -d)
   curl -fsSL https://github.com/caiomarxm/skills/archive/refs/heads/main.zip -o "$tmp/skills.zip"
   unzip -q "$tmp/skills.zip" -d "$tmp"
   ```

   The files are in `skills-main/` inside the temporary folder.
3. **Copy these 8 folders** into the project at `.claude/skills/<folder>/`, replacing any older copy:

   | From `skills-main/` | To |
   |---|---|
   | `skills/vibecoding/make-app` | `.claude/skills/make-app` |
   | `skills/vibecoding/set-up-repo` | `.claude/skills/set-up-repo` |
   | `skills/vibecoding/write-spec` | `.claude/skills/write-spec` |
   | `skills/vibecoding/find-modules` | `.claude/skills/find-modules` |
   | `skills/vibecoding/prepare-to-build` | `.claude/skills/prepare-to-build` |
   | `skills/vibecoding/build-feature` | `.claude/skills/build-feature` |
   | `skills/productivity/grilling` | `.claude/skills/grilling` |
   | `skills/engineering/domain-modeling` | `.claude/skills/domain-modeling` |

4. **Write the starter `AGENTS.md`**, if there is none:

   ```markdown
   # Project

   ## Start here
   For any request about this app, use /make-app.
   ```

   `prepare-to-build` replaces it later with the full version.
5. **Write `CLAUDE.md`** with the single line `@AGENTS.md`. Claude Code reads `AGENTS.md` only when there is no `CLAUDE.md`, and this line makes it read both. If a `CLAUDE.md` already exists, add the line at the top.
6. **Delete the temporary folder.**
7. **Tell the user**, in their language: "Done. Type /make-app and tell me your idea." If `/make-app` doesn't show up, ask them to restart Claude Code.

Nothing is committed here: there may be no git yet. `set-up-repo` makes the first commit.

## Update

Repeat install steps 2, 3 and 6. Leave `AGENTS.md`, `CLAUDE.md` and everything else alone. If the project has git, commit with the message "Update make-app skills".
