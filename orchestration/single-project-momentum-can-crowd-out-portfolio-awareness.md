---
title: Single-project momentum can crowd out portfolio-level awareness in a multi-project coordinator
date: 2026-06-23
category: orchestration
tags: [autonomy, roles, lifecycle, multi-repo]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A coordinator running multiple active projects can enter a self-reinforcing single-project loop. Each fast, successful dispatch on one project encourages the next dispatch on the same project. Other active ventures receive no attention, not because they were deliberately deprioritized, but because the current project is always "next" in the coordinator's view.

This is distinct from the meta-work trap, where the coordinator spends time on orchestration infrastructure instead of product work. Here, the coordinator is doing real product work — just for one project while others stall.

The mitigation is a periodic lift-and-survey reflex: before going deep on a new large build for any single project, sweep the full portfolio state and explicitly note anything that has gone untended. The act of writing down "project X has had no activity this session" is often enough to trigger the re-prioritization.

A cross-project handoff document that lists every active project by status, updated each session, is the mechanical anchor. If the coordinator cannot name the current state of each active project, portfolio awareness has already been lost.
