---
title: Prove a green witness by making it go red — a check that can't fail validates nothing
date: 2026-06-20
category: guardrails
tags: [gating, determinism, evals, proofs]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A gate that reports clean was invoked with the file path as a positional argument; the gate reads from standard input and silently ignored the argument, scanning empty input and reporting clean. Two problems collapsed into one green verdict: the gate was not exercising the intended input at all, and the scope of "clean" was narrower than assumed (the gate checks for proprietary identifiers, not for all information that should be stripped before publication).

The repair has two steps. First, re-invoke with input piped through standard input to confirm the gate actually processes the content. Second, run a positive control: supply a known-bad input and confirm the gate exits with a non-zero code. A gate that cannot be made to fail is not exercising the right property, is not receiving the right input, or is not scoped to the hazard you believe it covers.

This is a specific instance of the general principle: a green witness that has never been observed going red is not evidence of safety — it is evidence that the witness might not be working. Before trusting any gate's clean verdict, plant a failure deliberately. The positive control costs one extra invocation and closes the entire class of "the gate passed but measured nothing" defects.

The corollary is that scope matters: a gate's clean verdict certifies only what the gate is specified to check. A scrub gate that validates proprietary identifier absence does not certify that the content is ready for public publication; paraphrase quality is a separate human judgment. Name what a gate certifies, not what you hope it certifies.
