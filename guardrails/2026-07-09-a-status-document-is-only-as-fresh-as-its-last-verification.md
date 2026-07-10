---
title: A status document is only as fresh as its last verification against reality
date: 2026-07-09
category: guardrails
tags: [docs, verify-then-merge, ci]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

Across one broad review pass covering many workstreams at once, several authoritative-sounding status claims in planning and hand-off documents turned out to be flatly contradicted by the actual, current state of the systems they described — not because anyone lied, but because the documents were written at one point in time and the underlying reality had moved on without the documents being refreshed. One document asserted a dependency "does not exist — confirmed directly," while that dependency had since been built and merged, meaning a piece of work was incorrectly marked blocked behind a dependency that was actually already satisfied. Another document claimed a piece of cost-tracking instrumentation was "live but producing no data," when in fact the instrumentation had essentially never run against real activity at all — a different and more serious problem than the document described. A third document referenced a specific local configuration that was no longer the one actually installed.

The general rule: treat any status table, planning document, or hand-off note that is older than the work it describes as a HYPOTHESIS, not a fact. Before sequencing new work on top of an inherited claim — "does X exist," "is Y blocked," "is Z instrumented and live" — re-verify that specific claim against the current, real state of the system, especially for anything load-bearing enough to determine what gets built next. A periodic pass whose only job is refreshing stale status claims against ground truth is cheap insurance against mis-scoping an entire wave of work on an outdated premise.

A related, narrower lesson about failing automated checks: when a pull request's automated checks fail, don't assume the fix is always "just rebase onto the latest base branch." Failures fall into at least three different buckets that need different fixes: the failure was already present on the current base before this change (inherited, not caused by this change), the branch is simply stale and a fresh merge/rebase resolves it (staleness), or the change itself actively reintroduces or conflicts with something that was fixed upstream after the branch was created (a baked-in regression, which needs a content fix, not a rebase). Diffing the failing change against the CURRENT base branch at the specific point of failure is what correctly distinguishes these — only the middle case is safe to resolve mechanically.
