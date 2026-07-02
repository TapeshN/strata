---
title: An idempotency marker written before its guarded effect, without wrapping both in one transaction, can permanently poison retries after a transient failure
date: 2026-07-02
category: guardrails
tags: [idempotency, contracts, determinism]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A webhook handler inserted an event's unique identifier into an idempotency ledger first, then applied the effect that identifier was meant to guard, as two separate, non-transactional writes. An independent review flagged this as high severity: if the process fails between the two writes (a transient database error, a crash), the identifier is now permanently marked "processed" even though the real effect never happened. Every subsequent retry of that same event — including legitimate ones from an upstream system that automatically retries failed deliveries — short-circuits as a duplicate and is silently dropped, with no recovery path.

The general pattern: an idempotency marker and the effect it's meant to deduplicate must be atomic with each other. Writing the marker first is only safe when both the marker and the effect live inside a single transaction that commits or rolls back together — never as two independent statements where a failure between them can leave the marker true and the effect false.

This generalizes to any consumer of an at-least-once delivery system (webhooks, queues, retried external callbacks): the fix is to wrap the marker-write and the effect together in one transaction, so a retried already-processed event can short-circuit safely via a read, while a genuine failure rolls both back cleanly and leaves the event retryable. Notably, the author's own tests validated the original, subtly-broken shape — only a reviewer explicitly looking for cross-write failure modes caught it, which is the case for an independent review existing as a distinct step from the author's own testing.
