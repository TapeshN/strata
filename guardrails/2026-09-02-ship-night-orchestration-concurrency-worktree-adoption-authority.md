---
title: Ship-night orchestration — concurrency, worktree adoption, and a passive write that would have escalated authority
date: 2026-09-02
category: guardrails
tags: [fan-out, concurrency, worktree, external-workers, authority, consent]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

**1. Fan-out concurrency has to respect the one machine it's actually running on.** Running the same full, multi-thousand-test suite concurrently across nine parallel lanes on a single workstation pushed load average to roughly twenty times the core count, individual suite runs stretched past thirty minutes, and worker-level timeouts produced noise that masked which results were even real. The same shape of oversubscription was also the root cause of a separate resource-leak incident the same night. Rule: cap how many full-suite runs are allowed to run concurrently on one machine, either as a hard concurrency limit in the fan-out contract, or by pushing the full-suite run to CI and having local lanes run only their own focused subset of tests.

**2. A worktree that looks abandoned may belong to a paused, not dead, worker.** A different agent's in-progress workspace looked stalled, with no recent activity, and was treated as free to adopt: its uncommitted work was banked aside and the branch continued under new ownership. It turned out the original worker was simply paused between operator sessions and was about to resume and commit its own work. Rule: before adopting another worker's workspace, check whatever ledger tracks worker status, or ask, to distinguish "paused" from "dead," and once adopted, make sure the original owner is told not to resume it.

**3. A passive, replayable action must never be allowed to bind authority on someone's behalf.** A convenience shortcut — automatically stamping a confirmation record from whatever the live version of a pending request currently says, whenever a delayed or replayed confirmation arrives for it — looks harmless but is actually an authority escalation: the live request can have been edited by someone else after the original confirmation was given, and a replay carries no evidence that the confirming party agreed to the edited version. Rule: a passive or replayable signal may never bind authority by itself; only an explicit, visible act performed against the current state may.
