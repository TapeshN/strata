---
title: A structural explanation is not a witness
date: 2026-08-09
category: guardrails
tags: [witness-discipline, verification, hitl]
confidence: hypothesis
source: private-work
implementation_target: agent-guardrails
---

In one observed incident, a claim that a UI now displayed a set of expected values was accompanied by a correct structural explanation for why a lower-level check couldn't see them — the values flowed through a different internal path than the one being probed. The explanation was accurate and resolved the immediate confusion, but it substituted for evidence: nothing was actually witnessed rendering the claimed values, and an independent verification step correctly rejected the claim as unproven. The distinction worth carrying forward is that explaining why a probe can't see something is a different act from running a probe that can. Where the rendering layer genuinely isn't reachable, the honest fallback is to run the narrowest path that is verifiable (the underlying test suite, run verbosely, with its own named assertions) and to scope the claim to exactly what that path proves — not to the broader claim the explanation was defending.

This is flagged as hypothesis rather than learned because it rests on a single incident, though it rhymes with a broader, independently-observed pattern that reasoning about a verification path is not the same act as running it.
