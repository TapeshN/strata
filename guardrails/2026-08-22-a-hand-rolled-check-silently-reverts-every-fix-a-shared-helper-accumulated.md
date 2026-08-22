---
title: A hand-rolled version of a check silently reverts every fix its shared helper accumulated
date: 2026-08-22
category: guardrails
tags: [security, tests, twin-implementation]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A new queue implemented its own inline version of an ownership-fencing check: it spread a fencing token into the query's filter conditions only when the token was present. Every other queue in the system used a shared helper function for the identical check — one that had, over time, accumulated the correct behavior of treating an omitted token as a refusal rather than a pass-through. The hand-rolled version silently reintroduced the exact gap the shared helper had been built to close, because "add the value if present" is not the same rule as "require the value, and refuse if it's missing."

General rule: when a new call site needs a check that already exists as a shared helper elsewhere in the codebase, reuse the helper rather than reimplementing the check inline — a hand-rolled reimplementation is a silent regression risk, not a shortcut. And test the omitted/missing-value case explicitly, not just the wrong-value case; a check that only validates "if present, is it correct" says nothing about what happens when the value is simply absent.
