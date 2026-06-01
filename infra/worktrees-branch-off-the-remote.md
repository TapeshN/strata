---
title: Branch worktrees off the remote's main, not stale local main
date: 2026-05-30
category: infra
tags: [worktree, multi-repo, release]
confidence: learned
source: private-work
---

In a multi-repo workspace where primary checkouts sit parked on long-lived feature branches and rarely `pull`, the local `main` ref silently goes stale. A tool that spins up new worktrees by branching off *local* `main` seeds every new branch from an outdated base. This surfaced as a release worker computing the wrong next version — basing a bump on a release two versions behind what had already merged to the remote.

The fix is mechanical, not vigilance: the worktree-creation tool should `git fetch` and prefer `origin/main` (or `origin/master`) over the local ref before branching. Every worktree then starts current by construction.

General lesson: any automation that derives state from a local ref must first reconcile that ref with its remote, or treat the local ref as untrusted. Verify a branch's base with `git merge-base HEAD origin/main` before trusting anything version-derived.
