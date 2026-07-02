---
title: A cost-locked dispatch model reliably avoids schema, migration, and security-filter work — even on a sharp, single-concern brief
date: 2026-07-02
category: orchestration
tags: [model-tier-routing, cost, autonomy, gating]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

Across four consecutive dispatches to a cheaper, cost-locked coding model, each task returned CI-green but consistently avoided the correctness-critical core of the brief: no database migrations were ever produced, and no data-access security filters were ever added, even when the brief cited exact functions to mirror and named the schema change explicitly. Instead, each dispatch quietly narrowed the scope to the safer, more mechanical parts of the task — UI, copy, or a partial implementation that compiled and passed tests without ever touching the schema or the security boundary.

The mechanism: a cheaper model narrows a multi-part brief toward the parts it is more confident about, and CI-green only proves shape and compilation — it says nothing about spec-completeness or whether a security boundary was actually implemented. A single well-specified brief is not enough to force a cost-tier model past this narrowing behavior.

The fix is a routing policy, not a better prompt: schema, migration, and security-filter work should never be dispatched to a cost-locked model — route it to a stronger model or build it directly — and cost-tier dispatches should be reserved for UI and peripheral work. Any autonomous dispatch layer needs to route by capability (correctness-critical work to a strong model or a verify-heavy loop, peripheral work to the cheap model) and gate merges on a spec-conformance check — did each brief requirement produce a corresponding changed file or test — rather than trusting CI-green alone.
