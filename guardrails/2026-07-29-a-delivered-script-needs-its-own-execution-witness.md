---
title: A delivered script needs its own execution witness — a green test suite around it proves nothing about whether it ever ran
date: 2026-07-29
category: guardrails
tags: [gating, evals]
confidence: learned
source: private-work
implementation_target: agent-guardrails
efficacy: decorative
---

A one-off script — a data-seeding utility — shipped as part of a larger, fully green batch: type-checks clean, hundreds of passing tests. It failed on its very first real invocation. It referenced an identifier format a related import path never actually produces, and wrote to a field that doesn't exist on the model it targeted. None of the batch's gates had ever executed the script; a compiling, well-typed script that no test imports is code no gate has actually verified.

The generalizable rule: any standalone deliverable script (seed, backfill, migration, one-off ops utility) must be run at least once against a representative environment as part of the same wave's gates that claim it's done, and the run's actual output — not just "it compiles" — belongs in the handback. A green suite around a script is not a witness for a code path the suite never executes; this is the same class of gap as an unimported export never running, just at the level of an entire script rather than a single function.
