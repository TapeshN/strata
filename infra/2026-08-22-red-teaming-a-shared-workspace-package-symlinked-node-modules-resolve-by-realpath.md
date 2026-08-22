---
title: Red-teaming a shared workspace package in a scratch copy — symlinked node_modules resolve by realpath, not by the path you copied to
date: 2026-08-22
category: infra
tags: [verification, harness]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

While preparing a scratch copy of a workspace package to test a security fix by reverting it (to confirm a regression test actually goes red), a naive symlink into the scratch copy's dependency tree resolved back to the original, already-patched worktree by realpath — so the "reverted" copy was silently still exercising the patched code, and the revert-then-test check would have passed for the wrong reason.

General rule: in any monorepo/workspace setup where package resolution follows symlinks, a scratch or throwaway copy used for red-teaming a fix must have its symlinked dependencies deliberately relinked to point at the scratch copy's own patched-or-reverted files — not left pointing at the original tree by default. Confirm which physical file a test is actually importing (follow the realpath) before trusting that a revert changed anything.
