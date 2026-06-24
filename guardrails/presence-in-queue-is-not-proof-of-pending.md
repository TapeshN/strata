---
title: Presence in a queue is not proof of pending — reconcile against the completion ledger before calling work stale
date: 2026-06-24
category: guardrails
tags: [verify-dont-trust, lifecycle, idempotency]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When a task system has a manual or deferred archival step, completed dispatches linger in the pending queue looking unfinished. Treating presence-in-queue as "pending" — without intersecting against the completion ledger — produces a false stale count. Work that was done appears dropped.

The failure mode is asymmetric: the coordinator calls out "stale" work that the operator knows shipped, which erodes trust and triggers unnecessary re-dispatches.

**The rule:** before labeling any work stale or dropped, reconcile the pending queue against the completion ledger (whatever records that the work landed — inbox results, merge records, PR status). "Still in the outbox" is not "not done" when the archival step is manual.

**The structural fix:** any task system that can accumulate this gap should have an automated reconciliation step — a janitor process that moves completed-but-un-archived items to a done state on a schedule. Until that is wired, the coordinator must do the reconciliation by hand before reporting queue state.

The underlying lesson applies beyond task queues: any assertion about what remains to be done must be grounded in a read of the completion record, not only the pending record.
