---
title: Pull one shared API snapshot per fan-out — N agents re-reading the same state drain the rate budget the fixes need
date: 2026-06-10
category: orchestration
tags: [fan-out, rate-limits, api-budget, parallel-sessions]
confidence: learned
source: private-work
---

A fan-out of ~27 audit agents each independently re-pulled the same project-board and pull-request state through a points-based API. The reads were individually cheap but collectively exhausted the hourly budget — and the exhaustion landed on the *mutation* phase: when the coordinator went to apply the very fixes the audit had identified, the shared pool was at zero and the writes were blocked until the window reset.

The pattern: in any fan-out over a shared rate-limited API, the coordinator pulls one snapshot inline before spawning and hands it to every agent via their prompts or arguments. Agents work from the snapshot; live API calls are reserved for the verification pass, where freshness actually matters. Before any mutation batch, check the remaining budget explicitly — and if the primary query interface is drained, a secondary interface with a separate budget (e.g. REST vs GraphQL) can carry the writes.
