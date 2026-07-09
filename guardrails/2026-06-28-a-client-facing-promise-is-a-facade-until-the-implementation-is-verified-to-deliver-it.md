---
title: A client-facing promise is a facade until the implementation that generates the artifact is verified to deliver it
date: 2026-06-28
category: guardrails
tags: [contracts, determinism]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

A team writing both a client-facing promise (marketing or onboarding copy describing what a feature does) and the implementation that produces the underlying artifact can end up with the two halves silently contradicting each other, because they were authored as separate steps with no step that checks one against the other. In one case, the copy promised a genuinely interactive, clickable output, while the generation instructions actually in force explicitly produced a static, non-interactive result — both halves were written by the same team in the same effort, yet neither was checked against the other.

A green build, a passing test suite, and even a coherent-looking piece of copy all say nothing about whether the *specific claim* made to an end user is actually true of the artifact they will receive. This is the same class of failure as any other facade: a claim that reads as complete but is not causally bound to the reality it describes.

The fix is procedural: any time a team writes a client-facing promise about what a generated or built artifact does, that promise should immediately be checked against the actual generation path — regenerate a real sample and confirm the specific claim holds, or soften the copy to what the implementation genuinely delivers. Treat marketing and onboarding copy as a testable claim about the product, not as decoration that exists independently of the build.
