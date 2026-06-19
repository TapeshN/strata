---
title: "Is main green?" — the top of `gh run list` lies two ways; read the PR-gate CI and drill a red scheduled run to its failed STEP
date: 2026-06-13
category: guardrails
tags: [ci-triage, green-verification, scheduled-workflow, report-step-vs-test, run-list-noise]
confidence: learned
source: private-work
---

a CI-health verdict from the top of the run list is unreliable — (1) filter out skipped/issue_comment bot runs; (2) confirm whether validation runs on push or only at the PR gate; (3) for any red, inspect the failed JOB/STEP before calling it a regression. Class-sibling of [[reference_gha_ci_gotchas]] (mergeStateStatus CLEAN≠green).
