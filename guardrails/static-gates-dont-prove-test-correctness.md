---
title: Static gates prove compilation and discovery, not that tests are correct
date: 2026-06-02
category: guardrails
tags: [gating, ci, evals, verify-dont-trust]
confidence: learned
source: private-work
---

A suite of tests that all pass static gates (type check, lint, list discovery) can still contain dozens of assertion errors the first time it runs against a live system. Common failure modes found: an unauthenticated fixture making calls that require authentication; a state-reset fixture not running because the fixture chain is incomplete; a guard test that pins current buggy behavior rather than intended behavior; and a framework config error that only surfaces during an actual live run.

Static gates prove that a suite compiles and that the test runner can discover its files. They do not prove that the tests execute correctly, that fixtures are wired as intended, or that assertions match the system's real behavior.

General lesson: a suite is "done" when it runs live against the real system and its failures have been triaged — not when it passes static analysis. Budget for at least one fix cycle between the first live run and declaring the suite ready.
