---
title: A new tenant-scoped data model must be threaded through the SAME authorization resolver every sibling read already uses
date: 2026-07-21
category: guardrails
tags: [security, owasp-a01, multi-tenancy, authorization]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

Adding a new client/tenant-scoped data model and scoping its reads by tenant ID alone felt sufficient — until an adversarial security review found the codebase actually enforces a FINER-grained authorization axis on every sibling read of comparable data, one that a tenant-ID-only scope completely bypasses. The gap meant a user with a restricted or partial grant over their own tenant's data could read another tenant's full records simply by supplying a different ID, because the new model's read path never called the shared resolver every other read already goes through.

**The rule:** adding a new tenant/client-scoped model is not "add a tenant ID column and filter on it." Find the authorization resolver every sibling read in the codebase already composes, and route the new model's reads through that exact same resolver — mirroring a comparable sibling's pattern exactly (including how it AND-composes an ownership bound onto a narrower grant) rather than reinventing a simpler check that happens to look sufficient in isolation.
