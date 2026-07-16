---
title: Stage one state for a look-check before building every state of a novel visual pattern, and stop live diagnosis once a diff proves the regression isn't in the code
date: 2026-07-16
category: orchestration
tags: [design-loop, diagnosis-budget, iteration-cadence]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

Building an entirely novel visual pattern — a new widget shape or layout, as opposed to a variation on an existing one — straight from a text description, all the way through implementation and verification, before a human ever sees it, risks discovering a fundamental direction mismatch only after the full build is already done, at which point the cost of the wrong direction is much higher than it needed to be. When a pattern is genuinely novel, stage a single cheap mock or state for a human look-check first, before building out every variant or state of that pattern; a quick look at one state catches a wrong direction for a fraction of the cost of catching it after every state has already been built.

A related but separate discipline: when investigating a regression that resists diagnosis, check early whether the regression's scope can be proven clean by diffing the actual logic files involved. If every changed file in that diff is purely cosmetic (styling, layout) and none of it touches the logic plausibly responsible for the regression, that is strong evidence that the live, hard-to-reproduce debugging session chasing a root cause is heading down an unproductive path. At that point, the better move is to stop the live diagnosis, record the investigation together with the evidence gathered so far for a later, better-resourced look, and move on to other work — rather than continuing to spend session time on a diagnosis that a clean diff has already shown isn't in the code path being examined.
