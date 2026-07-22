---
title: An unauthenticated health-check endpoint needs the same rate limiting as any public route
date: 2026-07-17
category: guardrails
tags: [security, throughput, cost, gating]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

"It's just a health check" is not a security exemption. A new uptime-probe endpoint that performs a real backend round-trip (a database query against the shared connection pool, even a trivially cheap one) is, from an abuse-resistance standpoint, indistinguishable from any other public route that touches a shared resource: an anonymous flood of requests against it is a lever on shared pool/connection capacity, and enough concurrent load can degrade authenticated traffic elsewhere in the same application. Type-checking, unit tests, and a production build are all blind to resource-pool contention under load — none of them simulate concurrent traffic — so this class of gap survives ordinary automated verification and is only caught by an adversarial review asking "what happens if this is hit thousands of times a minute by someone with no credentials."

The tell that should catch this before review does: check whether the new route follows the SAME defensive pattern every other public, resource-touching route in the codebase already follows. If every other unauthenticated route that reaches a shared resource applies rate limiting before the resource hit, and the new one doesn't, that asymmetry is the finding — a route added later, by a different author or a different session, drifting from an established pattern rather than deliberately deviating from it.

**The general rule:** before shipping any new unauthenticated route, grep how the codebase's existing unauthenticated routes defend themselves (IP-based rate limiting, a request cap with a retry-after response, or similar) and match that pattern by default, rather than treating a new route's "smallness" or "obviousness" as license to skip it. Keep an independent adversarial security review as a standing gate for any change that adds a new externally-reachable endpoint — this class of finding is exactly the kind that automated tooling does not catch and a reviewer looking for abuse cases does.
