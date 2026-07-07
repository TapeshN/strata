---
title: An optional local-model enhancement must fail closed to a human fallback, never to a paid cloud path, and gate on live reachability rather than static configuration
date: 2026-07-06
category: guardrails
tags: [no-egress, fail-closed, human-fallback, cost-safety, blast-radius]
confidence: learned
source: private-work
implementation_target: agent-guardrails
---

When a feature is enhanced by an optional local-model dependency (for example, a locally-hosted language model that a client-facing chat feature calls when available), three properties keep that dependency from becoming a liability if it goes offline. First, the critical path of the surrounding product must stay structurally independent of the local dependency — a chat feature can be optional, but authentication, the primary database, and other core functionality must not depend on the same host. Second, on failure, the feature must degrade to a cheap, safe fallback — a clear message that a human will follow up, or an equivalent low-cost path — and must never silently fail over to a metered, paid alternative that was never intended to bear that traffic. Making that impossible in code (not just in configuration) is stronger than a runtime toggle: if the enhanced code path structurally has no reference to the paid alternative, a misconfiguration cannot route traffic there by accident.

Third, and easy to get wrong, is how the system decides the dependency is unavailable. A naive approach waits for a live request to the dependency to time out before falling back, which means every user during an outage experiences a slow failure before finally seeing the fallback message. A better approach maintains a short-lived, cheap, cached reachability probe (a few seconds of staleness tolerance is fine) so the system already knows the dependency is down and can return the fallback state immediately and cleanly, rather than discovering it mid-request. The general principle: an optional dependency's failure mode should be fast, cheap, and to a safe state — never slow, never expensive, and never a stealth escalation to infrastructure that wasn't budgeted for that traffic.
