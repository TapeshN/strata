---
title: Five privilege-escalation classes that build tests passed and adversarial review caught
date: 2026-06-16
category: guardrails
tags: [security, owasp, stride, adversarial-review, access-control, fail-closed, payment, rate-limiting]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

An independent adversarial security review of a payment and access-control surface, applied after all build and unit tests were green, surfaced five classes of privilege escalation. None were caught by the prior test suites because each required reasoning about the failure path — the code path the author did not write tests for.

The five generalizable classes:

**Access gates that fail open.** A catch-all exception handler that swallows access errors and continues into protected code is not a gate — it is a scheduled bypass. Any catch block in an access-control path must default to the most restrictive outcome (deny, redirect, return 403) and log. Never let a catch clause silently skip the redirect.

**Client-supplied price or plan identifiers must be server-validated.** A checkout endpoint that accepts a price or plan identifier from the client and passes it directly to a payment provider allows a client to substitute any valid-looking identifier from the provider's catalog. Validate client-supplied price IDs against a server-side allowlist derived from environment configuration before calling the provider. An unknown identifier must error, never proceed.

**Redirect targets passed to a trusted third party must be same-origin validated.** When a return or redirect URL is supplied by the client and then handed to a trusted external service, the trusted service's domain elevates the redirect's authority. A redirect through a payment or identity provider is a high-trust open redirect. Validate the return URL for same-origin membership before forwarding it.

**Metering quota checks must surface over-quota responses, not swallow them.** A pattern of check-before, record-after for rate-limited expensive operations must propagate the over-quota signal (for example, 402) from the recording step. Swallowing it runs the operation without charging the quota — a cost-abuse window that widens under concurrency.

**Two-phase lazy-reset: the initial read must be inside the locking transaction.** A period-boundary reset that reads current state, then resets to zero inside a transaction is vulnerable to a concurrent increment between the read and the transaction. The read must move inside the transaction boundary (`SELECT ... FOR UPDATE`) so the increment is serialized.

These classes share a structure: the happy-path tests pass because they never exercise the error branch, the substitution, or the race. Catching them requires an adversarial framing — assume the attacker is trying to abuse the path — not a correctness framing.
