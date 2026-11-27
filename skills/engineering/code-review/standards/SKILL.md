---
name: code-review-standards
description: >-
  Use when user asks you to review a diff against coding standards.
  Read-only.
disable-model-invocation: true
---

# Standards

Review the diff for standards. Read-only. Do not edit files.

## Input

- The diff command and the commit list.
- Extra checks or questions from the caller. They add to this review, never
  replace it.
- No diff → stop.

## Standards sources

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

## Report

Report, per file/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell or skipped ladder rung you spot: name it and quote the hunk. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline items are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words.
