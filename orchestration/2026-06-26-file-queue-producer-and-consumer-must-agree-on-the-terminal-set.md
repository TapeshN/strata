---
title: A file queue's producer and consumer must share one definition of terminal vs retryable status
date: 2026-06-26
category: orchestration
tags: [dispatch, idempotency, eventually-consistent, contracts, lifecycle]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When a file-based queue passes work between a producer and a reconciler (janitor, archiver, or retry manager), both sides must agree on exactly which status values mark a task as done versus retryable. A mismatch strands work permanently or causes duplicate dispatch.

The failure mode is subtle: a status that means "could not run yet" (a transient SKIP) can look like a terminal result if the reconciler was written at a time when SKIP was rare or unexpected. If the producer writes a SKIP result and the consumer treats any result as terminal, the task is now un-reclaimable — it sits in the outbox looking done but never was. Conversely, if the reconciler treats SKIP as retryable but the claimer treats it as done, the same task is reclaimable and dispatched twice.

The compounding trap is silence: a "no-op" that reads as success ("outbox empty, processed 0") can mask both failure modes. A reconciler that ran, found nothing to do, and reported success looks identical to a reconciler pointed at the wrong directory. The fix is for a no-op reconciler to emit the reason loudly, not silently return 0.

To prevent this class: (1) define the terminal set as a constant shared by both producer and consumer, enforced by tests that assert both sides agree; (2) distinguish "could not run" (retryable) from "ran and produced an outcome" (terminal); (3) run reconciliation automatically on a schedule or session start, not only when the operator remembers to invoke it; (4) a reconciler's default path must point at the real data directory, verified by running it and checking the count changes.
