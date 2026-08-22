---
title: A same-day forensic pass found a kickoff brief's own "current state" observations already stale within hours — verify every inherited fact before planning against it
date: 2026-08-21
category: guardrails
tags: [verification, stale-premise, planning]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A morning planning brief described a set of specific facts about the current state of a system —
how far one component was behind another, which process held a particular lock, the state of a
particular environment, how many items were open, and which checkouts shared a given commit. By
the same evening, every single one of those facts had changed: the drift figure was now zero, the
lock was held by a different process, the environment reflected the latest build, the item count
and commit distribution had both shifted substantially. Planning against ANY of the original facts
would have produced entirely wrong next steps — work to fix an already-fixed thing, or a rebuild of
something that was already current.

The generalizable rule: every fact inherited from a kickoff brief or handoff document deserves a
fresh, timestamped re-verification against the live system (not the document) before it becomes
the basis for a plan — and the plan itself should record an explicit "what changed since the brief
was written" note, so the reader sees the delta rather than assuming the brief is still current. A
narrative fact without an accompanying live re-check is a hypothesis, not a fact.
