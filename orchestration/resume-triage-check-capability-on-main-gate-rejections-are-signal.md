---
title: Resume triage must check capability presence on main, not just branch PR status; gate rejections are a prioritisation signal worth instrumenting
date: 2026-06-14
category: orchestration
tags: [preflight, gating, parallel-sessions, docs]
confidence: learned
source: private-work
---

**Resume triage blind spot:** classifying stale work-in-progress by checking "does this branch have an open PR?" misses the case where the capability was shipped via a different lane. Unique-looking uncommitted code on a branch can be fully obsolete if the functionality landed on main through a parallel effort. Before resuming any stale work-in-progress, search main for the capability — by component name, function name, or test-id — rather than only checking whether the current branch has an associated PR.

**Gate rejections are telemetry, not waste.** When a deduplication or quality gate repeatedly holds or rejects the same learning, the rejection itself carries information: the principle is being re-derived with high frequency, which is evidence it is load-bearing or under-applied. Instead of discarding held entries, instrument the rejection stream: record what was held, what it duplicated, and how often. Aggregate this into a "most-reinforced principles" view. The gate-holds then become a prioritisation signal — which ideas should be elevated, enforced more mechanically, or better documented — rather than entries that simply fail to ship.

**The pattern generalises to any deduplication gate in a learning or knowledge pipeline.** Gate-hold data is a frequency distribution over concepts that keep surfacing. A principle that never makes it through deduplication (because it always duplicates an earlier entry) is precisely the one that deserves the strongest mechanical enforcement downstream.
