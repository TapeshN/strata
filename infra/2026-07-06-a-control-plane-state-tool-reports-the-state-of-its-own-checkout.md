---
title: A control-plane state tool reports the state of its own checkout — running it from a stale worktree produces phantom state instead of ground truth
date: 2026-07-06
category: infra
tags: [stale-worktree, ground-truth, resume, worktree]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A status or ledger-reading tool that operates on tracked files (for example, a tool that reports whether some long-running unit of work is currently open or closed by reading an append-only log committed to the repository) is only as fresh as the checkout it happens to run from. In a workflow that uses many parallel git worktrees alongside one canonical primary checkout, resuming a session can land you inside an older, unsynced worktree without that being obvious. Running the status tool there returns whatever that worktree's stale copy of the ledger says — which can show a unit of work as still open when it was actually closed and merged upstream long ago, because the close event lives only in the primary/remote history the stale worktree never pulled.

This is a dangerous class of bug because the tool's output looks completely legitimate: it runs without error and returns a plausible-looking state, giving no signal that it's reading from an out-of-date copy. The near-miss is acting on that phantom state — for instance, reopening or redoing work that was already finished. The general fix: any time you resume a session, switch between worktrees, or query state in a multi-checkout environment, verify ledger or status truth against the canonical primary checkout (or the remote's current history) before trusting or acting on it, rather than trusting whatever the current working directory happens to report.
