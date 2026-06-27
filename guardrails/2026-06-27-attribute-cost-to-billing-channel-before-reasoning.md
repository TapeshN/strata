---
title: Attribute cost signals to the right billing channel before reasoning about spend
date: 2026-06-27
category: guardrails
tags: [cost, latency, tokens]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A cost ledger that sums subscription-plan turns and metered API turns into a single total
produces a number that looks actionable but drives wrong decisions. Subscription-channel
turns on a flat-rate plan carry zero marginal cost; only API-channel turns represent real
spend. When the two are aggregated, the total is dominated by the high-volume unmetered
channel, creating the illusion of large spend where none exists — while the small volume
of genuinely metered calls is invisible under the noise.

The practical consequence is that model-tier choices, fan-out sizes, and prompt-caching
investments get optimized against a cost that does not exist on the plan in use, while the
real spend goes unmanaged.

The fix is to partition the ledger by billing channel at the schema level and expose the
partition to every consumer — the harvest step, the dashboard tile, and the gate that trips
on overage. Before any cost-optimization decision, confirm which channel the spend lives in
and whether that channel is metered on the current plan. "N thousand turns" is not a cost
signal without the billing model attached.

Any observability instrument that does not distinguish plan-channel from usage-channel is
a mis-attributed instrument: it produces a number, but the number does not represent what
it appears to represent.
