---
title: A status display that re-derives a gate's decision from a narrower set of inputs than the gate itself will silently diverge from it
date: 2026-07-14
category: guardrails
tags: [display-truth-drift, gate-inputs, verify-tail, ui-state]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A readiness banner independently recomputed "is this gated?" using only one of the several signals the real enforcement gate considered. A first attempt at fixing a reported mismatch added a second signal, but still didn't cover the full input set the actual gate used — so the banner and the underlying decision kept disagreeing in cases the fix hadn't anticipated, including one driven by an upstream classification signal and another driven by a bounded retry/round counter the banner didn't know existed.

The root cause: the display surface re-implemented the decision from its own partial view of the inputs instead of consuming the gate's own evaluation.

The general rule: any UI or status surface that reports on a gate's decision must call the SAME evaluation function the gate itself uses, never re-derive an approximation from a subset of its inputs. Verify this by asserting the display's output matches the gate's verdict across a fixture grid spanning every input dimension the real gate considers — pairwise agreement across the grid, not a couple of spot checks. Corollary: when a change adds a new input or descriptor to a shared decision, sweep every surface that renders a summary of that decision as part of the same change's verification pass.
