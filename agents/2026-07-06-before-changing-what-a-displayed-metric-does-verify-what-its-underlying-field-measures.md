---
title: Before changing what a displayed metric does, verify what its underlying field actually measures at the producer — a readout's label is not proof of its meaning
date: 2026-07-06
category: agents
tags: [metric-semantics, producer-first, gauge, mislabeled-readout]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A request to make a displayed number "reset daily" implicitly assumes that number is a cumulative count of something like spend or usage. Reading the actual code that produces the field showed it was never a running total at all — it was a live snapshot of current in-memory context occupancy, which naturally grows within a single working session and drops back to near-zero whenever that session's context gets compacted. Under that real semantic, "make it reset daily" was not a sensible instruction to implement, because the field was never daily-cumulative to begin with; the two concepts (live occupancy versus cumulative spend) happened to share a display position but measured entirely different things. Investigating further, the one part of the system that already recorded genuine cumulative usage over time existed but had been effectively unused for weeks.

The general lesson: when a request asks to change the *behavior* of a metric, start by reading the producer's own definition of what the underlying field represents — its writer code or its documentation — before touching the display layer. Building a new feature on top of a misread field produces confident, plausible-looking work that answers the wrong question entirely. Where the mismatch is real, the durable fix is two-part: build or wire the actually-needed cumulative source properly, and rename the old readout so its label stops implying a meaning it never had.
