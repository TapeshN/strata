---
title: Recover a crashed builder from its on-disk work rather than restarting from scratch
date: 2026-06-07
category: orchestration
tags: [lifecycle, subagents, fan-out, worktree]
confidence: learned
source: private-work
---

When a builder process dies mid-execution, any files it wrote to disk survive the crash. Before restarting from scratch, check the worktree for uncommitted files — the builder may have completed most of its work.

Commit and push those files immediately to make them durable, then verify they compile and pass tests, then finish only the remaining work. Recovering from on-disk state preserves the completed work that a full restart would discard and waste.

General lesson: uncommitted files survive a process death on disk. "Get the work committed and pushed" is always the first step after a builder crash — durability before anything else. Role separation is preserved: the coordinator commits the recovered work and the independent review still happens at the review layer.
