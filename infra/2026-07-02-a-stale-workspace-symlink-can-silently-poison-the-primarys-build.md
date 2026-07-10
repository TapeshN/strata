---
title: A stale workspace symlink can silently poison the primary checkout's build
date: 2026-07-02
category: infra
tags: [worktree, npm-workspaces, symlink, shadow-state, stale-build]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A package-manager install run from inside a secondary working copy (a git worktree sharing a monorepo's dependency workspace) left the PRIMARY checkout's shared-package symlink pointing INTO that secondary copy instead of back at itself. From then on, the primary silently type-checked and built against whatever code happened to live in the secondary copy — not its own.

This is dangerous for two reasons. First, it is invisible to version control: a symlink target is not something an ordinary status or diff surfaces, so the primary can drift out of sync with its own source with zero git-visible trace. Second, it compounds with routine cleanup: if the secondary working copy is later reclaimed (deleted as "already merged, tree clean"), the primary's build breaks with no obvious cause — the failure surfaces long after the action that caused it.

The fix applied: re-running the package install from the primary re-pointed the symlink correctly; reading the symlink's actual target directly was the one-line diagnostic that made the cause obvious once suspected.

General rule: in any monorepo/workspace setup where multiple checkouts share installed dependencies via symlinks, treat "which tree does this symlink actually resolve into" as a thing to check after any cross-checkout package-manager operation — and before reclaiming a worktree, verify no other checkout's shared-dependency symlink still points inside it. This is one instance of a broader class: any piece of runtime or build state that can resolve into a tree other than the one it logically belongs to is a silent-poisoning risk, and the fix is always to make resolution point back to a canonical, stable location.
