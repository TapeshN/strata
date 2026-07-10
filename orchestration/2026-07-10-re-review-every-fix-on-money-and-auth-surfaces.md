---
title: Re-review every fix on money and auth surfaces, not just the original code
date: 2026-07-10
category: orchestration
tags: [security-review, double-verification, adversarial-testing, money-surfaces, auth-surfaces]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

**Rule:** On any surface that touches money, authentication, or capability grants, one clean adversarial review is not sufficient evidence of safety — treat each fix as a new claim that needs its own independent refutation, and only stop once successive rounds converge (findings shrinking in severity), not after a single pass reports zero issues.

**What happened:** A team ran four independent adversarial security reviews, one after another, against a single money-related control path (a spend-limiting kill-switch). Each reviewer found a distinct, reproducible way to bypass the control — severities ran CRITICAL, then HIGH, then HIGH, then MEDIUM — and each of those bypasses was invisible to the standard automated checks: type checking, linting, and continuous-integration test suites all passed cleanly throughout. Critically, every time a bypass was fixed, the fix itself was sent back through a fresh adversarial review rather than accepted on the strength of the fix having "addressed the reported issue." Had the team stopped after the first review — the common practice of "one reviewer signs off, ship it" — the CRITICAL-severity bypass would have shipped to production, and none of the automated tooling would ever have caught it.

**How to apply:** If you are shipping code that gates spend, grants access, or checks capabilities, do not treat a single passing review (human or automated) as proof of safety — these are exactly the surfaces where an attacker gets to choose the input, and standard build/test tooling is not built to think adversarially. Instead, run multiple independent reviews, and re-review each fix as though it were a brand-new, unverified claim, not a patch that closes the loop. Use the trend across rounds as your stopping signal: if each new round finds fewer and lower-severity issues than the last, you're converging on safe; if a new round keeps finding fresh high-severity issues, you're not done, no matter how many rounds have already passed.
