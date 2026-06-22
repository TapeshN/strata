---
title: Access-control gates must fail closed; client-supplied tier identifiers must be allowlist-validated server-side
date: 2026-06-20
category: guardrails
tags: [security, access-control, owasp-a01, owasp-a04, fail-closed, stride-elevation]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

An adversarial OWASP pass on five "green" (build + unit tests passing) monetization PRs found
two classes of access-control failure that CI and author tests are structurally blind to:

Class 1 — fail-OPEN error paths in access/tier gates: a catch-all exception handler in a tier
check caused it to fail open — on any error the user passed through to a paid-tier resource.
The fix: on any error inside an access gate, default to the MOST RESTRICTIVE outcome and log;
never let a catch block skip an access redirect. The test for correctness: deliberately inject an
error condition and assert the gate denies access, not grants it.

Class 2 — client-supplied tier/price IDs not validated server-side: a checkout flow accepted
a client-supplied price ID and forwarded it to the payment provider without checking it against
a server-side allowlist of known-valid price IDs. An attacker supplying an unknown or lower-tier
price ID could bypass pricing. The fix: validate the client-supplied ID against a server-derived
env-loaded allowlist BEFORE calling the payment provider; an unrecognized ID must error, never
fail-open to a paid tier.

Both classes share a root: the access/quota gate was written to handle the happy path correctly
but had no negative probe — the test confirmed the allowed user got in; nothing confirmed the
denied user stayed out under adversarial conditions (injection, error, unknown IDs).

Rule: for every access-control or tier-gate, the mandatory test set includes at minimum one
negative probe (error injection / unknown-ID / denied-user) that asserts the MOST RESTRICTIVE
outcome. Without the negative probe, the gate is unverified.
