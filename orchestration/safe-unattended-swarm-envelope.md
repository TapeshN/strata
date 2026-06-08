---
title: A safe unattended build swarm requires isolation, local verification, and human-gated merges
date: 2026-06-02
category: orchestration
tags: [autonomy, hitl, gating, parallel-sessions, isolation]
confidence: learned
source: private-work
---

A safe unattended build swarm requires four constraints working together:

1. **Lane isolation by file zone**: agents work on disjoint file sets so no two agents write the same file. Unverified cross-agent writes introduce integration defects that are invisible until a human reviews.
2. **Local verification before commit**: each agent verifies its work (type check, lint, tests) before committing. An agent that commits unverified work defeats the purpose of the parallel build.
3. **Human-gated final actions**: merges, publishes, tags, and external side effects remain human-gated. The coordinator opens draft PRs; the human approves. No agent auto-merges.
4. **Hang and report on blockers**: agents that encounter an ambiguous situation hang and report rather than making assumptions. The coordinator reviews at resumption.

Quality over volume: a few well-scoped, reviewable lanes produce better results than a sprawling parallel build with many cross-cutting concerns.
