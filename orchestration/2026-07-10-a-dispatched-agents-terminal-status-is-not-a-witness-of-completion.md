---
title: A dispatched agent's own terminal status is not a witness of completion — verify against artifacts on the remote
date: 2026-07-10
category: orchestration
tags: [autonomy, subagents, verify-dont-trust, idempotency, dispatch]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A remote build dispatch returned a terminal "finished" status with no summary text, no pull request, and no branch pushed to the remote. The orchestrating pipeline that received this result logged only a soft warning and moved on, having spent dispatch budget for zero durable output. The failure was named as a distinct class — a "silent no-op" — and the re-dispatch of the same task carried an explicit added instruction: a run that ends without any commits is a failure, not a success, regardless of what its own status field says. That framing produced a real branch on the retry.

The structural problem is that a dispatched agent's status field is self-reported: it reflects what the agent believes about its own turn, which can be truthful about intent while corresponding to nothing durable having actually happened. A status of "finished" or "success" answers the question "did the agent's own process exit cleanly," not the question "did this task produce the artifact it was dispatched to produce." Those are different questions, and only the second one is the one the orchestrating system actually needs answered before it counts the dispatch as complete or moves budget/attention elsewhere.

The generalizable rule: a dispatched task's completion must be witnessed by evidence that exists independently of the dispatched agent's own reporting — a pushed branch, a created commit, an opened pull request, a file that now exists at the expected path — never by the agent's self-reported terminal status alone. Any dispatch pipeline should check for this class of artifact before accepting a "finished" result as genuine completion, and a repeated no-op from the same task shape is itself a signal worth recording and feeding back into future dispatch instructions for that shape of task.
