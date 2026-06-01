---
title: Renaming a primary checkout orphans its worktrees — git worktree repair fixes it
date: 2026-05-31
category: infra
tags: [worktree, git, multi-repo]
confidence: learned
source: private-work
---

After renaming several primary checkout directories, an inventory found multiple worktrees the management tool still listed but that git itself couldn't operate on ("not a git repository," empty HEAD). Cause: each worktree's `.git` file pointed at the *pre-rename* gitdir inside the primary checkout, which no longer existed at that path. The worktree→primary link broke, and git couldn't resolve the worktree at all.

`git -C <renamed-primary> worktree repair` rewrote each linked worktree's `.git` pointer to the new gitdir, and all of them came back alive. No committed work was lost — every branch survived in the renamed primary's object store.

General lesson: moving or renaming a checkout that has linked worktrees breaks their back-pointers. Run `git worktree repair` as part of any such rename, and never assume a management tool's worktree list is operable — verify HEAD resolves before trusting an entry.
