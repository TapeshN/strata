---
title: Gate test-only endpoints on an explicit opt-in flag, not on the build-mode environment variable
date: 2026-06-02
category: infra
tags: [gating, ci, release]
confidence: learned
source: private-work
---

A web framework's production build mode forces a specific environment variable value regardless of the CI job's configuration — conflating "production build" with "production environment." A test-only endpoint gated on that variable will be blocked in CI's production-build test run, preventing the disposable test database from being reset.

The safer design: gate destructive test-only routes on an explicit opt-in flag set only in CI, and hard-block on a separate deployment-environment signal (for example, a platform-provided flag that distinguishes a real production deployment from a CI production-build test). This is strictly safer: the live production database stays blocked, and an accidental local production-database run is also blocked.

General lesson: build mode and deployment environment are two different concepts. Never conflate them in security or access gates.
