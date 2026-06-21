---
title: A per-IP rate limiter and a parallel test suite are structurally incompatible — bypass requires an opt-in, not resets
date: 2026-06-10
category: infra
tags: [evals, gating, ci, determinism, isolation]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A per-IP rate limiter counts requests from a shared IP address. An end-to-end test suite run in parallel spawns multiple workers, each making its own requests from the same IP. The combined request rate of the workers will reliably breach limits that a single serial run stays well within. Database reset procedures between tests do not help: the counter lives in the rate-limiter, not in the test database, and cannot be cleared by a test.

The fix is structural: the test environment must be able to opt out of the rate limiter's enforcement through an explicit signal (a server-side flag, a header, a config value) that is set only when running under test. This is architecturally different from configuring a generous limit — a generous limit still fires if enough parallel workers accumulate — and different from resetting between tests.

The opt-in design has an important constraint: at least one test must still exercise the real rate-limiting behavior with the bypass disabled, so the rate limiter is proven to work in production. The bypass is a test-infrastructure affordance, not a license to omit coverage.

An adjacent case where this compounds: a test environment that runs on a shared network address rather than a per-test address (for example, behind a corporate NAT or in a shared CI pool) will see the cumulative request rate of all tests running on that address, not just the current test run. This makes rate-limit thresholds that are calibrated for individual users structurally wrong for any environment where many users share an egress IP.

General lesson: when a test suite produces flaky failures whose rate scales with the degree of parallelism, the first hypothesis should be a shared counter somewhere in the system — rate limiter, audit log, event queue — that aggregates across workers. The fix is always structural: bypass the aggregation for test runs, not a reduction in parallelism.
