---
title: Recursive nested fan-out multiplies leaf agents beyond visibility — count leaves first and use a flat capped pool
date: 2026-06-29
category: orchestration
tags: [subagents, autonomy, throughput, dag]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When a coordinator dispatches a small number of agents and each agent itself invokes a research-style fan-out with further sub-agents, the total concurrent caller count is not the top-level dispatch count — it is the product of each nesting level. A small top-level dispatch produces dozens of concurrent callers within seconds through unbounded nesting, enough to saturate an account-level concurrency limit before any single task completes.

The leaf count is structurally invisible from the root dispatch call: each node reports its own launch, not its descendants. The first observable signal of runaway nesting is typically an account-level throttle error, which arrives after the damage is done.

The fix is to determine the expected leaf count before dispatching, and to instruct every leaf agent explicitly that it must not spawn sub-agents or invoke deep-research primitives. The instruction must be in the prompt, not a default: absent an explicit prohibition, a general-purpose agent will follow the most capable path available.

When a nested-fan-out signal appears mid-run — an unexpected wave of concurrent agent notifications or a throttle error — the correct response is to stop the in-flight set, wait for the cooldown, and re-run the same work as a flat pool of explicitly-bounded leaf agents.
