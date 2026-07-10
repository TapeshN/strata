---
title: A test that derives "now" from a different clock than the code under test can hide a real bug
date: 2026-07-10
category: guardrails
tags: [testing, determinism, ci]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

An automated test computed today's date using one method (the system's UTC clock) while the actual code it was testing computed today's date differently — by parsing dates out of entries that had been written in local time. In a timezone that sits behind UTC, there is a multi-hour window every evening, after local midnight has not yet arrived but UTC midnight has already passed, where these two methods disagree about what day it is. During exactly that window, an entry authored "right now" would be miscounted as belonging to yesterday.

The critical detail is that a continuous-integration runner conventionally operates in UTC, so on that runner the test's clock and the code's clock always agree — the test passed every single time in that environment, and only ever failed on an actual developer machine set to a different local timezone, during that specific evening window. This made the underlying bug look, at first glance, like test flakiness tied to a particular machine, when it was in fact a completely real and reproducible defect that the automated gate could never have caught, because the gate's own uniform environment happened to match the code's incorrect assumption.

The general rules: first, whenever code compares a freshly-computed "now" against a stored date, the timezone in which that stored date was originally authored is part of its implicit schema — pick one clock (and one timezone convention) and use it consistently on both the reading and writing side. Second, a test whose expected value is computed using a DIFFERENT clock or timezone convention than the implementation under test is not actually testing that implementation's correctness — it's only testing that the two clocks happen to agree in whatever environment the test happens to run in. Third, and most broadly: a uniform, clean continuous-integration environment (one timezone, one locale, a fresh checkout every time) systematically hides an entire class of bugs — timezone-, locale-, and environment-path-sensitive behavior — that only ever bite a human on a real, differently-configured machine. A green automated gate is not evidence of correctness for this class of behavior; it only proves the code works in the one environment the gate happens to run in.
