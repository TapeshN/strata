---
title: A completeness/disclosure CI gate must prove render-direction AND enumerate from source, and must scope its own claims honestly
date: 2026-07-19
category: guardrails
tags: [ci, gating, evals, completeness]
confidence: learned
source: private-work
implementation_target: infra-tooling
---

A gate meant to catch undisclosed data flows rendered a page and checked that every item already named in a registry appeared on it — which only proves the registry-to-page direction (whatever's registered gets shown), not the direction that actually matters (whatever the code actually does gets registered). A source-level enumeration of every real call-site is required to catch an entry that was never registered in the first place. Separately, a gate that strips code comments in one of its checks but not in a sibling check let a commented-out import satisfy a "not hand-typed" test; and a gate keyed to one specific call syntax (a particular function-call shape) is blind to the same effect achieved through a direct constructor or factory call.

**The rule:** a completeness-style gate must (1) enumerate from the actual source of truth, not merely check that whatever's already declared is rendered correctly, (2) apply the same normalization (e.g. comment-stripping) consistently across every raw-text check it runs, and (3) either handle every real syntactic form that achieves the same effect, or state its actual scanned scope honestly rather than implying total coverage.
