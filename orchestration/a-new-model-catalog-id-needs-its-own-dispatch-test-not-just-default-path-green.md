---
title: Adding a new model-catalog id to a dispatch path needs its own live test — a config field that only changes which model is invoked can still hang the entire pipeline
date: 2026-07-02
category: orchestration
tags: [model-tier-routing, cursor-dispatch, hang-diagnosis, testing]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A dispatch pipeline shipped an opt-in config field that let a caller request a specific model by catalog id, merged on green CI. The default path (no override) had been exercised in CI; the new, non-default catalog id had not. In production, dispatches carrying the new model id hung the dispatch worker indefinitely — in one case after the remote call had already fired and a remote agent was actively working, in another before any remote call was made at all. An otherwise byte-identical dispatch without the override completed normally in seconds.

The mechanism: a model-specific code path was shipped with only the default branch actually exercised end-to-end. CI-green proved the field compiled and the default path worked; it said nothing about whether the new branch — reached only when a caller supplies the new value — worked at all.

The generalizable rule: any feature that adds a new enum or catalog value to a code path needs a test that actually exercises that specific value, not just a compile check plus the pre-existing default-path test. Before re-running a dispatcher after a hang, first establish whether the earlier attempt's remote side effect already fired — a blind retry can double-fire a paid remote call. And any dispatch worker should carry a hard per-task timeout so a single hung task cannot block the pipeline indefinitely, rather than relying on someone noticing the silence.
