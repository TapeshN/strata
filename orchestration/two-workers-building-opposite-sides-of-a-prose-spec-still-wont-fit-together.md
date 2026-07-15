---
title: Two workers building opposite sides of an integration to the same prose spec can each pass their own tests and still not fit together
date: 2026-07-13
category: orchestration
tags: [contracts, parallel-sessions, evals]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

Two pieces of work were built in parallel by two different builders implementing opposite sides of the same handshake — a producer and a consumer of the same payload — from a shared written description of what that payload should look like. Each side's own tests passed, and each side's continuous-integration run was green. When the two sides were actually connected, the shapes didn't match: one side had guessed a slightly different field layout than the other side actually sent. Tellingly, the builder on one side had even left a comment anticipating that a reconciliation would eventually be needed — the mismatch wasn't a surprise once looked for, it was just never looked for until integration.

The root cause is treating a prose description as if it were a contract. Prose can be read two slightly different ways by two different builders, and passing your own tests only proves internal consistency with your own reading of the spec, not compatibility with the other side's. The fix at the source: any contract that crosses a build boundary — two repositories, two parallel workers, two layers of the same system — needs exactly one machine-readable shape, a shared schema snippet or fixture that both sides read from and test against, not two independent proses of the same idea. And the batch that builds both sides is not actually finished until a live, real cross-side check runs end to end — a passing pair of independent test suites is not evidence the two halves fit together.
