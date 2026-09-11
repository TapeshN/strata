---
title: A work brief's own acceptance line can be the defect — a worker stopping on that contract conflict is the right outcome, not a delay
date: 2026-09-05
category: orchestration
tags: [brief-authoring, contract-conflict, stop-and-report, review-discipline]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A written work brief's acceptance criteria stated a specific null-handling behavior for one field, in exact wording. An independent review before the change shipped further showed that exact wording would silently clear an existing value on every subsequent run of that same operation — and the worker executing the brief had already stopped and reported the conflict rather than picking a side. The same day, a separate brief named one integration target while the team's own higher-level policy said work of that type targets something else; another worker stopped on that contradiction too.

Before a brief is handed to a worker, its acceptance criteria deserve a reviewer's read — "what does satisfying this line literally do to existing data, or to the review gate" — and any brief naming a specific target, base, or default needs to be checked for agreement with the team's own higher-level policy, not just judged as internally consistent with itself. When a worker does encounter a brief whose literal acceptance criteria conflicts with reality or with a higher-level rule, stopping to surface that conflict rather than silently choosing an interpretation is the behavior worth rewarding. The fix for the cost of a stop is to shorten how quickly a conflict gets a ruling once raised, never to discourage a worker from raising one.
