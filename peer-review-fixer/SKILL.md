---
name: peer-review
description: Fixes code based on peer review comments and feature descriptions. Use when the user provides PR comments and a feature description (text, file, or Jira link) to address feedback in a codebase.
---

# Peer Review

You're working on a new feature describe as the user's input ticket or markdown file. Implementation is complete and you are now in peer review mode.

## Instructions

When the user provides a feature description and PR comments, follow this workflow:

1.  **Gather Context**:

    - If the `<feature_description>` contains a file path (e.g., `@path/to/file`), read the file.
    - If the `<feature_description>` contains a Jira ticket link (e.g., `https://checkr.atlassian.net/browse/EDATA-1234`), use the `user-Atlassian` MCP tool `getJiraIssue` to fetch the ticket details (summary and description).
    - If it's plain text, use it as the primary requirement source.

2.  **Analyze PR Comments**:

    - Carefully read the `<pr_comments>` provided by the user.
    - Identify the specific files and code sections mentioned in the comments.

3.  **Verify and Fix**:

    - Inspect the relevant code in the codebase.
    - Determine if each PR comment represents a valid issue based on the feature description and coding standards. You should judge critically whether a fix is necessary or not.
    - If the issue is valid, implement the fix.
    - Ensure the fixes follow the project's architecture and clean code rules.

4.  **Summarize**:
    - Provide a concise summary of the problems found and the fixes applied.
    - For each non-addressed comment, provide a recommended answer for the PR.
