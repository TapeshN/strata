---
title: Build the database test harness before the fixes it's meant to validate, not after
date: 2026-07-21
category: evals
tags: [testing, evals, postgres, harness-design]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A codebase whose automated test suite had never touched a real database meant every "fix" for a database-dependent bug could only be witnessed by a mock that shares the exact same assumption the bug depended on — so the fix looked verified while nothing had actually proven the real database behaves as expected. The missing piece wasn't the fixes; it was the harness that could run tests against a real, disposable database in the first place, and a platform-specific environment quirk (a locale/encoding default that crashes a throwaway local database process) was the actual blocker preventing that harness from existing.

**The rule:** when a batch of fixes is meant to stand on real-database behavior, treat building (or repairing) the real-database test harness as the prerequisite work, not a nice-to-have alongside the fixes — diagnose and resolve whatever environment blocker is preventing a real, disposable database in your test environment FIRST, because every fix built on top of a still-missing harness inherits the same unproven assumption.
