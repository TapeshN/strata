---
title: A coordinator session can go idle at a clean turn boundary while still holding a shared lock, and a lock resolved relative to the claiming session's own checkout silently becomes per-checkout instead of single-writer
date: 2026-07-01
category: orchestration
tags: [autonomy, multi-repo, worktree, roles, lifecycle]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A single-writer coordination lock is meant to guarantee exactly one active coordinator session across a whole workspace. Two independent failures compounded into an apparent "stuck" state. First, a coordinator process was alive and consuming negligible CPU, but its conversation had already reached a clean completion point (a merge landed, a summary was written) minutes earlier — the process was not mid-work, it was idle after finishing, yet a UI-level status indicator continued to display it as actively working. This is a UI/process desync, not a hang: the underlying session is safe to end, but nothing signals that distinction from the outside.

Second, and more seriously, when a replacement session started in a different checkout of the same logical workspace (a linked worktree rather than the primary checkout), the lock-acquisition logic resolved the lock's location relative to the current working directory's own repository root rather than the one true primary root. Because the lock file itself was excluded from version control, the new checkout's copy of that path was always empty and therefore always "claimable" — the replacement session was told it had become the coordinator, while the original session's lock (recorded against the primary root) still named the old, wedged process. Two sessions simultaneously believed they held sole coordination authority, because the lock had silently become scoped per-checkout instead of globally.

The general fixes: any lock or singleton-authority mechanism whose scope is meant to be workspace-wide must resolve its storage location through a canonical, checkout-independent root (for example, resolving the true top-level repository regardless of which linked working copy the code is currently running from), never through a path relative to the current process's own working directory. Separately, before terminating any process suspected of being stuck, verify safety directly — inspect where its most recent work actually ended (a clean boundary versus mid-operation) and check for any child processes with side effects still in flight — rather than assuming a quiet, low-CPU process is either safely idle or actively hung.
