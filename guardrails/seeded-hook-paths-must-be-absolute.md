---
title: Safety hooks seeded into isolated worktrees must use absolute paths to the hook files
date: 2026-06-04
category: guardrails
tags: [gating, worktree, isolation, multi-repo]
confidence: learned
source: private-work
---

Safety hooks seeded into a sub-repository worktree must use absolute paths to the hook files, because the hook files live in the control-plane tree — outside the worktree's directory. A relative path in the seeded settings resolves to a nonexistent file inside the worktree, so the hook is registered but inert.

This is the worktree-scoped instance of the "wired is not working" principle: a hook registered with an unresolvable path produces a settings file that reads green while enforcing nothing.

The seeding step's acceptance criterion is not "settings file written" but "path resolves to a real file AND the hook actually executes." Write the verification into the seeding step itself — resolve the path, then invoke the hook, then assert it exits cleanly.

General lesson: when propagating control-plane hooks to isolated worktrees, verify resolution and execution, not just registration.
