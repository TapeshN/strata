---
title: A background executor nested inside a background shell is orphaned when the shell exits — run it as a top-level background task
date: 2026-06-22
category: orchestration
tags: [lifecycle, autonomy, multi-agent]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Running a dispatch executor with a trailing ampersand inside a shell that is itself running in the background kills the executor when the outer shell exits. The dispatch envelope silently stays in the outbox as if never claimed, and no agent run is ever created — there is no error, only silence.

The fix is structural: the executor must be launched as a top-level background task, not nested inside another background process. A top-level background task runs independently of the shell that spawned it.

A related failure: an orphaned executor does not always die before reaching the dispatch step. If it has already posted to the remote before being killed, re-dispatching the same task fires a second agent on the same brief — two concurrent agents working the same spec. Before re-dispatching a task whose prior executor may have been orphaned, check whether a corresponding in-progress run or pull request already exists on the remote. If one does, work with it rather than firing a duplicate.

These two failure modes — silent-orphan (executor dies before posting) and double-fire (executor posts before dying) — bracket the same class: unverified dispatch state. The dispatch flow is only complete once the coordinator has confirmed the remote shows an active agent run.
