---
title: A healed workaround goes stale when the gate it describes is later fixed
date: 2026-06-25
category: guardrails
tags: [doctrine-drift, evolution-apply, heal-staleness, gate-calibration, workaround]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When a process document is healed to describe a gate's behavior — "use this workaround because the gate false-fires on X" — that advice is coupled to the gate's current implementation. If the gate is subsequently fixed to no longer false-fire on X, the healed advice becomes incorrect. The workaround now misleads contributors who follow it, and the gate is silently suboptimal because the fix is being routed around unnecessarily.

A same-day combination is especially deceptive: a heal and a gate fix land on the same day addressing the same trigger. Neither references the other. The healed document freezes the workaround advice at the moment it was written; the gate fix removes the condition that made the workaround necessary. Downstream readers see only the advice, not the gate's current behavior.

The prevention: whenever triaging, reviewing, or applying a healed piece of advice that describes a gate's behavior, re-verify the advice against the gate's current implementation. Read the gate code and confirm whether the described condition still applies. A same-day combination of a heal and a gate fix touching the same mechanism is a specific tell — reconcile them explicitly.

More broadly: documentation that describes a workaround for a known failure has a shorter validity horizon than documentation that describes a stable invariant. Build in a re-verification step whenever the underlying gate changes, not only when the documentation is reviewed for its own sake.
