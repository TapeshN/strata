---
title: A bounded-attempt counter stored inside a container a sibling write can overwrite is not a counter
date: 2026-07-13
category: guardrails
tags: [concurrency, race-conditions, idempotency, data-integrity]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A team needed to cap how many times a particular multi-step interaction could run for a given record, and chose to store that count as a field inside an existing JSON blob column rather than add a new database column — a reasonable-looking way to avoid a migration. The same JSON blob, however, was also the payload that an entirely separate, much more frequent write path (an ordinary state save that ran on every routine turn of the interaction) read, mutated for unrelated reasons, and wrote back in full. Because that frequent path did a read-modify-write of the whole blob rather than a targeted update of one field, a request that was actively updating the blob for unrelated reasons could race the counter's own write and silently reset it — re-opening exactly the abuse case the cap existed to close, under completely ordinary concurrent use, with no error or warning anywhere.

The fix was to give the counter its own dedicated column, bumped only through an atomic increment operation, and to deliberately keep that column out of the record type that the frequent whole-blob writer operates on — so that writer cannot touch it even by accident. The generalizable rule: before adding any bounded-attempt, rate, or round counter to a system, enumerate every code path that writes the container the counter would live in. If any of those paths does a read-modify-write or whole-object replacement of that container, the counter needs a separate, atomically-updated field — never a nested value inside something a sibling path can clobber. Avoiding a schema change is never worth a counter that a concurrent, completely unrelated write can silently roll back.
