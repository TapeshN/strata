---
title: A reviewed, locally-green test suite can still never run in CI
date: 2026-08-25
category: guardrails
tags: [ci, gating, review, suites-wired]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A pull request added a substantial new directory of tests, was reviewed carefully, and its author ran the suite locally to confirm every test passed before merging. Continuous integration on that same pull request was green — but only because nothing in the CI configuration actually invoked that directory; the new tests had never been executed by CI at all, reviewed-green and merged on the strength of a local run alone. The gap surfaced only when a later, unrelated change happened to add a structural check requiring that every top-level test directory have a corresponding CI step, and that check correctly flagged the earlier merge's omission.

The general failure: a code-review loop's "I ran the tests and they passed" and a CI system's "these are the steps that run on every push" are two independent mechanisms, and nothing automatically keeps them in sync. A new test directory can be reviewed, run once by a human, and merged clean — and then never execute again, silently, indefinitely, because CI's own step list was never updated to include it. The fix is a structural check, not a reviewing habit: something that enumerates every test directory in the repository and fails if any of them has no corresponding entry in the CI configuration. Any review process for a pull request that adds a new test directory should treat "does CI actually run this" as a distinct, explicit question from "did the author's local run pass" — the two can and do diverge.
