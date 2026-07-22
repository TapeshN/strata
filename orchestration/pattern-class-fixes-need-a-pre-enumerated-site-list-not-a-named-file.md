---
title: A "fix every instance of this pattern" task dispatched to a weaker model needs a pre-enumerated site list, not just a named file
date: 2026-07-18
category: orchestration
tags: [subagents, roles, gating, determinism]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A recurring, characteristic failure mode of at least one class of coding-agent model: solid at fixing the obvious, first-glance instance of a pattern, and reliably INCOMPLETE at generalizing that fix to every other instance of the same pattern across a codebase — even when the task description explicitly names the file containing some of the remaining instances. Naming a file is not the same as naming every SITE within that file the pattern touches; a model with this failure mode reliably fixes the parts it happens to notice while scanning and misses the rest, including, in one instance, a client-facing site where the miss meant an internal error message leaked directly to an external user.

**The fix that reliably works is dispatch-time, not review-time:** for any "close every instance of this defect class" task routed to a model with this known limitation, have a reviewer or the coordinator EXHAUSTIVELY enumerate every site the pattern needs to touch BEFORE dispatching — an explicit checklist with no discovery left for the model to do — rather than trusting the model to find them all itself, however clearly the pattern is described in prose. If a full enumeration genuinely isn't feasible ahead of time (the pattern's extent is itself uncertain), that is itself a signal the task should route to a stronger model instead, one capable of doing its own reliable discovery, rather than being dispatched to the weaker model with an incomplete spec and hoped to work out.

**Keep a mandatory second review pass regardless of which model did the work.** In this case, an independent adversarial review caught the incompleteness on the very first attempt, and a second full sweep after the pre-enumerated re-dispatch caught nothing further — the two-reviewer floor is what actually closed the loop across every round, not any single model's output being trusted on its own.
