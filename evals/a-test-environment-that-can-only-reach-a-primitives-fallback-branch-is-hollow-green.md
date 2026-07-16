---
title: A test environment that can only ever reach a primitive's fallback branch produces hollow-green coverage
date: 2026-07-16
category: evals
tags: [evals, hollow-green, reversion-litmus, serverless]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A background-work primitive that only functions inside a live request always throws when invoked from a unit-test or CI environment, because that environment never has an active request scope. Every test that exercised the code path routed through that primitive's fallback branch instead of its real registration path — not by test design, but because the environment made the real branch structurally unreachable. A downstream helper the fallback branch calls happened to perform its side effect synchronously, before any await, so the test's mocked assertion passed whether the work was wrapped in the primitive or simply invoked bare. Reverting the fix that added the primitive would leave every test green.

The generalizable litmus, applicable beyond this one primitive: before trusting a test's coverage of a fix, ask "would this suite still pass if the fix were fully reverted?" If the answer is yes, the suite is not exercising the changed code path — it may be structurally unable to, because the test environment can only ever reach one branch of a runtime-dependent primitive. The fix in that situation is not a bigger unit suite; it's a targeted mock or spy on the primitive itself that asserts it was actually invoked with the expected work, so the test can fail when the wrapping is removed even though the environment can never drive the real branch end-to-end.
