---
title: Tests that lock a taste call in as an exact parameter will churn the moment a human reviews the real thing — assert the invariant instead
date: 2026-07-29
category: evals
tags: [evals, hitl]
confidence: learned
source: private-work
implementation_target: shared-prompts
efficacy: uncertain
---

Two tests asserting specific aesthetic parameters — an animation's hold duration, a visible hint of particular wording — both failed after a live human review of the actual running product; the reviewer reversed both choices on sight. The tests weren't wrong about what they guarded; they were correctly locking in a taste call that a live look-and-feel review legitimately overturned.

Aesthetic parameters (durations, visible copy, degree of emphasis) asserted as exact values will churn at a predictable, non-trivial rate whenever a human reviews the real artifact — that churn is signal that the review loop is working, not test rot to be annoyed at. The fix is to assert the invariant the aesthetic choice serves (things stay synchronized across layers, an element never gets stuck mid-transition, an accessibility affordance is still present) rather than the specific number or string, and to keep the literal parameter in one named constant the test reads — so a taste reversal becomes a one-line edit instead of a test rewrite. When a human reviewer reverses a taste call, updating the test in the same pass — and noting the reversal somewhere visible — prevents the next person from re-arguing a decision that has already been made.
