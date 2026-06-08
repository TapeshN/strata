---
title: Stub-asserting tests become false negatives once the feature is implemented
date: 2026-06-03
category: guardrails
tags: [evals, determinism, verify-dont-trust]
confidence: learned
source: private-work
---

A test written to assert that a feature is "not yet implemented" (expecting a non-zero exit, a stub response, or an error message) becomes a false regression the moment the feature is actually implemented. The test still passes — because the stub behavior no longer exists — but may pass with zero meaningful assertions, or describe an absent behavior in its name while testing nothing.

This is a class of test debt that accumulates silently: the test was correct when written, then became incorrect when the feature shipped, with no visible failure to signal the update was needed.

Prevention: when implementing a previously-stubbed feature, grep the test suite for tests asserting stub or not-implemented behavior for that feature, and update them to assert the real behavior in the same change. A test that conditionally skips when the feature is absent must be flipped to positively assert the feature's behavior once the feature exists.
