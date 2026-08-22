---
title: A simultaneous batch kill leaves heterogeneous states — inspect each one
date: 2026-08-09
category: orchestration
tags: [subagents, parallel-sessions, rollback, idempotency]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A hard usage ceiling terminated several parallel background agents at the same instant. Recovery was not uniform across them: one had fully committed its work with its verification gates still unrun; one had a complete, uncommitted multi-file diff sitting in its own workspace; one had set up its workspace and done nothing further; and one had never even created a branch. Treating the batch as a single class — resume all of them, or re-dispatch all of them — would have either discarded finished work or duplicated it.

What worked was inspecting each workspace independently (its status, its commit log, its diff against the base) and triaging per unit: hand-finish anything that was committed or functionally complete by running the normal verification and shipping steps directly, and only re-dispatch the units that produced nothing. Most of the batch was recoverable in minutes this way; blindly re-running the whole batch would have spent the full cost of the batch a second time. The general rule: recover a simultaneously-killed batch from what is actually on disk in each unit, never from an assumption about what a unit "was doing," and never from a single uniform policy applied to the whole batch.
