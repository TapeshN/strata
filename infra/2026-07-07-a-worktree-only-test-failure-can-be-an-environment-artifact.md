---
title: A test that fails only inside a symlinked-dependency worktree is often an environment artifact
date: 2026-07-07
category: infra
tags: [worktree, symlink, npm-workspaces, testing]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

In a workspace where multiple working copies (git worktrees) of the same repository share a single installed-dependency tree via a symlink, a couple of automated tests started failing inside one specific worktree while passing everywhere else, right after new fields had been added to a shared internal package. The natural first read was "a code regression." Investigation showed the tests were invoking a workspace-aware build command that resolved the shared package back through the SYMLINKED dependency tree, which still pointed at the PRIMARY checkout's older version of that package — not the worktree's own, newly-edited copy. The worktree's own source was correct the whole time; the test was simply building against the wrong, stale copy of a dependency due to how the symlink resolved.

The way to confirm this diagnosis is to point the type-checker or build tool directly at the worktree's OWN copy of the shared source (bypassing the symlink) and confirm it's clean, and separately to trust a genuinely fresh, from-scratch dependency install (such as the one a continuous-integration run performs) as the real arbiter — if that's green, the worktree-local failure was environmental.

General rule: in a workspace that shares installed dependencies across multiple working copies via a symlink, a build or type-check failure that involves a workspace-internal package is a candidate environment artifact before it's a candidate code defect — verify against the worktree's own source directly, and trust a fresh, non-symlinked install as the tie-breaker, rather than chasing a failure that may not actually exist in the code.
