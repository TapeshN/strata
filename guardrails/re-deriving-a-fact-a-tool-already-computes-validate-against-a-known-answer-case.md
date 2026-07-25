---
title: When you must re-derive a fact a tool already computes, validate it against a known-answer case before trusting it on the unknowns
date: 2026-07-25
category: guardrails
tags: [verify-dont-trust, determinism, reproducibility]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Across one session, three separate hand-rolled re-derivations of a fact that an existing deterministic tool already computed were each wrong, and each wrong in the same direction — the manual version was the LEAST trustworthy of the available readings, not a reasonable fallback. A hand-written pattern-match meant to identify which relationships would cascade on delete stopped short of the field that actually determined the behavior, so it confidently reported one uniform (and incorrect) answer for every case; a simple structural count over-counted by a large margin relative to the tool built specifically for that count; and an exact-string match against recorded titles overcounted worse than either of the other two.

The general rule: when a fact can be computed by an existing, deterministic, purpose-built tool or matcher, prefer that tool's output over reimplementing the logic by hand, even when the hand version feels quicker in the moment. If you genuinely must re-derive something — the tool is unavailable, or you are validating the tool itself — first run the re-derivation against a case whose correct answer you already know, and only trust it on the unknown cases once it reproduces the known one exactly. A re-derivation that "looks right" and was never checked against a ground-truth case is not verification; it is a second, unvalidated guess standing in for the first.
