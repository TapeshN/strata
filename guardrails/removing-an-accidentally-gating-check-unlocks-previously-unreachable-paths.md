---
title: Removing an accidentally-gating check unlocks previously-unreachable code paths — re-audit their invariants
date: 2026-07-19
category: guardrails
tags: [security, code-review, invariant-checking, refactoring]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A bug fix removed an authorization check that had been applied to the wrong scope, accidentally making one code path completely unreachable. Once that mis-applied check was removed, the path became live for the first time — and an independent security review found it had a real race condition and was missing a sibling existence check that every other caller of the same primitive already had. Nobody had ever exercised those invariants because the path had never actually run.

**The rule:** when a fix removes a check that was silently blocking a whole path (even by accident), treat everything downstream of that path as newly-live code, not as already-tested code that merely regained access. Re-audit its races, its idempotency, and whether it's missing defense-in-depth checks that sibling callers of the same shared primitive already carry — a completeness gate scoped by a narrow parameter shape can also miss a privileged case laundered through a different shape, so add cheap checks to the shared primitive itself, not just the caller.
