---
title: A running subagent's model tier cannot be changed mid-flight — interrupt and relaunch fresh, and plan tier before dispatch
date: 2026-07-08
category: orchestration
tags: [subagents, model-tier-routing]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

An attempt to move an already-running subagent onto a stronger model partway through its task, by resuming its existing run with a different model specified, failed outright — a running agent process cannot have its underlying model swapped while it is still executing. The pattern that actually works: interrupt the running agent, confirm what it has produced so far without letting it commit anything further, then launch an entirely new task on the desired model, carrying forward whatever safe, uncommitted work is worth reusing.

The generalizable rule: model tier is a decision made at dispatch time, not a knob that can be turned on a live run. Plan which tier a task needs before launching it — a cheaper, faster model for well-specified, mechanical work that can merge automatically once green; the strongest available tier for conflict resolution, synthesis across ambiguous or contested findings, and anything requiring judgment under uncertainty. A coordinating or reviewing role should default to a lightweight channel for routine conversation, reserving a metered or premium path only for a genuine, otherwise-unblockable emergency.

A related discipline that held even under this kind of tier-juggling: work touching money handling, authentication, or access control kept its full independent review regardless of which tier built it or how the tiers were being reshuffled around it — mixing execution tiers to manage cost or speed must never be allowed to also relax which changes get an independent second look.
