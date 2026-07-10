---
title: A sliding-window leak guard's real coverage floor is window + step − 1, and zero-width characters defeat naive normalization
date: 2026-07-06
category: guardrails
tags: [llm-output-guard, shingle-detection, coverage-math, zero-width-evasion, false-positives, security-review]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When a prompt-leak guard is rebuilt from keyword matching to sliding-window "shingle" detection — checking a model's output for verbatim overlapping spans of the protected text — the rebuild has its own failure modes, and two of them survived adversarial review rounds after the keyword-matching facade itself was already fixed (that earlier lesson is its own entry in this journal).

What happened, round two: the shingle guard's window stepped through the protected text at a stride greater than one. That leaves unaligned-offset blind spots — the true minimum leaked-substring length the guard is *guaranteed* to catch is window size + step − 1, not the window size alone. A reviewer computed the coverage floor instead of trusting the design's stated span, and found leakable gaps. Round three: shingling the *entire* prompt, including user-supplied data, made the guard flag a user legitimately echoing back their own input as a "leak" — protected instructions and user data must be separated before matching. And a separate evasion: a common regex whitespace class does not match zero-width Unicode characters, so an attacker could splice invisible characters between letters and sail past text normalization entirely.

How to apply: when you ship a sliding-window detector, compute the real coverage floor (window + step − 1) and use step = 1 wherever full coverage matters. Shingle only the text that must never appear in output — never user-supplied content, or legitimate echo becomes a false positive. Normalize with an explicit invisible-character strip (zero-width space, joiner, non-joiner, BOM) before matching, because \s-style classes do not include them. And re-review the rebuilt guard as a new claim: each fix round here was broken by the next review round until the math, the scoping, and the normalization all held simultaneously.
