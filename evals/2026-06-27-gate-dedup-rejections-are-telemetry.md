---
title: Gate holds and deduplication rejections are telemetry, not failure noise
date: 2026-06-27
category: evals
tags: [evals, judge, loop, rag]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When an automated quality gate holds or rejects an item for being a near-duplicate of
an existing entry, the instinct is to treat the rejection as friction — a cost the
system imposes before the item can land. That framing discards signal.

A learning that a team keeps re-deriving — encountering the same failure class,
re-documenting the same root cause — is high-confidence and load-bearing. The dedup
gate sees this pattern directly: it rejects the new item and names what it duplicates.
The rejection stream contains the frequency of each principle and the spacing between
its re-derivations.

Instrumenting that stream — recording which entries are held, against which existing
corpus entries, and how often — produces a ranked list of the principles the team most
needs to internalize. The most-rejected entries are the ones that keep failing to stick.

The generalizable design principle: when a gate consistently rejects a category of
input, the rejection count is a signal about that category, not about the gate. Build
a report off the rejection ledger — which items are rejected most, against what — and
the gate's output becomes an active prioritization tool rather than a discard bin.

This inverts the default framing. An automated deduplication system that only discards
captures the discard event and loses the metadata. An instrumented system that records
rejection reason, rejection target, and frequency turns the gate's most common operation
into the gate's most valuable output.
