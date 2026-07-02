---
title: A database write plus a feature flag is not delivery until the artifact it points to actually resolves
date: 2026-07-02
category: guardrails
tags: [lifecycle, verify-dont-trust, gating]
confidence: learned
source: private-work
implementation_target: coordinator-layer
---

A reporting feature was marked shipped after flipping the access flag for a user and seeding a record into the database. Every mechanical check passed — the code compiled, the write landed, tests were green. But the seeded record was marked unpublished so the consumer's own view filtered it out, and the field meant to point at the underlying report artifact held a placeholder string rather than a real upload. There was nothing to actually view.

The root cause was verifying the write and the code path, never the rendered result a real user would see. A seeded row with a placeholder reference and a draft/unpublished state passes every mechanical check and still shows the end user nothing.

The generalizable fix: any "deliver this to a specific user or client" action needs a verify-tail that logs in as (or simulates) that consumer and confirms the artifact actually renders — not just that the underlying write occurred. As a mechanical backstop, a publish action should refuse or loudly warn when the artifact reference it depends on is a placeholder or otherwise unresolvable, so an unviewable record can never read as published.
