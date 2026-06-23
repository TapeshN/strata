---
title: Before writing a bespoke monitor or watchdog process, enumerate the platform-native primitives that could carry it
date: 2026-06-18
category: orchestration
tags: [loop, lifecycle, autonomy, hitl]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

The reflex when something needs monitoring is to write a process: a watchdog script, a polling loop, a background daemon. This reflex is expensive and usually wrong when the platform offers native primitives for the same purpose.

The tell is the delivery path. A monitoring process that exits with a non-zero code, or that fires a hook only within the current session, cannot reach the human when they are not watching. An exit code that nobody reads is not an alert. A hook that fires only in-session is invisible off-session.

Before building any monitor, alert, or automation, map the problem to platform-native primitives in priority order: scheduled tasks (which run independently and produce a run history), hooks (for in-session interception), push notifications (for off-session delivery to where the human watches), and subagents (for delegated execution). Bespoke code is appropriate only for the irreducible deterministic gap — the part the platform genuinely cannot do.

The check: if the signal disappears when the session closes, the delivery is not native. If the operator only finds out at the next scheduled review, the delivery is not native. Native delivery means the signal reaches the human wherever they are, off-session, at the moment the condition is detected.

Applying a native primitive at design time costs nothing. Retrofitting native delivery onto a bespoke process that has already accumulated integrations costs a rewrite.
