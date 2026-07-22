---
title: Build or deploy a third-party deliverable from an isolated clone, never a shared, actively-running dev tree
date: 2026-07-19
category: guardrails
tags: [deployment, isolation, worktree, safety]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

An actively-running development server for a separate, ongoing project must never be disturbed by an unrelated build/deploy task that happens to touch the same working directory. The safe pattern is to clone the target repository fresh into scratch space and build/deploy from there — but the same safety mechanisms that protect a primary working checkout (a guard against destructive recursive-deletes of scratch directories, a naming convention that recognizes managed worktrees) may not recognize a repository living entirely outside your usual workspace boundary, so plan for a plain clone rather than assuming your usual worktree tooling applies. Also worth remembering: a local clone's default branch can lag a remote merge commit — build from the branch tip whose actual file tree matches the merged result, not from chasing a specific merge commit a stale local mirror hasn't fetched yet.
