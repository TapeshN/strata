---
title: Circular Imports Crash Production Builds While Type Checks and Tests Stay Green
date: 2026-07-06
category: infra
tags: [circular-import, next-build, build-cache, tsc-blindspot, verification]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A value-level circular import between two modules can crash `next build` during page-data collection with an "Cannot access X before initialization" error — even though `tsc` and a full test suite (vitest, Jest, etc.) both pass cleanly. The bundler's static analysis of page/route dependency graphs is a different code path than the type checker or the test runner, and it is the only one of the three that will actually surface this class of bug.

What happened: one module imported a helper (e.g. a label-formatting function) from a second module, while that second module imported shared constants back from the first — a value-level import cycle, not a type-only one. TypeScript compiled fine because type-only cycles are tolerated; the test suite (hundreds of tests) passed because individual unit tests didn't exercise the specific initialization order the bundler uses when collecting page data for a route. Only running the actual production build against the affected route revealed the crash. To make it worse, the deployed environment's build cache had a stale, cached copy of the working page data from before the cycle was introduced, so the bug only manifested on a cache-miss (e.g. an unrelated change that happened to invalidate that cache entry) — meaning it could sit dormant in `main` for a while and then break with what looked like an unrelated deploy.

How to apply: if a bug only appears in a full production build and neither the type checker nor the test suite catches it, suspect a circular import or a module-initialization-order issue before anything else — treat `next build` (or equivalent bundler build) as its own required verification step, not a step implied by green tsc/tests. The structural fix is to hoist any constants or helpers that two modules mutually depend on into a third, leaf-level module that both import from, breaking the cycle entirely rather than reordering imports.
