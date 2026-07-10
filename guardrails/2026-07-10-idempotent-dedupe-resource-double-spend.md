---
title: A resource debit before an idempotent call must be refunded on a dedupe hit
date: 2026-07-10
category: guardrails
tags: [idempotency, resource-accounting, double-spend, rollback, code-review, concurrency]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

**The rule:** if a function both spends a limited or billable resource *and then* calls an idempotent operation, it must branch on whether that operation actually did new work versus just returned an existing result — and it must compensate (refund/rollback) on the "already existed" branch. An idempotent call that only returns an identifier, with no created-vs-existing signal, silently invites this bug: "I got an id back" gets treated as "the work was done," even when the id points at work that was already in flight or already finished.

**What happened:** A queue-style enqueue function deduplicated "one live job per unit of work" and returned just an id — nothing else. Its caller had already unconditionally debited one unit of a limited entitlement before calling enqueue, then treated getting an id back as proof the work had started. When the dedupe logic hit an existing in-flight job — because of a resumed session or a double-click — the caller still kept the debit, even though no new work was actually created. There was no rollback path for this case, because the only rollback that existed was triggered by a thrown exception, and a dedupe hit is a normal, non-throwing return. The bug was caught by an independent review focused specifically on financial/resource-accounting correctness, not by the original implementation or its tests. The fix was to change the idempotent function's return shape to include an explicit created-vs-existing flag, and make the caller refund the entitlement whenever that flag says "existing."

**How to apply:** Any time you write or review a function that spends a scarce/billable resource before calling something idempotent (a dedupe, an upsert, a get-or-create), check the return contract of that idempotent call. If it collapses "created" and "already existed" into the same shape (just an id, just a boolean success), that's a red flag — add an explicit created/existing discriminator and make every caller that pre-spent a resource branch on it and refund on the "existing" case. Don't rely on exception-based rollback alone; a dedupe hit is a normal control-flow path, not an error, and needs its own compensation logic.
