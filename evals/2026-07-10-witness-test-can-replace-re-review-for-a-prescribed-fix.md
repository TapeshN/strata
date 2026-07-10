---
title: A prescribed fix can be re-verified with one witness test instead of a full re-review
date: 2026-07-10
category: evals
tags: [testing, code-review, verification, security]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

On a money or auth-adjacent code path, verifying a bug fix doesn't always require re-running a full independent adversarial review from scratch. When the original reviewer already prescribed the exact fix and the change is small, the load-bearing step is a targeted witness test: one that exercises the specific failure path the review uncovered, and that would have failed before the fix and passes after it.

What happened: an adversarial review of a payment/credit-handling path found that the existing test suite mocked a downstream enqueue call to always succeed, which meant a duplicate-detection branch (an idempotency check hitting an existing record) was never actually exercised — so a bug in that branch, where a resource should have been refunded on the duplicate path but wasn't, wasn't visible to any test. The reviewer specified the exact fix. The engineer implemented it, then instead of dispatching a second full adversarial review, wrote one new test that mocks the duplicate-hit condition and asserts the resource is correctly refunded — directly exercising the path the original review flagged as blind.

How to apply: treat "review found the bug and prescribed the fix, engineer implemented exactly that prescription" as a convergence signal. When that signal holds, the highest-value re-verification isn't another round of open-ended review — it's a narrow, purpose-built test that forces execution through the specific branch the first review proved was previously untested. This is cheaper and often more rigorous than a second review, because it produces a concrete pass/fail witness rather than another round of manual reasoning. It does not replace independent review when the fix is large, touches new surface, or wasn't fully specified by the reviewer — in those cases a fresh full review is still warranted.
