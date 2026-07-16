---
title: A client-side timeout abandons a slow query without cancelling it
date: 2026-07-16
category: guardrails
tags: [deadline, database, concurrency, resource-leak]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A common deadline pattern races a database call against a timer and rejects if the timer wins. That pattern bounds how long the caller waits, but it does not touch the underlying query: the database keeps executing it and the connection stays checked out of the pool for as long as the query actually takes. Under sustained slowness, every "timed-out" request still leaks a live connection, which shrinks the pool further and makes the next request more likely to time out too — the deadline meant to contain the problem quietly deepens it instead.

The generalizable lesson: a race-based timeout is an abandon, not a cancel. It changes what the calling code observes without changing what the database is doing. A deadline that must actually bound resource usage — not just caller-perceived latency — needs a mechanism the database itself will honor, such as a statement-level timeout scoped to the query or transaction, or a client driver call that genuinely cancels the in-flight query. When reviewing a newly added deadline, check which side of the boundary it operates on: does it stop the work, or does it just stop waiting for the work?
