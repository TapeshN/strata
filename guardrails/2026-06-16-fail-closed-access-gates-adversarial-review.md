---
title: Fail-closed access gates: why passing tests don't catch privilege escalation
date: 2026-06-16
category: guardrails
tags: [security, access-control, fail-closed, code-review, testing]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Access-control and tier-gating code that uses a catch-all error handler to "fail open" is not actually a gate — it is a scheduled bypass waiting for the right exception. The general rule: any authorization check must fail CLOSED. On any unexpected error, exception, or unhandled branch, the default outcome must be the most restrictive one (deny, redirect, block) and the failure must be logged — never silently allowed through.

What happened: a security review of several stabilized monetization features found that a tier/access-control check had a catch-all exception handler which, on error, let the request continue instead of redirecting to a denial page. The build compiled cleanly and 250+ unit tests passed, because the unit tests exercised the happy path and the expected error path, but none of them simulated the specific runtime condition that hit the catch-all. An independent adversarial review — deliberately trying to break the gate rather than confirm it works — found two separate places where an unhandled edge case fell through to "allow" instead of "deny." This is a structural blind spot: tests written by the same person/process that wrote the gate tend to validate the gate's own assumptions, so they can't catch a bug in those assumptions. A second, adversarial reviewer with a different mental model is what catches it.

How to apply: audit every access-control, tier-check, and quota/rate-limit gate in your codebase for what happens on the exception path, not just the success and expected-failure paths. Rewrite any catch-all handler so the fallback is "deny and log" rather than "continue." Then, before shipping anything auth- or payment-adjacent, get a second reviewer (or a dedicated adversarial pass) whose explicit job is to try to bypass the gate, since "tests pass" only proves the gate works the way its author already believed it worked.
