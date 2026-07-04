---
title: git stash create captures the entire working tree, not just the file you meant to move — too broad for a targeted transfer
date: 2026-07-04
category: infra
tags: [worktree, git, multi-repo]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Moving a single edited file from a long-lived checkout into a fresh worktree by way of `git stash create` + `git stash apply` produced dozens of unrelated merge conflicts. The stash object created by `git stash create` snapshots every uncommitted change across the entire working tree at the moment it's taken — not just the one file the operator cared about. If that working tree also has unrelated in-progress deletions, renames, or edits (accumulated across a long session), all of them travel inside the same stash object. Applying that stash to a worktree branched from a clean, current remote state — where those other files are already in a different shape — produces conflicts on files the operator never intended to touch.

`git stash create` is only safe to apply elsewhere when the entire working-tree state is coherent with the destination branch. For a targeted single-file (or small, known-file-set) transfer between a working checkout and a fresh worktree, skip stash entirely: read the file's current content directly and write it into the destination worktree, then commit only that file there. This sidesteps the whole-tree-snapshot problem because the transfer primitive operates on exactly the content you intend to move, nothing else.

The general lesson: any git primitive that snapshots "the working tree" rather than "the file" inherits the risk of everything else dirty in that tree. Prefer explicit, scoped transfer (read the target content, write it to the destination) over a tree-wide snapshot-and-apply whenever the source and destination trees may have diverged.
