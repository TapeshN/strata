---
title: A legacy wildcard credential must be re-evaluated every time a new capability is added to a closed registry
date: 2026-08-22
category: guardrails
tags: [security, gateway]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A capability registry treated an old, broadly-scoped shared credential as a wildcard holder — granted whatever new capability got registered, by design, since it predated the fine-grained model. Adding a new, sensitive capability (access to raw recorded audio) to the registry silently extended it to that legacy credential too, a data class nobody had reviewed for that credential's exposure. Compounding it, the plan to eventually retire routes gated only by that legacy credential's presence could never actually fire, because "principals only" was unreachable while the wildcard still existed.

General rule: data-access-sensitive capabilities should be wildcard-ineligible by construction — express wildcard grants as a deny-set that new sensitive capabilities are added to by default, not as an allow-everything grant that silently absorbs anything registered later. And any "we'll retire this once nothing needs it" plan should key its readiness check on "does any principal actually need this capability," never on "does the legacy secret still exist" — the two conditions can diverge indefinitely.
