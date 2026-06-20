---
title: Scale fan-out only as fast as visibility allows
date: 2026-06-20
category: orchestration
tags: [autonomy, subagents, lifecycle, gating, dag, loop]
confidence: learned
source: private-work
---

A painful overnight incident made the ordering constraint concrete: concurrency limits should be a function of observability, not of model capability or throughput ambition. When a coordinator dispatched a large fan-out of parallel subagents, one agent entered a silent polling loop for nearly an hour with no check-in, no alarm, and no visible representation on any dashboard. A second agent was spawned onto the same work surface, causing a collision. The coordinator discovered both problems only by manually inspecting filesystem timestamps and process listings — nothing had alarmed. The session itself had no start event recorded, so the dashboard showed a hours-stale snapshot as though work was current.

The root cause was architectural: the harness emitted signal only on flight completion. A hung, looping, or silently failed subagent produced zero observable output. There was no in-flight manifest, no heartbeat protocol, and no silence detector. Fan-out had scaled past the point where a human coordinator could track it manually.

The recovery path required two layers of fix. Immediately: kill the stuck and colliding agents, re-establish a known-good state, and cap concurrency to a size that one person could watch. Structurally: build a traffic-control subsystem before expanding concurrency again. That subsystem needs at minimum three components — a live flights board that distinguishes in-transit, active, and landed work; a check-in mechanism so each subagent emits a heartbeat on a known cadence; and a silence monitor that alarms when any agent's last check-in age exceeds a configured threshold, escalating after repeated misses.

The governing principle that emerged: the safe concurrency ceiling is wherever your visibility ends. Raising the cap is a reward for shipping observability — manifest coverage, check-in discipline, silence alarms, and a collision gate — not a reward for model performance improvements. Research on multi-agent failure modes corroborates the urgency: a substantial fraction of the total token cost in a failed long-horizon run is consumed after the first detectable failure signal, and step-repetition together with agents that are unaware they have reached a terminal state are among the most common failure clusters. Both failure types are invisible without a heartbeat and silence-alarm layer. Ship visibility first; scale second.
