---
title: When an automated pipeline dies at its final verification step, check what was already produced on disk before assuming the whole run is lost
date: 2026-07-02
category: orchestration
tags: [subagents, lifecycle, verify-dont-trust]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A multi-step automated pipeline failed with a structured-output error at its very last stage — the stage responsible for verifying the earlier work, not the stage that produced it. On the surface this looked like a lost run that should be retried from scratch. Inspecting the working directory instead showed every earlier step's output fully present and the tree clean; only the final verification step's own output-formatting had failed, not the work it was meant to verify.

Rather than re-running or re-spawning the whole pipeline (which would waste the resources already spent and risked forking state if the retry diverged even slightly from the original), the verification was performed directly and manually against the artifacts already on disk — running the actual test suite and hand-triggering the same checks the automated verifier would have run. This manual pass found real issues the automated verifier would likely have caught, so nothing was actually lost by the failure, and re-deriving it manually added value rather than just recovering to parity.

The generalizable rule: on any pipeline or workflow failure, check the artifacts already produced before deciding whether to re-run anything — a failure at a late verification stage often means the actual work is intact and only the reporting step broke. A secondary lesson from the same incident: verification steps required to emit large, deeply-nested structured objects are a fragile link — keeping their required schema small (a verdict plus a short evidence field, rather than deep nesting) makes that stage less likely to be the one that fails.
