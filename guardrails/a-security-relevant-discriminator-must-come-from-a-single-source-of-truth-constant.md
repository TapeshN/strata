---
title: A security- or money-relevant discriminator value must come from a single source-of-truth constant, never a re-typed literal
date: 2026-07-21
category: guardrails
tags: [security, owasp-a04, maintainability, testing]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A code review found a filter that gates which records a query returns — a status or kind value with real security or ownership consequences — written as a re-typed string literal instead of importing the single exported constant the rest of the codebase already used for that same value. The risk isn't hypothetical: if that constant's underlying value is ever renamed or changed, the hand-typed copy silently stops matching, the gate quietly matches nothing, and every caller falls through to whatever the pre-gate default behavior was — reintroducing exactly the bug the gate was built to prevent. Worse, if the accompanying test also hardcodes the same literal instead of importing the constant, the test stays green through that exact failure.

**The rule:** any discriminator value with security, ownership, or money consequences must be imported from its single exported constant everywhere it's used, never re-typed — and its tests must assert against the imported constant too, not a duplicated literal, so a rename is caught rather than silently tolerated by both the code and its own test.
