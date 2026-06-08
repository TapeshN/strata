---
title: "Done" means reachable in a live path and enforced by an active gate, not just test-green
date: 2026-06-03
category: guardrails
tags: [gating, ci, verify-dont-trust, lifecycle]
confidence: learned
source: private-work
---

A project can accumulate hundreds of passing unit tests and still be entirely inert in production. If the tested units are never invoked in a live path — never called by a real runner, never registered in a real hook table, never included in a real CI run — the tests prove only that the units compute, not that they do anything.

Specific failure modes found: safety hooks present in the primary checkout but absent from every active worktree where work actually happens; a server whose main entry point was a stub; an eval ledger with no producer and no consumer; a preflight suite that nothing invoked; and no CI running any gate at all.

A unit test proves a unit computes. It does not prove the unit is reachable. These are different claims.

General lesson: "done" requires two checks in addition to green tests — (1) is there a live caller that invokes this in the actual execution path? (2) is there an active gate (CI check, hook, real path) that enforces it? No CI is itself a blocking gap.
