---
title: Strict file-ownership boundaries in a multi-agent build can produce orphaned work — the wiring lives in the one file nobody owns
date: 2026-07-30
category: orchestration
tags: [subagents, boundaries, parallel-sessions]
confidence: learned
source: private-work
implementation_target: coordinator-layer
efficacy: load-bearing
---

A parallel build finished with every static gate green — type-checks clean, every test passing, zero errors reported — and two of its deliverables were completely unreachable by any real user: a new feature surface that nothing linked to, and a new utility module with passing tests that called it directly but zero callers anywhere in the actual application.

The root cause is the ownership rule working exactly as intended, and still producing a dead result: telling each parallel agent "touch only your assigned files; another agent owns everything else" is the right rule for preventing collisions, but a feature's wiring — the navigation link, the route registration, the call site that actually invokes a new module — almost always lives in a file outside the feature's own assigned set. Each agent hit that boundary at exactly the wiring step, correctly declared it out of scope, and moved on; every local signal stayed green because everything that existed was correct — the only thing missing was the one connection that made it reachable. No static gate catches this: unreferenced exports and unlinked pages both type-check fine, and tests that import a module directly exercise code no actual user path reaches.

Two-part fix. First, name a reachability owner in the fan-out plan before launching it — either a dedicated integration pass that owns the shared registries (navigation, routing, wiring) as its own explicit slice, or a specific grant of those shared files to one particular agent for that round. Never leave wiring ownership implicit between two agents' boundaries. Second, ask every agent for the actual reach path in its handback, not just a diff — state the exact path a real user or caller takes to reach the change, and if there is none, say so explicitly and name what would need to change to make it reachable. An agent forced to write down the path notices its absence; an agent that only reports a list of files changed does not.
