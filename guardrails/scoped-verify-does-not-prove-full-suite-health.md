---
title: A tag-scoped or spec-scoped verify proves only that scope — not full suite health
date: 2026-06-25
category: guardrails
tags: [testing, scoped-verify, false-green, full-suite, witness-scope]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A test run filtered to a specific tag, spec file, or scenario subset reports green for the matching scenarios and marks everything else as pending. Pending is not passing. A scoped green run says nothing about the health of any scenario outside the filter — but it reads, superficially, like whole-suite health.

The failure pattern: a single failing test is fixed, the fix is verified by running only the scenarios that include the fixed test, and the result is reported as "the suite is green." A subsequent full run exposes a larger set of pre-existing failures that the scoped run never executed.

The claim "suite green" is only valid when the full, unfiltered suite ran and passed. If a scoped run is what actually ran, the correct report is "scenarios X and Y verified; the remaining suite was not exercised this run."

A practical note on triage efficiency: failure screenshots saved from a full run are often faster than re-running individual scenarios to diagnose why they are red. A screenshot proves whether the failure is a test-side selector problem or a genuine application bug without requiring another round-trip through the test harness.

The broader principle: every verification claim must name its scope. A claim with a scope narrower than the deliverable is not a verification of the deliverable — it is a verification of a subset. Name the subset explicitly, and run the full scope before asserting the deliverable is ready.
