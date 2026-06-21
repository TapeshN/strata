---
title: Money, auth, and security surfaces require two independent adversarial reviewers before merge
date: 2026-06-20
category: guardrails
tags: [security, adversarial-review, auth, billing, double-verification]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

On any change that touches billing, authentication, quota enforcement, or externally-reachable
endpoints, a single author-written test suite plus one reviewer is structurally insufficient:
the test suite encodes the author's mental model and is blind to the author's blind spots; the
first reviewer tends to share the same mental frame as the author.

Two incidents on the same codebase: (1) an adversarial 6-way review wave found an anonymous,
unmetered, uncapped LLM-judge path — a live cost-abuse hole — on a slice that had already been
through one OWASP hardening pass and had green CI; neither the author's tests nor the first
reviewer caught it. (2) A separate adversarial pass on five "green" (tsc/eslint/vitest PASS)
monetization PRs found three bugs the builders' own suites passed: a cache-token ledger that
systematically under-charged, an unchecked slug parameter enabling cross-challenge access, and
a webhook catch returning 200 for all errors including transient DB failures (suppressing Stripe
retries, silently leaving paid users on free tier).

The mechanism that caught both: cross-referencing two independent reviewers with DIFFERENT lenses
(build-correctness + OWASP-adversarial, or a cost-surface reviewer + an auth-surface reviewer).
The highest-value bug in each case lived in the seam between two reviews — invisible to each reviewer
alone, visible in their cross-product.

Rule: before merging any change that touches money, auth, quota, or security surface, budget for
two independent adversarial reviews with deliberately different lenses and cross-reference their
findings. This is not overhead — it is the mechanism that prevents shipping exploitable paths.
