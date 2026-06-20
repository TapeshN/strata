---
title: A threshold gate sourced from a constant enforces nothing
date: 2026-06-16
category: guardrails
tags: [cost, gating, determinism, evals, loop]
confidence: learned
source: private-work
---

During a cost-routing audit on a large agent fan-out, a circuit-breaker gate was found to be structurally inert. The gate accumulated per-turn cost estimates derived from a hardcoded constant rather than actual token usage, then compared the running total against a halt ceiling. Because the constant was far smaller than any realistic ceiling, the gate could never trip under real production load — it enforced nothing, silently, for as long as it had been running.

The root cause is architectural, not parametric: a gate whose input is computed from a fixed approximation rather than the actual measured quantity cannot respond to the real phenomenon it is meant to guard. Tuning the constant does not fix this; only sourcing the input from genuine measurement does.

The generalizable lesson is a definition of done for any threshold gate: (1) the metric driving the gate must come from its actual measurement substrate, not a proxy or estimate; (2) the gate must be exercised with a real input value that exceeds the threshold; and (3) the enforcement action must be observed to fire. A gate that has never been triggered by a real value above its ceiling is unproven, regardless of how long it has been in place.

This pattern appears wherever enforcement logic is wired before its data source is available and a placeholder constant is left in place indefinitely. The fix is not to deploy a better estimate — it is to refuse to ship a gate until it is connected to honest numbers and has been witnessed firing.
