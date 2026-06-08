---
title: CI must discover and run all test files, not a hand-maintained curated subset
date: 2026-06-07
category: guardrails
tags: [ci, gating, verify-dont-trust]
confidence: learned
source: private-work
---

A CI gate that runs a curated subset of test files does not protect against defects in new test files added in the same pull request. If a lane can merge with its own new tests never executed by CI, the green gate provides false confidence — it proves the old tests pass, not that the new ones do.

The fix: configure CI to discover and run all test files in the test directory rather than a hand-maintained list. Any new test file added to the directory is automatically included in the gate without configuration changes.

General lesson: a CI gate that doesn't run new tests is not a gate for new tests. Wildcard discovery is the standard; a curated list is a maintenance burden that silently degrades over time as new test files are added and forgotten.
