---
title: A stays-local network guard that checks the provider's name or a reachability flag, not the actual resolved destination, is defeated by config pointed at a public host wearing a local-sounding label
date: 2026-07-06
category: guardrails
tags: [no-egress, ssrf, toctou, destination-not-name, safety-gate, double-verification]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

A guard meant to guarantee that a component only talks to a local, non-egressing service is only as strong as what it actually inspects. A guard that validates a provider's declared name, or simply that a health probe succeeded, can be satisfied by a configuration value that names itself "local" while its underlying address resolves to an arbitrary public host that also happens to answer the probe. In that shape, the guard passes while the real traffic — including sensitive request content — leaves the machine entirely, which is exactly the outcome the guard exists to prevent. The correct check validates the resolved network destination itself: is it loopback, a private address range, or a link-local address, with cloud metadata-service addresses explicitly rejected and any non-"localhost" hostname refused.

A second, independent failure mode compounds the first: if the guard's validation happens once at setup time but the component re-reads a mutable configuration value at the moment it actually makes a call, something can change that value in between — reopening exactly the check-then-use race the guard was meant to close. The fix is to resolve and validate the destination exactly once, then capture that validated value and thread it directly into whatever performs the call, so there is no later re-read of a value that could have drifted since validation. Both failure modes were only caught by a deliberately adversarial, independent review of a guard that had already passed its own author's testing — a reminder that a security-shaped guard benefits from a second, skeptical reviewer specifically hunting for what the guard checks versus what it actually needs to guarantee.
