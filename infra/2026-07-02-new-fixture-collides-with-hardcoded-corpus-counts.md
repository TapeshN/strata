---
title: A new fixture or dataset entry colliding with a hardcoded corpus count is the guard working, not a bug — budget the count-maintenance tail up front
date: 2026-07-02
category: infra
tags: golden-sets, ci, evals, reproducibility
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Each time a new item was added to a growing internal corpus of fixture applications (each contributing some number of intentionally-seeded items to a shared index), it broke several places that hardcoded the previous total: an end-to-end test asserting an exact count on an index page, a table mapping each fixture to its expected item count, and unit-level assertions built on the old total. Every single time, the drift was caught immediately by CI going red — never a silent pass.

This is presented as a positive outcome, not a complaint: a drift-detector that fires the moment a new entry breaks an assumption about corpus size is exactly the guard doing its job, and the alternative (a count assumption that silently goes stale and nobody notices) is strictly worse.

The generalizable lesson is about budgeting, not correctness: any system that maintains a "total known items" invariant across a growing, multi-contributor corpus has a fixed, recurring maintenance tail every time a new contributor (a new fixture, a new dataset shard, a new plugin) is added — update the count table, update the index-level count assertion, update the unit-level count asserts. Treat this as a known, budgeted checklist item for "add a new fixture," not a surprise to debug fresh each time. If the collision is not immediately obvious from a red CI check, that is the signal something is wrong with the guard, not that the corpus grew.
