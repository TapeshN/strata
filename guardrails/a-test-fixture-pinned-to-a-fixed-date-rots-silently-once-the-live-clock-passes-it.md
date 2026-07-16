---
title: A test fixture pinned to a fixed date rots silently once the live clock passes it
date: 2026-07-16
category: guardrails
tags: [determinism, ci, reproducibility]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A test fixture that seeds evidence or spend data at a hardcoded "current" date, checked against code that reads the real system clock, is a time bomb: it passes at the moment it is written and turns red the instant the code's clock-relative window (a freshness check, a dark-window check, a rolling spend window) ages past that fixed timestamp. This class of failure tends to hit multiple tests at once, because the same easy-looking shortcut — "just hardcode today's date" — gets copied into sibling test files by different authors on different days, so several unrelated tests can rot on the exact same calendar boundary and block an unrelated batch of work all at the same time.

Prevention: any fixture whose code-under-test reads a live clock should stamp its timestamps relative to the actual current time (e.g. "now minus two hours") rather than a literal date, unless the code path being tested explicitly supports a frozen or injected clock — in which case the fixture should use that override and say so explicitly. A lightweight preflight check that flags a hardcoded current-year date literal in a test file, unless the line carries an explicit "frozen clock, safe" marker, catches the whole class before it ships rather than after it silently expires.
