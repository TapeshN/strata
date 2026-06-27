---
title: Time-based task IDs at second granularity collide under burst writes; two tasks in the same second silently become one
date: 2026-06-16
category: infra
tags: [idempotency, dispatch, determinism, tooling]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A task-ID scheme derived from a timestamp at second granularity fails silently when two tasks are written in the same second. The second write produces the same ID and therefore the same output filename; it overwrites the first. The caller sees no error, the outbox shows one file where two were expected, and the dropped task is unrecoverable.

This is a structural flaw, not a timing edge case. Any pipeline that fires multiple tasks programmatically in a loop can produce same-second writes. The failure is invisible because the file-write itself succeeds — only the count reveals it.

Three fixes address the root differently. The most defensive is to use an ID scheme with sufficient entropy for bursts: a millisecond timestamp with a short random suffix, or a UUID. The simplest operational workaround is for the caller to pass an explicit, unique ID per task rather than relying on auto-generation. The safest write-path guard is for the ID generator to refuse to overwrite an existing file without an explicit flag, surfacing the collision before it silently deletes work.

The broader principle: any auto-generated ID used as a filename or a queue key must be collision-resistant under the actual dispatch pattern, not under single-task assumptions. Verify the outbox file count equals the expected envelope count before consuming.
