---
title: Uncommitted edits to an append-only ledger on the shared primary are invisible to all worktrees
date: 2026-06-16
category: guardrails
tags: [worktree, primary-drift, orphaned-uncommitted, rule-12, learnings-ledger, extract-before-compact]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When an append-only ledger — a changelog, a process log, a learning record — is edited directly on a shared primary checkout without being committed, those edits exist only on that checkout. Every worktree branches off the remote's main branch, not the local primary. Any entry appended to the primary's working copy but never committed is invisible to all worktree branches, and therefore invisible to every pull request that originates from them. If another session's worktree PR then advances main, the uncommitted entries are stranded behind: the ledger's public version jumps past them while they sit untracked on the primary.

The gap compounds because the shared primary may be kept perpetually dirty — a post-merge fast-forward is skipped whenever the working tree has uncommitted changes. The dirty primary cannot pull. The ledger diverges further with each merge cycle that bypasses it.

The fix is mechanical: every ledger addition must be committed via a worktree PR in the same session it is written. Writing a learning, an observation, or a status update to a tracked file is only half the work; the other half is making it reachable from the remote. A ledger that exists only in a local working copy is at risk from any operation that touches the primary — a checkout, a reset, a stash pop — and it is invisible to every consumer that reads from the remote.

A practical check: before closing a session, confirm that no tracked files on the primary have uncommitted changes. If they do, create a worktree branch, port the edits, and submit a pull request.
