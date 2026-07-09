---
title: Static adversarial source review can pass what a runtime end-to-end test fails
date: 2026-07-02
category: evals
tags: [evals, determinism]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A verification workflow ran three independent review lenses over a change purely by reasoning about the source code, and all three correctly passed it — the logic they were checking (a mapping, a filter, a seed) really was sound. Yet the actual end-to-end test suite, run against the live application, failed on the same change, because a newly written test's own locator was buggy and never actually exercised the intended element. The static reviewers had no way to detect this, because a test-harness defect that only manifests when code is actually executed is invisible to any process that only reads and reasons about source text.

This is not a failure of the static review lenses — they answered the question they were built to answer, correctly. It is a boundary on what static, source-level review can ever tell you: it validates that the logic as written is sound, and structurally cannot catch a defect that only exists in how a runtime harness exercises that logic.

The generalizable rule: for any change to user-facing behavior, a runtime end-to-end run is the load-bearing verification step, and static or adversarial source review is a complement to it, never a substitute for it. Do not treat an all-pass verdict from purely reasoning-based reviewers as equivalent to a passing live run, especially for anything a static reviewer cannot itself execute.
