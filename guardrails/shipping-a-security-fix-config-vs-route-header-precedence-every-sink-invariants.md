---
title: Shipping a security fix: config-vs-route header precedence, every-sink invariants, and adjudicating a split verdict
date: 2026-07-18
category: guardrails
tags: [security, owasp-a03, owasp-a05, nextjs, csp, header-precedence]
confidence: learned
source: private-work
---

Three lessons from shipping one security fix. (1) Framework config-level headers can REPLACE per-route response headers — a per-response CSP is dead code unless the global config carries it too; verify security headers on the wire, never in source alone. (2) A security invariant must be enforced at EVERY sink that can violate it, not only the sink where the bug was found — enumerate the sinks first, then declare the fix complete. (3) When independent reviewers split on a verdict, the adjudicator reads the code and decides on evidence — never counts votes.
