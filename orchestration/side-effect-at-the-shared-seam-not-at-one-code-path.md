---
title: A side-effect wired to one code path starves when a second path produces the same artifact
date: 2026-06-17
category: orchestration
tags: [idempotency, side-effects, pipeline-seam, learning-loop, rag, consumer-producer]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When two execution paths both produce the same artifact — a result object, a record, an event — any side-effect wired only to one path will silently starve on the other. Consumer-side tests that seed the ledger directly will pass; nothing in the suite detects that the direct-producer path never fills it.

The pattern surfaces in learning loops and data pipelines: the "normal" orchestrated path (coordinator → router → executor) triggers the side-effect correctly; a second path (direct execution, a CLI runner, a smoke-test harness) produces the identical artifact and drops the persistence step on the floor because it bypasses the layer where the side-effect lives.

The fix is to move the persistence step into the shared seam that every execution path passes through — the single point of convergence regardless of how the artifact was produced. Make the step idempotent so that a double-call (one from each path) collapses safely: derive a deterministic ID from the artifact's content, and let a second write on the same ID be a no-op rather than a duplicate.

Idempotency is not optional here — it is the prerequisite that makes moving the side-effect to the shared seam safe. Without it, a path that reaches the seam twice (once from the executor, once from a higher orchestrator reading the same result) inflates the ledger.

Before declaring a loop or pipeline "wired end-to-end," verify that every execution path fills the ledger — not just the primary orchestrated route.
