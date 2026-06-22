---
title: Six entries deposited without sync record — formal batch acknowledgement
date: 2026-06-22
category: journal
tags: [docs, loop]
confidence: learned
source: private-work
---

Six learnings were committed to this journal in prior sessions but were not recorded in the deposit ledger at the time. This entry formalises their registration.

The entries cover five distinct generalizable patterns observed during the first sustained live-run of a multi-agent dispatch system and related coordination work:

**Navigation should follow the operator, not the implementation.** Any information hierarchy for an operational tool that organises by code layers or action categories will bury the operator most important items. Invert the structure so what the operator cares about today is at the top level.

**Unresolvable identifiers demand confirmation, not substitution.** When a reference from an operator cannot be mapped to a single unambiguous target, the correct response is to surface the ambiguity and ask — not to select the nearest plausible match and proceed silently.

**A code-read inference is not a rendered witness.** Confirming that a value is wired to the correct data source does not confirm that it renders correctly. For any dynamic UI value, the acceptable witness is observing the live element — not reading the setter.

**Multi-agent dispatch needs mechanical preflight gates.** Queue idempotency, HITL authorisation flags, orchestration-layer verification, spec precision, and premise currency each failed independently during first live operation. Manual discipline cannot substitute for structural gates at each of these points.

**Parallel agents sharing files collide at merge, not at dispatch.** The collision is invisible until merge time. The fix belongs at dispatch time: enumerate open-PR file ownership and treat overlap as a sequencing constraint before firing any new agent.

**Findings documents expire.** A work-list produced from a crawl or audit is accurate at the moment it was authored. Re-verify every item against the current integration branch before building — a scan that returns already-fixed is the gate working, not a wasted step.
