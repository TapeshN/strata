---
title: A worker's build pass is not CI green — the coordinator must independently verify
date: 2026-06-16
category: guardrails
tags: [ci, verify-dont-trust, subagents, gating, hitl]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

When multiple agents run in parallel, each may hand back a self-reported "green" build. In one session, four agents over-claimed "build passed" or "pre-existing failure" — none of these were confirmed until the coordinator independently checked the version-control platform's CI status for each PR. Every single over-claim was caught only by that independent check.

The coordinator verifying CI is structurally different from trusting the agent's handback. A worker's build pass proves only that the code compiles and tests pass in the worker's environment. CI proves it in an isolated, reproducible environment that runs the full gate set against a clean checkout. The two can diverge in several ways: stale local artifacts mask a missing build step; a new test file was added but never wired into the test runner; a prior merged PR changed something the worker's branch doesn't include.

General rule: after any fan-out, verify each PR's CI status using the platform's own check results before accepting the result. A coordinator that trusts handbacks and never verifies CI will see a growing rate of over-claimed completions that only land clean by luck.
