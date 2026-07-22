---
title: A permission grant and the action it authorizes must never be recorded in the same turn
date: 2026-07-22
category: guardrails
tags: [merge-floor, autonomy, gates, permission-separation]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A merge-gate design was tested by attempting to record a per-item merge grant and then immediately consume that grant to perform the merge, both inside one uninterrupted command sequence. The gate refused outright — and that refusal is the correct behavior to preserve, not a bug to route around. Even under a standing, broader authorization to operate autonomously for a bounded window, an agent recording its own permission and then spending that same permission in the same breath collapses the entire point of having a separate grant step: the grant exists specifically so that a human-authored record of intent precedes, and is distinguishable from, the automated action that follows it.

The generalizable rule: any gate that requires a prior authorization record must enforce that the record-writing step and the permission-consuming step happen as genuinely separate actions, ideally separated by something (a different turn, a different process invocation, an audit-visible gap) that a bypass attempt cannot collapse. A standing autonomy grant that lets an agent act without pausing for per-step confirmation should still never let that same agent both mint and spend a scoped permission atomically — the separation between "who authorized this" and "what happened as a result" is the entire safety property, and it must survive even well-intentioned attempts to save a round trip.
