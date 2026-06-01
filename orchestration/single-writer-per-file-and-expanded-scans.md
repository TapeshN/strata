---
title: Parallel write-agents need single-writer-per-file; scans must expand untracked dirs
date: 2026-05-31
category: orchestration
tags: [fan-out, isolation, subagents, ip-boundary, parallel-sessions]
confidence: learned
source: private-work
---

Processing a large parallel fan-out that built code across several worktrees surfaced two coordination failures.

First, a content-safety scan over a worktree reported "clean" but had silently skipped entire new directories: the porcelain status collapsed an untracked directory to a single entry, and the per-file scan loop's existence test skipped it. Re-running with untracked dirs fully expanded surfaced a real match the first pass missed. A scan that doesn't expand new directories is a false negative, not a pass.

Second, within one fan-out a "cleanup" agent deleted a module a sibling agent in the same wave had just created, breaking imports. Single-writer-*per-repo* wasn't enough.

General lessons: (1) any safety or secret scan over a tree must walk the actual files or force-expand untracked directories — never trust a collapsed status summary; (2) inside a fan-out, enforce single-writer-*per-file*, and forbid any cleanup/refactor stage from deleting or overwriting a file another agent in the same wave produced without an explicit reconcile step.
