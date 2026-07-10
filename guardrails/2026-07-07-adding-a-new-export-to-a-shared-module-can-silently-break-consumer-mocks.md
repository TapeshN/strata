---
title: Adding a new export to a shared module can silently break every consumer test that fully mocks it
date: 2026-07-07
category: guardrails
tags: [testing, ci, determinism]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Routing existing code through a new function added to a shared module's public surface seems like a safe, additive change, and a per-file type-check confirms it compiles cleanly. But any test elsewhere in the codebase that replaces that shared module with a complete, hand-written mock (rather than a partial mock or the real module) will now fail at runtime the moment the migrated code path executes, because the mock doesn't define the new export — and this failure is invisible to a type-checker, since it's a mock-resolution failure at test-run time, not a type error. Only running the FULL test suite surfaces it; checking individual files one at a time, however diligently, will not.

The general rule: adding a symbol to a shared module's public surface and routing live code through it has a blast radius equal to every test that fully replaces that module with a mock — before declaring such a change done, run the complete test suite, not a per-file type-check and not a targeted subset.

A related, separate lesson about a specific implementation choice: for a route or function that branches behavior between two different privilege tiers (say, an admin path and a client path), representing the authorization check as something that returns an explicit result value describing the outcome (rather than something that throws an exception on failure) is structurally safer for a shared/mixed code path. With a result-value approach, a branch that forgets to check the result and act on it simply has no valid data to proceed with — a compile error. With a throwing approach, a branch that forgets to catch the exception can let the failure escape uncaught, or — worse — a misplaced catch could swallow the denial and let execution continue as if authorized.
