---
title: Refactoring a hardcoded security constant into an overridable parameter moves enforcement from the type system to the caller
date: 2026-07-01
category: guardrails
tags: [security, contracts, layering, cost]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A shared UI component was extracted so two call sites could reuse one implementation. In the process, a hardcoded security-relevant constant that had previously been baked directly into the component became an optional parameter with a safe default. Both existing call sites passed the safe value, so every automated check and an initial manual review passed cleanly — a second, independent adversarial review caught it.

The underlying issue: as a hardcoded constant, the value was enforced by the type system — there was no way to pass an unsafe one without changing the component's source. As an optional parameter, it became enforced only by caller discipline — safe purely because every caller today happens to choose the safe value, with nothing stopping a future caller from passing an unsafe one with no compiler, lint, or test signal at all. A clean build and green tests only prove the code compiles and current behavior is as expected; neither proves that a security invariant is still enforced by construction rather than by convention.

The general rule: any time a refactor turns a hardcoded, security-relevant value into a prop, parameter, or config option — even when every current caller passes the safe value — treat that specific diff as high-scrutiny, because the risk is about future callers, not the current ones. Where possible, prefer a closed type that structurally cannot represent the unsafe value, or omit the override entirely, over an optional parameter with a "safe by convention" default. This is also a concrete case for why a second, independent adversarial reviewer earns its keep on security-adjacent changes — the automated pipeline and the first manual pass both went green on exactly the change that introduced the regression.
