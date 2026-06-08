---
title: Documentation rules for operational state are suggestions; mechanical enforcement in tools is the standard
date: 2026-06-01
category: infra
tags: [gating, worktree, parallel-sessions, docs]
confidence: learned
source: private-work
---

Documentation rules for operational state (which tasks are in flight, which stages they are in, which queues need action) are read once at session start and then forgotten. Task trackers and status boards go stale not through negligence but because the correct update action was never embedded in the tools that every operation calls.

Prevention: when you find yourself writing "always do X" in a documentation rule, identify which tool executes X automatically. If none does, build the tool hook first. Three enforcement points for board hygiene: (1) the worktree creation command, which knows what work is starting; (2) the pull-request creation command, which knows the work is ready for review; (3) the session-start script, which can surface stale items and emit fix commands.

General lesson: operational state (what is in flight) requires enforcement in the tools that are called on every operation — not just documentation that is read once. Documentation alone is a suggestion; a hook in a called tool is a constraint.
