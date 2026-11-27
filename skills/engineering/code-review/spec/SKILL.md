---
name: code-review-spec
description: >-
  Use when user asks you to review a diff against the originating
  spec. Read-only.
disable-model-invocation: true
---

# Spec

Review the diff against the spec. Read-only. Do not edit files.

Decisions the spec settles are settled. The review does not relitigate them.

## Input

- The diff command and the commit list.
- The path or fetched contents of the spec, and which part of it is in scope.
- No spec → report "no spec available" and stop.

## Report

Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words.
