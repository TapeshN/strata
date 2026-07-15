---
title: A fail-soft fallback that recomputes from a pre-failure snapshot is itself a writer starting from stale state
date: 2026-07-13
category: guardrails
tags: [fail-soft, race-conditions, data-integrity, idempotency]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A fallback path was added so that if a multi-step process failed partway through, the system would degrade gracefully to a simpler, legacy flow instead of surfacing an error. The fallback recomputed its result from the state object as it existed at the moment the primary process was invoked, then persisted that result as a full write. The flaw: by the time the primary process failed, one or more steps inside it had already committed real, partial writes of their own — a counter bump, a note, a status change — to the very same record. Because the fallback started from the pre-failure snapshot rather than the record's current state, its own write silently rolled those partial writes back, discarding real work with no error and no trace.

The fix was to have the failure handler re-read the record fresh, through the same store the rest of the request uses, immediately before running the fallback computation, and to fall back to the original snapshot only if no live store is reachable at all. The generalizable rule: any fallback, retry, or compensating path that recomputes-and-persists must treat "what happened between the snapshot and the failure" as unknown. Re-read current state before that computation rather than trusting the value captured earlier in the request — and scope the failure handler narrowly enough that a genuine construction bug still fails loudly instead of quietly masquerading as a graceful degradation.
