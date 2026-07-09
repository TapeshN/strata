---
title: Deferring a tier or paywall feature must not be read as license to drop the orthogonal per-scope authorization check
date: 2026-07-02
category: guardrails
tags: [boundaries, roles]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A worker given an instruction along the lines of "any authenticated identity may submit any item for now, since the paid tier isn't built yet" read that as license to remove the per-scope authorization check on the submission path entirely — not just the tiering/paywall logic. The result was a route that would score and return detailed, scored feedback for any scope an authenticated caller chose to request, regardless of whether that caller was actually authorized for that specific scope: an authorization bypass introduced by a feature-deferral instruction that never meant to touch security at all.

Tiering ("which paid plan unlocks which volume or feature") and per-scope authorization ("is this caller allowed to access this specific resource at all") are two entirely different axes, and an instruction that legitimately defers one must never be read as license to weaken the other. The ambiguity is easy to introduce precisely because both can be phrased using similar words like "access" or "allowed."

The generalizable practice: when specifying any deferral of a feature — especially one phrased as "no restriction yet" — explicitly name which existing security controls must remain untouched, rather than trusting that the reader will infer the boundary between "deferred feature" and "removed control." Any change to an authorization or scoping check, however incidental it looks relative to the stated task, warrants the same independent adversarial review as a deliberate security change.
