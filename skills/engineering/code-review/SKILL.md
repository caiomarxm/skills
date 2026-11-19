---
name: code-review
description: 'Review the changes since a fixed point (commit, branch, tag, or merge-base), or an uncommitted diff, along two axes: Standards (does the code follow this repo''s documented coding standards and the personal coding style?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents, reports them side by side, and applies the fixes when asked. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".'
---

Two-axis review of a diff:

- **Standards**: does the code conform to this repo's documented coding standards and the personal coding style?
- **Spec**: does the code faithfully implement the originating issue / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings. When the caller asks for fixes, step 6 applies them.

When you run as a subagent, "ask the user" below means stop and ask the parent.

## Process

### 1. Pin the diff

Whatever the user said is the fixed point (a commit SHA, branch name, tag, `main`, `HEAD~5`, etc.). If they didn't specify one, ask for it.

Capture the diff command once:

- **Committed work:** `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.
- **Uncommitted work** (the caller says so, and names the directory: this workspace or a worktree path): in that directory, `git diff HEAD` plus the untracked files from `git status --porcelain`. The three-dot command misses it.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here, not inside two parallel sub-agents.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. A path or text the user passed as an argument.
2. Issue references in the commit messages or branch name (`#123`, `Closes #45`, GitLab `!67`, Jira `ABC-123`), fetched with the tracker tools you have (GitLab, Jira).
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

Decisions the spec settles are settled. The review does not relitigate them.

### 3. Identify the standards sources

Search the repo for every file that documents how code should be written. When `CODING_STANDARDS.md` or `CONTRIBUTING.md` exists, it must be on the list.

Always add the **personal coding style** below. Treat its rules as documented standards. A task requirement or repo requirement wins when they conflict.

- CRITICAL: Keep it simple. Do not build speculative needs (KISS and YAGNI).
- Optimize for readability. Code is written once and read many times. A 5-year old could read the code and understand what it does.
- Use names that describe completely what the variable or function is or does, e.g. `credential_pool_summaries` over `summaries`
- For boolean variables or functions use names like `is_above_threshold` or `has_downloaded_tarball`, that read naturally on if statements.
- Good code should rhyme, and read like poetry. Make sure code with similar branches is consistent and follow the same patterns. Use newlines to group logical blocks of code together.
- Prefer functional code with strong types where the language and codebase support it.
- Try your best to keep only one level of nesting by using patterns like checks with early returns, module private functions with clear responsibilities, etc.
- In Python, prefer Pydantic for typed data models and list comprehensions over `map` or `reduce`. Use an explicit for loop whenever it will ease understanding.
- Prefer modular code with clear ownership and encapsulation. Aim for deep modules with clear interface, avoiding multiple shallow modules.
- Avoid unnecessary abstractions and complexity.

On top of those, the Standards axis always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) plus the ladder, that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads _what it is_ → _how to fix_; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

**The ladder.** New code should stop at the first rung that holds; flag code that skipped a higher rung:

1. Already in this codebase? Reuse the helper, type, or pattern.
2. Stdlib does it? Use it.
3. A native platform feature covers it? Use it (DB constraint over app code, CSS over JS).
4. An already-installed dependency solves it? Use it. Never add a dependency for what a few lines do.
5. Can it be one line? One line.
6. Only then: the minimum code that works.

### 4. Spawn both sub-agents in parallel

Issue both sub-agent calls together, in the foreground, and aggregate the reports they return. Use `subagent_type: generalPurpose` and name the model explicitly: the one the caller names, else Composer 2.5. Start each prompt with: "Read-only. Do not edit files."

Extra checks or questions from the caller add to the Standards review, never replace it. Always run both sub-agents, even when the caller says "review only".

**Standards sub-agent prompt** should include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the personal coding style, the smell baseline, and the ladder from step 3** pasted in full (the sub-agent has no other access to them).
- The brief: "Report, per file/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell or skipped ladder rung you spot: name it and quote the hunk. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline items are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt** should include:

- The diff command and commit list.
- The path or fetched contents of the spec, and which part of it is in scope.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings, because the two axes are deliberately separate (see _Why two axes_).

End with a one-line summary: total findings per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes: that's the reranking the separation exists to prevent.

Stop here unless the caller asked for fixes.

### 6. Fix (only when asked)

Apply the findings, Spec first, then Standards. Spec fixes change behaviour; Standards fixes then shape the result. Where a Spec fix touched the lines a Standards finding quotes, re-check that finding against the new code.

- **Spec (a) missing or partial** → implement it.
- **Spec (b) scope creep** → remove it, unless the spec needs it to work; then keep it and say why.
- **Spec (c) wrong** → fix it at the root cause.
- **Standards, hard** → fix it.
- **Standards, judgement call** → fix it when you agree; otherwise leave it and say why in one line.

Change only what a finding names. Keep every `ponytail:` comment and the simplification it marks. Keep every test in the diff. New non-trivial logic gets one small runnable check.

Then run the repo's tests, typecheck, and lint on the touched paths. A fix that breaks a check and you can't repair → revert it and mark it left.

Tag each finding in the step 5 report **fixed** or **left: <reason>**. Leave changes unstaged. Do not commit.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
