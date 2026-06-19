---
title: Cost anxiety was mis-attributed: subscription turns (unmetered) must be separated from API turns (real spend) before reasoning
date: 2026-06-16
category: infra
tags: [cost-attribution, subscription-vs-api, unmetered-plan, mis-attributed-spend, ledger-partition, channel-segment]
confidence: learned
source: private-work
---

a cost ledger that does not partition by billing model is a mis-attributed instrument — it produces a number that looks actionable but drives wrong decisions. The partition belongs in the schema (a `channel` field, which already exists) and in every consumer of the ledger (harvest, gate, dashboard). Heals [[reference_cost_breaker]] and the agent-memory entry "cost_breaker is a phantom backstop" with the correct framing: on a Max plan, subscription = zero marginal cost; only API calls meter.

before any cost-optimization decision (model tier, fan-out size, caching strategy), confirm which channel the spend lives in and whether it is metered on the current plan. "50k turns" is not a cost signal without the billing model attached. Add channel to the dashboard cost tile's primary display so the split is always visible at a glance.
