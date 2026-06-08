---
title: A test asserting a gap exists becomes hollow the moment the same PR closes the gap
date: 2026-06-07
category: guardrails
tags: [evals, determinism, gating, verify-dont-trust]
confidence: learned
source: private-work
---

A test written to assert that a gap exists (a feature is not yet implemented, a guard is absent, a behavior is missing) must be updated in the same pull request that closes the gap. If the gap is closed and the test is not updated, the test becomes a no-op: the conditional skip that detected the absence never fires, the test passes with zero meaningful assertions, and its name now describes an absent behavior.

This produces a "green" test that is actually testing nothing — worse than a red test, because it produces false confidence.

Prevention: when adding a capability that a gap-documenting test was watching for, flip the test to positively assert the new behavior in the same change. The name should also update: "gap documented" becomes "guard exists and fires."

General lesson: a test that documents an absence is only valid while the absence exists. It has a built-in expiration date.
