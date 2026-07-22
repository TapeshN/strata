---
title: When a product intentionally changes, rewrite the content-witness test to the new truth — never weaken or delete it
date: 2026-07-21
category: evals
tags: [testing, evals, regression, intent]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A test suite that pins exact product content — a specific title, a specific label, a specific set of visible items — will correctly go red the moment the product deliberately changes that content, potentially multiple times in the same session if the product changes multiple times. The skill this requires is telling apart "the test caught a real regression" from "the test is pinned to a superseded version of the truth" — and the two look identical from the failure message alone.

**The rule:** when a test fails because the product genuinely, intentionally changed, the correct response is to rewrite the assertion to the new truth (and, where useful, add the inverse assertion — explicitly asserting the OLD content is now absent) — never to weaken the assertion or delete the test to make it pass. A suite maintained this way keeps its full original count of passing, meaningful checks through every intentional product change, rather than slowly eroding into decoration.
