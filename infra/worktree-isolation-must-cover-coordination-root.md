---
title: Worktree isolation must cover the coordination-layer root, not only sub-repositories
date: 2026-06-06
category: infra
tags: [worktree, parallel-sessions, isolation, multi-repo]
confidence: learned
source: private-work
---

Worktree isolation — giving each agent its own isolated checkout instead of writing to a shared primary — must cover the coordination root, not only the sub-repositories. Two agents writing the shared coordination checkout in parallel produced a branch with intermixed commits from both agents, creating a confused history that required manual cleanup.

The fix: make the coordination root a first-class worktree target, and add a guard that blocks direct edits to root control-plane files unless the editing session is in an isolated worktree of the root or holds a coordinator lock.

General lesson: any shared checkout is vulnerable to parallel-write collisions. The coordination layer is not exempt. Apply the same isolation discipline to the root as to any sub-repository.
