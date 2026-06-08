---
title: Cucumber Before hooks with tag filters leak across all specs when session caching is enabled
date: 2026-06-03
category: infra
tags: [determinism, isolation, ci]
confidence: learned
source: private-work
---

In a Cypress + Cucumber preprocessor setup, `Before` hooks with tag filters are compiled into a global bundle for every spec. When session caching with cross-spec persistence is inside a `Before` hook, the preprocessor converts it to a `beforeEach` that fires for all specs regardless of the tag filter — causing authentication setup to run on specs that have no authentication requirement.

The workaround: move session and authentication setup inside the `Given` step that represents "I am authenticated." This provides per-scenario isolation and correct tag scoping — the setup only runs when the scenario explicitly requires it.

General lesson: do not put auth session setup inside `Before` hooks in a Cypress + Cucumber setup with cross-spec session caching enabled. Use `Given` steps instead.
