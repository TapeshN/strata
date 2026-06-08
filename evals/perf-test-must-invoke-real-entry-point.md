---
title: Performance and budget tests must invoke the real entry point, not an internal function call
date: 2026-06-07
category: evals
tags: [latency, evals, verify-dont-trust, ci]
confidence: learned
source: private-work
---

A performance or budget test that benchmarks an internal function call will report a different number than the actual entry-point invocation, because production entry points often run additional sections, setup phases, or duplicate passes that in-process calls skip. The latency the operator experiences is the full invocation's latency, not the function's.

In a concrete case, an in-process timing measured one duration while the real CLI invocation measured twice that — because the entry point ran every section twice. The in-process test was green; the CLI was over budget.

The fix: timing tests must invoke the real entry point via subprocess, measuring the full execution including startup and output handling. Any budget gate based on an in-process measurement is benchmarking the wrong thing.

General lesson: a performance test is correct only if it measures the path the operator actually runs.
