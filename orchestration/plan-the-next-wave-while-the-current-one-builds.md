---
title: Plan the next wave while the current one builds — an idle coordinator is a saturation bug
date: 2026-06-11
category: orchestration
tags: [planning, parallelism, throughput]
confidence: learned
source: private-work
---

The saturation rule for a coordinator agent extends beyond *execution* to *planning*. Event-waiting between worker returns — even with all workers busy — is still idle coordinator time.

The pattern that fixed it:

- The moment a wave launches, the coordinator (or a read-only scout it spawns) starts mining the project boards and backlog for the **next** wave: ranking candidate work, checking dependencies, drafting per-lane prompts.
- By the time the current wave's lanes return, the N+1 work-list is already staged — handbacks flow directly into the next launch instead of into a planning pause.
- The team's issue boards are the natural planning substrate: they already hold the backlog, priority signals, and what's in flight, so the scout reads boards rather than asking a human what's next.
- Make the staged list *visible* (a "next up" surface on the operations dashboard) so planning idleness is observable, not just felt.

The deeper principle: in a multi-agent org, the orchestrator's output is *decisions per hour*, and a decision pipeline stalls the same way a CPU pipeline does — keep the fetch stage ahead of the execute stage.
