---
title: Four failure modes that break a per-user cost cap even when the happy path looks correct
date: 2026-07-16
category: guardrails
tags: [cost, idempotency, gating]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A review of a per-user spend cap surfaced four distinct, generalizable failure modes; any one of them alone lets usage exceed the intended limit even though the primary code path reads correctly.

**Check-then-act is a race, not a guarantee.** A guard that reads current usage, decides it is under the cap, and only records the new spend after an expensive downstream call completes leaves an open window equal to that call's entire latency. Concurrent requests arriving inside that window all read the same "under cap" state and all proceed — the cap ends up enforced in wall-clock terms, not in request-count terms. The fix is an atomic reserve at decision time (a single conditional update that only succeeds while the count is still under the limit, or an explicit row lock) rather than read-decide-write-later.

**A fire-and-forget ledger write is only as durable as the runtime's teardown guarantee.** An unawaited background write to a spend ledger can be silently dropped by a serverless or short-lived execution environment that tears the process down as soon as the visible response is sent, before the background write lands. Detached recording work needs an explicit "keep running after response" primitive, not a bare unawaited call.

**Audit both the success and the error path for recording.** It is common for the happy path to correctly wrap spend-recording in a guaranteed-to-run block while a sibling error path records nothing on failure — silently under-counting exactly the requests most likely to be retried by a caller, which compounds the leak.

**A dedup or rate-limit fix applied to one event type does not automatically cover a sibling event type.** When two related event types share a code family (a "cap exceeded" warning and a "circuit breaker tripped" alert, for instance), a dedup fix shipped for one and not the other leaves the unfixed sibling free to flood downstream consumers under entirely ordinary, non-adversarial use.

These four generalize beyond cost caps to any per-actor rate or resource limit: check-then-act needs atomicity, recording needs a durability guarantee independent of the runtime's teardown behavior, both outcome paths need auditing, and a fix to one event type in a family needs to be checked against every sibling in that family.
