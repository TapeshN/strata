---
title: A delegate's "gate is green" is scoped to what it touched, not to the whole system
date: 2026-07-22
category: orchestration
tags: [delegation, scope, adjudication, false-green, subagents]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A subagent was asked to bring a classification gate up to date for a bounded batch of items — the ones it had been handed. It classified exactly those, re-ran the gate, and truthfully reported it green. Nothing in the report was false, and yet a much larger backlog of unclassified items existed outside that subagent's assignment, and the phrase "gate is green" read as if the whole system were clean.

The failure is not dishonesty, it is an ambiguity of scope that a delegate cannot resolve on its own: a subagent's task boundary and the gate's true domain are different things, and a truthful local verdict inherits none of the system-wide meaning a reader will attach to it. The fix belongs to the coordinator, not the delegate. Whenever a subagent reports that a gate passed, the honest restatement is "green for the slice it was given," and the coordinator — the party who can see the whole system — re-runs the same gate unscoped before treating anything beyond that delegate's slice as verified. A delegate reporting its own scope accurately is doing its job correctly; assuming that scope equals the system is the coordinator's mistake to avoid.
