---
title: A security guard labeled "structural" that is actually keyword matching is a facade — it inherits every weakness of substring filters and only an adversarial run against real output variation reveals it
date: 2026-07-06
category: guardrails
tags: [llm-output-guard, prompt-injection, facade, structural-not-substring, double-verification]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A guard built to stop a language model from leaking its own system instructions in its visible reply was first implemented as a fixed list of marker phrases to detect in the output. It was labeled a structural safeguard, but an independent adversarial reviewer who actually ran the code — rather than reading it — broke it in seconds: inserting a line break or wrapping a phrase in markdown emphasis made the exact same leaked content sail past the detector, because a fixed-phrase check only matches the literal strings a developer happened to type, not the many surface variations a model can produce.

The rebuilt version compared verbatim spans of the actual secret text using a sliding window, which is a real improvement but still failed an adversarial pass on two more subtle points. First, the sliding window's step size left a gap in its guaranteed coverage — a leaked span shorter than window-size-plus-step-minus-one could slip through an unaligned offset; the fix was to shrink the step to its minimum so the guaranteed catch floor actually matches the intended window size. Second, matching spans across the entire prompt — including the portion that echoes a user's own submitted data back to them — caused the guard to also block a user's legitimate reuse of their own words; the fix was to shingle only the static, secret instruction text and exclude the dynamic user-supplied portion from the comparison. A separate self-caught gap was that a common invisible Unicode character was not treated as whitespace by the normalization step, so it could be used to silently break up an otherwise-detectable match.

The general lesson: any claim that an output-side guard is "deterministic" or "structural" must be proven by running it against realistic output variation the underlying model can actually produce — different phrasing, formatting, whitespace, and invisible characters — not just the exact strings a developer wrote while building it. A sliding-window detector's true guaranteed catch floor is window-size plus step size minus one, so the step should default to the smallest value performance allows. And any guard built from a larger block of text that includes user-supplied content must separate the fixed secret material from the dynamic user data before comparing, or it will produce false positives against legitimate use.
