---
title: Two hook-resolution gotchas — a per-use grant file scoped to the wrong root, and a chained command blocked mid-line
date: 2026-07-17
category: infra
tags: [hooks, gating, worktree, autonomy]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Two separate mechanical gotchas surfaced from the same class of cause: a hook and the thing meant to satisfy it resolving paths from different roots.

**A per-use permission grant must be written under the exact root the consuming hook resolves from, or it is silently orphaned.** A command that grants a one-time permission (to allow a normally-blocked action once) was run from a primary checkout and wrote its grant file under that checkout's root. The pre-tool-use hook that consumes the grant, however, was running inside a session scoped to a DIFFERENT worktree, and resolves its "where do I look for a grant" path from that worktree's own root — a different absolute path. The grant file existed, was correctly formed, and was never found, so the gated action was blocked again as if no grant had been issued at all. The general fix: whenever a per-use grant, lock, or similar file is created to satisfy a hook, create it under the SAME root the hook's own code resolves paths from (typically the active session's project directory, not wherever the granting command happened to be run from) — and when a grant "doesn't take," the first diagnostic step is diffing the two resolved roots, not re-issuing the grant.

**A hook block on a chained shell command refuses the WHOLE line, not just the guarded step within it.** When a single command line chains multiple steps together (for example, a fix followed by a commit, joined with a logical AND), and a pre-execution safety hook blocks that command because one part of the chain matches a guarded pattern, NONE of the chain executes — including steps earlier in the line that looked safe and were not themselves the reason for the block. It is easy to assume the safe-looking earlier steps still ran, since they didn't trigger anything. The correct response after ANY hook block on a chained command is to explicitly re-check the actual current state (a status check, not memory of what the command was supposed to do) before retrying anything, and to prefer un-chaining commands that are likely to trigger a gate so that a block doesn't silently discard unrelated, already-safe work bundled into the same line.
