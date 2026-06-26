---
title: Coordinator saturation requires planning the next wave while the current one builds
date: 2026-06-11
category: orchestration
tags: [coordinator, planning, throughput, saturation, fan-out]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A coordinator that waits passively between lane completion notifications is operating below its saturation point. The builds are the slow path; the coordinator's contribution is the fast path — and idling the fast path while the slow path runs is waste.

The productive pattern is to treat each wave launch as a trigger: immediately spawn a planning scout (or perform planning inline) to mine the backlog, rank the next wave's work, and stage the work-list before any current-wave notifications arrive. When the first lane reports back, the next dispatch should be ready to fire without a round of analysis.

A dashboard or board that surfaces the staged next-wave list makes idleness visible — if the list is empty when lanes are building, the coordinator is behind on planning.

The saturation rule generalizes: a multi-stage pipeline maximizes throughput when each stage is fully utilized. In a coordinator-worker model, the coordinator's stage is planning and dispatch; it must run continuously in the background of worker execution, not in serial with it.
