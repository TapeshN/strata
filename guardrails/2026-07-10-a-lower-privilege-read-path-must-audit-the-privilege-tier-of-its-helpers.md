---
title: A new lower-privilege read path must audit the privilege tier of every helper it calls, not just the scoping of its own queries
date: 2026-07-10
category: guardrails
tags: [security, access-control, boundaries, isolation, ai-authored-code, independent-review]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A new client-facing aggregation endpoint scoped all of its own database queries correctly by tenant and by the requesting client. It then called a shared helper function whose only prior caller was an owner-gated internal admin view. That helper returned a tenant-wide row of free-text operational telemetry — internal routing labels, work-item references, and identifiers naming other clients' projects — and the new endpoint rendered a field from that telemetry to every client who called it. Full automated verification (type-checking, linting, and over a thousand passing tests) was green, and a manual diff review missed it. Only a standing independent adversarial review focused specifically on the client-facing data boundary caught the leak.

The reason this is invisible to normal review is structural: correctness review naturally checks the NEW code's own logic — did it scope its own queries, did it handle its own inputs — but a helper function imported from elsewhere carries an implicit privilege assumption inherited from whoever called it first. A helper that was always safe to call from an owner-only surface is not automatically safe to call from a client-facing one; nothing about the helper's own code changes, but the caller's privilege tier is now lower, and no compiler, linter, or type system tracks "the privilege level of my caller" as a property that must match.

The generalizable rule: when building any new read path at a LOWER privilege tier than paths that already exist in the codebase, enumerate every helper function it imports and ask, for each one, "who called this before, and were they gated at a higher tier than I am?" A helper's safety is a property of its callers, not of itself, so it must be re-audited every time a new, lower-tier caller is added. When a leak like this is found, the fix should remove the unsafe read entirely rather than filter its output after the fact — that way the regression test can assert non-callability of the sensitive helper from the low-tier path, which is a durable structural guarantee, rather than asserting non-rendering of a specific field, which is fragile to the next unrelated change in that helper's output shape.
