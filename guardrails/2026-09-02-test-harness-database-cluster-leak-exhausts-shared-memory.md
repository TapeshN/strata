---
title: A test harness that spawns one throwaway database cluster per test file can exhaust host resources when a worker process dies mid-run
date: 2026-09-02
category: guardrails
tags: [test-harness, postgres, leaked-process, resource-exhaustion, macos]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A test suite that isolates each test file by spinning up its own real database cluster (rather than mocking) gets stronger evidence, but every cluster is an OS-level resource — a process, shared-memory segments, file handles — and those are only released if the owning test process reaches its own cleanup step. During a large parallel run (many lanes each running a full suite concurrently), a coordinating process was killed before its children finished, and every spawned cluster was orphaned: no parent left to run the cleanup. Hours later, the host had accumulated well over a hundred orphaned database processes, every shared-memory slot the OS allows was consumed, and a completely unrelated later test run failed to even start a new cluster — with an OS-level error that reads like a disk problem, not a test-harness one.

General rule: a test harness that allocates any OS-level resource per test file (a process, a shared-memory segment, a socket) needs three things, not one. First, a preflight check before allocating a new resource that counts how many of that resource are already alive and refuses with a named remedy when near the ceiling, rather than failing opaquely at the OS call. Second, a process-exit/signal handler that tears its own resource down even on an abnormal exit, not only on the happy-path cleanup call. Third, a separate, manually-triggered sweep that can find and reclaim resources whose owning process is provably dead — not on a timer, since a scheduled reaper can race a resource that is still mid-use. "The lane prompt tells every worker to clean up after itself" is not a mechanism; it only works when the worker survives to run its own cleanup, and the failure mode that matters is exactly the one where it doesn't.
