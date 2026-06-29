---
title: Fan-out concurrency and executor-routing are orthogonal decisions — collapsing them defaults to the least-resistant path
date: 2026-06-29
category: orchestration
tags: [subagents, roles, autonomy, routing, dag]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When a coordinator decides to parallelize a task, two separate decisions are in play: (1) *how many concurrent units* to spawn, and (2) *which executor layer* should run the work. These decisions are orthogonal and must be made explicitly in sequence. Collapsing them into one "spawn subagents" reflex causes the concurrency decision to silently resolve the executor question by default, defaulting to whichever path has the least friction at the time.

In practice, the in-session primitive (spawning local agents) is always lower friction than a multi-step external dispatch path. When throughput pressure is high and both decisions happen in a single reflex, the low-friction executor wins without ever being consciously chosen.

The fix is a two-question checklist before any fan-out: first, how many parallel units are needed; second, which executor layer owns this work category. When those categories are held apart by organizational doctrine — for example, product repository work routes through a defined dispatch stack while control-plane work can run locally — the executor question must be answered from doctrine, not from friction.

A memory-resident rule that is not mechanically enforced is invisible under throughput pressure. The appropriate gate is a warn-on-mutation-in-wrong-executor hook that surfaces the routing question before the fan-out completes.
