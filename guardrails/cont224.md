---
title: "Three PRs in one night were green on a check that did not measure what the PR was for"
date: 2026-09-06
category: guardrails
tags: ["gate-scope", "positive-control", "ci-lint-gap", "witness-vs-check", "doctrine-16"]
confidence: learned
source: private-work
---

before accepting a PR's CI as the witness for its PURPOSE, read the workflow and confirm the gate that would catch this PR's failure mode actually runs. A check named after a repo is not a check named after a claim.

the positive control is the cheap half and the one that gets skipped — a suppression that silences nothing, a lint step scoped to no files, and a misresolved eslint config ALL exit 0. Prove the gate fails when it should before believing it passing means anything.

a green check answers "did the configured job succeed", never "is the thing this PR claims true". Those coincide only when someone deliberately wired them together, and that wiring is exactly what nobody checks.
