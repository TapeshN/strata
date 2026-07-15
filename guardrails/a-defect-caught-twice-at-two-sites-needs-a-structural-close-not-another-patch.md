---
title: A defect class caught twice at two different sites needs a structural close, not another point patch
date: 2026-07-12
category: guardrails
tags: [gating, determinism, ci]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Three unrelated pieces of work in one review cycle each burned several rounds chasing the same shape of defect at a new location every round — an escaping/sanitization gap that resurfaced at a different call site each pass, a cache-invalidation miss that resurfaced at a different write-site of the same gating field each pass, and a process-lock defect that resurfaced in a new form each pass. Patching each new instance individually never converged; a fresh finding kept appearing at the next site.

The fix that closed each one for good was structural: route every instance through a single choke point (one shared function every call site must use) or state a single invariant the code must obey, and back it with a mechanical guard — a source-scan or lint-style test — that fails the moment a new site bypasses the choke point. The crucial refinement is that the guard itself has to match the shape of the defect rather than enumerate known instances: a guard that lists specific field or variable names is still whack-a-mole, because it misses the same defect appearing under an unlisted name at an unswept site. Verify a new guard by testing it against an unknown name or location, not only the one that prompted it.

The general rule: when a review's second finding is the same class as its first finding at a different location, treat the repetition itself as the signal. The correct response is not another point patch but a single choke point or invariant plus a mechanical, shape-matching guard test that keeps the class closed going forward.
