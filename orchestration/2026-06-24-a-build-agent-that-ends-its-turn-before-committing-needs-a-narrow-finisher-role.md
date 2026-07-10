---
title: A build agent that ends its turn right after finishing work, before committing, needs a narrow finisher role
date: 2026-06-24
category: orchestration
tags: [subagents, lifecycle, roles]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

Across one working session, background build agents repeatedly finished the substantive work and then ended their turn one step early — narrating an intent to commit or open a pull request, but never actually executing it, leaving real, uncommitted changes with no artifact for a coordinator to pick up. This recurred multiple times in the same session, across different tasks, which rules out a one-off fluke.

The root cause is a property of the agent runtime's turn-ending behavior under long or complex builds, not a gap in the worker's instructions — the instructions already said to open a pull request. Telling an agent to "remember to commit" again does not reliably fix a runtime-level truncation.

Two mitigations proved effective in practice. First, dispatch a narrow, dedicated "finisher" whose stated first priority is committing and opening the pull request before any further verification — sequencing the side-effecting, hard-to-recover step ahead of the softer, repeatable verification step. Second, for a small remainder of unfinished work, a coordinator or supervising agent should simply hand-complete it rather than re-dispatching and risking the same truncation again. The general principle: when a class of agent reliably completes the risky, valuable part of a task but drops the low-risk finalization step, restructure the task so finalization happens first or is delegated to a role whose only job is finalization.
