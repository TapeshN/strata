---
title: Ground test-failure verdicts in the implementation or specification, not the failure message
date: 2026-06-02
category: guardrails
tags: [evals, verify-dont-trust, determinism]
confidence: learned
source: private-work
---

When diagnosing test failures, failure messages and assertion text are unreliable. A static message like "not rejected with code X" describes the expected behavior, not what actually happened — reading it as a description of the received value produces the wrong verdict. Always read the raw received value from the test output and cross-reference it against the implementation or the specification before concluding anything.

In a concrete case, a static assertion-message string was read as if it described the app's behavior, leading to the wrong conclusion that expected features were missing. The actual cause was a different HTTP status code from an unauthenticated fixture — a test bug, not a missing feature.

General lesson: assertion messages describe expectations; they do not describe reality. For any failing test, read the raw received value before forming a verdict.
