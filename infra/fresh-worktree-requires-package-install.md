---
title: A fresh worktree does not inherit installed packages; verify the build toolchain before launching a builder
date: 2026-06-07
category: infra
tags: [worktree, ci, isolation, reproducibility]
confidence: learned
source: private-work
---

A fresh worktree does not inherit the parent checkout's installed packages. Symlinking the package directory from the parent to the worktree breaks module resolution because the runtime resolves the symlink's canonical path and resolves packages relative to that location, not the worktree.

A missing development dependency can manifest as a cryptic crash (a raw engine backtrace) that superficially resembles an out-of-memory error. Isolation technique: reproduce the minimal reproduction — check whether the interpreter starts, whether the tool version-checks, whether the full build invocation runs — to distinguish a broken module graph from a memory issue.

Prevention: run a fresh package install in every new worktree. Verify that the primary build command actually executes before launching a builder there. A builder dispatched into a worktree with a broken toolchain will error immediately and waste the build slot.
