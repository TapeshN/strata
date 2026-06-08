---
title: Recon and suggestion agents are not specification-aware; cross-reference the spec before acting on their suggestions
date: 2026-06-02
category: guardrails
tags: [roles, autonomy, verify-dont-trust, contracts]
confidence: learned
source: private-work
---

A read-only recon or UX-suggestion subagent will recommend plausible improvements without consulting the project's intentional specification — a bug catalog, an acceptance-criteria list, or a set of intentionally-planted behaviors. A suggestion that "fixes" a confusing UI element may inadvertently remove a behavior that is intentionally present.

In a concrete case, a recon agent suggested making a UI element a navigating link. Reading the specification revealed the non-navigation behavior was intentional — the element was designed to exhibit a specific interaction bug. Accepting the suggestion would have masked the planted behavior.

Prevention: agents editing code that has an associated specification must cross-reference that specification before making changes. A "fix" must be verified not to mask or remove an intentional behavior. Subagent suggestions are UX/structure observations, not spec-aware verdicts.
