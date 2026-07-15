---
title: Hermetic unit fixtures can structurally dodge the exact integration seam where the real bug lives
date: 2026-07-12
category: evals
tags: [evals, reproducibility, gating]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A batch of changes each shipped with a fully green test suite and was still caught, every time, only by an adversarial reviewer reproducing the failure end-to-end through the real call path. In each case the unit tests had set up state directly — calling an internal helper to stage a fixture, or invoking an inner function instead of the outer entrypoint real usage goes through — which meant the exact seam where two pieces of logic actually interact was never exercised by the suite. A time-window check that only ever saw timestamps set directly by the test never saw a timestamp that had passed through the real claim/rename path that shifts its meaning. A conversion routine's tests never exercised the one input shape that the real adapter renders unsafely, so a broken conversion shipped green and would have misbehaved only in a real run.

The generalizable rule: a green suite proves that the fixtures the suite constructs behave correctly — it does not prove that the real production entrypoint, driving the real end-to-end path, produces the same state those fixtures assumed. When a test sets up its scenario directly instead of driving it through the actual entrypoint the system uses in production, that shortcut is exactly where a bug can hide invisibly behind 100% green. The counter-measure is an adversarial or integration pass that reproduces the failure by walking the real path, not a larger hermetic unit suite — the practical argument for including at least one reviewer whose job is specifically to attempt to reproduce a failure through the real wiring rather than read the code and the tests.
