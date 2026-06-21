---
title: An unconditional skip that documents a missing capability becomes a silent lie when the capability ships — flip it in the same change
date: 2026-06-16
category: guardrails
tags: [testing, verify-dont-trust, evals, lifecycle]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A test written to skip unconditionally when a precondition is absent (a scheduled task not installed, a feature not shipped, a dependency not present) is correct at the time it is written. It becomes incorrect the moment the precondition is satisfied, because the skip condition no longer reflects reality — the test silently passes while executing nothing, and its name continues to describe an absent behavior that now exists.

Two instances were found in the same audit:

- A scheduled task had been installed and was confirmed firing via the scheduler. Two tests unconditionally skipped "awaiting operator install" — the skip was never flipped when the task shipped, so both tests had been green-but-hollow for days.
- A gap-documenting test was written to skip when a guard was absent, then the same pull request added the guard. The skip branch never fires, the test passes with zero assertions, and the name reads as "gap documented" when the gap is closed.

The first case is harder to catch: the capability ships in a different lane than the test. The prevention reflex for this case is: when landing any capability (installing a task, shipping a feature, adding a guard), grep the test suite for unconditional `skip`, `skipTest`, or `xtest` on the capability's name or related identifier, and flip each one to a positive assertion of the new behavior.

The second case should be caught by the author or the reviewer in the same pull request that closes the gap — a test asserting absence and a change asserting presence cannot coexist without one of them being wrong.

A broader check applies at any point where a "this doesn't exist yet" claim was written — audit those claims against the current live state before trusting them.
