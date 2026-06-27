---
title: A correctness witness must assert the deterministic structural cause, not a rendered metric or timing value
date: 2026-06-22
category: evals
tags: [determinism, evals, golden-sets, judge, reproducibility]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A test that asserts a rendered metric — a pixel coordinate, a viewport-relative position, a timing value, or a cumulative layout shift score — is fragile in ways that structural assertions are not. Rendered values vary by viewport, scroll position, JavaScript optimizer behavior, and timing. A test that measures the wrong thing will pass when the feature is broken and fail when the feature is fixed.

The principle: a correctness witness asserts the deterministic cause, not an observable side effect of the cause.

Concrete patterns:

- For a performance defect that blocks the main thread, surface the computed result into rendered state (a data attribute) so the JavaScript optimizer cannot dead-code-eliminate the work. Assert the data attribute, not a timing value.
- For a layout overflow defect, assert that the element is inside its scroll container and that its content overflows the container's internal bounds — not that a rendered screen coordinate has a particular pixel value after scroll.
- For a behavioral defect with nondeterminism, seed the nondeterminism (use a deterministic seed that the implementation reads and tests control) rather than asserting on floating output.
- For a scoring or computation defect, derive the expected output independently (a re-implementation of the scoring logic in the test, not calling the same function) and assert exact equality.

The positive-control check closes the loop: after writing the test, verify it goes red when the defect is present. A test that passes regardless of whether the defect exists is not a test.
