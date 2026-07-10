---
title: Run a task on the substrate that actually generates the measurement you need
date: 2026-07-07
category: orchestration
tags: [orchestration, instrumentation, measure-what-you-run]
confidence: learned
source: private-work
---

A team building out cost/usage instrumentation for a background dispatch system deliberately wanted the first real research task routed THROUGH that dispatch system, specifically so the new instrumentation would have a real event to record and verify against. Running the same task through a different, un-instrumented execution path would have produced the same useful research output, but zero instrumentation data — silently defeating the actual purpose of choosing to run it at all.

The general rule: when a task's purpose includes generating measurement, telemetry, or a receipt for a system that is itself being verified or exercised, route it through the INSTRUMENTED substrate, even when a cheaper or more convenient path exists that would deliver the same nominal output — the untracked shortcut quietly defeats the actual goal, which was never just the output, it was proving the measurement pipeline works.
