---
title: Serial sibling lanes into shared registration files produce the SAME conflict every link — kill the hotspot, not the conflicts
date: 2026-06-11
category: orchestration
tags: [parallelism, merge, layering]
confidence: learned
source: private-work
---

Five dashboard panels built by parallel lanes, merged serially, each conflicted in the *same five places*: the route table, the cache-TTL map, the data-source list, the panel array, and the shared stylesheet. Every sibling adds one entry to each shared registration structure, so every merge link reproduces an identical add/add conflict shape.

Two takeaways at different time horizons:

- **Short term: the resolution prompt is a reusable template.** "Result must contain all previously-merged siblings' registrations plus this branch's, each exactly once" resolves every link mechanically. When the conflict shape is invariant, write the resolution rule once and reuse it — don't re-derive it per merge.
- **Long term: predictable add/add conflicts are an architecture smell, not a merge problem.** Central registration structures that every contributor appends to are a designed-in hotspot. The durable fix is a registry pattern — per-unit registration files or decorators that the framework discovers — so each sibling touches only files it owns and the conflict class disappears entirely. Queue that refactor as soon as the second identical conflict appears; by the fifth you've paid more in merge labor than the refactor costs.
