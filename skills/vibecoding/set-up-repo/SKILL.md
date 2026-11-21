---
name: set-up-repo
description: Install git and beads, create the project repo, and connect a private GitHub backup, for an app made with /make-app. Use when the user asks to set up the project or GitHub, or opens the project on a new computer. /make-app runs it as step 1.
---

# Set up the repo

Get the folder ready: git to keep every version, beads to track the building work, and optionally GitHub as a backup. Skip any part that is already done; this step also runs when someone opens the project on a new computer.

## Workflow

1. **Check what's there:** `git --version`, `bd version`, whether `.git/` exists, whether `bd ready` works.
2. **Explain and ask.** In one message, list only what is missing, with one line each:
   - git: "keeps every version of your work, so any mistake can be undone"
   - beads (`bd`): "a to-do list for the building work, so nothing gets lost between sessions"

   Wait for a yes. If the user says no, explain that the flow needs both and that they can run `/make-app` again when ready, then stop.
3. **Install what's missing.**

   | | Windows | macOS | Linux |
   |---|---|---|---|
   | git | `winget install --id Git.Git -e --source winget` | `xcode-select --install` | `sudo apt install git` (or the system's package manager) |
   | beads | `irm https://raw.githubusercontent.com/gastownhall/beads/main/install.ps1 \| iex` | `brew install beads` | `curl -fsSL https://raw.githubusercontent.com/gastownhall/beads/main/scripts/install.sh \| bash` |

   A command that asks for a password (`sudo`) is for the user to run in their own terminal; never type it for them. After installing, run the version command again. If it says "not found", the terminal needs a restart: ask the user to restart Claude Code, then continue.
4. **Create the repo.** If there is no `.git/`: `git init -b main`. If `git config user.name` is empty, ask the user what name to put on saved versions and set `user.name` and `user.email` for this repo only. Any email works; say so.
5. **Start beads**, if `bd ready` fails:
   - The project was cloned from GitHub (`.beads/config.yaml` exists): `bd bootstrap`. It fetches the existing tasks.
   - Otherwise: `bd init --quiet --skip-agents`. The flag stops beads from writing into `AGENTS.md`; `prepare-to-build` writes the beads instructions there itself.
6. **First save**, if `git status` shows changes: `git add -A`, then `git commit -m "Start project"`.
7. **Tools from the build**, on a cloned project: if `docs/DESIGN.md` has a "How it's built" section, install any tool it names that is missing here (explain, ask, then install).
8. **GitHub**, if `git remote -v` shows nothing. Ask: "Do you have a GitHub account? It keeps a private copy of your work online, as a backup, and lets you undo mistakes."
   - **No:** link https://github.com/signup and say they can say "set up GitHub" any time. Continue without it.
   - **Yes:**
     1. If `gh --version` fails, explain and ask, then install: Windows `winget install --id GitHub.cli -e`, macOS `brew install gh`, Linux see https://github.com/cli/cli#installation.
     2. Ask the user to run `gh auth login --web --git-protocol https` in their own terminal and follow the browser steps. Never enter their codes or passwords.
     3. Check with `gh auth status`.
     4. Propose a repo name (the folder name in kebab-case) and wait for an ok.
     5. `gh repo create <name> --private --source . --push`.
     6. Connect beads to the same place, so the task list is backed up too: if `bd dolt remote list` is empty, run `bd dolt remote add origin git+<the URL from git remote get-url origin>`. Then `bd dolt push`, commit any changed `.beads/` config, and `git push`.

## Constraints

- GitHub repos are always private. If the user wants it public, tell them they can change it themselves in the repo's settings on GitHub.
- `git push` doesn't carry the tasks. Everywhere these skills say "back up", run `git push` and then `bd dolt push`, and only if there is a remote.

## Done when

- `git log` shows a commit, `bd version` works and `bd ready` runs.
- `git remote -v` shows GitHub, or the user declined it.
