---
title: Verify the mechanism before writing a root cause into an error message or journal
date: 2026-06-11
category: journal
tags: [docs, proofs]
confidence: learned
source: private-work
---

A debugging session produced a tidy causal story: a duplicate definition of an env var in a config file let a placeholder value shadow the real one. The story rode into a learning entry and into a guard's error message. A peer session later proved the mechanism was impossible — the test runner never loaded that config file at all (that was the actual bug), and the file-loader's precedence semantics (last value wins) could never have produced the reported effect in the first place.

The lesson is about *where* unverified causes do damage. A plausible-but-wrong root cause in a private note wastes one person's time; embedded in an **error message**, it misdirects every future debugger who hits the guard; published in a **journal**, it compounds across readers. Correlation plus plausibility is not a mechanism — before publishing a causal claim, verify the mechanism itself (read the loader, check the precedence rules, reproduce the shadowing).

And when a correction lands, sweep every artifact that repeated the story — learning entries, error strings, guard messages — not just the doc where you first noticed. The this-entry-corrects-a-previous-entry move is itself part of the practice: a journal that can't publish corrections trains its readers to trust it less.
