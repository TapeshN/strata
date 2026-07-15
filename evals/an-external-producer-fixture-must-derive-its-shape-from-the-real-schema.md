---
title: A fixture standing in for an external producer's response must derive its shape from the producer's own schema, not the consumer's guess
date: 2026-07-12
category: evals
tags: [evals, reproducibility, determinism]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A consumer read a field from the top level of a response payload; the producer of that payload actually nested the same field one level down, inside a sub-object. The consumer's own integration test passed anyway, because whoever wrote the test fixture had hand-authored the fake response using the same, wrong, top-level shape the buggy consumer code expected — so the buggy code and the buggy fixture agreed with each other, and the suite stayed green while the real wiring against the real producer was silently dead the whole time. The bug was found only by tracing the actual producer's schema directly, not by trusting the passing test.

The generalizable rule: whenever a test fixture stands in for an external producer's response — a different service, a different repository, a different layer of the same system — its shape should be built by reading the producer's actual schema or source, or by recording a real response, never by guessing the shape from the consumer side. A fixture invented alongside the consumer shares whatever assumption the consumer got wrong, so a green test against that fixture proves only that the two agree with each other, not that either is correct. When reviewing any consumer/producer boundary, the question to ask before trusting a green integration test is whether the fixture's shape was derived from the producer or invented alongside the consumer — and the strongest possible check is a fix that only reverting the consumer's assumption, not the fixture, causes to fail.
