---
title: A success flag set when a precondition is met, rather than when the operation completes, misreports on the failure path
date: 2026-07-01
category: guardrails
tags: [security, determinism, contracts, testing]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A function that resolves a resource and then uses it — for example, finding a credential and then making a call with it — assigned an outcome flag ("this used the resolved resource") at the moment the resource was found, before the operation that actually uses it had run. When that subsequent operation then failed for an unrelated reason (a network error, a bad response), execution fell into a fallback path that still carried the earlier flag value, so a result that never completed the operation it claimed to describe reported as if it had.

The general trap: in any two-phase flow — resolve a resource, then perform an operation with it — a flag meaning "X happened" must only be set on the success exit of the code that actually performs X, never inherited from an earlier step where only a precondition for X was satisfied. If anything fallible sits between "resource resolved" and "function returns" (a network call, a parse step, any I/O), the flag is only trustworthy when it is re-asserted on every individual return path rather than carried forward from a shared variable.

The fix is to trace every such flag's assignment site relative to everything that can still fail after that assignment, and to hardcode the honest value on every fallback/error return rather than let it inherit. A regression test that forces the fallible step to fail and asserts the flag's value on that path is the concrete proof the fix holds — and is meaningfully different from a test that only exercises the happy path, since a flag bug like this is invisible unless the failure path is specifically exercised.
