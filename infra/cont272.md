---
title: "Worktrees left by earlier sessions can hold unpushed rebases that diverge from the PR head"
date: 2026-09-12
category: infra
tags: ["worktree-drift", "pr-head", "backup-refs"]
confidence: learned
source: private-work
---

every "work on PR #N" task starts with `gh pr view N --json headRefName,headRefOid` and `git -C <wt> log -1 origin/<head>`; if the worktree's HEAD ≠ the PR head, park and re-anchor — never force.
