---
title: Stamp a status at the event it represents, not at a downstream optional step
date: 2026-06-24
category: guardrails
tags: [lifecycle, determinism, contracts, interfaces]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A status that means "the user performed action X" should be recorded at the moment X occurs, not at a later step that optionally follows it.

When the stamp is deferred to a secondary completion step, any user who performs X but does not reach the secondary step appears inactive or unregistered despite having crossed the threshold. The secondary step may be optional, skippable, or reachable only under certain conditions. Tying the status stamp to it means the status is unreliable as an indicator of X.

The pattern that works: record the status change at the earliest unambiguous event that proves X has happened. Treat any step that follows as a non-blocking nudge or soft task, not as the condition that activates the status.

This applies to any state machine where a status represents a lifecycle event: activation, acceptance, verification, enrollment, and so on. Gate the status on the event itself, not on later UI flows, confirmations, or optional completions.
