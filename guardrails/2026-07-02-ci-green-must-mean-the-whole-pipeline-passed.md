---
title: CI-green must mean the whole pipeline passed, not a hand-picked subset
date: 2026-07-02
category: guardrails
tags: [ci, verify-then-merge, testing]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Two unrelated incidents in the same review cycle both trace back to "verifying against a subset of the real gate is not the same as verifying against the real gate."

In the first, a pull request went green against its unit and integration test suites but turned red on a distinct step later in the same CI pipeline — an automated scan step that checks for accidentally-committed secret-shaped literals — because the reviewer had run the test suites but not the full pipeline including that earlier-stage scan. The scan's finding was legitimate (a real-shaped literal existing on purpose as a test fixture), so the fix was to explicitly allowlist that specific case with a documented reason rather than obscure it — but the deeper lesson is that "the tests pass" and "the pipeline is green" are different claims, and only the second one is the actual merge bar.

In the second, a shared UI component that had shipped and been imported many times finally hit its first-ever automated rendering test, and immediately threw a runtime error: it used a UI templating syntax without the corresponding import that syntax depends on at runtime. Every previous use of that component had been exercised only by type-checking or by manual visual inspection, neither of which executes the component's actual runtime code path — so the missing import sat latent for a long time, invisible to every gate except one that actually renders the component.

General rule: verify against the entire CI pipeline (every distinct check it runs), not a hand-picked subset — a pass on unit tests while a later pipeline stage would fail is a false green. And any shared UI primitive that has type-checked cleanly but never actually been rendered by an automated test carries a standing risk of a latent runtime-only defect; the first real render test is often what surfaces it.
