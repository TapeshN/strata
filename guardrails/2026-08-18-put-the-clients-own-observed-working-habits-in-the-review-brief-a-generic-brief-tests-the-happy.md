---
title: Put the client's OWN OBSERVED WORKING HABITS in the review brief — a generic brief tests the happy path and misses the bug that actually bites
date: 2026-08-18
category: guardrails
tags: [review-loop, verification, client-grounding]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A pricing feature was reviewed against a brief that simply said "test the price schedule," and it
passed — until a reviewer was separately told, in the client's own words relayed by the operator,
that the client habitually enters prices for years into the future and had already done so once
in their current system. Testing THAT specific sequence (a far-future price entered, then a nearer
one entered afterward) surfaced a genuine high-severity bug: the feature resolved which price
applies by CREATION ORDER rather than by effective date, so the far-future price silently and
permanently stranded itself once a nearer one existed. A generic brief tests in-order entry and
passes; only the client's actual habit reproduces the defect that matters.

The generalizable practice: any review brief for a client-facing feature should carry a short,
concrete paragraph describing how that client actually works today — drawn from real observed
behavior (an export, a screenshot, something said in a call) — and should name the SPECIFIC
sequence that client would naturally perform. When an operator relays a client's habit, that
sentence belongs in the brief close to verbatim, as a literal test case, not as background color.
