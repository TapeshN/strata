---
title: A "must never contain this exact code" test failed because a code comment, not the code, contained the forbidden text
date: 2026-09-10
category: evals
tags: [source-text-assertion, matched-own-comment, positive-control]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

Two separate source-level "this file must not contain X" assertions failed even though the underlying fix was correct. In one case, the assertion was written against the general form `request.json` — meant to forbid an unwanted usage — but the actual, exact call form the code correctly used was `request.json()`, and the explanatory comment sitting right next to the fix also happened to name that same call form in prose, which is exactly what the substring check matched against. In the other case, an unrelated "no hard-coded literal" assertion failed on a code comment written earlier that happened to contain the literal being banned. Both gates were doing a plain text search over the whole file, including comments, so whether they passed or failed came down to a coin flip based on nearby prose rather than anything about the code's actual behavior.

Fix at the source: assert against the precise call form being illustrated — including exact syntax such as the closing parentheses of a function call — rather than a loose substring that a comment can also satisfy; or, when the positive assertions in the same test already prove the fix, drop the negative "must not contain" assertion entirely rather than keep a coin-flip check around. Every such assertion should carry its own positive control: temporarily revert the fix, confirm the test goes red for the right reason, then restore it.

General rule: a source-text "must not contain" assertion, run against a file that also legitimately contains comments discussing the very thing being forbidden, is unreliable by construction. Write the assertion against code shape, not prose, and control it with a deliberate, temporary regression.
