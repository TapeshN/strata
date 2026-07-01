---
title: Per-seat pricing is a feature to build, not a config option to flip
date: 2026-06-30
category: infra
tags: [contracts, interfaces, lifecycle, gating, hitl]
confidence: learned
source: private-work
---

When a product plan is described as per-seat, per-license, or usage-based, the payment processor's price object only encodes unit economics — it does not deliver the capability. A per-seat price ID sitting inside a checkout integration that hardcodes quantity to one will silently sell a single unit regardless of the plan's intent. The full feature requires at minimum: a checkout flow that accepts and validates a seat quantity, a webhook handler that reads the purchased quantity from the subscription and syncs it to a durable store, an entitlement model that maps the seat count to access grants (typically org membership, invite slots, or per-member allowances), and enforcement logic that caps new additions at the purchased limit and resolves tier correctly when quantity changes. The practical prevention is to read the actual checkout and webhook code before advising that a new price ID is sufficient. If the plan description includes words like 'seats,' 'licenses,' or 'per user,' treat that as a signal to scope a feature — confirm the seats-to-access mapping with the operator before building rather than discovering the gap at integration time. Skipping the artifact-read step and assuming the price configuration does the work is the root of the failure mode.
