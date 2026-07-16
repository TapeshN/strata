---
title: A long-running session's own hooks and gates can silently lag a fast-moving main branch
date: 2026-07-16
category: guardrails
tags: [lifecycle, gating, parallel-sessions]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Hooks and safety gates execute out of the working tree of the session that invokes them, not out of whatever is newest on the shared main line. A session whose working copy was checked out some days earlier keeps running the OLD versions of every hook — including ones whose entire job is to catch drift — for as long as that session stays alive, even after the shared main line has already shipped fixes to those exact hooks. In one observed case this produced two compounding false results in the same session: a hygiene check kept warning about a condition its own already-merged fix would have cleared, and a separate guard — predating an already-merged exemption — nearly blocked the very merge that would have brought the guard itself up to date.

Fix without waiting for a full session restart: refresh just the hook and tooling directory from the shared main line into the working tree (no commit needed, since hooks run from working-tree state, not from history). Prevention: a session-start check that compares the working tree's tooling directory against the shared main line and warns — never auto-overwrites, since a session may be deliberately testing a hook change in progress — when it has drifted meaningfully behind.
