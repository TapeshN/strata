---
title: A claim about what a network layer sends or blocks must be witnessed on the real path — a probe that can't reproduce the exact condition, or a read of the proxy's source, both lie
date: 2026-08-22
category: guardrails
tags: [verification, security, probes]
confidence: learned
source: private-work
implementation_target: shared-prompts
---

Two related failures surfaced while verifying an origin-bound access check behind a reverse proxy. First: an in-container probe sent every possible header shape to test the check, including the theoretically correct one, and got refused every time — reading as "the gate is broken." The actual cause was the HTTP client library itself silently dropping a caller-set forbidden header before the request ever left the process, so the probe never sent what it claimed to send; the health endpoint and the probe were both telling the truth about two different requests. Re-probing with a client that can't rewrite that header showed the binding was correct all along.

Second, and separately: whether the real reverse-proxy in front of the service preserves that header and adds the standard forwarded-header fields was a fact that had to be observed by making one real request through the live proxy after cutover — with a rollback ready — not derived by reading the proxy's own source or documentation.

General rule: before concluding a gate "refuses X" or a proxy "sends Y," prove the request you're reasoning about was actually sent as claimed — echo it back, or use a client that structurally cannot rewrite it — and for anything mediated by infrastructure you don't control end-to-end, make the first real request through the live path the decisive evidence, with a rollback already staged.
